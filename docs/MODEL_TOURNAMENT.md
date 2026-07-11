# Model Tournament

## Purpose

Select the champion route with a bounded test, not by preference. The tournament is intentionally small to protect credits and avoid endless experimentation.

## Candidate Routes

| Route | Vision role | Caption role | Repair role | Status |
|---|---|---|---|---|
| `mock_baseline` | deterministic local evidence | mock captions | deterministic cleanup | implemented and used for gates |
| `fireworks_kimi_glm` | `VISION_MODEL` over timestamped images | one `TEXT_MODEL` requested-style batch | per-style `TEXT_MODEL` recovery or deterministic evidence fallback | verified on holdout and v1-v3 direct Fireworks canaries |
| `specialist_vision_gemma_style` | best verified image-capable model | `GEMMA_MODEL` via `fireworks_direct` when doctor verifies it | `GEMMA_MODEL` or deterministic cleanup | blocked on serverless Gemma availability |
| `proxy_champion` | private proxy selected route | private proxy selected route | private proxy selected route | pending proxy deployment |

## Current Evidence

- Mock route passes schema, local tests, and Docker judged mode.
- Direct Fireworks route has validated a non-sample flower holdout plus v1-v3 practice outputs with two logical calls per video in the normal path.
- An unconditional third review call was measured and rejected because it changed none of 16 captions while increasing runtime and spend.
- Gemma specialist route is configured but not active: `accounts/fireworks/models/gemma-4-31b-it` is not serverless on the current account, so `captionman doctor` correctly fails that route.
- Proxy champion route is not active until `PROXY_BASE_URL` is configured and proxy doctor passes.

## Bounded Procedure

1. Run all mock, validator, Docker, source hygiene, and no-secrets gates.
2. Run `python scripts/run_model_tournament.py --routes mock_baseline` as a no-credit script check.
3. Run one canary on `v1` for a candidate route.
4. If `v1` is valid and qualitatively acceptable, run `v1` through `v3`.
5. Score each route on schema validity, runtime, model-call count, caption accuracy, style match, and fallback frequency.
6. Select one champion route and record it in `.env.example`, `docs/DECISIONS.md`, and this file.
7. Stop unless results are poor enough to justify one more bounded comparison.

## Champion

Current champion for safe local gates: `mock_baseline`.

Current real-provider champion: `fireworks_kimi_glm`.

Final public-image credential route: `fireworks_direct` with a temporary limited hackathon-only key after gates and explicit confirmation.
