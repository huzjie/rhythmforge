# -*- coding: utf-8 -*-
"""Render a snake run to a text-based frame log (no image deps)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rhythmforge.envs.snake import SnakeEnv
from rhythmforge.pipeline import RhythmForge
from rhythmforge.types import DecisionContext

rf = RhythmForge()
env = SnakeEnv(12, 12, max_steps=200)
state = env.reset(seed=42)
frames = []
while True:
    acts = env.available_actions(state)
    action = rf.planner.plan(env, state).chosen_action()
    state, r, done, info = env.step(action)
    frames.append(env.render(state))
    if done:
        break
print(f"frames={len(frames)} goals={state['goals']} cause={info.get('cause')}")
