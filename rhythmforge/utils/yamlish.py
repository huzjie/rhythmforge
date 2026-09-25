# -*- coding: utf-8 -*-
"""Minimal YAML-subset parser (no external deps).

Supports: nested mapping indentation, inline lists, scalars (str/int/float/bool/null),
trailing comments, and `key: value` pairs. Intended as a fallback so the zero-
dependency core can still read YAML configs without PyYAML.
"""
from __future__ import annotations

import re
from typing import Any


def _strip_comment(line: str) -> str:
    # crude: only strip comments when '#' is preceded by whitespace/start
    out = []
    in_quote = False
    q = ""
    for ch in line:
        if ch in ("\'", '\"') and not in_quote:
            in_quote = True
            q = ch
        elif ch == q and in_quote:
            in_quote = False
        if ch == "#" and not in_quote:
            break
        out.append(ch)
    return "".join(out).rstrip()


def _scalar(v: str) -> Any:
    v = v.strip()
    if v == "":
        return ""
    if v in ("null", "~", "Null", "NULL"):
        return None
    if v in ("true", "True", "TRUE"):
        return True
    if v in ("false", "False", "FALSE"):
        return False
    if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
        return v[1:-1]
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


def _parse_inline_list(s: str) -> list:
    s = s.strip()
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if inner == "":
            return []
        return [_scalar(x) for x in inner.split(",")]
    return [_scalar(x) for x in s.split(",")]


def parse_yaml(text: str) -> dict:
    lines = [_strip_comment(ln).rstrip() for ln in text.splitlines()]
    root: dict = {}
    stack: list = [(root, -1)]
    for raw in lines:
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if line.startswith("#"):
            continue
        if line.startswith("- "):
            # inline list item (minimal support): attach to current list key
            item = _scalar(line[2:].strip())
            continue
        if ":" in line:
            # pop stack entries at or deeper than the current indent
            while len(stack) > 1 and stack[-1][1] >= indent:
                stack.pop()
            parent = stack[-1][0]
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            if v == "":
                child: dict = {}
                parent[k] = child
                stack.append((child, indent))
            elif v.startswith("[") and v.endswith("]"):
                parent[k] = _parse_inline_list(v)
            else:
                parent[k] = _scalar(v)
    return root


def _assign(stack: list, indent: int, k: str, val: Any):
    # pop stack entries deeper than current indent
    while len(stack) > 1 and stack[-1][1] >= indent:
        stack.pop()
    parent = stack[-1][0]
    if isinstance(parent, dict):
        parent[k] = val
