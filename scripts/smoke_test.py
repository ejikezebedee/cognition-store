#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cognition_store.domains.agentshield.buyer_committee import run_demo
from cognition_store.domains.agentshield.buyer_committee import run_from_documents
from cognition_store.domains.agentshield.buyer_simulator import run_buyer_simulator
from cognition_store.domains.energy.market_simulation import run_energy_demo
from cognition_store.domains.energy.market_simulation import run_energy_from_documents
from cognition_store.runtime.task_hook import run_task_completion_hook
from cognition_store.governance.approval_gate import requires_approval
from cognition_store.governance.secret_redactor import has_secret_marker, redact_text


def main() -> int:
    assert has_secret_marker("api_key=abc123")
    assert "[REDACTED]" in redact_text("api_key=abc123")
    assert requires_approval("production_change")
    assert not requires_approval("local_simulation")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        result = run_demo(tmp_path)
        run_dir = Path(result["run_dir"])
        assert result["event_count"] == 20
        assert (run_dir / "manifest.json").exists()
        assert (run_dir / "knowledge_graph.json").exists()
        assert (run_dir / "actions.jsonl").exists()
        assert (run_dir / "verdict.json").exists()

        sample = tmp_path / "sample.md"
        sample.write_text(
            "The target company worries about downtime, compliance, vendor trust, and budget approval. "
            "AgentShield should begin as a read-only security audit with low operations disruption.",
            encoding="utf-8",
        )
        ingest = run_from_documents([sample], tmp_path, "ingest_smoke")
        ingest_dir = Path(ingest["run_dir"])
        assert ingest["evidence_count"] >= 2
        assert ingest["claim_count"] >= 2
        assert (ingest_dir / "evidence_index.json").exists()
        assert (ingest_dir / "claims.json").exists()

        buyer = run_buyer_simulator([sample], tmp_path, "Synthetic Target", "buyer_smoke")
        buyer_dir = tmp_path / "buyer_smoke"
        assert buyer["committee_count"] == 5
        assert buyer["friction_count"] >= 2
        assert (buyer_dir / "buyer_simulation.json").exists()
        assert (buyer_dir / "sales_brief.json").exists()

        energy = run_energy_demo(tmp_path)
        energy_dir = Path(energy["run_dir"])
        assert energy["event_count"] == 20
        assert energy["verdict"]["domain"] == "energy_crude_oil"
        assert (energy_dir / "knowledge_graph.json").exists()
        assert (energy_dir / "actions.jsonl").exists()

        energy_notes = tmp_path / "energy.md"
        energy_notes.write_text(
            "Crude cargo supply confirmation is incomplete. "
            "Buyer demand and price margin depend on freight, terminal, and laycan timing. "
            "Counterparty KYC, sanctions review, and payment LC verification are required.",
            encoding="utf-8",
        )
        energy_ingest = run_energy_from_documents([energy_notes], tmp_path, "energy_ingest_smoke")
        energy_ingest_dir = tmp_path / "energy_ingest_smoke"
        assert energy_ingest["event_count"] == 20
        assert energy_ingest["evidence_count"] >= 3
        assert energy_ingest["friction_count"] >= 3
        assert (energy_ingest_dir / "deal_friction_report.json").exists()

        runtime = run_task_completion_hook(
            "Delivered runtime hook. Verified smoke test passed. Protocol changes require approval.",
            "sample-project",
            tmp_path,
            "runtime_smoke",
        )
        runtime_dir = tmp_path / "runtime_smoke"
        assert runtime["lesson_count"] >= 3
        assert runtime["approval_draft_count"] >= 1
        assert (runtime_dir / "lessons.json").exists()
        assert (runtime_dir / "approval_drafts.json").exists()
    print("SMOKE_TEST_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
