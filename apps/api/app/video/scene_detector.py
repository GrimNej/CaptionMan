from __future__ import annotations


def detect_scene_boundaries(frame_count: int) -> list[int]:
    if frame_count <= 0:
        return []
    return [0, max(frame_count // 2, 0), frame_count - 1]
