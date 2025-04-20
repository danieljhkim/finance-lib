import pandas as pd
import matplotlib.pyplot as plt
from vibequant.utils.general import tableize
from vibequant.plots.wdm import (
    plot_weekday_averages,
    plot_day_of_month_averages,
    plot_calendar_change_bar,
)

class VibeFrame:

    def __init__(self, df: pd.DataFrame, type: str):
        self.df = df
        self.type = type
        self.vibe_plot_map = {
            "W": plot_weekday_averages,
            "M": plot_day_of_month_averages,
            "WM": plot_calendar_change_bar,
        }

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

    def plot(self, **kwargs):
        """
        Plot the DataFrame based on its type.
        Args:
            **kwargs: Additional keyword args passed to the plot function.
        Returns:
            matplotlib.figure.Figure | None
        """
        plot_func = self.vibe_plot_map.get(self.type, self.line_plot)
        return plot_func(**kwargs)

    def line_plot(self, columns=None, **kwargs):
        """
        Line plot of the DataFrame, optionally for selected columns.
        Args:
            columns (list, optional): List of column names to plot. Plots all if None.
            **kwargs: Additional keyword args passed to the plot function.
        Returns:
            matplotlib.figure.Figure
        """
        data = self.df[columns] if columns is not None else self.df
        ax = data.plot(kind="line", **kwargs)
        plt.title("Line Plot")
        plt.tight_layout()
        plt.show()
        return ax.get_figure()
