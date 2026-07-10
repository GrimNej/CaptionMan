from __future__ import annotations

from fastapi import APIRouter

from app.core.config import Settings
from app.providers.model_registry import doctor_report

router = APIRouter()


@router.get("/doctor")
def doctor(live: bool = True) -> dict[str, object]:
    return doctor_report(Settings(), provider_check=live)
