# Architecture

CaptionMan has two surfaces that share one pipeline:

- Judged runner: Dockerized CLI, no frontend dependency, official output only.
- Demo product: FastAPI plus Next.js Judge Replay UI using the same pipeline artifacts.

The schema adapter is the boundary between internal models and official files. The real-provider path samples 10-14 timestamped images, asks Kimi for domain-neutral evidence, and asks GLM for all requested tones in one JSON batch so every caption shares the same factual core. Provider calls are budget-controlled; incomplete, meta, or speculative-intent output is recovered per style without adding debug fields to official results.

Task IDs, filenames, and URLs are transport metadata only. They never seed judged scene content or fallback answers.
