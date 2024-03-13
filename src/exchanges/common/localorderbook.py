import numpy as np
from numpy.typing import NDArray
from typing import Dict

class BaseOrderBook:
    def __init__(self) -> None:
        self.asks = np.empty((0,2), dtype=np.float64)
        self.bids = np.empty((0,2), dtype=np.float64)

    def sort_book(self) -> None:
        """
        Sorts the ask order in ascending order by price and the bid order in descending order by price.
        """
        self.asks = self.asks[self.asks[:, 0].argsort()][:500]
        self.bids = self.bids[self.bids[:, 0].argsort()[::-1]][:500]

    def update_book(self, asks_or_bids: NDArray, data: NDArray) -> NDArray:
        """
        Updates the specified orderbook with new data
        :param asks_or_bids: current asks and bids
        :param data: new data to be integrated
        :return: updated orderbook
        """
        for price, qty in data:
            asks_or_bids = asks_or_bids[asks_or_bids[:, 0] != price]
            if qty > 0:
                asks_or_bids = np.vstack((asks_or_bids, np.array([price, qty])))
        return asks_or_bids