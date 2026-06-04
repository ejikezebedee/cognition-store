from __future__ import annotations


def validate_graph(graph: dict) -> list[str]:
    issues: list[str] = []
    entity_ids = {entity["id"] for entity in graph.get("entities", [])}
    if not entity_ids:
        issues.append("Graph has no entities")
    for rel in graph.get("relationships", []):
        if rel.get("source") not in entity_ids:
            issues.append(f"Relationship source missing: {rel.get('source')}")
        if rel.get("target") not in entity_ids:
            issues.append(f"Relationship target missing: {rel.get('target')}")
        if not rel.get("evidence_refs"):
            issues.append(f"Relationship lacks evidence: {rel.get('source')}->{rel.get('target')}")
    return issues

