# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2024-03-14

### Added
- Initial release
- Core functionality for calculating factor exposures (market beta, SMB, HML)
- Command-line interface for quick factor analysis
- Functions for loading Fama-French factor data
  - Online loading via pandas_datareader
  - Fallback to archived data
- Basic statistics calculations
  - Beta calculation
  - Sharpe ratio calculation
  - Annualized returns and volatility

### Dependencies
- pandas-datareader>=0.10.0
- pandas>=1.0.0
- fastparquet
- pyarrow
- numpy
- yfinance

[0.0.1]: https://github.com/finm-32900/stockbeta-example/releases/tag/v0.0.1 