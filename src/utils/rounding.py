from decimal import Decimal

def round_step(num: float, step: float) -> float:
    """
    Round a float to a given step size
    """
    num = Decimal(str(num))
    return float(num - num % Decimal(str(step)))