# -*- coding: utf-8 -*-
"""Transfer track: apply a learned rule to held-out contexts."""
from __future__ import annotations

from .base import BenchmarkTrack, TrackItem


class TransferTrack(BenchmarkTrack):
    name = "transfer"
    description = "Generalization: same decision rule, unseen contexts."

    def items(self):
        data = [
            ("transfer.a", ["left", "right"], "right"),
            ("transfer.b", ["left", "right"], "left"),
            ("transfer.c", ["up", "down"], "up"),
            ("transfer.d", ["up", "down"], "down"),
            ("transfer.e", ["in", "out"], "in"),
        ]
        return [TrackItem(k, a, c, "transfer") for k, a, c in data]
