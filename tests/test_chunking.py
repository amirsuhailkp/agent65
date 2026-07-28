from src.knowledge.repository import RawKnowledgeDoc
from src.knowledge.chunking import chunk_document


def _doc(doc_id="d1"):
    return RawKnowledgeDoc(
        doc_id=doc_id, title="Test Doc", source="unit-test", category="test",
        tags=[], trust_level="verified", technology="",
    )


def test_chunk_document_splits_by_heading():
    section_a = "# Heading A\n" + ("Filler sentence about topic A. " * 15)
    section_b = "# Heading B\n" + ("Filler sentence about topic B. " * 15)
    chunks = chunk_document(_doc(), f"{section_a}\n\n{section_b}")
    assert len(chunks) >= 2
    assert all(c.doc_id == "d1" for c in chunks)


def test_chunk_document_merges_tiny_trailing_section():
    content = "# Heading A\nsome text here\n\n# Heading B\nmore text"
    chunks = chunk_document(_doc("d3"), content)
    assert len(chunks) == 1
    assert "Heading A" in chunks[0].text and "Heading B" in chunks[0].text


def test_chunk_document_keeps_code_block_intact():
    code = "```python\nprint('hello')\n```"
    chunks = chunk_document(_doc("d2"), f"# Snippet\n{code}")
    joined = "\n".join(c.text for c in chunks)
    assert code in joined
