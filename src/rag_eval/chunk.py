from __future__ import annotations

from rag_eval.models import Chunk, Document


def chunk_document(doc: Document, size: int = 280, overlap: int = 40) -> list[Chunk]:
    text = " ".join(doc.text.split())
    if not text:
        return []
    chunks: list[Chunk] = []
    start = 0
    idx = 0
    step = max(size - overlap, 1)
    while start < len(text):
        end = min(start + size, len(text))
        piece = text[start:end]
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}:{idx}",
                doc_id=doc.doc_id,
                text=piece,
                start=start,
                end=end,
            )
        )
        if end == len(text):
            break
        start += step
        idx += 1
    return chunks


def chunk_corpus(docs: list[Document], size: int = 280, overlap: int = 40) -> list[Chunk]:
    out: list[Chunk] = []
    for doc in docs:
        out.extend(chunk_document(doc, size=size, overlap=overlap))
    return out
