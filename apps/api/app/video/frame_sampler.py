from __future__ import annotations

import subprocess
from pathlib import Path

from app.video.probe import probe_video


def sample_frames(video: Path, output_dir: Path, count: int) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_count = max(count, 0)
    if safe_count == 0:
        return []
    probe = probe_video(video)
    duration = max(float(probe.duration_seconds or safe_count), 0.1)
    timestamps = uniform_timestamps(duration, safe_count)
    frames: list[Path] = []
    for index, timestamp in enumerate(timestamps):
        frame = output_dir / f"frame-{index:03d}.jpg"
        command = [
            "ffmpeg",
            "-y",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-q:v",
            "3",
            str(frame),
        ]
        subprocess.run(command, check=True, capture_output=True, text=True, timeout=45)
        if frame.exists() and frame.stat().st_size > 0:
            frames.append(frame)
    return frames


def uniform_timestamps(duration_seconds: float, count: int) -> list[float]:
    if count <= 0:
        return []
    duration = max(duration_seconds, 0.1)
    if count == 1:
        return [duration / 2]
    margin = min(0.5, duration * 0.02)
    usable = max(duration - (2 * margin), 0)
    return [
        min(duration - 0.05, max(0.0, margin + (usable * index / (count - 1))))
        for index in range(count)
    ]
