# Official Schema Lock

## Status

- Schema status: confirmed
- Last checked date: 2026-07-11
- Checked by: Codex
- Official source checked: Participant Guide_ AMD Developer Hackathon (ACT II).pdf, plus organizer/maintainer clarification relayed by the user
- Source type: participant guide plus maintainer clarification

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
- Required style keys: every style requested by the corresponding input task
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
- Hidden evaluation may request a subset of styles; implementation validates against requested styles when input context is provided.

## Judging constraints rechecked on 2026-07-10

- Track 2 is Video Captioning.
- Expected output remains captions for requested styles, including `formal`, `sarcastic`, `humorous_tech`, and `humorous_non_tech` for the provided sample tasks.
- The submitted artifact is a publicly pullable Docker image.
- The image must support `linux/amd64`.
- The container must read `/input/tasks.json` on startup and write `/output/results.json` before exiting.
- Track 2 requires no inference log.
- Track 2 does not inject `FIREWORKS_API_KEY`, `FIREWORKS_BASE_URL`, or `ALLOWED_MODELS`; the final image must use CaptionMan's own temporary hackathon credential.
- Hidden clips are 30 seconds to 2 minutes and evaluation uses unseen video content.
- Scoring is based on caption accuracy and style match across clips and requested styles.
- The final score is a weighted average across roughly 12 hidden clips spanning nature, urban, animals, people, sports, food, weather, and technology.
- General rules prohibit hardcoding or caching answers for specific inputs.
- Missing requested styles score zero for that clip.
- Runtime limit is 10 minutes.
- Compressed image size must be under 10 GB.
- Live scoreboard failure modes to avoid include pull errors, runtime crashes, timeouts, invalid result schema, and missing output.

## Implementation status

- `schema_adapter.py` implemented: yes
- `validate_results.py` aligned: yes
- Input adapter infers scene content from task IDs, filenames, or URLs: no
- Judged visual evidence: 10-14 timestamped images across the full video
- Caption generation: one shared requested-style JSON batch plus targeted per-style recovery
- Final caption boundary: meaningful evidence-anchor overlap is required; unseen technical concepts must be explicitly figurative
- Hosted demo quality profile matches judged frame and recovery bounds: yes, verified by a 10-frame/four-call public replay; all frame URLs use the public origin
- Docker mock run validated: yes, from the anonymously pulled final image on 2026-07-11
- Retired public-validation set status: all v1-v8 tasks and 32 styles validated in 199.8 seconds
- Docker real v1-v8 run validated: yes, from exact final image digest `sha256:756a80fa9de66565476b4b50d4b5624e21dc3857483990329f55718e9105fe11`
