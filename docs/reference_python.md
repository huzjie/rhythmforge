# Python API 参考

- `RhythmForge(config)`：顶层门面，组合 backend + engine + planner。
- `RealtimeDecisionEngine(backend, engine_cfg).decide(ctx)`。
- `LookaheadPlanner.plan(env, state)`。
- `BenchmarkSuite(engine).run()`。
- `RealtimeAgent(rf, policy, learn).run_episode(env)`。

详见各模块 docstring 与 `examples/`。
