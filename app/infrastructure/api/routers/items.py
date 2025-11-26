# app/infrastructure/api/routes/items.py
from fastapi import APIRouter, HTTPException
from app.infrastructure.adapters.esi_adapter_items import ESIClientItems
from app.infrastructure.api.cache import cache_response
from app.infrastructure.config.settings import Settings

router = APIRouter(prefix="/items", tags=["Items"])
settings = Settings()


@router.get("/items", response_model=list[int])
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_items():
    """Endpoint para obtener todos los items"""
    try:
        client = ESIClientItems()
        items = await client.get_all_type_ids()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ESI Error: {str(e)}")


# Obtener información de un item específico
@router.get("/items/{item_id}", response_model=dict)
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_item(item_id: int):
    try:
        client = ESIClientItems()
        item_info = await client.get_type_info(item_id)
        return item_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ESI Error: {str(e)}")


# Buscar un item por nombre
@router.get("/items/search/{name}", response_model=list[int])
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def search_item(name: str):
    try:
        client = ESIClientItems()
        item_ids = await client.search_type_ids(name)
        return item_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ESI Error: {str(e)}")
