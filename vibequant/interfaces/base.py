from abc import ABC, abstractmethod

from vibequant.sources.yfinance_source import YFinanceSource
from vibequant.wrappers.vibes import VibeFrame


class BaseInterface(ABC):

    WEEK_DAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    def __init__(self):
        self.sources = {"yfinance": YFinanceSource()}

    def list_sources(self):
        return list(self.sources.keys())

    def _get_source(self, source):
        if source not in self.sources:
            raise ValueError(
                f"Source '{source}' not found. Available sources: {', '.join(self.sources.keys())}"
            )
        return self.sources[source]

    def list_tickers(self, source="yfinance"):
        return self._get_source(source).list_stock_tickers()

    def avg_by_weekday(self, ticker, start=None, end=None, source="yfinance"):
        df = self._get_source(source).fetch(ticker, start, end)
        wdf = df.groupby("Weekday")["Change"].mean()
        wdf = wdf.reindex(self.WEEK_DAYS)
        wdf_df = wdf.to_frame(name="AvgChange")
        vf = VibeFrame(wdf_df, "W")
        vf.original_df = df
        return vf

    def avg_by_day_of_month(self, ticker, start=None, end=None, source="yfinance"):
        df = self._get_source(source).fetch(ticker, start, end)
        dom_df = df.groupby("DayOfMonth")["Change"].mean()
        dom_df = dom_df.reindex(range(1, 32))
        dom_df = dom_df.to_frame(name="AvgChange")
        vf = VibeFrame(dom_df, "M")
        vf.original_df = df
        return vf

    def avg_by_weekday_and_dom(self, ticker, start=None, end=None, source="yfinance"):
        df = self._get_source(source).fetch(ticker, start, end)
        pivot = (
            df.groupby(["DayOfMonth", "Weekday"])["Change"]
            .mean()
            .unstack(fill_value=0)
        )
        pivot = pivot.reindex(columns=self.WEEK_DAYS, fill_value=0)
        pivot.index.name = "DayOfMonth"
        vf = VibeFrame(pivot, "WM")
        vf.original_df = df
        return vf
