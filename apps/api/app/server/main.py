from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings
from app.core.job_runner import LocalJobRunner
from app.server.routes import artifacts, doctor, health, runs

settings = Settings()
runner = LocalJobRunner(settings)

api = FastAPI(title="CaptionMan Demo API")
api.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.state.runner = runner


@api.on_event("startup")
def _startup() -> None:
    runner.recover_stale_runs()


api.include_router(health.router, prefix="/api")
api.include_router(doctor.router, prefix="/api")
api.include_router(runs.router, prefix="/api")
api.include_router(artifacts.router, prefix="/api")
