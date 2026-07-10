from __future__ import annotations

from app.evidence.evidence_schema import EvidenceGraph


def merge_evidence(
    primary: EvidenceGraph,
    _secondary: EvidenceGraph | None = None,
) -> EvidenceGraph:
    return primary
