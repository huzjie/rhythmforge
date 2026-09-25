# -*- coding: utf-8 -*-
"""Bearer-token auth (constant-time compare)."""
from __future__ import annotations

import hmac


def verify_token(expected: str, header: str) -> bool:
    if not expected:
        return True
    if not header:
        return False
    parts = header.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return False
    return hmac.compare_digest(parts[1].encode(), expected.encode())
