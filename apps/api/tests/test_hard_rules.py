from __future__ import annotations

from app.court.hard_rules import validate_caption


def test_hard_rules_reject_markdown_fence() -> None:
    result = validate_caption("```json\n{}\n```")
    assert not result.ok
    assert "markdown_fence" in result.reasons


def test_hard_rules_accept_plain_caption() -> None:
    assert validate_caption("A person moves through a short scene.").ok
