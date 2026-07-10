from __future__ import annotations

from app.core.budget import BudgetState
from app.core.config import Settings
from app.court.candidate_generator import generate_candidates
from app.evidence.evidence_schema import EvidenceGraph, EvidenceSegment
from app.io.official_schema import VideoTask
from app.providers.base import CaptionStyle


class CountingProvider:
    name = "counting"

    def __init__(self) -> None:
        self.calls = 0

    def caption(self, task: VideoTask, evidence: EvidenceGraph, style: CaptionStyle) -> str:
        self.calls += 1
        return f"{style} caption {self.calls}"

    def doctor(self) -> dict[str, object]:
        return {"provider": self.name, "ok": True}


def test_official_mode_forces_one_caption_candidate() -> None:
    provider = CountingProvider()
    evidence = EvidenceGraph(
        video_id="v1",
        overall_summary="A short clip is shown.",
        main_event="A short clip is shown.",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=1,
                observations=["A short clip is shown."],
            )
        ],
    )
    task = VideoTask(video_id="v1", video_uri="mock://video")
    budget = BudgetState(video_id="v1", max_model_calls=5, max_seconds=30)

    candidates = generate_candidates(
        task,
        evidence,
        "formal",
        provider,
        budget,
        Settings(official_mode=True, caption_candidates_per_style=3),
    )

    assert candidates == ["formal caption 1"]
    assert provider.calls == 1
