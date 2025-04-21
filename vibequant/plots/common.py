import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_bar(df, cols, top_n=10):
    plt.close('all')
    df = df.copy()
    if isinstance(cols, str):
        cols = [cols]
    pdf = df[cols].value_counts().head(top_n).reset_index()
    pdf.columns = list(pdf.columns[:-1]) + ['count']
    plt.figure(figsize=(10, 5))
    x = pdf[cols].astype(str).agg(' | '.join, axis=1)
    sns.barplot(x=x, y=pdf['count'])
    plt.xticks(rotation=45)
    plt.title(f"Top {top_n} Most Frequent: {', '.join(cols)}")
    plt.tight_layout()
    return plt

def plot_hist(df, cols, bins=30):
    plt.close('all')
    df = df.copy()
    if isinstance(cols, str):
        cols = [cols]
    plt.figure(figsize=(8, 5))
    for col in cols:
        plt.hist(df[col].dropna(), bins=bins, edgecolor='black', alpha=0.5, label=col)
    plt.title(f"Histogram of {', '.join(cols)}")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return plt

def plot_box(df, cols):
    plt.close('all')
    df = df.copy()
    if isinstance(cols, str):
        cols = [cols]
    plt.figure(figsize=(max(6, len(cols)*2), 4))
    sns.boxplot(data=df[cols].dropna())
    plt.title(f"Boxplot of {', '.join(cols)}")
    plt.tight_layout()
    return plt

def plot_correlation(df, cols):
    plt.close('all')
    df = df.copy()
    corr = df[cols].dropna().corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix")
    plt.tight_layout()
    return plt

def plot_time_series(df, time_col, value_col, agg='sum', freq='D'):
    plt.close('all')
    df = df.copy()
    if agg == 'sum':
        series = df[value_col].resample(freq).sum()
    elif agg == 'mean':
        series = df[value_col].resample(freq).mean()
    elif agg == 'count':
        series = df[value_col].resample(freq).count()
    else:
        raise ValueError("Unsupported aggregation")
    plt.figure(figsize=(10, 5))
    series.plot()
    plt.title(f"{agg.capitalize()} of {value_col} over time ({freq})")
    plt.xlabel("Date")
    plt.ylabel(value_col)
    plt.grid(True)
    plt.tight_layout()
    return plt