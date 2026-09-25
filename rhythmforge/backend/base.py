# -*- coding: utf-8 -*-
"""Abstract decision-model backend interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class DecisionModelBackend(ABC):
    """Scores candidate actions given a decision context.

    A concrete backend returns a score per action (higher is better). The
    engine converts scores into a probability distribution via softmax.
    """

    kind = "base"

    @abstractmethod
    def score_actions(self, context_key: str, actions: List[str], state=None, history=None) -> List[float]:
        """Return a score for each action (same length as `actions`)."""
        raise NotImplementedError

    def train_step(self, context_key: str, chosen: str, correct: str, reward: float = 0.0) -> None:
        """Optional: update internal parameters from feedback (used by trainable backends)."""

    def info(self) -> dict:
        return {"kind": self.kind}
