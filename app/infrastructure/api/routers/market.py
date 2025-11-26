# app/infrastructure/api/routes/market.py
from app.core.domain.value_objects.regions import RegionValueObject
from app.core.domain.value_objects.systems import SystemValueObject
from fastapi import APIRouter, HTTPException, Depends
from app.infrastructure.adapters.esi_adapter_market import ESIClientMarket
from app.infrastructure.api.cache import cache_response
from app.infrastructure.config.settings import Settings

router = APIRouter(prefix="/market", tags=["Market"])
settings = Settings()


# Endpoint para obtener las órdenes del mercado de una región específica
@router.get("/orders")
@cache_response(ttl=settings.ENDPOINT_MIN_AGE)
async def get_market_orders(
    region_id: int = RegionValueObject.THE_FORGE.value, type_id: int = 44992, order_type: str = "all"
):
    """
    Endpoint para obtener las órdenes del mercado de una región específica.
    order_type: 'buy', 'sell', 'all'
    """
    try:
        client = ESIClientMarket()
        orders = await client.get_market_orders(region_id, type_id, order_type)

        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ESI Error: {str(e)}")


# Endpoint para obtener las ordenes del mercado de un SISTEMA especifico
@router.get("/orders_by_system")
@cache_response(ttl=settings.ENDPOINT_MIN_AGE)
async def get_market_orders_by_system(
    system_id: int = SystemValueObject.JITA.value, type_id: int = None, order_type: str = "all"
):
    """
    Endpoint para obtener las órdenes del mercado de un sistema específico.
    order_type: 'buy', 'sell', 'all'
    """
    try:
        client = ESIClientMarket()
        orders = await client.get_market_orders_by_system(
            system_id, type_id, order_type
        )

        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ESI Error: {str(e)}")


from app.infrastructure.api.routers.dependencies import get_market_analyzer

@router.get("/analyze/{region_id}")
@cache_response(ttl=settings.ENDPOINT_MIN_AGE)
async def analyze_market(
    region_id: int,
    min_volume: int = 100,
    min_spread: float = 5.0,
    limit: int = 20,
    analysis_limit: int = 100,
    analyzer = Depends(get_market_analyzer)
):
    """
    Analiza el mercado de una región en busca de oportunidades de profit.
    """
    try:
        from app.core.domain.value_objects.market_values import Volume
        
        result = await analyzer.analyze_region_profit(
            region_id=region_id,
            min_volume=Volume(min_volume),
            min_spread=min_spread,
            limit=limit,
            analysis_limit=analysis_limit
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis Error: {str(e)}")
