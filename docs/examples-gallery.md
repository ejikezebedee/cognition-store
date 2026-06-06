# Examples Gallery

This gallery explains what the included demos generate and how a reviewer should read the outputs.

## AgentShield Buyer Committee Demo

Command:

```bash
python3 -m cognition_store.cli agentshield-demo --output artifacts/runs
```

Purpose:

- models a synthetic buying committee
- identifies adoption blockers
- produces recommended next actions for human review

Useful outputs:

- `verdict.json`: final decision-support summary
- `actions.jsonl`: event-by-event simulation trace
- `knowledge_graph.json`: evidence-linked entities and relationships

## AgentShield Buyer Simulator

Command:

```bash
python3 -m cognition_store.cli agentshield-buyer-sim examples/standard_b2b_sales/target-notes.md --target-name "Synthetic Target" --output artifacts/runs
```

Purpose:

- turns approved local target notes into a sales-readiness simulation
- maps buyer roles, objections, friction, and pitch angles
- keeps outreach and approval-sensitive actions as review-only outputs

Useful outputs:

- `buyer_simulation.json`: buyer committee, friction, and objections
- `sales_brief.json`: positioning and next-step recommendations
- `verdict.json`: guarded decision-support result

## Energy Market Demo

Command:

```bash
python3 -m cognition_store.cli energy-demo --output artifacts/runs
```

Purpose:

- models synthetic crude-market risk factors
- separates market-signal reasoning from trade execution authority
- highlights compliance, logistics, payment, and counterparty gates

Useful outputs:

- `deal_friction_report.json`: risk and friction summary
- `verdict.json`: recommendation with confidence and blockers
- `actions.jsonl`: simulation trace

## Runtime Completion Capture

Command:

```bash
python3 -m cognition_store.cli runtime-complete "Delivered local task. Verified smoke test passed." --project local-runtime --output artifacts/runs
```

Purpose:

- captures a completed task into evidence-backed memory artifacts
- converts operational lessons into reviewable local files
- creates a traceable completion record without sending context to a cloud memory backend

Useful outputs:

- `summary.json`: concise completion summary
- `claims.json`: extracted task claims
- `knowledge_graph.json`: task evidence and relationships

## How To Review A Run

1. Open `manifest.json` to confirm the run domain and guardrails.
2. Open `evidence_index.json` to confirm the evidence sources.
3. Open `claims.json` to inspect extracted claims.
4. Open `knowledge_graph.json` to review relationships.
5. Open `actions.jsonl` to audit the step-by-step trace.
6. Open `verdict.json` last to review the final recommendation.
