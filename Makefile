# Makefile
.PHONY: dev build prod down logs shell stop rm clean

# ARCHIVOS DE COMPOSE
DEV_COMPOSE=docker-compose.dev.yaml
PROD_COMPOSE=docker-compose.prod.yaml

# ----------- Desarrollo -----------

## dev: Iniciar entorno de desarrollo
dev:
	docker compose -f $(DEV_COMPOSE) up -d  --build
	
## rebuild: Reconstruir contenedores sin caché
rebuild:
	docker compose -f $(DEV_COMPOSE) build --no-cache

## shell: Acceder a la terminal del contenedor
shell:
	docker compose -f $(DEV_COMPOSE) exec eve-bot-dev bash

## logs: Ver logs en tiempo real
logs:
	docker compose -f $(DEV_COMPOSE) logs -f

## down: Detener y remover contenedores
down:
	docker compose -f $(DEV_COMPOSE) down

## stop: Detener contenedores sin removerlos
stop:
	docker compose -f $(DEV_COMPOSE) stop

## rm: Limpiar todo (contenedores, volúmenes, imágenes)
rm:
	docker compose -f $(DEV_COMPOSE) down --rmi all --volumes --remove-orphans

# ----------- Producción -----------

# Construir imagen de producción
## build: Construir imagen de producción
build:
	docker build --target production -t eve-bot:prod .

## prod: Iniciar entorno de producción
prod:
	docker compose -f $(PROD_COMPOSE) up -d

## prod-logs: Ver logs de producción
prod-logs:
	docker compose -f $(PROD_COMPOSE) logs -f

## prod-down: Detener entorno de producción
prod-down:
	docker compose -f $(PROD_COMPOSE) down

## clean: Limpiar sistema docker (prune)
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
