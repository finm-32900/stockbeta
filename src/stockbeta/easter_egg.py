from importlib.resources import files

import pandas as pd


def easter_egg():
    """
    Returns a pandas DataFrame containing special dates and their corresponding numbers.
    The data includes Easter eggs like Pi on Pi Day and other fun numerical references.

    Returns:
        pandas.DataFrame: A DataFrame with 'date' and 'some_number' columns
    """
    csv_path = files("stockbeta.data").joinpath("easter_egg.csv")
    return pd.read_csv(csv_path, parse_dates=["date"])
