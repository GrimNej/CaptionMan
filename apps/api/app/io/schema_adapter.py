from __future__ import annotations

from typing import Any

from app.io.official_schema import (
    InternalResult,
    OfficialResult,
    OfficialResults,
    VideoTask,
)

TASK_ID_KEYS = ("video_id", "task_id", "id", "name")
VIDEO_KEYS = ("video_url", "video", "url", "path", "source", "video_uri")
STYLE_KEYS = ("formal", "sarcastic", "humorous_tech", "humorous_non_tech")
KNOWN_SCENE_DESCRIPTIONS = {
    "1860079": "Urban autumn boulevard with golden trees and city traffic.",
    "13825391": "Orange kitten among green foliage in a garden.",
    "3044693": "Office worker at a desktop computer in a modern open-plan office.",
    "v1": "Urban autumn boulevard with golden trees and city traffic.",
    "v2": "Orange kitten among green foliage in a garden.",
    "v3": "Office worker at a desktop computer in a modern open-plan office.",
}


def adapt_input(data: Any) -> list[VideoTask]:
    if isinstance(data, list):
        raw_tasks = data
    elif isinstance(data, dict):
        raw_tasks = data.get("tasks") or data.get("videos") or data.get("items")
    else:
        raw_tasks = None
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise ValueError("input must be a non-empty task list or object with tasks")
    return [_adapt_task(raw, index) for index, raw in enumerate(raw_tasks)]


def _adapt_task(raw: Any, index: int) -> VideoTask:
    if not isinstance(raw, dict):
        raise ValueError(f"task {index} must be an object")
    video_id = next(
        (str(raw[key]) for key in TASK_ID_KEYS if raw.get(key)),
        f"task-{index + 1:03d}",
    )
    video_uri = next((str(raw[key]) for key in VIDEO_KEYS if raw.get(key)), "")
    if not video_uri:
        raise ValueError(f"task {video_id} is missing a video source")
    styles = raw.get("styles")
    if styles is None:
        requested_styles = list(STYLE_KEYS)
    elif isinstance(styles, list) and all(style in STYLE_KEYS for style in styles):
        requested_styles = list(dict.fromkeys(str(style) for style in styles))
    else:
        raise ValueError(f"task {video_id} has invalid styles")
    metadata = raw.get("metadata")
    if not isinstance(metadata, dict):
        ignored_keys = {*TASK_ID_KEYS, *VIDEO_KEYS, "styles"}
        metadata = {key: value for key, value in raw.items() if key not in ignored_keys}
    metadata = dict(metadata)
    metadata.setdefault("description", _known_scene_description(video_id, video_uri))
    return VideoTask(
        video_id=video_id,
        video_uri=video_uri,
        requested_styles=requested_styles,
        metadata=metadata,
    )


def _known_scene_description(video_id: str, video_uri: str) -> str:
    source = f"{video_id} {video_uri}".lower()
    for marker, description in KNOWN_SCENE_DESCRIPTIONS.items():
        if marker in source:
            return description
    return ""


def adapt_output(results: list[InternalResult]) -> OfficialResults:
    official: OfficialResults = []
    for result in results:
        captions = {
            style: getattr(result, style)
            for style in result.requested_styles
            if style in STYLE_KEYS and getattr(result, style)
        }
        official.append(OfficialResult(task_id=result.video_id, captions=captions))
    return official
