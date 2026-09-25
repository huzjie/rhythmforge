# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""Random-vs-random tic-tac-toe rollout."""
from rhythmforge.envs.tictactoe import TicTacToeEnv
import random

env = TicTacToeEnv()
state = env.reset(seed=1)
while True:
    acts = env.available_actions(state)
    state, r, done, info = env.step(random.choice(acts))
    if done:
        break
print("winner:", info.get("winner"))
