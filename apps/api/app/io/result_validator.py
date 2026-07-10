from __future__ import annotations

from typing import Any

REQUIRED_STYLES = ("formal", "sarcastic", "humorous_tech", "humorous_non_tech")
MAX_CAPTION_CHARS = 500


class OfficialResultValidationError(ValueError):
    pass


def validate_official_payload(
    payload: Any,
    expected_styles_by_task: dict[str, list[str]] | None = None,
) -> None:
    if not isinstance(payload, list) or not payload:
        raise OfficialResultValidationError("official output must be a non-empty list")
    seen_task_ids: set[str] = set()
    for result in payload:
        if not isinstance(result, dict):
            raise OfficialResultValidationError("each official result must be an object")
        if set(result) != {"task_id", "captions"}:
            raise OfficialResultValidationError(
                "official result must contain only task_id and captions"
            )
        task_id = result.get("task_id")
        if not isinstance(task_id, str) or not task_id.strip():
            raise OfficialResultValidationError("missing task_id")
        if task_id in seen_task_ids:
            raise OfficialResultValidationError(f"{task_id}: duplicate result")
        seen_task_ids.add(task_id)
        captions = result.get("captions")
        if not isinstance(captions, dict):
            raise OfficialResultValidationError(f"{task_id}: captions must be an object")
        unknown = set(captions) - set(REQUIRED_STYLES)
        if unknown:
            raise OfficialResultValidationError(
                f"{task_id}: unknown caption styles {sorted(unknown)}"
            )
        expected_styles = (
            expected_styles_by_task.get(task_id) if expected_styles_by_task is not None else None
        )
        if expected_styles is not None:
            missing = [style for style in expected_styles if style not in captions]
            extra = sorted(set(captions) - set(expected_styles))
            if missing:
                raise OfficialResultValidationError(f"{task_id}: missing caption styles {missing}")
            if extra:
                raise OfficialResultValidationError(
                    f"{task_id}: unrequested caption styles {extra}"
                )
        elif not captions:
            raise OfficialResultValidationError(f"{task_id}: captions must not be empty")
        for style, caption in captions.items():
            if not isinstance(caption, str) or not caption.strip():
                raise OfficialResultValidationError(f"{task_id}: missing caption for {style}")
            if len(caption) > MAX_CAPTION_CHARS:
                raise OfficialResultValidationError(f"{task_id}: caption too long for {style}")
            if caption.strip().startswith(("{", "[")) or "```" in caption:
                raise OfficialResultValidationError(f"{task_id}: unsafe caption for {style}")
    if expected_styles_by_task is not None:
        missing_results = sorted(set(expected_styles_by_task) - seen_task_ids)
        extra_results = sorted(seen_task_ids - set(expected_styles_by_task))
        if missing_results:
            raise OfficialResultValidationError(f"missing task results {missing_results}")
        if extra_results:
            raise OfficialResultValidationError(f"unexpected task results {extra_results}")
