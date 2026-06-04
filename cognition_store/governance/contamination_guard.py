from __future__ import annotations

from dataclasses import dataclass, field


FORBIDDEN_SOURCE_MARKERS = (
    "restricted-source",
    "reference-only",
    "copyleft-reference",
    "external-audit-sample",
)


@dataclass
class ContaminationReport:
    passed: bool
    warnings: list[str] = field(default_factory=list)


def check_source_manifest(source_names: list[str]) -> ContaminationReport:
    warnings: list[str] = []
    for source in source_names:
        if any(marker.lower() in source.lower() for marker in FORBIDDEN_SOURCE_MARKERS):
            warnings.append(f"Reference-only source detected: {source}. Do not import code, prompts, schemas, or assets.")
    return ContaminationReport(passed=True, warnings=warnings)
