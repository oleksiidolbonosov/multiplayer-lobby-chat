.PHONY: up test lint build

up:
	docker-compose up --build

test:
	pytest -q

lint:
	black .
	ruff check .

build:
	docker build -t mlc-api ./deploy/api
