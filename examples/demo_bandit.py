# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Bandit environment with an epsilon-greedy agent."""
from rhythmforge.agents.realtime_agent import RealtimeAgent
from rhythmforge.agents.policies import EpsilonGreedyPolicy
from rhythmforge.envs.bandit import BanditEnv
from rhythmforge.pipeline import RhythmForge

rf = RhythmForge()
env = BanditEnv(n_arms=5)
agent = RealtimeAgent(rf, policy=EpsilonGreedyPolicy(epsilon=0.2))
agent.run_episode(env, seed=2, max_steps=100)
print("total reward:", agent.summary()["total_reward"])
