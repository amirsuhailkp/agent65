"""Planner — the AI Brain's orchestrator. Vol III Ch2-3 (cognitive cycle),
Ch16 (state machine), Vol II Ch7.

Cycle: Observe -> Retrieve Knowledge -> Reason -> Generate Hypotheses ->
       Rank -> Decide -> Execute (Kali) -> Verify -> Update Memory -> Repeat
"""
from __future__ import annotations
from enum import Enum
from ..logging_setup import get_logger
from ..reasoning.reasoning_engine import ReasoningEngine
from .hypothesis_engine import HypothesisEngine
from .decision_engine import DecisionEngine
from .goal_manager import GoalManager
from .verification_engine import VerificationEngine
from .attack_graph import AttackGraph
from .resource_monitor import ResourceMonitor
from ..knowledge.knowledge_manager import KnowledgeManager
from ..memory.memory_manager import MemoryManager
from ..dispatcher.kali_dispatcher import KaliDispatcher
from ..reporting.evidence_collector import EvidenceCollector
from ..reasoning.impact_assessor import ImpactAssessor

log = get_logger("planner.core")


class PlannerState(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    VERIFYING = "verifying"
    UPDATING_MEMORY = "updating_memory"


class Planner:
    def __init__(
        self,
        goal_manager: GoalManager,
        knowledge_manager: KnowledgeManager,
        memory_manager: MemoryManager,
        reasoning_engine: ReasoningEngine,
        hypothesis_engine: HypothesisEngine,
        decision_engine: DecisionEngine,
        verification_engine: VerificationEngine,
        dispatcher: KaliDispatcher,
        evidence_collector: EvidenceCollector,
        resource_monitor: ResourceMonitor,
        checkpoint_interval_seconds: int,
        learning_engine=None,
        impact_assessor: ImpactAssessor | None = None,
    ):
        self.goal_manager = goal_manager
        self.knowledge_manager = knowledge_manager
        self.memory_manager = memory_manager
        self.reasoning_engine = reasoning_engine
        self.hypothesis_engine = hypothesis_engine
        self.decision_engine = decision_engine
        self.verification_engine = verification_engine
        self.dispatcher = dispatcher
        self.evidence_collector = evidence_collector
        self.resource_monitor = resource_monitor
        self.checkpoint_interval_seconds = checkpoint_interval_seconds
        # Playbook Learning Engine — optional so existing tests/wiring that
        # don't construct one keep working exactly as before (Vol II Ch11
        # extension, not a replacement).
        self.learning_engine = learning_engine
        # Deep-model escalation point — only invoked for the impact
        # judgment call (VerificationEngine's clear_impact gate), never
        # in the hot loop. Optional so callers without a second model
        # configured keep the previous (conservative) behavior.
        self.impact_assessor = impact_assessor

        self.attack_graph = AttackGraph()
        self.state = PlannerState.IDLE
        self._cycle_count = 0

    def run_cycle(self, current_goal: str, target_hint: str | None = None,
                  approve_high_risk: bool = False) -> dict:
        self._cycle_count += 1
        log.info(f"--- Cognitive cycle {self._cycle_count} :: goal='{current_goal}' ---")

        # Resource guard first — never burn GPU past safe threshold
        status = self.resource_monitor.snapshot()
        if self.resource_monitor.should_pause(status):
            self.state = PlannerState.WAITING
            self._checkpoint()
            self.resource_monitor.cooldown()

        self.state = PlannerState.PLANNING

        # 1. Retrieve Knowledge
        retrieved = self.knowledge_manager.retrieve(current_goal, top_k=6)

        # 1b. Retrieve synthesized Playbooks + real Experience (Learning
        # Engine extension) — optional, never blocks the cycle if absent
        # or if the category can't be inferred from the goal text.
        playbooks, experiences, matched_categories = [], [], []
        if self.learning_engine is not None:
            learned = self.learning_engine.retrieve_for_planning(current_goal)
            playbooks = learned.get("playbooks", [])
            experiences = learned.get("experiences", [])
            matched_categories = learned.get("categories_matched", [])

        # 2. Reason
        result = self.reasoning_engine.reason(
            current_goal=current_goal,
            scope={
                "program": self.goal_manager.program_name,
                "in_scope": self.goal_manager.in_scope,
                "forbidden_techniques": list(self.goal_manager.forbidden_techniques),
            },
            working_memory=self.memory_manager.working.to_dict(),
            retrieved_knowledge=retrieved,
            active_hypotheses=self.hypothesis_engine.active(),
            available_tools=self.dispatcher.registry.schema_summary(),
            resource_status=status,
            relevant_playbooks=playbooks,
            relevant_experiences=experiences,
        )

        if result.get("error"):
            log.warning(f"Cycle {self._cycle_count} aborted: {result['error']}")
            self.state = PlannerState.IDLE
            return {"cycle": self._cycle_count, "aborted": True, "reason": result["error"]}

        # 3. Generate + rank hypotheses
        self.hypothesis_engine.ingest(result.get("hypotheses", []))
        ranked = self.hypothesis_engine.rank()
        top = ranked[0] if ranked else None

        # 4. Decide
        decision = self.decision_engine.decide(
            next_action=result.get("next_action"),
            target_hint=target_hint,
            top_hypothesis_id=top.id if top else None,
        )
        if not decision:
            self.state = PlannerState.IDLE
            return {"cycle": self._cycle_count, "decision": None}

        if decision.requires_approval and not approve_high_risk:
            log.info(f"Decision requires human approval: {decision.tool} ({decision.reason})")
            self.state = PlannerState.WAITING
            return {"cycle": self._cycle_count, "pending_approval": decision.__dict__}

        # 5. Execute
        self.state = PlannerState.EXECUTING
        if top:
            self.hypothesis_engine.mark_testing(top.id)

        exec_result = self.dispatcher.execute(
            tool_name=decision.tool,
            params={"target": target_hint or "", **decision.params},
            approved=approve_high_risk,
        )

        # 6. Collect evidence
        evidence_id = self.evidence_collector.record(
            task_id=None,
            hypothesis_id=None,
            endpoint=target_hint,
            request=None,
            response=None,
            tool_output=exec_result.stdout or exec_result.stderr,
            planner_reasoning=decision.reason,
            confidence=top.confidence if top else 0.0,
        )

        # 7. Verify
        self.state = PlannerState.VERIFYING

        # This is the one deliberately expensive step in the cycle: judging
        # whether the evidence just gathered shows CLEAR impact (not just a
        # plausible signal) is exactly the kind of call a real pentester
        # slows down for. Escalate to the deep model only when it's worth
        # it — low-confidence hypotheses or failed tool runs never reach it.
        if self.impact_assessor and top and self.impact_assessor.should_escalate(
            hypothesis_confidence=top.confidence, exec_status=exec_result.status
        ):
            impact = self.impact_assessor.assess(
                vulnerability=top.observation,
                attack_strategy=top.attack_strategy,
                tool_output=exec_result.stdout or exec_result.stderr,
                decision_reasoning=decision.reason,
            )
        elif self.impact_assessor and top:
            impact = self.impact_assessor.skipped_result(
                "hypothesis confidence below deep-review threshold or tool run incomplete"
            )
        else:
            impact = {"clear_impact": False, "severity": "info", "false_positive_risk": "unknown",
                       "reasoning": "no impact assessor configured" if not self.impact_assessor
                       else "no active hypothesis this cycle"}

        verification = self.verification_engine.verify(
            reproductions=1 if exec_result.status == "completed" else 0,
            alternate_payloads_tried=0,
            evidence_count=1,
            stable_across_attempts=exec_result.status == "completed",
            clear_impact=impact["clear_impact"],
        )
        if top:
            self.hypothesis_engine.record_result(top.id, verification.verified, str(evidence_id))

        # 7b. Experience Learning — every real outcome becomes future
        # evidence, but only once it's terminal (confirmed/rejected/tool
        # failure) so a single "needs more evidence" retry doesn't spam
        # the Experience DB with noise.
        if self.learning_engine is not None and matched_categories:
            category = matched_categories[0]
            outcome = None
            reason = decision.reason
            failure_type = ""
            if exec_result.status != "completed":
                outcome, failure_type = "tool_failure", exec_result.status
            elif top and top.status.value == "confirmed":
                outcome = "success"
            elif top and top.status.value == "rejected":
                outcome = "failure"
            if outcome:
                self.learning_engine.record_experience(
                    outcome=outcome,
                    category=category,
                    technology="",
                    description=top.observation if top else "",
                    reason=reason,
                    environment=target_hint or "",
                    failure_type=failure_type,
                    session_id=self.memory_manager.session_id,
                    playbook_key=category,
                )

        # 8. Update memory + checkpoint
        self.state = PlannerState.UPDATING_MEMORY
        self.memory_manager.working.request_history.append({
            "tool": decision.tool, "status": exec_result.status, "cycle": self._cycle_count,
        })
        self._checkpoint()

        self.state = PlannerState.IDLE
        return {
            "cycle": self._cycle_count,
            "tool_executed": decision.tool,
            "exec_status": exec_result.status,
            "hypothesis": top.id if top else None,
            "verified": verification.verified,
            "impact_assessment": impact,
        }

    def _checkpoint(self):
        self.memory_manager.save_checkpoint(
            planner_state={"state": self.state.value, "cycle": self._cycle_count},
            attack_graph=self.attack_graph.to_dict(),
            task_queue={},
            resource_status=self.resource_monitor.snapshot(),
        )
