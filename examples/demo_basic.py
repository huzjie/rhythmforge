# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Minimal decision demo."""
from rhythmforge.pipeline import RhythmForge
from rhythmforge.types import DecisionContext

rf = RhythmForge()
ctx = DecisionContext(key="demo.basic", actions=["left", "right", "up", "down"])
res = rf.decide(ctx)
print(f"chosen={res.chosen_action} confidence={res.confidence:.3f} latency={res.latency_ms:.2f}ms")
for a in res.distribution:
    print(f"  {a.name:<8} {a.prob:.3f}")
