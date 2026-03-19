from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List
from urllib.error import URLError
from urllib.request import urlopen


@dataclass(frozen=True)
class DocumentSource:
    """
    source_type: can be ambiguous(text, file, url, etc)
    """
    source_type: str
    value: str
    name: str | None = None


@dataclass(frozen=True)
class Document:
    source_name: str
    content: str


def ingest_sources(sources: Iterable[DocumentSource]) -> List[Document]:
    documents: List[Document] = []
    for source in sources:
        if source.source_type == "text":
            documents.append(
                Document(
                    source_name=source.name or "inline_text",
                    content=source.value.strip(),
                )
            )
            continue

        if source.source_type == "file":
            documents.append(_ingest_file(source))
            continue

        if source.source_type == "url":
            documents.append(_ingest_url(source))
            continue

        raise ValueError(f"Unsupported source type: {source.source_type}")

    return [doc for doc in documents if doc.content]


def merge_documents(documents: Iterable[Document]) -> str:
    parts: List[str] = []
    for doc in documents:
        parts.append(f"## Source: {doc.source_name}\n{doc.content.strip()}")
    return "\n\n".join(parts).strip()


def _ingest_file(source: DocumentSource) -> Document:
    path = Path(source.value).expanduser().resolve()
    content = path.read_text(encoding="utf-8")
    return Document(source_name=source.name or path.name, content=content)


def _ingest_url(source: DocumentSource) -> Document:
    try:
        with urlopen(source.value, timeout=10) as response:
            raw = response.read().decode("utf-8", errors="ignore")
    except URLError as exc:
        raise ValueError(f"Failed to fetch URL {source.value}: {exc}") from exc

    return Document(source_name=source.name or source.value, content=raw)
