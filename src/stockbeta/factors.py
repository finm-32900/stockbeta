"""Functions for loading factor data from Ken French's data library."""

from __future__ import annotations

import logging
import warnings
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from datetime import datetime

try:
    import pandas_datareader.data as web
except ModuleNotFoundError as e:
    if "No module named 'distutils'" in str(e):
        warnings.warn(
            "Could not import pandas_datareader due to missing distutils. Please install setuptools package.",
            stacklevel=2,
        )
        web = None
    else:
        raise

# Suppress the specific FutureWarning about date_parser
warnings.filterwarnings("ignore", category=FutureWarning, message=".*date_parser.*")


def load_factors(start: str | datetime | None = None, end: str | datetime | None = None) -> pd.DataFrame:
    """
    Load Fama/French 3 Factors (Daily) from Ken French's data library.

    Parameters
    ----------
    start : str or datetime, optional
        Start date of the data. Format: 'YYYY-MM-DD'
    end : str or datetime, optional
        End date of the data. Format: 'YYYY-MM-DD'

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the following columns:
        - Mkt-RF: Excess return on the market
        - SMB: Small Minus Big (size factor)
        - HML: High Minus Low (value factor)
        - RF: Risk-free rate
    """
    if web is None:
        logging.warning("pandas_datareader is not available. Cannot load factors.")
        return pd.DataFrame()
    ff_factors = web.DataReader("F-F_Research_Data_Factors_Daily", "famafrench", start=start, end=end)

    # Explicitly cast the first table to DataFrame and convert from percentage to decimal
    return pd.DataFrame(ff_factors[0]).div(100)
