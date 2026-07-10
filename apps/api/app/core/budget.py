from __future__ import annotations

import time

from pydantic import BaseModel, Field


class BudgetExceededError(RuntimeError):
    pass


class BudgetState(BaseModel):
    video_id: str
    model_calls_used: int = 0
    max_model_calls: int
    started_at: float = Field(default_factory=time.monotonic)
    max_seconds: float
    call_stages: list[str] = Field(default_factory=list)

    def can_call_model(self) -> bool:
        return self.model_calls_used < self.max_model_calls and not self.should_fallback()

    def register_model_call(self, stage: str) -> None:
        if not self.can_call_model():
            raise BudgetExceededError(f"budget exceeded for {self.video_id}")
        self.model_calls_used += 1
        self.call_stages.append(stage)

    def should_fallback(self) -> bool:
        return (time.monotonic() - self.started_at) >= self.max_seconds
