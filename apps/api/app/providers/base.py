from __future__ import annotations

from typing import Literal, Protocol

from app.evidence.evidence_schema import EvidenceGraph
from app.io.official_schema import VideoTask

CaptionStyle = Literal["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]


class CaptionProvider(Protocol):
    name: str

    def caption(self, task: VideoTask, evidence: EvidenceGraph, style: CaptionStyle) -> str: ...

    def doctor(self) -> dict[str, object]: ...
