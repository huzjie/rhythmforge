# -*- coding: utf-8 -*-
"""Tic-tac-toe environment (turn-based decision making)."""
from __future__ import annotations

from .base import DecisionEnv


class TicTacToeEnv(DecisionEnv):
    def __init__(self):
        self.board = None
        self.turn = "X"

    def reset(self, seed=None):
        self.board = [" "] * 9
        self.turn = "X"
        return self._state()

    def _state(self):
        return {"board": list(self.board), "turn": self.turn}

    def available_actions(self, state=None):
        state = state or self._state()
        return [str(i) for i, c in enumerate(state["board"]) if c == " "]

    def step(self, action):
        idx = int(action)
        self.board[idx] = self.turn
        winner = self._winner()
        self.turn = "O" if self.turn == "X" else "X"
        if winner:
            return self._state(), 1.0, True, {"winner": winner}
        if " " not in self.board:
            return self._state(), 0.0, True, {"winner": "draw"}
        return self._state(), 0.0, False, {}

    def _winner(self):
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        for a, b, c in lines:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]
        return None

    def clone(self):
        c = TicTacToeEnv()
        c.board = list(self.board)
        c.turn = self.turn
        return c
