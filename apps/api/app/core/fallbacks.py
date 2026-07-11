from __future__ import annotations

from app.io.official_schema import InternalResult, VideoTask


def progressive_fallback_from_best_available_evidence(
    task: VideoTask,
    reason: str,
) -> InternalResult:
    subject = str(task.metadata.get("description") or "The provided video")
    subject = subject.rstrip(". ")
    return InternalResult(
        video_id=task.video_id,
        formal=f"{subject}.",
        sarcastic=f"{subject}, taking the ordinary scene impressively seriously.",
        humorous_tech=f"{subject}, delivering a concise real-world status update.",
        humorous_non_tech=f"{subject}, with enough everyday drama to earn a second look.",
        requested_styles=task.requested_styles,
        fallback_reason=reason,
    )
