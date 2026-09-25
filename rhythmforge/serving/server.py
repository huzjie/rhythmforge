# -*- coding: utf-8 -*-
"""Zero-dependency stdlib HTTP server exposing the decision engine.

Endpoints:
    GET  /health        -> {"status":"ok"}
    POST /decide        -> score & select among candidate actions
    POST /benchmark     -> run the benchmark suite
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

from ..config import DecisionConfig, default_config
from ..pipeline import RhythmForge
from ..types import DecisionContext
from ..benchmark.suite import BenchmarkSuite
from .auth import verify_token
from .models import build_decision_response, parse_decision_request
from .rate_limit import RateLimiter


class RhythmForgeServer:
    def __init__(self, config: Optional[DecisionConfig] = None):
        self.config = config or default_config()
        self.rf = RhythmForge(self.config)
        self.limiter = RateLimiter(self.config.serving.rate_limit)
        self._httpd = None

    def _handler(self):
        server = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):
                pass

            def _json(self, code, obj):
                body = json.dumps(obj).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _authed(self):
                return verify_token(server.config.serving.token, self.headers.get("Authorization", ""))

            def do_GET(self):
                if self.path == "/health":
                    self._json(200, {"status": "ok", "backend": server.rf.doctor()})
                else:
                    self._json(404, {"error": "not found"})

            def do_POST(self):
                if not server.limiter.allow():
                    self._json(429, {"error": "rate limited"})
                    return
                if not self._authed():
                    self._json(401, {"error": "unauthorized"})
                    return
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length) if length else b"{}"
                try:
                    body = json.loads(raw.decode("utf-8"))
                except Exception:
                    self._json(400, {"error": "invalid json"})
                    return
                if self.path == "/decide":
                    req = parse_decision_request(body)
                    ctx = DecisionContext(key=req["context_key"], actions=req["actions"], history=req["history"])
                    server.rf.engine.mode = req["mode"]
                    server.rf.engine.temperature = req["temperature"]
                    res = server.rf.decide(ctx, state=req["state"])
                    self._json(200, build_decision_response(res))
                elif self.path == "/benchmark":
                    out = BenchmarkSuite(server.rf.engine).run()
                    self._json(200, {"avg": out["avg"], "tracks": out["tracks"]})
                else:
                    self._json(404, {"error": "not found"})

        return Handler

    def serve(self, host=None, port=None):
        host = host or self.config.serving.host
        port = port or self.config.serving.port
        self._httpd = ThreadingHTTPServer((host, port), self._handler())
        print(f"[serve] listening on http://{host}:{port}", flush=True)
        self._httpd.serve_forever()

    def stop(self):
        if self._httpd:
            self._httpd.shutdown()
