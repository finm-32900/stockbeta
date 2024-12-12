import pandas as pd
import pytest
from stockbeta import load_archived_data, load_factors


def test_load_archived_data():
    """Test loading the archived Fama-French factor data."""
    df = load_archived_data()
    
    # Test that it returns a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Test that it has the expected columns
    expected_columns = {'Mkt-RF', 'SMB', 'HML', 'RF'}
    assert set(df.columns) == expected_columns
    
    # Test that the data types are numeric
    for col in expected_columns:
        assert pd.api.types.is_numeric_dtype(df[col])
    
    # Test that there's actual data
    assert len(df) > 0


@pytest.mark.filterwarnings("ignore::FutureWarning")  # Ignore pandas_datareader warning
def test_load_factors():
    """Test loading factors from Ken French's library."""
    # Test with a specific date range to ensure consistent results
    df = load_factors(start='2020-01-01', end='2020-01-31')
    
    # Test that it returns a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Test that it has the expected columns
    expected_columns = {'Mkt-RF', 'SMB', 'HML', 'RF'}
    assert set(df.columns) == expected_columns
    
    # Test that values are in decimal form (not percentages)
    assert all(df['Mkt-RF'].abs() < 1)  # Market returns should be decimals