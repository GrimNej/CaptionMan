from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

PRIVATE_HOSTS = {"localhost", "127.0.0.1", "::1", "0.0.0.0"}


def assert_safe_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("only http and https URLs are allowed")
    host = parsed.hostname
    if not host:
        raise ValueError("URL host is required")
    if host.lower() in PRIVATE_HOSTS:
        raise ValueError("private host is not allowed")
    try:
        ip = ipaddress.ip_address(host)
        if _is_private(ip):
            raise ValueError("private IP is not allowed")
    except ValueError as exc:
        if "private" in str(exc):
            raise
    for result in socket.getaddrinfo(host, None):
        ip = ipaddress.ip_address(result[4][0])
        if _is_private(ip):
            raise ValueError("host resolves to private IP")


def _is_private(ip: ipaddress._BaseAddress) -> bool:
    return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
