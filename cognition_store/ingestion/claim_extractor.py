from __future__ import annotations

from dataclasses import asdict, dataclass

from .evidence_indexer import EvidenceItem


@dataclass
class Claim:
    claim_id: str
    text: str
    claim_type: str
    evidence_refs: list[str]
    confidence: float

    def to_dict(self) -> dict:
        return asdict(self)


def extract_claims(evidence: list[EvidenceItem]) -> list[Claim]:
    claims: list[Claim] = []
    for index, item in enumerate(evidence, start=1):
        keywords = set(item.keywords)
        if {"payment", "lc", "escrow"} & keywords:
            claim_type = "energy_payment_risk"
        elif {"kyc", "sanctions", "counterparty"} & keywords:
            claim_type = "energy_compliance_gate"
        elif {"logistics", "freight", "terminal", "laycan"} & keywords:
            claim_type = "energy_logistics_risk"
        elif {"supply", "allocation", "seller", "cargo"} & keywords:
            claim_type = "energy_supply_signal"
        elif {"buyer", "demand", "price", "margin", "energy", "crude"} & keywords:
            claim_type = "energy_market_signal"
        elif {"budget", "procurement"} & keywords:
            claim_type = "commercial_blocker"
        elif {"downtime", "operations"} & keywords:
            claim_type = "operational_risk"
        elif {"security", "audit", "compliance"} & keywords:
            claim_type = "security_value"
        else:
            claim_type = "general_signal"
        claims.append(
            Claim(
                claim_id=f"claim_{index:03d}",
                text=item.text,
                claim_type=claim_type,
                evidence_refs=[item.evidence_id],
                confidence=0.65,
            )
        )
    return claims
