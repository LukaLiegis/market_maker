import numpy as np
from numba import njit

@njit(cache=True)
def log_price_difference(follow: float, base: float) -> float:
    """
    Calculates the logarithmic price difference between the price of the asset on the most liquid exchange and the price from the venue you\
    are following.
    :param follow: the asset on the most liquid exchange
    :param base: the asset on the venue that you are trading
    :return: the logarithmic difference between the two prices.
    """
    return np.log(base / follow) * 100