.PHONY: help lint test test-js e2e

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-10s %s\n", $$1, $$2}'

lint:  ## pre-commit on all files (ruff, eslint, prettier, migrations check)
	pre-commit run --all-files

test:  ## backend unit tests with coverage (needs db running)
	pytest -n auto --cov=api --cov-report=term-missing

test-js:  ## frontend tests (vitest)
	cd frontend && npm test

# Extra pytest flags go through E2E_ARGS, e.g. CI passes --tracing retain-on-failure.
E2E_ARGS ?=

# Needs a running, migrated stack:
#   docker compose up -d --build --wait
#   docker compose exec backend python manage.py migrate
e2e:  ## seed + e2e tests (needs running, migrated stack)
	docker compose exec -T -e ALLOW_E2E_SEED=1 backend python manage.py seed_e2e
	pytest tests-e2e --base-url http://localhost:5173 --retries 2 -n 2 $(E2E_ARGS)
	