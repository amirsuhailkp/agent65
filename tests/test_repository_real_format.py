"""Regression test against your actual Knowledge Collector output format —
catches drift if the collector's front-matter schema ever changes."""
from pathlib import Path
from src.knowledge.repository import KnowledgeRepository

FIXTURES = Path(__file__).parent / "fixtures" / "processed"


def test_repository_parses_real_collector_front_matter():
    repo = KnowledgeRepository(str(FIXTURES))
    docs = list(repo.iter_documents())
    assert len(docs) == 1

    doc, body = docs[0]
    assert doc.title == "A01:2021 – Broken Access Control"
    assert doc.source == "owasp.org"
    assert doc.category == "web-security"
    assert "access" in doc.tags
    assert doc.trust_level == "verified"  # collector == "owasp" is in the trusted set
    assert body.strip().startswith("# A01:2021")


def test_repository_marks_unknown_collectors_unverified(tmp_path):
    sample = tmp_path / "unknown-source.md"
    sample.write_text(
        "---\n"
        "title: Some Blog Post\n"
        "source: randomblog.example\n"
        "url: https://randomblog.example/post\n"
        "collector: single_page\n"
        "category: uncategorized\n"
        "tags: []\n"
        "date_collected: '2026-01-01T00:00:00Z'\n"
        "language: en\n"
        "---\n\n"
        "# Some Blog Post\nbody text\n",
        encoding="utf-8",
    )
    repo = KnowledgeRepository(str(tmp_path))
    [(doc, _)] = list(repo.iter_documents())
    assert doc.trust_level == "unverified"
