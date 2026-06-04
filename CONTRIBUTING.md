# Contributing

Thanks for helping improve Cognition Store.

## Principles

- Keep the engine local-first and auditable.
- Use synthetic examples unless real data is explicitly approved and sanitized.
- Preserve evidence links for claims and recommendations.
- Keep approval-sensitive actions as drafts only.
- Avoid adding network calls to the core engine.

## Development Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python3 scripts/smoke_test.py
python3 -m compileall cognition_store scripts
```

If `pytest` is available:

```bash
pytest
```

## Pull Requests

Before opening a pull request:

- run the smoke test
- run the compile check
- check new examples for private data
- document new commands in `README.md`
- keep generated artifacts out of commits unless they are intentional fixtures

## Data Hygiene

Do not commit:

- private paths
- credentials or tokens
- personal emails
- server IP addresses
- customer or counterparty data
- internal operational notes
