import os
import json

ticker_data = None

def load_tickers():
    if ticker_data is not None:
        return ticker_data
    tickers_path = os.path.join(
        os.path.dirname(__file__), "data", "tickers.json"
    )
    with open(tickers_path) as f:
        ticker_data = json.load(f)
    return ticker_data.copy()