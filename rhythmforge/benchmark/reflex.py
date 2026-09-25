# -*- coding: utf-8 -*-
"""Reflex track: additional rapid-response decisions (extended Nimble)."""
from __future__ import annotations

from .base import BenchmarkTrack, TrackItem


class ReflexTrack(BenchmarkTrack):
    name = "reflex"
    description = "Extended rapid-response decisions."

    def items(self):
        data = [
            ("reflex.fire", ["extinguish", "ignore", "observe"], "extinguish"),
            ("reflex.car", ["brake", "accelerate", "idle"], "brake"),
            ("reflex.ball", ["catch", "duck", "freeze"], "catch"),
            ("reflex.rain", ["umbrella", "none", "hat"], "umbrella"),
            ("reflex.door", ["push", "pull", "knock"], "push"),
        ]
        return [TrackItem(k, a, c, "reflex") for k, a, c in data]
