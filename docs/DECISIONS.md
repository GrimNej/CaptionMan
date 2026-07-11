# Architecture Decisions

## Decision Template

### ADR-000: Title
- Date:
- Status: proposed | accepted | superseded
- Context:
- Decision:
- Alternatives considered:
- Consequences:

### ADR-001: Adapter-Based Schema Until Official Contract Is Confirmed
- Date: 2026-07-08
- Status: accepted
- Context: The official input/output shape may change or be unavailable during development.
- Decision: Keep internal task/result models stable and translate only through `schema_adapter.py`.
- Alternatives considered: Hardcode a guessed schema directly in the pipeline.
- Consequences: The validator and writer can be updated by changing one adapter layer.

### ADR-002: Mock Provider Is the Default
- Date: 2026-07-08
- Status: accepted
- Context: Submission reliability must not depend on network access or provider credits.
- Decision: Default `AI_PROVIDER=mock` and require `captionman doctor` before Fireworks use.
- Alternatives considered: Make Fireworks the default provider.
- Consequences: Local tests and Docker judged mode remain deterministic.

### ADR-003: Fireworks Uses Verified Serverless Models With Deterministic Fallbacks
- Date: 2026-07-09
- Status: accepted
- Context: The activated Fireworks account exposes `kimi-k2p6` as an image-capable model and `glm-5p2` as a reliable text model. The vision model may return useful reasoning text instead of strict JSON.
- Decision: Use `accounts/fireworks/models/kimi-k2p6` for vision evidence and `accounts/fireworks/models/glm-5p2` for text/judge defaults. Keep live doctor verification and add deterministic cleanup/fallbacks before official output writing.
- Alternatives considered: Rely on raw model JSON compliance; use `gpt-oss-120b` for text; spend more credits probing additional models.
- Consequences: Real-provider runs are budget-capped and schema-safe even when a model returns unstructured or meta text.

### ADR-004: Final Captions Are Sanitized Outside Provider Code
- Date: 2026-07-09
- Status: accepted
- Context: Provider-specific cleanup is not enough; any model can return reasoning text, JSON wrappers, markdown, multiline output, or overlong captions.
- Decision: Add a central `caption_safety` layer after candidate selection and before internal results are finalized.
- Alternatives considered: Trust each provider implementation to clean its own output.
- Consequences: The official writer receives safer captions regardless of provider behavior, and failures degrade to evidence-grounded deterministic captions.

### ADR-005: Official Output Is Validated Before Atomic Write
- Date: 2026-07-09
- Status: accepted
- Context: External validation catches bad files after the fact, but the runner should avoid creating invalid official output in the first place.
- Decision: Validate the adapted official payload inside `write_official_results` before atomic write.
- Alternatives considered: Rely only on `scripts/validate_results.py`.
- Consequences: Invalid official output fails closed and leaves no partially written result file.

### ADR-006: Final Credential Strategy Uses Temporary Direct Key
- Date: 2026-07-09
- Status: accepted
- Context: Track 2 does not inject provider credentials, and the final Docker image must be public.
- Decision: Use `AI_PROVIDER=fireworks_direct` for final packaging with a separate temporary hackathon-only Fireworks key. Proxy remains optional and non-blocking.
- Alternatives considered: Make proxy mandatory; require evaluator-provided Fireworks variables; use mock provider for final scoring; use the user's main provider key.
- Consequences: Official runner reliability is not blocked by proxy infrastructure, but final image packaging must happen only after green gates and explicit confirmation, with strict revocation and no Git exposure.

### ADR-007: Gemma Is A Routed Specialist
- Date: 2026-07-09
- Status: accepted
- Context: Gemma can matter for the partner challenge, but forcing it into every role can hurt Track 2 accuracy and runtime.
- Decision: Represent Gemma in route configuration and doctor output, then activate it for style or repair only after measured canary results support the route.
- Alternatives considered: Gemma-only pipeline; Gemma mention in docs without runtime checks.
- Consequences: Gemma claims remain honest and testable, and the main Track 2 route can still use the strongest verified model per role.

### ADR-008: Use Kimi/GLM As Current Fireworks Champion
- Date: 2026-07-09
- Status: accepted
- Context: The user-approved temporary Fireworks key passed doctor with `kimi-k2p6` and `glm-5p2`. `gemma-4-31b-it` is configured but not serverless on the current account.
- Decision: Keep `GEMMA_MODEL` populated for proof and future activation, but set the active route to `fireworks_kimi_glm` with `GEMMA_USAGE_MODE=off`.
- Alternatives considered: Force Gemma specialist route despite doctor failure; use mock for final; spend more credits probing unverified models.
- Consequences: Track 2 readiness uses verified serverless models, and Gemma is not claimed active until doctor and canaries prove it.

### ADR-009: Frontend May Sell The System, But Not Drive Judged Mode
- Date: 2026-07-09
- Status: accepted
- Context: The public UI should make CaptionMan feel finished and understandable, but the official evaluator only needs the Docker runner, schema, output file, and provider behavior.
- Decision: Keep the Studio and landing page as demonstration and inspection surfaces. The judged Docker runner remains CLI-first, schema-adapter-backed, and independent from Next.js.
- Alternatives considered: Make the frontend the primary submission interface; keep only a minimal technical UI.
- Consequences: The project has a stronger demo without increasing evaluator risk. Any frontend failure should not break `/input/tasks.json` to `/output/results.json` judged execution.

### ADR-010: Caption Voice Is Professional Before Funny
- Date: 2026-07-09
- Status: accepted
- Context: Real canaries showed that raw model humor can sound AI-made, include word-count self-checks, or end mid-thought.
- Decision: Treat every caption style as a professional public-demo caption first. Formal stays editorial; sarcastic and humorous styles can be lightly witty, but must remain grounded, complete, and human.
- Alternatives considered: Let the model improvise more aggressively; rely only on post-generation cleanup; make all styles purely deterministic.
- Consequences: Captions are safer and more polished for judging. Some humor may be less wild, but official output is less likely to contain model chatter, hallucinated jokes, or unprofessional phrasing.

### ADR-011: Final Public Image Is Self-Contained
- Date: 2026-07-09
- Status: accepted
- Context: Track 2 submission guidance requires a publicly pullable Docker image that uses the project's own API credentials.
- Decision: Keep normal Docker images key-free and mock-default, but require final embedded-key images to set `AI_PROVIDER=fireworks_direct`, `OFFICIAL_MODE=true`, and the verified model route at build time.
- Alternatives considered: Require evaluator runtime environment variables; publish a mock-default image with an embedded key; make the private proxy mandatory.
- Consequences: The final submitted image can run without credential injection, while local development and normal Docker smoke tests remain safe and deterministic.

### ADR-012: Studio Is URL-First
- Date: 2026-07-10
- Status: accepted
- Context: Judges and reviewers are most likely to test with direct clip URLs or a local upload, and the main UI should not foreground validation-only artifacts.
- Decision: Make direct video URL submission the first Studio path, keep upload as a parallel path, and expose Judge Replay from completed runs rather than a standalone synthetic CTA.
- Alternatives considered: Keep a sample-batch-first workflow; require only file uploads; remove replay from the UI.
- Consequences: The product flow is simpler and closer to the judged input model while still showcasing the evidence/replay differentiator.

### ADR-013: Uploaded Filenames Are Not Scene Evidence
- Date: 2026-07-10
- Status: accepted
- Context: A local upload named `348656_medium.mp4` produced fake fallback wording derived from the filename.
- Decision: Filenames, task IDs, and URLs must not become scene descriptions. Only explicit user-provided scene hints may seed fallback evidence; judged runs rely on visual analysis.
- Alternatives considered: Keep deriving readable labels from filenames; require users to always provide scene hints.
- Consequences: Uploads rely on visual evidence first and fail more conservatively instead of inventing captions from filenames.

### ADR-014: Judge Verdict Is The User-Facing Replay Name
- Date: 2026-07-10
- Status: accepted
- Context: `Replay` was accurate internally but unclear to a first-time judge or user.
- Decision: Use `Open Judge Verdict` for the completed-run action and reserve Docker/submission language for packaging readiness.
- Alternatives considered: Keep `Open replay`; rename the whole feature to Submission.
- Consequences: Users can better understand that the post-run page explains evidence, repair, and final caption selection.

### ADR-015: Final Demo Launch Uses A Checked-In Script
- Date: 2026-07-10
- Status: accepted
- Context: Manual PowerShell launch commands can fail on small quoting or shim-resolution details, especially when setting comma-separated environment values like CORS origins.
- Decision: Use `scripts\launch_demo.ps1` for the Windows final-review demo path. The script owns environment setup, service startup, health checks, doctor checks, and ready URL reporting.
- Alternatives considered: Keep ad hoc terminal commands; use Docker Compose for the demo UI; require users to manually start API and web processes.
- Consequences: Local demo startup is more repeatable and easier to explain, while judged Docker mode remains CLI-first and independent from the frontend.

### ADR-016: Hidden-Set Quality Uses Multi-Image Evidence And One Shared Style Batch
- Date: 2026-07-11
- Status: accepted
- Context: The first scored image reached only 0.46. Audit evidence showed six video frames collapsed into a low-resolution contact sheet, one separate text call per style, broad safety phrase bans, sample-ID scene hints, and sample-specific fallback captions. A non-sample flower run also emitted an incomplete sarcastic fragment that passed schema validation.
- Decision: Remove every sample-derived scene hint and answer fallback. Send 10-14 individually compressed, timestamped images to Kimi with reasoning disabled, build domain-neutral semantic evidence, and ask GLM for all requested tones in one scoring-aligned JSON batch. Production aesthetics are omitted unless unmistakable and essential; uncertain computer and building-use subtypes are normalized to accurate parent categories. Reject structurally incomplete, meta, or speculative-intent drafts and recover only the affected style.
- Alternatives considered: Tune only the old per-style prompts; add an unconditional GLM review call; compare outputs with competitor submissions; activate an unverified Gemma route.
- Consequences: Normal real-provider execution drops from five logical calls to two, temporal and visual detail increase, all styles share one factual core, and hidden clips no longer inherit public-sample assumptions. A trial review call was rejected because it changed none of 16 measured captions while adding latency and cost.

### ADR-017: Qwen Primary Vision With Counted Kimi Fallback
- Date: 2026-07-11
- Status: accepted
- Context: The public-example calibration showed that compact subject/action/setting anchors score more directly against the published accuracy rubric. A bounded serverless tournament found Qwen3.7 Plus more specific and faster than the previous Kimi K2.6 route, but one Qwen request returned generic evidence.
- Decision: Use Qwen3.7 Plus as the primary visual observer, validate the semantic evidence before captioning, and spend at most one additional budgeted evidence call on Kimi K2.7 when the primary call fails or remains generic. Pass only compact normalized evidence to GLM 5.2 for four-style writing.
- Alternatives considered: Hardcode the three public descriptions; inspect other submissions; accept generic evidence; keep Kimi K2.6 without retesting; make every video use two vision models.
- Consequences: Normal execution remains two calls, the measured v1-v3 route is faster and semantically sharper, transient vision failures no longer silently become generic captions, and the official call budget accounts for fallback use.

### ADR-018: Final Captions Must Prove Anchor Overlap
- Date: 2026-07-11
- Status: accepted
- Context: A live calibration caption preserved the office scene but stated an unseen code deployment as a literal action. Prompt instructions alone did not guarantee that stylistic additions remained figurative, and schema validation cannot detect semantic drift.
- Decision: Require every final caption to share meaningful terms with the compact evidence anchor. For `humorous_tech`, any technical concept absent from the evidence must be explicitly marked as figurative with `like`, `as if`, or `as though`; otherwise use the evidence-grounded style fallback.
- Alternatives considered: Trust prompt compliance; ban all technical vocabulary; add another model judge; add public-sample-specific rules.
- Consequences: Unrelated captions and literal unseen software claims fail closed without another model call. Some risky jokes become conservative deterministic metaphors, preserving factuality, style presence, latency, and hidden-set generalization.
