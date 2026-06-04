from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from cognition_store.storage.json_store import append_jsonl


@dataclass
class ActionEvent:
    event_id: str
    run_id: str
    round: int
    persona_id: str
    action_type: str
    target: str
    content_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    belief_delta: dict = field(default_factory=dict)
    confidence: float = 0.5
    created_at: str = ""

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["created_at"] = payload["created_at"] or datetime.now(timezone.utc).isoformat()
        return payload


def append_event(path: Path, event: ActionEvent) -> None:
    append_jsonl(path, event.to_dict())

