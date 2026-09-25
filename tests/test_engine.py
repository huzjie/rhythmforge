# -*- coding: utf-8 -*-
import unittest

from rhythmforge.backend.mock import MockBackend
from rhythmforge.engine.decision_engine import RealtimeDecisionEngine
from rhythmforge.types import DecisionContext


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RealtimeDecisionEngine(MockBackend({"skill": 0.8, "noise": 0.0}), {"mode": "argmax"})

    def test_choose_action(self):
        res = self.engine.decide(DecisionContext(key="t", actions=["a", "b", "c"]))
        self.assertIn(res.chosen_action, ["a", "b", "c"])

    def test_distribution_sums_to_one(self):
        res = self.engine.decide(DecisionContext(key="t", actions=["a", "b", "c"]))
        self.assertAlmostEqual(sum(a.prob for a in res.distribution), 1.0, places=4)

    def test_empty_actions(self):
        res = self.engine.decide(DecisionContext(key="t", actions=[]))
        self.assertEqual(res.chosen_action, "")

    def test_sample_mode(self):
        eng = RealtimeDecisionEngine(MockBackend({}), {"mode": "sample"})
        res = eng.decide(DecisionContext(key="t", actions=["a", "b", "c"]))
        self.assertIn(res.chosen_action, ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()
