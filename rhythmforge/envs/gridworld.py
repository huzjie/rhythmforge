# -*- coding: utf-8 -*-
"""Small grid-world navigation environment for planner sanity checks."""
from __future__ import annotations

import random

from .base import DecisionEnv

DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


class GridWorldEnv(DecisionEnv):
    def __init__(self, width=8, height=8, walls=None):
        self.width = width
        self.height = height
        self.walls = set(walls or [])
        self.pos = (0, 0)
        self.goal = (width - 1, height - 1)
        self.steps = 0

    def reset(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.pos = (0, 0)
        self.steps = 0
        return self._state()

    def _state(self):
        return {"pos": self.pos, "goal": self.goal, "steps": self.steps, "width": self.width, "height": self.height}

    def available_actions(self, state=None):
        state = state or self._state()
        x, y = state["pos"]
        out = []
        for a, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.walls:
                out.append(a)
        return out

    def step(self, action):
        x, y = self.pos
        dx, dy = DIRS[action]
        self.pos = (x + dx, y + dy)
        self.steps += 1
        if self.pos == self.goal:
            return self._state(), 10.0, True, {"cause": "goal"}
        return self._state(), -0.01, False, {"cause": "step"}

    def clone(self):
        c = GridWorldEnv(self.width, self.height, self.walls)
        c.pos = self.pos
        c.steps = self.steps
        return c

    def render(self, state=None):
        s = state or self._state()
        gx, gy = s["goal"]
        px, py = s["pos"]
        grid = [["."] * self.width for _ in range(self.height)]
        grid[gy][gx] = "G"
        grid[py][px] = "P"
        return "\n".join("".join(row) for row in grid)
