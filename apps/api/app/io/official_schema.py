from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class VideoTask(BaseModel):
    model_config = ConfigDict(extra="allow")

    video_id: str
    video_uri: str
    requested_styles: list[str] = Field(
        default_factory=lambda: ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]
    )
    metadata: dict[str, object] = Field(default_factory=dict)


class InternalResult(BaseModel):
    video_id: str
    formal: str
    sarcastic: str
    humorous_tech: str
    humorous_non_tech: str
    requested_styles: list[str] = Field(
        default_factory=lambda: ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]
    )
    fallback_reason: str | None = None


class OfficialResult(BaseModel):
    task_id: str
    captions: dict[str, str]


OfficialResults = list[OfficialResult]
