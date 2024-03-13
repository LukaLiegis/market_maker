import numpy as np
from src.sharedstate import SharedState
from typing import Dict, List

class BinanceTradesHandler:
    def __init__(self):
        self.ss = SharedState()

    def initialize(self, data: List[Dict]) -> None:
        '''
        Initializes the shared state with historical trade data
        :param data: a list of dictionaries containing information about a single trade
        '''
        for row in data:
            time = float(row["time"])
            price = float(row["price"])
            qty = float(row["qty"])
            side = 1.0 if row['isBuyerMaker'] else 0.0
            new_trade = np.array([[time, side, price, qty]])
            self.ss.binance_trades.append(new_trade)

    def process(self, recv: Dict) -> None:
        """
        Processes a new incoming trade message and updates the shared state.
        :param recv: A dictionary containing information about a new trade.
        """
        time = float(recv["data"]["T"])
        price = float(recv["data"]["p"])
        qty = float(recv["data"]["q"])
        side = 1.0 if recv["data"]["m"] else 0.0
        new_trade = np.array([[time, side, price, qty]])
        self.ss.binance_trades.append(new_trade)
        self.ss.binance_last_price = float(price)