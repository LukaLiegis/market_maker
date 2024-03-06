import asyncio
import config
import pandas as pd
from binance.client import Client

client = Client(config.api_key, config.api_secret, testnet = False)

symbol = "DOGEUSDT"

class BinanceData:
    def __init__(self):
        self.symbol = symbol
    async def get_orderbook(self):
        return client.get_order_book(symbol = symbol)
    async def get_trades(self):
        return client.get_recent_trades(symbol = symbol)

