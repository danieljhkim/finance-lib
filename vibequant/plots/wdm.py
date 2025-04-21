import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_weekday_averages(weekday_averages, **kwargs):
    """
    Bar plot of average percentage change by weekday.
    """
    plt.close('all')
    weekday_averages.plot(
        kind="bar",
        figsize=kwargs.pop("figsize", (10, 6)),
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
    """
    plt.close('all')
    day_of_month_averages.plot(
        kind="bar",
        figsize=kwargs.pop("figsize", (14, 6)),
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
    """
    plt.close('all')
    df_avg.plot(
        kind=kwargs.pop("kind", "bar"),
        figsize=kwargs.pop("figsize", (18, 8)),
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
    """
    plt.close('all')
    plt.figure(figsize=kwargs.pop("figsize", (14, 8)))
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