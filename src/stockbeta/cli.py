import argparse
import logging

import pandas as pd
import yfinance as yf

from stockbeta.core import calculate_factor_exposures, load_archived_data
from stockbeta.factors import load_factors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_report(ticker: str, stats: dict) -> str:
    """Format the statistics into a readable report."""
    report = [
        f"Factor Analysis Report for {ticker}",
        "=" * 40,
        f"Average Annual Return: {stats['average_return']:,.2%}",
        f"Annual Volatility: {stats['volatility']:,.2%}",
        f"Sharpe Ratio: {stats['sharpe_ratio']:.2f}",
        "\nFactor Exposures:",
        f"Market Beta: {stats['market_beta']:.3f}",
        f"Size Factor (SMB) Beta: {stats['smb_beta']:.3f}",
        f"Value Factor (HML) Beta: {stats['hml_beta']:.3f}",
    ]
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Calculate stock factor exposures and statistics.")
    parser.add_argument("--ticker", required=True, help="Stock ticker symbol")
    parser.add_argument("--start", default="2021-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", default="2021-12-31", help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    # Load factor data
    try:
        factors = load_factors(start=args.start, end=args.end)
    except (ConnectionError, ValueError) as e:
        logger.warning("Error loading online data: %s", e)
        logger.info("Falling back to archived data...")
        factors = load_archived_data()

    # Download stock data
    stock_data = yf.download(args.ticker, start=args.start, end=args.end, progress=False)
    stock_returns = stock_data["Adj Close"].pct_change().dropna()

    # Align dates
    combined = pd.concat([stock_returns, factors], axis=1, join="inner")
    stock_returns = combined.iloc[:, 0]
    factors = combined.iloc[:, 1:]

    # Calculate statistics and generate report
    stats = calculate_factor_exposures(stock_returns, factors)
    logger.info(format_report(args.ticker, stats))


if __name__ == "__main__":
    main()
