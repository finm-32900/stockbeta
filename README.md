# stockbeta

[![PyPI - Version](https://img.shields.io/badge/TestPyPI-v0.0.4-blue?logo=pypi)](https://test.pypi.org/project/stockbeta)
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

Example Python package for teaching/learning.

This project uses [Hatch](https://github.com/pypa/hatch) as its build backend for packaging, but you can leverage [UV](https://github.com/astral-sh/uv) for everything else (e.g., environment creation, resolution, installation, publishing, etc.).

## Dynamic Version with Hatch

• The project’s version is stored in src/stockbeta/__about__.py and referenced via [tool.hatch.version] in pyproject.toml.  
• Hatch automatically infers the version from __version__ in __about__.py (so you don’t need to specify a static version in pyproject.toml).

## Development Using UV

Below are the notable UV commands to help you develop and maintain this project:

1. Create/Update a Virtual Environment:

   ```
   uv sync
   ```

   This command will install dependencies listed in pyproject.toml (and dev dependencies if you have them separated) into a virtual environment.

2. Run Tests:
   ```
   uv run pytest
   ```
   or (if you haven’t installed pytest yet):
   ```
   uv pip install pytest
   uv run pytest
   ```

3. Build with Hatch via UV:
   ```
   uv build
   ```
   UV will detect that this project uses Hatchling and invoke hatchling.build under the hood. By default, you will get both a wheel and an sdist in the dist/ directory.

4. Publishing (Optional):
   If you want to publish the built artifacts:
   ```
   uv publish
   ```
   Again, UV will defer to your Hatch build system. You’ll need to configure your PyPI credentials, etc., as usual.

## Linting and Formatting

You can combine tools such as Ruff, Black, or Mypy with UV easily:

```
uv pip install ruff mypy
uv run ruff check src tests
uv run mypy src tests
```

If you still want to use Hatch’s built-in commands (like hatch fmt or hatch shell), that’s also completely compatible. UV doesn’t interfere with any existing Hatch subcommands.

## Summary

• Hatch remains your build backend for packaging.  
• UV provides fast dependency resolution, environment management, script running, and more.  
• You can fully preserve your existing dynamic version with src/stockbeta/__about__.py.  

Happy coding!