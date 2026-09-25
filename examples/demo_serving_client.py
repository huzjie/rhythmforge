# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Talk to a running RhythmForgeServer."""
import sys
from rhythmforge.serving.client import RhythmForgeClient

c = RhythmForgeClient(base_url=sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000")
print("health:", c.health())
print("decide:", c.decide("client.demo", ["left", "right", "up", "down"]))
print("benchmark:", c.benchmark())
