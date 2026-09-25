# -*- coding: utf-8 -*-
import unittest

from rhythmforge.envs.snake import SnakeEnv
from rhythmforge.envs.gridworld import GridWorldEnv


class TestSnake(unittest.TestCase):
    def test_reset(self):
        env = SnakeEnv(10, 10)
        s = env.reset(seed=1)
        self.assertIn("snake", s)
        self.assertGreaterEqual(len(s["snake"]), 3)

    def test_step_legal(self):
        env = SnakeEnv(10, 10)
        s = env.reset(seed=1)
        a = env.available_actions(s)[0]
        s2, r, done, info = env.step(a)
        self.assertIsInstance(s2, dict)

    def test_no_reverse(self):
        env = SnakeEnv(10, 10)
        s = env.reset(seed=1)
        self.assertNotIn("left", env.available_actions(s))  # starts moving right


class TestGridWorld(unittest.TestCase):
    def test_reach_goal(self):
        env = GridWorldEnv(4, 4)
        s = env.reset(seed=1)
        # drive right then down deterministically
        while env.pos != (3, 3) and env.steps < 100:
            x, y = env.pos
            a = "right" if x < 3 else "down"
            s, r, done, _ = env.step(a)
            if done:
                break
        self.assertEqual(env.pos, (3, 3))


if __name__ == "__main__":
    unittest.main()
