# -*- coding: utf-8 -*-
"""Aggregate scoring (AVG) across benchmark tracks."""
from __future__ import annotations

from typing import Dict


def aggregate_score(track_scores: Dict[str, float]) -> float:
    if not track_scores:
        return 0.0
    return sum(track_scores.values()) / len(track_scores)


def track_report(scores: Dict[str, float]) -> dict:
    avg = aggregate_score(scores)
    return {"tracks": scores, "avg": round(avg, 2)}
