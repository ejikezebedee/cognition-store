from __future__ import annotations

from pathlib import Path

from cognition_store.graph.graph_builder import build_energy_graph_from_evidence
from cognition_store.graph.graph_builder import build_synthetic_energy_graph
from cognition_store.graph.graph_validation import validate_graph
from cognition_store.ingestion.claim_extractor import extract_claims
from cognition_store.ingestion.document_loader import load_documents
from cognition_store.ingestion.evidence_indexer import index_evidence
from cognition_store.personas.persona_generator import generate_energy_market_panel
from cognition_store.reporting.verdict_schema import build_energy_intelligence_report
from cognition_store.reporting.verdict_schema import build_energy_verdict
from cognition_store.simulation.round_engine import run_bounded_energy_rounds
from cognition_store.simulation.run_manifest import RunManifest
from cognition_store.storage.json_store import write_json


def describe_energy_module() -> dict:
    return {
        "status": "planned",
        "scope": "private local Energy & Crude Oil Market Intelligence simulations",
        "guardrail": "decision support only; no auto-trading, auto-contact, auto-contract, or fund movement",
    }


def run_energy_demo(output_root: Path) -> dict:
    run_id = "energy_crude_oil_synthetic_demo"
    run_dir = output_root / run_id
    actions_path = run_dir / "actions.jsonl"
    if actions_path.exists():
        actions_path.unlink()
    graph = build_synthetic_energy_graph().to_dict()
    issues = validate_graph(graph)
    if issues:
        raise RuntimeError(f"Graph validation failed: {issues}")

    personas = [persona.to_dict() for persona in generate_energy_market_panel()]
    question = "Which synthetic crude-market frictions should block or delay deal escalation?"
    manifest = RunManifest(
        run_id=run_id,
        domain="energy_crude_oil",
        question=question,
        max_rounds=4,
    ).to_dict()
    manifest["execution_guardrail"] = "decision_support_only"
    write_json(run_dir / "manifest.json", manifest)
    write_json(run_dir / "knowledge_graph.json", graph)
    write_json(run_dir / "personas.json", personas)
    events = run_bounded_energy_rounds(run_id, personas, actions_path, max_rounds=4)
    verdict = build_energy_verdict(run_id, question, events)
    write_json(run_dir / "verdict.json", verdict)
    write_json(run_dir / "summary.json", {"run_id": run_id, "event_count": len(events), "verdict": verdict["overall_verdict"]})
    return {"run_dir": str(run_dir), "event_count": len(events), "verdict": verdict}


def build_deal_friction_report(evidence: list[dict], claims: list[dict], verdict: dict) -> dict:
    keywords = {keyword for item in evidence for keyword in item.get("keywords", [])}
    friction = []
    if {"kyc", "sanctions", "counterparty", "compliance"} & keywords:
        friction.append({"area": "compliance", "severity": "high", "gate": "Do not escalate until KYC, sanctions, and counterparty documents are verified."})
    if {"payment", "lc", "escrow"} & keywords:
        friction.append({"area": "payment", "severity": "high", "gate": "Do not treat the opportunity as executable until settlement instrument terms are verified."})
    if {"logistics", "freight", "terminal", "laycan"} & keywords:
        friction.append({"area": "logistics", "severity": "medium", "gate": "Model terminal timing, freight, and laycan exposure before margin assumptions."})
    if {"supply", "allocation", "seller", "cargo"} & keywords:
        friction.append({"area": "supply", "severity": "high", "gate": "Confirm allocation, seller authority, and cargo evidence before commercial commitment."})
    if {"buyer", "demand", "price", "margin"} & keywords:
        friction.append({"area": "market", "severity": "medium", "gate": "Treat price and demand signals as weak until corroborated by approved sources."})
    if not friction:
        friction.append({"area": "manual_review", "severity": "medium", "gate": "Insufficient structured energy signals; collect stronger local evidence."})
    return {
        "decision_support_status": "not_executable_without_approval",
        "friction_points": friction,
        "claim_types": sorted({claim.get("claim_type", "unknown") for claim in claims}),
        "approval_gates": verdict.get("intelligence_summary", {}).get("approval_gates", []),
        "next_review_questions": [
            "What evidence confirms seller authority and cargo availability?",
            "What counterparty KYC and sanctions checks are complete?",
            "What payment instrument is proposed and who verifies it?",
            "What terminal, freight, and laycan assumptions affect margin?",
            "Which buyer demand signal is independently corroborated?",
        ],
    }


def run_energy_from_documents(paths: list[Path], output_root: Path, run_id: str = "energy_intelligence_ingest") -> dict:
    run_dir = output_root / run_id
    actions_path = run_dir / "actions.jsonl"
    if actions_path.exists():
        actions_path.unlink()
    documents = load_documents(paths)
    evidence = index_evidence(documents)
    energy_evidence = [
        item for item in evidence
        if set(item.keywords) & {
            "energy", "crude", "cargo", "supply", "allocation", "logistics", "freight", "terminal", "laycan",
            "payment", "lc", "escrow", "kyc", "sanctions", "buyer", "seller", "counterparty", "demand", "price", "margin",
        }
    ]
    if not energy_evidence:
        raise RuntimeError("No energy/crude-oil evidence extracted from supplied local files")
    claims = extract_claims(energy_evidence)
    graph = build_energy_graph_from_evidence("kg_energy_ingested", energy_evidence, claims).to_dict()
    issues = validate_graph(graph)
    if issues:
        raise RuntimeError(f"Graph validation failed: {issues}")

    personas = [persona.to_dict() for persona in generate_energy_market_panel()]
    question = "Which local crude-market intelligence signals should block, delay, or support deal escalation?"
    manifest = RunManifest(
        run_id=run_id,
        domain="energy_crude_oil",
        question=question,
        max_rounds=4,
    ).to_dict()
    manifest["source_manifest"] = [document.source.to_dict() for document in documents]
    manifest["execution_guardrail"] = "decision_support_only"
    write_json(run_dir / "manifest.json", manifest)
    write_json(run_dir / "evidence_index.json", [item.to_dict() for item in energy_evidence])
    write_json(run_dir / "claims.json", [claim.to_dict() for claim in claims])
    write_json(run_dir / "knowledge_graph.json", graph)
    write_json(run_dir / "personas.json", personas)
    events = run_bounded_energy_rounds(run_id, personas, actions_path, max_rounds=4)
    verdict = build_energy_intelligence_report(
        run_id,
        question,
        events,
        [item.to_dict() for item in energy_evidence],
        [claim.to_dict() for claim in claims],
    )
    friction = build_deal_friction_report([item.to_dict() for item in energy_evidence], [claim.to_dict() for claim in claims], verdict)
    write_json(run_dir / "verdict.json", verdict)
    write_json(run_dir / "deal_friction_report.json", friction)
    write_json(
        run_dir / "summary.json",
        {
            "run_id": run_id,
            "event_count": len(events),
            "evidence_count": len(energy_evidence),
            "claim_count": len(claims),
            "friction_count": len(friction["friction_points"]),
            "verdict": verdict["overall_verdict"],
        },
    )
    return {
        "run_dir": str(run_dir),
        "evidence_count": len(energy_evidence),
        "claim_count": len(claims),
        "event_count": len(events),
        "friction_count": len(friction["friction_points"]),
        "verdict": verdict,
    }
