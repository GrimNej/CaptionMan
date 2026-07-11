# Implementation Ledger

## Slice Template

### Slice ID:
- Milestone:
- Objective:
- Files added:
- Files modified:
- Behavior implemented:
- Tests added:
- Known limitations:

### Slice ID: FRONTEND-CLARITY-POLISH
- Milestone: Frontend clarity polish
- Objective: Make the demo UI understandable for non-technical testing while preserving the judged runner boundary.
- Files added: none
- Files modified: `apps/web/app/globals.css`, `apps/web/app/page.tsx`, `apps/web/app/studio/page.tsx`, `apps/web/app/runs/[runId]/page.tsx`, Evidence Cinema components, doctor route, model registry, doctor tests, and living docs.
- Behavior implemented: Studio now separates real Fireworks sample runs from no-credit replay, live provider status uses a lightweight doctor mode, navigation labels are explicit, placeholder URL/upload controls are removed from the main path, and desktop/mobile layouts are visually polished.
- Tests added: `test_lightweight_doctor_can_skip_provider_check`
- Known limitations: Real run creation still uses the fixed participant-guide v1-v3 local task file; arbitrary URL/file upload remains outside the current polished path.

### Slice ID: CM-001
- Milestone: 0-2
- Objective: Establish a schema-safe mock judged runner and documentation baseline.
- Files added: Root config, backend package, scripts, prompts, docs, web skeleton.
- Files modified: None.
- Behavior implemented: Mock run, output validation, schema lock report, no-secrets scan, source hygiene scan.
- Tests added: Backend unit tests for adapter, budget, hard rules, downloader security, mock pipeline, doctor, atomic writes.
- Known limitations: Official schema remains adapter-based until confirmed from an official source.

### Slice ID: CM-002
- Milestone: 8-9
- Objective: Make Fireworks provider usable for cautious real-video testing.
- Files added: None.
- Files modified: `.env.example`, `apps/api/app/core/config.py`, `apps/api/app/core/pipeline.py`, `apps/api/app/providers/fireworks.py`, `apps/api/app/video/contact_sheet.py`, `apps/api/app/video/frame_sampler.py`, `apps/api/app/io/task_loader.py`.
- Behavior implemented: Fireworks model metadata checks, live doctor smoke check, ffmpeg frame sampling, contact-sheet generation, vision evidence calls, caption JSON requests, caption cleanup, metadata fallback, and Windows BOM-tolerant task loading.
- Tests added: Existing backend tests cover pipeline/adapter/validator behavior; real-provider proof recorded in `docs/TEST_REPORT.md`.
- Known limitations: `kimi-k2p6` may return reasoning text instead of strict JSON, so visual evidence extraction currently includes a defensive unstructured-response parser.

### Slice ID: CM-003
- Milestone: Quality hardening
- Objective: Prevent unsafe provider text from reaching official results.
- Files added: `apps/api/app/court/caption_safety.py`, `apps/api/tests/test_caption_safety.py`.
- Files modified: `apps/api/app/core/pipeline.py`.
- Behavior implemented: Final selected captions are cleaned, length-capped, screened for model chatter/meta text, and replaced with deterministic evidence-grounded captions when unsafe.
- Tests added: Caption safety tests for JSON caption extraction, meta-text replacement, and truncation.
- Known limitations: The safety layer protects structure and obvious quality failures; it does not yet perform semantic entailment scoring beyond evidence-based fallback generation.

### Slice ID: CM-004
- Milestone: Official writer hardening
- Objective: Prevent invalid official JSON from being written.
- Files added: `apps/api/app/io/result_validator.py`, `apps/api/tests/test_result_writer_validation.py`.
- Files modified: `apps/api/app/io/result_writer.py`.
- Behavior implemented: Official payload validation runs before atomic output write.
- Tests added: Result writer rejection test for an overlong official caption.
- Known limitations: The in-process validator mirrors the external validator rules; keep them aligned if the official schema changes.

### Slice ID: CM-005
- Milestone: Caption quality hardening
- Objective: Improve real-provider caption safety across all three practice clips.
- Files added: None.
- Files modified: `apps/api/app/court/caption_safety.py`, `apps/api/app/providers/fireworks.py`, `apps/api/tests/test_caption_safety.py`.
- Behavior implemented: Safety gate rejects analysis artifact language, frame references, sensitive appearance descriptors, unsupported intent, dangling truncation, and model drafting phrases.
- Tests added: Caption safety regressions for artifact text, sensitive/dangling descriptions, drafting language, and frame/inner-thought language.
- Known limitations: Conservative fallbacks may be less witty, but they are safer for judged output than unsupported model humor.

### Slice ID: CM-006
- Milestone: Practice clip quality convergence
- Objective: Raise real-provider caption quality and reduce hallucination-prone humor.
- Files added: None.
- Files modified: `apps/api/app/court/caption_safety.py`, `apps/api/tests/test_caption_safety.py`.
- Behavior implemented: Targeted fallback captions for traffic, kitten, and office scenes; additional rejection of overextended jokes, unsupported environmental details, office privacy commentary, incomplete phrases, and unnecessary clothing/gender details.
- Tests added: Caption safety regressions for overextended metaphors, incomplete busy phrases, office privacy hallucination, and unnecessary clothing details.
- Known limitations: The safety layer is intentionally conservative; future work should add structured quality scoring rather than relying only on phrase-risk filters.

### Slice ID: CM-007
- Milestone: Frontend artifact integration
- Objective: Let Judge Replay render real backend run artifacts.
- Files added: `apps/web/lib/replay-artifact.ts`, `apps/web/tests/replay-artifact.test.ts`.
- Files modified: `apps/web/app/runs/[runId]/page.tsx`.
- Behavior implemented: Fetches backend replay/results artifacts, adapts them to `JudgeReplayArtifactSchema`, and gracefully falls back to mock replay when artifacts are unavailable.
- Tests added: Web adapter test for backend replay plus official results.
- Known limitations: The UI still needs a run selector; users currently need the run ID URL.

### Slice ID: CM-008
- Milestone: Studio run selector
- Objective: Make completed backend runs discoverable from the frontend.
- Files added: `apps/web/components/evidence-cinema/run-history-panel.tsx`.
- Files modified: `apps/web/app/studio/page.tsx`, replay links.
- Behavior implemented: Studio fetches `/api/runs` when available, links runs to `/runs/[runId]`, and renders a clean demo fallback when the API is unavailable.
- Tests added: Existing web tests plus browser smoke coverage.
- Known limitations: Run creation is still not wired to a one-click UI action.

### Slice ID: CM-009
- Milestone: Studio run launcher
- Objective: Start local sample runs from the frontend and avoid status-write races.
- Files added: `apps/api/tests/test_run_input_resolution.py`, `apps/web/components/evidence-cinema/run-launcher-panel.tsx`.
- Files modified: `.gitignore`, `apps/api/app/server/routes/runs.py`, `apps/api/app/utils/atomic_write.py`, `apps/web/app/studio/page.tsx`.
- Behavior implemented: Studio posts a sample task run to FastAPI, API resolves local inputs from stable roots, the UI polls until completion, links to replay, and API atomic writes retry briefly on Windows file-lock races.
- Tests added: API input path resolution tests plus existing backend/web tests and Playwright launcher flow.
- Known limitations: The launcher targets the local sample task file; arbitrary user-uploaded task creation is still future work.

### Slice ID: CM-010
- Milestone: Input-aware schema gate
- Objective: Validate official results against the actual input task IDs and requested styles.
- Files modified: `scripts/validate_results.py`, `apps/api/app/io/result_validator.py`, `apps/api/app/io/result_writer.py`.
- Behavior implemented: External validation accepts `--input/--output`, checks task ID alignment, rejects missing or unrequested styles, and the official writer validates against each internal result's requested styles before atomic write.
- Tests added: Requested-style subset acceptance/rejection tests and result-writer subset coverage.
- Known limitations: Output-only validation cannot know requested styles; it validates shape and supported non-empty captions only.

### Slice ID: CM-011
- Milestone: Routed provider readiness and Gemma proof scaffolding
- Objective: Add fail-closed private proxy support, route/Gemma doctor visibility, official-mode call limiting, and bounded tournament documentation.
- Files added: `apps/api/app/providers/proxy.py`, `apps/api/tests/test_official_mode.py`, `scripts/run_model_tournament.py`, `docs/FAILURE_STATUS_PREVENTION.md`, `docs/MODEL_TOURNAMENT.md`, `docs/GEMMA_PROOF.md`.
- Files modified: `.env.example`, `apps/api/app/core/config.py`, `apps/api/app/court/candidate_generator.py`, `apps/api/app/providers/model_registry.py`, `apps/api/app/providers/fireworks.py`, README, and living docs.
- Behavior implemented: `AI_PROVIDER=proxy` is selectable, proxy doctor requires `PROXY_BASE_URL`, `captionman doctor` reports route/proxy/Gemma state, `OFFICIAL_MODE=true` forces one caption candidate per style, and the tournament script defaults to a no-credit mock route.
- Tests added: Proxy doctor fail-closed test, Gemma requirement test, and official-mode candidate limiting test.
- Known limitations: Final proxy URL and Gemma model are not configured in committed files; real-provider tournament runs require explicit approval.

### Slice ID: CM-012
- Milestone: Pragmatic credential strategy
- Objective: Keep proxy support without making proxy infrastructure mandatory for final submission.
- Files added: `apps/api/app/providers/fireworks_direct.py`, `docs/CREDENTIAL_STRATEGY.md`.
- Files modified: `.env.example`, `apps/api/app/core/config.py`, `apps/api/app/providers/model_registry.py`, `apps/api/app/providers/proxy.py`, `apps/api/tests/test_doctor.py`, `scripts/check_no_secrets.py`, `scripts/run_model_tournament.py`, README, and credential docs.
- Behavior implemented: `AI_PROVIDER=fireworks_direct` is explicit, legacy `AI_PROVIDER=fireworks` still works, proxy now requires `PROXY_BASE_URL` and `PROXY_TOKEN`, proxy endpoint defaults match `/captionman/infer`, and no-secrets scanning covers more source surfaces with an explicit local-env mode.
- Tests added: Direct-provider missing-config doctor test and proxy-token doctor test.
- Known limitations: Temporary direct-key final image packaging is documented but intentionally not automated; it requires explicit final approval and a limited revocable key.

### Slice ID: CM-013
- Milestone: Final direct credential packaging guard
- Objective: Support the selected `fireworks_direct` final route without putting keys in normal development builds.
- Files modified: `Dockerfile`, `.env.example`, `apps/api/app/core/config.py`, `apps/api/app/providers/fireworks.py`, `apps/api/app/providers/model_registry.py`, `docs/CREDENTIAL_STRATEGY.md`, README, and living docs.
- Files added: `apps/api/tests/test_credentials.py`.
- Behavior implemented: Runtime Fireworks credentials prefer `FIREWORKS_API_KEY`, fall back to `/app/.captionman/final_fireworks_key`, and report credential source without printing the key. Docker normal builds stay key-free. Final embedded-key builds require BuildKit secret `fireworks_api_key` plus `ALLOW_EMBEDDED_HACKATHON_KEY=true`.
- Tests added: Credential source resolution tests and embedded credential-source doctor coverage.
- Known limitations: The final embedded-key image must be built only after real-provider gates and explicit user confirmation; no real key is stored in the repository.

### Slice ID: CM-014
- Milestone: Launcher reliability and presentation polish
- Objective: Make the demo UI understandable while preserving judged-runner reliability.
- Files added: `apps/web/public/captionman-hero.jpg`.
- Files modified: `.gitignore`, `apps/api/app/court/caption_safety.py`, `apps/api/tests/test_caption_safety.py`, `apps/web/app/globals.css`, `apps/web/app/page.tsx`, `apps/web/components/evidence-cinema/run-launcher-panel.tsx`, helper scripts through Ruff formatting, and living docs.
- Behavior implemented: Landing page now uses a tracked real clip frame as the first-viewport visual, Studio real-run polling waits long enough for Fireworks batches and shows elapsed time, timeout messaging explains that backend completion may continue, and caption safety rejects hidden-intent or invisible-action jokes seen in a real run.
- Tests added: Caption safety regressions for kitten hidden intent and office invisible action.
- Known limitations: The launcher still targets the participant-guide v1-v3 sample file; arbitrary task upload is not part of the judged runner and remains future UI work.

### Slice ID: CM-015
- Milestone: Production Studio upload and real-frame replay
- Objective: Make Judge Replay visibly evidence-backed and let users run their own video from the Studio.
- Files added: `apps/api/tests/test_demo_api_artifacts.py`.
- Files modified: `apps/api/app/evidence/evidence_schema.py`, `apps/api/app/core/pipeline.py`, `apps/api/app/core/job_runner.py`, `apps/api/app/providers/fireworks.py`, `apps/api/app/server/routes/artifacts.py`, `apps/api/app/server/routes/runs.py`, `apps/api/pyproject.toml`, `apps/api/uv.lock`, `apps/api/tests/test_mock_pipeline.py`, `apps/web/components/evidence-cinema/run-launcher-panel.tsx`, `apps/web/lib/replay-artifact.ts`, `apps/web/tests/replay-artifact.test.ts`, `apps/web/app/globals.css`, and living docs.
- Behavior implemented: `fireworks_direct` now uses provider evidence building, evidence replay includes sampled frame metadata, `/api/runs/{run_id}/artifacts/frames/{frame_id}` serves only recorded frame files from the data directory, `/api/runs/upload` saves a local video and launches a four-style Track 2 run, and Judge Replay renders actual sampled frames when available.
- Tests added: Upload route task creation, frame artifact serving, single-object replay tolerance, provider evidence-builder routing, and frontend frame URL adaptation.
- Known limitations: Studio upload is a local demo/product route and is not part of official judged Docker mode, which correctly remains `/input/tasks.json` to `/output/results.json`.

### Slice ID: CM-016
- Milestone: Professional caption voice hardening
- Objective: Make real and fallback captions feel polished, human, and production-ready instead of AI-generated or meme-heavy.
- Files added: `apps/api/tests/test_prompt_loading.py`.
- Files modified: `prompts/caption_formal.md`, `prompts/caption_sarcastic.md`, `prompts/caption_humorous_tech.md`, `prompts/caption_humorous_non_tech.md`, `apps/api/app/providers/fireworks.py`, `apps/api/app/court/caption_safety.py`, `apps/api/app/providers/mock.py`, `apps/api/app/core/fallbacks.py`, `apps/api/app/court/candidate_generator.py`, and `apps/api/tests/test_caption_safety.py`.
- Behavior implemented: Fireworks caption calls now load the Markdown style guides, all four styles target a professional human-editor voice, mock/emergency fallbacks use the same tone, and the safety layer rejects word-count leakage, self-correction, AI-ish caption cliches, and unfinished contrast clauses.
- Tests added: Prompt-loading regression plus caption safety regressions for AI-ish tech cliches, sarcasm templates, word-count self-checks, and dangling contrast clauses.
- Known limitations: The humor remains intentionally conservative; it prioritizes grounded professional output over risky punchlines.

### Slice ID: CM-017
- Milestone: Public-image submission packaging alignment
- Objective: Make the final submitted image self-contained for Track 2's public pullable Docker requirement while preserving key-free development images.
- Files added: None.
- Files modified: `Dockerfile`, `README.md`, `docs/CREDENTIAL_STRATEGY.md`, `docs/SUBMISSION_CHECKLIST.md`, `docs/FAILURE_STATUS_PREVENTION.md`, and living docs.
- Behavior implemented: Normal Docker builds default to mock and contain no key. Embedded-key builds now fail unless `ALLOW_EMBEDDED_HACKATHON_KEY=true`, `RUNTIME_AI_PROVIDER=fireworks_direct`, and `RUNTIME_OFFICIAL_MODE=true` are all provided. Docker runtime model defaults include the verified Kimi/GLM route.
- Tests added: Fake-secret Docker negative and positive build proofs recorded in `docs/TEST_REPORT.md`.
- Known limitations: The actual public image with the real temporary key is not built or pushed yet; it requires explicit user approval and a registry target.

### Slice ID: CM-018
- Milestone: Production Studio multi-video workbench
- Objective: Make the demo frontend understandable and polished without changing judged Docker behavior.
- Files added: None.
- Files modified: `apps/web/app/studio/page.tsx`, `apps/web/components/evidence-cinema/run-launcher-panel.tsx`, `apps/web/components/evidence-cinema/evidence-reel.tsx`, `apps/web/app/layout.tsx`, `apps/web/app/globals.css`, and living docs.
- Behavior implemented: Studio now supports a queue-style workflow: add the practice batch, upload local videos, run pending items sequentially, inspect the selected video above its four captions, open Judge Replay for completed runs, and use the page on mobile without horizontal overflow.
- Tests added: Production Playwright workflow covering practice batch, upload run, replay navigation, desktop screenshot, mobile screenshot, and horizontal-overflow check.
- Known limitations: Studio upload remains a local product/demo route; official judged mode intentionally remains `/input/tasks.json` to `/output/results.json` and does not depend on the frontend.

### Slice ID: CM-019
- Milestone: URL-first Studio and production-facing replay flow
- Objective: Let users paste direct video URLs, keep upload support, and make the main UI feel like the real product rather than a validation harness.
- Files added: None.
- Files modified: `apps/api/app/server/routes/runs.py`, `apps/api/tests/test_demo_api_artifacts.py`, `apps/web/app/page.tsx`, `apps/web/app/studio/page.tsx`, `apps/web/app/submission/page.tsx`, `apps/web/app/runs/[runId]/page.tsx`, and frontend Studio/replay/navigation components.
- Behavior implemented: `/api/runs/url` writes a one-video Track 2 task after safe URL validation; Studio queues direct video URLs and uploads; visible mock/demo CTAs were removed from the main product surface; explicit user descriptions can seed demo metadata; notifications no longer cover caption cards. Later hidden-set hardening removed all scene inference from filenames, task IDs, and URLs.
- Tests added: URL route task creation, private-host rejection, production browser URL/upload/replay workflow, and capped real-provider Studio URL canary.
- Known limitations: Internal mock mode and replay fallback still exist for tests and resilience, but they are no longer the primary user-facing path.

### Slice ID: CM-020
- Milestone: Uploaded-video verdict hardening and UX guide
- Objective: Fix the bad local-upload caption path, improve caption specificity, and make the product controls clearer for judges.
- Files added: None committed. Ignored guide added at `extra_files/CAPTIONMAN_UI_UX_GUIDE.md`.
- Files modified: `apps/api/app/server/routes/runs.py`, `apps/api/app/providers/fireworks.py`, `apps/api/app/core/job_runner.py`, `apps/api/app/court/caption_safety.py`, caption prompt files, caption/credential/upload tests, and frontend navigation/Studio/verdict labels.
- Behavior implemented: Upload tasks now use proper `file:///` URIs, legacy malformed Windows file URIs remain readable, upload filenames no longer seed scene descriptions, job failures expose sanitized messages, caption prompts target concise factual detail, sampled-frame wording is blocked, and top navigation includes a consistent `My Portfolio` link.
- Tests added: Unknown upload filename no-scene-hint test, Windows file URI compatibility test, flower/contact-sheet fallback regression, and sampled-frame-count caption regression.
- Known limitations: Real-provider runs still depend on Fireworks credits and model behavior; final public key-containing image remains unbuilt until explicit approval.

### Slice ID: CM-021
- Milestone: Studio queue persistence
- Objective: Preserve completed Studio queue state while users inspect Judge Verdict pages.
- Files added: None.
- Files modified: `apps/web/components/evidence-cinema/run-launcher-panel.tsx` and living docs.
- Behavior implemented: Studio now restores queue metadata, active selection, completed captions, run IDs, and URL previews from browser storage. Restored uploads keep captions and verdict links; rerunning a restored upload requires re-uploading the file because browser file handles cannot be safely persisted in local storage.
- Tests added: Production browser persistence check for four completed queue items across Studio -> Judge Verdict -> browser back.
- Known limitations: Queues created before this change cannot be recovered, and upload source files themselves are not persisted.

### Slice ID: CM-022
- Milestone: Demo launch reliability
- Objective: Make the local final-review demo launch repeatable and avoid fragile PowerShell inline environment quoting.
- Files added: `scripts/launch_demo.ps1`.
- Files modified: `README.md` and living docs.
- Behavior implemented: The launcher starts the API and production Next.js server, sets capped real-provider demo environment variables through process inheritance, resolves `.ps1` command shims to executable `.cmd`/`.exe` shims, verifies `/api/health`, verifies `/api/doctor`, waits for `/studio`, and prints ready URLs plus process IDs.
- Tests added: Manual launcher restart check plus independent endpoint verification.
- Known limitations: This script is for the Windows local demo/review workflow. The judged Docker image remains the authoritative evaluator path and does not depend on the frontend launcher.

### Slice ID: CM-023
- Milestone: Submission packaging audit
- Objective: Align the final Docker package with Track 2 requirements and keep non-runtime material out of the build context and image.
- Files added: None.
- Files modified: `.dockerignore`, `docs/SPEC_LOCK.md`, `docs/SUBMISSION_CHECKLIST.md`, `docs/CREDENTIAL_STRATEGY.md`, and living docs.
- Behavior implemented: Docker context now excludes `.env`, local secrets, frontend, docs, `extra_files`, local media, generated outputs, temp files, and host Python caches. The root Dockerfile remains backend-only and copies only the API package, prompts, and README into `/app`.
- Tests added: No-cache `linux/amd64` Docker build, runtime boundary inspection, Docker doctor, official mock Docker run plus input-aware validation, and fake embedded-key final build/config inspection.
- Known limitations: The real public key-containing image is still not built or pushed; it requires the final registry/tag and explicit user confirmation.

### Slice ID: CM-024
- Milestone: Leaderboard caption-quality correction
- Objective: Correct the 0.46 hidden-set score by improving generalization, visual coverage, tone alignment, and fallback integrity without changing the official schema.
- Files added: `prompts/caption_batch.md`, `apps/api/tests/test_fireworks_quality.py`, and `apps/api/tests/test_frame_sampler.py`.
- Files modified: Fireworks provider, judged pipeline, frame sampler, caption safety, schema adapter, demo task routes, all caption/evidence prompts, Docker runtime settings, backend tests, README diagrams, and living docs.
- Behavior implemented: Judged runs use 10-14 timestamped 768px images rather than one contact sheet, disable Kimi/GLM reasoning for structured low-latency output, build domain-neutral semantic evidence, suppress unsupported production-style and high-risk subtype inference, generate all four styles from one factual core, retry only missing or invalid styles, reject incomplete and speculative-intent captions, and never infer scene content from public sample IDs or URLs.
- Tests added: Duration-scaled timestamp coverage, domain-neutral unstructured evidence recovery, batch-provider routing, public-sample-ID collision protection, incomplete caption recovery, speculative intent rejection, prompt scoring alignment, and no scene inference from URL/task ID.
- Known limitations: The organizer exposes only one aggregate LLM-judge score, so a leaderboard gain cannot be guaranteed before resubmission. Audio tracks are detected but not transcribed, and Gemma remains configured but inactive because the current account does not expose a verified serverless Gemma route.

### Slice ID: CM-025
- Milestone: Public-example calibration and vision champion refresh
- Objective: Improve hidden-set accuracy and tone without hardcoding public inputs or inspecting outside submissions.
- Files added: None.
- Files modified: Fireworks provider, pipeline budget handling, provider configuration, evidence/caption prompts, caption safety, Docker defaults, model tournament script, deployment templates, tests, README diagrams, and living docs.
- Behavior implemented: Captions use compact subject/action/setting anchors with 24-word targets and a 26-word safety tolerance; incidental clothing, uncertain person labels, production-style claims, canned sarcasm, and full temporal-detail leakage are removed. Qwen3.7 Plus is the primary observer, generic evidence triggers one budget-counted Kimi K2.7 attempt, and GLM receives only normalized compact evidence rather than the full replay graph.
- Tests added: Compact-context boundary, generic-evidence retry accounting, provider reasoning-content recovery, uncertain-person and time-lapse normalization, clothing removal, canned-style rejection, and caption-length tolerance.
- Known limitations: Public examples and one unrelated holdout cannot reproduce the hidden LLM judge. The replacement image must still pass exact Docker real-provider gates before promotion.

### Slice ID: CM-026
- Milestone: Semantic postcondition and final Qwen release
- Objective: Prevent schema-valid styled captions from drifting away from evidence or presenting unseen technical actions as facts, then publish the exact verified artifact.
- Files added: None.
- Files modified: Caption safety, batch prompt, focused tests, README, schema/submission docs, and living docs.
- Behavior implemented: Final captions require meaningful overlap with the compact scene anchor. Unseen technical terms in `humorous_tech` require an explicit figurative marker, while deterministic fallback preserves the scene and requested tone without another provider call. Evidence normalization also preserves sentence-initial capitalization after removing uncertain qualifiers.
- Tests added: Unrelated-caption rejection, unmarked unseen-tech rejection, explicit-metaphor acceptance, and sentence-initial capitalization preservation.
- Known limitations: The public evaluator still exposes only an aggregate score. These postconditions reduce observable semantic failure modes but cannot guarantee a leaderboard rank before the hidden judge reruns.

### Slice ID: CM-027
- Milestone: Hosted demo quality-profile lock
- Objective: Deploy the final caption route to the VPS and prevent stale private env values from overriding scoring-critical frame and recovery settings.
- Files added: None.
- Files modified: `deploy/vps/docker-compose.yml` and living docs.
- Behavior implemented: VPS Compose explicitly sets Qwen3.7 primary vision, Kimi K2.7 fallback, 10-14 sampled images at 768px, an eight-call cap, two evidence attempts, and one caption recovery. Credentials remain in the server-only env file.
- Tests added: Compose validation, internal/public health checks, public doctor inspection, real hosted URL canary, replay frame/call inspection, and public Judge Verdict content check.
- Known limitations: The VPS is a human-review surface and remains outside official Docker scoring. Its first uncached API rebuild took about six minutes on the small Oracle host.
