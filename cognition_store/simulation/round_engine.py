from __future__ import annotations

from pathlib import Path

from .event_log import ActionEvent, append_event


def run_bounded_agentshield_rounds(run_id: str, personas: list[dict], actions_path: Path, max_rounds: int = 4) -> list[dict]:
    events: list[dict] = []
    for round_no in range(1, max_rounds + 1):
        for persona in personas:
            role = persona["role"]
            if "Finance" in role:
                summary = "Budget concern remains unless entry offer is clearly scoped."
                delta = {"budget": -0.08, "trust": 0.02}
            elif "IT" in role or "Security" in role:
                summary = "Technical trust improves if audit is read-only and evidence-backed."
                delta = {"technical_fit": 0.08, "trust": 0.05}
            elif "CEO" in role:
                summary = "Business urgency rises when downtime risk is tied to revenue impact."
                delta = {"urgency": 0.08, "trust": 0.03}
            else:
                summary = "Operational acceptance depends on low-disruption implementation."
                delta = {"implementation_risk": -0.04, "trust": 0.02}
            event = ActionEvent(
                event_id=f"evt_{round_no}_{persona['persona_id']}",
                run_id=run_id,
                round=round_no,
                persona_id=persona["persona_id"],
                action_type="belief_update",
                target="agentshield_adoption",
                content_summary=summary,
                evidence_refs=["ev_001", "ev_002"],
                belief_delta=delta,
                confidence=0.7,
            )
            append_event(actions_path, event)
            events.append(event.to_dict())
    return events


def run_bounded_energy_rounds(run_id: str, personas: list[dict], actions_path: Path, max_rounds: int = 4) -> list[dict]:
    events: list[dict] = []
    for round_no in range(1, max_rounds + 1):
        for persona in personas:
            role = persona["role"]
            if "Compliance" in role:
                summary = "Execution remains gated until KYC, sanctions, and document chain evidence are complete."
                delta = {"execution_readiness": -0.1, "compliance_confidence": 0.08}
            elif "Finance" in role:
                summary = "Payment instrument risk limits commitment until escrow, LC, or verified settlement terms are defined."
                delta = {"margin_confidence": -0.04, "payment_confidence": 0.06}
            elif "Logistics" in role:
                summary = "Terminal timing and freight exposure can erode margin if laycan assumptions are weak."
                delta = {"logistics_confidence": -0.06, "margin_confidence": -0.03}
            elif "Trader" in role:
                summary = "Commercial upside improves only when supply confirmation and buyer demand align."
                delta = {"deal_urgency": 0.07, "supply_confidence": 0.04}
            else:
                summary = "Market signal remains useful but weak without corroborated freight, demand, and counterparty evidence."
                delta = {"signal_confidence": 0.05, "execution_readiness": -0.03}
            event = ActionEvent(
                event_id=f"evt_{round_no}_{persona['persona_id']}",
                run_id=run_id,
                round=round_no,
                persona_id=persona["persona_id"],
                action_type="belief_update",
                target="crude_market_decision",
                content_summary=summary,
                evidence_refs=["ev_energy_001", "ev_energy_002"],
                belief_delta=delta,
                confidence=0.68,
            )
            append_event(actions_path, event)
            events.append(event.to_dict())
    return events
