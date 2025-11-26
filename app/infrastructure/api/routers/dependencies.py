from app.infrastructure.adapters.esi_adapter_market import ESIClientMarket
from app.infrastructure.adapters.esi_adapter_universe import ESIClientUniverse
from app.core.domain.services.market_analyzer import MarketAnalyzer

def get_market_analyzer() -> MarketAnalyzer:
    """Dependency provider for MarketAnalyzer"""
    from app.infrastructure.adapters.esi_adapter_items import ESIClientItems
    
    market_client = ESIClientMarket()
    universe_client = ESIClientUniverse()
    items_client = ESIClientItems()
    return MarketAnalyzer(market_client, universe_client, items_client)
