from __future__ import annotations

import re


SECRET_MARKERS = (
    "api_key",
    "apikey",
    "secret",
    "token",
    "password",
    "private key",
    "bearer ",
    "sk-",
)


def has_secret_marker(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in SECRET_MARKERS)


def redact_text(text: str) -> str:
    value = text
    value = re.sub(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*\S+", r"\1=[REDACTED]", value)
    value = re.sub(r"(?i)bearer\s+[a-z0-9._~+/=-]+", "Bearer [REDACTED]", value)
    value = re.sub(r"sk-[A-Za-z0-9_-]+", "sk-[REDACTED]", value)
    return value

