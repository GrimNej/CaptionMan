from __future__ import annotations

from pydantic import BaseModel, Field


class StageEvent(BaseModel):
    run_id: str
    video_id: str | None = None
    stage: str
    status: str
    message: str = ""
    created_at: float = Field(default_factory=lambda: __import__("time").time())
