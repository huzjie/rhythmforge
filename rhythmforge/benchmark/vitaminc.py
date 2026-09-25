# -*- coding: utf-8 -*-
"""VitaminC track: commonsense factual decisions (named after the VITAMINC benchmark)."""
from __future__ import annotations

from .base import BenchmarkTrack, TrackItem


class VitaminCTrack(BenchmarkTrack):
    name = "vitaminc"
    description = "Commonsense factual decisions."

    def items(self):
        data = [
            ("vc.fruit", ["apple", "rock", "wire"], "apple"),
            ("vc.water", ["sand", "water", "oil"], "water"),
            ("vc.freeze", ["freezer", "oven", "microwave_high"], "freezer"),
            ("vc.sky", ["blue", "green", "red"], "blue"),
            ("vc.sleep", ["run", "sleep", "shout"], "sleep"),
        ]
        return [TrackItem(k, a, c, "commonsense") for k, a, c in data]
