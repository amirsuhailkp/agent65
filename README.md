# Agent Cyber

Fully local, evidence-driven AI bug bounty agent. Ollama (Qwen3:8b) + ChromaDB +
SSH-dispatched Kali tooling, built around your existing, completed **Knowledge
Collector Framework** (`F:\agent-cyber\knowledge_collector` — not touched, not
rebuilt, only consumed).

## Spec → Code Map

| Volume | Subsystem | Code |
|---|---|---|
| I | Vision / Ethics | governs every module below |
| II Ch6 | Goal Manager | `src/planner/goal_manager.py` |
| II Ch7 / III | Planner (cognitive cycle) | `src/planner/planner.py` |
| II Ch8 / III Ch6 | Reasoning Engine | `src/reasoning/reasoning_engine.py` |
| II Ch9 / III Ch7 | Hypothesis Engine | `src/planner/hypothesis_engine.py` |
| II Ch10 / IV | Memory Manager (working/session/long-term) | `src/memory/memory_manager.py` |
| II Ch11 / IV | Knowledge Manager (RAG) | `src/knowledge/` (repository, chunking, embedding, vector_store, knowledge_manager) |
| II Ch13 / VII Ch5 | Tool Registry | `src/tools/tool_registry.py`, `config/tools_registry.yaml` |
| II Ch14 / VII | Kali Dispatcher (SSH) | `src/dispatcher/kali_dispatcher.py` |
| II Ch15 / IX | Evidence Collector | `src/reporting/evidence_collector.py` |
| II Ch16 / V Ch13 | Verification Engine | `src/planner/verification_engine.py` |
| II Ch17 / IX | Report Engine | `src/reporting/report_engine.py` |
| II Ch18 / X | Attack Graph | `src/planner/attack_graph.py` |
| II Ch19 / IV Ch13 | Checkpoint Manager | `MemoryManager.save_checkpoint/resume_session` |
| II Ch20 | Resource Monitor (GPU guard) | `src/planner/resource_monitor.py` |
| III Ch8 | Decision Engine | `src/planner/decision_engine.py` |
| III Ch9 | Ollama client (retry/backoff) | `src/reasoning/ollama_client.py` |
| III Ch14 | Prompt Architecture | `src/reasoning/prompt_builder.py` |
| VI Ch10 | DB init | `scripts/init_db.py`, `src/memory/db_models.py` |
| — (Learning Engine Update) | Playbook Learning Engine | `src/learning/` (db_models, incremental_indexer, observation_extractor, confidence, playbook_synthesizer, experience_store, learning_engine) |

## Collector integration — verified against your real code

Pulled your actual `amirsuhailkp/agent` repo and checked the real output
contract (`metadata/metadata_generator.py`, `storage/filesystem.py`,
`config/settings.py`), not assumptions. Found and fixed one real mismatch:

- **Before:** `src/knowledge/repository.py` expected a sidecar
  `<doc>.meta.json` next to each `.md` file. Your collector doesn't produce
  that — it never did, nothing is missing on your end.
- **Reality:** `MetadataGenerator.generate()` prepends YAML front matter
  directly into the single `.md` file (`title/source/url/collector/category/
  tags/date_collected/language`). Confirmed against 224 real files in
  `knowledge_collector/processed/`.
- **Fix:** `repository.py` now parses that front matter directly. No sidecar
  files, one less moving part. `trust_level` (a concept from Vol IV Ch8,
  not something your collector emits) is derived from a small trusted-source
  allowlist (`owasp`, `portswigger`, `hacktricks`, etc.) based on the
  `collector` field — anything outside that list stays `unverified` until a
  human promotes it, per the Vol IV Ch14 learning rules.
- Added `tests/test_repository_real_format.py`, which parses an actual
  sample from your `processed/` folder, so this can't silently regress again.
- Verified against all 224 real files in your repo: 224/224 parse correctly.

Nothing in your collector (`knowledge_collector/`) was touched — nothing
needed to be. It's clean, has its own test suite, and the `chunker/`,
`embeddings/`, `vector_store/` folders in it are explicitly marked as
reserved extension points in their own `__init__.py` docstrings, which is
exactly what `src/knowledge/` in this repo now fills in. No duplication.



```bash
pip install -r requirements.txt --break-system-packages
python scripts/init_db.py
```

Edit `config/config.yaml`:
- `kali_vm` — your bridged-adapter IP + SSH key path
- `knowledge_collector.processed_output_path` — points at your collector's
  `processed/` directory directly (confirmed against your collector's
  `config/settings.py`: `processed_directory = <collector_root>/processed`,
  no intermediate `storage/` folder)

Edit `config/scope.yaml` before any run — the Goal Manager refuses to start
without `in_scope` entries.

## Run

```bash
# one-time: index whatever the collector has already produced
python scripts/sync_knowledge.py

# run the agent
python main.py --goal "Enumerate and test authentication endpoints" \
                --target "app.example.com" --cycles 5 --sync-knowledge
```

High-risk tools (e.g. sqlmap) are blocked until you pass `--approve-high-risk`
or wire an approval prompt in your UI layer (`src/ui/`, not yet built).

## Playbook Learning Engine

Implements `Claude_Playbook_Learning_Engine_Update.md`. This is **not**
fine-tuning — the LLM (Ollama/Qwen3:8b) stays the reasoning engine. The
agent gets better at investigating by building structured, auditable
knowledge around it, in four independent layers:

1. **Knowledge Database** — already existed (`src/knowledge/repository.py`),
   raw collector output, never modified, treated as immutable evidence.
2. **Observation Database** (`src/learning/db_models.py::Observation`) — one
   row per structured fact extracted from one document (vulnerability,
   preconditions, discovery sequence, payloads, tool usage, decision points,
   false positives, failure reasons, validation steps, severity, references).
   The planner never queries raw documents directly — only observations
   (and playbooks synthesized from them).
3. **Playbook Database** (`src/learning/db_models.py::Playbook`) — a
   synthesized methodology, never copied from a single report. Workflow
   steps are merged across every supporting observation by average relative
   position (so a step that consistently shows up early across many reports
   stays early); tools/mistakes/false-positives are merged by frequency.
   Versioned and append-only: a new version is only created on a real
   structural change (workflow/tools/mistakes) or a material confidence
   shift — nothing is ever deleted or overwritten, older versions stay
   available for auditing.
4. **Experience Database** (`src/learning/db_models.py::Experience`) — every
   real engagement outcome (success/failure/duplicate/invalid/partial/
   tool_failure/false_positive) becomes future evidence. A later document
   can be linked to an old unexplained failure once it explains why.

**Incremental import**: `src/learning/incremental_indexer.py` hashes
(SHA256) each document and skips anything already indexed and unchanged —
if 100,000 reports exist and 3 are new, only those 3 get processed.

**Confidence** (`src/learning/confidence.py`): structurally capped at 0.3
for a playbook backed by a single report, regardless of any other factor —
"never increase confidence from one report alone" is enforced in code, not
just documentation. Grows with independent source diversity and personal
successful findings; shrinks with contradictory experience.

**Planner integration**: `Planner` (given an optional `learning_engine=`)
retrieves relevant playbooks + experience before every reasoning cycle
(`reasoning/prompt_builder.py` adds "Relevant Playbooks" / "Relevant
Experience" sections) and records the real outcome back into the
Experience DB once a hypothesis reaches a terminal state.

Run the pipeline (safe/cheap to re-run often — unmodified documents are
always skipped):

```bash
python scripts/run_learning_pipeline.py
# or as part of a normal run:
python main.py --goal "..." --target "..." --learn-knowledge
```

## Two-Model Hybrid (fast loop / deep escalation)

Tuned for constrained hardware (e.g. RTX 3050 4GB laptop): one small model
drives the hot loop, a larger model is called rarely, only for the one
judgment call that benefits from deeper reasoning.

- **`llm`** (config.yaml) — fast model (e.g. `qwen3:4b`), fully fits in
  4GB VRAM with no CPU offload. Drives `ReasoningEngine`: hypothesis
  generation, per-cycle reasoning, decisions. Runs every cycle.
- **`llm_deep`** (config.yaml) — larger model (e.g. `qwen3:8b`), used for
  two things only:
  1. **`src/reasoning/impact_assessor.py`** — the `clear_impact` judgment
     in `VerificationEngine` (previously hardcoded `False`, meaning
     nothing could ever reach `verified=True`). `ImpactAssessor` asks the
     deep model to judge, like an experienced pentester, whether gathered
     evidence shows real, demonstrated impact — not just a plausible
     signal. Escalation is gated by `verification.min_confidence_for_deep_review`
     in config.yaml: only hypotheses that already cleared a confidence bar
     *and* whose tool run actually completed trigger the deep-model call,
     so it stays rare (bounded latency/heat) rather than firing every cycle.
     Fails **closed** on any error — `clear_impact` stays `False` rather
     than risk a false "verified" finding.
  2. **Learning Engine extraction** (`scripts/run_learning_pipeline.py`,
     `--learn-knowledge`) — this runs offline/infrequently, so extraction
     quality matters more than latency here.

If `llm_deep` isn't set in config, everything falls back to the `llm`
(fast) model's settings — this is additive, not a breaking change.



- Anything resembling a crawler/scraper — that's the Knowledge Collector's job.
- Browser automation engine (Vol VIII) — stub only, extend `src/dispatcher/`
  with a Playwright-backed controller when you're ready for it.
- CVE/JWT local tools, YAML-registry extensions, recon-runner API/auth
  discovery — you already have these; this build extends the AI Brain +
  memory + knowledge layers around them, doesn't replace them.

## Tests

```bash
pytest tests/
```
