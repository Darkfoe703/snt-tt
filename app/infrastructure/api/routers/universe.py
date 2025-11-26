# app/infrastructure/api/routes/universe.py
from fastapi import APIRouter, HTTPException
from app.infrastructure.adapters.esi_adapter_universe import ESIClientUniverse

from app.infrastructure.api.cache import cache_response
from app.infrastructure.config.settings import Settings

router = APIRouter(prefix="/universe", tags=["Universe"])
settings = Settings()


# REGIONES
@router.get("/regions")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_all_regions():
    """Obtener todas las regiones"""
    try:
        client = ESIClientUniverse()
        region_ids = await client.get_all_regions()
        return {"total_regions": len(region_ids), "region_ids": region_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/region/{region_id}")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_region_info(region_id: int):
    """Obtener información de una región específica"""
    try:
        client = ESIClientUniverse()
        region_info = await client.get_region_info(region_id)
        return region_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/region/search/{name}")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_region_by_name(name: str):
    """Buscar una región por nombre y obtener su información"""
    try:
        client = ESIClientUniverse()
        region_id = await client.get_region_id_by_name(name)

        if not region_id:
            raise HTTPException(status_code=404, detail=f"Region '{name}' not found")

        region_info = await client.get_region_info(region_id)
        return region_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# CONSTELACIONES
@router.get("/constellations")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_all_constellations():
    """Obtener todas las constelaciones"""
    try:
        client = ESIClientUniverse()
        constellation_ids = await client.get_all_constellations()
        return {
            "total_constellations": len(constellation_ids),
            "constellation_ids": constellation_ids,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/constellation/{constellation_id}")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_constellation_info(constellation_id: int):
    """Obtener información de una constelación específica"""
    try:
        client = ESIClientUniverse()
        constellation_info = await client.get_constellation_info(constellation_id)
        return constellation_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/constellation/search/{name}")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_constellation_by_name(name: str):
    """Buscar una constelación por nombre y obtener su información"""
    try:
        client = ESIClientUniverse()
        constellation_id = await client.get_constellation_id_by_name(name)

        if not constellation_id:
            raise HTTPException(
                status_code=404, detail=f"Constellation '{name}' not found"
            )

        constellation_info = await client.get_constellation_info(constellation_id)
        return constellation_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# SISTEMAS
@router.get("/systems")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_all_systems():
    """Obtener todas los sistemas"""
    try:
        client = ESIClientUniverse()
        system_ids = await client.get_all_systems()
        return {"total_systems": len(system_ids), "system_ids": system_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/system/{system_id}")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_system_info(system_id: int):
    """Obtener información de un sistema específico"""
    try:
        client = ESIClientUniverse()
        system_info = await client.get_system_info(system_id)
        return system_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/system/search/{name}")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_system_by_name(name: str):
    """Buscar un sistema por nombre y obtener su información"""
    try:
        client = ESIClientUniverse()
        system_id = await client.get_system_id_by_name(name)

        if not system_id:
            raise HTTPException(status_code=404, detail=f"System '{name}' not found")

        system_info = await client.get_system_info(system_id)
        return system_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# CORPORACIONES NPC
@router.get("/npcs")
@cache_response(ttl=settings.ENDPOINT_MAX_AGE)
async def get_all_npc_corps():
    """Obtener todas las corporaciones NPC"""
    try:
        client = ESIClientUniverse()
        npc_ids = await client.get_all_npc_corps()
        return {"total_npcs": len(npc_ids), "npc_ids": npc_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
