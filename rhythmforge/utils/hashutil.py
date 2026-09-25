# -*- coding: utf-8 -*-
"""Deterministic hashing helpers (stable across runs, unlike builtin hash())."""
from __future__ import annotations

import hashlib


def stable_md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def stable_float(text: str, lo: float = 0.0, hi: float = 1.0) -> float:
    h = int(stable_md5(text)[:12], 16)
    frac = h / float(0xFFFFFFFFFFFF)
    return lo + frac * (hi - lo)


def world_answer(context_key: str, actions) -> str:
    """Deterministic hidden 'correct' action for a synthetic decision context.

    Both the mock backend and the benchmark scorer derive the ground-truth
    answer from this same function, so a high-skill model scores high and
    `train_step` produces a measurable accuracy improvement.
    """
    if not actions:
        return ""
    idx = int(stable_md5("answer:" + context_key)[:8], 16) % len(actions)
    return list(actions)[idx]
