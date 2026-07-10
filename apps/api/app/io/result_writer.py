from __future__ import annotations

from pathlib import Path

from app.io.official_schema import InternalResult
from app.io.result_validator import validate_official_payload
from app.io.schema_adapter import adapt_output
from app.utils.atomic_write import atomic_write_json


def write_official_results(results: list[InternalResult], path: Path) -> None:
    official = adapt_output(results)
    payload = [result.model_dump() for result in official]
    expected_styles_by_task = {
        result.video_id: list(result.requested_styles)
        for result in results
        if result.requested_styles
    }
    validate_official_payload(payload, expected_styles_by_task=expected_styles_by_task)
    atomic_write_json(path, payload)
