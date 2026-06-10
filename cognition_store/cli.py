from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognition_store.domains.agentshield.buyer_committee import run_demo
from cognition_store.domains.agentshield.buyer_committee import run_from_documents
from cognition_store.domains.agentshield.buyer_simulator import run_buyer_simulator
from cognition_store.domains.energy.market_simulation import run_energy_demo
from cognition_store.domains.energy.market_simulation import run_energy_from_documents
from cognition_store.runtime.task_hook import run_task_completion_hook
from cognition_store.web_app import serve


def main() -> int:
    parser = argparse.ArgumentParser(description="Cognition Store")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("agentshield-demo", help="Run synthetic AgentShield buyer-committee simulation")
    demo.add_argument("--output", type=Path, default=Path("artifacts/runs"))

    ingest = sub.add_parser("agentshield-ingest", help="Run AgentShield simulation from approved local text/markdown files")
    ingest.add_argument("files", nargs="+", type=Path)
    ingest.add_argument("--output", type=Path, default=Path("artifacts/runs"))
    ingest.add_argument("--run-id", default="agentshield_ingest_demo")

    buyer = sub.add_parser("agentshield-buyer-sim", help="Build AgentShield buyer-committee sales simulation from local target notes")
    buyer.add_argument("files", nargs="+", type=Path)
    buyer.add_argument("--target-name", required=True)
    buyer.add_argument("--output", type=Path, default=Path("artifacts/runs"))
    buyer.add_argument("--run-id", default="agentshield_buyer_sim")

    energy = sub.add_parser("energy-demo", help="Run synthetic Energy & Crude Oil market-intelligence simulation")
    energy.add_argument("--output", type=Path, default=Path("artifacts/runs"))

    energy_ingest = sub.add_parser("energy-ingest", help="Run Energy & Crude Oil intelligence simulation from approved local files")
    energy_ingest.add_argument("files", nargs="+", type=Path)
    energy_ingest.add_argument("--output", type=Path, default=Path("artifacts/runs"))
    energy_ingest.add_argument("--run-id", default="energy_intelligence_ingest")

    runtime = sub.add_parser("runtime-complete", help="Capture a completed task into local cognition artifacts")
    runtime.add_argument("summary")
    runtime.add_argument("--project", default="local-runtime")
    runtime.add_argument("--output", type=Path, default=Path("artifacts/runs"))
    runtime.add_argument("--run-id", default="runtime_completion")

    web = sub.add_parser("serve", help="Run the local full-stack dashboard and JSON API")
    web.add_argument("--host", default="127.0.0.1")
    web.add_argument("--port", type=int, default=8765)
    web.add_argument("--output", type=Path, default=Path("artifacts/runs"))

    args = parser.parse_args()
    if args.command == "agentshield-demo":
        print(json.dumps(run_demo(args.output), ensure_ascii=False, indent=2))
        return 0
    if args.command == "agentshield-ingest":
        print(json.dumps(run_from_documents(args.files, args.output, args.run_id), ensure_ascii=False, indent=2))
        return 0
    if args.command == "agentshield-buyer-sim":
        print(json.dumps(run_buyer_simulator(args.files, args.output, args.target_name, args.run_id), ensure_ascii=False, indent=2))
        return 0
    if args.command == "energy-demo":
        print(json.dumps(run_energy_demo(args.output), ensure_ascii=False, indent=2))
        return 0
    if args.command == "energy-ingest":
        print(json.dumps(run_energy_from_documents(args.files, args.output, args.run_id), ensure_ascii=False, indent=2))
        return 0
    if args.command == "runtime-complete":
        print(json.dumps(run_task_completion_hook(args.summary, args.project, args.output, args.run_id), ensure_ascii=False, indent=2))
        return 0
    if args.command == "serve":
        serve(args.host, args.port, output_root=args.output)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
