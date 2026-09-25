# -*- coding: utf-8 -*-
"""Runs all benchmark tracks against the engine and aggregates an AVG score."""
from __future__ import annotations

from typing import Dict, List, Optional

from ..types import DecisionContext
from .nimble import NimbleTrack
from .vitaminc import VitaminCTrack
from .massive import MASSIVETrack
from .transfer import TransferTrack
from .knowledge import KnowledgeTrack
from .semantic import SemanticTrack
from .reflex import ReflexTrack
from .safety import SafetyTrack
from .scoring import aggregate_score

TRACKS = {
    "nimble": NimbleTrack,
    "vitaminc": VitaminCTrack,
    "massive": MASSIVETrack,
    "transfer": TransferTrack,
    "knowledge": KnowledgeTrack,
    "semantic": SemanticTrack,
    "reflex": ReflexTrack,
    "safety": SafetyTrack,
}

DEFAULT_TRACKS = ["nimble", "vitaminc", "massive", "transfer", "knowledge", "semantic"]


class BenchmarkSuite:
    def __init__(self, engine, tracks: Optional[List[str]] = None, seed: int = 42):
        self.engine = engine
        self.tracks = tracks or list(DEFAULT_TRACKS)
        self.seed = seed

    def run(self) -> dict:
        scores: Dict[str, float] = {}
        details: Dict[str, dict] = {}
        for name in self.tracks:
            cls = TRACKS[name]
            track = cls()
            correct = 0
            total = 0
            per = []
            for item in track.items():
                ctx = DecisionContext(key=item.context_key, actions=item.actions)
                res = self.engine.decide(ctx)
                ok = track.score(res, item)
                correct += ok
                total += 1
                per.append({"item": item.context_key, "correct": item.correct, "chosen": res.chosen_action, "ok": bool(ok)})
            scores[name] = (correct / total * 100.0) if total else 0.0
            details[name] = {"correct": correct, "total": total, "acc": round(scores[name], 2), "items": per}
        avg = aggregate_score(scores)
        return {"tracks": scores, "avg": round(avg, 2), "details": details}


def run_benchmarks(engine, tracks=None, seed=42) -> dict:
    return BenchmarkSuite(engine, tracks=tracks, seed=seed).run()
