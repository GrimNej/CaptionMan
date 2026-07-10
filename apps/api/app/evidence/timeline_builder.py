from __future__ import annotations

from app.evidence.evidence_schema import EvidenceGraph, EvidenceSegment
from app.io.official_schema import VideoTask


def build_evidence(task: VideoTask) -> EvidenceGraph:
    description = str(task.metadata.get("description") or "A short video clip")
    return EvidenceGraph(
        video_id=task.video_id,
        overall_summary=description,
        main_event=description,
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=[description],
            )
        ],
        global_subjects=["visible subject"],
        global_objects=[],
        visible_text=[],
        audio_cues=["audio not analyzed in mock mode"],
        forbidden_assumptions=["Do not infer identities, brands, locations, or intent."],
        uncertainty_notes=["Mock mode uses supplied metadata instead of frame analysis."],
    )
