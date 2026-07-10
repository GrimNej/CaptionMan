from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw


def build_contact_sheet(frames: list[Path], output: Path) -> Path:
    if not frames:
        raise ValueError("cannot build contact sheet without frames")
    output.parent.mkdir(parents=True, exist_ok=True)
    opened = [Image.open(frame).convert("RGB") for frame in frames]
    try:
        thumb_width = 320
        thumb_height = 180
        columns = min(3, len(opened))
        rows = math.ceil(len(opened) / columns)
        sheet = Image.new("RGB", (columns * thumb_width, rows * thumb_height), (10, 10, 10))
        draw = ImageDraw.Draw(sheet)
        for index, image in enumerate(opened):
            image.thumbnail((thumb_width, thumb_height))
            x = (index % columns) * thumb_width
            y = (index // columns) * thumb_height
            sheet.paste(image, (x, y))
            draw.rectangle((x + 6, y + 6, x + 58, y + 28), fill=(0, 0, 0))
            draw.text((x + 12, y + 10), f"F{index + 1:02d}", fill=(245, 230, 180))
        sheet.save(output, format="JPEG", quality=86)
    finally:
        for image in opened:
            image.close()
    return output
