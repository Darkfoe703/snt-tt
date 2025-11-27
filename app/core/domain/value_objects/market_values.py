# app/core/domain/value_objects/market_values.py
from dataclasses import dataclass
from typing import NewType

MIN_SPREAD_PERCENTAGE = 5.0
MIN_VOLUME = 100

# Type Aliases para mayor claridad
ISK = NewType('ISK', float)
ItemId = NewType('ItemId', int)
RegionId = NewType('RegionId', int)
Volume = NewType('Volume', int)
ConfidenceScore = NewType('ConfidenceScore', float)

@dataclass(frozen=True)
class PricePoint:
    """Punto de precio con volumen"""
    price: ISK
    volume: Volume
    
    def value(self) -> ISK:
        """Valor total en ISK"""
        return ISK(self.price * self.volume)

@dataclass(frozen=True)
class MarketSpread:
    """Spread entre precios de compra y venta"""
    best_buy: ISK
    best_sell: ISK
    buy_volume: Volume
    sell_volume: Volume
    
    @property
    def absolute_spread(self) -> ISK:
        """Spread absoluto en ISK"""
        return ISK(self.best_sell - self.best_buy)
    
    @property
    def percentage_spread(self) -> float:
        """Spread como porcentaje del precio de venta"""
        if self.best_sell > 0:
            return (self.absolute_spread / self.best_sell) * 100
        return 0.0
    
    @property
    def tradable_volume(self) -> Volume:
        """Volumen que se puede realmente tradear"""
        return Volume(min(self.buy_volume, self.sell_volume))
    
    def is_viable(self, min_spread_percentage: float = MIN_SPREAD_PERCENTAGE, min_volume: Volume = MIN_VOLUME) -> bool:
        """Determina si el spread es viable para trading"""
        return (self.percentage_spread >= min_spread_percentage and 
                self.tradable_volume >= min_volume)