from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cognition_store.governance.secret_redactor import redact_text
from cognition_store.governance.source_manifest import SourceRecord, build_source_record


SUPPORTED_SUFFIXES = {".txt", ".md"}


@dataclass
class LoadedDocument:
    source: SourceRecord
    text: str

    def to_dict(self) -> dict:
        return {"source": self.source.to_dict(), "text": self.text}


def load_document(path: Path, source_id: str) -> LoadedDocument:
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Unsupported document type: {path.suffix}")
    text = path.read_text(encoding="utf-8")
    return LoadedDocument(source=build_source_record(path, source_id), text=redact_text(text))


def load_documents(paths: list[Path]) -> list[LoadedDocument]:
    return [load_document(path, f"src_{index + 1:03d}") for index, path in enumerate(paths)]

