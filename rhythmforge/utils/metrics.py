# -*- coding: utf-8 -*-
"""Probability / entropy / ranking helpers."""
from __future__ import annotations

import math
from typing import List


def softmax(scores: List[float], temperature: float = 1.0) -> List[float]:
    if not scores:
        return []
    t = max(temperature, 1e-6)
    mx = max(scores)
    exps = [math.exp((s - mx) / t) for s in scores]
    total = sum(exps)
    if total == 0:
        return [1.0 / len(scores)] * len(scores)
    return [e / total for e in exps]


def entropy(probs: List[float]) -> float:
    if not probs:
        return 0.0
    return -sum(p * math.log(p) for p in probs if p > 0)


def topk_indices(scores: List[float], k: int = 1) -> List[int]:
    idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return idx[:k]
