# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Planner sanity check on a grid world."""
from rhythmforge.envs.gridworld import GridWorldEnv
from rhythmforge.pipeline import RhythmForge
from rhythmforge.types import DecisionContext

rf = RhythmForge()
env = GridWorldEnv(width=8, height=8)
state = env.reset(seed=1)
steps = 0
while True:
    acts = env.available_actions(state)
    if not acts:
        break
    plan = rf.planner.plan(env, state)
    a = plan.chosen_action() or acts[0]
    state, r, done, info = env.step(a)
    steps += 1
    if done:
        break
print(f"reached goal in {steps} steps  cause={info.get('cause')}")
