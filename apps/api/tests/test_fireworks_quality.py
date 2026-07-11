from __future__ import annotations

from types import SimpleNamespace

from app.core.config import Settings
from app.evidence.evidence_schema import EvidenceGraph, EvidenceSegment
from app.providers.fireworks import (
    _caption_context_json,
    _extract_json_or_fallback,
    _frame_count,
    _message_content,
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


def test_evidence_normalization_removes_incidental_clothing() -> None:
    normalized = _normalize_evidence_text(
        "A person in an orange top types at a desktop computer in a modern office."
    )

    assert normalized == "A person types at a desktop computer in a modern office."


def test_evidence_normalization_removes_conjoined_incidental_clothing() -> None:
    normalized = _normalize_evidence_text(
        "A person wearing a black jacket and orange top types in an office."
    )

    assert normalized == "A person types in an office."


def test_evidence_normalization_neutralizes_uncertain_person_labels() -> None:
    normalized = _normalize_evidence_text(
        "A woman types while a boy watches the man's computer screen."
    )

    assert normalized == "A person types while a child watches the person's computer screen."


def test_evidence_normalization_preserves_sentence_initial_capitalization() -> None:
    normalized = _normalize_evidence_text(
        "Woman types at a white desk in an office with a large monitor."
    )

    assert normalized == "Person types at a white desk in an office with a large monitor."


def test_evidence_normalization_removes_inferred_time_lapse_language() -> None:
    anchor = _normalize_evidence_text(
        "Time-lapse of traffic flowing through a city street with autumn trees."
    )
    event = _normalize_evidence_text(
        "Vehicles move rapidly through an intersection in a time-lapse sequence."
    )

    assert anchor == "Traffic flowing through a city street with autumn trees."
    assert event == "Vehicles move through an intersection."


def test_caption_context_excludes_incidental_timeline_details() -> None:
    evidence = EvidenceGraph(
        video_id="hidden-4",
        overall_summary="A cyclist rides along a wet city street.",
        main_event="Cyclist travels through the city in rain.",
        global_subjects=["cyclist"],
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=5,
                observations=["A red sign appears briefly behind the cyclist."],
            )
        ],
    )

    context = _caption_context_json(evidence)

    assert "scene_anchor" in context
    assert "wet city street" in context
    assert "red sign" not in context
    assert "segments" not in context


def test_message_content_recovers_provider_reasoning_field() -> None:
    message = SimpleNamespace(
        content="",
        reasoning_content=None,
        model_extra={"reasoning_content": '{"overall_summary":"A cyclist rides."}'},
    )

    assert _message_content(message) == '{"overall_summary":"A cyclist rides."}'
