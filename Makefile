.PHONY: up down test lint format terraform-init terraform-plan

up:
	docker compose up --build

down:
	docker compose down

test:
	cd backend && python -m pytest

lint:
	cd backend && python -m ruff check .

format:
	cd backend && python -m ruff format .

terraform-init:
	cd infra/azure && terraform init

terraform-plan:
	cd infra/azure && terraform plan
