# -*- coding: utf-8 -*-
"""OpenAI-compatible decision backend (uses stdlib urllib; zero hard deps).

Requires `base_url`, `model`, and `api_key`. Actions are scored by prompting
the model to rank candidates and parsing a numeric score per action.
"""
from __future__ import annotations

import json
import os
import urllib.request
from typing import List

from .base import DecisionModelBackend


class OpenAICompatBackend(DecisionModelBackend):
    kind = "openai"

    def __init__(self, cfg=None):
        cfg = cfg or {}
        get = (lambda k, d: getattr(cfg, k, d)) if not isinstance(cfg, dict) else (lambda k, d: cfg.get(k, d))
        self.base_url = (get("base_url", "") or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.model = get("model", "jev-4b")
        self.api_key = get("api_key", "") or os.environ.get("OPENAI_API_KEY", "")
        self.temperature = float(get("temperature", 0.0))

    def score_actions(self, context_key, actions, state=None, history=None) -> List[float]:
        prompt = self._prompt(context_key, actions)
        body = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": 256,
            "messages": [{"role": "user", "content": prompt}],
        }
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions", data=data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            out = json.loads(resp.read().decode("utf-8"))
        text = out["choices"][0]["message"]["content"]
        return self._parse(text, actions)

    def _prompt(self, ctx, actions):
        return (
            "You are a realtime decision model. Given the state below and the list of "
            f"candidate actions, output one score (0-1) per action on its own line, format 'name: score'.\n"
            f"State: {ctx}\nActions: {', '.join(actions)}\nScores:"
        )

    def _parse(self, text, actions):
        scores = []
        for a in actions:
            v = 0.5
            for line in text.splitlines():
                if line.strip().lower().startswith(a.lower() + ":"):
                    try:
                        v = float(line.split(":", 1)[1].strip())
                    except ValueError:
                        pass
            scores.append(v)
        return scores

    def info(self):
        return {"kind": self.kind, "model": self.model, "base_url": self.base_url}
