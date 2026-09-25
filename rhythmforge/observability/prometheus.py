# -*- coding: utf-8 -*-
"""Prometheus text-exposition format emitter (optional integration)."""
from __future__ import annotations

from .stats import DecisionStats


def to_prometheus(stats: DecisionStats) -> str:
    s = stats.summary()
    if not s:
        return ""
    lines = [
        "# HELP rhythmforge_decision_count Total decisions made.",
        "# TYPE rhythmforge_decision_count counter",
        f"rhythmforge_decision_count {s['count']}",
        "# HELP rhythmforge_decision_latency_ms Decision latency.",
        "# TYPE rhythmforge_decision_latency_ms gauge",
        f"rhythmforge_decision_latency_ms {s['latency_avg_ms']}",
    ]
    return "\n".join(lines) + "\n"
