# Agent Handoff

## Current State

- Current milestone: The Qwen champion judged image with semantic postconditions is built, real-provider validated, published, and anonymously pull-verified. The human demo remains live at `https://captionman.grimnej.com/studio`; judged Docker behavior remains independent from the frontend.
- Current branch: `main`
- Last completed task: Promoted Qwen3.7 Plus with a counted Kimi K2.7 fallback, added evidence-overlap and figurative-tech final gates, replaced the Docker Hub submission tag, and verified the public artifact end to end.
- Final submission reference: `docker.io/grimnej/captionman:submission`
- Immutable digest: `sha256:0e672ddfcf898971344043be5d29bffa01de132e15e6e929cf84e876608fdfae`
- Image contract: plain Docker v2 manifest, `linux/amd64`, 277.20 MiB compressed, default command `captionman run --input /input/tasks.json --output /output/results.json`.
- Last passing gates: full backend suite with 79 tests; Ruff lint and format checks; no-secrets and source-hygiene scans; exact-image doctor; mounted official mock run; exact-image real v1-v3 run in 56.43 seconds; input-aware validator; manual review of all 12 captions; anonymous Docker Hub manifest inspection and pull; published-digest live doctor and mock run.
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
- Do not claim Gemma is active. Doctor currently reports Gemma configured, usage `off`, and active `false`; Qwen3.7 Plus with one counted Kimi K2.7 evidence fallback and GLM 5.2 writing is the verified champion route.
- The scoreboard is authoritative. The prior 0.46 score was from the replaced image, not proof that the new image will reach a particular rank.
- After judging, revoke the temporary Fireworks key, revoke the GitHub token disclosed during setup, delete local secret files, and remove the key-containing image if practical.
