SHELL := /bin/sh

.PHONY: help run stop logs ps clean rebuild

help:
	@echo "Available targets:"
	@echo "  make run     - Build and start app + mongo"
	@echo "  make stop    - Stop and remove containers"
	@echo "  make logs    - Tail logs for all services"
	@echo "  make ps      - Show service status"
	@echo "  make clean   - Stop services and remove named volume"
	@echo "  make rebuild - Rebuild and restart services"

run:
	docker compose up --build

stop:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

clean:
	docker compose down -v

rebuild:
	docker compose down
	docker compose up --build
