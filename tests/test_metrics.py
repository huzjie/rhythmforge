# -*- coding: utf-8 -*-
import unittest

from rhythmforge.utils.metrics import softmax, entropy, topk_indices


class TestMetrics(unittest.TestCase):
    def test_softmax_sums_one(self):
        p = softmax([1.0, 2.0, 3.0])
        self.assertAlmostEqual(sum(p), 1.0, places=6)

    def test_entropy_uniform(self):
        import math
        self.assertAlmostEqual(entropy([0.25] * 4), math.log(4), places=4)

    def test_topk(self):
        self.assertEqual(topk_indices([0.1, 0.9, 0.5], 2), [1, 2])


if __name__ == "__main__":
    unittest.main()
