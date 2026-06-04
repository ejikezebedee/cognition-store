from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class Persona:
    persona_id: str
    domain: str
    role: str
    authority_level: int
    risk_tolerance: int
    budget_sensitivity: int
    technical_depth: int
    trust_bias: str
    primary_goals: list[str] = field(default_factory=list)
    private_concerns: list[str] = field(default_factory=list)
    decision_weight: float = 1.0

    def to_dict(self) -> dict:
        return asdict(self)

