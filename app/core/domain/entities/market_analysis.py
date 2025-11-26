# app/core/domain/entities/market_analysis.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class MarketOrderSummary:
    """Resumen de órdenes de mercado para un item específico"""
    type_id: int
    name: str
    best_buy: float  # Mejor precio de compra (más alto)
    best_sell: float  # Mejor precio de venta (más bajo)
    buy_volume: int
    sell_volume: int
    spread: float  # Diferencia entre compra y venta
    spread_percentage: float  # Spread como porcentaje
    total_volume: int
    
    def is_profitable(self, min_spread_percentage: float = 5.0) -> bool:
        """Determina si el spread es suficientemente rentable"""
        return self.spread_percentage >= min_spread_percentage
    
    def has_sufficient_volume(self, min_volume: int = 100) -> bool:
        """Verifica si tiene volumen suficiente para operar"""
        return self.buy_volume >= min_volume and self.sell_volume >= min_volume

@dataclass(frozen=True)
class ProfitOpportunity:
    """Oportunidad de profit identificada"""
    type_id: int
    name: str
    region_id: int
    region_name: str
    best_buy_price: float
    best_sell_price: float
    spread: float
    spread_percentage: float
    buy_volume: int
    sell_volume: int
    confidence: float  # 0-1 basado en volumen y consistencia
    updated_at: datetime
    
    def calculate_profit_per_unit(self, tax_rate: float = 0.0) -> float:
        """Calcula el profit por unidad después de impuestos"""
        return self.spread * (1 - tax_rate)
    
    def calculate_total_profit_potential(self, tax_rate: float = 0.0) -> float:
        """Calcula el profit potencial total basado en volumen disponible"""
        profit_per_unit = self.calculate_profit_per_unit(tax_rate)
        tradable_volume = min(self.buy_volume, self.sell_volume)
        return profit_per_unit * tradable_volume
    
    def is_high_confidence(self) -> bool:
        """Determina si es una oportunidad de alta confianza"""
        return self.confidence >= 0.7

@dataclass(frozen=True)
class MarketAnalysisResult:
    """Resultado completo del análisis de mercado"""
    region_id: int
    region_name: str
    opportunities: list[ProfitOpportunity]
    total_items_analyzed: int
    total_opportunities: int
    analysis_timestamp: datetime
    parameters: dict
    
    @property
    def top_opportunity(self) -> Optional[ProfitOpportunity]:
        """Retorna la mejor oportunidad"""
        return self.opportunities[0] if self.opportunities else None
    
    @property
    def high_confidence_opportunities(self) -> list[ProfitOpportunity]:
        """Retorna solo oportunidades de alta confianza"""
        return [opp for opp in self.opportunities if opp.is_high_confidence()]
    
    def get_opportunities_above_spread(self, min_spread: float) -> list[ProfitOpportunity]:
        """Filtra oportunidades por spread mínimo"""
        return [opp for opp in self.opportunities if opp.spread_percentage >= min_spread]