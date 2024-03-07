import time
import asyncio
import config
from binance.client import Client

class MarketMaker:
    def __init__(self, symbol, api_key, api_secret):
        self.symbol = symbol
        self.client = Client(api_key, api_secret)
        self.min_spread = 0.0001  # Minimum spread between bid and ask
        self.position = 0  # Current position
        self.last_bid = 0
        self.last_ask = 0

    def get_orderbook(self):
        orderbook = self.client.futures_order_book(symbol=self.symbol)
        return orderbook

    def place_order(self, price, quantity, side):
        try:
            order = self.client.futures_create_order(
                symbol=self.symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price)
            return order
        except Exception as e:
            print("Failed to place order:", e)
            return None

    def cancel_order(self, order_id):
        try:
            self.client.futures_cancel_order(symbol=self.symbol, orderId=order_id)
            print("Order cancelled successfully")
        except Exception as e:
            print("Failed to cancel order:", e)

    def update_prices(self):
        orderbook = self.get_orderbook()
        bid_price = float(orderbook['bids'][0][0])
        ask_price = float(orderbook['asks'][0][0])
        self.last_bid = bid_price
        self.last_ask = ask_price

    def calculate_spread(self):
        return self.last_ask - self.last_bid

    def trade(self):
        spread = self.calculate_spread()
        mid_price = (self.last_bid + self.last_ask) / 2
        bid_price = mid_price - spread / 4
        ask_price = mid_price + spread / 4

        if spread < self.min_spread:
            return

        # Cancel previous orders
        self.cancel_order()

        # Place new orders
        self.place_order(bid_price, 0.01, 'BUY')
        self.place_order(ask_price, 0.01, 'SELL')

    def run(self):
        while True:
            try:
                self.update_prices()
                self.trade()
                time.sleep(5)  # Adjust sleep time as needed
            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    # Replace these values with your Binance API key and secret
    api_key = config.api_key
    api_secret = config.api_secret
    symbol = 'BTCUSDT_PERP'  # Example symbol

    market_maker = MarketMaker(symbol, api_key, api_secret)
    market_maker.run()
