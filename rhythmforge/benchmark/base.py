# -*- coding: utf-8 -*-
"""A single benchmark track: (input -> expected decision) items + scoring."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List


@dataclass
class TrackItem:
    context_key: str
    actions: List[str]
    correct: str
    label: str = ""


class BenchmarkTrack:
    name = "track"
    description = ""

    def items(self) -> List[TrackItem]:
        raise NotImplementedError

    def score(self, result, item: TrackItem) -> float:
        from ..utils.hashutil import world_answer
        answer = world_answer(item.context_key, item.actions)
        return 1.0 if result.chosen_action == answer else 0.0
