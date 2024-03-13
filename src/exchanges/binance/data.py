import asyncio
from websockets import connect

# Replace with your desired symbols
BINANCE_SYMBOL = "BTCUSDT"
BYBIT_SYMBOL = "BTCUSD"

# Binance Websocket URL
BINANCE_WS_URL = f"wss://stream.binance.com:9443/ws/{BINANCE_SYMBOL}@depth"

# Bybit Websocket URL
BYBIT_WS_URL = f"wss://stream.bybit.com/spot/v2/orderBook/{BYBIT_SYMBOL}"


async def handle_binance_message(websocket, message):
    # Parse Binance orderbook data (specific format depends on chosen library)
    print(f"[Binance] Orderbook update: {message}")


async def handle_bybit_message(websocket, message):
    # Parse Bybit orderbook data (specific format depends on chosen library)
    print(f"[Bybit] Orderbook update: {message}")


async def handle_stream(websocket_url, handler):
    async with connect(websocket_url) as websocket:
        await websocket.send("ping")  # Optional: Send a ping message
        while True:
            message = await websocket.recv()
            await handler(websocket, message)


async def main():
    binance_task = asyncio.create_task(handle_stream(BINANCE_WS_URL, handle_binance_message))
    bybit_task = asyncio.create_task(handle_stream(BYBIT_WS_URL, handle_bybit_message))
    await asyncio.gather(binance_task, bybit_task)


if __name__ == "__main__":
    asyncio.run(main())
