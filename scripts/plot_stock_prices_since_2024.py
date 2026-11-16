"""Plot each stock relative to its 2024 start value."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from prices import TICKERS, load_prices


def main() -> None:
    """Save a chart comparing percentage changes in the repo's three stocks."""
    fig, ax = plt.subplots(figsize=(12, 7))

    for ticker in TICKERS:
        prices = load_prices(ticker).copy()
        if "Adj Close" not in prices.columns:
            raise ValueError(f"{ticker} does not contain an 'Adj Close' column")

        series = prices["Adj Close"].dropna()
        if series.empty:
            continue

        start_value = series.iloc[0]
        pct_change = (series / start_value - 1) * 100
        label = ticker if ticker != "ULVR.L" else "ULVR.L (Unilever)"
        ax.plot(pct_change.index, pct_change.values, label=label, linewidth=2)

    ax.axhline(0, color="black", linewidth=0.8, alpha=0.55)
    ax.set_title("Stock performance since 2024")
    ax.set_xlabel("Date")
    ax.set_ylabel("Percent change since first available trading day (%)")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend()
    fig.tight_layout()

    output = Path(__file__).resolve().parents[1] / "figures" / "stock_prices_since_2024.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200)
    plt.close(fig)

    print(f"Saved chart to {output}")


if __name__ == "__main__":
    main()
