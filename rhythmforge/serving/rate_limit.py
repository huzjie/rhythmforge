# -*- coding: utf-8 -*-
"""Simple in-memory sliding-window rate limiter."""
from __future__ import annotations

import time
from collections import deque


class RateLimiter:
    def __init__(self, limit: int = 60, window: float = 60.0):
        self.limit = limit
        self.window = window
        self._hits = deque()

    def allow(self) -> bool:
        now = time.monotonic()
        while self._hits and now - self._hits[0] > self.window:
            self._hits.popleft()
        if len(self._hits) >= self.limit:
            return False
        self._hits.append(now)
        return True
