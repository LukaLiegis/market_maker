class Inventory:
    """
    Manages inventory calculations for trading positions, including the calculation of position delta
    relative to the account size and leverage.
    """
    def __init__(self, ss) -> None:
        self.ss = ss

    def position_delta(self, side: str, value: float, leverage: int) -> None:
        """
        Updates the shared state with the current position delta
        :param side: The side of the position, either Buy or Sell.
        :param value: The value of the position.
        :param leverage: The leverage applied to the position.
        :return: None
        """
        if side:
            # Calculate the maximum account value adjusted for leverage and a scaling factor.
            acc_max = (self.ss.account_size * leverage) / 2.05

            # Adjust the value based on the side of the position.
            value = value if side == "Buy" else - value

            # Update the inventory delta in shared state.
            self.ss.inventory_delta = value / acc_max