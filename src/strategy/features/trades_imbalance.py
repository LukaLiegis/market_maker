import numpy as np
from numba import njit
from numpy.typing import NDArray
from src.indicators.ema import ema_weights

@njit(cache=True)
def trades_imbalance(trades: NDArray, window: int) -> float:
    """
    Calculates the normalized imbalance between buy and sell trades within a specific window,
    using geometrically weighted quantities. The imbalance reflects the dominance of buy or sell trades,
    weighted by the recency of the trades in the window.
    :param trades: A 2D array with trade data, where each row represents a trade in the form [timestamp, side, price, volume]
    :param window: The number of most recent trades to consider for the imbalance calculation.
    :return: The normalized imbalance ranging from -1 (complete sell dominance) to 1 (complete buy dominance).
    """
    window = min(window, trades.shape[0])
    weights = ema_weights(window, reverse=True)
    delta_buys, delta_sells = 0.0, 0.0

    for i in range(window):
        trade_side = trades[i, 1]
        weighted_qty = np.log(1 + trades[i, 3]) * weights[i]

        if trade_side == 0.0:
            delta_buys += weighted_qty
        else:
            delta_sells += weighted_qty

    return (delta_buys - delta_sells) / (delta_buys + delta_sells)