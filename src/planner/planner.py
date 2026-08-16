"""Planner — the AI Brain's orchestrator. Vol III Ch2-3 (cognitive cycle),
Ch16 (state machine), Vol II Ch7.

Cycle: Observe -> Retrieve Knowledge -> Reason -> Generate Hypotheses ->
       Rank -> Decide -> Execute (Kali) -> Verify -> Update Memory -> Repeat
"""
from __future__ import annotations
from enum import Enum
from ..logging_setup import get_logger
from ..reasoning.reasoning_engine import ReasoningEngine, format_shape_correction
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
from ..reporting.report_engine import ReportEngine
from .report_builder import build_finding_draft
from ..reasoning.impact_assessor import ImpactAssessor
from .findings_summary import summarize as summarize_findings

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
        report_engine: ReportEngine | None = None,
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
        # Built, tested, but never previously wired to anything — this was
        # the actual bug behind "it doesn't report even on fail": nothing
        # in the codebase ever called ReportEngine.export(). Optional here
        # for the same reason impact_assessor is, so existing wiring/tests
        # that don't construct one keep working unchanged.
        self.report_engine = report_engine

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

        # 2. Reason (+ 3. hypotheses + 4. decide, as one retryable unit)
        #
        # A model that drifts the target out of scope used to cost an
        # entire cycle for nothing: decide() rejects it, we log a warning,
        # and the *next* cycle starts from scratch with no idea the last
        # one already failed this exact way. Since decision_engine now
        # remembers *why* it blocked (last_block_reason), retry once
        # in-place with a correction message naming the rejected value and
        # the canonical target, before giving up on the cycle. Capped at
        # one retry — this is for "drifted the target," a specific,
        # correctable mistake, not a general-purpose retry-until-it-works
        # loop for the model being wrong in other ways.
        correction = None
        result: dict = {}
        top = None
        decision = None
        for attempt in range(2):
            result = self.reasoning_engine.reason(
                current_goal=current_goal,
                scope={
                    "program": self.goal_manager.program_name,
                    "in_scope": self.goal_manager.in_scope,
                    "forbidden_techniques": list(self.goal_manager.forbidden_techniques),
                    "known_credentials": self.goal_manager.known_credentials,
                    "session_auth_ground_truth": self.goal_manager.session_auth_ground_truth,
                    "url_structure_ground_truth": self.goal_manager.url_structure_ground_truth,
                },
                working_memory=self.memory_manager.working.to_dict(),
                retrieved_knowledge=retrieved,
                active_hypotheses=self.hypothesis_engine.active(),
                available_tools=self.dispatcher.registry.schema_summary(),
                resource_status=status,
                relevant_playbooks=playbooks,
                relevant_experiences=experiences,
                target=target_hint,
                correction=correction,
            )

            if result.get("error"):
                log.warning(f"Cycle {self._cycle_count} aborted: {result['error']}")
                self.state = PlannerState.IDLE
                return {"cycle": self._cycle_count, "aborted": True, "reason": result["error"]}

            self.hypothesis_engine.ingest(result.get("hypotheses", []))
            ranked = self.hypothesis_engine.rank()
            top = ranked[0] if ranked else None

            decision = self.decision_engine.decide(
                next_action=result.get("next_action"),
                target_hint=target_hint,
                top_hypothesis_id=top.id if top else None,
                recent_actions=self.memory_manager.working.request_history,
            )
            if decision:
                break

            correction = self.decision_engine.correction_message(target_hint)
            correction_kind = "scope drift" if correction else None
            if not correction:
                shape_warning = result.get("shape_warning")
                if shape_warning:
                    correction = format_shape_correction(shape_warning)
                    correction_kind = "malformed next_action"
            if not correction or attempt == 1:
                # Neither retryable failure mode applied (correction_message
                # and shape_warning both empty means the model genuinely
                # returned no next_action at all, or decide() rejected it for
                # a reason retrying won't fix — e.g. an unknown tool name),
                # or we've already used the one retry. Stop here either way.
                break
            log.info(
                f"Cycle {self._cycle_count}: decision blocked ({correction_kind}), "
                f"retrying once in-place with a correction"
            )

        if not decision:
            # next_action can be missing/None/{} for two very different
            # reasons: the model genuinely concluded there's nothing left
            # to try, or it just produced a malformed/empty next_action
            # while still writing a useful analysis. Previously this
            # branch discarded `result` entirely, so a cycle could go
            # silent with zero trace of what the model was thinking —
            # and, since this is an early return before step 8, zero
            # trace in request_history either, so the *next* cycle had no
            # idea a dead end had already been hit and could repeat it.
            analysis = (result.get("analysis") or "").strip()
            log.info(
                f"Cycle {self._cycle_count}: no decision made. "
                f"Model analysis: {analysis[:500] or '(none provided)'} | "
                f"raw next_action={result.get('next_action')!r}"
            )
            self.memory_manager.working.request_history.append({
                "tool": None, "status": "no_action", "cycle": self._cycle_count,
                "summary": analysis[:500] or "model produced no next_action and no analysis",
            })
            self.state = PlannerState.IDLE
            return {"cycle": self._cycle_count, "decision": None, "analysis": analysis}

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
            hypothesis_id=None,  # Evidence.hypothesis_id is an Integer FK into a
            # `hypotheses` DB table nothing populates — HypothesisEngine tracks
            # hypotheses in-memory only, with string ids like "hyp_2026...".
            # Passing that string here would violate the FK / corrupt the column.
            # top.id is preserved instead in the report's evidence_refs via
            # report_builder, so it's not actually lost — just not stored here.
            endpoint=target_hint,
            request=exec_result.command.encode() if exec_result.command else None,
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
            hypothesis_confidence=top.confidence, exec_status=exec_result.status,
            tool_output=exec_result.stdout or exec_result.stderr,
        ):
            impact = self.impact_assessor.assess(
                vulnerability=top.observation,
                attack_strategy=top.attack_strategy,
                tool_output=exec_result.stdout or exec_result.stderr,
                decision_reasoning=decision.reason,
            )
            escalated = True
        elif self.impact_assessor and top:
            impact = self.impact_assessor.skipped_result(
                "hypothesis confidence below deep-review threshold or tool run incomplete"
            )
            escalated = False
        else:
            impact = {"clear_impact": False, "severity": "info", "false_positive_risk": "unknown",
                       "reasoning": "no impact assessor configured" if not self.impact_assessor
                       else "no active hypothesis this cycle"}
            escalated = False

        verification = self.verification_engine.verify(
            reproductions=1 if exec_result.status == "completed" else 0,
            alternate_payloads_tried=0,
            evidence_count=1,
            stable_across_attempts=exec_result.status == "completed",
            clear_impact=impact["clear_impact"],
        )
        if top:
            self.hypothesis_engine.record_result(top.id, verification.verified, str(evidence_id))

        # 7a. Report — fires on BOTH confirmed and rejected, deliberately.
        # A real pentest report documents what was tested and ruled out,
        # not only what succeeded. "needs_more_evidence" is intentionally
        # excluded here (same terminal-outcome gate as 7b below) so a
        # hypothesis still being retried doesn't generate a new report
        # every single cycle before it's actually settled.
        if self.report_engine is not None and top and top.status.value in ("confirmed", "rejected"):
            category = matched_categories[0] if matched_categories else "uncategorized"
            finding = build_finding_draft(
                hypothesis=top, decision=decision, exec_result=exec_result,
                impact=impact, verification=verification, category=category,
                evidence_id=evidence_id, target_hint=target_hint,
            )
            report_path = self.report_engine.export(finding, fmt="markdown")
            log.info(f"Report drafted ({finding.verified=}): {report_path}")

        # 7b. Experience Learning — terminal outcomes (confirmed/rejected/
        # tool failure) always become experience. Non-terminal
        # "needs_more_evidence" cycles ALSO become experience now, but only
        # once per hypothesis (via `partial_recorded`) — so a hypothesis
        # that gets retried 2-3 times before resolving doesn't spam the
        # Experience DB with duplicate mid-flight signal, but the signal
        # from that mid-flight state isn't silently discarded either.
        #
        # Hypothesis verdict takes priority over raw tool exec status.
        # A hypothesis reaches "rejected" only after max_retries failed
        # verification attempts (see HypothesisEngine.record_result), and
        # verification requires exec_result.status == "completed" to even
        # count as a reproduction — so a hypothesis's *final* rejecting
        # cycle is very likely to also be a cycle with a non-"completed"
        # tool status. Checking tool status first (as this used to) would
        # silently reclassify that rejection as generic "tool_failure",
        # discarding the actual hypothesis-testing signal. "tool_failure"
        # is now only used when there's no hypothesis verdict to report.
        if self.learning_engine is not None and matched_categories:
            category = matched_categories[0]
            outcome = None
            reason = decision.reason
            failure_type = ""
            if top and top.status.value == "confirmed":
                outcome = "success"
            elif top and top.status.value == "rejected":
                outcome = "failure"
                if exec_result.status != "completed":
                    failure_type = exec_result.status
            elif (
                top
                and top.status.value == "needs_more_evidence"
                and not top.partial_recorded
                and exec_result.status == "completed"
            ):
                # A real, completed test cycle that didn't yet clear the
                # bar for confirmed/rejected — still genuine signal (e.g.
                # a promising lead still being narrowed down), distinct
                # from a raw tool failure. Recorded once per hypothesis:
                # set the flag right here, while `top` is still narrowed
                # to non-None by this branch's own condition, rather than
                # via a separate bool checked later where that narrowing
                # is lost to static analysis.
                outcome = "partial"
                top.partial_recorded = True
            elif exec_result.status != "completed":
                outcome, failure_type = "tool_failure", exec_result.status
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
        # Previously only {tool, status, cycle} carried forward — the next
        # cycle's LLM call had no idea what a tool actually found (or why
        # it failed), only pass/fail. That's how the agent kept re-running
        # near-identical scans: it couldn't see "0 matches" vs "no output
        # captured" vs a real error, so it had nothing concrete to adapt to.
        tool_spec = self.dispatcher.registry.get(decision.tool)
        output_format = (tool_spec.output_schema or {}).get("format") if tool_spec else None
        summary = summarize_findings(decision.tool, output_format, exec_result)
        history_entry = {
            "tool": decision.tool, "status": exec_result.status, "cycle": self._cycle_count,
            "summary": summary, "params": decision.params,
        }
        if escalated:
            # The deep model (qwen3:8b) sees the FULL raw tool output and
            # often catches something the shallow `summary` above doesn't
            # surface at all — e.g. "the author param IS reaching a live
            # SQL query, just not the two specific values tried" is a real,
            # actionable lead that a generic tool-output summary has no way
            # to express. Previously this reasoning was computed, used once
            # for verification/reporting, then thrown away — the NEXT
            # cycle's fast-model prompt never saw it, so a genuinely
            # promising lead could vanish after one cycle instead of
            # prompting a follow-up test. Only attached when the deep
            # model actually ran (escalated=True) — skipped/no-assessor
            # placeholder text isn't worth the tokens every cycle.
            history_entry["deep_review"] = {
                "clear_impact": impact["clear_impact"],
                "severity": impact["severity"],
                "reasoning": impact["reasoning"],
            }
        self.memory_manager.working.request_history.append(history_entry)
        self._checkpoint()

        self.state = PlannerState.IDLE
        return {
            "cycle": self._cycle_count,
            "tool_executed": decision.tool,
            "exec_status": exec_result.status,
            "hypothesis": top.id if top else None,
            "verified": verification.verified,
            "impact_assessment": impact,
            "summary": summary,  # what actually got carried into next cycle's
            # working memory — was invisible in logs before this, making it
            # impossible to tell "the mechanism is broken" from "the
            # mechanism works but the content isn't useful" without a DB dive
        }

    def _checkpoint(self):
        self.memory_manager.save_checkpoint(
            planner_state={"state": self.state.value, "cycle": self._cycle_count},
            attack_graph=self.attack_graph.to_dict(),
            task_queue={},
            resource_status=self.resource_monitor.snapshot(),
        )