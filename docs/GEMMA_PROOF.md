# Gemma Proof

## Current Claim

CaptionMan supports Gemma as a routed specialist for style-controlled caption writing and repair when it is configured and verified. The project does not claim Gemma-only or Gemma multimodal behavior by default.

## Runtime Evidence Required

Before making a submission claim about Gemma, collect:

- `captionman doctor` output showing `GEMMA_MODEL` is configured.
- Provider or proxy health check showing the selected Gemma route is reachable.
- A bounded canary result on `v1`.
- Validated `v1` through `v3` results if the canary is acceptable.
- Notes comparing style match, factuality, runtime, and fallback frequency against the current real-provider route.

## Current Status

- `GEMMA_MODEL`: not configured in `.env.example`.
- `GEMMA_USAGE_MODE`: defaults to `off`.
- `REQUIRE_GEMMA_FOR_SUBMISSION`: defaults to `false`.
- `captionman doctor`: reports Gemma configured, active, required, and model fields.

## Activation Rule

Set `GEMMA_USAGE_MODE=specialist` only after `captionman doctor` verifies the Gemma model and the bounded tournament shows that Gemma improves or preserves Track 2 quality for style or repair.
