from __future__ import annotations

from app.providers.fireworks import _batch_prompt, _evidence_prompt, _style_prompt


def test_fireworks_caption_prompt_loads_markdown_style_guide() -> None:
    prompt = _style_prompt("humorous_tech")

    assert "recognizable technology or programming metaphor" in prompt
    assert "main visible subject" in prompt


def test_fireworks_batch_prompt_tracks_official_scoring_dimensions() -> None:
    prompt = _batch_prompt()

    assert "Accuracy" in prompt
    assert "Style match" in prompt
    assert "humorous_non_tech" in prompt
    assert "image-production process" in prompt


def test_fireworks_evidence_prompt_does_not_infer_visual_style_from_blur() -> None:
    prompt = _evidence_prompt(duration_seconds=30, image_count=10)

    assert "do not prove" in prompt
    assert "painterly" in prompt
    assert "separate monitor" in prompt
    assert "hairstyle" in prompt
