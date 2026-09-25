# -*- coding: utf-8 -*-
"""Core dataclasses shared across the engine, planner, envs and serving layer."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Action:
    """A candidate action within a decision context."""

    name: str
    score: float = 0.0
    prob: float = 0.0
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "score": self.score, "prob": self.prob, "meta": self.meta}


@dataclass
class DecisionContext:
    """The full state presented to the decision model at a single step."""

    state: Any = None
    actions: List[str] = field(default_factory=list)
    history: List[str] = field(default_factory=list)
    key: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)

    def candidate_actions(self) -> List[CandidateAction]:
        return [CandidateAction(name=a) for a in self.actions]


@dataclass
class CandidateAction:
    """Lightweight wrapper for an action name pending scoring."""

    name: str
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionResult:
    """The outcome of a single decision step."""

    context_key: str = ""
    chosen_action: str = ""
    distribution: List[Action] = field(default_factory=list)
    latency_ms: float = 0.0
    confidence: float = 0.0
    entropy: float = 0.0
    mode: str = "argmax"
    safety_ok: bool = True
    rationale: str = ""

    def top_actions(self, k: int = 3) -> List[Action]:
        return sorted(self.distribution, key=lambda a: a.prob, reverse=True)[:k]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "context_key": self.context_key,
            "chosen_action": self.chosen_action,
            "distribution": [a.to_dict() for a in self.distribution],
            "latency_ms": self.latency_ms,
            "confidence": self.confidence,
            "entropy": self.entropy,
            "mode": self.mode,
            "safety_ok": self.safety_ok,
            "rationale": self.rationale,
        }


@dataclass
class PlanStep:
    """One step of a lookahead plan."""

    action: str
    state: Any = None
    score: float = 0.0
    survival: float = 1.0


@dataclass
class Plan:
    """A forward-looking plan produced by the safety planner."""

    steps: List[PlanStep] = field(default_factory=list)
    total_score: float = 0.0
    survival_space: int = 0
    dead_end: bool = False
    planner: str = ""

    def chosen_action(self) -> str:
        return self.steps[0].action if self.steps else ""


@dataclass
class EnvStep:
    """Result of advancing a decision environment by one action."""

    state: Any = None
    reward: float = 0.0
    done: bool = False
    info: Dict[str, Any] = field(default_factory=dict)
