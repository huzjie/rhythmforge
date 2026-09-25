# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="rhythmforge",
    version="1.0.0",
    description="Realtime Decision Engine & Lookahead Safety Planner",
    packages=find_packages(include=["rhythmforge", "rhythmforge.*"]),
    python_requires=">=3.9",
    entry_points={"console_scripts": ["rhythmforge=rhythmforge.cli.main:main"]},
)
