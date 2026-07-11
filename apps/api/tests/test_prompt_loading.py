from __future__ import annotations

from app.providers.fireworks import _batch_prompt, _style_prompt


def test_fireworks_caption_prompt_loads_markdown_style_guide() -> None:
    prompt = _style_prompt("humorous_tech")

    assert "recognizable technology or programming metaphor" in prompt
    assert "main visible subject" in prompt


def test_fireworks_batch_prompt_tracks_official_scoring_dimensions() -> None:
    prompt = _batch_prompt()

    assert "Accuracy" in prompt
    assert "Style match" in prompt
    assert "humorous_non_tech" in prompt
