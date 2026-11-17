from __future__ import annotations

from pathlib import Path

from rag_eval.models import Document

SUPPORTED = {".txt", ".md", ".pdf", ".pptx"}


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix == ".pptx":
        return _extract_pptx(path)
    raise ValueError(f"formato no soportado: {suffix}")


def _extract_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        sidecar = path.with_suffix(".txt")
        if sidecar.exists():
            return sidecar.read_text(encoding="utf-8")
        raise RuntimeError(
            "pypdf no instalado y no hay sidecar .txt para el PDF"
        ) from None
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _extract_pptx(path: Path) -> str:
    try:
        from pptx import Presentation
    except ImportError:
        sidecar = path.with_suffix(".txt")
        if sidecar.exists():
            return sidecar.read_text(encoding="utf-8")
        raise RuntimeError(
            "python-pptx no instalado y no hay sidecar .txt"
        ) from None
    prs = Presentation(str(path))
    parts: list[str] = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text:
                parts.append(shape.text)
    return "\n".join(parts)


def load_corpus(docs_dir: str | Path) -> list[Document]:
    root = Path(docs_dir)
    docs: list[Document] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED:
            continue
        if path.suffix.lower() in {".pdf", ".pptx"} and path.with_suffix(".txt").exists():
            continue
        text = extract_text(path)
        docs.append(Document(doc_id=path.stem, path=str(path), text=text))
    return docs
