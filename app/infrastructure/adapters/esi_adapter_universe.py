# app/infrastructure/adapters/esi_adapter_universe.py
import httpx
from typing import List, Dict, Any
from app.infrastructure.config.settings import Settings


class ESIClientUniverse:
    def __init__(self):
        self.settings = Settings()
        self.base_url = self.settings.ESI_URL

    ### ==================== REGIONES ==================== ###
    # Método para obtener todas las REGIONES
    async def get_all_regions(self) -> List[int]:
        """Obtiene la lista de IDs de todas las regiones."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/universe/regions/")
            return response.json()

    # Método para obtener detalles de una región específica
    async def get_region_info(self, region_id: int) -> Dict[str, Any]:
        """Obtiene información detallada de una región."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/universe/regions/{region_id}/"
            )
            return response.json()

    # Método para resolver nombre de región a ID
    async def get_region_id_by_name(self, region_name: str) -> int | None:
        """Resuelve el nombre de una región a su ID."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/universe/ids/", json=[region_name]
            )
            data = response.json()
            # La respuesta tiene formato: {"regions": [{"id": 123, "name": "Name"}]}
            if "regions" in data and len(data["regions"]) > 0:
                return data["regions"][0]["id"]
            return None

    ### ==================== CONSTELACIONES ==================== ###
    # Método para obtener todas las CONSTELACIONES
    async def get_all_constellations(self) -> List[int]:
        """Obtiene la lista de IDs de todas las constelaciones."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/universe/constellations/")
            return response.json()

    # Método para obtener detalles de una constelación específica
    async def get_constellation_info(self, constellation_id: int) -> Dict[str, Any]:
        """Obtiene información detallada de una constelación."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/universe/constellations/{constellation_id}/"
            )
            return response.json()

    # Método para resolver nombre de constelación a ID
    async def get_constellation_id_by_name(self, constellation_name: str) -> int | None:
        """Resuelve el nombre de una constelación a su ID."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/universe/ids/", json=[constellation_name]
            )
            data = response.json()
            # La respuesta tiene formato: {"constellations": [{"id": 123, "name": "Name"}]}
            if "constellations" in data and len(data["constellations"]) > 0:
                return data["constellations"][0]["id"]
            return None

    ### ==================== SISTEMAS ==================== ###
    # Método para obtener todas los SISTEMAS
    async def get_all_systems(self) -> List[int]:
        """Obtiene la lista de IDs de todas los sistemas."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/universe/systems/")
            return response.json()

    # Método para obtener detalles de un sistema específico
    async def get_system_info(self, system_id: int) -> Dict[str, Any]:
        """Obtiene información detallada de un sistema."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/universe/systems/{system_id}/"
            )
            return response.json()

    # Método para resolver nombre de sistema a ID
    async def get_system_id_by_name(self, system_name: str) -> int | None:
        """Resuelve el nombre de un sistema a su ID."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/universe/ids/", json=[system_name]
            )
            data = response.json()
            # La respuesta tiene formato: {"systems": [{"id": 123, "name": "Name"}]}
            if "systems" in data and len(data["systems"]) > 0:
                return data["systems"][0]["id"]
            return None


##########################################################################33
