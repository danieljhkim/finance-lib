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
    Wrapper for a pandas DataFrame with convenience plotting and statistics methods.
    """

    WEEK_DAYS: List[str] = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]

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
        self._original_df: pd.DataFrame = self._ensure_time_features(df)
        self.type: Optional[str] = type
        transform_map = self._get_transform_map()
        if type in transform_map:
            self.df: pd.DataFrame = transform_map[type](self._original_df)
        else:
            self.df: pd.DataFrame = self._original_df.copy()

    @property
    def original_df(self) -> pd.DataFrame:
        """
        Returns the original DataFrame (with time features ensured).

        Returns:
            pd.DataFrame: The original DataFrame.
        """
        return self._original_df

    def dataframe(self) -> pd.DataFrame:
        """
        Returns the current (possibly transformed) DataFrame.

        Returns:
            pd.DataFrame: The wrapped DataFrame.
        """
        return self.df

    def print(self) -> None:
        """
        Print the current DataFrame in a table format.
        """
        print(tableize(self.df))

    def __repr__(self) -> str:
        """
        String representation of the VibeFrame.

        Returns:
            str: String representation.
        """
        return f"VibeFrame(type={self.type}, shape={self.df.shape})"

    # --- Transformation logic ---

    @classmethod
    def _get_transform_map(cls) -> Dict[str, Callable[[pd.DataFrame], pd.DataFrame]]:
        """
        Returns a mapping from type string to transformation function.

        Returns:
            Dict[str, Callable]: Mapping of type to transformation function.
        """
        return {
            "W": cls._transform_weekday,
            "M": cls._transform_day_of_month,
            "WM": cls._transform_weekday_and_dom,
        }

    @staticmethod
    def _ensure_time_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure 'DayOfMonth', 'Weekday', and 'Change' columns exist in the DataFrame.
        If missing, infer from Date index/column and calculate 'Change' from 'Open' and 'Close'.
        Collapses MultiIndex columns to first level if present.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with required time features.
        """
        df = df.copy()
        # Collapse MultiIndex columns to first level if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        # Infer date features if missing
        if "DayOfMonth" not in df.columns or "Weekday" not in df.columns:
            if isinstance(df.index, pd.DatetimeIndex):
                date_index = df.index
            else:
                date_col = None
                for col in df.columns:
                    if col.lower() in ["date", "datetime", "timestamp", "time"]:
                        date_col = col
                        break
                if date_col:
                    df[date_col] = pd.to_datetime(df[date_col])
                    date_index = pd.DatetimeIndex(df[date_col])
                else:
                    raise ValueError(
                        "No datetime index or column found to infer 'DayOfMonth' and 'Weekday'."
                    )
            df["DayOfMonth"] = date_index.day
            df["Weekday"] = date_index.day_name()
        # Calculate Change if missing
        if "Change" not in df.columns:
            if "Open" in df.columns and "Close" in df.columns:
                df["Change"] = ((df["Close"] - df["Open"]) / df["Open"]) * 100
            else:
                raise ValueError(
                    "Cannot compute 'Change': missing 'Open' or 'Close' columns."
                )
        return df

    @staticmethod
    def _transform_weekday(df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform DataFrame to average change by weekday.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with average change by weekday.
        """
        df = VibeFrame._ensure_time_features(df)
        week_days = VibeFrame.WEEK_DAYS
        wdf = df.groupby("Weekday")["Change"].mean().reindex(week_days)
        return wdf.to_frame(name="AvgChange")

    @staticmethod
    def _transform_day_of_month(df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform DataFrame to average change by day of month.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with average change by day of month.
        """
        df = VibeFrame._ensure_time_features(df)
        dom_df = df.groupby("DayOfMonth")["Change"].mean().reindex(range(1, 32))
        return dom_df.to_frame(name="AvgChange")

    @staticmethod
    def _transform_weekday_and_dom(df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform DataFrame to average change by both weekday and day of month.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: Pivot table with average change by day of month and weekday.
        """
        df = VibeFrame._ensure_time_features(df)
        week_days = VibeFrame.WEEK_DAYS
        pivot = (
            df.groupby(["DayOfMonth", "Weekday"])["Change"]
            .mean()
            .unstack(fill_value=0)
            .reindex(columns=week_days, fill_value=0)
        )
        pivot.index.name = "DayOfMonth"
        return pivot

    def set_type(self, type: str) -> None:
        """
        Set the type of the VibeFrame for plotting dispatch and mutate self.df accordingly.

        Args:
            type (str): The type string (e.g., 'W', 'M', 'WM').
        """
        self.type = type
        df = self.original_df if self.original_df is not None else self.df
        transform_map = self._get_transform_map()
        if type in transform_map:
            self.df = transform_map[type](df)
        # else: do not mutate self.df

    # --- Statistics ---

    def stat(self) -> pd.DataFrame:
        """
        Return statistics for each numeric column in the DataFrame.

        Returns:
            pd.DataFrame: Statistics (describe) for numeric columns.
        """
        return self.df.describe().T

    def grouped_stats(
        self, by: Union[str, List[str]] = "Weekday", col: str = "Change"
    ) -> pd.DataFrame:
        """
        Return grouped statistics for a column.

        Args:
            by (str or list, optional): Column(s) to group by. Defaults to "Weekday".
            col (str): Column to compute statistics on.

        Returns:
            pd.DataFrame: Grouped statistics.
        """
        if self.original_df is None:
            raise ValueError("No original DataFrame set for grouped statistics.")
        stats = self.original_df.groupby(by)[col].agg(
            ["mean", "std", "min", "max", "count", "median"]
        )
        return stats

    # --- Plotting ---

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

    def line_plot(
        self, columns: Optional[Union[str, List[str]]] = None, **kwargs
    ) -> Any:
        """
        Line plot of the DataFrame, optionally for selected columns.

        Args:
            columns (str or list, optional): Column name or list of column names to plot. Plots all if None.
            **kwargs: Additional keyword arguments passed to the plot function.

        Returns:
            Any: The plot object (typically matplotlib.pyplot).
        """
        plt.close("all")
        data = self.df if columns is None else self.df[columns]
        data.plot(kind="line", **kwargs)
        plt.title("Line Plot")
        plt.tight_layout()
        return plt

    def bar_plot(
        self, columns: Optional[Union[str, List[str]]] = None, **kwargs
    ) -> Any:
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

    def hist_plot(
        self, columns: Optional[Union[str, List[str]]] = None, **kwargs
    ) -> Any:
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

    def box_plot(
        self, columns: Optional[Union[str, List[str]]] = None, **kwargs
    ) -> Any:
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

    def correlation_plot(
        self, columns: Optional[List[str]] = None, **kwargs
    ) -> Any:
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
        **kwargs,
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
        if (
            time_col is None
            and self.original_df is not None
            and self.original_df is not df
        ):
            return plot_time_series(
                df=self.original_df,
                time_col=None,
                value_col=value_col,
                agg=agg,
                freq=freq,
                **kwargs,
            )
        if time_col is None:
            raise ValueError("No datetime column found in DataFrame.")

        return plot_time_series(df, time_col, value_col, agg=agg, freq=freq, **kwargs)