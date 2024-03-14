from numpy.typing import NDArray

def bba_imbalance(bba: NDArray) -> float:
    """
    Calculates the imbalance between the bid and ask quantities.
    :param bba: An array containing the bid and ask quantities.
    :return: The imbalance between the bid and ask quantities between 1 and -1.
    """
    return ((bba[0,1] / (bba[1,1] + bba[0,1])) - 0.5)