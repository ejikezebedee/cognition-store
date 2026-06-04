from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass
class RunManifest:
    run_id: str
    domain: str
    question: str
    max_rounds: int
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    guardrails: list[str] = field(default_factory=lambda: [
        "decision_support_only",
        "no_external_action",
        "no_plaintext_secrets",
        "clean_room_no_agpl_code",
    ])

    def to_dict(self) -> dict:
        return asdict(self)

