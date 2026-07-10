from __future__ import annotations

from app.court.caption_safety import clean_caption, ensure_safe_caption
from app.evidence.evidence_schema import EvidenceGraph, EvidenceSegment


def _evidence() -> EvidenceGraph:
    return EvidenceGraph(
        video_id="v1",
        overall_summary="Urban autumn boulevard with golden trees and city traffic",
        main_event="Traffic moves through an autumn city boulevard",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["Cars move along a boulevard lined with golden trees."],
            )
        ],
    )


def test_clean_caption_extracts_json_caption() -> None:
    assert clean_caption('{"caption": "Cars move through an autumn boulevard."}') == (
        "Cars move through an autumn boulevard."
    )


def test_ensure_safe_caption_replaces_meta_text() -> None:
    caption = ensure_safe_caption("Count characters: roughly 160. Good.", _evidence(), "formal")
    assert (
        caption
        == "Cars move along a broad city boulevard lined with golden autumn trees "
        "and tall buildings on both sides."
    )


def test_ensure_safe_caption_replaces_analysis_artifact_text() -> None:
    evidence = EvidenceGraph(
        video_id="v2",
        overall_summary=(
            "The image shows a contact sheet with 4 frames labeled F01, F02, F03, F04. "
            "There is a small orange kitten in green foliage."
        ),
        main_event="A kitten moves through foliage",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["A small orange kitten moves through green foliage."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "The image shows a contact sheet with 4 frames labeled F01 through F04.",
        evidence,
        "formal",
    )

    assert (
        caption
        == "An orange kitten sits low among dense green leaves, framed closely by "
        "the garden foliage around it."
    )


def test_ensure_safe_caption_rejects_sensitive_dangling_description() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="Office worker at a desktop computer in a modern open-plan office",
        main_event="Office worker at a desktop computer",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["A person works at a desktop computer in an office."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "They show a woman with dark skin and natural hair sitting at a desk with a",
        evidence,
        "formal",
    )

    assert (
        caption
        == "An office worker sits at a desktop computer inside a bright, modern "
        "open-plan workspace with other desks nearby."
    )


def test_ensure_safe_caption_rejects_drafting_language() -> None:
    caption = ensure_safe_caption(
        "Or something more tied to the office setting",
        _evidence(),
        "humorous_tech",
    )
    assert caption == (
        "Autumn traffic gets beautiful color grading, even while road throughput "
        "stays stubbornly low between the buildings."
    )


def test_ensure_safe_caption_rejects_frame_and_inner_thought_language() -> None:
    caption = ensure_safe_caption(
        "Four frames of a worker staring at a computer like she should have called in sick.",
        _evidence(),
        "humorous_non_tech",
    )
    assert (
        caption
        == "Autumn made the boulevard look fancy, while the cars continued moving "
        "like nobody got the memo."
    )


def test_ensure_safe_caption_rejects_hallucinated_joke_details() -> None:
    caption = ensure_safe_caption(
        "The tiny orange overlord emerges from the jungle to demand snacks.",
        _evidence(),
        "sarcastic",
    )
    assert (
        caption
        == "The golden trees work overtime to make the slow city traffic look almost "
        "worth waiting for."
    )


def test_ensure_safe_caption_rejects_overextended_metaphors() -> None:
    evidence = EvidenceGraph(
        video_id="v2",
        overall_summary="Orange kitten among green foliage in a garden",
        main_event="Orange kitten moves through foliage",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An orange kitten moves through green foliage."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "A tiny orange fugitive attempts to camouflage in terrifying wilderness.",
        evidence,
        "humorous_non_tech",
    )

    assert (
        caption
        == "That kitten found the leafiest seat in the garden and settled in like "
        "it had reserved the place."
    )


def test_ensure_safe_caption_rejects_hidden_kitten_intent() -> None:
    evidence = EvidenceGraph(
        video_id="v2",
        overall_summary="Orange kitten among green foliage in a garden",
        main_event="Orange kitten moves through foliage",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An orange kitten moves through green foliage."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "A tiny orange kitten is definitely not plotting world domination.",
        evidence,
        "sarcastic",
    )

    assert (
        caption
        == "A small orange kitten supervises the garden from the safest leafy "
        "headquarters available, naturally taking the job very seriously."
    )


def test_ensure_safe_caption_rejects_invisible_office_action() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="Office worker at a desktop computer in a modern open-plan office",
        main_event="Office worker at desktop computer",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An office worker uses a desktop computer."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "The office computer waits patiently to watch you Google 'how to email'.",
        evidence,
        "humorous_tech",
    )

    assert caption == (
        "The workstation keeps monitor, keyboard, and productivity latency neatly "
        "in view inside the open office."
    )


def test_ensure_safe_caption_rejects_incomplete_busy_phrase() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="Office worker at a desktop computer in a modern open-plan office",
        main_event="Office worker at desktop computer",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An office worker uses a desktop computer."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "Mastering the office art of looking incredibly busy while doing absolutely",
        evidence,
        "humorous_non_tech",
    )

    assert (
        caption
        == "Someone gets office work done at a desktop while the open office quietly "
        "pretends to be peaceful."
    )


def test_ensure_safe_caption_rejects_office_privacy_hallucination() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="Office worker at a desktop computer in a modern open-plan office",
        main_event="Office worker at desktop computer",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An office worker uses a desktop computer."],
            )
        ],
    )

    caption = ensure_safe_caption(
        (
            "Open-plan office: where productivity and privacy go to die, "
            "but the monitor has your back."
        ),
        evidence,
        "humorous_tech",
    )

    assert caption == (
        "The workstation keeps monitor, keyboard, and productivity latency neatly "
        "in view inside the open office."
    )


def test_ensure_safe_caption_rejects_unnecessary_clothing_details() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="Office worker at a desktop computer in a modern open-plan office",
        main_event="Office worker at desktop computer",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An office worker uses a desktop computer."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "A woman in a light jacket and orange top types at a desktop computer.",
        evidence,
        "formal",
    )

    assert (
        caption
        == "An office worker sits at a desktop computer inside a bright, modern "
        "open-plan workspace with other desks nearby."
    )


def test_ensure_safe_caption_rejects_aiish_tech_cliches() -> None:
    evidence = EvidenceGraph(
        video_id="v2",
        overall_summary="Orange kitten among green foliage in a garden",
        main_event="Orange kitten moves through foliage",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An orange kitten moves through green foliage."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "Local orange debugging unit infiltrates the garden codebase.",
        evidence,
        "humorous_tech",
    )

    assert (
        caption
        == "The orange kitten runs a quiet garden scan, using the surrounding "
        "leaves as extra visual cover."
    )


def test_ensure_safe_caption_rejects_aiish_sarcasm_template() -> None:
    evidence = EvidenceGraph(
        video_id="v1",
        overall_summary="Urban autumn boulevard with golden trees and city traffic",
        main_event="Traffic moves through an autumn city boulevard",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["Cars move along a boulevard lined with golden trees."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "Ah yes, city traffic disguised as a boulevard fashion show on Earth.",
        evidence,
        "sarcastic",
    )

    assert (
        caption
        == "The golden trees work overtime to make the slow city traffic look almost "
        "worth waiting for."
    )


def test_ensure_safe_caption_rejects_word_count_self_check() -> None:
    caption = ensure_safe_caption("That's 16 words. Let", _evidence(), "humorous_tech")

    assert caption == (
        "Autumn traffic gets beautiful color grading, even while road throughput "
        "stays stubbornly low between the buildings."
    )


def test_ensure_safe_caption_rejects_dangling_contrast_clause() -> None:
    caption = ensure_safe_caption(
        "The boulevard's autumn palette is stunning, but lane distribution",
        _evidence(),
        "humorous_tech",
    )

    assert caption == (
        "Autumn traffic gets beautiful color grading, even while road throughput "
        "stays stubbornly low between the buildings."
    )


def test_ensure_safe_caption_rejects_dangling_preposition_phrase() -> None:
    evidence = EvidenceGraph(
        video_id="v2",
        overall_summary="Orange kitten among green foliage in a garden",
        main_event="Orange kitten moves through foliage",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An orange kitten moves through green foliage."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "A ginger kitten demonstrates forward deployment across a",
        evidence,
        "humorous_tech",
    )

    assert (
        caption
        == "The orange kitten runs a quiet garden scan, using the surrounding "
        "leaves as extra visual cover."
    )


def test_ensure_safe_caption_rejects_dangling_as_if_clause() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="Office worker at a desktop computer in a modern open-plan office",
        main_event="Office worker at desktop computer",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An office worker uses a desktop computer."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "The seated operator keeps her head-position drift impressively low, as if the monitor",
        evidence,
        "humorous_tech",
    )

    assert caption == (
        "The workstation keeps monitor, keyboard, and productivity latency neatly "
        "in view inside the open office."
    )


def test_ensure_safe_caption_rejects_dangling_all() -> None:
    evidence = EvidenceGraph(
        video_id="v2",
        overall_summary="Orange kitten among green foliage in a garden",
        main_event="Orange kitten moves through foliage",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An orange kitten moves through green foliage."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "A ginger kitten posed like the garden had been waiting all",
        evidence,
        "humorous_non_tech",
    )

    assert (
        caption
        == "That kitten found the leafiest seat in the garden and settled in like "
        "it had reserved the place."
    )


def test_ensure_safe_caption_rejects_prompt_review_language() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="Office worker at a desktop computer in a modern open-plan office",
        main_event="Office worker at desktop computer",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An office worker uses a desktop computer."],
            )
        ],
    )

    caption = ensure_safe_caption(
        (
            "That works. It's grounded in visible motion, uses a light technical "
            "metaphor, and is witty without being meme-y."
        ),
        evidence,
        "humorous_tech",
    )

    assert caption == (
        "The workstation keeps monitor, keyboard, and productivity latency neatly "
        "in view inside the open office."
    )


def test_ensure_safe_caption_rejects_unprofessional_office_style() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="Office worker at a desktop computer in a modern open-plan office",
        main_event="Office worker at desktop computer",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["An office worker uses a desktop computer."],
            )
        ],
    )

    caption = ensure_safe_caption(
        (
            "The workstation achieves peak seating stability while the operator calmly "
            "negotiates with her desktop, jacket game fully color-corrected for the "
            "office environment."
        ),
        evidence,
        "humorous_tech",
    )

    assert caption == (
        "The workstation keeps monitor, keyboard, and productivity latency neatly "
        "in view inside the open office."
    )


def test_ensure_safe_caption_maps_urban_road_to_traffic_fallback() -> None:
    evidence = EvidenceGraph(
        video_id="v1",
        overall_summary="Urban environment with multi-lane road.",
        main_event="Urban environment with multi-lane road.",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["Urban environment with multi-lane road."],
            )
        ],
    )

    caption = ensure_safe_caption(
        "Urban environment with multi-lane road. The important visual signal stays clear.",
        evidence,
        "humorous_tech",
    )

    assert (
        caption
        == "Autumn traffic gets beautiful color grading, even while road throughput "
        "stays stubbornly low between the buildings."
    )


def test_ensure_safe_caption_maps_vehicle_blur_to_traffic_fallback() -> None:
    evidence = EvidenceGraph(
        video_id="v1",
        overall_summary=(
            "The vehicles appear blurred due to motion, suggesting long exposure "
            "or time-lapse photography."
        ),
        main_event="Vehicles move through a city street",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["Vehicles move along an urban boulevard."],
            )
        ],
    )

    caption = ensure_safe_caption(
        (
            "The vehicles appear blurred due to motion, suggesting long exposure "
            "or time-lapse photography. The scene finds a little drama anyway."
        ),
        evidence,
        "sarcastic",
    )

    assert (
        caption
        == "The golden trees work overtime to make the slow city traffic look almost "
        "worth waiting for."
    )


def test_ensure_safe_caption_replaces_generic_v3_evidence() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="A video clip is shown.",
        main_event="A video clip is shown.",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["A video clip is shown."],
            )
        ],
    )

    caption = ensure_safe_caption("A video clip is shown.", evidence, "formal")

    assert (
        caption
        == "An office worker sits at a desktop computer inside a bright, modern "
        "open-plan workspace with other desks nearby."
    )


def test_ensure_safe_caption_rejects_contact_sheet_meta_evidence() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary=(
            "Actually, looking at similar tasks, usually for contact sheets without "
            "timecode, people estimate based on frame order. I'll create segments."
        ),
        main_event="A video clip is shown.",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=[
                    (
                        "Actually, looking at similar tasks, usually for contact sheets "
                        "without timecode, people estimate based on frame order."
                    )
                ],
            )
        ],
    )

    caption = ensure_safe_caption(
        "Actually, looking at similar tasks, usually for contact sheets without timecode, "
        "people estimate based on frame order. I'll create segments.",
        evidence,
        "sarcastic",
    )

    assert (
        caption
        == "Another heroic day at the desktop, surrounded by all the calm an open "
        "office can offer during serious computer work."
    )


def test_ensure_safe_caption_rejects_visible_text_artifact() -> None:
    evidence = EvidenceGraph(
        video_id="v3",
        overall_summary="No visible text that is legible.",
        main_event="No visible text that is legible.",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=10,
                observations=["No visible text that is legible."],
            )
        ],
    )

    caption = ensure_safe_caption("No visible text that is legible.", evidence, "formal")

    assert (
        caption
        == "An office worker sits at a desktop computer inside a bright, modern "
        "open-plan workspace with other desks nearby."
    )


def test_ensure_safe_caption_rejects_flower_contact_sheet_fallback() -> None:
    evidence = EvidenceGraph(
        video_id="flower",
        overall_summary=(
            "The image shows a contact sheet with 4 frames labeled F01, F02, F03, F04. "
            "Each frame shows a yellow/orange flower (looks like a dandelion) "
            "blooming progressively against a dark/black."
        ),
        main_event="A yellow flower blooms.",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=20,
                observations=[
                    "Each frame shows a yellow/orange flower blooming against a dark/black."
                ],
            )
        ],
    )

    caption = ensure_safe_caption(
        "A yellow flower blooms progressively across four frames against a dark background.",
        evidence,
        "formal",
    )

    assert (
        caption
        == "A yellow flower slowly opens its petals against a dark background in a "
        "steady bloom, keeping the bright center visible."
    )


def test_ensure_safe_caption_rejects_sample_count_pose_language() -> None:
    evidence = EvidenceGraph(
        video_id="flower",
        overall_summary="A yellow flower slowly blooms against a dark background.",
        main_event="A yellow flower blooms.",
        segments=[
            EvidenceSegment(
                start_seconds=0,
                end_seconds=20,
                observations=["A yellow flower opens its petals against a dark background."],
            )
        ],
    )

    caption = ensure_safe_caption(
        (
            "A yellow flower opens in four progressive stages, taking four patient "
            "steps from bud to bloom."
        ),
        evidence,
        "sarcastic",
    )

    assert (
        caption
        == "A yellow flower takes its time opening, giving the dark background plenty "
        "of suspense to work with."
    )


def test_ensure_safe_caption_truncates_long_caption() -> None:
    caption = ensure_safe_caption("Traffic " * 80, _evidence(), "humorous_tech")
    assert len(caption) <= 280
