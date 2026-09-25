# -*- coding: utf-8 -*-
"""Optional decision cache keyed by context, for repeated identical states."""
from __future__ import annotations

from collections import OrderedDict


class DecisionCache:
    def __init__(self, capacity: int = 4096):
        self._data = OrderedDict()
        self.capacity = capacity

    def get(self, key: str):
        if key in self._data:
            self._data.move_to_end(key)
            return self._data[key]
        return None

    def put(self, key: str, value):
        self._data[key] = value
        self._data.move_to_end(key)
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def __len__(self):
        return len(self._data)
