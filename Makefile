
.PHONY: help lint format format-check typecheck security radon-cc radon-mi radon-hal radon-raw check

help:
	@echo Available commands:
	@echo make lint - Check code with Ruff
	@echo make format - Format code with Ruff
	@echo make format-check - Check formatting
	@echo make typecheck - Check types with Mypy
	@echo make security - Security analysis with Bandit
	@echo make radon-cc - Cyclomatic complexity
	@echo make radon-mi - Maintainability index
	@echo make radon-hal - Halstead metrics
	@echo make radon-raw - Raw metrics
	@echo make check - Run basic quality checks

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

format-check:
	poetry run ruff format --check .

typecheck:
	poetry run mypy src

security:
	poetry run bandit -r src

radon-cc:
	poetry run radon cc src -s -a

radon-mi:
	poetry run radon mi src -s

radon-hal:
	poetry run radon hal src

radon-raw:
	poetry run radon raw src

check: lint format-check