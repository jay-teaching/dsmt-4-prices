"""Plot Apple and Unilever price changes during 2025."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from prices import load_prices


def main() -> None:
    """Save a chart comparing Apple and Unilever during 2025."""
    start_date = "2025-01-02"
    end_date = "2025-12-31"
    tickers = {
        "AAPL": {"label": "Apple", "color": "#555555"},
        "ULVR.L": {"label": "Unilever", "color": "#1F36C7"},
    }

    fig, ax = plt.subplots(figsize=(10, 6))

    for ticker, config in tickers.items():
        prices = load_prices(ticker).copy()
        series = prices["Close"].loc[start_date:end_date].dropna()
        if series.empty:
            continue

        start_value = series.iloc[0]
        pct_change = (series / start_value - 1) * 100
        ax.plot(pct_change.index, pct_change.values, label=config["label"], color=config["color"], linewidth=2)

    ax.axhline(0, color="black", linewidth=0.8, alpha=0.55)
    ax.set_title(f"Apple vs Unilever price change ({start_date} to {end_date})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Change since first day (%)")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend()
    ax.text(0.02, 0.02, "Source: Yahoo Finance", transform=ax.transAxes, fontsize=9, color="dimgray")
    fig.tight_layout()

    output = Path(__file__).resolve().parents[1] / "figures" / "unilever_vs_apple_2025.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=150)
    plt.close(fig)

    print(f"Saved chart to {output}")


if __name__ == "__main__":
    main()
