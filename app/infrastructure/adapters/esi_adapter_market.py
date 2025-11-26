# app/infrastructure/adapters/esi_adapter_market.py
import httpx
import asyncio
from typing import List, Dict, Any

from app.infrastructure.config.settings import Settings


class ESIClientMarket:
    def __init__(self):
        self.settings = Settings()
        self.base_url = self.settings.ESI_URL

    # Método para obtener las ordenes del mercado de una REGION específica
    async def get_market_orders(
        self, region_id: int, type_id: int = None, order_type: str = "all"
    ) -> List[Dict[str, Any]]:
        """Obtiene las ordenes del mercado de una región específica. Soporta paginación y filtrado por tipo de orden."""
        all_orders = []
        params = {"order_type": order_type}
        if type_id:
            params["type_id"] = type_id

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/markets/{region_id}/orders/", params=params
            )
            all_orders.extend(response.json())

            total_pages = int(response.headers.get("X-Pages", 1))
            if total_pages > 1:
                tasks = []
                for page in range(2, total_pages + 1):
                    p = params.copy()
                    p["page"] = page
                    tasks.append(
                        client.get(
                            f"{self.base_url}/markets/{region_id}/orders/", params=p
                        )
                    )
                responses = await asyncio.gather(*tasks)
                for r in responses:
                    all_orders.extend(r.json())
        return all_orders

    # Método para obtener las ordenes del mercado de un SISTEMA específico
    async def get_market_orders_by_system(
        self, system_id: int, type_id: int = None, order_type: str = "all"
    ) -> List[Dict[str, Any]]:
        """Obtiene las ordenes del mercado de un sistema específico. Opcionalmente filtra por tipo."""
        from app.infrastructure.adapters.esi_adapter_universe import ESIClientUniverse

        universe_client = ESIClientUniverse()

        # 1. Obtener info del sistema para saber la constelación
        system_info = await universe_client.get_system_info(system_id)
        if not system_info or "constellation_id" not in system_info:
            return []

        constellation_id = system_info["constellation_id"]

        # 2. Obtener info de la constelación para saber la región
        constellation_info = await universe_client.get_constellation_info(
            constellation_id
        )
        if not constellation_info or "region_id" not in constellation_info:
            return []

        region_id = constellation_info["region_id"]

        # 3. Obtener órdenes de la región (filtrando por tipo si se especifica)
        # Esto es mucho más eficiente si se da el type_id
        all_region_orders = await self.get_market_orders(region_id, type_id, order_type)

        # 4. Filtrar por system_id
        system_orders = [
            order for order in all_region_orders if order.get("system_id") == system_id
        ]

        return system_orders
