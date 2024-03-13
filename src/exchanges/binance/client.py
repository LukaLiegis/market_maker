from binance.client import Client
from typing import Dict
from src.sharedstate import SharedState

class BinancePublicData:
    """
    Retrieves data from Binance such as orderbook, trades, and candlestick data.
    """
    def __init__(self, ss: SharedState):
        self.ss = ss
        self.symbol: str = self.ss.binance_symbol
        self.client = Client()

    async def get_orderbook(self, limit:int) -> Dict:
        return self.client.futures_order_book(symbol=self.symbol, limit=limit)

    async def get_trades(self, limit:int) -> Dict:
        return self.client.get_recent_trades(symbol=self.symbol, limit=limit)

    async def get_candlestick(self, limit:int, interval:str) -> Dict:
        return self.client.get_klines(symbol=self.symbol, interval=interval, limit=limit)

    async def instrument_info(self) -> Dict:
        return self.client.get_symbol_info(symbol=self.symbol)