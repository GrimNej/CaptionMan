from __future__ import annotations

from app.video.frame_sampler import uniform_timestamps


def test_uniform_timestamps_cover_beginning_and_end() -> None:
    timestamps = uniform_timestamps(120, 12)

    assert len(timestamps) == 12
    assert timestamps[0] == 0.5
    assert timestamps[-1] == 119.5
    assert timestamps == sorted(timestamps)


def test_uniform_timestamps_handles_single_and_empty_requests() -> None:
    assert uniform_timestamps(20, 1) == [10]
    assert uniform_timestamps(20, 0) == []
