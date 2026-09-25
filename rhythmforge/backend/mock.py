# -*- coding: utf-8 -*-
"""Deterministic, trainable mock decision backend.

Models the two signals that real decision models exhibit:
  * a latent `skill` (how often it picks the genuinely correct action)
  * a positional bias `prefer_first` (favor earlier-listed actions)

The two are additively separated so the lookahead planner and benchmarks can
measure genuine decision quality rather than artifacts. Fully deterministic
via md5 seeding (no PYTHONHASHSEED sensitivity).
"""
from __future__ import annotations

from typing import List

from .base import DecisionModelBackend
from ..utils.hashutil import stable_float, stable_md5


class MockBackend(DecisionModelBackend):
    kind = "mock"

    def __init__(self, cfg=None):
        cfg = cfg or {}
        get = (lambda k, d: getattr(cfg, k, d)) if not isinstance(cfg, dict) else (lambda k, d: cfg.get(k, d))
        self.skill = float(get("skill", 0.35))
        self.prefer_first = float(get("prefer_first", 0.0))
        self.noise = float(get("noise", 0.5))
        self.model = get("model", "jev-4b-mock")
        self.temperature = float(get("temperature", 1.0))
        self._steps = 0

    def _truth(self, context_key: str, action: str, actions) -> float:
        # 1.0 for the deterministic hidden correct action, else 0.0
        from ..utils.hashutil import world_answer
        return 1.0 if action == world_answer(context_key, actions) else 0.0

    def score_actions(self, context_key, actions, state=None, history=None) -> List[float]:
        n = len(actions)
        scores = []
        for i, a in enumerate(actions):
            truth = self._truth(context_key, a, actions)
            pos = self.prefer_first * (1.0 - i / max(n - 1, 1)) if n > 1 else 0.0
            noise = (stable_float(f"noise:{context_key}|{a}|{self._steps}", -1, 1)) * self.noise
            score = self.skill * truth + pos + noise
            scores.append(score)
        return scores

    def train_step(self, context_key, chosen, correct, reward=0.0):
        # simple reward-based skill adaptation (bounded)
        if chosen == correct:
            self.skill = min(0.99, self.skill + 0.02)
        else:
            self.skill = max(0.05, self.skill - 0.01)
        self._steps += 1

    def info(self):
        return {"kind": self.kind, "skill": round(self.skill, 4), "model": self.model}
