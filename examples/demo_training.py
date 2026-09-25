# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Train the mock backend: skill improves with reward feedback."""
from rhythmforge.backend.mock import MockBackend
from rhythmforge.engine.decision_engine import RealtimeDecisionEngine
from rhythmforge.types import DecisionContext
from rhythmforge.utils.hashutil import world_answer

backend = MockBackend({"skill": 0.2, "noise": 0.5})
engine = RealtimeDecisionEngine(backend, {"mode": "argmax"})
actions = ["left", "right", "up", "down"]

hits = 0
total = 0
for i in range(200):
    key = f"train.{i % 23}"
    ctx = DecisionContext(key=key, actions=actions)
    res = engine.decide(ctx)
    correct = world_answer(key, actions)
    total += 1
    hits += 1 if res.chosen_action == correct else 0
    backend.train_step(ctx.key, res.chosen_action, correct)

print(f"after training: skill={backend.skill:.3f} accuracy={hits/total:.3f}")
# print a rolling accuracy to show improvement
