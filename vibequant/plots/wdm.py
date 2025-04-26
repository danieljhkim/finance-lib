import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import math


def plot_weekday_averages(df, **kwargs):
    """
    Bar plot of average percentage change by weekday.
    """
    plt.close("all")
    df.plot(
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


def plot_day_of_month_averages(df, **kwargs):
    """
    Bar plot of average percentage change by day of month.
    """
    plt.close("all")
    df.plot(
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
    plt.close("all")
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
    plt.close("all")
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


def plot_monthly_averages(df, **kwargs):
    """
    Bar plot of average percentage change by month.
    Args:
        df (pd.Series): Series indexed by month (1-12 or month names).
        **kwargs: Additional keyword arguments for plotting.
    Returns:
        matplotlib.pyplot: The plot object.
    """
    plt.close("all")
    plt.figure(figsize=kwargs.pop("figsize", (14, 8)))
    df.plot(
        kind="bar",
        figsize=kwargs.pop("figsize", (16, 6)),
        color=kwargs.pop("color", "orchid"),
        edgecolor=kwargs.pop("edgecolor", "black"),
        **kwargs,
    )
    plt.title(kwargs.pop("title", "Average % Change by Month"))
    plt.xlabel(kwargs.pop("xlabel", "Month"))
    plt.ylabel(kwargs.pop("ylabel", "Average % Change"))
    plt.xticks(rotation=kwargs.pop("xticks_rotation", 0))
    plt.tight_layout()
    return plt


def plot_month_dom_weekday_heatmaps(df, **kwargs):
    """
    Plot all monthly heatmaps in a single figure with subplots.
    Args:
        df (pd.DataFrame): MultiIndex (Month, DayOfMonth) with Weekday columns.
        **kwargs: Additional keyword arguments for seaborn.heatmap.
    Returns:
        matplotlib.figure.Figure: The combined figure object.
    """
    months = df.index.get_level_values("Month").unique()
    n_months = len(months)
    ncols = 4
    nrows = math.ceil(n_months / ncols)
    figsize = kwargs.pop("figsize", (ncols * 6, nrows * 5))
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False)

    for i, month in enumerate(months):
        row, col = divmod(i, ncols)
        ax = axes[row][col]
        data = df.loc[month]
        sns.heatmap(
            data,
            annot=kwargs.get("annot", False),
            fmt=kwargs.get("fmt", ".2f"),
            cmap=kwargs.get("cmap", "coolwarm"),
            cbar_kws=kwargs.get("cbar_kws", {"label": "Average % Change"}),
            ax=ax,
            **kwargs,
        )
        ax.set_title(f"{calendar.month_name[month]}")
        ax.set_xlabel("Weekday")
        ax.set_ylabel("Day of Month")

    # Hide any unused subplots
    for j in range(i + 1, nrows * ncols):
        row, col = divmod(j, ncols)
        fig.delaxes(axes[row][col])

    plt.tight_layout()
    return plt
