from functools import lru_cache
import os
import json

@lru_cache(maxsize=1)
def load_tickers():
    tickers_path = os.path.join(
        os.path.dirname(__file__), "data", "tickers.json"
    )
    with open(tickers_path) as f:
        return json.load(f)