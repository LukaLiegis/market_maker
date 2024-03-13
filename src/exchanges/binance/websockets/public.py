from typing import List, Tuple
from src.exchanges.binance.endpoints import WsStreamLinks
from src.sharedstate import SharedState

class PublicWebsockets:
    """
    Public Websocket request.
    """
    def __init__(self, ss: SharedState):
        self._ss = ss
        self.symbol: str = self.binance_symbol.lower()
        self.futures_base_url = WsStreamLinks.FUTURES_PUBLIC_STREAM

    def multi_stream_request(self, topics: List[str], **kwargs) -> Tuple[str, List[str]]:
        """
        Constructs and returns a WebSocket request URL and a corresponding list of topics for subscription.
        :param topics: A list of topics to subscribe to
        :param kwargs: Keyword arguments for specific subscriptions.
        :return: A tuple containing the request URL and a list of stream topics.
        """
        list_of_topics = []
        url = self.futures_base_url + "/stream?streams="

        for topic in topics:
            stream = ""
            if topic == "Trades":
                stream = f"{self.symbol}@trade/"
            elif topic == "Orderbook":
                stream = f"{self.symbol}@depth@100ms/"
            elif topic == "BBA":
                stream = f"{self.symbol}@bookTicker/"
            elif topic == "Kline" and "interval" in kwargs:
                stream = f"{self.symbol}@kline_{kwargs['interval']}/"

            if stream:
                url += stream
                list_of_topics.append(stream[:-1])

        return url[:-1], list_of_topics