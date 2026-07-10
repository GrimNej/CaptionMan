from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
        newline="\n",
    ) as handle:
        handle.write(text)
        temp_name = handle.name
    last_error: PermissionError | None = None
    for _ in range(8):
        try:
            os.replace(temp_name, path)
            return
        except PermissionError as exc:
            last_error = exc
            time.sleep(0.05)
    try:
        Path(temp_name).unlink(missing_ok=True)
    finally:
        if last_error is not None:
            raise last_error


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
