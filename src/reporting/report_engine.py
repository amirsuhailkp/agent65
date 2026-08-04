"""Report Engine — Vol II Ch17, Vol IX Ch9-11.

Pipeline: Evidence -> Normalization -> Finding Builder -> Template -> Markdown/HTML/JSON
Severity stays a human review point (Vol IX 'Severity Assessment') — this
engine never auto-assigns final severity, only drafts it for review.
"""
from __future__ import annotations
import json
import datetime as dt
from pathlib import Path
from dataclasses import dataclass

GENERIC_TEMPLATE = """# {title}

**Category:** {category}
**Draft Severity (human review required):** {severity}
**Confidence:** {confidence}
**Verified:** {verified}
**Date:** {date}

## Summary
{description}

## Steps to Reproduce
{steps_to_reproduce}

## Impact
{impact}

## Remediation
{remediation}

## Evidence References
{evidence_refs}
"""


@dataclass
class FindingDraft:
    title: str
    category: str
    severity: str
    confidence: float
    verified: bool
    description: str
    steps_to_reproduce: str
    impact: str
    remediation: str
    evidence_refs: list[str]


class ReportEngine:
    def __init__(self, reports_dir: str):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def render_markdown(self, finding: FindingDraft) -> str:
        return GENERIC_TEMPLATE.format(
            title=finding.title,
            category=finding.category,
            severity=finding.severity,
            confidence=round(finding.confidence, 2),
            verified=finding.verified,
            date=dt.datetime.utcnow().strftime("%Y-%m-%d"),
            description=finding.description,
            steps_to_reproduce=finding.steps_to_reproduce,
            impact=finding.impact,
            remediation=finding.remediation,
            evidence_refs="\n".join(f"- {r}" for r in finding.evidence_refs) or "- none",
        )

    def export(self, finding: FindingDraft, fmt: str = "markdown") -> str:
        # Strip everything except alphanumerics/underscore/hyphen. A raw
        # ":" from a title like "IDOR: blog page leaks..." would crash
        # Path.write_text on Windows (invalid filename character) — this
        # runs on the operator's Windows host, not just the Kali VM.
        import re
        slug = re.sub(r"[^a-z0-9]+", "_", finding.title.lower()).strip("_")[:60]
        ts = dt.datetime.utcnow().strftime("%Y%m%d%H%M%S")

        if fmt == "markdown":
            content = self.render_markdown(finding)
            path = self.reports_dir / f"{ts}_{slug}.md"
            path.write_text(content, encoding="utf-8")
        elif fmt == "json":
            content = json.dumps(finding.__dict__, indent=2)
            path = self.reports_dir / f"{ts}_{slug}.json"
            path.write_text(content, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported format: {fmt}")

        return str(path)