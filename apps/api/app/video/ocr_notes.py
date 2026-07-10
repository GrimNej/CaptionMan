from __future__ import annotations


def summarize_visible_text(notes: list[str]) -> list[str]:
    return [note.strip() for note in notes if note.strip()]
