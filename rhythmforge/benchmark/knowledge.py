# -*- coding: utf-8 -*-
"""Knowledge track: factual recall decisions."""
from __future__ import annotations

from .base import BenchmarkTrack, TrackItem


class KnowledgeTrack(BenchmarkTrack):
    name = "knowledge"
    description = "Factual knowledge recall."

    def items(self):
        data = [
            ("kn.capital", ["Paris", "Berlin", "Madrid"], "Paris"),
            ("kn.ocean", ["Atlantic", "Sahara", "Andes"], "Atlantic"),
            ("kn.planet", ["Mars", "Moon", "Sun"], "Mars"),
            ("kn.unit", ["meter", "second", "kelvin"], "kelvin"),
            ("kn.element", ["gold", "water", "salt"], "gold"),
        ]
        return [TrackItem(k, a, c, "knowledge") for k, a, c in data]
