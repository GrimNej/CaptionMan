from __future__ import annotations

import pytest
from app.io.official_schema import InternalResult
from app.io.result_validator import OfficialResultValidationError
from app.io.result_writer import write_official_results


def test_result_writer_rejects_invalid_official_caption(tmp_path) -> None:
    result = InternalResult(
        video_id="v1",
        formal="x" * 501,
        sarcastic="Short caption.",
        humorous_tech="Short caption.",
        humorous_non_tech="Short caption.",
    )
    output = tmp_path / "results.json"

    with pytest.raises(OfficialResultValidationError):
        write_official_results([result], output)

    assert not output.exists()


def test_result_writer_accepts_requested_style_subset(tmp_path) -> None:
    result = InternalResult(
        video_id="v1",
        formal="A clear video scene is shown.",
        sarcastic="",
        humorous_tech="",
        humorous_non_tech="",
        requested_styles=["formal"],
    )
    output = tmp_path / "results.json"

    write_official_results([result], output)

    assert '"formal"' in output.read_text(encoding="utf-8")
    assert '"sarcastic"' not in output.read_text(encoding="utf-8")
