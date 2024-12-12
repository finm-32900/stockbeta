import pandas as pd
from datetime import datetime
from stockbeta import easter_egg

def test_easter_egg():
    # Get the easter egg data
    df = easter_egg()
    
    # Test that it returns a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Test that it has the expected columns
    assert set(df.columns) == {"date", "some_number"}
    
    # Test that dates are parsed correctly (should be datetime objects)
    assert isinstance(df["date"].iloc[0], pd.Timestamp)
    
    # Test a specific known value (Pi day)
    pi_day = df[df["date"] == "2024-03-14"].iloc[0]
    assert abs(pi_day["some_number"] - 3.141) < 0.001  # Using approx comparison for floats 