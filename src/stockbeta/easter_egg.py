from importlib.abc import Traversable  # Changed from importlib.resources.abc to importlib.abc
from importlib.resources import files
from pathlib import Path

import pandas as pd


def easter_egg():
    """
    Returns a pandas DataFrame containing special dates and their corresponding numbers.
    The data includes Easter eggs like Pi on Pi Day and other fun numerical references.

    Returns:
        pandas.DataFrame: A DataFrame with 'date' and 'some_number' columns
    """
    csv_path = files("stockbeta.data").joinpath("easter_egg.csv")
    return read_data(csv_path)


def read_data(file_path: Path | Traversable) -> pd.DataFrame:
    """Read data from a CSV file.

    Args:
        file_path: Path or Traversable object pointing to the CSV file

    Returns:
        pandas.DataFrame: The data from the CSV file
    """
    return pd.read_csv(str(file_path), parse_dates=["date"])
