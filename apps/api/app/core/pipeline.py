from __future__ import annotations

from app.core.budget import BudgetExceededError, BudgetState
from app.core.config import Settings
from app.core.fallbacks import progressive_fallback_from_best_available_evidence
from app.court.candidate_generator import generate_candidates
from app.court.caption_safety import ensure_safe_caption
from app.court.final_selector import select_final
from app.court.hard_rules import validate_caption
from app.evidence.timeline_builder import build_evidence
from app.io.official_schema import InternalResult, VideoTask
from app.providers.base import CaptionStyle
from app.providers.model_registry import make_provider

STYLES: tuple[CaptionStyle, ...] = (
    "formal",
    "sarcastic",
    "humorous_tech",
    "humorous_non_tech",
)


def run_pipeline(
    tasks: list[VideoTask],
    settings: Settings,
) -> tuple[list[InternalResult], list[dict[str, object]]]:
    provider = make_provider(settings)
    results: list[InternalResult] = []
    replay: list[dict[str, object]] = []
    for task in tasks:
        budget = BudgetState(
            video_id=task.video_id,
            max_model_calls=settings.max_model_calls_per_video,
            max_seconds=settings.max_seconds_per_video,
        )
        try:
            if hasattr(provider, "build_evidence"):
                budget.register_model_call("evidence:vision")
                evidence = provider.build_evidence(task)  # type: ignore[attr-defined]
            else:
                evidence = build_evidence(task)
            style_outputs: dict[str, str] = {}
            court_rows: list[dict[str, object]] = []
            requested_styles = (
                tuple(style for style in STYLES if style in set(task.requested_styles)) or STYLES
            )
            for style in requested_styles:
                candidates = generate_candidates(task, evidence, style, provider, budget, settings)
                accepted = [caption for caption in candidates if validate_caption(caption).ok]
                caption = ensure_safe_caption(
                    select_final(accepted or candidates, style), evidence, style
                )
                style_outputs[style] = caption
                court_rows.append({"style": style, "candidates": candidates, "selected": caption})
            for style in STYLES:
                style_outputs.setdefault(style, "")
            result = InternalResult(
                video_id=task.video_id,
                requested_styles=list(requested_styles),
                **style_outputs,
            )
        except BudgetExceededError:
            result = progressive_fallback_from_best_available_evidence(task, "budget_exceeded")
            court_rows = []
            evidence = build_evidence(task)
        results.append(result)
        replay.append(
            {
                "video_id": task.video_id,
                "evidence": evidence.model_dump(),
                "caption_court": court_rows,
                "budget": budget.model_dump(),
            }
        )
    return results, replay
