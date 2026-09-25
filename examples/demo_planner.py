# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Lookahead planner demo on the snake environment."""
from rhythmforge.envs.snake import SnakeEnv
from rhythmforge.pipeline import RhythmForge

rf = RhythmForge()
env = SnakeEnv(width=20, height=20)
state = env.reset(seed=7)
plan = rf.planner.plan(env, state)
print(f"planner={plan.planner} chosen={plan.chosen_action()} survival_space={plan.survival_space}")
print("steps:", [s.action for s in plan.steps])
