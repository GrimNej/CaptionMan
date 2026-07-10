from __future__ import annotations

from app.io.official_schema import InternalResult, VideoTask


def progressive_fallback_from_best_available_evidence(
    task: VideoTask,
    reason: str,
) -> InternalResult:
    subject = task.metadata.get("description") or "the provided video"
    return InternalResult(
        video_id=task.video_id,
        formal=f"{subject}.",
        sarcastic=f"{subject}, finding a little drama in the ordinary.",
        humorous_tech=f"{subject}, with the key visual signal still clear.",
        humorous_non_tech=f"{subject}, keeping the scene clear without overexplaining it.",
        requested_styles=task.requested_styles,
        fallback_reason=reason,
    )
