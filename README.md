#  SNT Trade Tool - A Tool for EVE Online Market 

Herramienta para análisis de mercado de EVE Online.

## Comandos Make

El proyecto incluye un `Makefile` para facilitar las tareas comunes de desarrollo y despliegue.

### Desarrollo

- `make dev`: Iniciar entorno de desarrollo (construye si es necesario).
- `make rebuild`: Reconstruir contenedores sin caché.
- `make shell`: Acceder a la terminal del contenedor `eve-bot-dev`.
- `make logs`: Ver logs en tiempo real.
- `make down`: Detener y remover contenedores.
- `make stop`: Detener contenedores sin removerlos.
- `make rm`: Limpiar todo (contenedores, volúmenes, imágenes).
- `make test`: Ejecutar tests.
- `make lint`: Ejecutar linters.

### Producción

- `make build`: Construir imagen de producción.
- `make prod`: Iniciar entorno de producción.
- `make prod-logs`: Ver logs de producción.
- `make prod-down`: Detener entorno de producción.
- `make clean`: Limpiar sistema docker (prune).

### Ayuda

- `make help`: Mostrar la ayuda con todos los comandos disponibles.

## Comandos CLI

La aplicación incluye una herramienta de línea de comandos para consultar órdenes de mercado directamente.

### Uso

```bash
python -m app.cli.market_cli <region_id> [type_id] [order_type]
```

### Argumentos

- `region_id`: ID de la región a consultar (Requerido).
- `type_id`: ID del tipo de ítem a filtrar (Opcional).
- `order_type`: Tipo de orden a filtrar. Puede ser `all`, `buy` o `sell` (Opcional, por defecto `all`).

### Ejemplos

Consultar todas las órdenes en la región The Forge (10000002):
```bash
python -m app.cli.market_cli 10000002
```

Consultar órdenes de Tritanium (34) en The Forge:
```bash
python -m app.cli.market_cli 10000002 34
```

Consultar solo órdenes de compra de Tritanium en The Forge:
```bash
python -m app.cli.market_cli 10000002 34 buy
```
