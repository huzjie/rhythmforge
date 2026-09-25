# -*- coding: utf-8 -*-
"""Millisecond wall-clock timer."""
from __future__ import annotations

import time


class Timer:
    def __init__(self):
        self._start = time.perf_counter()

    def ms(self) -> float:
        return (time.perf_counter() - self._start) * 1000.0

    def reset(self):
        self._start = time.perf_counter()
        return self
