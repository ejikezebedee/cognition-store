from __future__ import annotations


def build_verdict(run_id: str, domain: str, question: str, events: list[dict]) -> dict:
    blockers = []
    opportunities = []
    for event in events:
        text = event.get("content_summary", "")
        if "Budget concern" in text:
            blockers.append("Finance may block if pricing and scope are not controlled.")
        if "read-only" in text:
            opportunities.append("Lead with read-only audit posture and evidence-backed findings.")
        if "downtime" in text:
            opportunities.append("Tie AgentShield to downtime prevention and business continuity.")
    return {
        "run_id": run_id,
        "domain": domain,
        "question": question,
        "overall_verdict": "AgentShield adoption is plausible if positioned as low-disruption, read-only, evidence-backed, and tightly scoped.",
        "confidence": 0.72,
        "consensus_score": 0.68,
        "disagreement_score": 0.32,
        "risk_drawdown": [
            "Use audit-first scope before managed-service upsell.",
            "Avoid asking for broad access in the first conversation.",
            "Show business impact, not only technical findings."
        ],
        "top_blockers": sorted(set(blockers)),
        "top_opportunities": sorted(set(opportunities)),
        "recommended_actions": [
            "Open with downtime and compliance risk.",
            "Offer a fixed-scope defensive audit.",
            "Prepare technical proof for IT and cost control for finance."
        ],
        "evidence_refs": ["ev_001", "ev_002"],
        "assumptions": ["Synthetic target data only; live company data not used."],
        "invalid_or_weak_claims": []
    }


def build_energy_verdict(run_id: str, question: str, events: list[dict]) -> dict:
    blockers = []
    opportunities = []
    for event in events:
        text = event.get("content_summary", "")
        if "KYC" in text or "sanctions" in text:
            blockers.append("Compliance must gate any trade simulation before commercial commitment.")
        if "Payment instrument" in text:
            blockers.append("Payment terms remain a core execution risk.")
        if "Terminal timing" in text:
            blockers.append("Freight, laycan, and terminal assumptions can erode margin.")
        if "Commercial upside" in text:
            opportunities.append("Prioritize scenarios where supply confirmation and buyer demand converge.")
        if "Market signal" in text:
            opportunities.append("Use market signals only after corroboration across freight, demand, and counterparty evidence.")
    return {
        "run_id": run_id,
        "domain": "energy_crude_oil",
        "question": question,
        "overall_verdict": "Synthetic crude market opportunity should remain gated until supply, compliance, logistics, and payment evidence are aligned.",
        "confidence": 0.7,
        "consensus_score": 0.64,
        "disagreement_score": 0.36,
        "risk_drawdown": [
            "Require document-chain completeness before decision escalation.",
            "Separate market-signal intelligence from trade execution authority.",
            "Model freight, laycan, payment, and compliance as independent gates."
        ],
        "top_blockers": sorted(set(blockers)),
        "top_opportunities": sorted(set(opportunities)),
        "recommended_actions": [
            "Keep module local and decision-support only.",
            "Collect approved evidence into the knowledge graph before simulation.",
            "Escalate any live trade, finance, contract, or counterparty action for explicit approval."
        ],
        "evidence_refs": ["ev_energy_001", "ev_energy_002"],
        "assumptions": ["Synthetic energy-market scenario only; no live market data, counterparty data, finance action, or contract action used."],
        "invalid_or_weak_claims": []
    }


def build_energy_intelligence_report(run_id: str, question: str, events: list[dict], evidence: list[dict], claims: list[dict]) -> dict:
    verdict = build_energy_verdict(run_id, question, events)
    claim_types = sorted({claim.get("claim_type", "unknown") for claim in claims})
    evidence_keywords = sorted({keyword for item in evidence for keyword in item.get("keywords", [])})
    gates = []
    if {"kyc", "sanctions", "counterparty", "compliance"} & set(evidence_keywords):
        gates.append("compliance_gate")
    if {"payment", "lc", "escrow"} & set(evidence_keywords):
        gates.append("payment_gate")
    if {"logistics", "freight", "terminal", "laycan"} & set(evidence_keywords):
        gates.append("logistics_gate")
    if {"supply", "allocation", "seller", "cargo"} & set(evidence_keywords):
        gates.append("supply_confirmation_gate")
    verdict["intelligence_summary"] = {
        "evidence_count": len(evidence),
        "claim_count": len(claims),
        "claim_types": claim_types,
        "detected_keywords": evidence_keywords,
        "approval_gates": gates or ["manual_review_gate"],
    }
    verdict["recommended_actions"] = [
        "Keep this as decision-support intelligence until an authorized reviewer explicitly approves any live action.",
        "Verify supply, counterparty, compliance, logistics, and payment evidence independently.",
        "Separate market opportunity scoring from trade execution authority.",
    ]
    verdict["assumptions"] = ["Simulation used approved local files only; no live market data, trading, finance, counterparty contact, or contract action used."]
    verdict["evidence_refs"] = [item.get("evidence_id", "") for item in evidence[:10]]
    return verdict
