# -*- coding: utf-8 -*-
"""Request/response JSON models for the HTTP API."""
from __future__ import annotations

from typing import Any, Dict, List, Optional


def parse_decision_request(body: dict) -> dict:
    return {
        "context_key": body.get("context_key", body.get("key", "")),
        "actions": body.get("actions", []),
        "state": body.get("state"),
        "history": body.get("history", []),
        "mode": body.get("mode", "argmax"),
        "temperature": body.get("temperature", 1.0),
    }


def build_decision_response(result) -> dict:
    return {
        "chosen_action": result.chosen_action,
        "distribution": [a.to_dict() for a in result.distribution],
        "latency_ms": round(result.latency_ms, 3),
        "confidence": round(result.confidence, 4),
        "entropy": round(result.entropy, 4),
        "mode": result.mode,
        "safety_ok": result.safety_ok,
    }
