import asyncio
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.infrastructure.adapters.esi_adapter_market import ESIClientMarket
from app.infrastructure.adapters.esi_adapter_universe import ESIClientUniverse
from app.infrastructure.adapters.esi_adapter_items import ESIClientItems
from app.core.domain.services.market_analyzer import MarketAnalyzer
from app.core.domain.value_objects.market_values import Volume

async def debug_analysis():
    print("🚀 Starting Debug Analysis...")
    
    # Instantiate clients
    market_client = ESIClientMarket()
    universe_client = ESIClientUniverse()
    items_client = ESIClientItems()
    
    analyzer = MarketAnalyzer(market_client, universe_client, items_client)
    
    # Parameters from user request
    region_id = 10000002 # The Forge
    min_volume = Volume(1)
    min_spread = 1.0
    limit = 20
    analysis_limit = 100
    
    print(f"📊 Parameters: Region={region_id}, MinVolume={min_volume}, MinSpread={min_spread}, Limit={limit}, AnalysisLimit={analysis_limit}")
    
    try:
        # Manually run parts of analyze_region_profit to debug
        print(f"🔍 Fetching orders for region {region_id}...")
        all_orders = await market_client.get_market_orders(region_id)
        print(f"✅ Fetched {len(all_orders)} total orders.")
        
        if not all_orders:
            print("❌ No orders returned from ESI.")
            return

        orders_by_type = analyzer._group_orders_by_type(all_orders)
        print(f"📦 Grouped into {len(orders_by_type)} unique item types.")
        
        print(f"🕵️ Analyzing first {analysis_limit} items...")
        
        analyzed_count = 0
        opportunities = []
        
        for type_id, orders in list(orders_by_type.items())[:analysis_limit]:
            analyzed_count += 1
            print(f"  [{analyzed_count}] Analyzing TypeID {type_id} ({len(orders)} orders)...")
            
            # Check buy/sell split
            buy_orders = [o for o in orders if o.get('is_buy_order')]
            sell_orders = [o for o in orders if not o.get('is_buy_order')]
            
            if not buy_orders or not sell_orders:
                print(f"    ⚠️ Skipped: Missing buy or sell orders (Buy: {len(buy_orders)}, Sell: {len(sell_orders)})")
                continue
                
            market_spread = analyzer._calculate_market_spread(buy_orders, sell_orders)
            
            print(f"    💰 Spread: {market_spread.percentage_spread:.2f}% (Min: {min_spread}%)")
            print(f"    📦 Volume: {market_spread.tradable_volume} (Min: {min_volume})")
            
            if not market_spread.is_viable(min_spread, min_volume):
                print("    ❌ Not viable.")
                continue
            
            print("    ✅ VIABLE OPPORTUNITY FOUND!")
            opportunity = await analyzer._analyze_item_profit(
                region_id, type_id, orders, min_volume, min_spread
            )
            if opportunity:
                opportunities.append(opportunity)
        
        print(f"\n🏁 Finished. Found {len(opportunities)} opportunities.")
        
    except Exception as e:
        print(f"💥 Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_analysis())
