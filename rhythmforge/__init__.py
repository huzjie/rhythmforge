# -*- coding: utf-8 -*-
"""rhythmforge: Realtime Decision Engine & Lookahead Safety Planner.

A lightweight (zero-dependency core) framework for millisecond-grade
realtime decision making, inspired by the NeoHorse-Jev-4B realtime
decision model. It combines a pluggable decision-model backend with a
lookahead safety planner that avoids "painting yourself into a corner"
across long decision sequences (e.g. the classic snake game).

Key components:
    - RealtimeDecisionEngine: enumerate candidate actions, score, sample.
    - LookaheadSafetyPlanner: beam / monte-carlo / hybrid forward planning.
    - BenchmarkSuite: six evaluation tracks (Nimble / VitaminC / MASSIVE /
      Transfer / Knowledge / Semantic) with an aggregate AVG score.
    - SnakeEnv / GridWorldEnv: reference decision environments.
    - Zero-dependency stdlib HTTP serving + client.
"""

from ._version import __version__
from .config import DecisionConfig, load_config
from .pipeline import RhythmForge
from .engine.decision_engine import RealtimeDecisionEngine
from .engine.action_space import ActionSpace
from .types import (
    Action,
    DecisionContext,
    DecisionResult,
    CandidateAction,
)

__all__ = [
    "__version__",
    "DecisionConfig",
    "load_config",
    "RhythmForge",
    "RealtimeDecisionEngine",
    "ActionSpace",
    "Action",
    "DecisionContext",
    "DecisionResult",
    "CandidateAction",
]
