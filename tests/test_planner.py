# -*- coding: utf-8 -*-
import unittest

from rhythmforge.envs.snake import SnakeEnv
from rhythmforge.pipeline import RhythmForge


class TestPlanner(unittest.TestCase):
    def test_beam_plan(self):
        rf = RhythmForge()
        env = SnakeEnv(10, 10)
        state = env.reset(seed=3)
        plan = rf.planner.plan(env, state)
        self.assertTrue(plan.steps)
        self.assertEqual(plan.planner, "hybrid")

    def test_monte_carlo_plan(self):
        from rhythmforge.planner.monte_carlo import MonteCarloPlanner
        env = SnakeEnv(10, 10)
        state = env.reset(seed=3)
        plan = MonteCarloPlanner(None, {"rollouts": 8, "depth": 4}).plan(env, state)
        self.assertTrue(plan.steps)


if __name__ == "__main__":
    unittest.main()
