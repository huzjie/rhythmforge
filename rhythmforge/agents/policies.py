# -*- coding: utf-8 -*-
"""Action-selection policies used by the agent loop."""
from __future__ import annotations

import random
from typing import List

from ..types import DecisionContext, DecisionResult


class GreedyPolicy:
    name = "greedy"

    def choose(self, engine, env, state) -> str:
        acts = env.available_actions(state)
        ctx = DecisionContext(key=f"step.{state.get('steps', 0) if isinstance(state, dict) else 0}", actions=acts, state=state)
        return engine.decide(ctx, state=state).chosen_action


class PlannerPolicy:
    name = "planner"

    def __init__(self, planner):
        self.planner = planner

    def choose(self, engine, env, state) -> str:
        return self.planner.plan(env, state).chosen_action()


class EpsilonGreedyPolicy(GreedyPolicy):
    name = "epsilon_greedy"

    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon

    def choose(self, engine, env, state) -> str:
        acts = env.available_actions(state)
        if random.random() < self.epsilon:
            return random.choice(acts)
        return super().choose(engine, env, state)
