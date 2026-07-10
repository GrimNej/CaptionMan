from __future__ import annotations

import json
import subprocess
from pathlib import Path

from pydantic import BaseModel


class VideoProbe(BaseModel):
    path: str
    duration_seconds: float | None = None
    width: int | None = None
    height: int | None = None
    has_audio: bool = False


def probe_video(path: Path) -> VideoProbe:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        str(path),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)
    data = json.loads(completed.stdout)
    streams = data.get("streams", [])
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), {})
    duration = data.get("format", {}).get("duration") or video.get("duration")
    return VideoProbe(
        path=path.name,
        duration_seconds=float(duration) if duration else None,
        width=video.get("width"),
        height=video.get("height"),
        has_audio=any(stream.get("codec_type") == "audio" for stream in streams),
    )
