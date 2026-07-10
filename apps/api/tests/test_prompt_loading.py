from __future__ import annotations

from app.providers.fireworks import _style_prompt


def test_fireworks_caption_prompt_loads_markdown_style_guide() -> None:
    prompt = _style_prompt("humorous_tech")

    assert "Quality target" in prompt
    assert "Sound like a witty human" in prompt
    assert "debugging unit" in prompt
