import config
from binance import Client

client = Client(api_key=config.api_key)


def orderbook():
    """
    Fetches the orderbook for the symbol
    :return: dictionary containing the orderbook
    """
    return client.get_order_book(symbol=config.ticker, limit=config.limit)


def trades():
    """
    Gets recent trades for the symbol
    :return:
    """
    return client.get_recent_trades(symbol=config.ticker, limit=config.limit)
