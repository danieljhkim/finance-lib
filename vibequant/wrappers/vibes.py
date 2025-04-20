import pandas as pd
import matplotlib.pyplot as plt
from vibequant.utils.general import tableize
from vibequant.plots.wdm import (
    plot_weekday_averages,
    plot_day_of_month_averages,
    plot_calendar_change_bar,
    plot_calendar_change_grid
)
from vibequant.plots.common import (
    plot_bar,
    plot_hist,
    plot_box,
    plot_correlation,
    plot_time_series,
)


class VibeFrame:

    def __init__(self, df: pd.DataFrame, type: str):
        self.df = df
        self.original_df = None
        self.type = type
        self.vibe_plot_map = {
            "W": plot_weekday_averages,
            "M": plot_day_of_month_averages,
            "WM": plot_calendar_change_grid,
        }
    
    def __repr__(self):
        """
        Return a string representation of the VibeFrame.
        """
        return f"VibeFrame(type={self.type}, shape={self.df.shape})"
    
    @property
    def original_dataframe(self):
        """
        Return the original DataFrame.
        """
        return self.original_df

    def dataframe(self):
        """
        Return the DataFrame.
        """
        return self.df

    def print(self):
        """
        Print the DataFrame.
        """
        print(tableize(self.df))

    def vibe_plot(self, **kwargs):
        """
        Plot the DataFrame based on its type.
        Args:
            **kwargs: Additional keyword args passed to the plot function.
        Returns:
            matplotlib.figure.Figure | None
        """
        plot_func = self.vibe_plot_map.get(self.type, self.line_plot)
        return plot_func(self.df, **kwargs)

    def line_plot(self, columns=None, **kwargs):
        """
        Line plot of the DataFrame, optionally for selected columns.
        Args:
            columns (list, optional): List of column names to plot. Plots all if None.
            **kwargs: Additional keyword args passed to the plot function.
        Returns:
            matplotlib.figure.Figure
        """
        plt.close("all")
        data = self.df[columns] if columns is not None else self.df
        ax = data.plot(kind="line", **kwargs)
        plt.title("Line Plot")
        plt.tight_layout()
        return plt

    def bar_plot(self, column=None, **kwargs):
        """
        Bar plot of the DataFrame, optionally for selected columns.
        Args:
            column (string or list, optional): Column(s) to plot. Plots all if None.
            **kwargs: Additional keyword args passed to the plot function.
        Returns:
            matplotlib.figure.Figure
        """
        cols = self.df.columns if column is None else column
        return plot_bar(self.df, cols, **kwargs)

    def hist_plot(self, column=None, **kwargs):
        """
        Histogram plot of the DataFrame, optionally for selected columns.
        Args:
            column (string or list, optional): Column(s) to plot. Plots all if None.
            **kwargs: Additional keyword args passed to the plot function.
        Returns:
            matplotlib.figure.Figure
        """
        cols = self.df.columns if column is None else column
        return plot_hist(self.df, cols, **kwargs)

    def box_plot(self, column=None, **kwargs):
        """
        Box plot of the DataFrame, optionally for selected columns.
        Args:
            column (string or list, optional): Column(s) to plot. Plots all if None.
            **kwargs: Additional keyword args passed to the plot function.
        Returns:
            matplotlib.figure.Figure
        """
        cols = self.df.columns if column is None else column
        return plot_box(self.df, cols, **kwargs)

    def correlation_plot(self, columns=None, **kwargs):
        """
        Correlation plot of the DataFrame, optionally for selected columns.
        Args:
            columns (list, optional): List of column names to plot. Plots all if None.
            **kwargs: Additional keyword args passed to the plot function.
        Returns:
            matplotlib.figure.Figure
        """
        cols = self.df.columns if columns is None else columns
        return plot_correlation(self.df, cols, **kwargs)

    def time_series_plot(
        self, df=None, time_col=None, value_col="Close", agg="sum", freq="D", **kwargs
    ):
        """
        Time series plot of the DataFrame.
        Args:
            df (pd.DataFrame, optional): DataFrame to plot. Uses self.df if None.
            time_col (str, optional): Name of the timestamp/date column. Inferred if None.
            value_col (str): Column to aggregate and plot.
            agg (str): Aggregation method: 'sum', 'mean', 'count'.
            freq (str): Resample frequency: 'D'=day, 'W'=week, 'M'=month, etc.
            **kwargs: Additional keyword args passed to the plot function.
        Returns:
            matplotlib.figure.Figure
        """
        if df is None:
            df = self.df
        if time_col is None and isinstance(df.index, pd.DatetimeIndex):
            time_col = df.index.name if df.index.name else "index"

        if time_col is None or time_col == "index":
            for col in df.columns:
                if col.lower() in ["date", "datetime", "timestamp", "time"]:
                    time_col = col
                    break
            if time_col is None or time_col == "index":
                dt_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns
                if len(dt_cols) > 0:
                    time_col = dt_cols[0]
            if (
                (time_col is None or time_col == "index")
                and self.original_df is not None
                and self.original_df is not df
            ):
                return plot_time_series(
                    df=self.original_df,
                    time_col=None,
                    value_col=value_col,
                    agg=agg,
                    freq=freq,
                    **kwargs
                )
            if time_col is None or time_col == "index":
                raise ValueError("No datetime column found in DataFrame.")

        return plot_time_series(df, time_col, value_col, agg=agg, freq=freq, **kwargs)
