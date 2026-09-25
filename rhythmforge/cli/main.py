# -*- coding: utf-8 -*-
"""Command-line interface: doctor / demo / bench / snake / plan / serve."""
from __future__ import annotations

import argparse
import json
import sys

from .._version import __version__
from ..config import load_config, default_config
from ..pipeline import RhythmForge


def cmd_doctor(args):
    rf = RhythmForge(args.config)
    print(json.dumps(rf.doctor(), ensure_ascii=False, indent=2))
    return 0


def cmd_demo(args):
    from ..types import DecisionContext
    cfg = args.config
    rf = RhythmForge(cfg)
    ctx = DecisionContext(key="demo.direction", actions=["up", "down", "left", "right"])
    res = rf.decide(ctx)
    print(f"decision: {res.chosen_action}  confidence={res.confidence:.3f}  latency={res.latency_ms:.2f}ms")
    for a in res.distribution:
        print(f"  {a.name:<8} prob={a.prob:.3f}")
    return 0


def cmd_bench(args):
    from ..benchmark.suite import BenchmarkSuite
    rf = RhythmForge(args.config)
    out = BenchmarkSuite(rf.engine, tracks=cfg_bench_tracks(args.config), seed=args.seed).run()
    print(f"AVG = {out['avg']}")
    for k, v in out["tracks"].items():
        print(f"  {k:<12} {v:.2f}")
    return 0


def cmd_snake(args):
    from ..envs.snake import SnakeEnv
    from ..types import DecisionContext
    rf = RhythmForge(args.config)
    env = SnakeEnv(width=args.width, height=args.height, max_steps=args.steps)
    state = env.reset(seed=args.seed)
    done = False
    while not done:
        acts = env.available_actions(state)
        ctx = DecisionContext(key=f"snake.{state['steps']}", actions=acts, state=state)
        # use planner for lookahead safety when enabled
        if args.planner:
            plan = rf.planner.plan(env, state)
            action = plan.chosen_action()
        else:
            action = rf.decide(ctx, state=state).chosen_action
        state, reward, done, info = env.step(action)
    print(f"snake done: steps={state['steps']} goals={state['goals']} cause={info.get('cause')}")
    return 0


def cmd_plan(args):
    from ..envs.snake import SnakeEnv
    rf = RhythmForge(args.config)
    env = SnakeEnv(width=args.width, height=args.height)
    state = env.reset(seed=args.seed)
    plan = rf.planner.plan(env, state)
    print(f"plan: {[s.action for s in plan.steps]}  survival={plan.survival_space}  planner={plan.planner}")
    return 0


def cmd_serve(args):
    from ..serving.server import RhythmForgeServer
    srv = RhythmForgeServer(args.config)
    srv.serve(args.host, args.port)
    return 0


def cfg_bench_tracks(config):
    return getattr(config.benchmark, "tracks", None) or None


def build_parser():
    p = argparse.ArgumentParser(prog="rhythmforge", description="Realtime Decision Engine & Lookahead Safety Planner")
    p.add_argument("--version", action="version", version=f"rhythmforge {__version__}")
    p.add_argument("--config", type=lambda s: load_config(s), default=default_config(),
                   help="path to config.yaml/config.json")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("doctor", help="print engine wiring info").set_defaults(func=cmd_doctor)

    d = sub.add_parser("demo", help="run a single demo decision")
    d.set_defaults(func=cmd_demo)

    b = sub.add_parser("bench", help="run the six-track benchmark suite")
    b.add_argument("--seed", type=int, default=42)
    b.set_defaults(func=cmd_bench)

    s = sub.add_parser("snake", help="play snake with the engine/planner")
    s.add_argument("--width", type=int, default=20)
    s.add_argument("--height", type=int, default=20)
    s.add_argument("--steps", type=int, default=3000)
    s.add_argument("--seed", type=int, default=42)
    s.add_argument("--planner", action="store_true", help="enable lookahead safety planner")
    s.set_defaults(func=cmd_snake)

    pl = sub.add_parser("plan", help="show a lookahead plan for the snake env")
    pl.add_argument("--width", type=int, default=20)
    pl.add_argument("--height", type=int, default=20)
    pl.add_argument("--seed", type=int, default=42)
    pl.set_defaults(func=cmd_plan)

    sv = sub.add_parser("serve", help="start the HTTP decision server")
    sv.add_argument("--host", default="127.0.0.1")
    sv.add_argument("--port", type=int, default=8000)
    sv.set_defaults(func=cmd_serve)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
