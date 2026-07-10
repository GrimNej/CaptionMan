from __future__ import annotations

import json
import subprocess
import threading
from pathlib import Path

from app.core.config import Settings
from app.core.pipeline import run_pipeline
from app.io.result_writer import write_official_results
from app.io.task_loader import load_tasks
from app.utils.atomic_write import atomic_write_json
from app.utils.ids import new_run_id


class LocalJobRunner:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.root = settings.data_dir / "runs"
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def recover_stale_runs(self) -> None:
        for status_path in self.root.glob("*/status.json"):
            status = json.loads(status_path.read_text(encoding="utf-8-sig"))
            if status.get("status") == "running":
                status["status"] = "interrupted"
                atomic_write_json(status_path, status)

    def start_run(self, input_path: Path) -> str:
        run_id = new_run_id()
        run_dir = self.root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        atomic_write_json(run_dir / "status.json", {"run_id": run_id, "status": "queued"})
        thread = threading.Thread(target=self._run, args=(run_id, input_path), daemon=True)
        thread.start()
        return run_id

    def cancel(self, run_id: str) -> None:
        atomic_write_json(self.root / run_id / "cancel.json", {"cancel": True})

    def _run(self, run_id: str, input_path: Path) -> None:
        with self._lock:
            run_dir = self.root / run_id
            status_path = run_dir / "status.json"
            if (run_dir / "cancel.json").exists():
                atomic_write_json(status_path, {"run_id": run_id, "status": "cancelled"})
                return
            atomic_write_json(status_path, {"run_id": run_id, "status": "running"})
            try:
                tasks = load_tasks(input_path)
                results, replay = run_pipeline(tasks, self.settings)
                write_official_results(results, run_dir / "results.json")
                atomic_write_json(run_dir / "judge_replay.json", replay)
                atomic_write_json(status_path, {"run_id": run_id, "status": "complete"})
            except Exception as exc:  # noqa: BLE001
                message = _safe_error_message(exc)
                atomic_write_json(
                    status_path,
                    {
                        "run_id": run_id,
                        "status": "failed",
                        "error": type(exc).__name__,
                        "message": message,
                    },
                )

    def list_runs(self) -> list[dict[str, object]]:
        return [self.get_run(path.parent.name) for path in self.root.glob("*/status.json")]

    def get_run(self, run_id: str) -> dict[str, object]:
        path = self.root / run_id / "status.json"
        if not path.exists():
            return {"run_id": run_id, "status": "missing"}
        return json.loads(path.read_text(encoding="utf-8-sig"))


def _safe_error_message(exc: Exception) -> str:
    if isinstance(exc, subprocess.CalledProcessError):
        stderr = (exc.stderr or "").strip().splitlines()
        stdout = (exc.stdout or "").strip().splitlines()
        detail = stderr[-1] if stderr else stdout[-1] if stdout else str(exc)
        return detail[:300]
    return str(exc)[:300] or type(exc).__name__
