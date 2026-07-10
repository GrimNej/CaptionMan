from __future__ import annotations


def uncertainty_label(notes: list[str]) -> str:
    return "low" if not notes else "medium"
