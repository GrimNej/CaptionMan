from __future__ import annotations

from app.core.config import Settings
from app.providers.fireworks import (
    _extract_json_or_fallback,
    _frame_count,
    _normalize_evidence_text,
    _summary_from_observations,
)


def test_frame_count_scales_with_hidden_clip_duration() -> None:
    settings = Settings(num_frames=12, min_frames=10, max_frames=14)

    assert _frame_count(30, settings) == 10
    assert _frame_count(60, settings) == 12
    assert _frame_count(120, settings) == 14


def test_unstructured_vision_fallback_is_domain_neutral() -> None:
    payload = _extract_json_or_fallback(
        "A goalkeeper dives to the left.\nThe ball travels toward the lower corner."
    )

    assert "goalkeeper" in payload["overall_summary"].lower()
    assert payload["segments"][0]["observations"]


def test_summary_selection_is_not_hardcoded_to_public_domains() -> None:
    summary = _summary_from_observations(
        [
            "Rain falls across a quiet field.",
            "Dark clouds move over the field as wind bends the tall grass.",
        ]
    )

    assert "Rain falls" in summary
    assert "Dark clouds" in summary


def test_evidence_normalization_prefers_safe_visible_categories() -> None:
    normalized = _normalize_evidence_text(
        "A person with an afro hairstyle types on a laptop beside "
        "light-colored residential buildings."
    )

    assert normalized == "A person types on a computer beside buildings."


def test_evidence_normalization_preserves_confident_specific_details() -> None:
    normalized = _normalize_evidence_text(
        "An orange kitten rests beside a desktop computer and green foliage."
    )

    assert "orange kitten" in normalized
    assert "desktop computer" in normalized
    assert "green foliage" in normalized
