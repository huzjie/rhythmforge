# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Episodic memory store / recall demo."""
from rhythmforge.memory.episodic import EpisodicMemory

m = EpisodicMemory(capacity=100)
m.store("ctx.1", "right", 1.0)
m.store("ctx.2", "left", -1.0)
print("recall ctx.1:", m.recall("ctx.1"))
print("recent:", m.recent(5))
print("best_action ctx.1:", m.best_action("ctx.1"))
