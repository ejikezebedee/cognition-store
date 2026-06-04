# Ingestion Workflow

The ingestion path accepts approved local `.txt` and `.md` files only.

1. Load local documents.
2. Redact credential-like strings.
3. Create a source manifest with path, size, and SHA-256.
4. Split text into evidence items.
5. Extract typed claims from evidence.
6. Build a local knowledge graph.
7. Validate graph relationships.
8. Run bounded simulation and write artifacts.

Example:

```bash
python3 -m cognition_store.cli agentshield-ingest ./approved-notes.md --output artifacts/runs
```

Simulation output is decision support only.

