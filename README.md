# stockbeta

[![PyPI - Version](https://img.shields.io/pypi/v/stockbeta.svg)](https://pypi.org/project/stockbeta)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stockbeta.svg)](https://pypi.org/project/stockbeta)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Development](#development)

## Installation

```console
pip install stockbeta
```

## Usage

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

This will automatically install all dependencies and the package in editable mode. You can now import and use the package in Python:

```python
import stockbeta
factors = stockbeta.load_factors()
```

### Running Tests

To run tests (once implemented):
```console
hatch run test
```

### Type Checking

To run type checking:
```console
hatch run types:check
```

### Development Tips

- The development environment created by `hatch shell` includes all necessary dependencies
- No need to manually install in editable mode (`pip install -e .`) as Hatch handles this
- Any changes you make to the source code will be immediately reflected when you import the package
- To exit the Hatch shell environment, simply type `exit`
```

This should be inserted before the License section in the README.md. The instructions reference the project configuration that's already in your `pyproject.toml` (see lines 39-44 for the types configuration).

The development instructions cover:
1. Setting up the development environment
2. Using Hatch for development
3. Running tests and type checking
4. Tips for development workflow

Note that I see you have mypy configured in your `pyproject.toml` (lines 39-44), which is why I included the type checking instructions. The configuration also shows coverage setup (lines 46-63), though you might want to add test files and a test runner configuration if you haven't already.
