# -*- coding: utf-8 -*-
"""Decision latency & confidence statistics."""
from __future__ import annotations

from statistics import mean, median


class DecisionStats:
    def __init__(self):
        self.latencies = []
        self.confidences = []
        self.entropies = []
        self.count = 0

    def record(self, result):
        self.latencies.append(result.latency_ms)
        self.confidences.append(result.confidence)
        self.entropies.append(result.entropy)
        self.count += 1

    def summary(self) -> dict:
        if not self.latencies:
            return {"count": 0}
        return {
            "count": self.count,
            "latency_avg_ms": round(mean(self.latencies), 4),
            "latency_p50_ms": round(median(self.latencies), 4),
            "latency_max_ms": round(max(self.latencies), 4),
            "confidence_avg": round(mean(self.confidences), 4),
            "entropy_avg": round(mean(self.entropies), 4),
        }
