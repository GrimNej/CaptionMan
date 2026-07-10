from __future__ import annotations

from app.io.schema_lock import write_schema_lock_report


def test_schema_lock_report_has_required_sections(tmp_path) -> None:
    path = tmp_path / "SPEC_LOCK.md"
    write_schema_lock_report(path)
    text = path.read_text(encoding="utf-8")
    assert "# Official Schema Lock" in text
    assert "## Adapter mapping" in text
    assert "`schema_adapter.py` implemented: yes" in text
