from __future__ import annotations

from pathlib import Path

from PIL import Image


def compress_image(path: Path, output: Path, max_width: int, quality: int) -> Path:
    with Image.open(path) as image:
        image.thumbnail((max_width, max_width * 10))
        output.parent.mkdir(parents=True, exist_ok=True)
        image.convert("RGB").save(output, format="JPEG", quality=quality)
    return output
