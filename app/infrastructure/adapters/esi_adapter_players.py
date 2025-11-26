import httpx
from typing import List, Dict, Any
from app.infrastructure.config.settings import Settings


class ESIClientPlayers:
    def __init__(self):
        self.settings = Settings()
        self.base_url = self.settings.ESI_URL

    # Método para obtener todas las CORPS NPC
    async def get_all_npc_corps(self) -> List[int]:
        """Obtiene la lista de IDs de todas las corporaciones NPC."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/corporations/npccorps/")
            return response.json()
