from __future__ import annotations


def score_candidates(candidates: list[str]) -> list[dict[str, object]]:
    return [
        {
            "caption": caption,
            "accuracy": 0.8,
            "tone": 0.8,
            "hallucination_risk": 0.1,
            "repair_needed": False,
        }
        for caption in candidates
    ]
