from __future__ import annotations

import json

from app.utils.atomic_write import atomic_write_json


def test_atomic_write_json(tmp_path) -> None:
    path = tmp_path / "nested" / "data.json"
    atomic_write_json(path, {"ok": True})
    assert json.loads(path.read_text(encoding="utf-8")) == {"ok": True}
