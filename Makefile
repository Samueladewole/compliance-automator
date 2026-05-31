# Compliance Automator — developer Makefile

.PHONY: help install lint test eval run clean

help:
	@echo "Targets:"
	@echo "  install    Install Python dependencies"
	@echo "  lint       Run ruff lint + mypy type-check"
	@echo "  test       Run pytest"
	@echo "  eval       Run the evaluation harness against the golden set"
	@echo "  run        Run a sample query through the local CLI"
	@echo "  clean      Remove build / cache artefacts"

install:
	uv venv && uv pip install -e ".[dev,eval]"

lint:
	ruff check agent/ eval/
	mypy agent/

test:
	pytest -v --cov=agent --cov-report=term-missing

eval:
	python eval/run_eval.py

run:
	python -m agent.cli "Show me all privileged-access changes in production for the past 90 days, with the approval trail, mapped to NDPA Section 39."

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache htmlcov dist build *.egg-info
