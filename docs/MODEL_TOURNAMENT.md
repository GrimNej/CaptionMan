# Model Tournament

## Purpose

Select the champion route with a bounded test, not by preference. The tournament is intentionally small to protect credits and avoid endless experimentation.

## Candidate Routes

| Route | Vision role | Caption role | Repair role | Status |
|---|---|---|---|---|
| `mock_baseline` | deterministic local evidence | mock captions | deterministic cleanup | implemented and used for gates |
| `fireworks_kimi_glm` | `VISION_MODEL` over timestamped images | one `TEXT_MODEL` requested-style batch | per-style `TEXT_MODEL` recovery or deterministic evidence fallback | verified on holdout and v1-v3 direct Fireworks canaries |
| `fireworks_qwen37_glm` | Qwen3.7 Plus over timestamped images, then Kimi K2.7 only for failed/generic evidence | GLM 5.2 compact four-style batch | per-style GLM recovery or deterministic evidence fallback | selected champion after bounded public-example and unrelated-holdout comparison |
| `specialist_vision_gemma_style` | best verified image-capable model | `GEMMA_MODEL` via `fireworks_direct` when doctor verifies it | `GEMMA_MODEL` or deterministic cleanup | blocked on serverless Gemma availability |
| `proxy_champion` | private proxy selected route | private proxy selected route | private proxy selected route | pending proxy deployment |

## Current Evidence

- Mock route passes schema, local tests, and Docker judged mode.
- Direct Fireworks route has validated a non-sample flower holdout plus v1-v3 practice outputs with two logical calls per video in the normal path.
- The 2026-07-11 vision tournament compared Kimi K2.6, Qwen3.7 Plus, MiniMax M3, and Kimi K2.7 on the difficult animal example. Qwen3.7 produced the most discriminative evidence in 10.9 seconds with two calls; its full v1-v3 run completed in 46.7 seconds. Qwen also passed the unrelated flower holdout in 19.4 seconds.
- One later Qwen request returned generic evidence. The selected route therefore validates evidence and makes one budget-counted retry through Kimi K2.7 instead of accepting a generic caption or relying on one provider response.
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

Current real-provider champion: `fireworks_qwen37_glm`.

Final public-image credential route: `fireworks_direct` with a temporary limited hackathon-only key after gates and explicit confirmation.
