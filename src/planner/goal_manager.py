"""Goal Manager — Vol II Ch6, Vol V Ch3.

Parses scope/rules, tracks progress, is the single source of truth for
"is this target allowed". No testing begins until scope is understood.
"""
from __future__ import annotations
import fnmatch
from ..logging_setup import get_logger

log = get_logger("planner.goal_manager")


class GoalManager:
    def __init__(self, scope: dict):
        self.program_name = scope.get("program_name", "unknown")
        self.in_scope = scope.get("in_scope", [])
        self.out_of_scope = scope.get("out_of_scope", [])
        self.forbidden_techniques = set(scope.get("forbidden_techniques", []))
        self.rate_limit_rps = scope.get("rate_limit", {}).get("requests_per_second", 5)
        self.coverage: dict[str, bool] = {}  # area -> tested

        if not self.in_scope:
            raise ValueError("Scope file has no in_scope entries — refusing to start")

        # Fail loudly HERE, with a message pointing at the actual mistake,
        # rather than crashing deep inside fnmatch on the first cycle with
        # a cryptic "expected str, ... not list" TypeError. The most common
        # real cause: an indentation slip in scope.yaml that nests a list
        # inside in_scope/out_of_scope instead of a flat list of strings, e.g.
        #   in_scope:
        #     -                        # WRONG — nests a list inside a list
        #       - "192.168.56.101"
        #       - "192.168.56.102"
        # instead of
        #   in_scope:
        #     - "192.168.56.101"
        #     - "192.168.56.102"
        for field_name, entries in (("in_scope", self.in_scope), ("out_of_scope", self.out_of_scope)):
            for entry in entries:
                if not isinstance(entry, str):
                    raise ValueError(
                        f"scope.yaml's '{field_name}' must be a flat list of strings, but found "
                        f"a {type(entry).__name__} ({entry!r}) instead. This is usually a YAML "
                        f"indentation mistake — check for an accidentally nested list under "
                        f"'{field_name}:'."
                    )

    def is_in_scope(self, target: str) -> bool:
        for pattern in self.out_of_scope:
            if fnmatch.fnmatch(target, pattern):
                return False
        for pattern in self.in_scope:
            if fnmatch.fnmatch(target, pattern):
                return True
        return False

    def is_technique_allowed(self, technique: str) -> bool:
        return technique not in self.forbidden_techniques

    def mark_tested(self, area: str):
        self.coverage[area] = True

    def coverage_percent(self, all_areas: list[str]) -> float:
        if not all_areas:
            return 0.0
        tested = sum(1 for a in all_areas if self.coverage.get(a))
        return round(100 * tested / len(all_areas), 1)
