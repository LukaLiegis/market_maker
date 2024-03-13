import numpy as np
from typing import Dict
from src.exchanges.common.localorderbook import BaseOrderBook

class BinanceOrderBook(BaseOrderBook):
    def process_snapshot(self, snapshot: Dict) -> None:
        self.asks = np.array(snapshot['asks'], dtype=float)
        self.bids = np.array(snapshot['bids'], dtype=float)
        self.sort_book()

    def process(self, recv: Dict) -> None:
        """
        Processes real time updates to the orderbook
        :param recv: a dictionary containing updates
        """
        asks = np.array(recv['data']['a'], dtype=float)
        bids = np.array(recv['data']['b'], dtype=float)
        self.asks = self.update_book(self.asks, asks)
        self.bids = self.update_book(self.bids)
        self.sort_book()

class BinanceBBAHandler:
    """
    Handler for processing the best bid and ask prices and volumes.
    """
    def __init__(self, ss) -> None:
        self.ss = ss

    def process(self, recv: Dict) -> None:
        """
        Processes real time updates to the best bid and ask.
        :param recv: A dictionary containing latest bid and ask prices and volumes.
        """
        self.ss.binance_bba[0, 0] = float(recv['data']['b'])
        self.ss.binance_bba[0, 1] = float(recv['data']['B'])
        self.ss.binance_bba[1, 0] = float(recv['data']['a'])
        self.ss.binance_bba[1, 1] = float(recv['data']['A'])
