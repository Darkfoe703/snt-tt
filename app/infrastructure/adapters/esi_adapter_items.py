# app/infrastructure/adapters/esi_adapter_items.py
import httpx
import asyncio
from typing import List, Dict, Any

from app.infrastructure.config.settings import Settings


class ESIClientItems:
    def __init__(self):
        self.settings = Settings()
        self.base_url = self.settings.ESI_URL

    async def get_all_type_ids(self) -> List[int]:
        """
        Obtiene TODOS los IDs de tipos (items) del juego.
        Maneja la paginación de ESI automáticamente usando asyncio.gather.
        """
        all_ids = []
        async with httpx.AsyncClient() as client:
            # Primera llamada para obtener datos y número de páginas
            response = await client.get(f"{self.base_url}/universe/types/")
            all_ids.extend(response.json())

            total_pages = int(response.headers.get("X-Pages", 1))

            if total_pages > 1:
                tasks = []
                for page in range(2, total_pages + 1):
                    tasks.append(
                        client.get(
                            f"{self.base_url}/universe/types/", params={"page": page}
                        )
                    )

                responses = await asyncio.gather(*tasks)

                for response in responses:
                    all_ids.extend(response.json())

        return all_ids

    async def get_type_info(self, type_id: int) -> Dict[str, Any]:
        """Obtiene información detallada de un tipo (item) específico."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/universe/types/{type_id}/")
            return response.json()

    # Método para buscar items por nombre
    async def search_type_ids(self, type_name: str) -> List[int]:
        """
        Busca items por nombre exacto usando /universe/ids/.
        Por ahora solo soporta coincidencia exacta.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/universe/ids/", json=[type_name]
            )
            data = response.json()
            # La respuesta tiene formato: {"inventory_types": [{"id": 123, "name": "Name"}]}
            if "inventory_types" in data:
                return [item["id"] for item in data["inventory_types"]]
            return []
