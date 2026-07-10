from __future__ import annotations

import secrets
import time


def new_run_id() -> str:
    return f"run_{int(time.time())}_{secrets.token_hex(4)}"
