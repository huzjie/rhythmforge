# -*- coding: utf-8 -*-
"""Backend registry + factory."""
from __future__ import annotations

from .base import DecisionModelBackend

_REGISTRY: dict = {}


def register_backend(kind: str, cls):
    _REGISTRY[kind] = cls


def list_backends():
    return sorted(_REGISTRY.keys())


def make_backend(cfg) -> DecisionModelBackend:
    """Instantiate a backend from a BackendConfig (or dict-like)."""
    if isinstance(cfg, dict):
        kind = cfg.get("kind", "mock")
    else:
        kind = getattr(cfg, "kind", "mock")
    if kind == "mock":
        from .mock import MockBackend
        return MockBackend(cfg)
    if kind == "openai":
        from .openai_compat import OpenAICompatBackend
        return OpenAICompatBackend(cfg)
    if kind == "vllm":
        from .vllm import VLLMBackend
        return VLLMBackend(cfg)
    cls = _REGISTRY.get(kind)
    if cls is None:
        raise ValueError(f"unknown backend kind: {kind!r} (available: {list_backends() + ['mock','openai','vllm']})")
    return cls(cfg)


def _register_builtins():
    from .mock import MockBackend
    from .openai_compat import OpenAICompatBackend
    from .vllm import VLLMBackend
    register_backend("mock", MockBackend)
    register_backend("openai", OpenAICompatBackend)
    register_backend("vllm", VLLMBackend)


_register_builtins()
