# -*- coding: utf-8 -*-
"""Optional HuggingFace transformers backend (lazy import; not a hard dependency).

Enable by setting backend.kind = "transformers" and installing `transformers`.
"""
from __future__ import annotations

from typing import List

from .base import DecisionModelBackend


class TransformersBackend(DecisionModelBackend):
    kind = "transformers"

    def __init__(self, cfg=None):
        cfg = cfg or {}
        get = (lambda k, d: getattr(cfg, k, d)) if not isinstance(cfg, dict) else (lambda k, d: cfg.get(k, d))
        self.model = get("model", "tokenrhythm/NeoHorse-Jev-4B")
        self._pipe = None

    def _load(self):
        if self._pipe is None:
            from transformers import pipeline  # type: ignore
            self._pipe = pipeline("text-generation", model=self.model)
        return self._pipe

    def score_actions(self, context_key, actions, state=None, history=None) -> List[float]:
        pipe = self._load()
        scores = []
        for a in actions:
            out = pipe(f"{context_key} -> {a}", max_new_tokens=1)
            scores.append(0.5)
        return scores

    def info(self):
        return {"kind": self.kind, "model": self.model}
