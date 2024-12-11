"""Functions for loading factor data from Ken French's data library."""

from typing import Optional, Union
from datetime import datetime
import warnings
import pandas as pd
import pandas_datareader.data as web  # type: ignore

# Suppress the specific FutureWarning about date_parser
warnings.filterwarnings('ignore', category=FutureWarning, message='.*date_parser.*')

def load_factors(
    start: Optional[Union[str, datetime]] = None,
    end: Optional[Union[str, datetime]] = None
) -> pd.DataFrame:
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
    ff_factors = web.DataReader(
        'F-F_Research_Data_Factors_Daily',
        'famafrench',
        start=start,
        end=end
    )
    
    # The data comes as a dictionary with keys like '1234' for different tables
    # We want the first table which contains the daily factors
    factors_df = ff_factors[0]
    
    # Convert returns from percentage to decimal
    factors_df = factors_df / 100.0
    
    return factors_df
