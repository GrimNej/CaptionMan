from __future__ import annotations

from app.core.config import Settings
from app.io.official_schema import VideoTask
from app.providers.fireworks_direct import FireworksDirectProvider
from app.providers.model_registry import doctor_report


def test_fireworks_key_prefers_environment_value(tmp_path) -> None:
    embedded = tmp_path / "fireworks.key"
    embedded.write_text("embedded_test_key", encoding="utf-8")
    settings = Settings(
        fireworks_api_key="your_key_here",
        embedded_fireworks_key_path=embedded,
    )

    assert settings.resolved_fireworks_api_key() == "your_key_here"
    assert settings.fireworks_credential_source() == "local_env"


def test_fireworks_key_falls_back_to_embedded_file(tmp_path) -> None:
    embedded = tmp_path / "fireworks.key"
    embedded.write_text("embedded_test_key\n", encoding="utf-8")
    settings = Settings(
        fireworks_api_key="",
        embedded_fireworks_key_path=embedded,
    )

    assert settings.resolved_fireworks_api_key() == "embedded_test_key"
    assert settings.fireworks_credential_source() == "embedded_hackathon_key"


def test_direct_doctor_reports_embedded_credential_source(tmp_path) -> None:
    embedded = tmp_path / "fireworks.key"
    embedded.write_text("embedded_test_key", encoding="utf-8")
    report = doctor_report(
        Settings(
            ai_provider="fireworks_direct",
            fireworks_api_key="",
            vision_model="",
            text_model="",
            judge_model="",
            embedded_fireworks_key_path=embedded,
        )
    )

    assert report["checks"]["routing"]["credential_source"] == "embedded_hackathon_key"
    assert report["checks"]["provider"]["credential_source"] == "embedded_hackathon_key"
    assert "FIREWORKS_API_KEY_OR_EMBEDDED_KEY" not in report["checks"]["provider"]["missing"]


def test_fireworks_direct_uses_gemma_as_specialist_caption_model() -> None:
    provider = FireworksDirectProvider(
        Settings(
            text_model="accounts/fireworks/models/glm-5p2",
            gemma_model="accounts/fireworks/models/gemma-4-31b-it",
            gemma_usage_mode="specialist",
        )
    )

    assert provider._caption_model() == "accounts/fireworks/models/gemma-4-31b-it"


def test_fireworks_resolves_windows_file_uri_without_extra_root() -> None:
    provider = FireworksDirectProvider(Settings())
    task = VideoTask(video_id="local", video_uri="file:///E:/Trmp/348656_medium.mp4")

    assert str(provider._resolve_video(task)).replace("\\", "/") == "E:/Trmp/348656_medium.mp4"


def test_fireworks_resolves_legacy_windows_file_uri() -> None:
    provider = FireworksDirectProvider(Settings())
    task = VideoTask(video_id="local", video_uri="file://E:/Trmp/348656_medium.mp4")

    assert str(provider._resolve_video(task)).replace("\\", "/") == "E:/Trmp/348656_medium.mp4"
