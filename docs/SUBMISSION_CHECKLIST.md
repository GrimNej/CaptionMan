# Submission Checklist

## Final Submission Artifact

- Docker image URL: `docker.io/grimnej/captionman:submission`
- Current manifest digest: `sha256:b0626dc06303c3b711b0e29711b2b485eac6b84b5daef84dd10ebd12af99af2c`
- Public pull verified: yes, with a clean unauthenticated Docker config
- Final image doctor verified: yes
- Final guide practice v1-v3 run verified: yes
- GitHub repository: `https://github.com/GrimNej/CaptionMan`

## Track 2 Requirements

- Submit a publicly pullable Docker image.
- Image must include a `linux/amd64` manifest.
- Container must read `/input/tasks.json` on startup.
- Container must write `/output/results.json` before exiting.
- Output must include every requested style for every clip.
- Track 2 requires no inference log.
- Track 2 does not inject provider credentials or model restrictions; final image uses CaptionMan's temporary hackathon-only Fireworks key.
- Hidden clips are 30 seconds to 2 minutes.
- Maximum runtime is 10 minutes.
- Compressed image must remain under 10 GB.

## Pre-Push Gates

Run from the repository root unless noted.

```powershell
cd apps\api
uv run pytest
cd ..\..
python scripts\check_no_secrets.py
python scripts\check_source_hygiene.py
docker buildx build --no-cache --platform linux/amd64 -t captionman:submission-audit --load .
docker run --rm captionman:submission-audit captionman doctor
docker run --rm -e AI_PROVIDER=mock -e OFFICIAL_MODE=true -v "${PWD}/input:/input" -v "${PWD}/output:/output" captionman:submission-audit
python scripts\validate_results.py --input input/tasks.json --output output/results.json
```

Expected result:

- Backend tests pass.
- No secrets detected.
- Source hygiene passes.
- Docker image reports `amd64 linux`.
- Docker doctor passes.
- Docker judged mock run writes `/output/results.json`.
- Validator passes with input-aware style checking.

## Packaging Boundary Check

The root Dockerfile is backend-only. The final runtime image should contain:

- `/app/app`
- `/app/prompts`
- `/app/README.md`
- `/app/.venv`

It should not contain:

- `.env`
- `extra_files`
- `apps/web`
- `docs`
- `input`
- `output`
- local videos or screenshots
- Python cache files copied from the host

Quick check:

```powershell
docker run --rm --entrypoint sh captionman:submission-audit -c "test ! -e /app/.env && test ! -e /app/extra_files && test ! -e /app/apps && test ! -e /app/docs && echo runtime-boundary-clean"
```

## Final Public Image Build

Only run this after:

- the pre-push gates pass
- the user gives the final registry/image tag
- the user explicitly confirms final key-containing packaging

Use the temporary hackathon-only key file under ignored `.data/final-secrets/`.

```powershell
docker buildx build `
  --platform linux/amd64 `
  --no-cache `
  --build-arg ALLOW_EMBEDDED_HACKATHON_KEY=true `
  --build-arg RUNTIME_AI_PROVIDER=fireworks_direct `
  --build-arg RUNTIME_OFFICIAL_MODE=true `
  --secret id=fireworks_api_key,src=.data/final-secrets/fireworks_api_key.txt `
  -t <public-registry>/<namespace>/captionman:<tag> `
  --push .
```

## Public Pull Verification

After pushing, verify from the public image reference:

```powershell
docker pull --platform linux/amd64 <public-registry>/<namespace>/captionman:<tag>
docker run --rm <public-registry>/<namespace>/captionman:<tag> captionman doctor
docker run --rm -v "${PWD}/input:/input" -v "${PWD}/output:/output" <public-registry>/<namespace>/captionman:<tag>
python scripts\validate_results.py --input input/tasks.json --output output/results.json
```

The final doctor check must report:

- `AI_PROVIDER=fireworks_direct`
- `OFFICIAL_MODE=true`
- credential source `embedded_hackathon_key`
- route `fireworks_kimi_glm`
- Gemma configured but inactive unless a verified serverless Gemma route is later activated

Latest verified digest:

```text
docker.io/grimnej/captionman:submission@sha256:b0626dc06303c3b711b0e29711b2b485eac6b84b5daef84dd10ebd12af99af2c
```

## Submit

Submit the public Docker image URL/tag in the Track 2 submission form. Keep the GitHub repository URL available if the platform asks for supporting material, but the Track 2 runtime artifact is the Docker image.

## After Judging

- Revoke or rotate the temporary Fireworks key.
- Delete local secret files under `.data/final-secrets/`.
- Remove or pull down the key-containing image if possible.
