.PHONY: lint test e2e

lint:
	pre-commit run --all-files

test:
	pytest -n auto --cov=api --cov-report=term-missing

# Needs a running, migrated stack:
#   docker compose up -d --build --wait
#   docker compose exec backend python manage.py migrate
e2e:
	docker compose exec -e ALLOW_E2E_SEED=1 backend python manage.py seed_e2e
	pytest tests-e2e --base-url http://localhost:5173 --retries 2 -n 2
