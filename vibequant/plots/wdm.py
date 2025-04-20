import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_weekday_averages(weekday_averages, **kwargs):
    """
    Bar plot of average percentage change by weekday.

    Args:
        weekday_averages (pd.Series): Series with weekdays as index and averages as values.
        **kwargs: Additional keyword arguments for pandas.Series.plot().
    Returns:
        matplotlib.pyplot: The plot object.
    """
    plt.close('all')
    plt.figure(figsize=kwargs.pop("figsize", (6, 4)))
    weekday_averages.plot(
        kind="bar",
        color=kwargs.pop("color", "skyblue"),
        edgecolor=kwargs.pop("edgecolor", "black"),
        **kwargs,
    )
    plt.title(kwargs.pop("title", "Average % Change by Weekday"))
    plt.xlabel(kwargs.pop("xlabel", "Weekday"))
    plt.ylabel(kwargs.pop("ylabel", "Average % Change"))
    plt.xticks(rotation=kwargs.pop("xticks_rotation", 45))
    plt.tight_layout()
    
    return plt

def plot_day_of_month_averages(day_of_month_averages, **kwargs):
    """
    Bar plot of average percentage change by day of month.

    Args:
        day_of_month_averages (pd.Series): Series with day of month as index and averages as values.
        **kwargs: Additional keyword arguments for pandas.Series.plot().
    Returns:
        matplotlib.pyplot: The plot object.
    """
    plt.close('all')
    plt.figure(figsize=kwargs.pop("figsize", (8, 4)))
    day_of_month_averages.plot(
        kind="bar",
        color=kwargs.pop("color", "lightgreen"),
        edgecolor=kwargs.pop("edgecolor", "black"),
        **kwargs,
    )
    plt.title(kwargs.pop("title", "Average % Change by Day of Month"))
    plt.xlabel(kwargs.pop("xlabel", "Day of Month"))
    plt.ylabel(kwargs.pop("ylabel", "Average % Change"))
    plt.xticks(rotation=kwargs.pop("xticks_rotation", 0))
    plt.tight_layout()
    
    return plt

def plot_calendar_change_bar(df_avg: pd.DataFrame, **kwargs):
    """
    Bar plot of average percentage change by day of month, grouped by weekday.

    Args:
        df_avg (pd.DataFrame): DataFrame with day of month as index and weekdays as columns.
        **kwargs: Additional keyword arguments for pandas.DataFrame.plot().
    Returns:
        matplotlib.pyplot: The plot object.
    """
    plt.close('all')
    plt.figure(figsize=kwargs.pop("figsize", (20, 6)))
    df_avg.plot(
        kind=kwargs.pop("kind", "bar"),
        colormap=kwargs.pop("colormap", "viridis"),
        edgecolor=kwargs.pop("edgecolor", "black"),
        legend=kwargs.pop("legend", True),
        ax=plt.gca(),
        **kwargs,
    )
    plt.title(kwargs.pop("title", "Average % Change by Day of Month & Weekday"))
    plt.xlabel(kwargs.pop("xlabel", "Day of Month"))
    plt.ylabel(kwargs.pop("ylabel", "Average % Change"))
    plt.xticks(rotation=kwargs.pop("xticks_rotation", 0))
    plt.legend(
        title=kwargs.pop("legend_title", "Weekday"),
        bbox_to_anchor=kwargs.pop("legend_bbox", (1.05, 1)),
        loc=kwargs.pop("legend_loc", "upper left"),
    )
    plt.tight_layout()
    
    return plt

def plot_calendar_change_grid(df_avg: pd.DataFrame, **kwargs):
    """
    Heatmap of average percentage change by day of month (rows) and weekday (columns).

    Args:
        df_avg (pd.DataFrame): DataFrame with day of month as index and weekdays as columns.
        **kwargs: Additional keyword arguments for seaborn.heatmap().
    Returns:
        matplotlib.pyplot: The plot object.
    """
    plt.close('all')
    plt.figure(figsize=kwargs.pop("figsize", (10, 6)))
    sns.heatmap(
        df_avg,
        annot=kwargs.pop("annot", True),
        fmt=kwargs.pop("fmt", ".2f"),
        cmap=kwargs.pop("cmap", "coolwarm"),
        cbar_kws=kwargs.pop("cbar_kws", {"label": "Average % Change"}),
        **kwargs,
    )
    plt.title(kwargs.pop("title", "Average % Change by Day of Month & Weekday"))
    plt.xlabel(kwargs.pop("xlabel", "Weekday"))
    plt.ylabel(kwargs.pop("ylabel", "Day of Month"))
    plt.tight_layout()
    return plt
