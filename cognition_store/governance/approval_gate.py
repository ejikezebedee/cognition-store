from __future__ import annotations


APPROVAL_GATED_ACTIONS = {
    "production_change",
    "external_communication",
    "financial_action",
    "contract_action",
    "identity_change",
    "governance_change",
    "system_service_change",
    "sensitive_data_use",
}


def requires_approval(action_type: str) -> bool:
    return action_type in APPROVAL_GATED_ACTIONS

