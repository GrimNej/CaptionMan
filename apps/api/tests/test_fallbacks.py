from __future__ import annotations

from app.core.fallbacks import progressive_fallback_from_best_available_evidence
from app.io.official_schema import VideoTask


def test_fallback_produces_all_styles() -> None:
    result = progressive_fallback_from_best_available_evidence(
        VideoTask(video_id="a", video_uri="mock://a", metadata={"description": "A demo"}),
        "test",
    )
    assert result.formal
    assert result.sarcastic
    assert result.humorous_tech
    assert result.humorous_non_tech
