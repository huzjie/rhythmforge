# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Plug in a custom decision backend."""
from rhythmforge.backend.base import DecisionModelBackend
from rhythmforge.engine.decision_engine import RealtimeDecisionEngine
from rhythmforge.types import DecisionContext


class AlwaysLastBackend(DecisionModelBackend):
    kind = "always_last"

    def score_actions(self, context_key, actions, state=None, history=None):
        return [i for i in range(len(actions))]


engine = RealtimeDecisionEngine(AlwaysLastBackend(), {"mode": "argmax"})
res = engine.decide(DecisionContext(key="x", actions=["a", "b", "c"]))
print("chosen (should be 'c'):", res.chosen_action)
