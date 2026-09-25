# -*- coding: utf-8 -*-
"""Action space construction and candidate enumeration."""
from __future__ import annotations

from typing import List, Optional


class ActionSpace:
    """Builds and filters the candidate action list for a decision step."""

    def __init__(self, actions: Optional[List[str]] = None):
        self._actions = list(actions or [])

    @classmethod
    def from_state(cls, state, default_actions=None):
        # states may expose `.available_actions()`
        if hasattr(state, "available_actions"):
            return cls(state.available_actions())
        if isinstance(state, dict) and "actions" in state:
            return cls(state["actions"])
        return cls(default_actions or [])

    @classmethod
    def cardinal(cls, directions=("up", "down", "left", "right")):
        return cls(list(directions))

    def filter(self, predicate) -> "ActionSpace":
        self._actions = [a for a in self._actions if predicate(a)]
        return self

    def actions(self) -> List[str]:
        return list(self._actions)

    def __len__(self):
        return len(self._actions)

    def __iter__(self):
        return iter(self._actions)
