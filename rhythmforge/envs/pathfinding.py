# -*- coding: utf-8 -*-
"""Weighted grid pathfinding environment (cost-aware decisions)."""
from __future__ import annotations

import random

from .base import DecisionEnv

DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


class PathfindingEnv(DecisionEnv):
    def __init__(self, width=8, height=8, obstacles=None, cost=None):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles or [])
        self.cost = cost or {}
        self.pos = (0, 0)
        self.goal = (width - 1, height - 1)
        self.steps = 0
        self.total_cost = 0.0

    def reset(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.pos = (0, 0)
        self.steps = 0
        self.total_cost = 0.0
        return self._state()

    def _state(self):
        return {"pos": self.pos, "goal": self.goal, "steps": self.steps, "total_cost": self.total_cost}

    def available_actions(self, state=None):
        state = state or self._state()
        x, y = state["pos"]
        out = []
        for a, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.obstacles:
                out.append(a)
        return out

    def step(self, action):
        x, y = self.pos
        dx, dy = DIRS[action]
        self.pos = (x + dx, y + dy)
        self.steps += 1
        c = self.cost.get(self.pos, 1.0)
        self.total_cost += c
        if self.pos == self.goal:
            return self._state(), 10.0, True, {"cause": "goal"}
        return self._state(), -c, False, {"cause": "step"}

    def clone(self):
        c = PathfindingEnv(self.width, self.height, self.obstacles, self.cost)
        c.pos = self.pos
        c.steps = self.steps
        c.total_cost = self.total_cost
        return c
