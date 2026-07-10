from __future__ import annotations

from app.evidence.evidence_schema import EvidenceGraph
from app.io.official_schema import VideoTask
from app.providers.base import CaptionStyle


class MockProvider:
    name = "mock"

    def caption(self, task: VideoTask, evidence: EvidenceGraph, style: CaptionStyle) -> str:
        summary = evidence.overall_summary.rstrip(".")
        match style:
            case "formal":
                return f"{summary}."
            case "sarcastic":
                return f"{summary}, finding a little drama in the ordinary."
            case "humorous_tech":
                return f"{summary}, with the key visual signal still clear."
            case "humorous_non_tech":
                return f"{summary}, keeping the scene clear without overexplaining it."

    def doctor(self) -> dict[str, object]:
        return {"provider": self.name, "ok": True, "details": "deterministic local provider"}
