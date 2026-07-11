# Known Issues

## Issue Template

### ISSUE-000: Title
- Severity: low | medium | high | blocker
- Area:
- Description:
- Reproduction:
- Current workaround:
- Owner/next step:

### ISSUE-001: Public Submission Image Contains A Temporary Embedded Key
- Severity: high
- Area: Submission credentials
- Description: Track 2 injects no credentials, so the approved public submission image intentionally contains a temporary, spend-limited hackathon-only Fireworks key. Repository and normal development images remain key-free.
- Reproduction: Run `captionman doctor` inside the final image without `FIREWORKS_API_KEY`; credential source reports `embedded_hackathon_key`.
- Current workaround: Auto top-up is disabled, the key is separate from the user's main key, and embedding requires the explicit final-build guard. Do not reuse this image or key outside judging.
- Owner/next step: Revoke the temporary Fireworks key immediately after judging, then remove the public key-containing tags where practical.

### ISSUE-002: Fireworks Provider Requires Credentials
- Severity: low
- Area: Provider
- Description: Real Fireworks calls require `FIREWORKS_API_KEY` and compatible model IDs. This is configured for the current local environment, but remains a setup requirement for any new machine or account.
- Reproduction: Run `AI_PROVIDER=fireworks_direct uv run captionman doctor` without credentials.
- Current workaround: Use `AI_PROVIDER=mock` for local and Docker gates.
- Owner/next step: Keep `.env` ignored and rerun doctor when credentials or model IDs change.

### ISSUE-003: Docker Desktop Linux Engine Not Running
- Severity: low
- Area: Docker judged mode
- Description: `docker build -t captionman .` can fail when Docker Desktop's Linux engine is not reachable at `npipe:////./pipe/dockerDesktopLinuxEngine`.
- Reproduction: Run Docker commands while Docker Desktop is stopped.
- Current workaround: Docker Desktop Linux engine was running for the 2026-07-10 submission packaging audit; keep Docker Desktop running for final build/push and public pull verification.
- Owner/next step: Keep Docker Desktop running when executing final Docker gates.

### ISSUE-004: Fireworks Vision Response May Be Empty Or Unstructured
- Severity: low
- Area: Provider quality
- Description: Serverless vision responses can occasionally be empty, generic, or place usable content in a provider reasoning field even when JSON output is requested.
- Reproduction: Run a real-provider task with debug replay and inspect whether `uncertainty_notes` reports an unstructured response.
- Current workaround: Recover provider reasoning content when present, reject generic evidence, and make one budget-counted evidence retry with Kimi K2.7 after Qwen3.7 Plus. The domain-neutral parser remains the final boundary and never uses filenames, task IDs, URLs, or sample descriptions.
- Owner/next step: Keep retry/model-readiness regressions and monitor real runs; do not add benchmark-specific fallback answers.

### ISSUE-005: Gemma Specialist Route Not Serverless On Current Account
- Severity: medium
- Area: Model routing
- Description: `GEMMA_MODEL=accounts/fireworks/models/gemma-4-31b-it` is configured, but Fireworks doctor/model-list evidence shows it is not serverless for this account, so it cannot be the active caption model for the current direct route.
- Reproduction: Set `GEMMA_USAGE_MODE=specialist` and run `uv run captionman doctor`; the caption model check fails closed on `serverless=false`.
- Current workaround: Keep `GEMMA_USAGE_MODE=off` and use the verified `fireworks_qwen37_glm` champion route.
- Owner/next step: Only activate Gemma if a serverless Gemma model becomes available and `captionman doctor` plus bounded canaries pass.

### ISSUE-006: Studio Upload Is Demo-Only, Not Judged Mode
- Severity: low
- Area: Frontend demo
- Description: Studio now supports direct URL and user video upload for the local product experience. Official judged Docker mode still intentionally ignores the frontend and reads `/input/tasks.json`.
- Reproduction: Open `/studio`; direct URL and upload sections create ignored local task files for completed runs.
- Current workaround: None needed for normal use. Use judged Docker mode for final evaluator behavior.
- Owner/next step: Keep upload/demo behavior separate from judged runner behavior.

### ISSUE-007: Real-Provider Humor Can Still Need Safety Repair
- Severity: low
- Area: Caption quality
- Description: Humor can introduce figurative comparisons that are stylistically strong but add unnecessary unsupported specificity.
- Reproduction: Run varied hidden-like videos and inspect whether jokes introduce brands, private intent, profession, or unseen outcomes.
- Current workaround: Batch prompts ban unsupported brands/classifications and private intent; structural safety rejects speculative-intent patterns and regenerates only the affected style.
- Owner/next step: Prefer evidence-preserving prompt changes over broad phrase blacklists or sample-specific canned captions.

### ISSUE-008: Restored Uploads Cannot Rerun Without Re-Selecting The File
- Severity: low
- Area: Frontend demo
- Description: Browser storage can restore uploaded-video captions and Judge Verdict links, but it cannot safely persist the original local `File` object across navigation or reloads.
- Reproduction: Upload a local file, complete the run, open Judge Verdict, go back, then try to rerun the restored upload.
- Current workaround: The restored result remains reviewable, and the user can re-upload the source file to run it again.
- Owner/next step: Consider IndexedDB file persistence only if rerunning restored uploads becomes essential.

### ISSUE-009: Aggregate Leaderboard Score Has No Per-Style Diagnostics
- Severity: medium
- Area: Evaluation
- Description: The public leaderboard exposes only the aggregate Track 2 LLM-judge score, so the exact hidden clip, style, and accuracy-versus-tone losses behind 0.46 are unavailable.
- Reproduction: Inspect the scored leaderboard entry; no per-clip or per-style report is provided.
- Current workaround: Optimize strictly against the published rubric, use non-sample holdouts, remove all sample-derived behavior, validate every output structurally, and compare call/runtime/fallback evidence across bounded canaries.
- Owner/next step: Resubmit the updated public image and use the next aggregate score as the only authoritative external measurement. Do not claim a top-five score before the leaderboard confirms it.
