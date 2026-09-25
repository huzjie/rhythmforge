# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Full snake game: greedy vs lookahead-safety comparison."""
from rhythmforge.envs.snake import SnakeEnv
from rhythmforge.pipeline import RhythmForge
from rhythmforge.types import DecisionContext

rf = RhythmForge()

def run(mode, seed=42):
    env = SnakeEnv(width=20, height=20, max_steps=3000)
    state = env.reset(seed=seed)
    while True:
        acts = env.available_actions(state)
        if mode == "planner":
            action = rf.planner.plan(env, state).chosen_action()
        else:
            action = rf.decide(DecisionContext(key=f"s.{state['steps']}", actions=acts, state=state), state=state).chosen_action
        state, _, done, info = env.step(action)
        if done:
            return state["goals"], state["steps"], info.get("cause")

for mode in ("greedy", "planner"):
    goals, steps, cause = run(mode)
    print(f"{mode:<10} goals={goals:<4} steps={steps:<5} cause={cause}")
