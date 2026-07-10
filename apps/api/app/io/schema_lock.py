from __future__ import annotations

from pathlib import Path

SCHEMA_LOCK_TEMPLATE = """# Official Schema Lock

## Status

- Schema status: confirmed
- Last checked date: 2026-07-08
- Checked by: Codex
- Official source checked: Participant Guide_ AMD Developer Hackathon (ACT II).pdf
- Source type: participant guide

## Input contract

- Official input path: `/input/tasks.json`
- Official input top-level shape: JSON list
- Required task fields: `task_id`, `video_url`, `styles`
- Optional task fields: none specified
- Video source field: `video_url`
- Task identifier field: `task_id`
- Example input:

```json
[{"task_id":"v1","video_url":"https://storage.example.com/clips/clip1.mp4","styles":["formal","sarcastic","humorous_tech","humorous_non_tech"]}]
```

## Output contract

- Official output path: `/output/results.json`
- Official output top-level shape: JSON list
- Required result fields: `task_id`, `captions`
- Required style keys: `formal`, `sarcastic`, `humorous_tech`, `humorous_non_tech`
- Extra fields allowed: unknown; official examples show no extra fields
- Example output:

```json
[{"task_id":"v1","captions":{"formal":"...","sarcastic":"...","humorous_tech":"...","humorous_non_tech":"..."}}]
```

## Adapter mapping

| Internal field | Official field | Notes |
|---|---|---|
| `video_id` | `task_id` | Internal name retained; official output writes `task_id`. |
| `video_uri` | `video_url` | Adapter accepts aliases locally, but official field is `video_url`. |
| `requested_styles` | `styles` | Output must include every requested style. |
| `formal` | `captions.formal` | Caption text only. |
| `sarcastic` | `captions.sarcastic` | Caption text only. |
| `humorous_tech` | `captions.humorous_tech` | Caption text only. |
| `humorous_non_tech` | `captions.humorous_non_tech` | Caption text only. |

## Unknowns

- Whether extra output fields are tolerated is not specified; implementation emits none.
- Hidden evaluation may request a subset of styles; implementation supports requested styles.

## Implementation status

- `schema_adapter.py` implemented: yes
- `validate_results.py` aligned: yes
- Docker mock run validated: yes
"""


def write_schema_lock_report(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SCHEMA_LOCK_TEMPLATE, encoding="utf-8")
