from __future__ import annotations

from pydantic import BaseModel


class HardRuleResult(BaseModel):
    ok: bool
    reasons: list[str]


def validate_caption(caption: str) -> HardRuleResult:
    reasons: list[str] = []
    stripped = caption.strip()
    if not stripped:
        reasons.append("empty")
    if "```" in stripped:
        reasons.append("markdown_fence")
    if stripped.startswith("{") or stripped.startswith("["):
        reasons.append("json_like")
    if len(stripped) > 500:
        reasons.append("too_long")
    if "\n" in stripped:
        reasons.append("multiline")
    return HardRuleResult(ok=not reasons, reasons=reasons)
