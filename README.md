# CaptionMan

Captions With Receipts

CaptionMan is an evidence-grounded video captioning system for AMD Developer Hackathon ACT II Track 2. It creates requested caption styles by building a structured evidence file, generating candidate captions, auditing them with deterministic and model-based checks, repairing weak candidates, and exporting schema-ready results.

## What CaptionMan Does

CaptionMan runs as a CLI-first judged runner and as a separate demo product surface. The judged runner reads `/input/tasks.json`, adapts the top-level task array through a schema boundary, builds safe evidence, produces every requested style, validates the output, and writes `/output/results.json` atomically.

## Why It Is Different

The pipeline is judge-aware: captions are generated from evidence, checked against hard rules, scored for tone and hallucination risk, and repaired when needed. The implementation avoids debug leakage in official output and keeps all provider calls behind budget guards.

## Track Alignment

CaptionMan supports:

- `formal`
- `sarcastic`
- `humorous_tech`
- `humorous_non_tech`

The adapter layer keeps the internal model separate from the official Track 2 schema:

```json
[
  {
    "task_id": "v1",
    "captions": {
      "formal": "...",
      "sarcastic": "...",
      "humorous_tech": "...",
      "humorous_non_tech": "..."
    }
  }
]
```

Track 2 does not require an inference log, does not inject API credentials, and does not require `ALLOWED_MODELS`. The submitted artifact is a publicly pullable Docker image that supports `linux/amd64` and can run with CaptionMan's own temporary hackathon API credentials.

## Architecture

- `apps/api`: Python CLI, FastAPI demo API, providers, video tools, evidence, Caption Court, and tests.
- `apps/web`: Next.js App Router demo UI.
- `prompts`: Model-facing prompt files with prompt-injection guardrails.
- `scripts`: Result validation, source hygiene, and secret scans.
- `docs`: Schema lock, architecture, security, and living handoff documents.

## Quickstart With Mock Provider

```bash
cd apps/api
uv sync
uv run captionman demo-fixture --output ../../input/tasks.json
AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json
cd ../..
python scripts/validate_results.py output/results.json
python scripts/validate_results.py --input input/tasks.json --output output/results.json
```

## Quickstart With Fireworks Provider

```bash
cp .env.example .env
# Set FIREWORKS_API_KEY, VISION_MODEL, TEXT_MODEL, and JUDGE_MODEL.
cd apps/api
AI_PROVIDER=fireworks uv run captionman doctor
```

Fireworks support is conditional on `captionman doctor` verifying API access and configured models.

CaptionMan supports multiple provider routes for Track 2 evaluation. During development, it can use local environment credentials. For final packaging, the selected route is a temporary limited hackathon credential through `AI_PROVIDER=fireworks_direct`; proxy support remains optional. Details live in `docs/CREDENTIAL_STRATEGY.md`.

## Docker Judged Mode

```bash
docker build -t captionman .
docker run --rm captionman captionman doctor
docker run --rm -e AI_PROVIDER=mock -v "$PWD/input:/input" -v "$PWD/output:/output" captionman
python scripts/validate_results.py output/results.json
python scripts/validate_results.py --input input/tasks.json --output output/results.json
```

The judged Dockerfile does not build or depend on the frontend.

## Final Public Image

Normal development images stay key-free and default to `AI_PROVIDER=mock`. The final submitted image is built only after green gates and explicit approval, with the temporary hackathon-only Fireworks key injected through a BuildKit secret:

```bash
docker buildx build \
  --platform linux/amd64 \
  --no-cache \
  --build-arg ALLOW_EMBEDDED_HACKATHON_KEY=true \
  --build-arg RUNTIME_AI_PROVIDER=fireworks_direct \
  --build-arg RUNTIME_OFFICIAL_MODE=true \
  --secret id=fireworks_api_key,src=.data/final-secrets/fireworks_api_key.txt \
  -t <public-registry>/<namespace>/captionman:<tag> \
  --push .
```

Before submitting the image URL, verify it from a clean pull:

```bash
docker pull --platform linux/amd64 <public-registry>/<namespace>/captionman:<tag>
docker run --rm <public-registry>/<namespace>/captionman:<tag> captionman doctor
```

The embedded-key image is temporary and must be revoked or rotated after judging.

## Demo Frontend

On Windows, use the checked-in launcher for final review/demo testing. It starts the FastAPI API and the built Next.js app, sets the real-provider demo environment without shell quoting, verifies `/api/health`, verifies `/api/doctor`, waits for `/studio`, and then prints the exact URLs and process IDs.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\launch_demo.ps1 -Restart
```

The UI includes a landing page, Run Studio, no-credit Judge Replay, real sample runs, uploaded-video runs, and real sampled-frame replay when backend artifacts are available. It is a demo/product surface and does not affect judged CLI output.

## Model Routing And Gemma

CaptionMan uses routed model configuration rather than assuming one model should do every job. `captionman doctor` reports the selected route, credential source, visual model, caption model, repair model, proxy status, and Gemma status.

Gemma is treated as a specialist for style control and repair when configured and measured. The project does not claim Gemma multimodal or Gemma-only behavior unless `captionman doctor` and the tournament docs verify that route.

## Environment Variables

See `.env.example` for provider, pipeline, download, API, and frontend variables.

## Schema Lock Note

The Track 2 schema is confirmed from the participant guide. Run:

```bash
cd apps/api
uv run captionman schema-lock
```

## Security

CaptionMan blocks obvious unsafe download targets, avoids logging secrets and signed URLs, redacts sensitive fields, and keeps debug artifacts out of official results.

## Testing

```bash
cd apps/api
uv run pytest
uv run ruff check .
cd ../..
python scripts/check_source_hygiene.py
python scripts/check_no_secrets.py
```

## Submission Checklist

Before submission, run the final green-flag gates in `docs/SUBMISSION_CHECKLIST.md` and update `docs/TEST_REPORT.md`.
