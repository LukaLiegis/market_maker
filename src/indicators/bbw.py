import numpy as np
from numba import njit
from numpy.typing import NDArray

@njit(cache=True)
def bbw(klines: NDArray, length: int, multiplier: float) -> float:
    """
    Calculates the Bollinger Band Width for a given set of klines.
    :param klines: Array of klines
    :param length: Number of periods used to calculate the EMA and standard deviation.
    :param multiplier: Multiplier for standard deviation used to calculate the width of the bands.
    :return: Width of the Bollinger Bands for the given parameters.
    """
    closes = klines[:, 4]
    dev = multiplier * np.std(closes[-length:])
    return 2 * dev