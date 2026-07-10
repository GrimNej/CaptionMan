# Agent Instructions for CaptionMan

Do not build a beautiful landing page first. Build the Judge Replay vertical slice first. The project wins when the flag -> repair -> verdict moment is unforgettable.

You are building CaptionMan, a professional video-captioning system for AMD Developer Hackathon ACT II Track 2.

## Absolute priorities

1. Keep judged Docker mode working.
2. Build in milestone order.
3. Lock official schema before final result writing.
4. Do not let frontend work break CLI mode.
5. Use MockProvider before real providers.
6. Keep model-call budget enforced in code.
7. Keep implementation docs updated.
8. Never commit secrets.
9. Never copy competitor content.
10. Stop and report when a stop rule is hit.

## Non-negotiables

- Use uv for Python.
- Use pnpm for JavaScript.
- Do not use Streamlit.
- Do not use Gradio as the primary UI.
- Do not hardcode API keys.
- Do not commit `.env`.
- Do not include competitor names, copied prompts, copied README text, copied screenshots, copied architecture labels, or copied branding.
- Do not make judged Docker depend on the frontend.
- Do not treat assumed schema as official. Use `schema_adapter.py`.
- Do not claim Gemma support beyond what `captionman doctor` verifies.
- Do not use `pnpm@latest`; pin a tested version.
- Do not use mutable list/dict defaults in Pydantic models.
- Do not log secrets, base64 payloads, provider headers, or signed URLs.
- Do not write debug fields into official judged output.

## Stop rules

Stop and report instead of continuing if:

- Official schema cannot be confirmed and no adapter-based fallback is possible.
- Docker mock run fails after two fix attempts.
- `scripts/validate_results.py` fails after two fix attempts.
- Fireworks provider fails because credits/API access are unavailable.
- A dependency requires paid access.
- A selected model does not support required image input.
- A command would require committing secrets.
- The frontend threatens to change judged runner behavior.
- The repo contains competitor names or copied project language.
- A model/provider cannot be verified by `captionman doctor`.
- A test requires network access when it should use MockProvider.

## Required living docs

Update whenever relevant:

- `docs/PROGRESS.md`
- `docs/DECISIONS.md`
- `docs/IMPLEMENTATION_LEDGER.md`
- `docs/KNOWN_ISSUES.md`
- `docs/TEST_REPORT.md`
- `docs/AGENT_HANDOFF.md`
- `docs/SPEC_LOCK.md`

## Source rules

Use only `docs/SAFE_REFERENCES.md` for tool documentation.

Do not crawl or copy other hackathon submission pages.

The official hackathon page may only be used for track-level constraints.

## Build order

1. Repository skeleton.
2. Validator and mock judged runner.
3. Schema adapter and schema lock.
4. Docker judged mode.
5. Video processing.
6. Evidence File.
7. Budgeted Caption Court.
8. Fireworks provider.
9. Doctor command.
10. FastAPI demo API.
11. Minimum premium frontend.
12. Optional frontend polish.

## Test rule

Before every milestone commit, run the smallest relevant checks.

Before final green-flag milestone, run:

```bash
uv run pytest
docker build -t captionman .
docker run --rm captionman captionman doctor
docker run --rm -e AI_PROVIDER=mock -v "$PWD/input:/input" -v "$PWD/output:/output" captionman
python scripts/validate_results.py output/results.json
python scripts/check_source_hygiene.py
python scripts/check_no_secrets.py
```

## Handoff rule

At the end of every session, update `docs/AGENT_HANDOFF.md`.

Never leave the next agent guessing.
