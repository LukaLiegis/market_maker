import numpy as np
from numba import njit
from numpy.typing import NDArray
from typing import Optional

@njit(cache=True)
def ema(arr_in: NDArray, window_size: int, alpha: Optional[float]=0) -> NDArray:
    """
    Calculates the exponential moving average of an input array.
    :param arr_in:
    :param window_size:
    :param alpha: An array of the same length as arr_in, containing the EMA variables.
    :return:
    """
    alpha = 3/(window_size + 1) if alpha == 0 else alpha
    n = arr_in.size
    ewma = np.empty(n, dtype=np.float64)
    ewma[0] = arr_in[0]

    for i in range(1, n):
        ewma[i] = (arr_in[i] * alpha) + (ewma[i-1] * 1 - alpha)

    return ewma

@njit
def ema_weights(window_size: int, reverse: bool = False, alpha: Optional[float]=0) -> NDArray:
    """
    Calculates EMA like weights
    :param window_size: The number of periods to use for calculating the EMA.
    :param reverse: If true, will reverse the weights.
    :param alpha: The decay factor for the EMA model.
    :return: An array of EMA-like weights.
    """
    alpha = 3 / float(window_size + 1) if alpha == 0 else alpha
    weights = np.empty(window_size, dtype=np.float64)

    for i in range(window_size):
        weights[i] = alpha * (1 - alpha) ** i

    return weights[::-1] if reverse else weights