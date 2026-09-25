.PHONY: install test lint doctor demo bench clean

PY ?= python

install:
	$(PY) -m pip install -e .

test:
	$(PY) -m unittest discover -s tests -t .

lint:
	$(PY) -m compileall rhythmforge examples tests

doctor:
	$(PY) -m rhythmforge.cli.main doctor

demo:
	$(PY) -m rhythmforge.cli.main demo

bench:
	$(PY) -m rhythmforge.cli.main bench

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist *.egg-info .pytest_cache
