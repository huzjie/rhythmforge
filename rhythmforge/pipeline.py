# -*- coding: utf-8 -*-
"""Top-level RhythmForge pipeline that wires backend + engine + planner together."""
from __future__ import annotations

from typing import Optional

from .config import DecisionConfig, default_config
from .backend.registry import make_backend
from .engine.decision_engine import RealtimeDecisionEngine
from .planner.registry import make_planner


class RhythmForge:
    """Convenience facade over the decision engine and safety planner."""

    def __init__(self, config: Optional[DecisionConfig] = None):
        self.config = config or default_config()
        self.backend = make_backend(self.config.backend)
        self.engine = RealtimeDecisionEngine(self.backend, self.config.engine)
        self.planner = make_planner(self.config.planner, self.engine)

    def decide(self, context, state=None, history=None):
        return self.engine.decide(context, state=state, history=history)

    def plan(self, env):
        return self.planner.plan(env)

    def doctor(self):
        return {
            "backend": self.backend.kind,
            "engine_mode": self.engine.mode,
            "planner": self.planner.kind,
        }
