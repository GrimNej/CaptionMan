from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_STYLES = ("formal", "sarcastic", "humorous_tech", "humorous_non_tech")
DEBUG_KEYS = {
    "evidence_file",
    "candidate_scores",
    "judge_replay",
    "debug_logs",
    "provider_metadata",
    "frame_paths",
    "base64_images",
    "timings",
    "model_ids",
    "stack_trace",
    "traceback",
    "results",
    "evidence",
    "evidence_graph",
    "court",
    "court_record",
    "debug",
    "metadata",
    "provider",
    "model",
    "logs",
    "inference_log",
    "frames",
    "error_trace",
}
MAX_CAPTION_CHARS = 500


class ValidationError(Exception):
    pass


def _load_json(path: Path) -> Any:
    if not path.exists():
        raise ValidationError(f"file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON: {exc}") from exc


def _results(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        results = data
    else:
        raise ValidationError(
            "top-level output must be the official Track 2 results list"
        )
    if not results:
        raise ValidationError("results must not be empty")
    if not all(isinstance(item, dict) for item in results):
        raise ValidationError("each result must be an object")
    return results


def requested_styles_by_task(input_data: Any) -> dict[str, list[str]]:
    if not isinstance(input_data, list) or not input_data:
        raise ValidationError("input must be a non-empty official Track 2 task list")
    expected: dict[str, list[str]] = {}
    for index, task in enumerate(input_data):
        if not isinstance(task, dict):
            raise ValidationError(f"input task {index} must be an object")
        task_id = task.get("task_id")
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValidationError(f"input task {index} missing task_id")
        if task_id in expected:
            raise ValidationError(f"duplicate input task_id: {task_id}")
        video_url = task.get("video_url")
        if not isinstance(video_url, str) or not video_url.strip():
            raise ValidationError(f"{task_id}: missing video_url")
        styles = task.get("styles")
        if styles is None or styles == []:
            requested = list(REQUIRED_STYLES)
        elif isinstance(styles, list) and all(
            isinstance(style, str) for style in styles
        ):
            requested = list(dict.fromkeys(styles))
        else:
            raise ValidationError(f"{task_id}: styles must be an array of strings")
        unknown = sorted(set(requested) - set(REQUIRED_STYLES))
        if unknown:
            raise ValidationError(f"{task_id}: unknown requested styles {unknown}")
        expected[task_id] = requested
    return expected


def validate_data(
    data: Any,
    expected_styles: dict[str, list[str]] | None = None,
) -> None:
    seen_task_ids: set[str] = set()
    for result in _results(data):
        leaked = DEBUG_KEYS.intersection(result)
        if leaked:
            raise ValidationError(
                f"debug keys leaked into official output: {sorted(leaked)}"
            )
        task_id = result.get("task_id")
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValidationError("missing task_id")
        if task_id in seen_task_ids:
            raise ValidationError(f"{task_id}: duplicate result")
        seen_task_ids.add(task_id)
        if set(result) != {"task_id", "captions"}:
            raise ValidationError(
                f"{task_id}: official result must contain only task_id and captions"
            )
        captions = result.get("captions")
        if not isinstance(captions, dict):
            raise ValidationError(f"{task_id}: captions must be an object")
        unknown_styles = set(captions) - set(REQUIRED_STYLES)
        if unknown_styles:
            raise ValidationError(
                f"{task_id}: unknown caption styles {sorted(unknown_styles)}"
            )
        if expected_styles is not None:
            if task_id not in expected_styles:
                raise ValidationError(f"{task_id}: unexpected result")
            missing_styles = [
                style for style in expected_styles[task_id] if style not in captions
            ]
            extra_styles = sorted(set(captions) - set(expected_styles[task_id]))
            if missing_styles:
                raise ValidationError(
                    f"{task_id}: missing caption styles {missing_styles}"
                )
            if extra_styles:
                raise ValidationError(
                    f"{task_id}: unrequested caption styles {extra_styles}"
                )
        elif not captions:
            raise ValidationError(f"{task_id}: captions must not be empty")
        for style, caption in captions.items():
            if not isinstance(caption, str) or not caption.strip():
                raise ValidationError(
                    f"{task_id}: missing or empty caption for {style}"
                )
            if "```" in caption:
                raise ValidationError(f"{task_id}: markdown fence in {style}")
            stripped = caption.strip()
            if stripped.startswith("{") or stripped.startswith("["):
                raise ValidationError(f"{task_id}: JSON-looking caption in {style}")
            if len(caption) > MAX_CAPTION_CHARS:
                raise ValidationError(f"{task_id}: caption too long for {style}")
        if any(value is None for value in result.values()) or any(
            value is None for value in captions.values()
        ):
            raise ValidationError(f"{task_id}: null value is not allowed")
    if expected_styles is not None:
        missing_results = sorted(set(expected_styles) - seen_task_ids)
        if missing_results:
            raise ValidationError(f"missing task results {missing_results}")


def validate_file(path: Path, input_path: Path | None = None) -> None:
    expected_styles = (
        requested_styles_by_task(_load_json(input_path))
        if input_path is not None
        else None
    )
    validate_data(_load_json(path), expected_styles=expected_styles)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    input_path: Path | None = None
    output_path: Path | None = None
    if len(args) == 1:
        output_path = Path(args[0])
    elif len(args) == 4 and args[0] == "--input" and args[2] == "--output":
        input_path = Path(args[1])
        output_path = Path(args[3])
    else:
        print(
            "usage: python scripts/validate_results.py output/results.json\n"
            "   or: python scripts/validate_results.py --input input/tasks.json --output output/results.json",
            file=sys.stderr,
        )
        return 2
    try:
        validate_file(output_path, input_path=input_path)
    except ValidationError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"validation passed: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
