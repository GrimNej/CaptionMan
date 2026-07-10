# Architecture

CaptionMan has two surfaces that share one pipeline:

- Judged runner: Dockerized CLI, no frontend dependency, official output only.
- Demo product: FastAPI plus Next.js Judge Replay UI using the same pipeline artifacts.

The schema adapter is the boundary between internal models and official files. Provider calls are budget-controlled and can fall back to deterministic captions when budget or provider state is unsafe.
