from __future__ import annotations

import json
from pathlib import Path

from app.io.official_schema import VideoTask
from app.io.schema_adapter import adapt_input
from app.utils.atomic_write import atomic_write_json


def load_tasks(path: Path) -> list[VideoTask]:
    return adapt_input(json.loads(path.read_text(encoding="utf-8-sig")))


def write_demo_fixture(path: Path) -> None:
    atomic_write_json(
        path,
        [
            {
                "task_id": "demo-001",
                "video_url": "mock://captionman/demo-001",
                "styles": ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"],
                "metadata": {
                    "description": "A short clip with a visible subject and simple action"
                },
            }
        ],
    )
