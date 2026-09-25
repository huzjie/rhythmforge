# -*- coding: utf-8 -*-
import threading
import unittest

from rhythmforge.serving.auth import verify_token
from rhythmforge.serving.rate_limit import RateLimiter


class TestAuth(unittest.TestCase):
    def test_verify(self):
        self.assertTrue(verify_token("tok", "Bearer tok"))
        self.assertFalse(verify_token("tok", "Bearer bad"))
        self.assertTrue(verify_token("", ""))  # no token -> open


class TestRateLimit(unittest.TestCase):
    def test_limit(self):
        rl = RateLimiter(limit=2, window=60)
        self.assertTrue(rl.allow())
        self.assertTrue(rl.allow())
        self.assertFalse(rl.allow())


if __name__ == "__main__":
    unittest.main()
