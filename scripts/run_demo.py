# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
"""Run a few demos quickly (dev convenience)."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
for name in ("demo_basic", "demo_planner", "demo_benchmark"):
    print(f"== {name} ==", flush=True)
    subprocess.run([sys.executable, str(root / "examples" / f"{name}.py")], check=False)
