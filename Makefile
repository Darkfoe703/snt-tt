# Makefile
.PHONY: dev build prod down logs shell stop rm clean

# ARCHIVOS DE COMPOSE
DEV_COMPOSE=docker-compose.dev.yaml
PROD_COMPOSE=docker-compose.prod.yaml

# ----------- Desarrollo -----------

dev:
	docker compose -f $(DEV_COMPOSE) up -d  --build
	
rebuild:
	docker compose -f $(DEV_COMPOSE) build --no-cache

shell:
	docker compose -f $(DEV_COMPOSE) exec eve-bot-dev bash

logs:
	docker compose -f $(DEV_COMPOSE) logs -f

down:
	docker compose -f $(DEV_COMPOSE) down

stop:
	docker compose -f $(DEV_COMPOSE) stop

rm:
	docker compose -f $(DEV_COMPOSE) down --rmi all --volumes --remove-orphans

# ----------- Producción -----------

# Construir imagen de producción
build:
	docker build --target production -t eve-bot:prod .

prod:
	docker compose -f $(PROD_COMPOSE) up -d

prod-logs:
	docker compose -f $(PROD_COMPOSE) logs -f

prod-down:
	docker compose -f $(PROD_COMPOSE) down

clean:
	docker system prune -af

# ----------- Utilidades -----------


## test: Ejecutar tests (cuando los tengas)
test:
	docker compose -f $(DEV_COMPOSE) exec eve-bot-dev poetry run pytest

## lint: Ejecutar linters (cuando los configures)
lint:
	docker compose -f $(DEV_COMPOSE) exec eve-bot-dev poetry run black .
	docker compose -f $(DEV_COMPOSE) exec eve-bot-dev poetry run flake8

## help: Mostrar esta ayuda
help:
	@echo "Comandos disponibles:"
	@echo ""
	@sed -n 's/^##//p' $(MAKEFILE_LIST) | column -t -s ':' | sed -e 's/^/ /'
