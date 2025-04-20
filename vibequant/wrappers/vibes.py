from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from vibequant.utils.general import tableize
from vibequant.plots.wdm import (
    plot_weekday_averages,
    plot_day_of_month_averages,
    plot_calendar_change_grid,
)
from vibequant.plots.common import (
    plot_bar,
    plot_hist,
    plot_box,
    plot_correlation,
    plot_time_series,
)
from typing import Optional, List, Any, Union, Callable, Dict


class VibeFrame:
    """
    Wrapper for a pandas DataFrame with convenience plotting and display methods.
    """

    _vibe_plot_map: Dict[str, Callable] = {
        "W": plot_weekday_averages,
        "M": plot_day_of_month_averages,
        "WM": plot_calendar_change_grid,
    }

    def __init__(self, df: pd.DataFrame, type: Optional[str] = None):
        """
        Initialize a VibeFrame.

        Args:
            df (pd.DataFrame): The DataFrame to wrap.
            type (str, optional): The type of data (e.g., 'W', 'M', 'WM') for plotting dispatch.
        """
        self.df: pd.DataFrame = df
        self.original_df: Optional[pd.DataFrame] = None
        self.type: Optional[str] = type

    def set_type(self, type: str) -> None:
        """
        Set the type of the VibeFrame for plotting dispatch.

        Args:
            type (str): The type string (e.g., 'W', 'M', 'WM').
        """
        self.type = type

    def __repr__(self) -> str:
        """
        Return a string representation of the VibeFrame.

        Returns:
            str: String representation.
        """
        return f"VibeFrame(type={self.type}, shape={self.df.shape})"

    @property
    def original_dataframe(self) -> Optional[pd.DataFrame]:
        """
        Return the original DataFrame, if set.

        Returns:
            Optional[pd.DataFrame]: The original DataFrame or None.
        """
        return self.original_df

    def dataframe(self) -> pd.DataFrame:
        """
        Return the wrapped DataFrame.

        Returns:
            pd.DataFrame: The wrapped DataFrame.
        """
        return self.df

    def print(self) -> None:
        """
        Print the DataFrame in a table format.
        """
        print(tableize(self.df))

    def vibe_plot(self, **kwargs) -> Any:
        """
        Plot the DataFrame based on its type using the appropriate plot function.

        Args:
            **kwargs: Additional keyword arguments passed to the plot function.

        Returns:
            Any: The plot object (typically matplotlib.pyplot).
        """
        plot_func = self._vibe_plot_map.get(self.type, self.line_plot)
        return plot_func(self.df, **kwargs)

    def line_plot(self, columns: Optional[Union[str, List[str]]] = None, **kwargs) -> Any:
        """
        Line plot of the DataFrame, optionally for selected columns.

        Args:
            columns (str or list, optional): Column name or list of column names to plot. Plots all if None.
            **kwargs: Additional keyword arguments passed to the plot function.

        Returns:
            Any: The plot object (typically matplotlib.pyplot).
        """
        plt.close("all")
        if columns is None:
            data = self.df
        else:
            data = self.df[columns]
        ax = data.plot(kind="line", **kwargs)
        plt.title("Line Plot")
        plt.tight_layout()
        return plt

    def bar_plot(self, columns: Optional[Union[str, List[str]]] = None, **kwargs) -> Any:
        """
        Bar plot of the DataFrame, optionally for selected columns.

        Args:
            columns (str or list, optional): Column name or list of column names to plot. Plots all if None.
            **kwargs: Additional keyword arguments passed to the plot function.

        Returns:
            Any: The plot object (typically matplotlib.pyplot).
        """
        cols = self.df.columns.tolist() if columns is None else columns
        return plot_bar(self.df, cols, **kwargs)

    def hist_plot(self, columns: Optional[Union[str, List[str]]] = None, **kwargs) -> Any:
        """
        Histogram plot of the DataFrame, optionally for selected columns.

        Args:
            columns (str or list, optional): Column name or list of column names to plot. Plots all if None.
            **kwargs: Additional keyword arguments passed to the plot function.

        Returns:
            Any: The plot object (typically matplotlib.pyplot).
        """
        cols = self.df.columns.tolist() if columns is None else columns
        return plot_hist(self.df, cols, **kwargs)

    def box_plot(self, columns: Optional[Union[str, List[str]]] = None, **kwargs) -> Any:
        """
        Box plot of the DataFrame, optionally for selected columns.

        Args:
            columns (str or list, optional): Column name or list of column names to plot. Plots all if None.
            **kwargs: Additional keyword arguments passed to the plot function.

        Returns:
            Any: The plot object (typically matplotlib.pyplot).
        """
        cols = self.df.columns.tolist() if columns is None else columns
        return plot_box(self.df, cols, **kwargs)

    def correlation_plot(self, columns: Optional[List[str]] = None, **kwargs) -> Any:
        """
        Correlation plot of the DataFrame, optionally for selected columns.

        Args:
            columns (list, optional): List of column names to plot. Plots all if None.
            **kwargs: Additional keyword arguments passed to the plot function.

        Returns:
            Any: The plot object (typically matplotlib.pyplot).
        """
        cols = self.df.columns.tolist() if columns is None else columns
        return plot_correlation(self.df, cols, **kwargs)

    def time_series_plot(
        self,
        df: Optional[pd.DataFrame] = None,
        time_col: Optional[str] = None,
        value_col: str = "Close",
        agg: str = "sum",
        freq: str = "D",
        **kwargs
    ) -> Any:
        """
        Time series plot of the DataFrame.

        Args:
            df (pd.DataFrame, optional): DataFrame to plot. Uses self.df if None.
            time_col (str, optional): Name of the timestamp/date column. Inferred if None.
            value_col (str): Column to aggregate and plot.
            agg (str): Aggregation method: 'sum', 'mean', 'count'.
            freq (str): Resample frequency: 'D'=day, 'W'=week, 'M'=month, etc.
            **kwargs: Additional keyword arguments passed to the plot function.

        Returns:
            Any: The plot object (typically matplotlib.pyplot).
        """
        if df is None:
            df = self.df
        # Prefer DatetimeIndex if present
        if time_col is None and isinstance(df.index, pd.DatetimeIndex):
            time_col = df.index.name if df.index.name else None

        # Try to infer time_col from columns if not found
        if time_col is None:
            for col in df.columns:
                if col.lower() in ["date", "datetime", "timestamp", "time"]:
                    time_col = col
                    break
            if time_col is None:
                dt_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns
                if len(dt_cols) > 0:
                    time_col = dt_cols[0]
        if time_col is None and self.original_df is not None and self.original_df is not df:
            return plot_time_series(
                df=self.original_df,
                time_col=None,
                value_col=value_col,
                agg=agg,
                freq=freq,
                **kwargs
            )
        if time_col is None:
            raise ValueError("No datetime column found in DataFrame.")

        return plot_time_series(df, time_col, value_col, agg=agg, freq=freq, **kwargs)