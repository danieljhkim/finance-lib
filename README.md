# 📊  vibequant

---

> Data analysis & visualization made chill 😎  
> **Minimal effort. Maximum clarity. One vibe.**

`vibequant` is a lightweight Python library that wraps the complexity of financial data exploration into a smooth, intuitive interface. Inspired by the idea of *vibe coding*, this library helps you do less — and see more.

---

## 🚀 Why vibequant?

We built `vibequant` to remove the friction from analyzing financial time series data. Whether you’re working with stocks, crypto, or your own datasets, `VibeFrame` lets you:

- Instantly wrap any DataFrame
- Use intuitive functions like `.vibe_plot()` and `.stat()`
- Switch effortlessly between display and return modes
- Focus on insights, not boilerplate
- Easily compute grouped statistics and transformations

---

## 📦 Installation 

*not yet available on PyPI*

```bash
pip install vibequant
```

---

## ⚡ Quickstart

```python
from vibequant import vstock, vcrypto, VibeFrame

# List available stock tickers
print(vstock.list_tickers())

# Stock: average change by weekday
vf = vstock.avg_by_weekday("AAPL", start="2020-01-01", end="2023-01-01")

# Crypto: average change by day of month
vf = vcrypto.avg_by_day_of_month("BTC-USD")

# Crypto: average change by weekday and day of month
vf = vcrypto.avg_by_weekday_and_dom("BTC-USD")

# Wrap your own DataFrame (OHLCV or custom)
vf = VibeFrame(df)

# Print the current DataFrame
vf.print()

# Summary statistics for all numeric columns
print(vf.stat())

# Grouped statistics (e.g. by weekday)
print(vf.grouped_stats(by="Weekday", col="Change"))

# Plot automatically based on data type
fig = vf.vibe_plot()
fig.show()

# Or choose specific plot types
vf.line_plot()
vf.bar_plot()
vf.hist_plot()
vf.box_plot()
vf.correlation_plot()
vf.time_series_plot()

# Save a plot
vf.vibe_plot().savefig("my_plot.png")
```

---

## 🧠 Core Philosophy

- 🌊 *Vibe coding: less is more*
- 🔮 *Sensible defaults, optional customization*
- 🧼 *Zero boilerplate, zero clutter*
- 🖼 *Visuals first, always beautiful*

---

## 🧰 VibeFrame Features

| Method | Description |
|--------|-------------|
| `VibeFrame(df)` | Wrap any DataFrame |
| `.vibe_plot()` | Smart default plot |
| `.stat()` | Summary statistics |
| `.grouped_stats(by, col)` | Aggregates by group |
| `.set_type(type)` | Set periodicity (`"W"`, `"M"`, `"WM"`) |
| `.line_plot()` etc. | All the plots you need (`bar`, `hist`, `box`, `corr`, `ts`) |

---

## 🗺️ Roadmap

- [x] VibeFrame with rich plotting
- [ ] Additional source connectors (e.g. Quandl, Deribit)
- [ ] SmartStats module (ML & signal detection)
- [ ] Interactive visualizations (Plotly/Altair)

---

## 🙏 Credits

- `chatGPT` — for vibe coding it up
- `yfinance`, `pandas`, `matplotlib`, `seaborn` — the data & plot stack

---

## 📜 License

MIT License

---
