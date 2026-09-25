# -*- coding: utf-8 -*-
"""Agent run state / episode bookkeeping."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class AgentState:
    episode: int = 0
    step: int = 0
    total_reward: float = 0.0
    decisions: int = 0
    history: List[str] = field(default_factory=list)
    done: bool = False
    info: dict = field(default_factory=dict)

    def record(self, action: str, reward: float):
        self.history.append(action)
        self.total_reward += reward
        self.decisions += 1
        self.step += 1
