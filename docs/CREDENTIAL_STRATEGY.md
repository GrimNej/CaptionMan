# Credential Strategy

## Decision

Final packaging route:

- `AI_PROVIDER=fireworks_direct`
- temporary hackathon-only Fireworks key
- key is separate from the normal/main key
- auto top-up disabled
- lowest practical spend or credit limit
- key revoked or rotated immediately after judging

CaptionMan still supports these provider routes:

- `AI_PROVIDER=proxy`
- `AI_PROVIDER=fireworks_direct`

The private proxy is optional and not blocking.

The 2026-07-10 Track 2 guide review plus maintainer clarification confirms that final Track 2 submission needs a publicly pullable Docker image using the project's own API credentials. The official Track 2 runner should not wait for organizer-injected Fireworks credentials.

## Direct Final Route

Local development reads `FIREWORKS_API_KEY` from the environment or `.env`.

Required config:

```env
AI_PROVIDER=fireworks_direct
FIREWORKS_API_KEY=your_key_here
FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1
GEMMA_MODEL=accounts/fireworks/models/gemma-4-31b-it
MODEL_ROUTING_MODE=champion
GEMMA_USAGE_MODE=off
REQUIRE_GEMMA_FOR_SUBMISSION=false
```

Final packaged images may read the temporary embedded key from:

```text
/app/.captionman/final_fireworks_key
```

`FIREWORKS_API_KEY` still takes precedence if it is present at runtime.

## Build Guard

Normal Docker builds do not embed any key.

Final embedded-key builds require both:

```bash
--build-arg ALLOW_EMBEDDED_HACKATHON_KEY=true
--build-arg RUNTIME_AI_PROVIDER=fireworks_direct
--build-arg RUNTIME_OFFICIAL_MODE=true
--secret id=fireworks_api_key,src=<temporary-key-file>
```

The Dockerfile refuses to embed a key unless `ALLOW_EMBEDDED_HACKATHON_KEY=true`, `RUNTIME_AI_PROVIDER=fireworks_direct`, and `RUNTIME_OFFICIAL_MODE=true`. Use `--no-cache` for final packaging validation if you are intentionally testing the negative guard path, because BuildKit may reuse a previous key-free layer.

Final build example:

```bash
docker buildx build \
  --platform linux/amd64 \
  --no-cache \
  --build-arg ALLOW_EMBEDDED_HACKATHON_KEY=true \
  --build-arg RUNTIME_AI_PROVIDER=fireworks_direct \
  --build-arg RUNTIME_OFFICIAL_MODE=true \
  --secret id=fireworks_api_key,src=.data/final-secrets/fireworks_api_key.txt \
  -t <registry>/captionman:latest \
  --push .
```

The `.data/final-secrets/` path is ignored and must never be committed.

## Temporary Key Checklist

- Create a separate provider key for judging.
- Disable auto top-up.
- Set a low spend or credit limit when available.
- Do not use the main personal key.
- Validate the runner before embedding the key.
- Build the key-containing image close to the deadline only.
- Do not push the key-containing image early.
- Do not commit the key, `.env`, or generated secret files.
- Verify the pushed image is public by pulling it from the registry before submitting.
- Revoke or rotate the key after judging.

This is a hackathon fallback, not production secret management.

## Optional Proxy Route

The proxy route remains available but is not blocking. Use it only if deployed, healthy, and canary-tested.

Required config:

```env
AI_PROVIDER=proxy
PROXY_BASE_URL=https://your-proxy-url.example.com
PROXY_TOKEN=your_proxy_token_here
```

The proxy must hold provider credentials server-side, require bearer auth, enforce timeouts and body limits, avoid logging secrets or base64 payloads, and return valid JSON errors.

## Doctor Expectations

`captionman doctor` must clearly report:

- selected `AI_PROVIDER`
- selected model route
- direct Fireworks config present or missing
- proxy config present or missing
- proxy health pass, fail, or skipped
- Gemma configured and active state
- credential source
- whether the current config can run official mode

Mock mode must pass with no credentials. Track 2 must not require `ALLOWED_MODELS`.

## Required Gates Before Embedded-Key Build

1. `validate_results.py` passes.
2. Mock official runner passes.
3. `linux/amd64` Docker smoke test passes.
4. Real-provider `v1` canary passes.
5. `v1`-`v3` real-provider run passes.
6. Repo no-secrets scan passes.
7. Source-hygiene scan passes.
8. README is final.
9. User explicitly confirms final packaging.

Latest pre-final audit status on 2026-07-10:

- Backend tests passed.
- Source hygiene and no-secrets scans passed.
- Normal `linux/amd64` Docker build passed with a tightened context.
- Docker doctor passed.
- Docker official mock run wrote valid `/output/results.json`.
- Fake embedded-key final build passed and reported `embedded_hackathon_key` without using the real key.
- Real final public image is still intentionally unbuilt until the user provides a registry target and explicitly confirms key-containing packaging.

## Secret Gates

Before public repository pushes:

```bash
python scripts/check_no_secrets.py
python scripts/check_source_hygiene.py
```

Before final direct-key image packaging, also run the local env scan intentionally:

```bash
python scripts/check_no_secrets.py --include-local-env
```

If that command flags `.env`, that is expected while a real local key is present. Do not commit or publish those files. Use the result as a reminder to keep local credentials out of the public repo and only package a temporary limited key at the final moment if explicitly approved.

## After Judging

- Revoke or rotate the temporary Fireworks key.
- Delete local secret files.
- Remove or pull down the final key-containing image if possible.
