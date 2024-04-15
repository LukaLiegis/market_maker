import json
from websocket import WebSocketApp
import config
from src.exchanges.binance.endpoints import WsStreamLinks


def on_message(ws, message):
    """Processes incoming messages from the WebSocket."""
    data = json.loads(message)
    # Check for update type ("partial" or "update")
    if data['u'] in ["partial", "update"]:
        # Extract bid and ask data
        bids = data['b']
        asks = data['a']

        # Process or store the order book data (bids and asks)
        # You can print them, calculate spread, etc.
        print(f"Bids: {bids}")
        print(f"Asks: {asks}")


def on_error(ws, error):
    """Handles errors during the WebSocket connection."""
    print(f"Error: {error}")


def on_close(ws):
    """Logs the WebSocket connection closure."""
    print("Connection closed")


symbol: str = config.binance_ticker.lower()

futures_base_url = WsStreamLinks.FUTURES_PUBLIC_STREAM
url = futures_base_url + "/stream?streams="
stream = f"{symbol}@depth@100ms/"
url += stream

# Create a WebSocket connection
ws_app = WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)

# Keep the connection open
ws_app.run_forever()