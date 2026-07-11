from __future__ import annotations

from app.core.config import Settings
from app.core.pipeline import run_pipeline
from app.evidence.evidence_schema import EvidenceGraph
from app.io.official_schema import VideoTask
from app.providers.mock import MockProvider


def test_mock_pipeline_produces_four_styles() -> None:
    results, replay = run_pipeline(
        [VideoTask(video_id="demo", video_uri="mock://demo", metadata={"description": "A demo"})],
        Settings(ai_provider="mock"),
    )
    assert len(results) == 1
    assert results[0].formal
    assert results[0].sarcastic
    assert results[0].humorous_tech
    assert results[0].humorous_non_tech
    assert replay[0]["video_id"] == "demo"


def test_pipeline_uses_provider_evidence_builder_when_available(monkeypatch) -> None:
    class EvidenceProvider(MockProvider):
        def build_evidence(self, task: VideoTask, attempt: int = 0) -> EvidenceGraph:
            return EvidenceGraph(
                video_id=task.video_id,
                overall_summary="Provider-built evidence",
                main_event="Provider evidence event",
            )

    monkeypatch.setattr("app.core.pipeline.make_provider", lambda _settings: EvidenceProvider())

    _results, replay = run_pipeline(
        [VideoTask(video_id="demo", video_uri="mock://demo")],
        Settings(ai_provider="mock"),
    )

    assert replay[0]["evidence"]["overall_summary"] == "Provider-built evidence"


def test_pipeline_retries_generic_provider_evidence_within_budget(monkeypatch) -> None:
    class EvidenceProvider(MockProvider):
        def __init__(self) -> None:
            self.attempts: list[int] = []

        def build_evidence(self, task: VideoTask, attempt: int = 0) -> EvidenceGraph:
            self.attempts.append(attempt)
            if attempt == 0:
                return EvidenceGraph(
                    video_id=task.video_id,
                    overall_summary="A video clip is shown.",
                    main_event="A video clip is shown.",
                )
            return EvidenceGraph(
                video_id=task.video_id,
                overall_summary="A surfer rides a breaking wave near shore.",
                main_event="A surfer balances on a board in the ocean.",
            )

    provider = EvidenceProvider()
    monkeypatch.setattr("app.core.pipeline.make_provider", lambda _settings: provider)

    _results, replay = run_pipeline(
        [VideoTask(video_id="hidden-surf", video_uri="mock://hidden-surf")],
        Settings(ai_provider="mock", max_evidence_attempts=2),
    )

    assert provider.attempts == [0, 1]
    assert "surfer" in replay[0]["evidence"]["overall_summary"].lower()
    assert replay[0]["budget"]["call_stages"][:2] == [
        "evidence:vision:1",
        "evidence:vision:2",
    ]


def test_pipeline_prefers_one_batch_caption_call(monkeypatch) -> None:
    class BatchProvider(MockProvider):
        def __init__(self) -> None:
            self.batch_calls = 0
            self.single_calls = 0

        def caption_batch(self, task, evidence, styles):  # noqa: ANN001
            self.batch_calls += 1
            return {
                "formal": "A runner crosses an outdoor track during a race.",
                "sarcastic": (
                    "A runner crosses the track, because standing still was never "
                    "competitive enough."
                ),
                "humorous_tech": (
                    "A runner crosses the track with the human processor firmly set to "
                    "performance mode."
                ),
                "humorous_non_tech": (
                    "A runner crosses the track while the finish line tries very hard to "
                    "look farther away."
                ),
            }

        def caption(self, task, evidence, style):  # noqa: ANN001
            self.single_calls += 1
            return super().caption(task, evidence, style)

    provider = BatchProvider()
    monkeypatch.setattr("app.core.pipeline.make_provider", lambda _settings: provider)

    results, replay = run_pipeline(
        [
            VideoTask(
                video_id="hidden-run",
                video_uri="mock://hidden-run",
                metadata={"description": "A runner crosses an outdoor track"},
            )
        ],
        Settings(ai_provider="mock", official_mode=True),
    )

    assert provider.batch_calls == 1
    assert provider.single_calls == 0
    assert results[0].formal.startswith("A runner")
    assert replay[0]["budget"]["call_stages"] == ["captions:batch"]
