# -*- coding: utf-8 -*-
"""Hybrid planner: use beam search, fall back to monte-carlo for tie-breaks."""
from __future__ import annotations

from ..types import Plan
from .base import LookaheadPlanner
from .beam import BeamPlanner
from .monte_carlo import MonteCarloPlanner


class HybridPlanner(LookaheadPlanner):
    kind = "hybrid"

    def __init__(self, engine=None, cfg=None):
        super().__init__(engine, cfg)
        self.beam = BeamPlanner(engine, cfg)
        self.mc = MonteCarloPlanner(engine, cfg)

    def plan(self, env, state=None):
        p = self.beam.plan(env, state)
        if p.dead_end or not p.steps:
            p = self.mc.plan(env, state)
        p.planner = self.kind  # surface the hybrid identity
        return p
