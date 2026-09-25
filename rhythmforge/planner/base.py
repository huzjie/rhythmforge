# -*- coding: utf-8 -*-
"""Abstract lookahead planner."""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..types import Plan


class LookaheadPlanner(ABC):
    kind = "base"

    def __init__(self, engine=None, cfg=None):
        self.engine = engine

    @abstractmethod
    def plan(self, env, state=None) -> Plan:
        raise NotImplementedError
