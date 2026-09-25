# -*- coding: utf-8 -*-
"""Stdlib HTTP client for the decision API."""
from __future__ import annotations

import json
import urllib.request
from typing import List, Optional


class RhythmForgeClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def health(self) -> dict:
        return self._request("GET", "/health")

    def decide(self, context_key: str, actions: List[str], state=None, mode: str = "argmax", temperature: float = 1.0) -> dict:
        body = {"context_key": context_key, "actions": actions, "state": state, "mode": mode, "temperature": temperature}
        return self._request("POST", "/decide", body)

    def benchmark(self) -> dict:
        return self._request("POST", "/benchmark", {})

    def _request(self, method, path, body=None):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(self.base_url + path, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
