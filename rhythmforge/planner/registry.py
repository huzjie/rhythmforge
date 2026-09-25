# -*- coding: utf-8 -*-
"""Planner factory."""
from __future__ import annotations


def make_planner(cfg, engine=None):
    kind = getattr(cfg, "kind", "hybrid") if not isinstance(cfg, dict) else cfg.get("kind", "hybrid")
    if kind == "beam":
        from .beam import BeamPlanner
        return BeamPlanner(engine, cfg)
    if kind == "monte_carlo":
        from .monte_carlo import MonteCarloPlanner
        return MonteCarloPlanner(engine, cfg)
    from .hybrid import HybridPlanner
    return HybridPlanner(engine, cfg)
