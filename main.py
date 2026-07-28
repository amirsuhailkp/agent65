"""Agent Cyber — entry point. Wires config -> memory -> knowledge -> reasoning
-> planner -> dispatcher -> reporting, then runs the cognitive cycle loop.

Usage:
    python main.py --goal "Discover and test authentication endpoints" \
                    --target "app.example.com" --resume-session 3
"""
from __future__ import annotations
import argparse
from src.config import load_config, load_scope, resolve_path
from src.logging_setup import get_logger
from src.memory.memory_manager import MemoryManager
from src.knowledge.knowledge_manager import KnowledgeManager
from src.reasoning.ollama_client import OllamaClient
from src.reasoning.reasoning_engine import ReasoningEngine
from src.reasoning.impact_assessor import ImpactAssessor
from src.planner.hypothesis_engine import HypothesisEngine
from src.planner.decision_engine import DecisionEngine
from src.planner.goal_manager import GoalManager
from src.planner.verification_engine import VerificationEngine
from src.planner.resource_monitor import ResourceMonitor
from src.planner.planner import Planner
from src.tools.tool_registry import ToolRegistry
from src.dispatcher.kali_dispatcher import KaliDispatcher
from src.reporting.evidence_collector import EvidenceCollector
from src.memory.db_models import get_session_factory
from src.knowledge.repository import KnowledgeRepository
from src.learning.learning_engine import LearningEngine

log = get_logger("main")


def build_planner() -> Planner:
    cfg = load_config()
    scope = load_scope()

    db_path = str(resolve_path(cfg["database"]["sqlite_path"]))
    session_factory = get_session_factory(db_path)

    goal_manager = GoalManager(scope)
    memory_manager = MemoryManager(db_path)
    knowledge_manager = KnowledgeManager(cfg)

    llm_client = OllamaClient(
        host=cfg["llm"]["host"], model=cfg["llm"]["model"],
        temperature=cfg["llm"]["temperature"], max_retries=cfg["llm"]["max_retries"],
        backoff_base_seconds=cfg["llm"]["backoff_base_seconds"],
    )
    # Deep model — only used for ImpactAssessor's escalation call and the
    # (offline, infrequent) Learning Engine observation extraction. Falls
    # back to the fast model's settings if llm_deep isn't configured, so
    # this doesn't break setups that haven't added the new config section.
    deep_cfg = cfg.get("llm_deep", cfg["llm"])
    llm_deep_client = OllamaClient(
        host=deep_cfg["host"], model=deep_cfg["model"],
        temperature=deep_cfg["temperature"], max_retries=deep_cfg["max_retries"],
        backoff_base_seconds=deep_cfg["backoff_base_seconds"],
    )
    reasoning_engine = ReasoningEngine(llm_client)
    hypothesis_engine = HypothesisEngine(max_retries=cfg["session"]["max_retry_per_hypothesis"])
    decision_engine = DecisionEngine(scope_checker=goal_manager.is_in_scope)
    verification_engine = VerificationEngine()
    resource_monitor = ResourceMonitor(
        gpu_temp_warn_c=cfg["resources"]["gpu_temp_warn_c"],
        gpu_temp_pause_c=cfg["resources"]["gpu_temp_pause_c"],
        vram_warn_pct=cfg["resources"]["vram_warn_pct"],
        ram_warn_pct=cfg["resources"]["ram_warn_pct"],
        cooldown_seconds=cfg["resources"]["cooldown_seconds"],
        cpu_warn_pct=cfg["resources"]["cpu_warn_pct"],
        cpu_pause_pct=cfg["resources"]["cpu_pause_pct"],
    )

    registry = ToolRegistry(str(resolve_path("config/tools_registry.yaml")))
    dispatcher = KaliDispatcher(
        host=cfg["kali_vm"]["host"], port=cfg["kali_vm"]["ssh_port"],
        user=cfg["kali_vm"]["ssh_user"], key_path=cfg["kali_vm"]["ssh_key_path"],
        connect_timeout=cfg["kali_vm"]["connect_timeout"], registry=registry,
    )
    evidence_collector = EvidenceCollector(str(resolve_path("evidence")), session_factory)

    # Playbook Learning Engine — reuses the same repository the
    # KnowledgeManager already opened (single source of truth for the
    # collector's processed/ output). Uses the DEEP model: this pipeline
    # runs offline/infrequently (--learn-knowledge), not in the hot loop,
    # so extraction quality matters more here than latency.
    learning_engine = LearningEngine(
        repository=knowledge_manager.repository,
        session_factory=session_factory,
        llm_client=llm_deep_client,
        config=cfg.get("learning", {}),
    )

    # Impact Assessor — the deliberate "deep thinking" escalation point.
    # Gated by verification.min_confidence_for_deep_review so the deep
    # model is only called for hypotheses that already look promising.
    impact_assessor = ImpactAssessor(
        deep_llm_client=llm_deep_client,
        min_confidence_to_escalate=cfg.get("verification", {}).get("min_confidence_for_deep_review", 0.5),
    )

    return Planner(
        goal_manager=goal_manager,
        knowledge_manager=knowledge_manager,
        memory_manager=memory_manager,
        reasoning_engine=reasoning_engine,
        hypothesis_engine=hypothesis_engine,
        decision_engine=decision_engine,
        verification_engine=verification_engine,
        dispatcher=dispatcher,
        evidence_collector=evidence_collector,
        resource_monitor=resource_monitor,
        checkpoint_interval_seconds=cfg["session"]["checkpoint_interval_seconds"],
        learning_engine=learning_engine,
        impact_assessor=impact_assessor,
    )


def main():
    parser = argparse.ArgumentParser(description="Agent Cyber")
    parser.add_argument("--goal", required=True, help="Current testing goal")
    parser.add_argument("--target", default=None, help="Target hint for scope check")
    parser.add_argument("--cycles", type=int, default=1, help="Number of cognitive cycles to run")
    parser.add_argument("--sync-knowledge", action="store_true",
                         help="Sync from Knowledge Collector output before running")
    parser.add_argument("--learn-knowledge", action="store_true",
                         help="Run the Playbook Learning Engine pipeline (extract observations, "
                              "synthesize/version playbooks) before running")
    parser.add_argument("--approve-high-risk", action="store_true")
    parser.add_argument("--resume-session", type=int, default=None)
    args = parser.parse_args()

    planner = build_planner()

    if args.sync_knowledge:
        n = planner.knowledge_manager.sync_from_collector()
        log.info(f"Synced {n} chunks from Knowledge Collector output")

    if args.learn_knowledge:
        summary = planner.learning_engine.import_knowledge()
        log.info(f"Playbook Learning Engine: {summary}")

    if args.resume_session:
        planner.memory_manager.resume_session(args.resume_session)
    else:
        planner.memory_manager.start_session(
            planner.goal_manager.program_name,
            {"in_scope": planner.goal_manager.in_scope},
        )

    for _ in range(args.cycles):
        outcome = planner.run_cycle(
            current_goal=args.goal, target_hint=args.target,
            approve_high_risk=args.approve_high_risk,
        )
        log.info(f"Cycle outcome: {outcome}")
        if outcome.get("pending_approval"):
            log.info("Stopping — awaiting human approval for high-risk action")
            break

    planner.dispatcher.close()


if __name__ == "__main__":
    main()