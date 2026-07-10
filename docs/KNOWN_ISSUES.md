# Known Issues

## Issue Template

### ISSUE-000: Title
- Severity: low | medium | high | blocker
- Area:
- Description:
- Reproduction:
- Current workaround:
- Owner/next step:

### ISSUE-001: Final Embedded-Key Image Not Yet Built
- Severity: medium
- Area: Submission credentials
- Description: The user-approved temporary hackathon-only Fireworks key is present locally in ignored `.env`, but the final public image with an embedded temporary key has not been built or pushed.
- Reproduction: Run the normal Docker image without `FIREWORKS_API_KEY`; it stays key-free by design. The 2026-07-10 fake embedded-key audit proves the final guard path works, but it intentionally did not use the real key.
- Current workaround: Use local `.env` for real-provider canaries and normal key-free Docker images for mock judged gates. Fake-key guard tests have proven the final image will default to `fireworks_direct`, `OFFICIAL_MODE=true`, and `embedded_hackathon_key` when built with the required final args.
- Owner/next step: Build and push the real embedded-key image only after explicit user confirmation and registry target selection, verify clean public pull, then revoke/rotate the key after judging.

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

### ISSUE-004: Fireworks Vision Model May Ignore JSON-Only Prompt
- Severity: medium
- Area: Provider quality
- Description: `kimi-k2p6` is verified as image-capable, but it may return useful reasoning-style observations instead of strict JSON evidence.
- Reproduction: Run the real-provider `v1` sample with debug replay enabled and inspect `uncertainty_notes`.
- Current workaround: Extract concrete visual observations from unstructured model output and fall back to task metadata when the response is unusable.
- Owner/next step: Probe alternative image-capable models only when the credit budget allows.

### ISSUE-005: Gemma Specialist Route Not Serverless On Current Account
- Severity: medium
- Area: Model routing
- Description: `GEMMA_MODEL=accounts/fireworks/models/gemma-4-31b-it` is configured, but Fireworks doctor/model-list evidence shows it is not serverless for this account, so it cannot be the active caption model for the current direct route.
- Reproduction: Set `GEMMA_USAGE_MODE=specialist` and run `uv run captionman doctor`; the caption model check fails closed on `serverless=false`.
- Current workaround: Keep `GEMMA_USAGE_MODE=off` and use the verified `fireworks_kimi_glm` champion route.
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
- Description: The live model can occasionally phrase humor around sampled-frame structure, such as count-based stages or poses, instead of only the video content.
- Reproduction: Run a short time-lapse-style upload and inspect humorous outputs.
- Current workaround: Caption safety now rejects sample-count language and replaces it with evidence-grounded fallbacks.
- Owner/next step: Keep adding regression tests for any new artifact phrasing found during user review.

### ISSUE-008: Restored Uploads Cannot Rerun Without Re-Selecting The File
- Severity: low
- Area: Frontend demo
- Description: Browser storage can restore uploaded-video captions and Judge Verdict links, but it cannot safely persist the original local `File` object across navigation or reloads.
- Reproduction: Upload a local file, complete the run, open Judge Verdict, go back, then try to rerun the restored upload.
- Current workaround: The restored result remains reviewable, and the user can re-upload the source file to run it again.
- Owner/next step: Consider IndexedDB file persistence only if rerunning restored uploads becomes essential.
