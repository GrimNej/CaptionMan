from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SENSITIVE_KEYS = {"api_key", "key", "token", "signature", "authorization", "x-api-key"}


def redact(value: str) -> str:
    redacted = value
    for key in SENSITIVE_KEYS:
        redacted = redacted.replace(key, f"{key[:2]}***")
    return redacted


def redact_url(url: str) -> str:
    parts = urlsplit(url)
    query = urlencode(
        (key, "[redacted]" if key.lower() in SENSITIVE_KEYS else value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
    )
    return urlunsplit((parts.scheme, parts.netloc, parts.path, query, ""))
