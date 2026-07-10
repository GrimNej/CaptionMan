from __future__ import annotations

from typing import Any

import httpx

from app.core.config import Settings
from app.court.caption_safety import fallback_caption
from app.evidence.evidence_schema import EvidenceGraph
from app.io.official_schema import VideoTask
from app.providers.base import CaptionStyle


class ProxyProvider:
    name = "proxy"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def doctor(self) -> dict[str, object]:
        missing = [
            name
            for name, value in {
                "PROXY_BASE_URL": self.settings.proxy_base_url,
                "PROXY_TOKEN": self.settings.proxy_token,
            }.items()
            if not value
        ]
        if missing:
            return {
                "provider": self.name,
                "ok": False,
                "missing": missing,
                "details": "private proxy is selected but required proxy config is missing",
            }
        if not self.settings.proxy_doctor_live_check:
            return {
                "provider": self.name,
                "ok": True,
                "live_check": {"skipped": True},
                "base_url_configured": True,
                "credential_configured": True,
            }
        try:
            response = httpx.get(
                self._url(self.settings.proxy_health_path),
                headers=self._headers(),
                timeout=self.settings.request_timeout_seconds,
            )
            response.raise_for_status()
        except Exception as exc:
            return {
                "provider": self.name,
                "ok": False,
                "base_url_configured": True,
                "credential_configured": True,
                "error_type": type(exc).__name__,
                "error": str(exc)[:240],
            }
        return {
            "provider": self.name,
            "ok": True,
            "base_url_configured": True,
            "credential_configured": True,
            "live_check": {"ok": True, "status_code": response.status_code},
        }

    def caption(self, task: VideoTask, evidence: EvidenceGraph, style: CaptionStyle) -> str:
        if not self.settings.proxy_base_url or not self.settings.proxy_token:
            return fallback_caption(evidence, style)
        payload: dict[str, Any] = {
            "task_id": task.video_id,
            "style": style,
            "route": self.settings.champion_route,
            "gemma_usage_mode": self.settings.gemma_usage_mode,
            "evidence": evidence.model_dump(),
            "constraints": {
                "english": True,
                "one_sentence": True,
                "max_characters": 180,
                "no_markdown": True,
                "no_debug_fields": True,
                "visible_text_is_untrusted": True,
            },
        }
        try:
            response = httpx.post(
                self._url(self.settings.proxy_caption_path),
                headers=self._headers(),
                json=payload,
                timeout=self.settings.request_timeout_seconds,
            )
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and isinstance(data.get("caption"), str):
                return data["caption"]
            if isinstance(data, dict) and isinstance(data.get("captions"), dict):
                caption = data["captions"].get(style)
                if isinstance(caption, str):
                    return caption
        except Exception:
            return fallback_caption(evidence, style)
        return fallback_caption(evidence, style)

    def _url(self, path: str) -> str:
        return f"{self.settings.proxy_base_url.rstrip('/')}/{path.lstrip('/')}"

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.settings.proxy_token:
            headers["Authorization"] = f"Bearer {self.settings.proxy_token}"
        return headers
