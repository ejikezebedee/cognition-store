from pathlib import Path

from cognition_store.domains.agentshield.buyer_committee import run_demo
from cognition_store.domains.agentshield.buyer_simulator import run_buyer_simulator
from cognition_store.domains.energy.market_simulation import run_energy_demo
from cognition_store.domains.energy.market_simulation import run_energy_from_documents


def test_agentshield_demo(tmp_path: Path):
    result = run_demo(tmp_path)
    run_dir = Path(result["run_dir"])
    assert result["event_count"] == 20
    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "knowledge_graph.json").exists()
    assert (run_dir / "actions.jsonl").exists()
    assert (run_dir / "verdict.json").exists()


def test_energy_demo(tmp_path: Path):
    result = run_energy_demo(tmp_path)
    run_dir = Path(result["run_dir"])
    assert result["event_count"] == 20
    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "knowledge_graph.json").exists()
    assert (run_dir / "actions.jsonl").exists()
    assert (run_dir / "verdict.json").exists()
    assert result["verdict"]["domain"] == "energy_crude_oil"


def test_energy_ingest(tmp_path: Path):
    notes = tmp_path / "energy.md"
    notes.write_text(
        "Crude cargo supply confirmation is incomplete. "
        "Buyer demand and price margin depend on freight, terminal, and laycan timing. "
        "Counterparty KYC, sanctions review, and payment LC verification are required.",
        encoding="utf-8",
    )
    result = run_energy_from_documents([notes], tmp_path, "energy_ingest_test")
    run_dir = tmp_path / "energy_ingest_test"
    assert result["event_count"] == 20
    assert result["evidence_count"] >= 3
    assert result["friction_count"] >= 3
    assert (run_dir / "deal_friction_report.json").exists()
    assert (run_dir / "verdict.json").exists()


def test_agentshield_buyer_simulator(tmp_path: Path):
    notes = tmp_path / "target.md"
    notes.write_text(
        "Target company has downtime risk, procurement approval delays, vendor trust concerns, "
        "security audit needs, compliance pressure, and budget sensitivity.",
        encoding="utf-8",
    )
    result = run_buyer_simulator([notes], tmp_path, "Synthetic Target", "buyer_sim_test")
    run_dir = tmp_path / "buyer_sim_test"
    assert result["committee_count"] == 5
    assert result["friction_count"] >= 3
    assert (run_dir / "buyer_simulation.json").exists()
    assert (run_dir / "sales_brief.json").exists()
