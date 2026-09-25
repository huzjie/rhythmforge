# -*- coding: utf-8 -*-
"""Nimble track: rapid reflex decisions under time pressure (deterministic truths)."""
from __future__ import annotations

from .base import BenchmarkTrack, TrackItem


class NimbleTrack(BenchmarkTrack):
    name = "nimble"
    description = "Rapid reflex decisions: pick the correct action from noisy candidates."

    def items(self):
        data = [
            ("nimble.obstacle", ["dodge_left", "dodge_right", "stay"], "dodge_right"),
            ("nimble.threat", ["retreat", "advance", "hold"], "retreat"),
            ("nimble.light", ["green", "red", "yellow"], "green"),
            ("nimble.gap", ["jump", "stop", "crawl"], "jump"),
            ("nimble.edge", ["turn", "continue", "brake"], "brake"),
        ]
        return [TrackItem(k, a, c, "reflex") for k, a, c in data]
