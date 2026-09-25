# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Load a YAML/JSON config and run."""
import sys
from rhythmforge.config import load_config
from rhythmforge.pipeline import RhythmForge
from rhythmforge.types import DecisionContext

path = sys.argv[1] if len(sys.argv) > 1 else "configs/config.yaml"
cfg = load_config(path)
rf = RhythmForge(cfg)
print("doctor:", rf.doctor())
print(rf.decide(DecisionContext(key="cfg.demo", actions=["a", "b", "c"])).to_dict())
