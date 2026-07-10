from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_validator():
    root = Path(__file__).resolve().parents[3]
    script = root / "scripts" / "validate_results.py"
    spec = importlib.util.spec_from_file_location("validate_results", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validator_rejects_debug_keys() -> None:
    validator = _load_validator()
    data = [
        {
            "task_id": "a",
            "captions": {
                "formal": "a",
                "sarcastic": "b",
                "humorous_tech": "c",
                "humorous_non_tech": "d",
            },
            "judge_replay": {},
        }
    ]
    try:
        validator.validate_data(data)
    except validator.ValidationError as exc:
        assert "debug keys" in str(exc)
    else:
        raise AssertionError("expected validation error")


def test_validator_accepts_requested_style_subset() -> None:
    validator = _load_validator()
    expected = validator.requested_styles_by_task(
        [
            {
                "task_id": "a",
                "video_url": "mock://video",
                "styles": ["formal", "sarcastic"],
            }
        ]
    )

    validator.validate_data(
        [
            {
                "task_id": "a",
                "captions": {
                    "formal": "A clear video scene is shown.",
                    "sarcastic": "A video scene happens, naturally.",
                },
            }
        ],
        expected_styles=expected,
    )


def test_validator_rejects_unrequested_style_when_input_is_provided() -> None:
    validator = _load_validator()
    expected = {"a": ["formal"]}

    try:
        validator.validate_data(
            [
                {
                    "task_id": "a",
                    "captions": {
                        "formal": "A clear video scene is shown.",
                        "sarcastic": "A video scene happens, naturally.",
                    },
                }
            ],
            expected_styles=expected,
        )
    except validator.ValidationError as exc:
        assert "unrequested caption styles" in str(exc)
    else:
        raise AssertionError("expected validation error")
