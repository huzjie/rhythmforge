# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Run the full RealtimeAgent loop on the snake env."""
from rhythmforge.agents.realtime_agent import RealtimeAgent
from rhythmforge.agents.policies import PlannerPolicy
from rhythmforge.envs.snake import SnakeEnv
from rhythmforge.pipeline import RhythmForge

rf = RhythmForge()
env = SnakeEnv(20, 20)
agent = RealtimeAgent(rf, policy=PlannerPolicy(rf.planner))
state = agent.run_episode(env, seed=5, max_steps=500)
print(agent.summary())
