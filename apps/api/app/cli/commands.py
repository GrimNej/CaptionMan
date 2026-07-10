from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from app.core.config import Settings
from app.core.pipeline import run_pipeline
from app.io.result_writer import write_official_results
from app.io.schema_lock import write_schema_lock_report
from app.io.task_loader import load_tasks, write_demo_fixture
from app.providers.model_registry import doctor_report
from app.video.probe import probe_video

app = typer.Typer(help="CaptionMan judged runner and demo utilities.")
console = Console()


@app.command()
def run(
    input: Annotated[Path, typer.Option("--input", exists=True, readable=True)],
    output: Annotated[Path, typer.Option("--output")],
    debug_dir: Annotated[Path | None, typer.Option("--debug-dir")] = None,
) -> None:
    """Run the schema-safe captioning pipeline and write official results."""
    settings = Settings()
    tasks = load_tasks(input)
    results, replay = run_pipeline(tasks=tasks, settings=settings)
    write_official_results(results, output)
    if debug_dir:
        debug_dir.mkdir(parents=True, exist_ok=True)
        (debug_dir / "judge_replay.json").write_text(
            json.dumps(replay, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    console.print(f"[green]wrote[/green] {output}")


@app.command()
def doctor() -> None:
    """Check local environment and configured provider readiness."""
    report = doctor_report(Settings())
    console.print_json(json.dumps(report, indent=2))
    if not report["ok"]:
        raise typer.Exit(1)


@app.command("demo-fixture")
def demo_fixture(output: Annotated[Path, typer.Option("--output")]) -> None:
    """Write a deterministic mock input fixture."""
    write_demo_fixture(output)
    console.print(f"[green]wrote[/green] {output}")


@app.command("inspect-video")
def inspect_video(path: Annotated[Path, typer.Argument(exists=True, readable=True)]) -> None:
    """Probe a local video with ffprobe."""
    console.print_json(json.dumps(probe_video(path).model_dump(), indent=2))


@app.command("schema-lock")
def schema_lock(
    output: Annotated[Path, typer.Option("--output")] = Path("../../docs/SPEC_LOCK.md"),
) -> None:
    """Generate the adapter-based schema lock report."""
    write_schema_lock_report(output)
    console.print(f"[green]wrote[/green] {output}")


@app.command("run-one")
def run_one(
    video: Annotated[str, typer.Argument()],
    out: Annotated[Path, typer.Option("--out")],
) -> None:
    """Run one video into a local artifact directory."""
    settings = Settings()
    task_path = out / "task.json"
    out.mkdir(parents=True, exist_ok=True)
    task_path.write_text(
        json.dumps({"tasks": [{"video_id": "manual-001", "video": video}]}, indent=2),
        encoding="utf-8",
    )
    tasks = load_tasks(task_path)
    results, replay = run_pipeline(tasks=tasks, settings=settings)
    write_official_results(results, out / "results.json")
    (out / "judge_replay.json").write_text(json.dumps(replay, indent=2), encoding="utf-8")
    console.print(f"[green]wrote[/green] {out}")
