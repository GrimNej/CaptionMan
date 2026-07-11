from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "apps" / "api"

ROUTE_ENVS: dict[str, dict[str, str]] = {
    "mock_baseline": {
        "AI_PROVIDER": "mock",
        "OFFICIAL_MODE": "true",
        "MODEL_ROUTING_MODE": "mock",
        "CHAMPION_ROUTE": "mock_baseline",
        "GEMMA_USAGE_MODE": "off",
    },
    "fireworks_kimi_glm": {
        "AI_PROVIDER": "fireworks_direct",
        "OFFICIAL_MODE": "true",
        "MODEL_ROUTING_MODE": "champion",
        "CHAMPION_ROUTE": "fireworks_kimi_glm",
        "GEMMA_USAGE_MODE": "off",
    },
    "fireworks_qwen37_glm": {
        "AI_PROVIDER": "fireworks_direct",
        "OFFICIAL_MODE": "true",
        "MODEL_ROUTING_MODE": "champion",
        "CHAMPION_ROUTE": "fireworks_qwen37_glm",
        "VISION_MODEL": "accounts/fireworks/models/qwen3p7-plus",
        "VISION_FALLBACK_MODEL": "accounts/fireworks/models/kimi-k2p7-code",
        "GEMMA_USAGE_MODE": "off",
    },
    "specialist_vision_gemma_style": {
        "AI_PROVIDER": "fireworks_direct",
        "OFFICIAL_MODE": "true",
        "MODEL_ROUTING_MODE": "champion",
        "CHAMPION_ROUTE": "specialist_vision_gemma_style",
        "GEMMA_USAGE_MODE": "specialist",
    },
    "proxy_champion": {
        "AI_PROVIDER": "proxy",
        "OFFICIAL_MODE": "true",
        "MODEL_ROUTING_MODE": "champion",
        "CHAMPION_ROUTE": "proxy_champion",
        "PROXY_CAPTION_PATH": "/captionman/infer",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a bounded CaptionMan route tournament."
    )
    parser.add_argument("--input", default="input/tasks.json")
    parser.add_argument("--output-root", default=".data/tournament")
    parser.add_argument(
        "--routes",
        nargs="+",
        default=["mock_baseline"],
        choices=sorted(ROUTE_ENVS),
        help="Routes to run. Real-provider routes may spend credits.",
    )
    parser.add_argument(
        "--skip-doctor",
        action="store_true",
        help="Skip per-route doctor checks before running.",
    )
    args = parser.parse_args()

    input_path = (ROOT / args.input).resolve()
    output_root = (ROOT / args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    report: list[dict[str, Any]] = []

    for route in args.routes:
        report.append(
            _run_route(route, input_path, output_root, skip_doctor=args.skip_doctor)
        )

    report_path = output_root / "tournament_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"wrote {report_path}")
    failed = [item for item in report if item["status"] != "passed"]
    return 1 if failed else 0


def _run_route(
    route: str,
    input_path: Path,
    output_root: Path,
    skip_doctor: bool,
) -> dict[str, Any]:
    route_dir = output_root / route
    route_dir.mkdir(parents=True, exist_ok=True)
    output_path = route_dir / "results.json"
    env = os.environ.copy()
    env.update(ROUTE_ENVS[route])
    started = time.monotonic()
    item: dict[str, Any] = {"route": route, "status": "started"}

    if not skip_doctor:
        doctor = _run(["uv", "run", "captionman", "doctor"], cwd=API_DIR, env=env)
        item["doctor_exit_code"] = doctor.returncode
        if doctor.returncode != 0:
            item["status"] = "doctor_failed"
            item["stderr"] = doctor.stderr[-800:]
            return item

    run = _run(
        [
            "uv",
            "run",
            "captionman",
            "run",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        cwd=API_DIR,
        env=env,
    )
    item["run_exit_code"] = run.returncode
    if run.returncode != 0:
        item["status"] = "run_failed"
        item["stderr"] = run.stderr[-800:]
        return item

    validate = _run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_results.py"),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        cwd=ROOT,
        env=env,
    )
    item["validate_exit_code"] = validate.returncode
    item["elapsed_seconds"] = round(time.monotonic() - started, 3)
    item["output"] = str(output_path.relative_to(ROOT))
    item["status"] = "passed" if validate.returncode == 0 else "validation_failed"
    if validate.returncode != 0:
        item["stderr"] = validate.stderr[-800:]
    return item


def _run(
    command: list[str],
    cwd: Path,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


if __name__ == "__main__":
    raise SystemExit(main())
