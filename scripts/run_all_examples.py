# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
"""Run every example script in sequence."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
ex = sorted((root / "examples").glob("demo_*.py"))
ok = 0
for p in ex:
    print(f"== {p.name} ==", flush=True)
    r = subprocess.run([sys.executable, str(p)], check=False)
    if r.returncode == 0:
        ok += 1
    else:
        print(f"   !! {p.name} exited {r.returncode}", flush=True)
print(f"{ok}/{len(ex)} examples passed", flush=True)
