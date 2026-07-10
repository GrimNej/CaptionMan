from __future__ import annotations

from pathlib import Path

from app.server.routes import runs


def test_resolve_input_path_accepts_absolute_path(tmp_path) -> None:
    input_file = tmp_path / "tasks.json"
    input_file.write_text("[]", encoding="utf-8")

    assert runs.resolve_input_path(str(input_file)) == input_file


def test_resolve_input_path_finds_repo_relative_sample(monkeypatch, tmp_path) -> None:
    sample = tmp_path / ".data" / "samples" / "track2" / "tasks.local.json"
    sample.parent.mkdir(parents=True)
    sample.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(runs, "REPO_ROOT", tmp_path)
    workdir = tmp_path / "workdir"
    workdir.mkdir()
    monkeypatch.chdir(workdir)

    assert runs.resolve_input_path(".data/samples/track2/tasks.local.json") == sample


def test_resolve_input_path_preserves_missing_relative_path(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(runs, "API_ROOT", tmp_path / "api")
    monkeypatch.setattr(runs, "REPO_ROOT", tmp_path / "repo")
    monkeypatch.chdir(tmp_path)

    assert runs.resolve_input_path("input/tasks.json") == Path("input/tasks.json")
