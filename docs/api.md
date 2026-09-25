# HTTP API

启动服务：

```bash
python -m rhythmforge serve --host 0.0.0.0 --port 8000
```

## GET /health

```json
{"status": "ok", "backend": {"backend": "mock", "engine_mode": "argmax", "planner": "hybrid"}}
```

## POST /decide

请求：

```json
{"context_key": "demo", "actions": ["left", "right", "up", "down"], "mode": "argmax", "temperature": 1.0}
```

响应：

```json
{"chosen_action": "up", "distribution": [{"name": "up", "prob": 0.41, "score": 1.2}, "..."], "latency_ms": 0.01, "confidence": 0.41, "entropy": 1.1, "mode": "argmax", "safety_ok": true}
```

## POST /benchmark

返回 `{"avg": 91.67, "tracks": {...}}`。

## 鉴权

设置 `serving.token` 后，请求头需带 `Authorization: Bearer <token>`。
