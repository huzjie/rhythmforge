# -*- coding: utf-8 -*-
import unittest

from rhythmforge.pipeline import RhythmForge
from rhythmforge.benchmark.suite import BenchmarkSuite


class TestBenchmark(unittest.TestCase):
    def test_all_tracks_run(self):
        rf = RhythmForge()
        out = BenchmarkSuite(rf.engine).run()
        self.assertEqual(set(out["tracks"].keys()), {"nimble", "vitaminc", "massive", "transfer", "knowledge", "semantic"})
        self.assertIsInstance(out["avg"], float)


if __name__ == "__main__":
    unittest.main()
