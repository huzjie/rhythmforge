# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Decision stats + prometheus exposition."""
from rhythmforge.pipeline import RhythmForge
from rhythmforge.observability.stats import DecisionStats
from rhythmforge.observability.prometheus import to_prometheus
from rhythmforge.types import DecisionContext

rf = RhythmForge()
stats = DecisionStats()
for i in range(100):
    stats.record(rf.decide(DecisionContext(key=f"obs.{i}", actions=["a", "b", "c", "d"])))
print(stats.summary())
print(to_prometheus(stats))
