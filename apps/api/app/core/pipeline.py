from __future__ import annotations

from typing import cast

from app.core.budget import BudgetExceededError, BudgetState
from app.core.config import Settings
from app.core.fallbacks import progressive_fallback_from_best_available_evidence
from app.court.candidate_generator import generate_candidates
from app.court.caption_safety import (
    caption_is_safe_for_evidence,
    ensure_safe_caption,
    fallback_caption,
)
from app.court.final_selector import select_final
from app.court.hard_rules import validate_caption
from app.evidence.evidence_schema import EvidenceGraph
from app.evidence.timeline_builder import build_evidence
from app.io.official_schema import InternalResult, VideoTask
from app.providers.base import BatchCaptionProvider, CaptionStyle, EvidenceProvider
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
        evidence = build_evidence(task)
        court_rows: list[dict[str, object]] = []
        try:
            if hasattr(provider, "build_evidence"):
                evidence = _build_provider_evidence(
                    cast(EvidenceProvider, provider),
                    task,
                    evidence,
                    budget,
                    settings,
                )
            style_outputs: dict[str, str] = {}
            requested_styles = (
                tuple(style for style in STYLES if style in set(task.requested_styles)) or STYLES
            )
            batch_method = getattr(provider, "caption_batch", None)
            batch_outputs: dict[CaptionStyle, str] = {}
            caption_recovery_calls = 0
            if callable(batch_method) and budget.can_call_model():
                budget.register_model_call("captions:batch")
                try:
                    batch_provider = cast(BatchCaptionProvider, provider)
                    batch_outputs = batch_provider.caption_batch(task, evidence, requested_styles)
                except Exception:  # noqa: BLE001
                    batch_outputs = {}
            for style in requested_styles:
                candidates = []
                batch_caption = batch_outputs.get(style, "")
                if batch_caption and caption_is_safe_for_evidence(
                    batch_caption,
                    evidence,
                    style,
                ):
                    candidates.append(batch_caption)
                if not candidates and caption_recovery_calls < settings.max_caption_recovery_calls:
                    try:
                        candidates = generate_candidates(
                            task, evidence, style, provider, budget, settings
                        )
                        caption_recovery_calls += 1
                    except Exception:  # noqa: BLE001
                        candidates = [fallback_caption(evidence, style)]
                if not candidates:
                    candidates = [fallback_caption(evidence, style)]
                accepted = [
                    caption
                    for caption in candidates
                    if validate_caption(caption).ok
                    and caption_is_safe_for_evidence(caption, evidence, style)
                ]
                selected = select_final(accepted or candidates, style)
                caption = ensure_safe_caption(selected, evidence, style)
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
            if evidence.overall_summary and evidence.overall_summary != "A short video clip":
                style_outputs = {style: fallback_caption(evidence, style) for style in STYLES}
                result = InternalResult(
                    video_id=task.video_id,
                    requested_styles=task.requested_styles,
                    fallback_reason="budget_exceeded",
                    **style_outputs,
                )
            else:
                result = progressive_fallback_from_best_available_evidence(task, "budget_exceeded")
            court_rows = []
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


def _build_provider_evidence(
    provider: EvidenceProvider,
    task: VideoTask,
    initial_evidence: EvidenceGraph,
    budget: BudgetState,
    settings: Settings,
) -> EvidenceGraph:
    best_evidence = initial_evidence
    attempts = max(1, settings.max_evidence_attempts)
    for attempt in range(attempts):
        if not budget.can_call_model():
            break
        budget.register_model_call(f"evidence:vision:{attempt + 1}")
        try:
            candidate = provider.build_evidence(task, attempt=attempt)
        except Exception:  # noqa: BLE001
            continue
        best_evidence = candidate
        if _evidence_is_usable(candidate):
            break
    return best_evidence


def _evidence_is_usable(evidence: EvidenceGraph) -> bool:
    generic = {
        "a short video clip",
        "a short video clip is shown",
        "a video clip is shown",
        "the provided video",
    }
    summary = evidence.overall_summary.strip().lower().rstrip(".")
    event = evidence.main_event.strip().lower().rstrip(".")
    if summary in generic and event in generic:
        return False
    combined = f"{summary} {event}"
    if "model returned unstructured visual evidence" in combined:
        return False
    return len(combined.split()) >= 6
