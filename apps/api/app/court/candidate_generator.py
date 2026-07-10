from __future__ import annotations

from app.core.budget import BudgetState
from app.core.config import Settings
from app.evidence.evidence_schema import EvidenceGraph
from app.io.official_schema import VideoTask
from app.providers.base import CaptionProvider, CaptionStyle


def generate_candidates(
    task: VideoTask,
    evidence: EvidenceGraph,
    style: CaptionStyle,
    provider: CaptionProvider,
    budget: BudgetState,
    settings: Settings,
) -> list[str]:
    count = 1 if settings.official_mode else max(1, settings.caption_candidates_per_style)
    candidates: list[str] = []
    for _ in range(count):
        if not budget.can_call_model():
            break
        budget.register_model_call(f"caption:{style}")
        candidates.append(provider.caption(task, evidence, style))
    if not candidates:
        candidates.append(evidence.overall_summary.rstrip(".") + ".")
    return candidates
