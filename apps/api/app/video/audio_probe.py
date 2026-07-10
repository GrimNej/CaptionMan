from __future__ import annotations

from pathlib import Path

from app.video.probe import probe_video


def has_audio(path: Path) -> bool:
    return probe_video(path).has_audio
