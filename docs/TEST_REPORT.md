# Test Report

## Test Entry Template

### YYYY-MM-DD HH:MM
- Command:
- Environment:
- Result: pass | fail
- Output summary:
- Failures:
- Fixes attempted:

### 2026-07-08 00:00
- Command: Pending local verification.
- Environment: Windows PowerShell, uv available, pnpm 11.7.0, Docker available.
- Result: fail
- Output summary: Checks have not run yet.
- Failures: Not applicable.
- Fixes attempted: Not applicable.

### 2026-07-08 23:00
- Command: `uv run pytest`
- Environment: Windows PowerShell, uv-managed CPython 3.13.12.
- Result: pass
- Output summary: 13 tests passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:00
- Command: `uv run ruff check .` and `uv run ruff format --check .`
- Environment: Windows PowerShell, uv-managed CPython 3.13.12.
- Result: pass
- Output summary: Ruff lint passed and 68 files were already formatted.
- Failures: Initial line length issues were fixed before final run.
- Fixes attempted: Applied Ruff formatting and wrapped long lines.

### 2026-07-08 23:00
- Command: `uv run captionman doctor`
- Environment: Windows PowerShell, mock provider, local ffmpeg/ffprobe.
- Result: pass
- Output summary: Mock provider ready, ffmpeg and ffprobe found.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:00
- Command: `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`
- Environment: Windows PowerShell, mock provider.
- Result: pass
- Output summary: Wrote `output/results.json`.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:00
- Command: `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, Python 3.11.0.
- Result: pass
- Output summary: Official output validation passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:00
- Command: `python scripts/check_source_hygiene.py` and `python scripts/check_no_secrets.py`
- Environment: Windows PowerShell, Python 3.11.0.
- Result: pass
- Output summary: Source hygiene passed and no secrets were detected.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:00
- Command: `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Biome checked 23 source files; Vitest passed 1 test; Next.js production build completed.
- Failures: Initial Biome scan included `.next` and Next route params needed async typing.
- Fixes attempted: Scoped Biome to source paths, formatted source, and updated dynamic route props.

### 2026-07-08 23:00
- Command: `docker build -t captionman .`
- Environment: Windows PowerShell, Docker CLI installed.
- Result: fail
- Output summary: Docker could not connect to Docker Desktop Linux engine.
- Failures: `open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`.
- Fixes attempted: Added `.dockerignore`; no code retry possible until Docker daemon is running.

### 2026-07-08 23:10
- Command: `docker build -t captionman .`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Built `captionman:latest`; Dockerfile `RUN captionman --help` passed inside the image.
- Failures: None.
- Fixes attempted: Docker Desktop Linux engine was started before rerun.

### 2026-07-08 23:10
- Command: `docker run --rm captionman captionman doctor`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Mock provider ready; ffmpeg and ffprobe present inside container.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:10
- Command: `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Container wrote `/output/results.json`.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:10
- Command: `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, Python 3.11.0.
- Result: pass
- Output summary: Docker-produced official output validation passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:25
- Command: `uv run pytest`
- Environment: Windows PowerShell, uv-managed CPython 3.13.12.
- Result: pass
- Output summary: 13 tests passed after Track 2 schema migration.
- Failures: None.
- Fixes attempted: Updated tests to assert official `task_id` and nested `captions` output.

### 2026-07-08 23:25
- Command: `uv run ruff check .` and `uv run ruff format --check .`
- Environment: Windows PowerShell, uv-managed CPython 3.13.12.
- Result: pass
- Output summary: Ruff lint passed and 68 backend files were formatted.
- Failures: One file needed formatting during migration.
- Fixes attempted: Ran `uv run ruff format .`.

### 2026-07-08 23:25
- Command: `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`
- Environment: Windows PowerShell, mock provider.
- Result: pass
- Output summary: Wrote official Track 2 list output with `task_id` and `captions`.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:25
- Command: `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, Python 3.11.0.
- Result: pass
- Output summary: Confirmed official Track 2 output shape.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:25
- Command: `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Biome, Vitest, and Next.js build passed with nested `captions` schema.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:25
- Command: `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`
- Environment: Windows PowerShell, Docker Desktop Linux engine.
- Result: pass
- Output summary: Docker image rebuilt, doctor passed, and Docker mock judged run wrote official Track 2 output.
- Failures: None.
- Fixes attempted: None.

### 2026-07-08 23:25
- Command: `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`
- Environment: Windows PowerShell, Python 3.11.0.
- Result: pass
- Output summary: Source hygiene passed and no secrets were detected.
- Failures: None.
- Fixes attempted: Added `extra_files/` to `.gitignore` before reading the participant guide.

### 2026-07-09 00:15
- Command: `pnpm --filter web lint`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Biome checked 39 frontend source files with no fixes needed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 00:15
- Command: `pnpm --filter web test`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Vitest passed 1 schema test.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 00:15
- Command: `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Next.js production build completed for `/`, `/studio`, `/runs/[runId]`, `/submission`, and legacy redirect routes.
- Failures: None.
- Fixes attempted: Removed stale `.next` before the clean build.

### 2026-07-09 00:15
- Command: Playwright production browser checks against `http://localhost:3000/runs/demo`
- Environment: Windows PowerShell, Next.js production server on port 3000, Chromium via local Playwright dependency.
- Result: pass
- Output summary: Page returned 200, no failed requests, no console warnings/errors, Judge Replay/Court/Diff content present, Verdict tab opened, and desktop/mobile screenshots were reviewed at `output/playwright/runs-demo-desktop.png` and `output/playwright/runs-demo-mobile.png`.
- Failures: Initial CLI screenshot invocation failed because PowerShell split the viewport argument; direct local Playwright capture succeeded.
- Fixes attempted: Re-captured screenshots through the local Playwright runtime.

### 2026-07-09 09:11
- Command: `AI_PROVIDER=fireworks uv run captionman doctor`
- Environment: Windows PowerShell, Fireworks API key from ignored `.env`.
- Result: pass
- Output summary: ffmpeg and ffprobe were found; Fireworks `kimi-k2p6` vision model and `glm-5p2` text/judge model were ready, serverless, chat-capable, and the text model passed a live health check.
- Failures: Earlier `gpt-oss-120b` smoke check returned no visible content with a tiny token cap, so text/judge defaults were changed to `glm-5p2`.
- Fixes attempted: Updated `.env.example` and local `.env` model defaults without exposing secrets.

### 2026-07-09 09:11
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`
- Environment: Windows PowerShell, uv-managed CPython 3.13.12.
- Result: pass
- Output summary: Ruff lint passed, 68 backend files were formatted, and 13 tests passed.
- Failures: Intermediate formatting issue in `fireworks.py` was fixed before final run.
- Fixes attempted: Ran Ruff formatter on the provider file.

### 2026-07-09 09:11
- Command: `AI_PROVIDER=fireworks NUM_FRAMES=4 CAPTION_CANDIDATES_PER_STYLE=1 MAX_MODEL_CALLS_PER_VIDEO=5 uv run captionman run --input ../../.data/manual-fireworks-v1/input.json --output ../../.data/manual-fireworks-v1/results.json --debug-dir ../../.data/manual-fireworks-v1/debug`
- Environment: Windows PowerShell, Fireworks real provider, local `v1` sample video.
- Result: pass
- Output summary: Wrote official result for `v1`; budget recorded exactly 5 model calls: one vision evidence call and four caption calls.
- Failures: Earlier runs exposed non-JSON vision output and meta caption text; official validation rejected one overlong caption before cleanup was added.
- Fixes attempted: Added JSON-mode requests, unstructured vision observation extraction, task-metadata fallback, caption cleanup, meta-caption detection, and deterministic fallback captions.

### 2026-07-09 09:11
- Command: `python scripts/validate_results.py .data/manual-fireworks-v1/results.json`
- Environment: Windows PowerShell, Python 3.11.0.
- Result: pass
- Output summary: Official Track 2 result validation passed for the real-provider `v1` output.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-09 09:14
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`
- Environment: Windows PowerShell, uv-managed CPython 3.13.12.
- Result: pass
- Output summary: Ruff lint passed, 70 backend files were formatted, and 16 tests passed including caption safety tests.
- Failures: Ruff initially requested formatting in `pipeline.py`.
- Fixes attempted: Ran Ruff formatter.

### 2026-07-09 09:14
- Command: `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, mock provider.
- Result: pass
- Output summary: Mock judged runner wrote official output and validation passed after central caption safety was added.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:16
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`
- Environment: Windows PowerShell, uv-managed CPython 3.13.12.
- Result: pass
- Output summary: Ruff lint passed, 72 backend files were formatted, and 17 tests passed including result writer validation.
- Failures: Ruff initially requested formatting/import cleanup in the new validator files.
- Fixes attempted: Ran Ruff formatter and import fixer.

### 2026-07-09 09:16
- Command: `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, mock provider.
- Result: pass
- Output summary: Mock judged runner wrote official output through the in-process result validator, and the external validator also passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:18
- Command: `docker build -t captionman .`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Docker image built and Dockerfile `RUN captionman --help` passed.
- Failures: First attempt failed because Docker Desktop Linux engine was not running.
- Fixes attempted: Started Docker Desktop and waited for `docker info` to report `linux 29.5.3`.

### 2026-07-09 09:18
- Command: `docker run --rm captionman captionman doctor`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Mock provider ready; ffmpeg and ffprobe available inside the container.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:18
- Command: `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`; `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Docker mock judged run wrote `/output/results.json`; host-side official output validation passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:18
- Command: `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`
- Environment: Windows PowerShell, Python 3.11.0.
- Result: pass
- Output summary: Source hygiene passed and no secrets were detected.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:30
- Command: capped Fireworks `v2` run with `NUM_FRAMES=4`, `CAPTION_CANDIDATES_PER_STYLE=1`, and `MAX_MODEL_CALLS_PER_VIDEO=5`
- Environment: Windows PowerShell, Fireworks real provider.
- Result: pass
- Output summary: Official `v2` result validation passed; final output was grounded in the orange kitten garden clip and recorded exactly 5 model calls.
- Failures: Earlier `v2` output exposed traffic-themed fallback text and contact-sheet/frame language.
- Fixes attempted: Routed provider fallback through central caption safety and blocked analysis artifact language.

### 2026-07-09 09:30
- Command: capped Fireworks `v3` run with `NUM_FRAMES=4`, `CAPTION_CANDIDATES_PER_STYLE=1`, and `MAX_MODEL_CALLS_PER_VIDEO=5`
- Environment: Windows PowerShell, Fireworks real provider.
- Result: pass
- Output summary: Official `v3` result validation passed; final output was grounded in the office-worker computer clip and recorded exactly 5 model calls.
- Failures: Earlier `v3` output exposed unnecessary appearance details, dangling truncation, frame references, unsupported internal-thought humor, and drafting language.
- Fixes attempted: Added safety rules for sensitive appearance descriptors, dangling phrase endings, frame references, unsupported intent, and drafting-language fragments.

### 2026-07-09 09:30
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, uv-managed CPython 3.13.12.
- Result: pass
- Output summary: Ruff passed, 21 backend tests passed, mock judged run wrote output, and official validation passed.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-09 09:33
- Command: `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`; `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Docker image rebuilt after the quality safety commit; container doctor passed; Docker mock judged run wrote official output; host validator passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:33
- Command: `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`
- Environment: Windows PowerShell, Python 3.11.0.
- Result: pass
- Output summary: Source hygiene passed and no secrets were detected after final Docker verification.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:51
- Command: capped Fireworks runs for `v1`, `v2`, and `v3` with `NUM_FRAMES=4`, `CAPTION_CANDIDATES_PER_STYLE=1`, and `MAX_MODEL_CALLS_PER_VIDEO=5`
- Environment: Windows PowerShell, Fireworks real provider.
- Result: pass
- Output summary: All three practice outputs validated; each debug replay recorded exactly 5 model calls.
- Failures: Iterations exposed unsupported joke details such as exhaust fumes, demand-snacks kitten humor, office privacy commentary, incomplete drafting phrases, and unnecessary clothing/gender details.
- Fixes attempted: Added regression-tested safety rules and targeted evidence-grounded fallback captions.

### 2026-07-09 09:51
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`
- Environment: Windows PowerShell, uv-managed CPython 3.13.12.
- Result: pass
- Output summary: Ruff passed, 72 backend files were formatted, and 26 tests passed.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-09 09:51
- Command: `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`; `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Docker image rebuilt after final safety changes; container doctor passed; Docker mock judged run wrote official output; host validator passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:55
- Command: `pnpm --filter web lint`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Biome checked 41 web source files after formatting the new replay adapter.
- Failures: Initial run required formatting in `lib/replay-artifact.ts` and `tests/replay-artifact.test.ts`.
- Fixes attempted: Ran `pnpm --filter web exec biome check --write lib/replay-artifact.ts tests/replay-artifact.test.ts`.

### 2026-07-09 09:55
- Command: `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Vitest passed 2 web tests, including the backend replay adapter test; Next.js production build completed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:55
- Command: Playwright browser smoke check for `http://localhost:3000/runs/demo`
- Environment: Windows PowerShell, Next.js production server on port 3000.
- Result: pass
- Output summary: Page returned 200, replay/court/diff content was present, and there were no failed requests or console warnings/errors.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 09:59
- Command: `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Biome checked 42 files, Vitest passed 2 tests, and Next.js production build completed.
- Failures: Initial lint run required formatting in the new run history panel.
- Fixes attempted: Ran Biome formatter on `components/evidence-cinema/run-history-panel.tsx`.

### 2026-07-09 09:59
- Command: Playwright browser smoke check for `http://localhost:3000/studio`
- Environment: Windows PowerShell, Next.js production server on port 3000.
- Result: pass
- Output summary: Page returned 200, Studio and Run History content were present, fallback state rendered, and there were no failed requests or console warnings/errors.
- Failures: Initial smoke check observed an aborted Next.js prefetch request for `/runs/demo`.
- Fixes attempted: Disabled prefetch on replay links.

### 2026-07-09 10:07
- Command: Playwright launcher flow on `http://localhost:3000/studio` against FastAPI mock server on port 8000
- Environment: Windows PowerShell, Next.js production server, FastAPI demo API with `AI_PROVIDER=mock`.
- Result: pass
- Output summary: Studio launcher posted to `/api/runs`, created a completed run, and the generated `/runs/{runId}` page loaded backend replay/results artifacts.
- Failures: Initial polling flow exposed a Windows `PermissionError` while replacing `status.json` during repeated status reads.
- Fixes attempted: Added retry behavior to `atomic_write_text` and restarted the API server.

### 2026-07-09 10:07
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell.
- Result: pass
- Output summary: Backend lint/format passed, 29 backend tests passed, web lint passed, 2 web tests passed, and web production build passed.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-09 10:12
- Command: `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`; `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`; `python scripts/validate_results.py output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine.
- Result: pass
- Output summary: Source hygiene passed, no secrets were detected, Docker image built, container doctor passed with mock provider and ffmpeg/ffprobe, judged mock container wrote `/output/results.json`, and official output validation passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 10:28
- Command: `uv run pytest tests/test_validate_results.py tests/test_result_writer_validation.py tests/test_schema_adapter.py`; `uv run pytest tests/test_doctor.py tests/test_official_mode.py tests/test_budget.py`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `uv run captionman doctor`; `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; `python scripts/run_model_tournament.py --routes mock_baseline`; `python -m py_compile scripts/run_model_tournament.py scripts/validate_results.py scripts/check_no_secrets.py scripts/check_source_hygiene.py`; `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`
- Environment: Windows PowerShell.
- Result: pass
- Output summary: Focused backend tests passed, full backend suite passed with 35 tests, doctor reported provider/routing/Gemma/proxy state, official-mode mock run wrote `output/results.json`, input-aware result validation passed, the no-credit mock tournament route passed, source hygiene passed, and no secrets were detected.
- Failures: Initial focused checks found formatting and one line-length issue. Two shell attempts used bash-style env syntax or the wrong `uv` working directory in PowerShell.
- Fixes attempted: Ran Ruff formatting, split the long Fireworks prompt string, and reran the mock official command from `apps/api` with PowerShell environment variables.

### 2026-07-09 10:36
- Command: `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine.
- Result: pass
- Output summary: The linux/amd64 image built, container doctor passed, official-mode mock container wrote `/output/results.json`, and input-aware official validation passed.
- Failures: First Docker attempt failed because `com.docker.service` was stopped and the `dockerDesktopLinuxEngine` pipe was unavailable.
- Fixes attempted: Launched Docker Desktop, waited for `docker info` to report `linux 29.5.3`, then reran the Docker gate successfully.

### 2026-07-09 12:27
- Command: `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Biome checked 43 files, Vitest passed 2 tests, and Next.js production build completed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 12:45
- Command: `uv run ruff check app/core/config.py app/providers/model_registry.py app/providers/proxy.py app/providers/fireworks_direct.py tests/test_doctor.py`; `uv run pytest tests/test_doctor.py tests/test_official_mode.py`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `python -m py_compile scripts/check_no_secrets.py scripts/run_model_tournament.py`
- Environment: Windows PowerShell.
- Result: pass
- Output summary: Focused provider/doctor tests passed, source hygiene passed, no secrets were detected, and credential scripts compiled.
- Failures: The first stricter no-secrets run produced false positives on safe placeholders and Python provider parameters.
- Fixes attempted: Tightened assignment matching to avoid crossing lines, allow safe placeholders, and allow internal `settings.*` parameter references.

### 2026-07-09 12:58
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; `python scripts/run_model_tournament.py --routes mock_baseline`; `AI_PROVIDER=mock uv run captionman doctor`; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine.
- Result: pass
- Output summary: Backend lint/format passed, 37 backend tests passed, no secrets were detected, source hygiene passed, official mock run validated, mock tournament passed, Docker linux/amd64 build passed, container doctor passed, and Docker official-mode mock output validated.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-09 13:18
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; `python scripts/run_model_tournament.py --routes mock_baseline`; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; fake-secret Docker guard checks.
- Environment: Windows PowerShell, Docker Desktop Linux engine.
- Result: pass
- Output summary: Backend lint/format passed, 40 backend tests passed, source scans passed, official mock and tournament runs passed, normal Docker image had no embedded key file, fake embedded-key Docker build succeeded only through `ALLOW_EMBEDDED_HACKATHON_KEY=true`, and Docker official-mode mock output validated.
- Failures: A negative fake-secret build without the explicit flag reused Docker cache and therefore succeeded key-free; this was verified by checking that the produced image did not contain `/app/.captionman/final_fireworks_key`. A follow-up shell assertion for the fake embedded file initially used PowerShell-expanded `$()`.
- Fixes attempted: Verified the normal image has no embedded key file and reran the positive embedded-key image check with a simple file-presence assertion.

### 2026-07-09 13:30
- Command: `uv run captionman doctor`
- Environment: Windows PowerShell, local `.env` with user-approved temporary Fireworks key.
- Result: pass
- Output summary: Direct provider doctor passed with credential source `local_env`, `AI_PROVIDER=fireworks_direct`, champion route `fireworks_kimi_glm`, vision model `accounts/fireworks/models/kimi-k2p6`, caption/judge model `accounts/fireworks/models/glm-5p2`, and live check passed.
- Failures: Gemma specialist route did not pass earlier verification because `accounts/fireworks/models/gemma-4-31b-it` is not serverless on this account.
- Fixes attempted: Kept `GEMMA_MODEL` populated, set `GEMMA_USAGE_MODE=off`, and used the verified Kimi/GLM route for Track 2 readiness.

### 2026-07-09 13:30
- Command: capped `fireworks_direct` v1 canary and v1-v3 practice run; `python scripts/validate_results.py --input .data/manual-fireworks-v1-direct/input.json --output .data/manual-fireworks-v1-direct/results.json`; `python scripts/validate_results.py --input .data/samples/track2/tasks.local.json --output .data/manual-fireworks-v1-v3-direct/results.json`
- Environment: Windows PowerShell, official-mode constraints, `NUM_FRAMES=4`, `CAPTION_CANDIDATES_PER_STYLE=1`, `MAX_MODEL_CALLS_PER_VIDEO=5`.
- Result: pass
- Output summary: v1 canary completed in about 23 seconds and validated. The v1-v3 run completed in under one minute, produced captions for all four requested styles per task, and validated against the participant-guide task list.
- Failures: The first disposable v1 input was written with a UTF-8 BOM, and the validator rejected it even though the runtime loader accepted BOM-marked JSON.
- Fixes attempted: Updated `scripts/validate_results.py` to read `utf-8-sig`; focused validator tests passed.

### 2026-07-09 13:30
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine.
- Result: pass
- Output summary: Backend lint/format passed, 41 backend tests passed, web lint passed, 2 web tests passed, web production build passed, no secrets were detected, source hygiene passed, normal linux/amd64 Docker build passed, container doctor passed, Docker official-mode mock run wrote `/output/results.json`, and validation passed.
- Failures: Full backend suite initially caught that `REQUIRE_GEMMA_FOR_SUBMISSION=true` only checked whether a Gemma model was named, not whether Gemma was active in the selected route.
- Fixes attempted: Changed doctor to fail closed when Gemma is required but inactive and updated the unit test; full suite then passed.

### 2026-07-09 18:10
- Command: `uv run pytest tests/test_doctor.py`; `uv run ruff check app/providers/model_registry.py app/server/routes/doctor.py tests/test_doctor.py`; `uv run ruff format --check app/providers/model_registry.py app/server/routes/doctor.py tests/test_doctor.py`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, local FastAPI/Next.js dev servers on ports 8000 and 3000.
- Result: pass
- Output summary: Focused backend doctor suite passed with 6 tests, backend lint/format passed, Biome checked 43 frontend files, Vitest passed 2 tests, and Next.js production build completed.
- Failures: First Playwright screenshots showed an unstyled/stale dev-server state because `next build` had been run while the dev server was active, leaving mixed `.next` chunks.
- Fixes attempted: Stopped the web listener, removed generated `apps/web/.next`, restarted Next.js, and recaptured desktop/mobile Studio and Replay screenshots.

### 2026-07-09 18:10
- Command: Playwright screenshots for `http://127.0.0.1:3000/studio` and `http://127.0.0.1:3000/runs/demo` at desktop and mobile viewports.
- Environment: Chromium via Playwright CLI, local API with `/api/doctor?live=false`.
- Result: pass
- Output summary: Studio clearly shows real Fireworks run vs no-credit replay, recent runs, a real-run process checklist, and verification guidance. Mobile stacks into a single-column flow without overlapping text. Replay page remains responsive and visually styled.
- Failures: Provider status initially stayed in `Checking API` during screenshots because it used the full provider doctor path.
- Fixes attempted: Added lightweight API status through `/api/doctor?live=false` and updated the provider card to avoid the expensive provider verification path on page load.

### 2026-07-09 18:36
- Command: `uv run pytest tests/test_caption_safety.py`; `uv run pytest`; `uv run ruff check .`; `uv run ruff format --check .`
- Environment: Windows PowerShell, backend package managed by `uv`.
- Result: pass
- Output summary: Focused caption safety passed with 14 tests, full backend passed with 44 tests, Ruff lint passed, and Ruff format check passed after formatting helper scripts.
- Failures: First focused test command from the repo root hit a Python import-path issue; format check flagged four helper scripts for line wrapping.
- Fixes attempted: Reran focused tests from `apps/api`; applied `uv run ruff format` to the helper scripts and reran format check.

### 2026-07-09 18:36
- Command: `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Biome checked 43 frontend files, Vitest passed 2 tests, and Next.js production build completed.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-09 18:36
- Command: Playwright screenshots for `http://127.0.0.1:3000/` and `http://127.0.0.1:3000/studio` at desktop and mobile viewports.
- Environment: Chromium via Playwright CLI, FastAPI on port 8000, Next.js dev server on port 3000.
- Result: pass
- Output summary: Landing page renders a full image-backed CaptionMan first screen, Studio clearly separates real Fireworks runs from mock replay, and mobile layouts stack without text overlap.
- Failures: First mobile landing screenshot showed oversized hero badges because mobile grid stretch affected the chip row.
- Fixes attempted: Added landing-specific mobile badge alignment rules and recaptured the mobile screenshot.

### 2026-07-09 18:36
- Command: `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; local official mock run and validation; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; Docker official mock run and validation.
- Environment: Windows PowerShell, Docker Desktop Linux engine.
- Result: pass
- Output summary: No secrets were detected, source hygiene passed, local official-mode mock output validated, linux/amd64 Docker image rebuilt key-free, container doctor passed, Docker official-mode mock run wrote `/output/results.json`, and input-aware validation passed.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-09 19:10
- Command: `uv run pytest`; focused upload/artifact tests; `uv run ruff check .`; `uv run ruff format --check .`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, local FastAPI/Next.js dev servers.
- Result: pass
- Output summary: Backend passed 47 tests, web passed 3 tests, frontend lint/build passed, backend lint/format passed, and upload/frame artifact tests covered the new Studio product path.
- Failures: Initial API restart exposed BOM-marked local smoke artifacts in artifact/status readers.
- Fixes attempted: Made artifact JSON reads and run status reads `utf-8-sig` tolerant.

### 2026-07-09 19:10
- Command: Playwright screenshots for `http://127.0.0.1:3000/studio` and `http://127.0.0.1:3000/runs/ui_frame_smoke`.
- Environment: Chromium via Playwright CLI, FastAPI on port 8000, Next.js on port 3000.
- Result: pass
- Output summary: Studio shows both the practice batch and upload-video path on desktop/mobile. Judge Replay renders actual sampled urban boulevard JPEG frames through the API frame artifact endpoint.
- Failures: First replay screenshot fell back to mock data because the smoke artifact used a single replay object rather than a list.
- Fixes attempted: Made the frontend replay adapter accept both list and single-object replay/results artifacts; recaptured screenshot confirmed real frames.

### 2026-07-09 19:10
- Command: capped real-provider `frame-canary-v1` run; `python scripts/validate_results.py --input .data/frame-fireworks-v1-canary/input.json --output .data/frame-fireworks-v1-canary/results.json`
- Environment: Windows PowerShell, `AI_PROVIDER=fireworks_direct`, `OFFICIAL_MODE=true`, `NUM_FRAMES=4`, `CAPTION_CANDIDATES_PER_STYLE=1`, `MAX_MODEL_CALLS_PER_VIDEO=5`.
- Result: pass
- Output summary: Single v1 canary completed, official output validated, and four sampled frame JPEGs plus a contact sheet were produced under the API data directory.
- Failures: Two initial canary attempts failed before provider calls due to PowerShell path/JSON array creation issues.
- Fixes attempted: Rewrote the input file with absolute file URL and explicit JSON array text before rerunning.

### 2026-07-09 19:10
- Command: local official mock run and validation; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; Docker official mock run and validation; source hygiene and no-secrets scans.
- Environment: Windows PowerShell, Docker Desktop Linux engine.
- Result: pass
- Output summary: Local official-mode mock output validated, linux/amd64 Docker image rebuilt with `python-multipart`, container doctor passed, Docker official-mode mock output validated, source hygiene passed, and no secrets were detected.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-09 19:45
- Command: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`
- Environment: Windows PowerShell, backend package managed by `uv`.
- Result: pass
- Output summary: Ruff lint passed, 79 backend files were already formatted, and the full backend suite passed with 53 tests.
- Failures: Earlier focused tests failed because exact fallback-string expectations still reflected older, less professional captions.
- Fixes attempted: Updated the tests to assert the new professional fallback wording and reran the suite.

### 2026-07-09 19:45
- Command: capped real-provider `frame-canary-v1` run; `python scripts/validate_results.py --input .data/frame-fireworks-v1-canary/input.json --output .data/natural-caption-v1-canary/results.json`
- Environment: Windows PowerShell, `AI_PROVIDER=fireworks_direct`, `OFFICIAL_MODE=true`, `NUM_FRAMES=4`, `CAPTION_CANDIDATES_PER_STYLE=1`, `MAX_MODEL_CALLS_PER_VIDEO=5`, verified Kimi/GLM champion route.
- Result: pass
- Output summary: Final canary validated and produced: formal `"Cars and buses travel along a multi-lane autumn boulevard lined with golden trees and high-rise buildings."`, sarcastic `"The golden trees are working overtime to make traffic look worth the wait."`, tech `"Autumn traffic gets beautiful color grading, even while throughput stays low."`, and non-tech `"Autumn made the boulevard look fancy; the traffic did not get the memo."`
- Failures: Earlier canaries exposed a Gemma specialist `404`/non-serverless route, a word-count self-check leak, and an unfinished tech clause.
- Fixes attempted: Kept Gemma inactive, loaded Markdown style prompts into Fireworks caption calls, added word-count and dangling-clause safety regressions, and reran the constrained canary.

### 2026-07-09 19:45
- Command: `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ...tasks.local.json --output ...natural-caption-mock/results.json`; `python scripts/validate_results.py --input .data/samples/track2/tasks.local.json --output .data/natural-caption-mock/results.json`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`
- Environment: Windows PowerShell, local mock provider and repository scans.
- Result: pass
- Output summary: Local official mock output validated, no secrets were detected, and source hygiene passed.
- Failures: First mock command used an API-folder-relative input path and failed before pipeline execution.
- Fixes attempted: Reran with absolute repo paths.

### 2026-07-09 19:45
- Command: `docker buildx build --platform linux/amd64 -t captionman:test --load .`
- Environment: Windows PowerShell, Docker CLI.
- Result: fail
- Output summary: Docker could not connect to `npipe:////./pipe/dockerDesktopLinuxEngine`.
- Failures: Docker Desktop Linux engine was not reachable.
- Fixes attempted: Started Docker Desktop in the background; Docker gate still needs rerun when the engine is ready.

### 2026-07-09 19:48
- Command: `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Linux/amd64 image built, Dockerfile copied `prompts` into `/app/prompts`, container doctor passed, container official-mode mock run wrote `/output/results.json`, and host validation passed.
- Failures: None after Docker Desktop started.
- Fixes attempted: None.

### 2026-07-09 20:15
- Command: `uv run pytest tests/test_credentials.py tests/test_doctor.py`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`
- Environment: Windows PowerShell.
- Result: pass
- Output summary: Focused credential/doctor suite passed with 10 tests, no secrets were detected, and source hygiene passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 20:15
- Command: normal Docker build, doctor, mock judged run, and validation.
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Normal `captionman:test` image built for `linux/amd64`, defaulted to `AI_PROVIDER=mock`, had no embedded credential source, container doctor passed, official-mode mock container run wrote `/output/results.json`, and input-aware validation passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-09 20:15
- Command: fake embedded-key Docker guard tests.
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3, fake ignored key file under `.data/final-secrets/`.
- Result: pass
- Output summary: Negative build with `ALLOW_EMBEDDED_HACKATHON_KEY=true` but no final runtime args failed with `Embedded-key final images must set RUNTIME_AI_PROVIDER=fireworks_direct`. Positive fake final build with `RUNTIME_AI_PROVIDER=fireworks_direct` and `RUNTIME_OFFICIAL_MODE=true` succeeded. Runtime inspection reported `fireworks_direct`, `True`, `champion`, `fireworks_kimi_glm`, `embedded_hackathon_key`, `kimi-k2p6`, and `glm-5p2` without printing the secret.
- Failures: The negative build failed intentionally as the guard proof.
- Fixes attempted: None.

### 2026-07-10 09:40
- Command: `pnpm --filter web lint`; `pnpm --filter web test`; clean `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Biome checked 43 files, Vitest passed 3 tests, and Next.js production build completed after removing stale `.next` output.
- Failures: The first production `next start` hit a stale `.next/server` vendor chunk error.
- Fixes attempted: Stopped the web server, removed only `apps/web/.next`, rebuilt, and restarted production mode from `apps/web`.

### 2026-07-10 09:40
- Command: Playwright production browser workflow for `/studio` and `/runs/[runId]`.
- Environment: Chromium via Playwright, FastAPI mock provider on port 8000, Next.js production server on port 3000.
- Result: pass
- Output summary: Added the practice batch, ran it, uploaded `v1_urban_autumn_boulevard.mp4`, ran it, verified caption cards and controlled video preview, opened replay, captured desktop/mobile screenshots, and verified mobile horizontal overflow was `0px`.
- Failures: Early checks exposed unhydrated dev-server assets, over-strict duplicate text assertions, and mobile overflow in recent-run rows.
- Fixes attempted: Switched to production `next start`, tightened assertions to intended elements, added an upload input label, and changed mobile recent-run rows to wrap inside the card.

### 2026-07-10 09:40
- Command: `uv run pytest` from `apps/api`; local `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../.data/verify/ui-polish-results.json --debug-dir ../../.data/verify/ui-polish-debug`; `python ../../scripts/validate_results.py ../../.data/verify/ui-polish-results.json`
- Environment: Windows PowerShell, backend package managed by `uv`.
- Result: pass
- Output summary: API test suite passed with 53 tests, local judged mock run wrote a valid results file, and the validator passed.
- Failures: Running `uv run pytest` from the repository root failed because the root is not a Python project and imports resolved against the wrong environment.
- Fixes attempted: Reran from `apps/api`, where `pyproject.toml` and the `uv` environment are defined.

### 2026-07-10 09:40
- Command: `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `docker build -t captionman .`
- Environment: Windows PowerShell.
- Result: partial
- Output summary: No-secrets and source-hygiene scans passed. Docker build could not start because the Docker Desktop Linux engine was not reachable at `npipe:////./pipe/dockerDesktopLinuxEngine`.
- Failures: Docker daemon unavailable.
- Fixes attempted: None in code; rerun Docker gates after Docker Desktop Linux engine is started.

### 2026-07-10 10:10
- Command: focused URL/upload route tests; `uv run pytest`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, backend package managed by `uv`, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Focused API route/security tests passed with 10 tests, the full API suite passed with 55 tests, frontend lint passed, frontend Vitest passed with 3 tests, and Next.js production build completed.
- Failures: Initial route lint reported import ordering and one long known-clip description line.
- Fixes attempted: Ran Ruff fix and split the long string.

### 2026-07-10 10:10
- Command: Playwright production browser workflow for `/studio` with direct URL, upload, replay navigation, desktop/mobile screenshots, and hidden demo-copy check.
- Environment: Chromium via Playwright, FastAPI on port 8000, Next.js production server on port 3000.
- Result: pass
- Output summary: Direct URL input queued and completed, file upload queued and completed, replay opened from the result panel, mobile had no horizontal overflow, and the main Studio page did not show removed mock/no-credit/practice wording.
- Failures: First assertion matched the same office phrase in all four caption cards.
- Fixes attempted: Tightened the assertion to the first matching caption card and reran the workflow.

### 2026-07-10 10:10
- Command: capped real-provider URL canary through CLI and capped real-provider URL run through Studio.
- Environment: `AI_PROVIDER=fireworks_direct`, `OFFICIAL_MODE=true`, `MODEL_ROUTING_MODE=champion`, `CHAMPION_ROUTE=fireworks_kimi_glm`, `GEMMA_USAGE_MODE=off`, `CAPTION_CANDIDATES_PER_STYLE=1`, `MAX_MODEL_CALLS_PER_VIDEO=5`, `NUM_FRAMES=4`.
- Result: pass
- Output summary: CLI URL canary validated official output. Studio URL run completed with grounded captions about an office worker, desktop computer, keyboard, and open-plan office; screenshot captured at `apps/web/output/playwright/studio-real-url-complete.png`.
- Failures: First CLI canary input was accidentally written under `apps/api/.data` instead of root `.data`, so the runner could not find it. No provider call was made on that failed attempt.
- Fixes attempted: Rewrote the canary input under root `.data/verify/url-real-v3` and reran.

### 2026-07-10 10:10
- Command: `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: Linux/amd64 image built, container doctor passed, mounted official-mode run wrote `/output/results.json`, and input-aware validation passed.
- Failures: None after Docker Desktop was running.
- Fixes attempted: None.

### 2026-07-10 13:40
- Command: focused route/credential/caption checks; `uv run pytest`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, backend package managed by `uv`, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Focused backend checks passed, full backend suite passed with 60 tests, web lint passed, Vitest passed with 3 tests, and Next.js production build completed.
- Failures: Caption-safety test expectations initially still used the older shorter fallback copy.
- Fixes attempted: Updated the expected strings to lock in the richer captions.

### 2026-07-10 13:40
- Command: Playwright production browser canary for uploaded `E:\Trmp\348656_medium.mp4`.
- Environment: Chromium via Playwright, FastAPI on port 8000 with capped `fireworks_direct`, Next.js production server on port 3000.
- Result: pass
- Output summary: Uploaded the local flower video, completed a real-provider run, verified `My Portfolio` points to `https://grimnej.com`, confirmed banned filename/contact-sheet/sample-count phrases were absent, captured `apps/web/output/playwright/studio-upload-348656-fixed.png`, opened Judge Verdict, and captured `apps/web/output/playwright/judge-verdict-348656-fixed.png`.
- Failures: Earlier canaries exposed malformed upload file URI generation and model outputs that mentioned sampled-frame structure.
- Fixes attempted: Switched upload tasks to `Path.as_uri()`, made Fireworks file resolution tolerate legacy `file://E:/...`, and added caption guards for sampled-frame count wording.

### 2026-07-10 13:40
- Command: `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`
- Environment: Windows PowerShell, Docker Desktop Linux engine.
- Result: pass
- Output summary: No secrets were detected, source hygiene passed, normal linux/amd64 image built key-free, container doctor passed with mock default, Docker official-mode mock run wrote `/output/results.json`, and validation passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-10 13:55
- Command: `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0.
- Result: pass
- Output summary: Biome checked 43 files, Vitest passed 3 tests, and Next.js production build completed.
- Failures: First lint run required a formatter line break in the restore logic.
- Fixes attempted: Applied the formatter-compatible line break and reran.

### 2026-07-10 13:55
- Command: Playwright production browser persistence check for `/studio`.
- Environment: Chromium via Playwright, Next.js production server on port 3000.
- Result: pass
- Output summary: Seeded four completed Studio queue items in browser storage, loaded Studio, opened a Judge Verdict link, navigated back, confirmed `4 queued` still rendered, selected a restored upload, confirmed its captions remained, and captured `apps/web/output/playwright/studio-queue-persistence.png`.
- Failures: The first browser assertion targeted a broad recent-history verdict link instead of the result-panel verdict button.
- Fixes attempted: Scoped the assertion to `a.cm-button-primary[href^="/runs/"]` and reran.

### 2026-07-10 13:55
- Command: `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`
- Environment: Windows PowerShell.
- Result: pass
- Output summary: No secrets were detected and source hygiene passed after the Studio persistence change.
- Failures: None.
- Fixes attempted: None.

### 2026-07-10 14:10
- Command: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\launch_demo.ps1 -Restart -SkipOpen`
- Environment: Windows PowerShell, local `.env`, FastAPI on port 8000, Next.js production server on port 3000.
- Result: pass
- Output summary: The checked-in launcher restarted both services, set capped `fireworks_direct` demo settings, verified `/api/health`, verified `/api/doctor?live=false`, waited for `/studio`, and printed the ready Studio/API URLs plus process IDs.
- Failures: First draft exposed two launcher bugs before final pass: `pnpm` resolved to a PowerShell shim that `Start-Process` could not execute directly, and host-only output was not visible in command logs.
- Fixes attempted: Resolved `.ps1` command shims to `.cmd`/`.exe` when available and switched final status lines to `Write-Output`.

### 2026-07-10 14:10
- Command: Independent endpoint checks after launcher pass.
- Environment: Windows PowerShell, launcher-started services.
- Result: pass
- Output summary: Ports 8000 and 3000 were listening; `/api/health` returned `ok: true`; `/api/doctor?live=false` returned `ok: true` with `AI_PROVIDER=fireworks_direct` and the verified Kimi/GLM route; `/studio` returned HTTP 200.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-10 14:10
- Command: `Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/doctor?live=true'`
- Environment: Windows PowerShell, launcher-started API using local temporary Fireworks credentials.
- Result: pass
- Output summary: Live provider doctor returned `ok: true`; `fireworks_direct` credential source was local env; `kimi-k2p6` vision, `glm-5p2` caption, and `glm-5p2` judge checks were ready/serverless as applicable; live text-model check passed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-10 14:45
- Command: Participant-guide PDF extraction and Track 2 requirement review.
- Environment: Windows PowerShell, local ignored guide at `extra_files/Participant Guide_ AMD Developer Hackathon (ACT II).pdf`.
- Result: pass
- Output summary: Confirmed Track 2 requires a publicly pullable Docker image, `linux/amd64`, `/input/tasks.json` input, `/output/results.json` output, no inference log, no injected credentials or model restrictions, own credentials inside the container, hidden 30-second to 2-minute clips, every requested style present, valid JSON, 10-minute runtime cap, and image under 10 GB compressed.
- Failures: None.
- Fixes attempted: None.

### 2026-07-10 14:45
- Command: `uv run pytest`
- Environment: Windows PowerShell, backend package under `apps/api`.
- Result: pass
- Output summary: 60 backend tests passed with 1 Starlette deprecation warning.
- Failures: None.
- Fixes attempted: None.

### 2026-07-10 14:45
- Command: `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`
- Environment: Windows PowerShell.
- Result: pass
- Output summary: No secrets detected and source hygiene passed after tightening `.dockerignore`.
- Failures: None.
- Fixes attempted: None.

### 2026-07-10 14:45
- Command: `docker buildx build --no-cache --platform linux/amd64 -t captionman:submission-audit --load .`
- Environment: Docker Desktop Linux engine 29.5.3.
- Result: pass
- Output summary: No-cache `linux/amd64` build succeeded with tightened Docker context. Image inspection reported `amd64 linux` and size about 291 MB.
- Failures: The first audit found host `__pycache__` files copied into `/app/app`.
- Fixes attempted: Added Python cache exclusions to `.dockerignore` and rebuilt with `--no-cache`.

### 2026-07-10 14:45
- Command: Docker runtime boundary checks for `captionman:submission-audit`.
- Environment: Docker Desktop Linux engine.
- Result: pass
- Output summary: Container doctor passed with mock default. `/app` contained runtime backend app, prompts, README, and virtualenv only; boundary check confirmed no `/app/.env`, `/app/extra_files`, `/app/apps`, or `/app/docs`; no copied app `__pycache__` or `*.pyc` files were found.
- Failures: None after `.dockerignore` cache exclusions.
- Fixes attempted: None.

### 2026-07-10 14:45
- Command: `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:submission-audit`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`
- Environment: Docker Desktop Linux engine with mounted official input/output folders.
- Result: pass
- Output summary: Container wrote `/output/results.json`; host validator passed with input-aware style checking.
- Failures: None.
- Fixes attempted: None.

### 2026-07-10 14:45
- Command: Fake embedded-key final build and config inspection.
- Environment: Docker Desktop Linux engine, ignored fake key file under `.data/final-secrets/`.
- Result: pass
- Output summary: Build with `ALLOW_EMBEDDED_HACKATHON_KEY=true`, `RUNTIME_AI_PROVIDER=fireworks_direct`, `RUNTIME_OFFICIAL_MODE=true`, and BuildKit secret succeeded. Runtime config inspection reported `fireworks_direct`, `OFFICIAL_MODE=True`, champion route `fireworks_kimi_glm`, credential source `embedded_hackathon_key`, and a present credential without printing it.
- Failures: None.
- Fixes attempted: None.

### 2026-07-10 15:05
- Command: Public Git branch safety rewrite.
- Environment: Windows PowerShell, Git remote `https://github.com/GrimNej/CaptionMan.git`.
- Result: pass
- Output summary: Working tree and full local history were scanned for secret patterns without printing matched values; public `main` and `master` were force-pushed to the same single clean root commit `0a96e0b`; pushed tree scan found no `.env`, secret files, competitor folders, PDFs, videos, node_modules, `.next`, or generated private data.
- Failures: First orphan-branch attempt timed out before any commit because the local Git version did not support the desired start-point syntax.
- Fixes attempted: Stopped stale Git processes, restored `master`, created a parentless root commit from the current tree with `git commit-tree`, and pushed that commit to both public branches.

### 2026-07-10 15:05
- Command: Final real embedded-key image build and doctor.
- Environment: Docker Desktop Linux engine, ignored temporary hackathon key file under `.data/final-secrets/`.
- Result: pass
- Output summary: Built `ghcr.io/grimnej/captionman:final` locally for `linux/amd64` with `ALLOW_EMBEDDED_HACKATHON_KEY=true`, `RUNTIME_AI_PROVIDER=fireworks_direct`, and `RUNTIME_OFFICIAL_MODE=true`. Image inspection reported `amd64 linux` and about 291 MB. Runtime config inspection reported `fireworks_direct`, `OFFICIAL_MODE=True`, route `fireworks_kimi_glm`, credential source `embedded_hackathon_key`, and a present credential without printing it. Container doctor passed with Kimi vision and GLM caption/judge models ready.
- Failures: None.
- Fixes attempted: None.

### 2026-07-10 15:05
- Command: `docker push ghcr.io/grimnej/captionman:final`
- Environment: Docker Desktop Linux engine.
- Result: fail
- Output summary: Push reached GHCR but returned `denied`.
- Failures: Local Docker client is not authenticated to GHCR.
- Fixes attempted: None in code. User must run `docker login ghcr.io -u GrimNej` and paste the GitHub token into Docker's password prompt, then rerun the push.

### 2026-07-10 15:35
- Command: Public GHCR push and unauthenticated pull.
- Environment: Docker Desktop Linux engine, GHCR authenticated for push, clean temporary Docker config for public pull.
- Result: pass
- Output summary: Pushed `ghcr.io/grimnej/captionman:final`, then pulled it through a clean unauthenticated Docker config. Manifest digest `sha256:78c2f4235c779684c608561c0313769c52cdf8f0a96dd40f0e7f37a1410c9b33` includes a `linux/amd64` manifest.
- Failures: The first public-image mounted run used the old local `mock://` sample input and failed under real provider mode, which correctly expects video URLs.
- Fixes attempted: Replaced tracked `input/tasks.json` with the Track 2 guide practice video URLs.

### 2026-07-10 15:35
- Command: Final caption-safety regression and rebuilt public image.
- Environment: Windows PowerShell, backend tests, Docker Desktop Linux engine.
- Result: pass
- Output summary: A real public-image practice run exposed one incomplete caption ending in `across a`; added a caption-safety regression for dangling preposition phrases, then reran `uv run pytest tests/test_caption_safety.py` with 21 passed and full `uv run pytest` with 61 passed.
- Failures: One real v2 `humorous_tech` caption from the previous image ended mid-phrase.
- Fixes attempted: Broadened `_looks_unsafe` to reject captions ending with dangling prepositions/determiners, rebuilt `ghcr.io/grimnej/captionman:final`, and pushed the replacement image.

### 2026-07-10 15:35
- Command: Final public image doctor and real practice run.
- Environment: Clean unauthenticated Docker config pulling `ghcr.io/grimnej/captionman:final`, mounted guide practice `input/tasks.json`, mounted `output/`.
- Result: pass
- Output summary: Public-pulled image doctor passed with `AI_PROVIDER=fireworks_direct`, `OFFICIAL_MODE=true`, credential source `embedded_hackathon_key`, Kimi vision ready, GLM caption/judge ready, and `linux_amd64=true`. The public image ran v1-v3 guide practice videos, wrote `/output/results.json`, and `python scripts/validate_results.py --input input/tasks.json --output output/results.json` passed. Final captions were complete and free of mock/frame/sample/contact-sheet artifact wording.
- Failures: None in final run.
- Fixes attempted: None.

### 2026-07-10 16:20
- Command: `uv run pytest`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`
- Environment: Windows PowerShell, backend package under `apps/api`.
- Result: pass
- Output summary: Backend suite passed with 71 tests, no secrets were detected, and source hygiene passed after the final caption-safety guards.
- Failures: None in final run.
- Fixes attempted: Added regression coverage for generic/gated caption failures found during repeated real public-image runs.

### 2026-07-10 16:20
- Command: final embedded-key `docker buildx build`, `docker push ghcr.io/grimnej/captionman:final`, clean unauthenticated public pull, `docker run --rm ghcr.io/grimnej/captionman:final captionman doctor`, public-image v1-v3 run, and `python scripts/validate_results.py --input input/tasks.json --output .data/verify/public-final-output/results.json`
- Environment: Docker Desktop Linux engine, clean temporary Docker config for public pull, ignored final Fireworks key file.
- Result: pass
- Output summary: Public image digest is `sha256:138ce0b9828aff1cd65b13143d14962c1d94e2d72e034a630ed691c660c8293c`; manifest includes `linux/amd64`; doctor passed with `fireworks_direct`, `OFFICIAL_MODE=true`, `embedded_hackathon_key`, Kimi vision ready, GLM caption/judge ready, and live provider check passing. Public v1-v3 output validation passed, and the artifact scan found no mock/contact-sheet/frame/sample/meta/dangling-caption failure patterns.
- Failures: Earlier public-image runs exposed generic v3 evidence, model self-commentary, visible-text artifacts, dangling endings, vehicle-blur-only v1 captions, and unprofessional office tech phrasing.
- Fixes attempted: Added caption-safety regressions and targeted Track 2 fallbacks before the final pushed image.

### 2026-07-10 20:00
- Command: `pnpm screenshots`; `pnpm export:pdf`; `pdfinfo CaptionMan_Track2_Presentation.pdf`; `pdftoppm -png -r 144 CaptionMan_Track2_Presentation.pdf rendered/pdf-page`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0, Slidev 52.2.3, Playwright Chromium, Sharp, Poppler/MiKTeX `pdfinfo` and `pdftoppm`.
- Result: pass
- Output summary: Slidev rendered ten 1920x1080 PNGs and `contact-sheet.png`; PDF export produced `CaptionMan_Track2_Presentation.pdf`; `pdfinfo` reported 10 pages and 1440 x 810 pt page size; PDF was rendered back to 10 PNG pages and key pages were visually inspected.
- Failures: Initial screenshots exposed Slidev's `#slidev-goto-dialog` overlay. Initial slide 9 product screenshot crop was too accidental, and slide 4 used stale exact frame-count wording.
- Fixes attempted: Hid Slidev UI chrome, generated a deliberate local product screenshot crop, refined the routing path geometry, and changed slide 4 to "bounded representative frames" before final export.

### 2026-07-10 20:25
- Command: Mock judged run, validation, doctor checks, demo launcher, endpoint checks, and Playwright showcase screenshots.
- Environment: Windows PowerShell, backend under `apps/api`, production Next.js app on port 3000, FastAPI on port 8000, Playwright from `apps/web`.
- Result: pass
- Output summary: Mock official run wrote `output/results.json`; input-aware validation passed; mock doctor passed; `fireworks_direct` doctor passed with Gemma configured as repair model but inactive; launcher brought up API and Studio; `/api/health`, `/api/doctor?live=false`, and `/studio` responded; 11 showcase screenshots and 3 representative sampled frames were generated under `extra_files/showcase_video_kit/`.
- Failures: Initial Playwright screenshot script was run from the repo root and could not resolve `@playwright/test`; the first raw doctor screenshot was visually weak; the first Gemma proof card rendered unsupported glyphs.
- Fixes attempted: Reran Playwright from `apps/web`, replaced the raw doctor screenshot with a designed proof card, and regenerated the card with ASCII-only text.

### 2026-07-11 00:45
- Command: VPS Docker deployment, internal health checks, and deployed live-provider URL canary.
- Environment: Oracle Ubuntu 22.04 VPS, Docker 29.1.3, Docker Compose 2.40.3, Caddy 2 Alpine, API/web built from source, API credentials from server-only env file.
- Result: pass
- Output summary: Containers `captionman-api-1`, `captionman-web-1`, and `captionman-caddy-1` are running. Internal `http://127.0.0.1/api/health` returned ok, `http://127.0.0.1/studio` returned 200, and `http://127.0.0.1/api/doctor?live=false` reported `fireworks_direct`, `official_mode=true`, Kimi/GLM champion route, and Gemma configured but inactive. A deployed real-provider URL run for the v2 kitten clip completed and produced grounded formal, sarcastic, humorous tech, and humorous non-tech captions. After DNS/ingress were added, public DNS resolved, public TCP 80/443 passed, Caddy obtained a Let's Encrypt certificate, public HTTPS health and doctor checks passed, and a browser smoke test loaded `https://captionman.grimnej.com/studio`.
- Failures: The first API container crashed because the FastAPI route assumed a local `repo/apps/api` path shape; public IP checks to TCP 80/443 initially timed out from outside the VPS; Caddy initially could not issue the `captionman.grimnej.com` certificate before DNS existed.
- Fixes attempted: Patched route root resolution for `/app` container layout, rebuilt the API container, opened and persisted Ubuntu iptables rules for TCP 80/443, added Oracle Cloud ingress and DNS, restarted Caddy, and verified certificate issuance plus public HTTPS.

### 2026-07-11 01:35
- Command: `pnpm --filter web test`; targeted `pnpm --filter web exec biome check ...`; `pnpm --filter web build`
- Environment: Windows PowerShell, Node v24.14.0, pnpm 11.7.0, Next.js 15.5.20.
- Result: pass
- Output summary: Web tests passed with 2 files and 5 tests. Targeted Biome check passed on the files touched by the Judge Verdict fix. Production `next build` completed and marked `/runs/[runId]` as dynamic server-rendered content. The VPS web container was rebuilt and restarted. Public verification for `https://captionman.grimnej.com/runs/run_1783712063_ed14b152` returned 200, contained the real screen/keyboard caption, and did not contain the previous kitchen/chef placeholder wording. Browser smoke verification passed and saved `output/playwright/captionman-live-verdict-real-run.png`.
- Failures: Full `pnpm --filter web lint` still fails on pre-existing CRLF formatting diagnostics across unrelated web files.
- Fixes attempted: Added `getApiBase()` with server/client-aware URL resolution, configured VPS web runtime with `API_INTERNAL_BASE_URL=http://api:8000`, removed silent mock fallback for real run artifact failures, added regression tests, and removed static demo wording from real verdict components.
