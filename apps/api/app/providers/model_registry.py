from __future__ import annotations

import os
import platform
import shutil
from pathlib import Path

from app.core.config import Settings
from app.providers.base import CaptionProvider
from app.providers.fireworks_direct import FireworksDirectProvider
from app.providers.mock import MockProvider
from app.providers.proxy import ProxyProvider


def make_provider(settings: Settings) -> CaptionProvider:
    if settings.ai_provider in {"fireworks", "fireworks_direct"}:
        return FireworksDirectProvider(settings)
    if settings.ai_provider == "proxy":
        return ProxyProvider(settings)
    return MockProvider()


def doctor_report(settings: Settings, provider_check: bool = True) -> dict[str, object]:
    provider_report = (
        make_provider(settings).doctor()
        if provider_check
        else {
            "provider": settings.ai_provider,
            "ok": True,
            "skipped": True,
            "reason": "provider check disabled for lightweight status",
        }
    )
    route = _route_report(settings)
    filesystem = _filesystem_report()
    warnings = _warnings(settings, route, filesystem)
    checks = {
        "python_package": True,
        "ffmpeg": shutil.which("ffmpeg") is not None,
        "ffprobe": shutil.which("ffprobe") is not None,
        "filesystem": filesystem,
        "mode": {
            "official_mode": settings.official_mode,
            "pipeline_mode": settings.pipeline_mode,
            "ai_provider": settings.ai_provider,
        },
        "routing": route,
        "provider": provider_report,
        "track2": {
            "allowed_models_required": False,
            "allowed_models_env_present": bool(os.environ.get("ALLOWED_MODELS")),
        },
    }
    ok = bool(checks["ffmpeg"] and checks["ffprobe"] and provider_report.get("ok"))
    if settings.require_gemma_for_submission and not route["gemma"]["active"]:
        ok = False
    return {
        "ok": ok,
        "checks": checks,
        "warnings": warnings,
    }


def _route_report(settings: Settings) -> dict[str, object]:
    visual_model = settings.vision_model or settings.gemma_model
    caption_model = _caption_model(settings)
    repair_model = settings.repair_model or settings.gemma_model or settings.judge_model
    gemma_active = bool(settings.gemma_model) and settings.gemma_usage_mode in {
        "specialist",
        "fallback",
    }
    return {
        "model_routing_mode": settings.model_routing_mode,
        "champion_route": settings.champion_route,
        "official_safe": settings.ai_provider in {"mock", "proxy", "fireworks", "fireworks_direct"},
        "visual_model": visual_model or None,
        "visual_fallback_model": settings.vision_fallback_model or None,
        "caption_model": caption_model or None,
        "repair_model": repair_model or None,
        "proxy_route_active": settings.ai_provider == "proxy",
        "credential_source": _credential_source(settings),
        "gemma": {
            "configured": bool(settings.gemma_model),
            "usage_mode": settings.gemma_usage_mode,
            "active": gemma_active,
            "required_for_submission": settings.require_gemma_for_submission,
            "model": settings.gemma_model or None,
        },
    }


def _caption_model(settings: Settings) -> str:
    if settings.gemma_usage_mode == "specialist" and settings.gemma_model:
        return settings.gemma_model
    return settings.text_model or settings.gemma_model


def _credential_source(settings: Settings) -> str:
    if settings.ai_provider == "proxy":
        return "proxy" if settings.proxy_token else "proxy_missing_token"
    if settings.ai_provider in {"fireworks", "fireworks_direct"}:
        return settings.fireworks_credential_source()
    return "none_required"


def _filesystem_report() -> dict[str, object]:
    input_path = Path("/input")
    output_path = Path("/output")
    return {
        "input_mount_present": input_path.exists(),
        "input_readable": input_path.exists() and os.access(input_path, os.R_OK),
        "output_mount_present": output_path.exists(),
        "output_writable": output_path.exists() and os.access(output_path, os.W_OK),
        "machine": platform.machine(),
        "linux_amd64": platform.machine().lower() in {"x86_64", "amd64"},
    }


def _warnings(
    settings: Settings,
    route: dict[str, object],
    filesystem: dict[str, object],
) -> list[str]:
    warnings: list[str] = []
    if settings.ai_provider in {"fireworks", "fireworks_direct"} and settings.official_mode:
        warnings.append(
            "official mode is using direct Fireworks credentials; use only a temporary limited "
            "hackathon key for final direct packaging"
        )
    if settings.ai_provider == "proxy" and not settings.proxy_token:
        warnings.append("proxy route has no PROXY_TOKEN configured")
    if settings.require_gemma_for_submission and not route["gemma"]["active"]:  # type: ignore[index]
        warnings.append("Gemma is required for submission but is not active in the selected route")
    if settings.official_mode and settings.caption_candidates_per_style > 1:
        warnings.append("official mode forces one caption candidate per style")
    if filesystem["output_mount_present"] and not filesystem["output_writable"]:
        warnings.append("/output is present but not writable")
    return warnings
