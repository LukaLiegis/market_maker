import asyncio
import config
import pandas as pd
from binance.client import Client

client = Client(config.api_key, config.api_secret)

