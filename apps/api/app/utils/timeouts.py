from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def timeout_scope(_seconds: float) -> Iterator[None]:
    yield
