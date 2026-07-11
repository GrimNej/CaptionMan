from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ai_provider: Literal["mock", "fireworks", "fireworks_direct", "proxy"] = "mock"
    official_mode: bool = False
    model_routing_mode: Literal["mock", "champion", "tournament"] = "mock"
    champion_route: str = "mock_baseline"
    gemma_usage_mode: Literal["off", "specialist", "fallback"] = "off"
    require_gemma_for_submission: bool = False
    fireworks_api_key: str = ""
    fireworks_base_url: str = "https://api.fireworks.ai/inference/v1"
    vision_model: str = Field(
        default="",
        validation_alias=AliasChoices("VISION_MODEL", "DEFAULT_VISION_MODEL"),
    )
    vision_fallback_model: str = ""
    text_model: str = Field(
        default="",
        validation_alias=AliasChoices("TEXT_MODEL", "DEFAULT_TEXT_MODEL"),
    )
    judge_model: str = ""
    repair_model: str = ""
    gemma_model: str = ""
    enable_gemma_court: bool = False
    proxy_base_url: str = ""
    proxy_token: str = Field(
        default="",
        validation_alias=AliasChoices("PROXY_TOKEN", "PROXY_API_KEY"),
    )
    proxy_health_path: str = "/health"
    proxy_caption_path: str = "/captionman/infer"
    proxy_repair_path: str = "/captionman/repair"
    proxy_doctor_live_check: bool = True
    embedded_fireworks_key_path: Path = Field(default=Path("/app/.captionman/final_fireworks_key"))

    pipeline_mode: Literal["fast", "balanced", "quality"] = "balanced"
    num_frames: int = 12
    min_frames: int = 10
    max_frames: int = 14
    scene_threshold: float = 0.30
    frame_max_width: int = 768
    frame_jpeg_quality: int = 82
    frame_dedupe_hamming_threshold: int = 6
    caption_candidates_per_style: int = 2
    enable_self_repair: bool = True
    max_repair_attempts_per_style: int = 1
    max_caption_recovery_calls: int = 3
    max_video_seconds: int = 130
    max_seconds_per_video: float = 120
    max_total_seconds: float = 900
    max_model_calls_per_video: int = 14
    max_evidence_attempts: int = 2
    request_timeout_seconds: int = 120
    max_retries: int = 3
    style_concurrency: int = 2
    run_concurrency: int = 1
    fireworks_doctor_live_check: bool = True
    fireworks_max_output_tokens: int = 220
    fireworks_temperature: float = 0.2

    max_redirects: int = 3
    max_download_mb: int = 250
    download_timeout_seconds: int = 60

    data_dir: Path = Field(default=Path(".data"))
    cors_origins: str = "http://localhost:3000"

    def resolved_fireworks_api_key(self) -> str:
        if self.fireworks_api_key:
            return self.fireworks_api_key
        try:
            if self.embedded_fireworks_key_path.exists():
                return self.embedded_fireworks_key_path.read_text(encoding="utf-8").strip()
        except OSError:
            return ""
        return ""

    def fireworks_credential_source(self) -> str:
        if self.fireworks_api_key:
            return "local_env"
        if self.embedded_fireworks_key_path.exists():
            return "embedded_hackathon_key"
        return "missing"
