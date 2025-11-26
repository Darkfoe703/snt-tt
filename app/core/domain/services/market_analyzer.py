# app/core/domain/services/market_analyzer.py
import asyncio
from typing import List, Dict
from datetime import datetime
from app.core.domain.entities.market_analysis import (
    ProfitOpportunity, 
    MarketAnalysisResult
)
from app.core.domain.value_objects.market_values import (
    MarketSpread, ISK, Volume, ConfidenceScore
)

class MarketAnalyzer:
    def __init__(self, market_client, universe_client, items_client):
        self.market_client = market_client
        self.universe_client = universe_client
        self.items_client = items_client
    
    async def analyze_region_profit(
        self, 
        region_id: int, 
        min_volume: Volume = Volume(100), 
        min_spread: float = 5.0,
        limit: int = 20,
        offset: int = 0,
        analysis_limit: int = 100
    ) -> MarketAnalysisResult:
        """Analiza oportunidades de profit en una región"""
        print(f"🔍 Analizando región {region_id}...")
        
        # Obtener todas las órdenes de la región
        all_orders = await self.market_client.get_market_orders(region_id)
        
        # Agrupar órdenes por type_id
        orders_by_type = self._group_orders_by_type(all_orders)
        
        # Analizar cada tipo de item
        opportunities = []
        total_analyzed = 0
        
        for type_id, orders in list(orders_by_type.items())[:analysis_limit]:  # Limitar para performance
            total_analyzed += 1
            try:
                opportunity = await self._analyze_item_profit(
                    region_id, type_id, orders, min_volume, min_spread
                )
                if opportunity:
                    opportunities.append(opportunity)
            except Exception as e:
                print(f"⚠️ Error analizando item {type_id}: {e}")
                continue
        
        # Ordenar por mejor spread
        opportunities.sort(key=lambda x: x.spread_percentage, reverse=True)
        
        total_opportunities = len(opportunities)
        
        region_name = await self._get_region_name(region_id)
        
        return MarketAnalysisResult(
            region_id=region_id,
            region_name=region_name,
            opportunities=opportunities[offset : offset + limit],
            total_items_analyzed=total_analyzed,
            total_opportunities=total_opportunities,
            analysis_timestamp=datetime.now(),
            parameters={
                'min_volume': min_volume,
                'min_spread': min_spread,
                'limit': limit,
                'offset': offset,
                'analysis_limit': analysis_limit
            }
        )
    
    def _group_orders_by_type(self, orders: List[Dict]) -> Dict[int, List[Dict]]:
        """Agrupa órdenes por type_id"""
        grouped = {}
        for order in orders:
            type_id = order.get('type_id')
            if type_id not in grouped:
                grouped[type_id] = []
            grouped[type_id].append(order)
        return grouped
    
    async def _analyze_item_profit(
        self, 
        region_id: int, 
        type_id: int, 
        orders: List[Dict], 
        min_volume: Volume, 
        min_spread: float
    ) -> ProfitOpportunity:
        """Analiza profit para un item específico"""
        # Separar órdenes de compra y venta
        buy_orders = [o for o in orders if o.get('is_buy_order')]
        sell_orders = [o for o in orders if not o.get('is_buy_order')]
        
        if not buy_orders or not sell_orders:
            return None
        
        # Calcular market spread
        market_spread = self._calculate_market_spread(buy_orders, sell_orders)
        
        # Verificar viabilidad
        if not market_spread.is_viable(min_spread, min_volume):
            return None
        
        # Obtener nombres
        item_name = await self._get_item_name(type_id)
        region_name = await self._get_region_name(region_id)
        
        # Calcular confianza
        confidence = self._calculate_confidence(market_spread)
        
        return ProfitOpportunity(
            type_id=type_id,
            name=item_name,
            region_id=region_id,
            region_name=region_name,
            best_buy_price=market_spread.best_buy,
            best_sell_price=market_spread.best_sell,
            spread=market_spread.absolute_spread,
            spread_percentage=market_spread.percentage_spread,
            buy_volume=market_spread.buy_volume,
            sell_volume=market_spread.sell_volume,
            confidence=confidence,
            updated_at=datetime.now()
        )
    
    def _calculate_market_spread(self, buy_orders: List[Dict], sell_orders: List[Dict]) -> MarketSpread:
        """Calcula el spread de mercado"""
        best_buy = ISK(max([o.get('price', 0) for o in buy_orders]))
        best_sell = ISK(min([o.get('price', 0) for o in sell_orders]))
        buy_volume = Volume(sum([o.get('volume_remain', 0) for o in buy_orders]))
        sell_volume = Volume(sum([o.get('volume_remain', 0) for o in sell_orders]))
        
        return MarketSpread(
            best_buy=best_buy,
            best_sell=best_sell,
            buy_volume=buy_volume,
            sell_volume=sell_volume
        )
    
    def _calculate_confidence(self, market_spread: MarketSpread) -> ConfidenceScore:
        """Calcula la confianza basada en volumen y spread"""
        volume_confidence = min(market_spread.tradable_volume / 1000, 1.0)
        spread_confidence = min(market_spread.percentage_spread / 20, 1.0)  # Máx 20% spread
        
        # Promedio ponderado
        confidence = (volume_confidence * 0.6) + (spread_confidence * 0.4)
        return ConfidenceScore(confidence)
    
    async def _get_item_name(self, type_id: int) -> str:
        """Obtiene el nombre de un item"""
        try:
            item_info = await self.items_client.get_type_info(type_id)
            return item_info.get('name', f'Item_{type_id}')
        except:
            return f'Item_{type_id}'
    
    async def _get_region_name(self, region_id: int) -> str:
        """Obtiene el nombre de una región"""
        try:
            region_info = await self.universe_client.get_region_info(region_id)
            return region_info.get('name', f'Region_{region_id}')
        except:
            return f'Region_{region_id}'