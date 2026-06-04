from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class SourceRecord:
    source_id: str
    path: str
    sha256: str
    size_bytes: int
    approved_for_simulation: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_source_record(path: Path, source_id: str) -> SourceRecord:
    resolved = path.resolve()
    return SourceRecord(
        source_id=source_id,
        path=str(path),
        sha256=file_sha256(resolved),
        size_bytes=resolved.stat().st_size,
    )

