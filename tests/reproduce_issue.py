import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.domain.value_objects.market_values import MarketSpread, ISK, Volume

def test_market_spread():
    # Scenario: Normal Market
    # Best Sell (Ask): 100
    # Best Buy (Bid): 90
    # Expected for Station Trading: Profit = 100 - 90 = 10
    
    spread = MarketSpread(
        best_buy=ISK(90.0),
        best_sell=ISK(100.0),
        buy_volume=Volume(1000),
        sell_volume=Volume(1000)
    )
    
    print(f"Best Buy: {spread.best_buy}")
    print(f"Best Sell: {spread.best_sell}")
    print(f"Absolute Spread (Current): {spread.absolute_spread}")
    print(f"Percentage Spread (Current): {spread.percentage_spread}%")
    
    if spread.absolute_spread < 0:
        print("Result: NEGATIVE spread (Current behavior: Bid - Ask)")
    else:
        print("Result: POSITIVE spread (Ask - Bid)")

if __name__ == "__main__":
    test_market_spread()
