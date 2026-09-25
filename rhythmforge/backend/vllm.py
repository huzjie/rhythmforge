# -*- coding: utf-8 -*-
"""vLLM OpenAI-compatible serving backend (drop-in alias of the openai backend)."""
from __future__ import annotations

from .openai_compat import OpenAICompatBackend


class VLLMBackend(OpenAICompatBackend):
    kind = "vllm"

    def __init__(self, cfg=None):
        cfg = cfg or {}
        get = (lambda k, d: getattr(cfg, k, d)) if not isinstance(cfg, dict) else (lambda k, d: cfg.get(k, d))
        if not get("base_url", ""):
            cfg = dict(cfg) if isinstance(cfg, dict) else {**cfg.__dict__}
            cfg["base_url"] = "http://127.0.0.1:8000/v1"
        super().__init__(cfg)
        self.kind = "vllm"
