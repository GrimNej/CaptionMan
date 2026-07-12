# Track 2 Judging FAQ Audit

## Audit Scope

- Source reviewed: `extra_files/AMD Hackathon Judging FAQ and Self-Check Guide.pdf`
- Pages reviewed: all 9 pages, using text extraction and rendered-page inspection
- Track assessed: Track 2, Video Captioning
- Audit date: 2026-07-12

The guide states that its eight videos are retired public validation examples, not final judging inputs. It also states that internal judge prompts and hidden cases are not shared. CaptionMan therefore uses these examples as black-box quality tests only. No task ID, URL, filename, media hash, reference caption, or sample-specific scene mapping is present in the runtime.

## Release Under Audit

- Submission tag: `docker.io/grimnej/captionman:submission`
- Immutable digest: `sha256:756a80fa9de66565476b4b50d4b5624e21dc3857483990329f55718e9105fe11`
- Platform: `linux/amd64`
- Compressed size: 277.20 MiB
- Default command: `captionman run --input /input/tasks.json --output /output/results.json`
- Provider route: Qwen3.7 Plus vision, one counted Kimi K2.7 evidence fallback, GLM 5.2 caption writing

## Track 2 Criteria

| Criterion | Status | Verification |
|---|---|---|
| Accurate captions | Pass | All 32 captions from the eight retired clips were manually checked against sampled source frames. |
| Correct requested style | Pass | Every clip produced four distinct outputs: formal, sarcastic, humorous tech, and humorous non-tech. |
| Specific video details | Pass | Outputs retained discriminative subjects, actions, settings, objects, and stable colors instead of generic video wording. |
| No major hallucinations | Pass | Evidence overlap, speculative-intent filters, figurative-tech checks, subtype normalization, and bounded recovery remain active. |
| Complete clips and styles | Pass | Eight input tasks produced eight results and all 32 requested caption fields. |
| Exact task IDs | Pass | `v1` through `v8` were preserved without rewriting. |
| Valid result schema | Pass | Input-aware `scripts/validate_results.py` completed successfully. |
| Runtime | Pass | Full eight-task Docker run completed in 199.8 seconds against a 600-second limit. |

The FAQ's final style checklist says `non-humorous tech`, but the Track 2 schema declaration and every public example use `humorous_non_tech`. CaptionMan preserves `humorous_non_tech`, which is the actual requested field.

## Submission Self-Check

| FAQ Check | Status | Evidence |
|---|---|---|
| Pull exact image from a clean client | Pass | The immutable digest pulled with a credential-free Docker config. |
| Run without manual setup | Pass | The default command starts automatically; only `/input` and `/output` mounts are needed. |
| Write expected output | Pass | `/output/results.json` is written before successful exit. |
| Validate JSON | Pass | Published-image mock output and real eight-task output both validated. |
| Return every task | Pass | Pipeline fallbacks preserve one output row per input task. |
| Stay under runtime limit | Pass | Eight retired tasks used 33.3% of the limit. |
| Public image and repository | Pass | Docker Hub tag is anonymously pullable and GitHub `main` is public. |

## Failure-Code Prevention

| Failure | Prevention |
|---|---|
| `PULL_ERROR` | Public Docker Hub tag, anonymous manifest and digest pull verification. |
| `RUNTIME_ERROR` | Self-contained dependencies, correct `linux/amd64` command, doctor check, and no frontend dependency. |
| `TIMEOUT` | Bounded frames, sequential tasks, eight-call per-video ceiling, and measured eight-task runtime. |
| `OUTPUT_MISSING` | Atomic official result writing and mounted-output smoke tests. |
| `INVALID_RESULTS_SCHEMA` | Schema adapter, in-process validation, and external input-aware validator. |
| `MISSING_TASKS` | Per-task processing and evidence-grounded fallback rather than silent skips. |
| `ACCURACY_GATE_FAILED` | Multi-frame evidence, compact scene anchors, specific-detail prompts, semantic safety, and public holdout review. |
| `INFRA_ERROR` | Organizer-side condition; repeated resubmission is not used as a workaround. |

## Calibration Decision

The public reference captions demonstrate acceptable tone, but they are not literal target strings. Some use imaginative speculation, mention production framing, or omit visible details. CaptionMan optimizes the guide's explicit criteria instead: factual scene coverage first, recognizable tone second, and no major unsupported claim. This is safer for the separate hidden set than copying reference wording.

## Residual Risks

- The hidden videos and judge prompt remain unavailable, so no rank or score can be guaranteed.
- Fireworks output has bounded variation; up to three unsafe or missing styles can now use targeted recovery while total calls remain capped at eight.
- Audio presence is detected but speech is not transcribed.
- The public image intentionally contains a temporary spend-limited hackathon key and must be removed after judging.
