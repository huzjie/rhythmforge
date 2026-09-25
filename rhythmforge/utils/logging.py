# -*- coding: utf-8 -*-
"""Small logging shim."""
from __future__ import annotations

import logging
import sys


def get_logger(name: str = "rhythmforge", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stderr)
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(h)
    logger.setLevel(level)
    return logger
