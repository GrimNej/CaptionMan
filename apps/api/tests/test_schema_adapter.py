from __future__ import annotations

from app.io.official_schema import InternalResult
from app.io.schema_adapter import adapt_input, adapt_output


def test_adapt_input_accepts_official_track2_list() -> None:
    tasks = adapt_input(
        [
            {
                "task_id": "abc",
                "video_url": "mock://video",
                "styles": ["formal", "sarcastic"],
            }
        ]
    )
    assert tasks[0].video_id == "abc"
    assert tasks[0].video_uri == "mock://video"
    assert tasks[0].requested_styles == ["formal", "sarcastic"]


def test_adapt_input_does_not_infer_scene_from_task_id_or_url() -> None:
    tasks = adapt_input(
        [
            {
                "task_id": "v3",
                "video_url": (
                    "https://storage.googleapis.com/amd-hackathon-clips/"
                    "3044693-uhd_3840_2160_24fps.mp4"
                ),
                "styles": ["formal"],
            }
        ]
    )

    assert tasks[0].metadata == {}


def test_adapt_output_drops_debug_fields() -> None:
    official = adapt_output(
        [
            InternalResult(
                video_id="abc",
                formal="Formal.",
                sarcastic="Sarcastic.",
                humorous_tech="Tech.",
                humorous_non_tech="Non tech.",
                fallback_reason="not exported",
            )
        ]
    )
    dumped = [result.model_dump() for result in official]
    assert dumped == [
        {
            "task_id": "abc",
            "captions": {
                "formal": "Formal.",
                "sarcastic": "Sarcastic.",
                "humorous_tech": "Tech.",
                "humorous_non_tech": "Non tech.",
            },
        }
    ]
