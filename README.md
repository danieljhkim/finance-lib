# 📊 vibequant

---

`vibequant` is a lightweight Python library that wraps the complexity of financial data exploration into a smooth, intuitive interface. Inspired by the idea of *vibe coding*, this library helps you do less and see more.

---

## Installation 

*not yet available on PyPI*

```bash
pip install vibequant
```

---

## Quickstart

```python
from vibequant import vstock, vcrypto, VibeFrame

# List available stock tickers
print(vstock.list_tickers())

# fetch data and return vibeFrame
vf = vstock.fetch("MSFT")

# transform view to either: DWM, D, W, M, WM
vf.transform_view("DWM")

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

## VibeFrame Features

| Method | Description |
|--------|-------------|
| `VibeFrame(df)` | Wrap any DataFrame |
| `.vibe_plot()` | Smart default plot |
| `.stat()` | Summary statistics |
| `.grouped_stats(by, col)` | Aggregates by group |
| `.transform_view(type)` | Set periodicity (`"D"`, `"W"`, `"M"`, `"WM"`, `"DWM"`) |
| `.line_plot()` etc. | All the plots you need (`bar`, `hist`, `box`, `corr`, `ts`) |

---

## Credits

- `yfinance`, `pandas`, `matplotlib`, `seaborn` — the data & plot stack

---

## License

MIT License
