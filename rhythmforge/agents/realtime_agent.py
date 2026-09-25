# -*- coding: utf-8 -*-
"""RealtimeAgent: a complete perceive -> decide -> act -> learn loop."""
from __future__ import annotations

from typing import Optional

from ..pipeline import RhythmForge
from ..envs.base import DecisionEnv
from .state import AgentState
from .policies import GreedyPolicy


class RealtimeAgent:
    """Drives an environment with the engine (and optionally the planner)."""

    def __init__(self, rf: Optional[RhythmForge] = None, policy=None, learn: bool = False):
        self.rf = rf or RhythmForge()
        self.policy = policy or GreedyPolicy()
        self.learn = learn
        self.state = AgentState()

    def run_episode(self, env: DecisionEnv, seed=None, max_steps: int = 1000) -> AgentState:
        state = env.reset(seed=seed)
        self.state = AgentState()
        while not self.state.done and self.state.step < max_steps:
            acts = env.available_actions(state)
            if not acts:
                break
            action = self.policy.choose(self.rf.engine, env, state)
            new_state, reward, done, info = env.step(action)
            self.state.record(action, reward)
            if self.learn and hasattr(self.rf.backend, "train_step"):
                correct = info.get("correct_action", action)
                self.rf.backend.train_step(f"step.{self.state.step}", action, correct, reward)
            self.state.done = done
            self.state.info = info
            state = new_state
        return self.state

    def summary(self) -> dict:
        return {
            "episode": self.state.episode,
            "steps": self.state.step,
            "decisions": self.state.decisions,
            "total_reward": self.state.total_reward,
            "done": self.state.done,
            "info": self.state.info,
        }
