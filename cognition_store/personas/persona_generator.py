from __future__ import annotations

from .persona_schema import Persona


def generate_agentshield_committee() -> list[Persona]:
    return [
        Persona("p_ceo", "agentshield_sales", "CEO", 5, 2, 3, 2, "trust_requires_business_case", ["reduce business risk"], ["unclear ROI"], 1.4),
        Persona("p_it", "agentshield_sales", "IT Lead", 4, 3, 2, 5, "trust_requires_technical_proof", ["avoid downtime"], ["vendor access risk"], 1.3),
        Persona("p_security", "agentshield_sales", "Security Reviewer", 4, 2, 2, 5, "trust_requires_evidence", ["reduce exposure"], ["false claims"], 1.2),
        Persona("p_finance", "agentshield_sales", "Finance Controller", 3, 3, 5, 2, "trust_requires_price_control", ["control spend"], ["hidden costs"], 1.0),
        Persona("p_ops", "agentshield_sales", "Operations Manager", 3, 4, 3, 3, "trust_requires_low_disruption", ["keep operations moving"], ["workflow interruption"], 0.9),
    ]


def generate_energy_market_panel() -> list[Persona]:
    return [
        Persona("p_trader", "energy_crude_oil", "Physical Crude Trader", 4, 4, 2, 3, "trust_requires_supply_confirmation", ["secure profitable cargo flow"], ["unverified allocation"], 1.3),
        Persona("p_logistics", "energy_crude_oil", "Logistics Coordinator", 3, 2, 3, 4, "trust_requires_route_clarity", ["avoid demurrage"], ["unclear terminal timing"], 1.1),
        Persona("p_compliance", "energy_crude_oil", "Compliance Reviewer", 5, 1, 2, 4, "trust_requires_document_chain", ["avoid sanctions and KYC risk"], ["weak counterparty documents"], 1.4),
        Persona("p_finance_energy", "energy_crude_oil", "Trade Finance Lead", 4, 2, 5, 3, "trust_requires_payment_security", ["protect working capital"], ["payment instrument risk"], 1.2),
        Persona("p_market_intel", "energy_crude_oil", "Market Intelligence Analyst", 3, 4, 2, 5, "trust_requires_multi_source_signal", ["detect price dislocation"], ["thin evidence"], 1.0),
    ]
