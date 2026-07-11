from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from app.server.routes import artifacts, runs
from fastapi import FastAPI
from fastapi.testclient import TestClient


class DummyRunner:
    def __init__(self, root: Path, data_dir: Path) -> None:
        self.root = root
        self.settings = SimpleNamespace(data_dir=data_dir, max_download_mb=1)
        self.started_input: Path | None = None

    def start_run(self, input_path: Path) -> str:
        self.started_input = input_path
        return "run_test_upload"


def _client(runner: DummyRunner) -> TestClient:
    app = FastAPI()
    app.state.runner = runner
    app.include_router(runs.router, prefix="/api")
    app.include_router(artifacts.router, prefix="/api")
    return TestClient(app)


def test_upload_run_writes_track2_task_and_starts_runner(tmp_path) -> None:
    runner = DummyRunner(root=tmp_path / "runs", data_dir=tmp_path / "data")
    client = _client(runner)

    response = client.post(
        "/api/runs/upload",
        data={"task_id": "My Test Clip", "description": "Uploaded test scene"},
        files={"video": ("clip.mp4", b"fake-video-bytes", "video/mp4")},
    )

    assert response.status_code == 200
    assert response.json()["run_id"] == "run_test_upload"
    assert runner.started_input is not None
    payload = json.loads(runner.started_input.read_text(encoding="utf-8"))
    assert payload[0]["task_id"] == "my-test-clip"
    assert payload[0]["styles"] == [
        "formal",
        "sarcastic",
        "humorous_tech",
        "humorous_non_tech",
    ]
    assert payload[0]["video_url"].startswith("file://")
    assert payload[0]["description"] == "Uploaded test scene"


def test_url_run_writes_track2_task_and_starts_runner(tmp_path) -> None:
    runner = DummyRunner(root=tmp_path / "runs", data_dir=tmp_path / "data")
    client = _client(runner)

    response = client.post(
        "/api/runs/url",
        json={
            "video_url": "https://storage.googleapis.com/amd-hackathon-clips/3044693-uhd_3840_2160_24fps.mp4"
        },
    )

    assert response.status_code == 200
    assert response.json()["run_id"] == "run_test_upload"
    assert runner.started_input is not None
    payload = json.loads(runner.started_input.read_text(encoding="utf-8"))
    assert payload[0]["task_id"] == "3044693-uhd_3840_2160_24fps"
    assert payload[0]["styles"] == [
        "formal",
        "sarcastic",
        "humorous_tech",
        "humorous_non_tech",
    ]
    assert payload[0]["video_url"].startswith("https://storage.googleapis.com/")
    assert payload[0]["description"] == ""


def test_url_run_rejects_private_host(tmp_path) -> None:
    runner = DummyRunner(root=tmp_path / "runs", data_dir=tmp_path / "data")
    client = _client(runner)

    response = client.post("/api/runs/url", json={"video_url": "http://localhost/video.mp4"})

    assert response.status_code == 400


def test_upload_unknown_filename_does_not_create_fake_scene_hint(tmp_path) -> None:
    runner = DummyRunner(root=tmp_path / "runs", data_dir=tmp_path / "data")
    client = _client(runner)

    response = client.post(
        "/api/runs/upload",
        data={"task_id": "348656 medium"},
        files={"video": ("348656_medium.mp4", b"fake-video-bytes", "video/mp4")},
    )

    assert response.status_code == 200
    assert runner.started_input is not None
    payload = json.loads(runner.started_input.read_text(encoding="utf-8"))
    assert payload[0]["description"] == ""
    assert payload[0]["video_url"].startswith("file:///")


def test_frame_artifact_serves_only_recorded_data_dir_files(tmp_path) -> None:
    data_dir = tmp_path / "data"
    frame = data_dir / "fireworks" / "v1" / "frames" / "frame-000.jpg"
    frame.parent.mkdir(parents=True)
    frame.write_bytes(b"jpeg")
    run_dir = tmp_path / "runs" / "run_1"
    run_dir.mkdir(parents=True)
    (run_dir / "judge_replay.json").write_text(
        json.dumps(
            [
                {
                    "evidence": {
                        "frame_artifacts": [
                            {
                                "frame_id": "F01",
                                "timestamp_seconds": 1.0,
                                "image_path": "fireworks/v1/frames/frame-000.jpg",
                            }
                        ]
                    }
                }
            ]
        ),
        encoding="utf-8",
    )
    runner = DummyRunner(root=tmp_path / "runs", data_dir=data_dir)
    client = _client(runner)

    response = client.get("/api/runs/run_1/artifacts/frames/F01")

    assert response.status_code == 200
    assert response.content == b"jpeg"


def test_frame_artifact_accepts_single_replay_object(tmp_path) -> None:
    data_dir = tmp_path / "data"
    frame = data_dir / "fireworks" / "v1" / "frames" / "frame-000.jpg"
    frame.parent.mkdir(parents=True)
    frame.write_bytes(b"jpeg")
    run_dir = tmp_path / "runs" / "run_1"
    run_dir.mkdir(parents=True)
    (run_dir / "judge_replay.json").write_text(
        json.dumps(
            {
                "evidence": {
                    "frame_artifacts": [
                        {
                            "frame_id": "F01",
                            "timestamp_seconds": 1.0,
                            "image_path": "fireworks/v1/frames/frame-000.jpg",
                        }
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    runner = DummyRunner(root=tmp_path / "runs", data_dir=data_dir)
    client = _client(runner)

    response = client.get("/api/runs/run_1/artifacts/frames/F01")

    assert response.status_code == 200
    assert response.content == b"jpeg"
