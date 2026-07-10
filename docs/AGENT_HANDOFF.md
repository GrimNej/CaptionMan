# Agent Handoff

## Current State
- Current milestone: Final public submission image is pushed and verified. Judged Docker behavior remains independent from the frontend.
- Current branch: `main`
- Last completed task: Pushed `ghcr.io/grimnej/captionman:final`, verified clean unauthenticated public pull, fixed real public-image caption regressions found during v1-v3 runs, rebuilt/repushed, and verified the public image against the Track 2 guide practice videos.
- Last passing commands: `uv run pytest` from `apps/api` with 71 tests; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`; final embedded-key build and push; clean unauthenticated `docker pull --platform linux/amd64 ghcr.io/grimnej/captionman:final`; `docker run --rm ghcr.io/grimnej/captionman:final captionman doctor`; public-image v1-v3 practice run; `python scripts/validate_results.py --input input/tasks.json --output .data/verify/public-final-output/results.json`; caption artifact scan.
- Known failing commands: Root-level `uv run pytest` is not valid because the backend project lives in `apps/api`; run `uv run pytest` from `apps/api`.
- Environment assumptions: `uv` manages CPython 3.13.12 for the backend; `.node-version` requests Node 22, local Node v24.14.0 satisfies `>=22 <25`; pnpm is pinned to 11.7.0. Docker Desktop Linux engine is running. Final public image is `ghcr.io/grimnej/captionman:final` with digest `sha256:138ce0b9828aff1cd65b13143d14962c1d94e2d72e034a630ed691c660c8293c`.
- Git status: Public repo is intentionally one clean root commit. Ignored local artifacts include `.env`, `.data/final-secrets/`, `extra_files/`, `.next/`, Playwright screenshots, generated outputs, and `tmp/`.

## Next Safest Task
- Task: User should submit `ghcr.io/grimnej/captionman:final` in the Track 2 Docker image field. After judging, revoke the temporary Fireworks key, revoke the GitHub token pasted during setup, delete local secret files, and remove/pull down the key-containing image if possible.
- Files likely involved: no more source files expected unless final submission docs need the final package URL.
- Risks: Real-provider Studio runs spend Fireworks credits; final embedded-key image contains a temporary key by design and must not be built or pushed early; never use the main key; revoke/rotate after judging; Gemma must not be claimed active until doctor and tournament evidence exists.
- Final packaging status: complete and verified at digest `sha256:138ce0b9828aff1cd65b13143d14962c1d94e2d72e034a630ed691c660c8293c`.

## Do Not Forget
- Keep official results debug-free.
- Keep frontend independent from judged runner.
- Do not copy or reference outside project submissions in code, docs, README, screenshots, or branding.
- Run `captionman doctor` with Fireworks credentials before claiming real provider readiness after any model/config change.
- Final public image is already built, pushed, publicly pulled, doctor-verified, and v1-v3 run-verified. Post-judging key revocation remains required.
