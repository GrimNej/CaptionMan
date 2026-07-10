from __future__ import annotations


def repair_caption(caption: str) -> str:
    return caption.strip().replace("```", "")
