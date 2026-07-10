from __future__ import annotations

from pydantic import BaseModel, Field


class EvidenceSegment(BaseModel):
    start_seconds: float
    end_seconds: float
    observations: list[str] = Field(default_factory=list)


class EvidenceFrame(BaseModel):
    frame_id: str
    timestamp_seconds: float
    image_path: str
    kind: str = "single_frame"


class EvidenceGraph(BaseModel):
    video_id: str
    overall_summary: str
    main_event: str
    segments: list[EvidenceSegment] = Field(default_factory=list)
    frame_artifacts: list[EvidenceFrame] = Field(default_factory=list)
    global_subjects: list[str] = Field(default_factory=list)
    global_objects: list[str] = Field(default_factory=list)
    visible_text: list[str] = Field(default_factory=list)
    audio_cues: list[str] = Field(default_factory=list)
    forbidden_assumptions: list[str] = Field(default_factory=list)
    uncertainty_notes: list[str] = Field(default_factory=list)
