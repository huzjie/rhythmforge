# -*- coding: utf-8 -*-
"""Multi-armed bandit environment (exploration/exploitation decisions)."""
from __future__ import annotations

import random

from .base import DecisionEnv


class BanditEnv(DecisionEnv):
    def __init__(self, n_arms: int = 5, means=None):
        self.n_arms = n_arms
        self.means = means or [0.1, 0.3, 0.5, 0.7, 0.9][:n_arms]
        self.total_reward = 0.0
        self.pulls = 0

    def reset(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.total_reward = 0.0
        self.pulls = 0
        return self._state()

    def _state(self):
        return {"pulls": self.pulls, "total_reward": self.total_reward}

    def available_actions(self, state=None):
        return [str(i) for i in range(self.n_arms)]

    def step(self, action):
        idx = int(action)
        r = 1.0 if random.random() < self.means[idx] else 0.0
        self.total_reward += r
        self.pulls += 1
        return self._state(), r, self.pulls >= 100, {}

    def clone(self):
        c = BanditEnv(self.n_arms, self.means)
        c.total_reward = self.total_reward
        c.pulls = self.pulls
        return c
