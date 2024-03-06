from binance.client import Client
from src.sharedstate import SharedState

class BinanceData:
  def __init__(self, api_key, api_secret, testnet=False):
    """
    Initializes the BinanceData class with API credentials and optional testnet flag.
    """
    self.client = Client(api_key, api_secret, testnet=testnet)

  async def get_orderbook(self):
    """
    Gets the current order book for a specific symbol using the synchronous API.

    Args:
      symbol: The symbol of the cryptocurrency pair (e.g., "BTCUSDT").

    Returns:
      A dictionary containing the order book data.
    """
    return self.client.get_orderbook(symbol = self.symbol, limit = limit)

  async def get_candlesticks(self, interval, limit):
    """
    Gets candlestick data for a specific symbol using the asynchronous API.

    Args:
      symbol: The symbol of the cryptocurrency pair (e.g., "BTCUSDT").
      interval: The candlestick interval (e.g., Client.KLINE_INTERVAL_1MINUTE).
      limit: The maximum number of candlesticks to retrieve.

    Returns:
      A list of candlestick data points.
    """
    return self.client.get_klines(symbol = self.symbol, interval = interval, limit=limit)

  async def trades(self, limit):
      """
      Get a list of recent trades
      """
      return self.client.get_recent_trades(symbol = self.symbol, limit = limit)