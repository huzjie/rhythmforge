# -*- coding: utf-8 -*-
"""Survival-space estimator: how much free maneuver room a state leaves."""
from __future__ import annotations

from typing import Any


class SafetyEvaluator:
    """Estimates the "survival space" of a state.

    For snake-like environments, survival space is the number of reachable free
    cells (a crude flood-fill) plus a penalty for being boxed in. Larger is safer.
    """

    def survival(self, state: Any) -> float:
        if state is None:
            return 0.0
        if isinstance(state, dict) and "snake" in state:
            return self._snake_survival(state)
        if isinstance(state, dict) and "pos" in state:
            return self._grid_survival(state)
        return 1.0

    def _snake_survival(self, state):
        w, h = state.get("width", 20), state.get("height", 20)
        snake = set(state.get("snake", []))
        head = state.get("head", (0, 0))
        if not snake:
            return 0.0
        # flood fill from head
        seen = set()
        stack = [head]
        while stack:
            c = stack.pop()
            if c in seen or c in snake:
                continue
            seen.add(c)
            x, y = c
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and (nx, ny) not in snake:
                    stack.append((nx, ny))
        total_free = w * h - len(snake)
        return min(1.0, len(seen) / max(total_free, 1))

    def _grid_survival(self, state):
        w, h = state.get("width", 8), state.get("height", 8)
        return 1.0
