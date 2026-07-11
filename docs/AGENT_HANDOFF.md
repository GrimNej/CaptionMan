# Agent Handoff

## Current State

- Current milestone: The leaderboard-quality judged image is built, real-provider validated, published, and anonymously pull-verified. The human demo remains live at `https://captionman.grimnej.com/studio`; judged Docker behavior remains independent from the frontend.
- Current branch: `main`
- Last completed task: Replaced the Docker Hub submission tag with the hidden-set-generalized two-call caption pipeline and verified the public artifact end to end.
- Final submission reference: `docker.io/grimnej/captionman:submission`
- Immutable digest: `sha256:c5faf2947724f36e186ba5b03eaa700de91d5fb4328816d6561cacb521966af1`
- Image contract: plain Docker v2 manifest, `linux/amd64`, 277.21 MiB compressed, default command `captionman run --input /input/tasks.json --output /output/results.json`.
- Last passing gates: full backend suite with 62 tests; Ruff lint and format checks; no-secrets and source-hygiene scans; exact-image doctor; mounted official mock run; exact-image real v1-v3 run in 95.06 seconds; input-aware validator; caption quality scans; anonymous Docker Hub manifest inspection and pull; published-image live doctor and mock run.
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
- Do not claim Gemma is active. Doctor currently reports Gemma configured, usage `off`, and active `false`; Kimi K2.6 plus GLM 5.2 is the verified champion route.
- The scoreboard is authoritative. The prior 0.46 score was from the replaced image, not proof that the new image will reach a particular rank.
- After judging, revoke the temporary Fireworks key, revoke the GitHub token disclosed during setup, delete local secret files, and remove the key-containing image if practical.
