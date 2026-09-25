# -*- coding: utf-8 -*-
"""Semantic track: semantic similarity / entailment-style decisions."""
from __future__ import annotations

from .base import BenchmarkTrack, TrackItem


class SemanticTrack(BenchmarkTrack):
    name = "semantic"
    description = "Semantic judgment (synonymy / entailment)."

    def items(self):
        data = [
            ("sem.1", ["entailment", "contradiction", "neutral"], "entailment"),
            ("sem.2", ["contradiction", "entailment", "neutral"], "contradiction"),
            ("sem.3", ["neutral", "entailment", "contradiction"], "neutral"),
            ("sem.4", ["entailment", "neutral", "contradiction"], "entailment"),
            ("sem.5", ["contradiction", "neutral", "entailment"], "neutral"),
        ]
        return [TrackItem(k, a, c, "semantic") for k, a, c in data]
