# stockbeta

[![PyPI - Version](https://img.shields.io/badge/TestPyPI-v0.0.4-blue?logo=pypi)](https://test.pypi.org/project/stockbeta)
<!-- [![PyPI version](https://img.shields.io/pypi/v/stockbeta?logo=pypi)](https://pypi.org/project/stockbeta/) -->
[![PyPI - Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://test.pypi.org/project/stockbeta)
[![Tests](https://github.com/finm-32900/stockbeta-example/actions/workflows/test.yml/badge.svg)](https://github.com/finm-32900/stockbeta-example/actions/workflows/test.yml)

A Python package for analyzing stock factor exposures using Fama-French factors.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Loading Factor Data](#loading-factor-data)
  - [Factor Analysis Reports](#factor-analysis-reports)
    - [Command Line Interface](#command-line-interface)
    - [Python Library Usage](#python-library-usage)
- [API Reference](#api-reference)
- [Error Handling](#error-handling)
- [License](#license)
- [Development](#development)

## Installation

```console
pip install stockbeta
```

## Quick Start

```python
import stockbeta

# Load factor data and analyze a stock
factors = stockbeta.load_factors(start='2020-01-01')
analysis = stockbeta.analyze_stock('AAPL', factors)
print(f"Market Beta: {analysis['market_beta']:.2f}")
```

## Usage Guide

### Loading Factor Data

The package provides easy access to Fama-French factor data through the Ken French Data Library.

```python
import stockbeta

# Load all available daily factor data
factors = stockbeta.load_factors()

# Load factors for a specific date range
factors = stockbeta.load_factors(start='2020-01-01', end='2023-12-31')
```

The returned DataFrame contains the following factors (all values are in decimal form):
- `Mkt-RF`: Excess return on the market
- `SMB`: Small Minus Big (size factor)
- `HML`: High Minus Low (value factor)
- `RF`: Risk-free rate

Example of working with the data:
```python
import stockbeta

# Load the last 5 years of factor data
factors = stockbeta.load_factors(start='2019-01-01')

# Calculate the market return
factors['Mkt'] = factors['Mkt-RF'] + factors['RF']

# Get summary statistics
print(factors.describe())
```

### Factor Analysis Reports

You can analyze a stock's factor exposures in two ways:

#### Command Line Interface

The package provides a CLI tool for quick factor analysis. After installation,
you can run it directly:

```console
stockbeta --ticker AAPL --start 2020-01-01 --end 2023-12-31
```

This will output a report like:
```
Factor Analysis Report for AAPL
========================================
Average Annual Return: 23.45%
Annual Volatility: 28.32%
Sharpe Ratio: 0.83

Factor Exposures:
Market Beta: 1.142
Size Factor (SMB) Beta: -0.234
Value Factor (HML) Beta: -0.456
```
You can install it from the local directory like this:
```
pip install -e .
```

I recommend using the Hatch shell environment to install the package.
```
hatch shell
pip install -e .
```

#### Python Library Usage

You can also generate factor analysis reports programmatically:

```python
import stockbeta
import yfinance as yf

# Download stock data
ticker = "AAPL"
stock_data = yf.download(ticker, start="2020-01-01", end="2023-12-31", progress=False)
stock_returns = stock_data["Adj Close"].pct_change().dropna()

# Load factor data (will try online first, then fall back to archived data)
try:
    factors = stockbeta.load_factors(start="2020-01-01", end="2023-12-31")
except Exception:
    factors = stockbeta.load_archived_data()

# Align dates and calculate factor exposures
import pandas as pd
combined = pd.concat([stock_returns, factors], axis=1, join="inner")
stock_returns = combined.iloc[:, 0]
factors = combined.iloc[:, 1:]

# Get factor analysis statistics
stats = stockbeta.calculate_factor_exposures(stock_returns, factors)

# Access individual statistics
print(f"Market Beta: {stats['market_beta']:.3f}")
print(f"Size Factor Beta: {stats['smb_beta']:.3f}")
print(f"Value Factor Beta: {stats['hml_beta']:.3f}")
print(f"Annual Sharpe Ratio: {stats['sharpe_ratio']:.2f}")
```

### Easter Eggs 🥚

The package includes some fun easter eggs! Try this:

```python
from stockbeta import easter_egg

df = easter_egg()
print(df)
```

You might find some interesting numbers on special dates! 🎯 🥧 The purpose of this is to demonstrate how to ship datasets with a package.

## License

`stockbeta` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Development

This package uses [Hatch](https://hatch.pypa.io/) for development and package management. Here's how to set up your development environment:

1. First, install Hatch if you haven't already:
```console
pip install hatch
```

2. Clone the repository:
```console
git clone https://github.com/finm-32900/stockbeta-example.git
cd stockbeta-example
```

3. Create and activate a development environment:
```console
hatch shell
```

This will automatically install all dependencies and the package in editable mode.

> **Educational Note**: This package demonstrates why matrix testing across Python versions is important. The tests will fail on Python 3.8 because we use `importlib.resources.files`, which was introduced in Python 3.9. This is a common issue in Python development - features available in newer versions might not work in older ones. Matrix testing helps catch these compatibility issues early.
>
> To fix this, we could either:
> 1. Drop support for Python 3.8
> 2. Use a compatibility package (`importlib_resources`)
> 3. Write version-specific code using `try`/`except`
>
> Each approach has its trade-offs. For learning purposes, we're keeping this issue to demonstrate real-world package development challenges.

### Running Tests

The package uses pytest for testing. To run tests:

```console
hatch test
```

You can also run tests with coverage:
```console
hatch test --cover
```

Or run specific test files:
```console
hatch test tests/test_easter_egg.py
```

For verbose output:
```console
hatch test -v
```

### Type Checking

To run type checking:
```console
hatch run types:check
```

### Formatting and Linting

You can use `hatch fmt` to format your Python code. This uses Ruff under the hood. 

```bash
hatch fmt
```
Hatch's formatter supports configuration options such as quote style, indent style, and line width through the project's configuration file. However, it's worth noting that if you need to both sort imports and format code, you'll need to run two commands:

```bash
hatch fmt --check  # for just checking formatting
```

### Development Tips

- The development environment created by `hatch shell` includes all necessary dependencies
- No need to manually install in editable mode (`pip install -e .`) as Hatch handles this
- Any changes you make to the source code will be immediately reflected when you import the package
- To exit the Hatch shell environment, simply type `exit`