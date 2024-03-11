import asyncio
from src.exchanges.binance import data

live = data.trades()
print(live)