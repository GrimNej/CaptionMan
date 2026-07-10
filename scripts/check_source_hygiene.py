from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_TARGETS = ("README.md", "docs", "apps", "packages", "prompts")
EXCLUDED_PARTS = {
    ".git",
    ".next",
    "dist",
    "coverage",
    "node_modules",
    ".venv",
    ".data",
    "output",
    "docs/FORBIDDEN_TERMS.txt",
}
BASE_FORBIDDEN = {
    "guaranteed winner",
    "perfect captions",
    "zero hallucinations",
    "fully real-time",
    "pnpm@latest",
}


def _is_excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return (
        any(part in path.relative_to(ROOT).parts for part in EXCLUDED_PARTS)
        or rel in EXCLUDED_PARTS
    )


def _terms() -> set[str]:
    terms = set(BASE_FORBIDDEN)
    denylist = ROOT / "docs" / "FORBIDDEN_TERMS.txt"
    if denylist.exists():
        for line in denylist.read_text(encoding="utf-8").splitlines():
            term = line.strip()
            if term and not term.startswith("#"):
                terms.add(term.lower())
    return terms


def _files() -> list[Path]:
    files: list[Path] = []
    for target in SCAN_TARGETS:
        path = ROOT / target
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
    return [p for p in files if not _is_excluded(p)]


def main() -> int:
    failures: list[str] = []
    terms = _terms()
    for path in _files():
        try:
            text = path.read_text(encoding="utf-8").lower()
        except (FileNotFoundError, UnicodeDecodeError):
            continue
        for term in terms:
            if term in text:
                failures.append(f"{path.relative_to(ROOT)}: forbidden phrase '{term}'")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("source hygiene passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
