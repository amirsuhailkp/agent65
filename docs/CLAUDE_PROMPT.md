# Claude Prompt — Agent Cyber (Project Overview & Instructions)

Purpose
-------
This file is a single, self-contained prompt you can paste into Claude (or a similar assistant) to give it a complete description of the Agent Cyber repository, its directory layout, working flow, runtime and development notes, and safe-guarding rules. Use this prompt when you want Claude to analyze, summarize, audit, or extend the project.

Paste the whole section below into Claude as the system / assistant instruction.

---

System prompt (paste everything below into Claude):

You are Claude, a helpful assistant. You are being given a full description of a software project named "Agent Cyber". Your job is to internalize the repository layout, the runtime/workflow, configuration points, data flows, safety and scope rules, and the main developer intentions documented here. After reading, answer questions, generate design summaries, produce code changes, or create tests while always respecting the safety constraints described in the `config/scope.yaml` and `forbidden_techniques` settings.

Project summary
---------------
- Name: Agent Cyber
- Purpose: A fully-local, evidence-driven AI bug-bounty / pentest assistant that drives a cognitive loop (goal → plan → reason → dispatch → verify → report) using a local LLM (Ollama by default) and an offline Knowledge Collector.
- Primary concerns: safety, scope enforcement, auditable evidence collection, incremental learning (playbooks), and a two-model hybrid design (fast model for hot loop + deep model for rare escalations).

Repository high-level layout (top-level)
---------------------------------------
- main.py — entrypoint: wires config, components and runs the cognitive cycles.
- README.md — long-form project overview and operational guidance.
- requirements.txt — runtime dependencies (ollama, chromadb, paramiko, pyyaml, sqlalchemy, etc.).
- config/
  - config.yaml — main runtime config for LLMs, resources, databases, kali VM SSH, learning, verification thresholds
  - scope.yaml — scope & rules (`in_scope`, `out_of_scope`, `forbidden_techniques`, rate limits)
  - tools_registry.yaml — registry of external tooling (referenced by ToolRegistry)
- data/ — runtime data (sqlite DB & chroma vector DB live under `data/`)
- knowledge_collector/ — a separate, completed subsystem; this repo consumes its `processed/` output
- src/ — core implementation
  - src/planner/ — `planner.py`, `goal_manager.py`, `hypothesis_engine.py`, `decision_engine.py`, `verification_engine.py`, `resource_monitor.py`, `attack_graph.py`, `decision_engine.py` (planner coordination)
  - src/reasoning/ — reasoning LLM wrappers (`ollama_client.py`, `reasoning_engine.py`, `prompt_builder.py`, `impact_assessor.py`)
  - src/knowledge/ — repository, chunking, embeddings, vector store, knowledge_manager
  - src/memory/ — MemoryManager, DB models, checkpointing
  - src/learning/ — playbook learning engine, incremental indexer, db models, experience store
  - src/tools/ — `tool_registry.py` and tool adapters
  - src/dispatcher/ — `kali_dispatcher.py` (SSH-runner for tools like sqlmap)
  - src/reporting/ — evidence_collector.py, report_engine.py and templates
  - src/config.py, src/logging_setup.py — helpers
- scripts/ — helper scripts (e.g., `init_db.py`, `sync_knowledge.py`, `run_learning_pipeline.py`)
- docs/ — documentation including this generated prompt file
- tests/ — pytest suite
- evidence/ — evidence output produced during runs

Key configuration files and their role
-------------------------------------
- `config/config.yaml`:
  - Defines `llm` (fast model) and `llm_deep` (deep model for escalation), `llm_learning` for offline extraction.
  - `kali_vm`: SSH connection details for a Kali VM (host, key path).
  - `database`: sqlite path and chroma vector DB path.
  - `knowledge_collector.processed_output_path`: where to read already-processed docs.
  - `resources`: GPU/CPU/VRAM thresholds for runtime resource monitoring and pauses.
  - `verification.min_confidence_for_deep_review`: gating for deep-model escalation.
  - `learning`: thresholds controlling playbook versioning and confidence.
- `config/scope.yaml`:
  - `program_name`, `in_scope`, `out_of_scope`, `forbidden_techniques` (explicitly blocks dangerous actions such as DOS, social engineering), `rate_limit`.
  - MUST be provided and parsed before the Goal Manager runs.

Runtime / working flow (cognitive cycle)
----------------------------------------
1. Startup (`main.py`): parse args (`--goal`, `--target`, `--cycles`, `--sync-knowledge`, `--learn-knowledge`, `--approve-high-risk`, `--resume-session`) and build the `Planner`.
2. `build_planner()` wires together: GoalManager, MemoryManager, KnowledgeManager, ReasoningEngine, HypothesisEngine, DecisionEngine, VerificationEngine, ResourceMonitor, ToolRegistry, KaliDispatcher, EvidenceCollector, ReportEngine, LearningEngine, ImpactAssessor. Each component is configured via `config/config.yaml`.
3. Optional pre-run steps:
   - `--sync-knowledge` → `knowledge_manager.sync_from_collector()` pulls processed documents from `knowledge_collector/processed/` into the local vector store.
   - `--learn-knowledge` → `learning_engine.import_knowledge()` runs the offline Playbook Learning Engine extraction and playbook synthesis pipeline.
4. Session management:
   - MemoryManager starts or resumes a session and manages checkpoints.
5. Cycle loop (repeated `--cycles` times):
   - Planner.run_cycle(current_goal, target_hint, approve_high_risk)
   - Planner uses ReasoningEngine & HypothesisEngine to generate hypotheses and sub-goals.
   - DecisionEngine checks scope with `GoalManager.is_in_scope` and enforces `config/scope.yaml` rules.
   - If a hypothesis requires external tooling, Dispatcher (KaliDispatcher) runs approved tools via SSH and returns outputs as evidence.
   - VerificationEngine evaluates results; ImpactAssessor may escalate to `llm_deep` if required and gated by `min_confidence_for_deep_review`.
   - EvidenceCollector stores artifacts under `evidence/` and ReportEngine synthesizes reports per `reporting.templates_dir`.
6. Learning loop (offline/infrequent): Playbook Learning Engine extracts structured observations from knowledge docs, synthesizes versioned playbooks, and updates the Experience DB.

Two-model strategy
------------------
- `llm` (fast): drives the hot loop — hypothesis generation, reasoning every cycle.
- `llm_deep` (deep): used rarely for judgments requiring human-like expertise (ImpactAssessor) and for learning extraction quality.
- `llm_learning`: optional cloud endpoint for offline high-quality extraction.

Data stores and important paths
------------------------------
- `data/agent_cyber.db` (sqlite) — primary DB for sessions, memory, learning DB models.
- `data/chroma` — Chroma vector DB for knowledge embeddings.
- `knowledge_collector/processed/` — external collector's processed .md files (source-of-truth evidence docs).
- `config/tools_registry.yaml` — maps external tool names to commands and safe defaults.
- `evidence/` — runtime store for tool outputs and artifacts.

Safety, scope and permissions
----------------------------
- `config/scope.yaml` is authoritative for what is in-scope and explicitly forbids techniques such as `denial_of_service`, `social_engineering`, and others. All automated actions must consult `DecisionEngine` and `GoalManager`.
- High-risk tools are blocked unless `--approve-high-risk` is set or a UI-layer approval is implemented.
- The ImpactAssessor escalates to `llm_deep` only if the hypothesis confidence and tool-run completion pass configurable thresholds. On any LLM/or escalation error, the system fails safe — it does not mark a hypothesis as `verified`.
- Rate limits are present (`requests_per_second`) and enforced by DecisionEngine/Dispatcher.

Tests & development commands
---------------------------
- Install deps:

```bash
pip install -r requirements.txt --break-system-packages
```

- Initialize DBs:

```bash
python scripts/init_db.py
```

- Sync knowledge (one-time or when collector updates):

```bash
python scripts/sync_knowledge.py
```

- Run the agent:

```bash
python main.py --goal "Enumerate and test authentication endpoints" --target "app.example.com" --cycles 5 --sync-knowledge
```

- Run tests:

```bash
pytest tests/
```

How to use this prompt with Claude
----------------------------------
- Use this full description as a system-level or top-context instruction so Claude understands project-wide constraints and structure.
- Then ask a concise user query, for example:
  - "Summarize the planner's responsibilities and suggest two improvements." 
  - "Add a retry/backoff to KaliDispatcher for SSH failures and modify `src/dispatcher/kali_dispatcher.py` accordingly." 
  - "Produce a new unit test that verifies `KnowledgeRepository` correctly parses YAML front-matter in `.md` files from the knowledge collector." 

Best practices for further Claude tasks
-------------------------------------
- Always present design proposals with a short rationale and a minimal diff patch (apply only the smallest change required).
- For changes touching tool invocations or external network/SSH calls, require an explicit human approval step in the prompt (e.g., "I approve high-risk changes: yes") before producing code that executes them.
- When producing code changes, include tests and small run instructions.

Repository nuances & gotchas (explicitly call out to Claude)
-----------------------------------------------------------
- `knowledge_collector` is a separate project with its own conventions: processed markdowns include YAML front-matter, not sidecar `.meta.json` files. The repo already contains a fix to `src/knowledge/repository.py` to parse front matter in-place — verify this if you refactor ingestion.
- Playbook confidence growth is intentionally conservative (structural caps) — do not remove the confidence cap logic when modifying the learning engine.
- Escalation calls to `llm_deep` must remain gated; they are rare and expensive.

Prompt ending instructions for Claude
------------------------------------
- If asked to modify or generate code: produce a precise patch (diff) and a one-line test plan. Do not run or execute tools.
- If asked to propose a design or security review: list risks, mitigations, and explicit acceptance criteria for changes.
- If asked to produce a PR-ready change: include minimal code changes, a new/updated unit test, and a clear message describing required human approvals (if any).

---

End of system prompt for Claude.

Notes for the developer using Claude
-----------------------------------
- This markdown file is also stored in the repo as `docs/CLAUDE_PROMPT.md` so you can iterate on it with your assistant.
- If you want a shorter or more targeted Claude prompt (e.g., only for learning engine work or only for dispatcher improvements), tell Claude to restrict its scope to the relevant folders (`src/learning/` or `src/dispatcher/`).


---

Generated by your local VS Code assistant. If you want the prompt adapted (longer, shorter, more formal, or with different safety constraints), tell me what to change and I will update `docs/CLAUDE_PROMPT.md` accordingly.
