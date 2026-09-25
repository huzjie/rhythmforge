# -*- coding: utf-8 -*-
"""Episodic memory: store past (context, action, outcome) triples."""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, List


class EpisodicMemory:
    def __init__(self, capacity: int = 10000):
        self._entries: "OrderedDict[str, dict]" = OrderedDict()
        self.capacity = capacity

    def store(self, context_key: str, action: str, reward: float, meta: Any = None):
        self._entries[context_key] = {"action": action, "reward": reward, "meta": meta}
        self._entries.move_to_end(context_key)
        while len(self._entries) > self.capacity:
            self._entries.popitem(last=False)

    def recall(self, context_key: str) -> dict:
        return self._entries.get(context_key)

    def recent(self, n: int = 10) -> List[dict]:
        return list(self._entries.values())[-n:]

    def best_action(self, context_key: str) -> str:
        e = self._entries.get(context_key)
        return e["action"] if e else ""

    def __len__(self):
        return len(self._entries)
