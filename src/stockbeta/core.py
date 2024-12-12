import os

import numpy as np
import pandas as pd


def load_archived_data():
    """Load archived Fama-French factor data included with the package."""
    data_path = os.path.join(os.path.dirname(__file__), "data", "ff3factors.parquet")
    return pd.read_parquet(data_path)


def calculate_beta(stock_returns: pd.Series, factor_returns: pd.Series) -> float:
    """Calculate beta with respect to any factor."""
    cov = np.cov(stock_returns, factor_returns)[0, 1]
    var = np.var(factor_returns)
    return cov / var


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: pd.Series) -> float:
    """Calculate the Sharpe ratio for a series of returns."""
    excess_returns = returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns)


def calculate_factor_exposures(stock_returns: pd.Series, factors: pd.DataFrame) -> dict:
    """Calculate factor exposures (betas) and other statistics."""
    excess_returns = stock_returns - factors["RF"]
    market_excess = factors["Mkt-RF"]

    return {
        "average_return": stock_returns.mean() * 252,  # Annualized
        "volatility": stock_returns.std() * np.sqrt(252),  # Annualized
        "sharpe_ratio": calculate_sharpe_ratio(stock_returns, factors["RF"]) * np.sqrt(252),  # Annualized
        "market_beta": calculate_beta(excess_returns, market_excess),
        "smb_beta": calculate_beta(excess_returns, factors["SMB"]),
        "hml_beta": calculate_beta(excess_returns, factors["HML"]),
    }
