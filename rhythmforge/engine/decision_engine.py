# -*- coding: utf-8 -*-
"""The realtime decision engine: enumerate -> score -> softmax -> select."""
from __future__ import annotations

from typing import List, Optional

from ..backend.base import DecisionModelBackend
from ..types import Action, DecisionContext, DecisionResult
from ..utils.metrics import entropy, softmax, topk_indices
from ..utils.timer import Timer


class RealtimeDecisionEngine:
    """Turns a DecisionContext into a DecisionResult in milliseconds."""

    def __init__(self, backend: DecisionModelBackend, engine_cfg=None):
        self.backend = backend
        cfg = engine_cfg or {}
        get = (lambda k, d: getattr(cfg, k, d)) if not isinstance(cfg, dict) else (lambda k, d: cfg.get(k, d))
        self.mode = get("mode", "argmax")
        self.temperature = float(get("temperature", 1.0))
        self.min_confidence = float(get("min_confidence", 0.0))
        self.top_k = int(get("top_k", 1))

    def decide(self, context: DecisionContext, state=None, history=None) -> DecisionResult:
        timer = Timer()
        actions = list(context.actions)
        if not actions:
            return DecisionResult(context_key=context.key, latency_ms=timer.ms(), rationale="no actions")

        scores = self.backend.score_actions(context.key or str(context.state), actions, state=state, history=history)
        probs = softmax(scores, self.temperature)
        dist = [Action(name=a, score=s, prob=p) for a, s, p in zip(actions, scores, probs)]

        if self.mode == "sample":
            chosen = self._sample(actions, probs)
        elif self.mode == "topk":
            chosen = [actions[i] for i in topk_indices(scores, self.top_k)]
            chosen = chosen[0] if chosen else ""
        else:  # argmax
            chosen = actions[topk_indices(scores, 1)[0]]

        best = max(probs)
        result = DecisionResult(
            context_key=context.key,
            chosen_action=chosen,
            distribution=dist,
            latency_ms=timer.ms(),
            confidence=best,
            entropy=entropy(probs),
            mode=self.mode,
            safety_ok=best >= self.min_confidence,
            rationale=f"chose {chosen!r} with confidence {best:.3f}",
        )
        return result

    def _sample(self, actions, probs):
        import random
        r = random.random()
        acc = 0.0
        for a, p in zip(actions, probs):
            acc += p
            if r <= acc:
                return a
        return actions[-1]

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, v):
        self._mode = v
