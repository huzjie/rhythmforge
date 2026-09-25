# -*- coding: utf-8 -*-
"""Abstract decision environment interface (for lookahead planning & demos)."""
from __future__ import annotations

from abc import ABC, abstractmethod


class DecisionEnv(ABC):
    @abstractmethod
    def reset(self, seed=None):
        """Return the initial state."""

    @abstractmethod
    def available_actions(self, state=None):
        """Return the list of legal action names."""

    @abstractmethod
    def step(self, action):
        """Apply an action, returning (state, reward, done, info)."""

    @abstractmethod
    def clone(self):
        """Return a deep-ish copy for rollouts."""

    def render(self, state=None):
        return ""
