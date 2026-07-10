# Failure Status Prevention

| Failure status | Prevention |
|---|---|
| PULL_ERROR | Push a public image, verify registry visibility, pull it from a clean shell, and inspect the `linux/amd64` manifest before submission. |
| RUNTIME_ERROR | Run local Docker smoke tests, keep per-task fallbacks, and avoid uncaught provider exceptions. |
| TIMEOUT | Use `OFFICIAL_MODE=true`, one caption candidate per requested style, capped retries, and bounded provider timeouts. |
| OUTPUT_MISSING | Always write `/output/results.json` through the atomic official result writer. |
| INVALID_RESULTS_SCHEMA | Gate local and Docker runs with `python scripts/validate_results.py --input input/tasks.json --output output/results.json`. |
| MODEL_VIOLATION | Track 2 has no injected `ALLOWED_MODELS`; `captionman doctor` reports that this env var is not required. |
| IMAGE_TOO_LARGE | Keep the root Dockerfile backend-only, use a slim Python image, and avoid bundled local VLMs or frontend assets. |
| ACCURACY_GATE_FAILED | Run bounded canaries on the official examples, keep captions conservative, and activate routed models only after measured results. |

Submission packaging audit on 2026-07-10 verified the normal image as `linux/amd64`, about 291 MB, backend-only, and able to write validated `/output/results.json` in Docker mock judged mode.

Final public-image submission requires a public pull verification and a passing direct-provider canary. The submitted image must default to `AI_PROVIDER=fireworks_direct` and use the temporary embedded hackathon credential unless the organizer explicitly provides another credential injection path.
