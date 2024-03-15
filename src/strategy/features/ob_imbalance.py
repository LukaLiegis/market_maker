import numpy as np
from numba import njit
from numpy.typing import NDArray
from src.indicators.ema import ema_weights

@njit(cache=True)
def orderbook_imbalance(bids: NDArray, asks: NDArray, depths: NDArray) -> float:
    """
    Calculates the geometrically weighted order book imbalance across different price depths.
    :param bids: An array of bids prices and quantities.
    :param asks: An array of ask prices and quantities.
    :param depths: An array of price depth (in basis points) at which to calculate imbalance.
    :return: The geometrically weighted imbalance across specified price depths.
    """
    num_depths = depths.size
    depths = depths / 1e-4 # Converting from BPS to decimal
    weights = ema_weights(num_depths)
    imbalance = np.empty(num_depths, dtype=np.float64)

    bid_p, bid_q = bids.T
    ask_p, ask_q = asks.T
    best_bid_p, best_ask_p = bid_p[0], ask_p[0]

    for i in range(num_depths):
        min_bid = best_bid_p * (1 - depths[i])
        max_ask = best_ask_p * (1 + depths[i])

        num_bids_within_depth = bid_p[bid_p >= min_bid].size
        num_asks_within_depth = ask_p[ask_p <= max_ask].size
        total_bid_size_within_depth = np.sum(bid_q[:num_bids_within_depth])
        total_ask_size_within_depth = np.sum(ask_q[:num_asks_within_depth])

        imbalance[i] = np.log(total_bid_size_within_depth / total_ask_size_within_depth)

    weighted_imbalance = np.sum(imbalance * weights)

    return weighted_imbalance