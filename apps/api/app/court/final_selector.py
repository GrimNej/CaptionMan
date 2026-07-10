from __future__ import annotations


def select_final(candidates: list[str], _style: str) -> str:
    return next(
        (caption.strip() for caption in candidates if caption.strip()),
        "A short clip is shown.",
    )
