# Agent Handoff

## Current State
- Current milestone: Final public submission image is pushed and verified, the final 10-slide presentation PDF is built and QA-checked, and a separate showcase video kit has been prepared. Judged Docker behavior remains independent from the frontend.
- Current branch: `main`
- Last completed task: Condensed `extra_files/showcase_video_kit/SHOWCASE_VIDEO_GUIDE.md` into a short screenshot-backed cue sheet with direct bullet points, Gemma wording guardrail, 11 product/proof screenshots, and 3 sampled-frame assets for the three practice videos.
- Last passing commands: Showcase checks: `AI_PROVIDER=mock OFFICIAL_MODE=true uv run captionman run --input ../../input/tasks.json --output ../../output/results.json` from `apps/api`; `python scripts/validate_results.py --input input/tasks.json --output output/results.json`; `uv run captionman doctor` with mock; `AI_PROVIDER=fireworks_direct OFFICIAL_MODE=true uv run captionman doctor`; `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\launch_demo.ps1 -Restart -SkipOpen`; endpoint checks for `/api/health`, `/api/doctor?live=false`, and `/studio`; Playwright screenshot capture from `apps/web`. Prior runtime checks: `uv run pytest` from `apps/api` with 71 tests; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; clean unauthenticated public image pull, doctor, v1-v3 run, and validation.
- Known failing commands: Root-level `uv run pytest` is not valid because the backend project lives in `apps/api`; run `uv run pytest` from `apps/api`.
- Environment assumptions: `uv` manages CPython 3.13.12 for the backend; `.node-version` requests Node 22, local Node v24.14.0 satisfies `>=22 <25`; pnpm is pinned to 11.7.0. Docker Desktop Linux engine is running. Final public image is `ghcr.io/grimnej/captionman:final` with digest `sha256:138ce0b9828aff1cd65b13143d14962c1d94e2d72e034a630ed691c660c8293c`.
- Git status: Public repo is intentionally one clean root commit. New presentation artifacts live under `presentation/`; the new showcase kit lives under ignored `extra_files/showcase_video_kit/`. Ignored local artifacts include `.env`, `.data/final-secrets/`, `extra_files/`, `.next/`, Playwright screenshots, generated outputs, and `tmp/`.

## Next Safest Task
- Task: Use the concise `extra_files/showcase_video_kit/SHOWCASE_VIDEO_GUIDE.md` cue sheet and screenshots to assemble the video presentation; use `presentation/CaptionMan_Track2_Presentation.pdf` for the deck submission/presentation package; submit `ghcr.io/grimnej/captionman:final` in the Track 2 Docker image field. After judging, revoke the temporary Fireworks key, revoke the GitHub token pasted during setup, delete local secret files, and remove/pull down the key-containing image if possible.
- Files likely involved: no more source files expected unless final submission docs need the final package URL.
- Risks: Real-provider Studio runs spend Fireworks credits; final embedded-key image contains a temporary key by design and must not be built or pushed early; never use the main key; revoke/rotate after judging; Gemma must not be claimed active until doctor and tournament evidence exists.
- Final packaging status: complete and verified at digest `sha256:138ce0b9828aff1cd65b13143d14962c1d94e2d72e034a630ed691c660c8293c`.

## Do Not Forget
- Keep official results debug-free.
- Keep frontend independent from judged runner.
- Do not copy or reference outside project submissions in code, docs, README, screenshots, or branding.
- Run `captionman doctor` with Fireworks credentials before claiming real provider readiness after any model/config change.
- Do not claim Gemma is active in the showcase unless a fresh doctor run reports `gemma.active=true`; the current showcase guide correctly says Gemma is configured as a routed repair specialist but inactive in the verified champion route.
- Final public image is already built, pushed, publicly pulled, doctor-verified, and v1-v3 run-verified. Post-judging key revocation remains required.
- Final presentation PDF is already built, exactly 10 pages, 16:9, rendered to PNG, contact-sheeted, PDF-rerendered, and documented in `presentation/DECK_QA.md` and `presentation/SOURCES.md`.
- Showcase video kit is under `extra_files/showcase_video_kit/` and includes `SHOWCASE_VIDEO_GUIDE.md`, product screenshots, a Gemma routing proof card, and representative sampled frames.
