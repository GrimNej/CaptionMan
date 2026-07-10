from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRA_SOURCE_FILES = (
    "Dockerfile",
    ".dockerignore",
    ".env.example",
    "package.json",
    "pnpm-lock.yaml",
    "pnpm-workspace.yaml",
)
SCAN_DIRS = (
    "README.md",
    "AGENTS.md",
    *EXTRA_SOURCE_FILES,
    "docs",
    "apps",
    "packages",
    "prompts",
    "scripts",
    ".github",
)
EXCLUDED_PARTS = {".git", "node_modules", ".venv", ".data", "output", ".next"}
SAFE_PLACEHOLDERS = {
    "",
    "your_key_here",
    "your_proxy_token_here",
    "your_token_here",
    "changeme",
    "...",
    "<PROXY_TOKEN>",
}
SECRET_PATTERNS = {
    "generic api key assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|token|proxy_token|fireworks_api_key)[ \t]*=[ \t]*['\"]?([^'\"\s#]+)"
    ),
    "bearer token": re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-\.]{20,}"),
    "fireworks key": re.compile(r"fw_[A-Za-z0-9_\-]{20,}"),
    "openai-style key": re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    "authorization header": re.compile(
        r"(?i)\bauthorization\s*[:=]\s*bearer\s+[^'\"\s]+"
    ),
}


def iter_files(include_local_env: bool = False) -> list[Path]:
    files: list[Path] = []
    for item in SCAN_DIRS:
        path = ROOT / item
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
    if include_local_env:
        files.extend(path for path in ROOT.glob(".env*") if path.is_file())
    unique = list(dict.fromkeys(files))
    return [p for p in unique if EXCLUDED_PARTS.isdisjoint(p.relative_to(ROOT).parts)]


def _is_safe_assignment(pattern: re.Pattern[str], match: re.Match[str]) -> bool:
    if pattern is SECRET_PATTERNS["authorization header"]:
        return "<PROXY_TOKEN>" in match.group(
            0
        ) or "your_proxy_token_here" in match.group(0)
    if pattern is not SECRET_PATTERNS["generic api key assignment"]:
        return False
    value = match.group(2).strip().strip("'\"")
    return (
        value in SAFE_PLACEHOLDERS
        or value.startswith("your_")
        or value.startswith("settings.")
        or value.startswith("self.")
    )


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    include_local_env = "--include-local-env" in args
    failures: list[str] = []
    for path in iter_files(include_local_env=include_local_env):
        try:
            text = path.read_text(encoding="utf-8")
        except (FileNotFoundError, UnicodeDecodeError):
            continue
        for label, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(text):
                if _is_safe_assignment(pattern, match):
                    continue
                failures.append(f"{path.relative_to(ROOT)}: possible {label}")
                break
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("no secrets detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
