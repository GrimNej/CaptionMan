# Progress Log

## Entry Template

### YYYY-MM-DD HH:MM
- Milestone:
- Summary:
- Files changed:
- Commands run:
- Result:
- Next step:

### 2026-07-08 00:00
- Milestone: 0-1
- Summary: Fresh repository implementation started from final blueprint.
- Files changed: Repository scaffold, backend, scripts, docs, prompts, and frontend skeleton.
- Commands run: Tool version checks.
- Result: In progress.
- Next step: Run sync, tests, validation, hygiene, and Docker mock gates.

### 2026-07-08 23:00
- Milestone: 0-8
- Summary: Implemented mock judged runner, schema adapter, validator, Dockerfile, FastAPI demo API, and minimum Next.js Judge Replay UI.
- Files changed: Root config, `apps/api`, `apps/web`, `packages/shared-schemas`, `docs`, `prompts`, `scripts`.
- Commands run: `uv sync`; `uv run pytest`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run captionman doctor`; `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py output/results.json`; `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`; `pnpm install`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; `uv run captionman schema-lock`; `docker build -t captionman .`.
- Result: All non-Docker gates passed. Docker build blocked because Docker Desktop Linux engine is not running.
- Next step: Start Docker Desktop and rerun Docker judged-mode gates.

### 2026-07-08 23:10
- Milestone: 2
- Summary: Docker judged mode verified after Docker Desktop Linux engine became available.
- Files changed: `docs/PROGRESS.md`, `docs/TEST_REPORT.md`, `docs/AGENT_HANDOFF.md`, `docs/SPEC_LOCK.md`, `docs/KNOWN_ISSUES.md`.
- Commands run: `docker version`; `docker info --format '{{.OSType}} {{.ServerVersion}}'`; `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`; `python scripts/validate_results.py output/results.json`.
- Result: Docker image built, doctor passed, mock judged run passed, and output validation passed.
- Next step: Confirm official schema and configure Fireworks credentials/models for real provider readiness.

### 2026-07-08 23:25
- Milestone: 1.5-2
- Summary: Confirmed Track 2 schema from the participant guide and migrated the runner, validator, docs, and demo schema to official `task_id` plus nested `captions` output.
- Files changed: `.gitignore`, `input/tasks.json`, `apps/api/app/io`, `apps/api/app/core`, `apps/api/tests`, `scripts/validate_results.py`, `apps/web/lib`, `apps/web/components/run`, `apps/web/tests`, `README.md`, `docs/SPEC_LOCK.md`, `docs/OFFICIAL_SCHEMA_NOTES.md`.
- Commands run: `pdftotext`; `uv run captionman schema-lock`; `uv run pytest`; `uv run ruff check .`; `uv run ruff format --check .`; `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py output/results.json`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`; `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`.
- Result: Official Track 2 schema is confirmed and all mock/local/Docker gates passed.
- Next step: Configure real provider credentials and test real video-caption quality.

### 2026-07-08 23:45
- Milestone: Repository discipline
- Summary: Initialized Git and committed the completed work in major slices.
- Files changed: Git history plus living docs.
- Commands run: `git init`; `git status --short --ignored`; `git check-ignore`; `git commit`.
- Result: Three implementation commits created and private/generated files remain ignored.
- Next step: Continue committing after each verified major change.

### 2026-07-09 00:15
- Milestone: Frontend evidence cinema
- Summary: Rebuilt the web frontend around the Judge Replay vertical slice from the revised Evidence Cinema blueprint, with cinematic replay framing, caption court review, repair diff, evidence reel, temporal evidence file, final verdict cards, submission readiness, and official JSON export paths.
- Files changed: `AGENTS.md`, `apps/web/app`, `apps/web/components/layout`, `apps/web/components/evidence-cinema`, `apps/web/lib`, `apps/web/package.json`, `pnpm-lock.yaml`, and living docs.
- Commands run: `pnpm --filter web remove framer-motion`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; Playwright production browser checks and screenshots against `http://localhost:3000/runs/demo`.
- Result: Frontend lint, unit test, production build, resource/console browser check, tab interaction check, and desktop/mobile visual screenshot review passed.
- Next step: Wire the replay UI to real run artifacts once provider-backed video analysis is available.

### 2026-07-09 09:11
- Milestone: Fireworks provider readiness
- Summary: Configured Fireworks defaults, verified account/model readiness, added live doctor checks, implemented frame sampling/contact-sheet evidence generation, and ran one capped real-provider test on `v1`.
- Files changed: `.env.example`, `apps/api/app/core`, `apps/api/app/providers/fireworks.py`, `apps/api/app/video`, `apps/api/app/io/task_loader.py`, and living docs.
- Commands run: `AI_PROVIDER=fireworks uv run captionman doctor`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `AI_PROVIDER=fireworks NUM_FRAMES=4 CAPTION_CANDIDATES_PER_STYLE=1 MAX_MODEL_CALLS_PER_VIDEO=5 uv run captionman run --input ../../.data/manual-fireworks-v1/input.json --output ../../.data/manual-fireworks-v1/results.json --debug-dir ../../.data/manual-fireworks-v1/debug`; `python scripts/validate_results.py .data/manual-fireworks-v1/results.json`.
- Result: Fireworks doctor passed; one real sample run completed with 5 model calls; official output validation passed. Kimi vision did not reliably return JSON, so the provider extracts useful visual observations from unstructured responses and uses task metadata as a final fallback.
- Next step: Run the same capped real-provider path on `v2` and `v3` only when more quality testing is worth the credits.

### 2026-07-09 09:14
- Milestone: Caption safety hardening
- Summary: Added a provider-independent final caption safety layer so selected captions are cleaned, capped, checked for meta/model chatter, and replaced with evidence-grounded deterministic fallbacks when unsafe.
- Files changed: `apps/api/app/court/caption_safety.py`, `apps/api/app/core/pipeline.py`, `apps/api/tests/test_caption_safety.py`, and living docs.
- Commands run: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py output/results.json`.
- Result: 16 backend tests passed and mock judged output validation passed.
- Next step: Extend this same safety approach to score/report caption quality in Judge Replay artifacts.

### 2026-07-09 09:16
- Milestone: Official writer hardening
- Summary: Added in-process validation before official result writes so malformed, overlong, missing, JSON-looking, or markdown-fenced captions fail before any output file is created.
- Files changed: `apps/api/app/io/result_validator.py`, `apps/api/app/io/result_writer.py`, `apps/api/tests/test_result_writer_validation.py`, and living docs.
- Commands run: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py output/results.json`.
- Result: 17 backend tests passed and mock judged output validation passed.
- Next step: Keep final submission using both in-process validation and external `scripts/validate_results.py`.

### 2026-07-09 09:18
- Milestone: Judged-mode regression gate
- Summary: Reran the full final green-flag judged-mode gate set after Fireworks, caption safety, and writer validation hardening.
- Files changed: Living docs only.
- Commands run: `uv run pytest`; `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`; `python scripts/validate_results.py output/results.json`; `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`.
- Result: All final judged-mode gates passed. Docker Desktop Linux engine had to be started first, then Docker build/run succeeded.
- Next step: Continue quality work without breaking judged Docker mode.

### 2026-07-09 09:30
- Milestone: Caption quality safety expansion
- Summary: Ran capped Fireworks checks on `v2` and `v3`, then expanded final caption safety to block analysis artifact language, frame references, sensitive appearance descriptors, unsupported intent, and model drafting language.
- Files changed: `apps/api/app/court/caption_safety.py`, `apps/api/app/providers/fireworks.py`, `apps/api/tests/test_caption_safety.py`, and living docs.
- Commands run: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; capped Fireworks runs for `v2` and `v3`; `python scripts/validate_results.py .data/manual-fireworks-v2/results.json`; `python scripts/validate_results.py .data/manual-fireworks-v3/results.json`; `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py output/results.json`; `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`.
- Result: `v2` and `v3` real-provider outputs validated with 5 model calls each; backend tests increased to 21 passing tests; mock judged output still validates.
- Next step: Rerun Docker judged gates after committing this hardening slice.

### 2026-07-09 09:33
- Milestone: Post-quality Docker regression gate
- Summary: Reran final Docker judged-mode gates after the caption quality safety expansion.
- Files changed: Living docs only.
- Commands run: `uv run pytest`; `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`; `python scripts/validate_results.py output/results.json`; `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`.
- Result: 21 backend tests passed; Docker build, Docker doctor, Docker mock run, official validation, hygiene, and secret scan all passed.
- Next step: Connect validated run artifacts to the Judge Replay UI.

### 2026-07-09 09:51
- Milestone: Practice clip quality convergence
- Summary: Iterated on all three Fireworks practice clips until outputs validated, stayed budget-capped, and avoided artifact language, unsupported intent, unnecessary appearance details, and overextended joke hallucinations.
- Files changed: `apps/api/app/court/caption_safety.py`, `apps/api/tests/test_caption_safety.py`, and living docs.
- Commands run: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; capped Fireworks runs for `v1`, `v2`, and `v3`; `python scripts/validate_results.py .data/manual-fireworks-v1/results.json`; `python scripts/validate_results.py .data/manual-fireworks-v2/results.json`; `python scripts/validate_results.py .data/manual-fireworks-v3/results.json`; `AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py output/results.json`; `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`.
- Result: `v1`, `v2`, and `v3` real-provider outputs all validated at 5 model calls each; backend tests increased to 26 passing tests; Docker judged mode still passed.
- Next step: Feed real validated artifacts into Judge Replay instead of static mock replay data.

### 2026-07-09 09:55
- Milestone: Real artifact Judge Replay adapter
- Summary: Added a web adapter that fetches backend `judge_replay.json` plus official results for a run, transforms them into the Evidence Cinema artifact schema, and falls back to the mock replay if the API artifact is unavailable.
- Files changed: `apps/web/lib/replay-artifact.ts`, `apps/web/app/runs/[runId]/page.tsx`, `apps/web/tests/replay-artifact.test.ts`, and living docs.
- Commands run: `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; Playwright browser smoke check for `http://localhost:3000/runs/demo`.
- Result: Web lint passed, 2 web tests passed, production build passed, and browser smoke check passed with no failed resources or console warnings.
- Next step: Add a run selector in the UI so completed backend runs can be opened from the studio without manually entering the run ID.

### 2026-07-09 09:59
- Milestone: Studio run selector
- Summary: Added a Studio run history panel that lists available backend API runs with direct replay links and falls back cleanly to the demo when the API is offline.
- Files changed: `apps/web/components/evidence-cinema/run-history-panel.tsx`, `apps/web/app/studio/page.tsx`, replay links, and living docs.
- Commands run: `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; Playwright browser smoke check for `http://localhost:3000/studio`.
- Result: Web lint passed, 2 web tests passed, production build passed, and `/studio` browser smoke passed with no failed requests or console warnings.
- Next step: Add a one-click API run launcher for the sample Track 2 tasks.

### 2026-07-09 10:07
- Milestone: Studio run launcher
- Summary: Added a one-click Studio launcher for the local Track 2 sample batch, completion polling before replay links appear, robust API input path resolution, and Windows-safe atomic write retries for API run status updates.
- Files changed: `.gitignore`, `apps/api/app/server/routes/runs.py`, `apps/api/app/utils/atomic_write.py`, `apps/api/tests/test_run_input_resolution.py`, `apps/web/components/evidence-cinema/run-launcher-panel.tsx`, `apps/web/app/studio/page.tsx`, and living docs.
- Commands run: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`; `docker build -t captionman .`; `docker run --rm captionman captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman`; `python scripts/validate_results.py output/results.json`; Playwright launcher flow against local Next.js plus FastAPI mock server.
- Result: 29 backend tests passed, 2 web tests passed, web production build passed, hygiene and secret scans passed, Docker judged mode passed, launcher created a completed API run, and direct replay page loaded backend artifacts.
- Next step: Add arbitrary task creation/upload support or run final capped Fireworks checks against the official input set when available.

### 2026-07-09 10:28
- Milestone: Input-aware schema gate and routed provider readiness
- Summary: Added input-aware official result validation, requested-style enforcement in the writer, `AI_PROVIDER=proxy`, explicit route/Gemma doctor reporting, official-mode candidate limiting, and a bounded model tournament script.
- Files changed: `scripts/validate_results.py`, `scripts/run_model_tournament.py`, `.env.example`, `apps/api/app/io`, `apps/api/app/providers`, `apps/api/app/core/config.py`, `apps/api/app/court/candidate_generator.py`, backend tests, README, and docs.
- Commands run: focused backend tests; `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `uv run captionman doctor`; `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; `python scripts/run_model_tournament.py --routes mock_baseline`; `python -m py_compile scripts/run_model_tournament.py scripts/validate_results.py scripts/check_no_secrets.py scripts/check_source_hygiene.py`; `python scripts/check_source_hygiene.py`; `python scripts/check_no_secrets.py`.
- Result: Validator now supports `--input/--output`, 35 backend tests passed, mock doctor reports routing/proxy/Gemma state, official-mode mock run validated, no-credit tournament route passed, source hygiene passed, and no secrets were detected.
- Next step: Run full backend/Docker gates after the documentation slice is committed, then run proxy or Fireworks canaries only with explicit approval.

### 2026-07-09 10:36
- Milestone: Routed blueprint Docker green gate
- Summary: Re-ran the final Docker path after the routed validation/proxy/Gemma proof slices.
- Files changed: living docs only.
- Commands run: `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`.
- Result: Docker Desktop initially had to be started; after that the linux/amd64 image built, container doctor passed, official-mode mock container wrote `/output/results.json`, and input-aware validation passed.
- Next step: Provide/deploy the private proxy or approve a capped real-provider/Gemma canary.

### 2026-07-09 12:45
- Milestone: Pragmatic credential strategy
- Summary: Updated provider routing so proxy is supported but not mandatory, added explicit `AI_PROVIDER=fireworks_direct`, switched proxy auth to `PROXY_TOKEN`, documented the temporary limited direct-key fallback, and strengthened the secret scan.
- Files changed: `.env.example`, provider config/registry/proxy code, `scripts/check_no_secrets.py`, `scripts/run_model_tournament.py`, README, `docs/CREDENTIAL_STRATEGY.md`, and living docs.
- Commands run: `uv run ruff check app/core/config.py app/providers/model_registry.py app/providers/proxy.py app/providers/fireworks_direct.py tests/test_doctor.py`; `uv run pytest tests/test_doctor.py tests/test_official_mode.py`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `python -m py_compile scripts/check_no_secrets.py scripts/run_model_tournament.py`.
- Result: Focused provider tests passed, default no-secrets scan passed, source hygiene passed, and the scanner now supports explicit local `.env` scanning through `--include-local-env`.
- Next step: Run the full backend/Docker gates with the renamed direct-provider mode and then choose proxy vs temporary direct-key packaging only after canaries.

### 2026-07-09 12:58
- Milestone: Pragmatic credential green gate
- Summary: Re-ran full backend, official mock, no-credit tournament, source scans, and Docker `linux/amd64` gates after adding `fireworks_direct` and `PROXY_TOKEN`.
- Files changed: living docs only.
- Commands run: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; `python scripts/run_model_tournament.py --routes mock_baseline`; `AI_PROVIDER=mock uv run captionman doctor`; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`.
- Result: 37 backend tests passed, source scans passed, official mock run validated, no-credit tournament passed, linux/amd64 Docker image built, container doctor passed, and Docker official-mode mock run validated.
- Next step: Decide final real-provider route: canary-tested proxy if reliable, otherwise user-approved temporary limited direct key.

### 2026-07-09 13:18
- Milestone: Final direct credential packaging guard
- Summary: Implemented the selected final route: `AI_PROVIDER=fireworks_direct` with a temporary hackathon-only key that can be embedded only through an explicit BuildKit secret path and `ALLOW_EMBEDDED_HACKATHON_KEY=true`.
- Files changed: `Dockerfile`, `.env.example`, Fireworks credential resolution, provider doctor reporting, credential tests, `docs/CREDENTIAL_STRATEGY.md`, README, and living docs.
- Commands run: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; `python scripts/run_model_tournament.py --routes mock_baseline`; normal `docker buildx build --platform linux/amd64 -t captionman:test --load .`; Docker doctor/run/validation; fake-secret `captionman:embedded-test` build with `ALLOW_EMBEDDED_HACKATHON_KEY=true`.
- Result: 40 backend tests passed, normal Docker image remained key-free, fake embedded-key image contained the expected ignored fake key file, source scans passed, and Docker official-mode mock validation passed.
- Next step: Run real-provider `v1` canary and `v1`-`v3` only after the temporary hackathon Fireworks key is created and explicitly approved for testing.

### 2026-07-09 13:30
- Milestone: Fireworks direct readiness gate
- Summary: Verified the user-approved temporary Fireworks direct key, populated the local Gemma model field, tested the official Track 2 practice clips from the participant guide, and selected the reliable active route based on doctor evidence.
- Files changed: `.env.example`, `scripts/validate_results.py`, `apps/api/app/providers/model_registry.py`, `apps/api/tests/test_doctor.py`, and living docs.
- Commands run: `uv run captionman doctor`; capped `fireworks_direct` v1 canary; `python scripts/validate_results.py --input .data/manual-fireworks-v1-direct/input.json --output .data/manual-fireworks-v1-direct/results.json`; capped `fireworks_direct` v1-v3 run; `python scripts/validate_results.py --input .data/samples/track2/tasks.local.json --output .data/manual-fireworks-v1-v3-direct/results.json`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`.
- Result: Direct Fireworks doctor passed with `kimi-k2p6` vision and `glm-5p2` caption/judge models; v1 canary and v1-v3 official practice outputs validated; backend reached 41 passing tests; web lint/test/build passed; source hygiene and no-secrets scans passed; normal Docker linux/amd64 judged mode passed. Fireworks reports `accounts/fireworks/models/gemma-4-31b-it` as ready/chat/image-capable but not serverless, so Gemma remains configured but inactive.
- Next step: Do not claim Gemma active unless a serverless Gemma model becomes available and `captionman doctor` passes with it. Final embedded-key image still requires explicit user confirmation after README/final packaging review.

### 2026-07-09 18:10
- Milestone: Frontend clarity polish
- Summary: Reworked the product UI around two unambiguous paths: real Fireworks sample run and no-credit mock replay. Removed misleading placeholder URL/upload controls from the main Studio path, added live lightweight provider status, sharpened the visual system, improved mobile stacking, and clarified navigation labels.
- Files changed: `apps/web/app/globals.css`, `apps/web/app/page.tsx`, `apps/web/app/studio/page.tsx`, `apps/web/app/runs/[runId]/page.tsx`, Evidence Cinema components, `apps/api/app/server/routes/doctor.py`, `apps/api/app/providers/model_registry.py`, and doctor tests.
- Commands run: `uv run pytest tests/test_doctor.py`; `uv run ruff check app/providers/model_registry.py app/server/routes/doctor.py tests/test_doctor.py`; `uv run ruff format --check app/providers/model_registry.py app/server/routes/doctor.py tests/test_doctor.py`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; Playwright screenshots for desktop/mobile Studio and Replay pages.
- Result: Focused backend doctor tests passed with 6 tests, backend lint/format passed, web lint passed, 2 web tests passed, production build passed, and browser screenshots confirmed styled responsive Studio/Replay layouts. UI status now uses `/api/doctor?live=false` so page loads do not trigger the expensive provider verification path.
- Next step: Final README/submission packaging review, then user confirmation before any embedded-key Docker image build.

### 2026-07-09 18:36
- Milestone: Launcher reliability and submission sanity pass
- Summary: Verified official Track 2 constraints from the participant guide and public hackathon pages, fixed the Studio launcher timeout by extending real-run polling to about 11 minutes, added a stronger image-backed landing page, tracked the landing hero asset, and hardened caption safety against unsupported hidden intent/action jokes found in a real run.
- Files changed: `.gitignore`, `apps/api/app/court/caption_safety.py`, `apps/api/tests/test_caption_safety.py`, `apps/web/app/globals.css`, `apps/web/app/page.tsx`, `apps/web/components/evidence-cinema/run-launcher-panel.tsx`, `apps/web/public/captionman-hero.jpg`, formatter-only script updates, and living docs.
- Commands run: `uv run pytest tests/test_caption_safety.py`; `uv run pytest`; `uv run ruff check .`; `uv run ruff format --check .`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; Playwright screenshots for landing and Studio desktop/mobile.
- Result: 44 backend tests passed, 2 web tests passed, frontend production build passed, source hygiene and no-secrets scans passed, local and Docker official-mode mock output validated, and desktop/mobile screenshots showed no overlapping text or stale styling. The prior launcher error was a frontend wait-time limit; the backend run completed and its results validated.
- Next step: Final README/submission packaging review, then explicit user confirmation before any key-containing final image build or push.

### 2026-07-09 19:10
- Milestone: Production Studio upload and real-frame replay
- Summary: Added first-class Studio video upload, persisted uploaded videos as ignored local demo inputs, exposed sampled frame artifacts through safe API routes, rendered real sampled frames in Judge Replay, fixed `fireworks_direct` evidence building, and made replay/status artifact reads BOM-tolerant on Windows.
- Files changed: backend evidence schema, pipeline, Fireworks provider, job runner, FastAPI run/artifact routes, API dependency lock, frontend replay adapter, Studio launcher UI, web tests, backend tests, and living docs.
- Commands run: focused backend upload/artifact tests; `uv run pytest`; `uv run ruff check .`; `uv run ruff format --check .`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; local official mock run and validation; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; Docker doctor; Docker official mock run and validation; Playwright screenshots for Studio upload and real-frame replay; capped real-provider `frame-canary-v1` run.
- Result: 47 backend tests passed, 3 web tests passed, Docker linux/amd64 judged mock path passed, no secrets/source hygiene passed, uploaded-video UI rendered on desktop/mobile, real-frame replay rendered actual sampled video frames, and the single Fireworks canary validated while producing four frame JPEGs.
- Next step: Final README/submission packaging review, then explicit user confirmation before any key-containing final image build or push.

### 2026-07-09 19:45
- Milestone: Professional caption voice hardening
- Summary: Wired the real Fireworks caption provider to the Markdown style guides, rewrote all style prompts around a polished human-editor voice, and expanded the safety layer to reject AI-ish cliches, word-count/self-correction leaks, and unfinished contrast clauses.
- Files changed: `prompts/caption_*.md`, `apps/api/app/providers/fireworks.py`, `apps/api/app/court/caption_safety.py`, `apps/api/app/providers/mock.py`, `apps/api/app/core/fallbacks.py`, `apps/api/app/court/candidate_generator.py`, and caption safety tests.
- Commands run: `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; focused caption safety tests; capped real-provider `frame-canary-v1` runs; input-aware validation of `.data/natural-caption-v1-canary/results.json`; local official mock run and validation; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; `docker run --rm captionman:test captionman doctor`; `docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:test`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`.
- Result: 53 backend tests passed, source hygiene and no-secrets scans passed, local official mock output validated, the final real v1 canary produced professional grounded captions, and Docker linux/amd64 judged mock mode passed after Docker Desktop started.
- Next step: Commit this quality slice, then continue final README/submission packaging review.

### 2026-07-09 20:15
- Milestone: Public-image submission packaging alignment
- Summary: Updated the final Docker packaging path so embedded-key images must default to `AI_PROVIDER=fireworks_direct` and `OFFICIAL_MODE=true`, while normal development images remain key-free and mock-default.
- Files changed: `Dockerfile`, `README.md`, `docs/CREDENTIAL_STRATEGY.md`, `docs/SUBMISSION_CHECKLIST.md`, `docs/FAILURE_STATUS_PREVENTION.md`, and living docs.
- Commands run: focused credential/doctor tests; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; normal `docker buildx build --platform linux/amd64 -t captionman:test --load .`; Docker doctor/run/validation; negative fake-secret embedded build; positive fake-secret embedded build with final runtime args; runtime config inspection without printing secrets.
- Result: Normal image remains `AI_PROVIDER=mock` and key-free. Embedded-key builds fail unless final runtime args are set. The fake embedded final image reports `fireworks_direct`, `OFFICIAL_MODE=true`, `embedded_hackathon_key`, and baked Kimi/GLM model IDs.
- Next step: Commit this packaging correction. Final real key-containing public image still requires explicit user approval, real key secret file, registry target, push, clean public pull verification, and post-judging key revocation.

### 2026-07-10 09:40
- Milestone: Production Studio multi-video workbench
- Summary: Rebuilt Studio into a clear add-video queue with practice batch support, local video upload, sequential run execution, video preview, four-style caption review, replay links, and responsive desktop/mobile layouts.
- Files changed: `apps/web/app/studio/page.tsx`, `apps/web/components/evidence-cinema/run-launcher-panel.tsx`, `apps/web/components/evidence-cinema/evidence-reel.tsx`, `apps/web/app/layout.tsx`, `apps/web/app/globals.css`, and living docs.
- Commands run: `pnpm --filter web lint`; `pnpm --filter web test`; clean `pnpm --filter web build`; production `next start`; Playwright browser workflow for practice batch, upload, replay, and mobile; `uv run pytest` from `apps/api`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; local `AI_PROVIDER=mock` judged run plus `scripts/validate_results.py`.
- Result: Web lint/build passed, web tests passed, API tests passed with 53 tests, browser workflow passed in production mode, mobile layout has no horizontal overflow, no secrets/source hygiene passed, and local judged mock output validated.
- Next step: Docker smoke test still needs Docker Desktop Linux engine running; final public image still needs registry target and explicit approval before any key-containing build/push.

### 2026-07-10 10:10
- Milestone: URL-first Studio and production-facing replay flow
- Summary: Added direct video URL submission to the FastAPI run API, shifted Studio to a URL/file workflow, removed mock/demo CTAs from the main frontend, improved fallback scene hints for known Track 2 clips, and verified a real Fireworks URL run from the UI.
- Files changed: `apps/api/app/server/routes/runs.py`, `apps/api/tests/test_demo_api_artifacts.py`, frontend Studio/navigation/submission/replay components, and living docs.
- Commands run: focused API route tests; full `uv run pytest`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; Playwright URL/upload/replay flow; capped real Fireworks URL run through Studio; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; Docker linux/amd64 build, doctor, official mock run, and validation.
- Result: API tests passed with 55 tests, frontend lint/test/build passed, URL and upload UI flows passed, real Studio URL run produced grounded office-scene captions, no-secrets/source hygiene passed, and Docker judged smoke passed.
- Next step: Keep the real provider server running for user review. Final public image still needs registry target and explicit user approval before building/pushing the embedded-key image.

### 2026-07-10 13:40
- Milestone: Uploaded-video verdict hardening and UX guide
- Summary: Fixed uploaded Windows video URI generation, stopped unknown filenames from becoming fake scene captions, expanded caption prompts and safety fallbacks for richer scene detail, blocked sampled-frame language such as `four stages` or `four poses`, renamed replay actions to Judge Verdict, added a consistent `My Portfolio` nav link, and wrote a user guide under ignored `extra_files/`.
- Files changed: `apps/api/app/server/routes/runs.py`, `apps/api/app/providers/fireworks.py`, `apps/api/app/core/job_runner.py`, `apps/api/app/court/caption_safety.py`, `apps/api/tests/test_caption_safety.py`, `apps/api/tests/test_credentials.py`, `apps/api/tests/test_demo_api_artifacts.py`, `prompts/caption_*.md`, frontend navigation/Studio/verdict labels, and living docs.
- Commands run: focused backend route/credential/caption tests; `uv run pytest`; `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; Playwright upload canary for `E:\Trmp\348656_medium.mp4`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `docker buildx build --platform linux/amd64 -t captionman:test --load .`; Docker doctor; Docker official mock run; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`.
- Result: Backend tests passed with 60 tests, web lint/test/build passed, exact local upload completed through Studio with real Fireworks and opened Judge Verdict, captions no longer leaked filename/contact-sheet/sample-count artifacts, `My Portfolio` linked to `https://grimnej.com`, no-secrets/source hygiene passed, and Docker linux/amd64 judged mock mode passed.
- Next step: User review at `http://localhost:3000/studio`; final public image still needs registry target and explicit user approval before any key-containing build/push.

### 2026-07-10 13:55
- Milestone: Studio queue persistence
- Summary: Persisted Studio queue metadata, active selection, completed captions, and Judge Verdict links in browser storage so users can open a verdict and return without losing the completed queue.
- Files changed: `apps/web/components/evidence-cinema/run-launcher-panel.tsx` and living docs.
- Commands run: `pnpm --filter web lint`; `pnpm --filter web test`; `pnpm --filter web build`; Playwright browser persistence check; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`.
- Result: Four restored completed items survived navigation from Studio to Judge Verdict and back. Restored uploaded files keep captions and verdict links, with rerun disabled until the source file is uploaded again.
- Next step: User review at `http://localhost:3000/studio`; final public image still needs registry target and explicit user approval before any key-containing build/push.

### 2026-07-10 14:10
- Milestone: Demo launch reliability
- Summary: Added a checked-in Windows demo launcher that starts the API and web app without fragile inline PowerShell environment quoting, verifies the correct `/api` routes, and prints ready URLs/process IDs.
- Files changed: `scripts/launch_demo.ps1`, `README.md`, and living docs.
- Commands run: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\launch_demo.ps1 -Restart -SkipOpen`; independent checks for `/api/health`, `/api/doctor?live=false`, and `/studio`.
- Result: Launcher restarted both services successfully with `fireworks_direct`, API health passed, lightweight doctor passed, and Studio returned HTTP 200.
- Next step: Use `scripts\launch_demo.ps1 -Restart` for final local review; final public image still needs registry target and explicit user approval before any key-containing build/push.

### 2026-07-10 14:45
- Milestone: Submission packaging audit
- Summary: Re-read the Track 2 participant guide, confirmed public `linux/amd64` Docker image requirements, tightened Docker context exclusions, and re-ran judged Docker gates.
- Files changed: `.dockerignore`, `docs/SPEC_LOCK.md`, `docs/SUBMISSION_CHECKLIST.md`, `docs/CREDENTIAL_STRATEGY.md`, and living docs.
- Commands run: participant-guide PDF extraction; `uv run pytest`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; `docker buildx build --no-cache --platform linux/amd64 -t captionman:submission-audit --load .`; Docker doctor; runtime boundary checks; Docker official mock run; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; fake embedded-key final build and config inspection.
- Result: Track 2 requirements align with the implementation. The normal image is backend-only, key-free, `linux/amd64`, about 291 MB, writes valid official output, and excludes `.env`, frontend, docs, extra files, local media, and copied host Python caches. The fake embedded-key build confirms final image guard behavior without using the real key.
- Next step: User must provide the public registry/tag and explicitly approve the real temporary-key-containing final build/push.

### 2026-07-10 15:35
- Milestone: Final public submission image
- Summary: Pushed the final Track 2 public image to GHCR, verified public unauthenticated pull, fixed a real dangling-caption regression, rebuilt, repushed, and verified the public image against the guide practice videos.
- Files changed: `apps/api/app/court/caption_safety.py`, `apps/api/tests/test_caption_safety.py`, `input/tasks.json`, and living docs.
- Commands run: `docker push ghcr.io/grimnej/captionman:final`; clean-config public pull; `docker run --rm ghcr.io/grimnej/captionman:final captionman doctor`; public-image v1-v3 practice run; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; caption-safety focused tests; full backend tests; rebuilt and repushed final image.
- Result: Final image `ghcr.io/grimnej/captionman:final` is publicly pullable, `linux/amd64`, official-mode, `fireworks_direct`, embedded temporary hackathon credential, and verified on v1-v3 guide practice tasks. Current manifest digest is `sha256:78c2f4235c779684c608561c0313769c52cdf8f0a96dd40f0e7f37a1410c9b33`.
- Next step: Submit `ghcr.io/grimnej/captionman:final` to the Track 2 Docker image field, then revoke the GitHub token and temporary Fireworks key after judging.

### 2026-07-10 16:20
- Milestone: Final public submission image green flag
- Summary: Re-verified the public GHCR image after several real-output caption quality regressions were fixed and locked with tests.
- Files changed: `apps/api/app/court/caption_safety.py`, `apps/api/tests/test_caption_safety.py`, and living docs.
- Commands run: `uv run pytest`; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; final embedded-key `docker buildx build`; `docker push ghcr.io/grimnej/captionman:final`; clean unauthenticated public pull; `docker run --rm ghcr.io/grimnej/captionman:final captionman doctor`; public-image v1-v3 practice run; `python scripts/validate_results.py --input input/tasks.json --output .data/verify/public-final-output/results.json`; caption artifact scan.
- Result: Final image `ghcr.io/grimnej/captionman:final` is publicly pullable, `linux/amd64`, official-mode, `fireworks_direct`, embedded temporary hackathon credential, and verified on v1-v3 guide practice tasks. Current manifest digest is `sha256:138ce0b9828aff1cd65b13143d14962c1d94e2d72e034a630ed691c660c8293c`.
- Next step: Submit `ghcr.io/grimnej/captionman:final` to the Track 2 Docker image field. After judging, revoke the temporary Fireworks key and the GitHub token, delete local secret files, and remove/pull down the key-containing image if possible.

### 2026-07-10 20:00
- Milestone: Final presentation deck
- Summary: Built the editable Slidev source and final 10-slide CaptionMan Track 2 PDF deck with local assets, local font packages, real product screenshots, real sampled frames, claim traceability, and visual QA documentation.
- Files changed: `presentation/` source tree and generated assets, plus living docs.
- Commands run: `pnpm install` and `pnpm rebuild esbuild sharp playwright-chromium` from `presentation`; `pnpm screenshots`; `pnpm export:pdf`; `pdfinfo CaptionMan_Track2_Presentation.pdf`; `pdftoppm -png -r 144 CaptionMan_Track2_Presentation.pdf rendered/pdf-page`.
- Result: `presentation/CaptionMan_Track2_Presentation.pdf` has exactly 10 pages at 1440 x 810 pt, all ten 1920x1080 slide PNGs were generated, the 5x2 contact sheet was generated, and PDF-rendered pages 1, 4, 6, 9, and 10 were inspected without clipping, missing images, margins, or font fallback issues.
- Next step: Use `presentation/CaptionMan_Track2_Presentation.pdf` for the hackathon presentation package.

### 2026-07-10 20:25
- Milestone: Showcase video kit
- Summary: Launched the local product, verified mock judged mode, checked live doctor routing state, captured a guided screenshot set for the three practice video runs, generated a Gemma routing proof card, and wrote a detailed video narration/showcase guide under ignored `extra_files/`.
- Files changed: `extra_files/showcase_video_kit/` assets and living docs.
- Commands run: `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ../../input/tasks.json --output ../../output/results.json`; `uv run captionman doctor` with mock; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; `AI_PROVIDER=fireworks_direct OFFICIAL_MODE=true uv run captionman doctor`; `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\launch_demo.ps1 -Restart -SkipOpen`; endpoint checks for `/api/health`, `/api/doctor?live=false`, and `/studio`; Playwright screenshot generation from `apps/web`.
- Result: Showcase guide is at `extra_files/showcase_video_kit/SHOWCASE_VIDEO_GUIDE.md` with 11 screenshots and 3 representative sampled frames. Doctor confirms Gemma is configured as the repair model but inactive in the current verified champion route, so the guide includes an accurate Gemma claim line.
- Next step: Use the showcase kit assets to assemble the video presentation.

### 2026-07-11 00:45
- Milestone: VPS demo deployment
- Summary: Added non-secret VPS deployment templates under `deploy/vps/`, installed Docker and Compose on the Oracle VPS, staged CaptionMan in `/opt/captionman`, copied the runtime-only secret env file to `/opt/captionman/secrets/api.env`, built API/web images on the server, and launched API, web, and Caddy containers.
- Files changed: `deploy/vps/`, `apps/api/app/server/routes/runs.py`, and living docs.
- Commands run: server Docker/Compose install; server build/start via `docker compose`; local route tests `uv run pytest tests/test_demo_api_artifacts.py tests/test_run_input_resolution.py`; internal VPS checks for `/api/health`, `/api/doctor?live=false`, `/studio`; live-provider URL canary for the kitten practice clip.
- Result: Public VPS demo is healthy after Oracle Cloud ingress and DNS were configured. `captionman.grimnej.com` resolves to `193.122.147.68`, public TCP 80/443 is reachable, Caddy obtained a Let's Encrypt certificate, public `https://captionman.grimnej.com/api/health` returns ok, public `/api/doctor?live=false` reports `fireworks_direct` with runtime credentials, and public `/studio` returns 200. A Playwright browser smoke test loaded the live Studio and captured `output/playwright/captionman-live-studio.png`.
- Next step: Use `https://captionman.grimnej.com/studio` as the hosted demo URL for the submission, and monitor Fireworks credit usage during judging.

### 2026-07-11 01:35
- Milestone: Live Judge Verdict artifact fix
- Summary: Fixed the deployed web replay route so server-rendered Judge Verdict pages load the real run artifacts through `API_INTERNAL_BASE_URL` instead of silently falling back to the bundled demo replay. Added an explicit verdict-load error state for real run IDs and regression tests that prevent mock fallback for missing artifacts.
- Files changed: `apps/web/lib/api-base.ts`, replay loading code, verdict page, provider/history API calls, `deploy/vps/docker-compose.yml`, and web tests.
- Commands run: `pnpm --filter web test`; targeted `pnpm --filter web exec biome check ...`; `pnpm --filter web build`.
- Result: Local tests and production web build pass. Full `pnpm --filter web lint` still reports pre-existing CRLF formatting issues across unrelated web files, so only touched files were formatted/checked.
- Follow-up: Removed static demo wording from the signature strip and repair diff highlight terms, redeployed the VPS web container, and verified the user's real run `run_1783712063_ed14b152` over public HTTPS. The page now contains the screen/keyboard caption, does not contain the kitchen/chef placeholder wording, and the browser screenshot was saved to `output/playwright/captionman-live-verdict-real-run.png`.
- Next step: Use the live demo URL in the final submission and keep Fireworks usage monitored during judging.

### 2026-07-11 02:10
- Milestone: Public README polish
- Summary: Reworked the README into a professional submission-facing project page with banner/logo branding, live links, accurate Docker/Gemma wording, and four animated SVG diagrams under `SVGs/`.
- Files changed: `README.md`, `.gitignore`, `.dockerignore`, `assets/`, `SVGs/`, and living docs.
- Commands run: SVG XML validation; Playwright direct SVG render screenshots; ASCII scan for README/SVGs; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`.
- Result: README/SVG files are ASCII-safe, SVGs are XML-valid, direct browser render checks found no text outside the viewport, secret scan passed, and source hygiene passed. Changes are intentionally not pushed so the user can review first.
- Next step: User reviews the README and diagrams locally; after approval, commit and push the README asset update.

### 2026-07-11 09:20
- Milestone: Submission Docker reference compatibility
- Summary: Replaced the digest-form submission recommendation with a tag-only, single-platform-compatible GHCR reference after the submission page reported `PULL_ERROR` for the digest reference.
- Files changed: `README.md`, `docs/SUBMISSION_CHECKLIST.md`, `docs/AGENT_HANDOFF.md`, `docs/PROGRESS.md`, and `docs/TEST_REPORT.md`.
- Commands run: Anonymous clean-config pull of `ghcr.io/grimnej/captionman:final`; `docker run --rm ghcr.io/grimnej/captionman:final captionman doctor`; mock official mounted run plus `scripts/validate_results.py`; real-provider v1 canary; real-provider v1-v3 full mounted run; rebuilt and pushed `ghcr.io/grimnej/captionman:submission` with `--platform linux/amd64 --provenance=false --sbom=false`; anonymous clean-config pull of `ghcr.io/grimnej/captionman:submission`; `docker run --rm ghcr.io/grimnej/captionman:submission captionman doctor`; real-provider v1-v3 mounted run plus `scripts/validate_results.py`.
- Result: `ghcr.io/grimnej/captionman:submission` is publicly pullable without credentials, served as a plain Docker v2 manifest, `linux/amd64`, official-mode, `fireworks_direct`, embedded temporary hackathon credential, doctor-verified, and schema-valid on the v1-v3 practice task set in about 94 seconds.
- Next step: Re-save the Track 2 submission with the exact tag-only image reference `ghcr.io/grimnej/captionman:submission`, not a digest reference.

### 2026-07-11 10:15
- Milestone: Docker Hub public fallback
- Summary: Mirrored the exact verified submission image to Docker Hub after the submission platform still could not anonymously pull the GHCR package.
- Files changed: `README.md`, `docs/SUBMISSION_CHECKLIST.md`, `docs/AGENT_HANDOFF.md`, `docs/PROGRESS.md`, and `docs/TEST_REPORT.md`.
- Commands run: Direct anonymous GHCR registry manifest check; `docker tag ghcr.io/grimnej/captionman:submission grimnej/captionman:submission`; `docker push grimnej/captionman:submission`; direct anonymous Docker Hub registry manifest check; `docker manifest inspect docker.io/grimnej/captionman:submission`; `docker pull --platform linux/amd64 docker.io/grimnej/captionman:submission`; `docker run --rm docker.io/grimnej/captionman:submission captionman doctor`; mounted mock official run plus `scripts/validate_results.py`.
- Result: `docker.io/grimnej/captionman:submission` is publicly pullable through Docker Hub, served as a plain Docker v2 manifest, and has the same manifest digest `sha256:b0626dc06303c3b711b0e29711b2b485eac6b84b5daef84dd10ebd12af99af2c` as the verified GHCR image. No model, prompt, runtime, credential, or caption-quality behavior changed.
- Next step: Re-save the Track 2 submission with `docker.io/grimnej/captionman:submission`.

### 2026-07-11 11:55
- Milestone: Hidden-set leaderboard quality correction
- Summary: Audited the official LLM-judge scoring contract after the first successful submission scored 0.46, reproduced a schema-valid but incomplete caption on a non-sample holdout, removed benchmark-specific scene hints/fallbacks, replaced contact-sheet evidence with timestamped multi-image evidence, and changed caption writing to one shared four-style batch with targeted recovery.
- Files changed: Judged pipeline, Fireworks provider, frame sampling, caption safety, schema adapter, demo routes, Docker settings, prompts, backend tests, README diagrams, and living docs.
- Commands run: Participant-guide PDF extraction and page rendering; official event-page scoring audit; Fireworks model capability query; baseline and improved real-provider flower holdouts; two v1-v3 real-provider practice runs; `uv run captionman doctor`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; input-aware result validation; source-hygiene and no-secrets scans.
- Result: Official scoring is confirmed as LLM-judged accuracy plus tone rather than string similarity. Baseline holdout used five calls in 25.6 seconds and emitted an incomplete sarcastic fragment. The corrected path used two calls, produced strict evidence plus four complete styles, passed validation, and ran the v1-v3 practice set in 75.2 seconds. A three-call review experiment was discarded after changing zero of 16 captions while adding latency. Backend finished with 59 passing tests.
- Next step: Build the exact embedded-key `linux/amd64` submission image, run Docker mock and real-provider gates, push the replacement tag, verify anonymous pull, and resubmit the unchanged Docker reference.

### 2026-07-11 12:15
- Milestone: Semantic evidence correction
- Summary: Visually inspected the Docker v1 canary frames and caught an unsupported production-style interpretation: ordinary photographic traffic footage was described as painterly with visible brushstrokes. Tightened evidence and batch prompts to prioritize semantic events and suppress inferred filters, rendering, animation, time-lapse, camera technique, and visual style.
- Files changed: `prompts/evidence_extraction.md`, `prompts/caption_batch.md`, prompt-loading tests, and living docs.
- Commands run: Original-frame visual inspection; focused Ruff and prompt tests; real-provider v1 rerun; input-aware validation; production-style artifact scan.
- Result: The rerun described vehicles, the intersection, traffic signals, trees, and tall buildings; all painterly, brushstroke, rendering, filter, and platform-brand language was absent. Two-call execution and official schema remained intact.
- Next step: Rebuild the exact final image from the semantic prompt commit and repeat Docker gates.
