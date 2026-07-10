# Agent Handoff

## Current State
- Current milestone: Final public submission image is pushed and verified, the final 10-slide presentation PDF is built and QA-checked, a separate showcase video kit has been prepared, and an Oracle VPS demo stack is running internally behind Caddy. Judged Docker behavior remains independent from the frontend.
- Current branch: `main`
- Last completed task: Deployed the demo stack to the Oracle VPS under `/opt/captionman`, added repeatable non-secret templates under `deploy/vps/`, fixed container path handling for FastAPI run routes, and verified an internal real-provider URL canary.
- Last passing commands: VPS checks: server `docker compose up -d`, internal `curl http://127.0.0.1/api/health`, internal `curl http://127.0.0.1/studio`, internal `curl http://127.0.0.1/api/doctor?live=false`, and v2 kitten URL canary through the deployed API. Local checks: `uv run pytest tests/test_demo_api_artifacts.py tests/test_run_input_resolution.py` from `apps/api`. Showcase checks and final public image checks remain as previously recorded.
- Known failing commands: Root-level `uv run pytest` is not valid because the backend project lives in `apps/api`; run `uv run pytest` from `apps/api`.
- Environment assumptions: `uv` manages CPython 3.13.12 for the backend; `.node-version` requests Node 22, local Node v24.14.0 satisfies `>=22 <25`; pnpm is pinned to 11.7.0. Docker Desktop Linux engine is running. Final public image is `ghcr.io/grimnej/captionman:final` with digest `sha256:138ce0b9828aff1cd65b13143d14962c1d94e2d72e034a630ed691c660c8293c`.
- Git status: Public repo is intentionally one clean root commit. New presentation artifacts live under `presentation/`; the new showcase kit lives under ignored `extra_files/showcase_video_kit/`. Ignored local artifacts include `.env`, `.data/final-secrets/`, `extra_files/`, `.next/`, Playwright screenshots, generated outputs, and `tmp/`.

## Next Safest Task
- Task: User must open Oracle Cloud ingress for TCP 80 and 443 to the VPS and add DNS `A` record `captionman.grimnej.com -> 193.122.147.68`. After that, restart or wait for Caddy to issue TLS, then verify `https://captionman.grimnej.com/studio`. Submit `ghcr.io/grimnej/captionman:final` in the Track 2 Docker image field. VPS demo deployment templates live under `deploy/vps/`; server-side secrets must remain in `/opt/captionman/secrets/api.env`, not Git. After judging, revoke the temporary Fireworks key, revoke the GitHub token pasted during setup, delete local secret files, and remove/pull down the key-containing image if possible.
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
- VPS demo is internally healthy, but public access is blocked until Oracle Cloud ingress and DNS are configured.
