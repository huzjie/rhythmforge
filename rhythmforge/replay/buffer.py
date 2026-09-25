# -*- coding: utf-8 -*-
"""Replay buffer for offline / online training of the mock backend."""
from __future__ import annotations

import random
from typing import List


class ReplayBuffer:
    def __init__(self, capacity: int = 100000):
        self.capacity = capacity
        self._buf: List[dict] = []

    def push(self, context_key: str, action: str, reward: float):
        self._buf.append({"context_key": context_key, "action": action, "reward": reward})
        if len(self._buf) > self.capacity:
            self._buf = self._buf[-self.capacity:]

    def sample(self, n: int = 32) -> List[dict]:
        n = min(n, len(self._buf))
        return random.sample(self._buf, n)

    def __len__(self):
        return len(self._buf)
