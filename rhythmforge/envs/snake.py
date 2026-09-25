# -*- coding: utf-8 -*-
"""Classic snake environment — the reference "don't paint yourself into a corner" task.

The score (food eaten) and survival (snake length vs free space) make it a clean
test of lookahead safety: greedy play dies early; a planner that preserves free
space survives thousands of steps (cf. NeoHorse-Jev-4B's 3000-step / 89-goal run).
"""
from __future__ import annotations

import random
from collections import deque

from .base import DecisionEnv

DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}


class SnakeEnv(DecisionEnv):
    def __init__(self, width: int = 20, height: int = 20, max_steps: int = 3000):
        self.width = width
        self.height = height
        self.max_steps = max_steps
        self.snake: deque = deque()
        self.food = (0, 0)
        self.direction = "right"
        self.steps = 0
        self.goals = 0

    def reset(self, seed=None):
        if seed is not None:
            random.seed(seed)
        cx, cy = self.width // 2, self.height // 2
        self.snake = deque([(cx, cy), (cx - 1, cy), (cx - 2, cy)])
        self.direction = "right"
        self.steps = 0
        self.goals = 0
        self._spawn_food()
        return self._state()

    def _state(self):
        return {
            "snake": list(self.snake),
            "head": self.snake[0],
            "food": self.food,
            "direction": self.direction,
            "steps": self.steps,
            "goals": self.goals,
            "length": len(self.snake),
            "width": self.width,
            "height": self.height,
        }

    def _spawn_food(self):
        free = [(x, y) for y in range(self.height) for x in range(self.width) if (x, y) not in self.snake]
        if free:
            self.food = random.choice(free)

    def available_actions(self, state=None):
        state = state or self._state()
        d = state["direction"]
        return [a for a in DIRS if a != OPPOSITE[d]]

    def step(self, action):
        if action == OPPOSITE[self.direction]:
            action = self.direction
        dx, dy = DIRS[action]
        hx, hy = self.snake[0]
        nh = (hx + dx, hy + dy)
        self.steps += 1

        # wall collision
        if nh[0] < 0 or nh[0] >= self.width or nh[1] < 0 or nh[1] >= self.height:
            return self._state(), -1.0, True, {"cause": "wall", "steps": self.steps, "goals": self.goals}

        # self collision (tail moves away, so eating vs not matters)
        eating = nh == self.food
        body = list(self.snake) if eating else list(self.snake)[:-1]
        if nh in body:
            return self._state(), -1.0, True, {"cause": "self", "steps": self.steps, "goals": self.goals}

        self.snake.appendleft(nh)
        if eating:
            self.goals += 1
            self._spawn_food()
        else:
            self.snake.pop()

        self.direction = action
        done = self.steps >= self.max_steps
        reward = 1.0 if eating else 0.0
        return self._state(), reward, done, {"cause": "food" if eating else "step", "steps": self.steps, "goals": self.goals}

    def clone(self):
        c = SnakeEnv(self.width, self.height, self.max_steps)
        c.snake = deque(self.snake)
        c.food = self.food
        c.direction = self.direction
        c.steps = self.steps
        c.goals = self.goals
        return c

    def render(self, state=None):
        s = state or self._state()
        grid = [["."] * self.width for _ in range(self.height)]
        fx, fy = s["food"]
        grid[fy][fx] = "*"
        for i, (x, y) in enumerate(s["snake"]):
            grid[y][x] = "@" if i == 0 else "o"
        return "\n".join("".join(row) for row in grid)
