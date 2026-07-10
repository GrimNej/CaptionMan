from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

router = APIRouter()


def _artifact(request: Request, run_id: str, filename: str) -> object:
    path = request.app.state.runner.root / run_id / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="artifact not found")
    return json.loads(path.read_text(encoding="utf-8-sig"))


@router.get("/runs/{run_id}/artifacts/evidence")
def evidence(run_id: str, request: Request) -> object:
    replay = _artifact(request, run_id, "judge_replay.json")
    items = _replay_items(replay)
    return items[0]["evidence"] if items else {}


@router.get("/runs/{run_id}/artifacts/judge-replay")
def judge_replay(run_id: str, request: Request) -> object:
    return _artifact(request, run_id, "judge_replay.json")


@router.get("/runs/{run_id}/artifacts/results")
def results(run_id: str, request: Request) -> object:
    return _artifact(request, run_id, "results.json")


@router.get("/runs/{run_id}/artifacts/frames/{frame_id}")
def frame_image(run_id: str, frame_id: str, request: Request) -> FileResponse:
    replay = _artifact(request, run_id, "judge_replay.json")
    for item in _replay_items(replay):
        evidence_payload = item.get("evidence")
        if not isinstance(evidence_payload, dict):
            continue
        for frame in evidence_payload.get("frame_artifacts", []):
            if not isinstance(frame, dict) or frame.get("frame_id") != frame_id:
                continue
            image_path = frame.get("image_path")
            if not isinstance(image_path, str):
                raise HTTPException(status_code=404, detail="frame not found")
            resolved = _resolve_data_file(request.app.state.runner.settings.data_dir, image_path)
            if not resolved.exists():
                raise HTTPException(status_code=404, detail="frame file not found")
            return FileResponse(resolved, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="frame not found")


def _replay_items(replay: object) -> list[dict[str, object]]:
    if isinstance(replay, dict):
        return [replay]
    if isinstance(replay, list):
        return [item for item in replay if isinstance(item, dict)]
    return []


def _resolve_data_file(data_dir: Path, image_path: str) -> Path:
    candidate = Path(image_path)
    resolved = candidate.resolve() if candidate.is_absolute() else (data_dir / candidate).resolve()
    data_root = data_dir.resolve()
    if data_root != resolved and data_root not in resolved.parents:
        raise HTTPException(status_code=403, detail="frame path outside data directory")
    return resolved
