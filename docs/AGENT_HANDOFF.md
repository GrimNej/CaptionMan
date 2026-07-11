# Agent Handoff

## Current State
- Current milestone: Final public submission image is pushed and verified, the final 10-slide presentation PDF is built and QA-checked, a separate showcase video kit has been prepared, the Oracle VPS demo is publicly live at `https://captionman.grimnej.com/studio`, and a polished README/diagram pass is ready for user review but not pushed. Judged Docker behavior remains independent from the frontend.
- Current branch: `main`
- Last completed task: Reworked the README with banner/logo branding and four animated SVG diagrams under `SVGs/`, then validated the diagrams with browser screenshots and repository hygiene scans.
- Last passing commands: SVG XML validation; Playwright direct SVG render screenshots; ASCII scan for README/SVGs; `python scripts/check_no_secrets.py`; `python scripts/check_source_hygiene.py`. Prior passing checks include `pnpm --filter web test`, targeted Biome checks, `pnpm --filter web build`, VPS web rebuild/restart, and public HTML/Playwright checks for the live verdict fix.
- Known failing commands: Root-level `uv run pytest` is not valid because the backend project lives in `apps/api`; run `uv run pytest` from `apps/api`.
- Environment assumptions: `uv` manages CPython 3.13.12 for the backend; `.node-version` requests Node 22, local Node v24.14.0 satisfies `>=22 <25`; pnpm is pinned to 11.7.0. Docker Desktop Linux engine is running. Final submission image is `ghcr.io/grimnej/captionman:submission` with digest `sha256:b0626dc06303c3b711b0e29711b2b485eac6b84b5daef84dd10ebd12af99af2c`.
- Git status: Public repo is intentionally one clean root commit. New presentation artifacts live under `presentation/`; the new showcase kit lives under ignored `extra_files/showcase_video_kit/`. Ignored local artifacts include `.env`, `.data/final-secrets/`, `extra_files/`, `.next/`, Playwright screenshots, generated outputs, and `tmp/`.

## Next Safest Task
- Task: Submit `ghcr.io/grimnej/captionman:submission` in the Track 2 Docker image field and `https://captionman.grimnej.com/studio` as the hosted demo URL. Use the tag-only reference, not the digest reference, because the submission validator requires a tag. VPS demo deployment templates live under `deploy/vps/`; server-side secrets must remain in `/opt/captionman/secrets/api.env`, not Git. After judging, revoke the temporary Fireworks key, revoke the GitHub token pasted during setup, delete local secret files, and remove/pull down the key-containing image if possible.
- Files likely involved: no more source files expected unless final submission docs need the final package URL.
- Risks: Real-provider Studio runs spend Fireworks credits; final embedded-key image contains a temporary key by design and must not be built or pushed early; never use the main key; revoke/rotate after judging; Gemma must not be claimed active until doctor and tournament evidence exists.
- Final packaging status: complete and verified at digest `sha256:b0626dc06303c3b711b0e29711b2b485eac6b84b5daef84dd10ebd12af99af2c`.

## Do Not Forget
- Keep official results debug-free.
- Keep frontend independent from judged runner.
- Do not copy or reference outside project submissions in code, docs, README, screenshots, or branding.
- Run `captionman doctor` with Fireworks credentials before claiming real provider readiness after any model/config change.
- Do not claim Gemma is active in the showcase unless a fresh doctor run reports `gemma.active=true`; the current showcase guide correctly says Gemma is configured as a routed repair specialist but inactive in the verified champion route.
- Final submission image is already built, pushed, publicly pulled, doctor-verified, and v1-v3 run-verified. Post-judging key revocation remains required.
- Final presentation PDF is already built, exactly 10 pages, 16:9, rendered to PNG, contact-sheeted, PDF-rerendered, and documented in `presentation/DECK_QA.md` and `presentation/SOURCES.md`.
- Showcase video kit is under `extra_files/showcase_video_kit/` and includes `SHOWCASE_VIDEO_GUIDE.md`, product screenshots, a Gemma routing proof card, and representative sampled frames.
- VPS demo is publicly healthy over HTTPS. Monitor Fireworks credit usage and shut down or rotate the demo key after judging.
