# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Run the six-track benchmark suite."""
from rhythmforge.pipeline import RhythmForge
from rhythmforge.benchmark.suite import BenchmarkSuite

rf = RhythmForge()
out = BenchmarkSuite(rf.engine).run()
print(f"AVG = {out['avg']}")
for k, v in out["tracks"].items():
    print(f"  {k:<12} {v:.2f}")
