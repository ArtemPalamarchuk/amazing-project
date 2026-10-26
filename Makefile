.PHONY: lint test

lint:
	pre-commit run --all-files

test:
	pytest -n auto --cov=api --cov-report=term-missing
