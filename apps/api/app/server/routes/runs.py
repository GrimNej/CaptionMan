from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated
from urllib.parse import urlparse
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel

from app.utils.url_security import assert_safe_url

router = APIRouter()
API_ROOT = Path(__file__).resolve().parents[3]
REPO_ROOT = API_ROOT.parents[1] if len(API_ROOT.parents) > 1 else API_ROOT
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
TRACK2_STYLES = ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]


class RunCreate(BaseModel):
    input_path: str = "input/tasks.json"


class UrlRunCreate(BaseModel):
    video_url: str
    task_id: str = ""
    description: str = ""


@router.post("/runs")
def create_run(payload: RunCreate, request: Request) -> dict[str, object]:
    run_id = request.app.state.runner.start_run(resolve_input_path(payload.input_path))
    return {"run_id": run_id, "status": "queued"}


@router.post("/runs/url")
def create_url_run(payload: UrlRunCreate, request: Request) -> dict[str, object]:
    try:
        assert_safe_url(payload.video_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    suffix = Path(urlparse(payload.video_url).path).suffix.lower()
    if suffix and suffix not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="unsupported video URL file type")

    settings = request.app.state.runner.settings
    safe_task_id = _safe_task_id(payload.task_id or _source_stem(payload.video_url))
    run_input_id = uuid4().hex
    input_dir = settings.data_dir / "url-runs" / run_input_id
    input_dir.mkdir(parents=True, exist_ok=True)
    task_path = input_dir / "tasks.json"
    task = _track2_task(
        task_id=safe_task_id,
        video_url=payload.video_url,
        description=payload.description.strip(),
        source_label=payload.video_url,
    )
    task_path.write_text(json.dumps([task], indent=2), encoding="utf-8")
    run_id = request.app.state.runner.start_run(task_path)
    return {
        "run_id": run_id,
        "status": "queued",
        "task_id": safe_task_id,
        "input_path": str(task_path),
    }


@router.post("/runs/upload")
async def create_upload_run(
    request: Request,
    video: Annotated[UploadFile, File()],
    task_id: Annotated[str, Form()] = "uploaded-video",
    description: Annotated[str, Form()] = "",
) -> dict[str, object]:
    filename = video.filename or "video.mp4"
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="unsupported video file type")

    settings = request.app.state.runner.settings
    upload_id = uuid4().hex
    safe_task_id = _safe_task_id(task_id)
    upload_dir = settings.data_dir / "uploads" / upload_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    video_path = upload_dir / f"{safe_task_id}{suffix}"
    max_bytes = settings.max_download_mb * 1024 * 1024
    written = 0
    with video_path.open("wb") as output:
        while chunk := await video.read(1024 * 1024):
            written += len(chunk)
            if written > max_bytes:
                output.close()
                video_path.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="uploaded video is too large")
            output.write(chunk)

    task_path = upload_dir / "tasks.json"
    task = _track2_task(
        task_id=safe_task_id,
        video_url=video_path.resolve().as_uri(),
        description=description.strip(),
        source_label=filename,
    )
    task_path.write_text(json.dumps([task], indent=2), encoding="utf-8")
    run_id = request.app.state.runner.start_run(task_path)
    return {
        "run_id": run_id,
        "status": "queued",
        "task_id": safe_task_id,
        "input_path": str(task_path),
    }


@router.get("/runs")
def list_runs(request: Request) -> list[dict[str, object]]:
    return request.app.state.runner.list_runs()


@router.get("/runs/{run_id}")
def get_run(run_id: str, request: Request) -> dict[str, object]:
    return request.app.state.runner.get_run(run_id)


@router.get("/runs/{run_id}/events")
def events(run_id: str) -> list[dict[str, object]]:
    return [{"run_id": run_id, "stage": "mock", "status": "available"}]


@router.post("/runs/{run_id}/cancel")
def cancel(run_id: str, request: Request) -> dict[str, object]:
    request.app.state.runner.cancel(run_id)
    return {"run_id": run_id, "status": "cancel_requested"}


def resolve_input_path(input_path: str) -> Path:
    path = Path(input_path)
    if path.is_absolute():
        return path
    for base in (Path.cwd(), API_ROOT, REPO_ROOT):
        candidate = base / path
        if candidate.exists():
            return candidate
    return path


def _safe_task_id(task_id: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", task_id.strip()).strip("-").lower()
    return cleaned[:48] or "uploaded-video"


def _track2_task(
    *,
    task_id: str,
    video_url: str,
    description: str,
    source_label: str,
) -> dict[str, object]:
    return {
        "task_id": task_id,
        "video_url": video_url,
        "styles": TRACK2_STYLES,
        "description": description,
        "source_label": source_label,
        "created_at": datetime.now(UTC).isoformat(),
    }


def _source_stem(source: str) -> str:
    path = urlparse(source).path if "://" in source else source
    stem = Path(path).stem
    return stem or "video"
