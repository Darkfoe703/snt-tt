# app/infrastructure/api/web/routes/views.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.infrastructure.config.templates import templates
from app.infrastructure.api.routers.dependencies import get_market_analyzer
from app.core.domain.value_objects.market_values import Volume
from app.core.domain.value_objects.regions import RegionValueObject
from app.core.domain.constants.universe import Region
import math

router = APIRouter(tags=["Web"])

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard principal"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "Dashboard - SNT Trade Tool"
    })

@router.get("/market", response_class=HTMLResponse)
async def market_view(
    request: Request,
    region_id: int = None,
    min_volume: int = 1,
    min_spread: float = 2.0,
    page: int = 1,
    limit: int = 100,
    analysis_limit: int = 250,
    submitted: bool = False,
    analyzer = Depends(get_market_analyzer) 
):
    """Vista del mercado"""
    results = None
    total_pages = 0

    # Si no se proporciona region_id, usa The Forge por defecto
    if region_id is None:
        region_id = Region.THE_FORGE.value
    
    if submitted and region_id:
        offset = (page - 1) * limit
        results = await analyzer.analyze_region_profit(
            region_id=region_id,
            min_volume=Volume(min_volume),
            min_spread=min_spread,
            limit=limit,
            offset=offset,
            analysis_limit=analysis_limit,
        )
        total_pages = math.ceil(results.total_opportunities / limit)

    context = {
        "request": request,
        "title": "Mercado - SNT Trade Tool",
        "results": results,
        "region_id": region_id,
        "regions": RegionValueObject.get_choices(),
        "min_volume": min_volume,
        "min_spread": min_spread,
        "page": page,
        "limit": limit,
        "analysis_limit": analysis_limit,
        "total_pages": total_pages
    }

    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("partials/market_results.html", context)

    return templates.TemplateResponse("market.html", context)

@router.get("/alerts", response_class=HTMLResponse)
async def alerts_view(request: Request):
    """Vista de alertas"""
    return templates.TemplateResponse("alerts.html", {
        "request": request,
        "title": "Alertas - SNT Trade Tool"
    })

@router.get("/regions", response_class=HTMLResponse)
async def regions_view(request: Request):
    """Vista de regiones"""
    return templates.TemplateResponse("regions.html", {
        "request": request,
        "title": "Regiones - SNT Trade Tool"
    })