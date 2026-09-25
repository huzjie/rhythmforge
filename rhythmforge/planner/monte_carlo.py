# -*- coding: utf-8 -*-
"""Monte-Carlo rollout planner: average value over N sampled random rollouts."""
from __future__ import annotations

import random

from ..types import Plan, PlanStep
from .base import LookaheadPlanner
from .safety import SafetyEvaluator


class MonteCarloPlanner(LookaheadPlanner):
    kind = "monte_carlo"

    def __init__(self, engine=None, cfg=None):
        super().__init__(engine, cfg)
        get = (lambda k, d: getattr(cfg, k, d)) if cfg and not isinstance(cfg, dict) else (lambda k, d: cfg.get(k, d) if cfg else d)
        self.rollouts = int(get("rollouts", 32))
        self.depth = int(get("depth", 8))
        self.safety = SafetyEvaluator()

    def plan(self, env, state=None):
        state = state if state is not None else env.reset()
        first_actions = env.available_actions(state)
        if not first_actions:
            return Plan(planner=self.kind, dead_end=True)
        best_a = first_actions[0]
        best_v = float("-inf")
        for a in first_actions:
            total = 0.0
            for _ in range(self.rollouts):
                c = env.clone()
                c = self._set_state(c, state)
                s, r, done, _ = c.step(a)
                val = r
                d = 0
                while not done and d < self.depth:
                    acts = c.available_actions(s)
                    if not acts:
                        break
                    s, r, done, _ = c.step(random.choice(acts))
                    val += r
                    d += 1
                val += self.safety.survival(s) * 0.2
                total += val
            avg = total / self.rollouts
            if avg > best_v:
                best_v = avg
                best_a = a
        return Plan(steps=[PlanStep(action=best_a)], total_score=best_v, planner=self.kind)

    def _set_state(self, env, state):
        if hasattr(env, "snake") and isinstance(state, dict) and "snake" in state:
            from collections import deque
            env.snake = deque(state["snake"])
            env.food = state["food"]
            env.direction = state["direction"]
            env.steps = state["steps"]
            env.goals = state["goals"]
        elif hasattr(env, "pos") and isinstance(state, dict) and "pos" in state:
            env.pos = state["pos"]
            env.steps = state["steps"]
        return env
