from __future__ import annotations

from pathlib import Path

from cognition_store.graph.graph_builder import build_synthetic_agentshield_graph
from cognition_store.graph.graph_builder import build_graph_from_evidence
from cognition_store.graph.graph_validation import validate_graph
from cognition_store.ingestion.claim_extractor import extract_claims
from cognition_store.ingestion.document_loader import load_documents
from cognition_store.ingestion.evidence_indexer import index_evidence
from cognition_store.personas.persona_generator import generate_agentshield_committee
from cognition_store.reporting.verdict_schema import build_verdict
from cognition_store.simulation.round_engine import run_bounded_agentshield_rounds
from cognition_store.simulation.run_manifest import RunManifest
from cognition_store.storage.json_store import write_json


def run_demo(output_root: Path) -> dict:
    run_id = "agentshield_synthetic_demo"
    run_dir = output_root / run_id
    actions_path = run_dir / "actions.jsonl"
    if actions_path.exists():
        actions_path.unlink()
    graph = build_synthetic_agentshield_graph().to_dict()
    issues = validate_graph(graph)
    if issues:
        raise RuntimeError(f"Graph validation failed: {issues}")

    personas = [persona.to_dict() for persona in generate_agentshield_committee()]
    manifest = RunManifest(
        run_id=run_id,
        domain="agentshield_sales",
        question="Where will a synthetic SME buying committee resist AgentShield adoption?",
        max_rounds=4,
    ).to_dict()
    write_json(run_dir / "manifest.json", manifest)
    write_json(run_dir / "knowledge_graph.json", graph)
    write_json(run_dir / "personas.json", personas)
    events = run_bounded_agentshield_rounds(run_id, personas, actions_path, max_rounds=4)
    verdict = build_verdict(run_id, "agentshield_sales", manifest["question"], events)
    write_json(run_dir / "verdict.json", verdict)
    write_json(run_dir / "summary.json", {"run_id": run_id, "event_count": len(events), "verdict": verdict["overall_verdict"]})
    return {"run_dir": str(run_dir), "event_count": len(events), "verdict": verdict}


def run_from_documents(paths: list[Path], output_root: Path, run_id: str = "agentshield_ingest_demo") -> dict:
    run_dir = output_root / run_id
    actions_path = run_dir / "actions.jsonl"
    if actions_path.exists():
        actions_path.unlink()
    documents = load_documents(paths)
    evidence = index_evidence(documents)
    if not evidence:
        raise RuntimeError("No evidence extracted from supplied documents")
    claims = extract_claims(evidence)
    graph = build_graph_from_evidence("kg_agentshield_ingested", evidence, claims).to_dict()
    issues = validate_graph(graph)
    if issues:
        raise RuntimeError(f"Graph validation failed: {issues}")

    personas = [persona.to_dict() for persona in generate_agentshield_committee()]
    manifest = RunManifest(
        run_id=run_id,
        domain="agentshield_sales",
        question="Where will the buyer committee resist AgentShield adoption based on approved local evidence?",
        max_rounds=4,
    ).to_dict()
    manifest["source_manifest"] = [document.source.to_dict() for document in documents]
    write_json(run_dir / "manifest.json", manifest)
    write_json(run_dir / "evidence_index.json", [item.to_dict() for item in evidence])
    write_json(run_dir / "claims.json", [claim.to_dict() for claim in claims])
    write_json(run_dir / "knowledge_graph.json", graph)
    write_json(run_dir / "personas.json", personas)
    events = run_bounded_agentshield_rounds(run_id, personas, actions_path, max_rounds=4)
    verdict = build_verdict(run_id, "agentshield_sales", manifest["question"], events)
    verdict["evidence_refs"] = [item.evidence_id for item in evidence[:10]]
    verdict["assumptions"] = ["Simulation used approved local files only; output is decision support."]
    write_json(run_dir / "verdict.json", verdict)
    write_json(run_dir / "summary.json", {"run_id": run_id, "event_count": len(events), "evidence_count": len(evidence), "claim_count": len(claims), "verdict": verdict["overall_verdict"]})
    return {"run_dir": str(run_dir), "evidence_count": len(evidence), "claim_count": len(claims), "event_count": len(events), "verdict": verdict}
