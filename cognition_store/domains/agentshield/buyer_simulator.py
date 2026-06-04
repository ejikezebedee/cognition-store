from __future__ import annotations

from pathlib import Path

from cognition_store.domains.agentshield.buyer_committee import run_from_documents
from cognition_store.ingestion.claim_extractor import Claim
from cognition_store.ingestion.document_loader import load_documents
from cognition_store.ingestion.evidence_indexer import EvidenceItem, index_evidence
from cognition_store.personas.persona_generator import generate_agentshield_committee
from cognition_store.storage.json_store import write_json


def _contains_any(items: list[str], options: set[str]) -> bool:
    return bool(set(items) & options)


def _committee_member(persona: dict, evidence: list[EvidenceItem]) -> dict:
    keywords = {keyword for item in evidence for keyword in item.keywords}
    role = persona["role"]
    likely_objections = list(persona.get("private_concerns", []))
    if role == "CEO" and _contains_any(list(keywords), {"downtime", "risk", "operations"}):
        likely_objections.append("Needs a direct revenue-continuity business case.")
    if role == "IT Lead" and _contains_any(list(keywords), {"security", "audit", "vendor", "trust"}):
        likely_objections.append("Needs read-only scope, access boundaries, and proof of technical competence.")
    if role == "Security Reviewer" and _contains_any(list(keywords), {"compliance", "security", "audit"}):
        likely_objections.append("Needs evidence quality, defensible findings, and no inflated claims.")
    if role == "Finance Controller" and _contains_any(list(keywords), {"budget", "approval", "procurement"}):
        likely_objections.append("Needs fixed price, defined scope, and clear approval path.")
    if role == "Operations Manager" and _contains_any(list(keywords), {"downtime", "operations"}):
        likely_objections.append("Needs low-disruption scheduling and no workflow interruption.")

    return {
        "persona_id": persona["persona_id"],
        "role": role,
        "authority_level": persona["authority_level"],
        "decision_weight": persona["decision_weight"],
        "trust_bias": persona["trust_bias"],
        "primary_goals": persona.get("primary_goals", []),
        "likely_objections": sorted(set(likely_objections)),
        "recommended_handling": _handling_for_role(role),
    }


def _handling_for_role(role: str) -> str:
    if role == "CEO":
        return "Open with business continuity, downtime exposure, and executive risk reduction."
    if role == "IT Lead":
        return "Lead with read-only audit method, access limits, and technical evidence trail."
    if role == "Security Reviewer":
        return "Show defensible findings, proof standards, and remediation clarity."
    if role == "Finance Controller":
        return "Offer fixed-scope pricing, capped discovery, and clear budget justification."
    if role == "Operations Manager":
        return "Emphasize low disruption, scheduling control, and practical implementation."
    return "Address role-specific risk with evidence and bounded scope."


def _friction_map(evidence: list[EvidenceItem], claims: list[Claim]) -> dict:
    keywords = {keyword for item in evidence for keyword in item.keywords}
    friction = []
    if _contains_any(list(keywords), {"budget", "approval", "procurement"}):
        friction.append({"area": "budget", "severity": "high", "mitigation": "Use fixed-scope audit offer with clear deliverables and no open-ended spend."})
    if _contains_any(list(keywords), {"vendor", "trust"}):
        friction.append({"area": "vendor_trust", "severity": "high", "mitigation": "Use read-only access, written boundaries, and evidence-backed reporting."})
    if _contains_any(list(keywords), {"downtime", "operations"}):
        friction.append({"area": "operations", "severity": "medium", "mitigation": "Schedule low-impact discovery and avoid workflow disruption."})
    if _contains_any(list(keywords), {"security", "audit", "compliance"}):
        friction.append({"area": "technical_proof", "severity": "medium", "mitigation": "Show audit method, evidence chain, and remediation examples."})
    if not friction:
        friction.append({"area": "unknown", "severity": "medium", "mitigation": "Ask discovery questions before proposing access or price."})

    return {
        "friction_points": friction,
        "claim_types": sorted({claim.claim_type for claim in claims}),
    }


def _sales_recommendation(evidence: list[EvidenceItem], friction: dict) -> dict:
    areas = {item["area"] for item in friction["friction_points"]}
    pitch_parts = ["Position AgentShield as a defensive, read-only business-risk audit."]
    if "operations" in areas:
        pitch_parts.append("Tie the first conversation to downtime prevention and continuity.")
    if "vendor_trust" in areas:
        pitch_parts.append("Lead with access boundaries and evidence quality before asking for trust.")
    if "budget" in areas:
        pitch_parts.append("Keep the first offer fixed-scope and easy to approve.")
    if "technical_proof" in areas:
        pitch_parts.append("Prepare a technical proof pack for IT and security reviewers.")

    return {
        "best_pitch_angle": " ".join(pitch_parts),
        "recommended_first_offer": {
            "name": "AgentShield Read-Only Risk Snapshot",
            "scope": [
                "Approved local/company-provided evidence review",
                "Read-only security and operational risk audit",
                "Executive risk summary",
                "Technical findings appendix",
                "Prioritized remediation roadmap",
            ],
            "exclusions": [
                "No production changes",
                "No broad administrative access in the first engagement",
                "No external communication from the simulator",
                "No guaranteed breach or compliance claims",
            ],
        },
        "opening_questions": [
            "Which system downtime would create the fastest business loss?",
            "Who signs off on a fixed-scope security audit?",
            "What access boundaries would IT require before approving a review?",
            "Which compliance or customer-risk issue is most urgent this quarter?",
        ],
        "follow_up_assets": [
            "One-page executive risk brief",
            "Read-only audit scope sheet",
            "Technical evidence-handling note",
            "Fixed-scope commercial offer",
        ],
    }


def build_buyer_simulation_report(target_name: str, evidence: list[EvidenceItem], claims: list[Claim], base_result: dict) -> dict:
    personas = [persona.to_dict() for persona in generate_agentshield_committee()]
    committee = [_committee_member(persona, evidence) for persona in personas]
    friction = _friction_map(evidence, claims)
    recommendation = _sales_recommendation(evidence, friction)
    return {
        "target_name": target_name,
        "domain": "agentshield_sales",
        "committee_map": sorted(committee, key=lambda item: item["decision_weight"], reverse=True),
        "sales_friction": friction,
        "sales_recommendation": recommendation,
        "simulation_verdict": base_result["verdict"],
        "guardrails": [
            "local_files_only",
            "decision_support_only",
            "no_live_outreach",
            "no_external_scan",
            "no_host_deployment",
        ],
    }


def run_buyer_simulator(paths: list[Path], output_root: Path, target_name: str, run_id: str = "agentshield_buyer_sim") -> dict:
    documents = load_documents(paths)
    evidence = index_evidence(documents)
    if not evidence:
        raise RuntimeError("No AgentShield-relevant evidence extracted from supplied target notes")
    from cognition_store.ingestion.claim_extractor import extract_claims

    claims = extract_claims(evidence)
    base_result = run_from_documents(paths, output_root, run_id)
    run_dir = output_root / run_id
    buyer_report = build_buyer_simulation_report(target_name, evidence, claims, base_result)
    write_json(run_dir / "buyer_simulation.json", buyer_report)
    write_json(
        run_dir / "sales_brief.json",
        {
            "target_name": target_name,
            "best_pitch_angle": buyer_report["sales_recommendation"]["best_pitch_angle"],
            "recommended_first_offer": buyer_report["sales_recommendation"]["recommended_first_offer"],
            "top_objections": [
                objection
                for member in buyer_report["committee_map"]
                for objection in member["likely_objections"]
            ][:12],
            "guardrails": buyer_report["guardrails"],
        },
    )
    return {
        "run_dir": str(run_dir),
        "target_name": target_name,
        "committee_count": len(buyer_report["committee_map"]),
        "friction_count": len(buyer_report["sales_friction"]["friction_points"]),
        "event_count": base_result["event_count"],
        "buyer_simulation": buyer_report,
    }
