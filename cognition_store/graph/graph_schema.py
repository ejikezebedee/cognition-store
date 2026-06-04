from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class Entity:
    id: str
    type: str
    name: str
    evidence_refs: list[str] = field(default_factory=list)
    confidence: float = 0.7


@dataclass
class Relationship:
    source: str
    target: str
    type: str
    evidence_refs: list[str] = field(default_factory=list)
    confidence: float = 0.7


@dataclass
class KnowledgeGraph:
    graph_id: str
    entities: list[Entity]
    relationships: list[Relationship]
    claims: list[dict]
    evidence_refs: list[dict]

    def to_dict(self) -> dict:
        return {
            "graph_id": self.graph_id,
            "entities": [asdict(entity) for entity in self.entities],
            "relationships": [asdict(rel) for rel in self.relationships],
            "claims": self.claims,
            "evidence_refs": self.evidence_refs,
        }

