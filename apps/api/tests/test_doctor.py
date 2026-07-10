from __future__ import annotations

from app.core.config import Settings
from app.providers.model_registry import doctor_report


def test_mock_doctor_is_ok() -> None:
    report = doctor_report(Settings(ai_provider="mock"))
    assert report["checks"]["provider"]["ok"] is True


def test_proxy_doctor_fails_closed_without_base_url() -> None:
    report = doctor_report(Settings(ai_provider="proxy"))

    assert report["ok"] is False
    assert report["checks"]["provider"]["missing"] == ["PROXY_BASE_URL", "PROXY_TOKEN"]
    assert report["checks"]["routing"]["proxy_route_active"] is True


def test_proxy_doctor_requires_token() -> None:
    report = doctor_report(
        Settings(
            ai_provider="proxy",
            proxy_base_url="https://proxy.example.invalid",
        )
    )

    assert report["ok"] is False
    assert report["checks"]["provider"]["missing"] == ["PROXY_TOKEN"]


def test_fireworks_direct_is_explicit_direct_provider() -> None:
    report = doctor_report(
        Settings(
            ai_provider="fireworks_direct",
            fireworks_api_key="",
            vision_model="",
            text_model="",
            judge_model="",
        )
    )

    assert report["ok"] is False
    assert report["checks"]["provider"]["provider"] == "fireworks_direct"
    assert "FIREWORKS_API_KEY_OR_EMBEDDED_KEY" in report["checks"]["provider"]["missing"]


def test_lightweight_doctor_can_skip_provider_check() -> None:
    report = doctor_report(
        Settings(
            ai_provider="fireworks_direct",
            fireworks_api_key="",
            vision_model="",
            text_model="",
            judge_model="",
        ),
        provider_check=False,
    )

    assert report["checks"]["provider"]["provider"] == "fireworks_direct"
    assert report["checks"]["provider"]["skipped"] is True


def test_gemma_requirement_is_reported() -> None:
    report = doctor_report(
        Settings(
            ai_provider="mock",
            gemma_model="accounts/fireworks/models/gemma-4-31b-it",
            gemma_usage_mode="off",
            require_gemma_for_submission=True,
        )
    )

    assert report["ok"] is False
    assert report["checks"]["routing"]["gemma"]["configured"] is True
    assert report["checks"]["routing"]["gemma"]["active"] is False
    assert "Gemma is required" in " ".join(report["warnings"])
