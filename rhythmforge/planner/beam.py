# -*- coding: utf-8 -*-
"""Beam-search lookahead planner: keep top-k action sequences by expected value."""
from __future__ import annotations

from ..types import Plan, PlanStep
from .base import LookaheadPlanner
from .safety import SafetyEvaluator


class BeamPlanner(LookaheadPlanner):
    kind = "beam"

    def __init__(self, engine=None, cfg=None):
        super().__init__(engine, cfg)
        get = (lambda k, d: getattr(cfg, k, d)) if cfg and not isinstance(cfg, dict) else (lambda k, d: cfg.get(k, d) if cfg else d)
        self.beam_width = int(get("beam_width", 4))
        self.depth = int(get("depth", 4))
        self.survival_weight = float(get("survival_weight", 0.4))
        self.safety = SafetyEvaluator()

    def plan(self, env, state=None):
        state = state if state is not None else env.reset() if hasattr(env, "reset") else None
        beams = [([], state, 0.0)]
        for _ in range(self.depth):
            nxt = []
            for path, st, score in beams:
                for a in env.available_actions(st):
                    cloned = env.clone()
                    # replay path to reach st is avoided: step from st directly via cloned env state
                    cloned = self._set_state(cloned, st)
                    s2, r, done, _info = cloned.step(a)
                    survival = self.safety.survival(s2)
                    val = score + r + (0.0 if done else self.survival_weight * survival)
                    nxt.append((path + [a], s2, val))
            nxt.sort(key=lambda x: -x[2])
            beams = nxt[: self.beam_width]
        if not beams:
            return Plan(planner=self.kind, dead_end=True)
        best_path, best_state, best_score = beams[0]
        steps = [PlanStep(action=a) for a in best_path]
        return Plan(steps=steps, total_score=best_score,
                     survival_space=int(self.safety.survival(best_state) * 100),
                     planner=self.kind)

    def _set_state(self, env, state):
        # snake envs clone cheaply; here we re-seat a cloned env to the given state
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
