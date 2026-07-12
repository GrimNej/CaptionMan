# Agent Handoff

## Current State

- Current milestone: The FAQ-audited Qwen champion image is published, anonymously pull-verified, and validated on all eight retired Track 2 examples. The hosted replay now serves run-specific frames through the public origin; judged Docker behavior remains independent from the frontend.
- Current branch: `main`
- Last completed task: Audited all nine FAQ pages, validated every retired Track 2 clip on the exact public digest, published a plain single-platform manifest, and deployed/visually verified the hosted replay fixes.
- Final submission reference: `docker.io/grimnej/captionman:submission`
- Immutable digest: `sha256:756a80fa9de66565476b4b50d4b5624e21dc3857483990329f55718e9105fe11`
- Image contract: plain Docker v2 manifest, `linux/amd64`, 277.20 MiB compressed, default command `captionman run --input /input/tasks.json --output /output/results.json`.
- Last passing gates: 83 backend tests; 5 web tests; targeted Biome; production Next.js build; Ruff; no-secrets and source-hygiene scans; key-free Docker boundary/mock checks; exact-image doctor/mock; exact public-digest v1-v8 run in 199.8 seconds; 8 tasks and 32 manually reviewed captions; input-aware validator and artifact scans; anonymous Docker Hub manifest/digest pull; hosted real-provider canary; all 10 public frame endpoints; Playwright with zero browser errors or warnings.
- Environment assumptions: `uv` manages the backend; pnpm is pinned to 11.7.0; Docker Desktop runs the Linux engine. The final image uses the approved temporary embedded hackathon credential because Track 2 does not inject credentials.
- Git state: `.env`, `.data/final-secrets/`, `extra_files/`, generated outputs, presentation work, and local Docker verification data remain ignored. No secret value is committed or documented.

## Next Safest Task

- Re-save or resubmit `docker.io/grimnej/captionman:submission` in the Track 2 Docker field so the evaluator pulls the replacement digest.
- Do not submit the digest form; the platform previously accepted the tag form and scored it.
- Wait for the new leaderboard evaluation before claiming a score improvement. The public contract confirms accuracy and tone judging, but hidden clips and judge outputs are not available locally.
- Keep `https://captionman.grimnej.com/studio` as the hosted demo URL if the submission form still requests one.

## Do Not Forget

- Keep official output debug-free and limited to `task_id` plus requested `captions`.
- Keep frontend work independent from the judged runner.
- Do not add benchmark-specific answers, task-ID scene hints, competitor language, or copied submission material.
- Treat FAQ examples as retired black-box validation only; do not copy their caption text or create URL/hash mappings.
- Do not claim Gemma is active. Doctor currently reports Gemma configured, usage `off`, and active `false`; Qwen3.7 Plus with one counted Kimi K2.7 evidence fallback and GLM 5.2 writing is the verified champion route.
- The scoreboard is authoritative. The prior 0.46 score was from the replaced image, not proof that the new image will reach a particular rank.
- After judging, revoke the temporary Fireworks key, revoke the GitHub token disclosed during setup, delete local secret files, and remove the key-containing image if practical.
