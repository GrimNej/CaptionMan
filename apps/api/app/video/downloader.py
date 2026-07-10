from __future__ import annotations

from pathlib import Path

import httpx

from app.core.config import Settings
from app.utils.url_security import assert_safe_url


def download_video(url: str, destination: Path, settings: Settings) -> Path:
    assert_safe_url(url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    max_bytes = settings.max_download_mb * 1024 * 1024
    with httpx.stream(
        "GET",
        url,
        timeout=settings.download_timeout_seconds,
        follow_redirects=False,
    ) as response:
        response.raise_for_status()
        size = 0
        with destination.open("wb") as handle:
            for chunk in response.iter_bytes():
                size += len(chunk)
                if size > max_bytes:
                    raise ValueError("download exceeds MAX_DOWNLOAD_MB")
                handle.write(chunk)
    return destination
