from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

from cognition_store.governance.approval_gate import requires_approval
from cognition_store.governance.secret_redactor import redact_text
from cognition_store.graph.graph_schema import Entity, KnowledgeGraph, Relationship
from cognition_store.ingestion.claim_extractor import Claim, extract_claims
from cognition_store.ingestion.evidence_indexer import EvidenceItem, split_sentences
from cognition_store.simulation.event_log import ActionEvent, append_event
from cognition_store.simulation.run_manifest import RunManifest
from cognition_store.storage.json_store import write_json


RUNTIME_KEYWORDS = (
    "completed",
    "delivered",
    "verified",
    "failed",
    "blocked",
    "guardrail",
    "approval",
    "risk",
    "lesson",
    "workflow",
    "memory",
    "protocol",
    "simulation",
    "ingestion",
    "energy",
    "agentshield",
)

APPROVAL_ACTION_KEYWORDS = {
    "production": "production_change",
    "deploy": "production_change",
    "external communication": "external_communication",
    "email": "external_communication",
    "finance": "financial_action",
    "payment": "financial_action",
    "contract": "contract_action",
    "identity": "identity_change",
    "governance": "governance_change",
    "protocol": "governance_change",
    "systemd": "system_service_change",
    "service": "system_service_change",
    "private data": "sensitive_data_use",
    "credential": "sensitive_data_use",
}


@dataclass
class RuntimeLesson:
    lesson_id: str
    text: str
    lesson_type: str
    evidence_refs: list[str]
    approval_required: bool = False
    approval_reason: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug[:48] or "runtime"


def _runtime_evidence(summary: str, source_id: str = "runtime_completion") -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for index, sentence in enumerate(split_sentences(redact_text(summary)), start=1):
        found = [keyword for keyword in RUNTIME_KEYWORDS if keyword in sentence.lower()]
        if not found:
            found = ["runtime"]
        evidence.append(
            EvidenceItem(
                evidence_id=f"ev_runtime_{index:03d}",
                source_id=source_id,
                text=sentence,
                keywords=found,
            )
        )
    return evidence


def _approval_reason(text: str) -> str:
    lower = text.lower()
    reasons = []
    for keyword, action_type in APPROVAL_ACTION_KEYWORDS.items():
        if keyword in lower and requires_approval(action_type):
            reasons.append(action_type)
    return ", ".join(sorted(set(reasons)))


def extract_runtime_lessons(evidence: list[EvidenceItem]) -> list[RuntimeLesson]:
    lessons: list[RuntimeLesson] = []
    for index, item in enumerate(evidence, start=1):
        lower = item.text.lower()
        if "blocked" in lower or "failed" in lower:
            lesson_type = "blocker"
        elif "verified" in lower or "passed" in lower:
            lesson_type = "verification"
        elif "guardrail" in lower or "approval" in lower:
            lesson_type = "governance"
        elif "workflow" in lower or "repeat" in lower:
            lesson_type = "procedure"
        else:
            lesson_type = "observation"
        reason = _approval_reason(item.text)
        lessons.append(
            RuntimeLesson(
                lesson_id=f"lesson_{index:03d}",
                text=item.text,
                lesson_type=lesson_type,
                evidence_refs=[item.evidence_id],
                approval_required=bool(reason),
                approval_reason=reason,
            )
        )
    return lessons


def build_runtime_graph(run_id: str, project: str, evidence: list[EvidenceItem], claims: list[Claim], lessons: list[RuntimeLesson]) -> dict:
    project_id = f"project_{_slug(project or 'general')}"
    entities = [Entity(project_id, "project", project or "general", [item.evidence_id for item in evidence], 0.75)]
    relationships: list[Relationship] = []

    for lesson in lessons:
        lesson_entity = Entity(f"entity_{lesson.lesson_id}", "runtime_lesson", lesson.lesson_type, lesson.evidence_refs, 0.7)
        entities.append(lesson_entity)
        relationships.append(Relationship(lesson_entity.id, project_id, "updates_runtime_understanding", lesson.evidence_refs, 0.68))

    return KnowledgeGraph(
        graph_id=f"kg_{_slug(run_id)}",
        entities=entities,
        relationships=relationships,
        claims=[claim.to_dict() for claim in claims],
        evidence_refs=[item.to_dict() for item in evidence],
    ).to_dict()


def build_runtime_verdict(run_id: str, project: str, lessons: list[RuntimeLesson]) -> dict:
    gated = [lesson for lesson in lessons if lesson.approval_required]
    blockers = [lesson.text for lesson in lessons if lesson.lesson_type == "blocker"]
    verification = [lesson.text for lesson in lessons if lesson.lesson_type == "verification"]
    return {
        "run_id": run_id,
        "domain": "local_runtime_learning",
        "project": project,
        "overall_verdict": "Runtime completion captured as local evidence and reusable lessons. Approval-gated changes were drafted only, not applied.",
        "confidence": 0.74 if lessons else 0.4,
        "consensus_score": 0.7 if verification else 0.55,
        "disagreement_score": 0.3 if verification else 0.45,
        "risk_drawdown": [
            "Keep runtime learning local and evidence-linked.",
            "Apply memory capture automatically only for explicitly assigned work.",
            "Draft protocol, governance, production, finance, contract, and sensitive-data changes for approval before execution.",
        ],
        "top_blockers": blockers[:5],
        "top_opportunities": verification[:5],
        "recommended_actions": [
            "Reuse captured lessons before similar future work.",
            "Review approval drafts before changing governance or runtime behavior.",
            "Continue verifying generated artifacts after each runtime hook execution.",
        ],
        "approval_draft_count": len(gated),
        "evidence_refs": sorted({ref for lesson in lessons for ref in lesson.evidence_refs}),
        "assumptions": ["Source was a local completed-task summary, not live production telemetry."],
        "invalid_or_weak_claims": [],
    }


def _display_path(path: Path) -> str:
    if not path.is_absolute():
        return str(path)
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        for parent in path.parents:
            if parent.name == "cognition-store":
                return str(Path("cognition-store") / path.relative_to(parent))
    return path.name


def run_task_completion_hook(summary: str, project: str, output_root: Path, run_id: str = "runtime_completion") -> dict:
    run_dir = output_root / run_id
    actions_path = run_dir / "actions.jsonl"
    if actions_path.exists():
        actions_path.unlink()
    safe_summary = redact_text(summary)
    evidence = _runtime_evidence(safe_summary)
    claims = extract_claims(evidence)
    lessons = extract_runtime_lessons(evidence)
    graph = build_runtime_graph(run_id, project, evidence, claims, lessons)
    verdict = build_runtime_verdict(run_id, project, lessons)
    manifest = RunManifest(
        run_id=run_id,
        domain="local_runtime_learning",
        question="What should Cognition Store learn from this completed task?",
        max_rounds=1,
    ).to_dict()
    manifest["project"] = project
    manifest["source"] = "runtime_completion_hook"

    write_json(run_dir / "manifest.json", manifest)
    write_json(run_dir / "completion_summary.json", {"summary": safe_summary})
    write_json(run_dir / "evidence_index.json", [item.to_dict() for item in evidence])
    write_json(run_dir / "claims.json", [claim.to_dict() for claim in claims])
    write_json(run_dir / "lessons.json", [lesson.to_dict() for lesson in lessons])
    write_json(run_dir / "approval_drafts.json", [lesson.to_dict() for lesson in lessons if lesson.approval_required])
    write_json(run_dir / "knowledge_graph.json", graph)
    write_json(run_dir / "verdict.json", verdict)
    write_json(
        run_dir / "summary.json",
        {
            "run_id": run_id,
            "project": project,
            "evidence_count": len(evidence),
            "claim_count": len(claims),
            "lesson_count": len(lessons),
            "approval_draft_count": verdict["approval_draft_count"],
            "verdict": verdict["overall_verdict"],
        },
    )
    for index, lesson in enumerate(lessons, start=1):
        append_event(
            actions_path,
            ActionEvent(
                event_id=f"evt_runtime_{index:03d}",
                run_id=run_id,
                round=1,
                persona_id="runtime_hook",
                action_type="lesson_capture",
                target=lesson.lesson_type,
                content_summary=lesson.text,
                evidence_refs=lesson.evidence_refs,
                belief_delta={"approval_required": int(lesson.approval_required)},
                confidence=0.7,
            ),
        )
    return {
        "run_dir": _display_path(run_dir),
        "evidence_count": len(evidence),
        "claim_count": len(claims),
        "lesson_count": len(lessons),
        "approval_draft_count": verdict["approval_draft_count"],
        "verdict": verdict,
    }
