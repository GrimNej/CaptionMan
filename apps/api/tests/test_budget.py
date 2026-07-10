from __future__ import annotations

import pytest
from app.core.budget import BudgetExceededError, BudgetState


def test_budget_prevents_excess_model_calls() -> None:
    budget = BudgetState(video_id="a", max_model_calls=1, max_seconds=60)
    budget.register_model_call("first")
    assert not budget.can_call_model()
    with pytest.raises(BudgetExceededError):
        budget.register_model_call("second")
