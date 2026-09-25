# -*- coding: utf-8 -*-
"""MASSIVE track: intent classification across (context, utterance) pairs."""
from __future__ import annotations

from .base import BenchmarkTrack, TrackItem


class MASSIVETrack(BenchmarkTrack):
    name = "massive"
    description = "Intent classification (spoken-language-understanding style)."

    def items(self):
        data = [
            ("massive.1", ["play_music", "set_alarm", "get_weather"], "set_alarm"),
            ("massive.2", ["get_weather", "play_music", "send_message"], "get_weather"),
            ("massive.3", ["send_message", "set_alarm", "play_music"], "send_message"),
            ("massive.4", ["set_alarm", "get_weather", "play_music"], "play_music"),
            ("massive.5", ["get_weather", "send_message", "set_alarm"], "get_weather"),
        ]
        return [TrackItem(k, a, c, "intent") for k, a, c in data]
