# 贡献指南

欢迎提交 PR。提交前请确保：

```bash
python -m compileall rhythmforge examples tests
python -m unittest discover -s tests -t .
```

新后端：继承 `DecisionModelBackend` 并在 `registry.py` 注册。
新基准：继承 `BenchmarkTrack` 并在 `suite.py` 的 `TRACKS` 注册。
