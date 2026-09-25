# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Realtime throughput demo: many decisions, measure latency."""
import time
from rhythmforge.pipeline import RhythmForge
from rhythmforge.types import DecisionContext

rf = RhythmForge()
actions = ["up", "down", "left", "right"]
N = 10000
t0 = time.perf_counter()
for i in range(N):
    rf.decide(DecisionContext(key=f"rt.{i % 97}", actions=actions))
dt = (time.perf_counter() - t0) * 1000
print(f"{N} decisions in {dt:.1f}ms  -> {dt/N*1000:.2f} us/decision")
