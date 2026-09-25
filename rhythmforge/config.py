# -*- coding: utf-8 -*-
"""Configuration loading with a zero-dependency YAML fallback."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Optional

from .utils.yamlish import parse_yaml


@dataclass
class BackendConfig:
    kind: str = "mock"
    skill: float = 0.5
    temperature: float = 1.0
    prefer_first: float = 0.0
    noise: float = 0.5
    model: str = "jev-4b-mock"
    base_url: str = ""
    api_key: str = ""


@dataclass
class EngineConfig:
    mode: str = "argmax"
    temperature: float = 1.0
    min_confidence: float = 0.0
    top_k: int = 1


@dataclass
class PlannerConfig:
    kind: str = "hybrid"
    beam_width: int = 4
    depth: int = 4
    rollouts: int = 32
    survival_weight: float = 0.4


@dataclass
class BenchmarkConfig:
    tracks: list = field(default_factory=lambda: ["nimble", "vitaminc", "massive", "transfer", "knowledge", "semantic"])
    seed: int = 42


@dataclass
class ServingConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    token: str = ""
    rate_limit: int = 60


@dataclass
class DecisionConfig:
    backend: BackendConfig = field(default_factory=BackendConfig)
    engine: EngineConfig = field(default_factory=EngineConfig)
    planner: PlannerConfig = field(default_factory=PlannerConfig)
    benchmark: BenchmarkConfig = field(default_factory=BenchmarkConfig)
    serving: ServingConfig = field(default_factory=ServingConfig)
    timezone: str = "Asia/Shanghai"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: Optional[str] = None, **overrides) -> DecisionConfig:
    """Load config from a YAML/JSON file, falling back to defaults."""
    data: Dict[str, Any] = {}
    if path and Path(path).exists():
        txt = Path(path).read_text(encoding="utf-8")
        if path.endswith(".json"):
            data = json.loads(txt)
        else:
            data = parse_yaml(txt) or {}
    data = _merge(data, {"_": overrides})  # overrides live under a scratch key; drop below
    data.pop("_", None)
    return _from_dict(data)


def _from_dict(data: Dict[str, Any]) -> DecisionConfig:
    cfg = DecisionConfig()
    if "backend" in data:
        b = cfg.backend
        for k, v in data["backend"].items():
            if hasattr(b, k):
                setattr(b, k, v)
    if "engine" in data:
        e = cfg.engine
        for k, v in data["engine"].items():
            if hasattr(e, k):
                setattr(e, k, v)
    if "planner" in data:
        p = cfg.planner
        for k, v in data["planner"].items():
            if hasattr(p, k):
                setattr(p, k, v)
    if "benchmark" in data:
        bm = cfg.benchmark
        for k, v in data["benchmark"].items():
            if hasattr(bm, k):
                setattr(bm, k, v)
    if "serving" in data:
        s = cfg.serving
        for k, v in data["serving"].items():
            if hasattr(s, k):
                setattr(s, k, v)
    return cfg


def default_config() -> DecisionConfig:
    return DecisionConfig()
