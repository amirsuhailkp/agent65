"""Playbook Learning Engine — Agent Cyber Learning Engine Update.

Extends the existing Knowledge/Memory layers with a fifth capability:
the agent gets *better at investigating* over time without any model
retraining. The LLM stays the reasoning engine; this package only
builds structured, auditable knowledge around it.

Four independent layers (never collapse these together):

  1. Knowledge Database    -> already exists: src/knowledge/repository.py
                               (raw collector output, read-only, immutable)
  2. Observation Database  -> src/learning/db_models.py::Observation
                               (one document -> structured facts)
  3. Playbook Database     -> src/learning/db_models.py::Playbook
                               (many observations -> synthesized methodology)
  4. Experience Database   -> src/learning/db_models.py::Experience
                               (every real engagement -> future evidence)

Pipeline:  Raw Documents -> Structured Observations -> Playbooks -> Experience
           -> Better Planning

Entry point for everything else in the codebase: LearningEngine
(src/learning/learning_engine.py).
"""
from .learning_engine import LearningEngine

__all__ = ["LearningEngine"]
