from __future__ import annotations

import re

from .graph_schema import Entity, KnowledgeGraph, Relationship
from cognition_store.ingestion.claim_extractor import Claim
from cognition_store.ingestion.evidence_indexer import EvidenceItem


def build_synthetic_agentshield_graph() -> KnowledgeGraph:
    evidence = [
        {"id": "ev_001", "summary": "Synthetic SME target worries about downtime and vendor trust."},
        {"id": "ev_002", "summary": "AgentShield is positioned as an audit-first defensive security offer."},
    ]
    entities = [
        Entity("org_target", "organization", "Synthetic Target Company", ["ev_001"]),
        Entity("role_ceo", "person_role", "CEO", ["ev_001"]),
        Entity("role_it", "person_role", "IT Lead", ["ev_001"]),
        Entity("offer_agentshield", "product", "AgentShield Audit", ["ev_002"]),
        Entity("risk_downtime", "risk", "Operational Downtime", ["ev_001"]),
        Entity("risk_vendor_trust", "risk", "Vendor Trust Gap", ["ev_001"]),
    ]
    relationships = [
        Relationship("role_ceo", "offer_agentshield", "approves", ["ev_001"], 0.6),
        Relationship("role_it", "offer_agentshield", "evaluates", ["ev_001", "ev_002"], 0.8),
        Relationship("risk_downtime", "role_ceo", "creates_urgency", ["ev_001"], 0.75),
        Relationship("risk_vendor_trust", "offer_agentshield", "blocks", ["ev_001"], 0.8),
    ]
    claims = [
        {"id": "claim_001", "text": "Audit-first positioning reduces adoption risk.", "evidence_refs": ["ev_002"], "confidence": 0.72}
    ]
    return KnowledgeGraph("kg_agentshield_synthetic", entities, relationships, claims, evidence)


def build_synthetic_energy_graph() -> KnowledgeGraph:
    evidence = [
        {"id": "ev_energy_001", "summary": "Synthetic crude desk scenario has supply uncertainty, payment risk, and terminal timing pressure."},
        {"id": "ev_energy_002", "summary": "Market intelligence scenario tracks freight, compliance, and buyer demand as decision signals."},
    ]
    entities = [
        Entity("asset_crude_cargo", "asset", "Synthetic Crude Cargo", ["ev_energy_001"]),
        Entity("risk_supply", "risk", "Supply Confirmation Risk", ["ev_energy_001"]),
        Entity("risk_payment", "risk", "Payment Instrument Risk", ["ev_energy_001"]),
        Entity("risk_terminal", "risk", "Terminal Timing Risk", ["ev_energy_001", "ev_energy_002"]),
        Entity("signal_freight", "market_signal", "Freight Pressure", ["ev_energy_002"]),
        Entity("signal_buyer_demand", "market_signal", "Buyer Demand Shift", ["ev_energy_002"]),
        Entity("control_compliance", "control", "KYC and Sanctions Review", ["ev_energy_002"]),
    ]
    relationships = [
        Relationship("risk_supply", "asset_crude_cargo", "blocks_confidence", ["ev_energy_001"], 0.78),
        Relationship("risk_payment", "asset_crude_cargo", "blocks_execution", ["ev_energy_001"], 0.74),
        Relationship("risk_terminal", "asset_crude_cargo", "raises_cost", ["ev_energy_001", "ev_energy_002"], 0.7),
        Relationship("signal_freight", "asset_crude_cargo", "changes_margin", ["ev_energy_002"], 0.66),
        Relationship("signal_buyer_demand", "asset_crude_cargo", "changes_urgency", ["ev_energy_002"], 0.68),
        Relationship("control_compliance", "risk_payment", "reduces", ["ev_energy_002"], 0.72),
    ]
    claims = [
        {"id": "claim_energy_001", "text": "A trade should remain gated until supply, compliance, logistics, and payment evidence align.", "evidence_refs": ["ev_energy_001", "ev_energy_002"], "confidence": 0.74}
    ]
    return KnowledgeGraph("kg_energy_synthetic", entities, relationships, claims, evidence)


def _entity_id(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return f"ent_{slug[:48]}" if slug else "ent_unknown"


def build_graph_from_evidence(graph_id: str, evidence: list[EvidenceItem], claims: list[Claim]) -> KnowledgeGraph:
    entities_by_id: dict[str, Entity] = {}

    def add_entity(entity_type: str, name: str, evidence_ref: str, confidence: float = 0.65) -> str:
        entity_id = _entity_id(f"{entity_type}_{name}")
        if entity_id not in entities_by_id:
            entities_by_id[entity_id] = Entity(entity_id, entity_type, name, [evidence_ref], confidence)
        elif evidence_ref not in entities_by_id[entity_id].evidence_refs:
            entities_by_id[entity_id].evidence_refs.append(evidence_ref)
        return entity_id

    relationships: list[Relationship] = []
    offer_id = add_entity("product", "AgentShield", "system")

    for item in evidence:
        keywords = set(item.keywords)
        if "budget" in keywords or "procurement" in keywords:
            blocker = add_entity("blocker", "Budget or Procurement Friction", item.evidence_id)
            relationships.append(Relationship(blocker, offer_id, "blocks", [item.evidence_id], 0.65))
        if "downtime" in keywords or "operations" in keywords:
            risk = add_entity("risk", "Operational Downtime", item.evidence_id)
            relationships.append(Relationship(risk, offer_id, "creates_urgency_for", [item.evidence_id], 0.68))
        if "security" in keywords or "audit" in keywords or "compliance" in keywords:
            value = add_entity("pain_point", "Security and Compliance Exposure", item.evidence_id)
            relationships.append(Relationship(offer_id, value, "reduces", [item.evidence_id], 0.7))
        if "vendor" in keywords or "trust" in keywords:
            trust = add_entity("blocker", "Vendor Trust Gap", item.evidence_id)
            relationships.append(Relationship(trust, offer_id, "blocks", [item.evidence_id], 0.66))

    return KnowledgeGraph(
        graph_id=graph_id,
        entities=list(entities_by_id.values()),
        relationships=relationships,
        claims=[claim.to_dict() for claim in claims],
        evidence_refs=[item.to_dict() for item in evidence],
    )


def build_energy_graph_from_evidence(graph_id: str, evidence: list[EvidenceItem], claims: list[Claim]) -> KnowledgeGraph:
    entities_by_id: dict[str, Entity] = {}

    def add_entity(entity_type: str, name: str, evidence_ref: str, confidence: float = 0.65) -> str:
        entity_id = _entity_id(f"{entity_type}_{name}")
        if entity_id not in entities_by_id:
            entities_by_id[entity_id] = Entity(entity_id, entity_type, name, [evidence_ref], confidence)
        elif evidence_ref not in entities_by_id[entity_id].evidence_refs:
            entities_by_id[entity_id].evidence_refs.append(evidence_ref)
        return entity_id

    cargo_id = add_entity("asset", "Crude Cargo Opportunity", "system", 0.6)
    relationships: list[Relationship] = []

    for item in evidence:
        keywords = set(item.keywords)
        if {"supply", "allocation", "seller", "cargo", "crude"} & keywords:
            supply = add_entity("market_signal", "Supply Confirmation", item.evidence_id)
            relationships.append(Relationship(supply, cargo_id, "changes_supply_confidence", [item.evidence_id], 0.68))
        if {"buyer", "demand", "price", "margin"} & keywords:
            demand = add_entity("market_signal", "Buyer Demand and Margin Signal", item.evidence_id)
            relationships.append(Relationship(demand, cargo_id, "changes_commercial_urgency", [item.evidence_id], 0.66))
        if {"logistics", "freight", "terminal", "laycan"} & keywords:
            logistics = add_entity("risk", "Logistics and Terminal Timing Risk", item.evidence_id)
            relationships.append(Relationship(logistics, cargo_id, "can_erode_margin", [item.evidence_id], 0.7))
        if {"payment", "lc", "escrow"} & keywords:
            payment = add_entity("risk", "Payment Instrument Risk", item.evidence_id)
            relationships.append(Relationship(payment, cargo_id, "blocks_execution", [item.evidence_id], 0.72))
        if {"kyc", "sanctions", "counterparty", "compliance"} & keywords:
            compliance = add_entity("control", "KYC Sanctions and Counterparty Review", item.evidence_id)
            relationships.append(Relationship(compliance, cargo_id, "gates_decision", [item.evidence_id], 0.75))

    return KnowledgeGraph(
        graph_id=graph_id,
        entities=list(entities_by_id.values()),
        relationships=relationships,
        claims=[claim.to_dict() for claim in claims],
        evidence_refs=[item.to_dict() for item in evidence],
    )
