# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Replay buffer sample demo."""
from rhythmforge.replay.buffer import ReplayBuffer

b = ReplayBuffer(capacity=1000)
for i in range(50):
    b.push(f"ctx.{i}", "up", 1.0 if i % 2 == 0 else 0.0)
print("buffer size:", len(b))
print("sample:", b.sample(3))
