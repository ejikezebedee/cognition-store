from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from .document_loader import LoadedDocument


@dataclass
class EvidenceItem:
    evidence_id: str
    source_id: str
    text: str
    keywords: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


KEYWORDS = (
    "downtime",
    "compliance",
    "budget",
    "security",
    "audit",
    "vendor",
    "trust",
    "operations",
    "risk",
    "approval",
    "procurement",
    "energy",
    "crude",
    "cargo",
    "supply",
    "allocation",
    "logistics",
    "freight",
    "terminal",
    "laycan",
    "payment",
    "lc",
    "escrow",
    "kyc",
    "sanctions",
    "buyer",
    "seller",
    "counterparty",
    "demand",
    "price",
    "margin",
)


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [part.strip() for part in parts if part.strip()]


def index_evidence(documents: list[LoadedDocument]) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    counter = 1
    for document in documents:
        for sentence in split_sentences(document.text):
            found = [keyword for keyword in KEYWORDS if keyword in sentence.lower()]
            if not found:
                continue
            evidence.append(
                EvidenceItem(
                    evidence_id=f"ev_{counter:03d}",
                    source_id=document.source.source_id,
                    text=sentence,
                    keywords=found,
                )
            )
            counter += 1
    return evidence
