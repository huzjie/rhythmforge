# -*- coding: utf-8 -*-
import unittest

from rhythmforge.backend.mock import MockBackend


class TestMockBackend(unittest.TestCase):
    def test_deterministic(self):
        b = MockBackend({"skill": 0.6, "noise": 0.0})
        s1 = b.score_actions("k", ["a", "b", "c"])
        s2 = b.score_actions("k", ["a", "b", "c"])
        self.assertEqual(s1, s2)

    def test_train_improves(self):
        b = MockBackend({"skill": 0.5, "noise": 0.0})
        b.train_step("k", "right", "right")
        self.assertGreater(b.skill, 0.5)

    def test_length_matches(self):
        b = MockBackend({})
        self.assertEqual(len(b.score_actions("k", ["a", "b", "c", "d"])), 4)


if __name__ == "__main__":
    unittest.main()
