from __future__ import annotations

from app.court.caption_safety import (
    caption_is_usable,
    clean_caption,
    ensure_safe_caption,
    fallback_caption,
)
from app.evidence.evidence_schema import EvidenceGraph, EvidenceSegment


def _evidence(video_id: str = "hidden-17") -> EvidenceGraph:
    return EvidenceGraph(
        video_id=video_id,
        overall_summary="A basketball player dribbles across an indoor court.",
        main_event="A basketball player dribbles toward the hoop in a gym.",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=8,
                observations=["The player moves across the court while controlling the ball."],
            )
        ],
    )


def test_clean_caption_extracts_json_and_adds_terminal_punctuation() -> None:
    assert clean_caption('{"caption":"A player dribbles across the court"}') == (
        "A player dribbles across the court."
    )


def test_clean_caption_joins_wrapped_caption_lines() -> None:
    assert clean_caption("Caption:\nA player crosses the court\nwhile dribbling the ball.") == (
        "A player crosses the court while dribbling the ball."
    )


def test_clean_caption_normalizes_smart_punctuation_for_portable_json() -> None:
    assert clean_caption(
        "Traffic reboots\u2014then moves through the city\u2019s intersection"
    ) == ("Traffic reboots - then moves through the city's intersection.")


def test_incomplete_caption_is_rejected() -> None:
    assert not caption_is_usable("A yellow flower opens against.")


def test_overlong_caption_is_rejected() -> None:
    caption = (
        "Traffic moves along a city boulevard while tall buildings, traffic lights, "
        "crosswalks, buses, cars, trees, sidewalks, windows, and distant signs all compete "
        "for unnecessary attention during rush hour."
    )

    assert len(caption.split()) > 26
    assert not caption_is_usable(caption)


def test_twenty_six_word_caption_is_within_safety_tolerance() -> None:
    caption = (
        "A cyclist rides through a rainy city street while pedestrians cross nearby, "
        "turning the wet commute into a careful balancing act for everyone involved each morning."
    )

    assert len(caption.split()) == 26
    assert caption_is_usable(caption)


def test_contact_sheet_language_is_rejected() -> None:
    assert not caption_is_usable("The contact sheet shows a flower opening in four frames.")


def test_natural_staring_and_as_if_language_is_not_blanket_banned() -> None:
    caption = "A worker stares at the monitor as if the spreadsheet has requested a rematch."
    assert caption_is_usable(caption)


def test_speculative_private_intent_is_rejected() -> None:
    assert not caption_is_usable(
        "A worker types at a desk, probably hoping the ceiling offers a better assignment."
    )
    assert not caption_is_usable(
        "A kitten sits in the woods, presumably solving mysteries while sunlight shifts."
    )
    assert not caption_is_usable(
        "A person types at a desk like someone pretending not to check the clock."
    )


def test_canned_style_openings_are_rejected() -> None:
    assert not caption_is_usable(
        "Nothing says autumn like traffic crawling past yellow trees in the city."
    )
    assert not caption_is_usable(
        "Behold, a kitten crosses the garden with the urgency of a royal inspection."
    )
    assert not caption_is_usable(
        "Traffic moves through the city, because nothing accelerates a commute like six lanes."
    )


def test_production_duration_jokes_are_rejected() -> None:
    assert not caption_is_usable(
        "Traffic races through the city after compressing the entire commute into six seconds."
    )


def test_fallback_uses_evidence_not_video_id() -> None:
    caption = fallback_caption(_evidence(video_id="v1"), "formal")
    assert "basketball" in caption.lower()
    assert "traffic" not in caption.lower()


def test_fallback_preserves_each_requested_tone() -> None:
    evidence = _evidence()
    outputs = {
        style: fallback_caption(evidence, style)
        for style in ("formal", "sarcastic", "humorous_tech", "humorous_non_tech")
    }
    assert len(set(outputs.values())) == 4
    assert "literal instruction" in outputs["humorous_tech"]
    assert "impressively official" in outputs["sarcastic"]
    assert "tiny performance" in outputs["humorous_non_tech"]


def test_unrelated_caption_is_replaced_with_evidence_anchor() -> None:
    caption = ensure_safe_caption(
        "A chef prepares a meal in a crowded restaurant kitchen.",
        _evidence(),
        "formal",
    )

    assert "basketball" in caption.lower()
    assert "chef" not in caption.lower()


def test_unseen_technical_claim_requires_a_figurative_marker() -> None:
    caption = ensure_safe_caption(
        "A basketball player dribbles across an indoor court while deploying code to production.",
        _evidence(),
        "humorous_tech",
    )

    assert "deploying code" not in caption.lower()
    assert "like a program" in caption.lower()


def test_explicit_technical_metaphor_remains_usable() -> None:
    raw_caption = (
        "A basketball player dribbles across an indoor court like an algorithm debugging its route."
    )

    assert ensure_safe_caption(raw_caption, _evidence(), "humorous_tech") == raw_caption


def test_ensure_safe_caption_replaces_dangling_generation() -> None:
    caption = ensure_safe_caption(
        "A yellow-orange flower unfurls petal by petal against",
        _evidence(),
        "sarcastic",
    )
    assert caption.endswith(".")
    assert not caption.endswith("against.")
    assert "basketball" in caption.lower()


def test_unknown_evidence_never_uses_public_sample_answer() -> None:
    evidence = EvidenceGraph(
        video_id="v2",
        overall_summary="A surfer rides a breaking wave near shore.",
        main_event="A surfer balances on a board as a wave curls behind them.",
    )
    caption = ensure_safe_caption("Analysis: write a caption", evidence, "formal")
    assert "surfer" in caption.lower()
    assert "kitten" not in caption.lower()


def test_long_caption_is_clipped_to_a_complete_sentence() -> None:
    caption = clean_caption(
        "A cyclist rides down a wet road beneath heavy clouds. "
        + ("Additional unsupported detail " * 30)
    )
    assert caption == "A cyclist rides down a wet road beneath heavy clouds."
