# Writing and Publishing Your Own Python Packages

## Introduction

### Motivation: Why Write Python Packages?

The ability to automate workflows and develop reusable tools is essential. Financial institutions and companies rely heavily on custom libraries to handle complex calculations, manipulate large datasets, and implement models that are central to their decision-making processes. Python has emerged as a dominant language in the finance industry, and understanding how to package and distribute Python libraries is a critical skill.

Knowing how to write Python packages provides several key benefits:

- **Reusability and Collaboration**: Packaging code allows you to create tools that can be easily reused across projects and shared with colleagues or clients.
- **Version Control and Maintenance**: A properly structured package supports versioning, making it easier to track changes and maintain functionality over time.
- **Career Readiness**: Many roles in quantitative finance, data science, and software engineering value candidates who can create and maintain robust software libraries.
- **Open Source Contributions**: Python packages are the building blocks of the open-source ecosystem. Understanding the packaging process allows you to contribute to or build on existing tools.
- **Scalability**: Developing modular code within a package structure helps scale analytics workflows and integrates with corporate software pipelines.

### Objectives of This Chapter

This chapter introduces the process of writing Python packages using a tool called [**Hatch**](https://hatch.pypa.io/), which is maintained by the Python Packaging Authority ([PyPA](https://www.pypa.io/)). We will:

1. Discuss the fundamental components of a Python package.
2. Demonstrate how to use Hatch for package development and management.
3. Walk through an example package, `stockbeta`, designed for quantitative finance applications.
4. Explore how this knowledge can be applied to real-world scenarios in the financial industry.

### Evolution of Python Packaging

The Python packaging ecosystem has evolved significantly over the years:

#### Historical Context

- **[Distutils](https://docs.python.org/3/library/distutils.html) (2000-2020)**: Python's original built-in packaging tool, included in the standard library. It provided basic functionality for:
  - Building source distributions
  - Installing Python modules
  - Basic compilation of extension modules

  However, it lacked crucial features like dependency management, binary distributions, and version handling. Its minimal feature set and inability to adapt to modern Python packaging needs led to its deprecation in Python 3.10 and removal in Python 3.12.

- **[Setuptools](https://setuptools.pypa.io/) (2004-present)**: Originally created as an enhancement to Distutils, it became the de facto standard for Python packaging. It introduced:

  - The `setup.py` configuration file
  - `easy_install` package installer
  - Dependency management
  - Entry points and console scripts
  - Automatic package discovery

  While still widely used, Setuptools has fallen out of favor due to:
  - Security concerns with executing arbitrary Python code in `setup.py`
  - Complex and sometimes unpredictable configuration (e.g., `setup.py` might behave differently based on installed packages or environment variables, making builds inconsistent across systems)
  - Lack of standardization in build processes (e.g., different packages might use different build backends, custom build steps, or non-standard commands in their `setup.py`, making it harder to understand and maintain build processes across projects)
  - Difficulty in maintaining reproducible builds (e.g., two developers running the same `setup.py` might produce different packages due to differences in their local Python environments or setuptools versions)

- **[pip](https://pip.pypa.io/) (2008-present)**: Replaced `easy_install` as the primary package installer, still dominant today. Introduced:

  - Requirements files for dependency specification (e.g., `requirements.txt`)
  - Better dependency resolution
  - More reliable installation process
  - Support for various package formats and sources (e.g., source distributions, binary distributions, and editable installs)

- **[wheel](https://wheel.readthedocs.io/) format (2012-present)**: Introduced a faster, more reliable binary package format that:

  - Eliminates the need to run `setup.py` during installation
  - Provides consistent installations across platforms
  - Reduces installation time
  - Supports reproducible builds

- **Python Packaging Authority (2011-present)**: Founded as the working group that maintains and evolves the core projects of Python packaging. It:

  - Maintains key tools like pip, wheel, and virtualenv
  - Develops packaging standards through PEPs (Python Enhancement Proposals)
  - Provides official documentation at packaging.python.org
  - Coordinates between different packaging tools and projects
  - Ensures security and reliability of Python's package ecosystem
  - Manages [PyPI](https://pypi.org/) (Python Package Index), the official package repository

#### Modern Packaging Tools

Several tools now compete in the Python packaging space:

- **[Hatch](https://hatch.pypa.io/)**: An official PyPA tool that provides a modern, comprehensive approach to package management. Benefits include:

  - Single `pyproject.toml` configuration. Note that `pyproject.toml` is the new standard for Python projects, replacing `setup.py` and `setup.cfg`. However, `setup.py` is still widely used and supported.
  - Built-in environment management (e.g., `hatch env create`). Recall that environment management means that Hatch will create a virtual environment with the dependencies installed.
  - Standardized build system (e.g., `hatch build`). 
  - Simplified publishing workflow (e.g., `hatch publish` will build the package and upload it to PyPI).
  - Active maintenance by PyPA

- **[Poetry](https://python-poetry.org/)**: Popular alternative that offers:

  - Dependency resolution
  - Virtual environment management
  - Similar `pyproject.toml` configuration
  - Strong community support

```{note}
Some criticisms of Poetry include:

- "Poetry does several things by default that are bad for libraries - see https://iscinumpy.dev/post/poetry-versions/ for some details." (from [here](https://news.ycombinator.com/item?id=31192499))
- Tensorflow and PyTorch have some issues on Poetry.
```

- **[PDM](https://pdm.fming.dev/)**: Newer tool focusing on:
  - PEP 582 compliance
  - Fast dependency resolution
  - Modern package management

- **[Flit](https://flit.pypa.io/)**: Lightweight tool ideal for:
  - Simple Python packages
  - Quick publishing to PyPI
  - Minimal configuration

- **[uv](https://github.com/astral-sh/uv)**: New tool that is gaining popularity. It is a drop-in replacement for `setuptools` and `wheel`. Benefits include:
  - Extremely fast package installation (10-100x faster than pip)
  - Written in Rust for performance and safety
  - Compatible with existing Python tooling (requirements.txt, pyproject.toml)
  - Smart caching of wheel builds
  - Built-in virtual environment management
  - Deterministic builds with precise dependency resolution
  - Memory efficient, using ~10MB RAM vs pip's ~100MB

```{note}
Many people see `uv` as the future of Python packaging. However, it is still in its early stages, though it is gaining traction and developing fast.
```

#### Cross-platform Package Management

The need for cross-platform package managers arose primarily from challenges in distributing scientific Python packages. In the early days of pip, packages with compiled extensions (like NumPy, SciPy) were difficult to install because they required:
- Specific C/Fortran compilers
- Complex build dependencies
- Platform-specific configurations

This led to the development of more comprehensive solutions:

- **[Conda](https://docs.conda.io/)**: Industry standard for cross-platform package management, particularly in data science. Created by Continuum Analytics (now Anaconda Inc.) in 2012 to solve the "dependency hell" of scientific Python packages. Benefits include:
  - Language-agnostic package management (handles Python, R, C++, etc.)
  - Built-in environment management
  - Binary package distribution
  - Platform-specific dependency resolution
  - Large ecosystem of pre-built scientific packages
  - Strong integration with commercial tools (Anaconda)
  - Ability to install non-Python dependencies (e.g., CUDA, MKL, compilers)

```{note}
Some criticisms of Conda include:
- Slower than pip for Python-only installations
- Can be complex to debug when environment conflicts occur
- Large installation size for the base system
```

- **[Mamba](https://mamba.readthedocs.io/)**: A faster reimplementation of Conda, written in C++. Features include:
  - Parallel downloads and faster dependency solving
  - Drop-in replacement for conda commands
  - Compatible with existing conda packages
  - Much better performance for large environments
  - More reliable solver that can better explain conflicts

- **[Pixi](https://pixi.sh/dev/)**: Modern alternative to Conda, built by Prefix.dev. (Also, see [here.]((https://prefix.dev/docs/pixi/overview))) Features include:
  - Rust-based implementation for better performance
  - Compatible with existing Conda packages
  - Simpler configuration via `pixi.toml`
  - Faster environment solving
  - Built-in task running capabilities
  - Lock file for reproducible environments
  - Project-based environment management

```{note}
While Pixi is promising, it's still relatively new (launched 2023) and the ecosystem is evolving. Some users report that certain edge cases aren't yet handled as well as in Conda.
```

#### Project-Based Package Management vs Environment-Based Package Management

- **Project-Based Package Management**: This is the approach used by Hatch, Poetry, and PDM. It involves:
  - A single configuration file (`pyproject.toml`) that defines both project metadata and dependencies
  - Dependencies are specified at the project level
  - Virtual environments are created automatically based on project needs
  - Build and development dependencies are clearly separated
  - Lock files ensure reproducible builds across different machines
  - Tools typically manage the entire project lifecycle (building, testing, publishing)

  This approach has gained favor in modern Python development because:
  - It follows the "configuration as code" principle
  - Makes projects more portable and reproducible
  - Reduces the gap between development and deployment
  - Better integrates with modern CI/CD practices
  - Follows similar patterns to other language ecosystems (npm for Node.js, Cargo for Rust)

- **Environment-Based Package Management**: This is the approach used by Conda, Mamba, and Pixi. It involves:
  - Creating isolated environments that can be activated/deactivated
  - Dependencies are managed at the environment level
  - One environment can be used for multiple projects
  - Environments can include non-Python packages
  - Manual environment activation is typically required
  - Configuration often spans multiple files (environment.yml, requirements.txt)

  This approach has historically been popular because:
  - It's more flexible for scientific computing needs
  - Better handles system-level dependencies
  - Works well for exploratory data science
  - Supports multiple programming languages in one environment

#### Pros and Cons

**Project-Based Approach**
Pros:
- Clearer dependency specification
- Better reproducibility
- Integrated tooling (build, test, publish)
- More aligned with modern DevOps practices
- Smaller, more focused environments

Cons:
- Limited to Python packages
- Can be more complex for beginners
- May require additional setup for system dependencies
- Multiple projects = multiple environments

**Environment-Based Approach**
Pros:
- Handles non-Python dependencies well
- More flexible for scientific computing
- Can share environments across projects
- Better for exploratory work
- Easier for beginners

Cons:
- Less reproducible across systems
- Configuration can be scattered
- Heavier weight solutions
- Manual environment management

#### The Shift Towards Project-Based Management

The Python ecosystem has been gradually shifting towards project-based management because:

1. **Modern Development Practices**:
   - Microservices architecture demands more isolated, reproducible projects
   - CI/CD pipelines benefit from deterministic builds
   - Container-based deployment favors project-specific dependencies

2. **Lessons from Other Ecosystems**:
   - Success of npm (Node.js) and Cargo (Rust) showed benefits of project-centric approach
   - Growing emphasis on reproducible builds
   - Need for better dependency resolution

3. **Python Packaging Standards**:
   - PEP 517/518 standardized build system specification
   - `pyproject.toml` provides a single source of truth
   - Better separation of development and runtime dependencies

However, both approaches remain valid, and the choice often depends on specific needs:
- Scientific computing often favors environment-based tools
- Web development typically uses project-based tools
- Data science might use a mix of both approaches

#### Evolution of Package Management

The landscape has evolved significantly:

1. **Early Days (pre-2012)**:
   - Pip struggled with binary distributions
   - Scientific packages were difficult to install
   - No standardized solution for non-Python dependencies

2. **Conda Era (2012-present)**:
   - Solved binary distribution problems
   - Provided consistent environments across platforms
   - Became standard in scientific computing

3. **Modern Convergence**:
   - Pip's wheel format (introduced 2012) solved many binary distribution issues
   - Build tools like `cibuildwheel` made it easier to distribute compiled packages
   - Conda remains valuable for:
     - Cross-language dependencies
     - System-level packages
     - Consistent scientific computing environments

Today, the choice between pip and conda often depends on:
- Whether you need non-Python dependencies
- The specific packages you're using
- Your platform requirements
- Performance considerations

#### Choosing a Packaging Tool

While this chapter focuses on Hatch, consider these factors when choosing a tool:

- **Project Size**: Smaller projects might benefit from Flit's simplicity.
- **Team Experience**: Some teams may be more familiar with Poetry or Setuptools.
- **Corporate Requirements**: Enterprise environments might have specific tooling needs.
- **Feature Requirements**: Different tools excel at different aspects of package management.

## Example Package: `stockbeta`

The `stockbeta` package is a practical demonstration of how to write a Python library for quantitative finance. This package performs factor-based analysis of stock returns, leveraging the Fama-French Three-Factor Model. It provides tools for:

1. Loading and manipulating factor data (e.g., market returns, size, and value factors).
2. Analyzing the factor exposures of individual stocks using their historical return data.
3. Generating concise reports summarizing the findings.

I chose this example because I wanted to demonstrate how to do the following things when creating a Python package:

- Add a command-line interface (CLI) to the package.
- Add the ability to use the functions in the package as a library or from the command line.
- Ship datasets with the package.

### CLI Development: Click vs. argparse

The `stockbeta` package also demonstrates how to create a command-line interface (CLI) using [Click](https://click.palletsprojects.com/), a modern Python package for creating beautiful command line interfaces. While Python's standard library includes [argparse](https://docs.python.org/3/library/argparse.html) for CLI development, we chose Click for several reasons:

#### Why Click Over argparse?

- **Decorator-Based Interface**: Click uses decorators to define commands and options, resulting in more readable and maintainable code:
  ```python
  # Click example
  @click.command()
  @click.option('--ticker', required=True, help='Stock ticker symbol')
  def analyze(ticker):
      """Analyze a stock's factor exposures."""
      pass

  # Equivalent argparse example
  parser = argparse.ArgumentParser()
  parser.add_argument('--ticker', required=True, help='Stock ticker symbol')
  args = parser.parse_args()
  ```

- **Automatic Help Generation**: Click automatically generates well-formatted help messages and documentation.
- **Nested Command Support**: Easily create complex CLI applications with subcommands (similar to `git commit`, `git push`).
- **Type Conversion**: Automatic type conversion and validation of input parameters.
- **Better Error Messages**: More user-friendly error messages out of the box.

#### Why argparse is Still Relevant

While we chose Click for `stockbeta`, argparse remains important to understand:
- It's part of Python's standard library (no additional dependencies)
- Many existing projects use it
- It's more than adequate for simple CLI needs
- It has been the standard since Python 2.7

#### Modern CLI Development

The trend in Python CLI development has moved towards more sophisticated tools like Click because:
- They reduce boilerplate code
- They encourage better CLI design practices
- They provide better developer experience
- They often result in better user experience

For `stockbeta`, Click allows us to create an intuitive interface that makes it easy for users to:
- Specify date ranges for analysis
- Select specific stocks or factors
- Control output formats
- Access help and documentation

## Developing a Python Package with Hatch

### 1. Overview of Hatch

Hatch is a modern Python packaging tool that simplifies the development, testing, and deployment of Python packages. Its features include:

- **Environment Management**: Automatically creates isolated development environments with dependencies installed.
- **Simplified Configuration**: Uses a single `pyproject.toml` file for project metadata.
- **Command Line Tools**: Provides commands for common tasks such as running tests, checking types, and formatting code.

### 2. Setting Up the Package

- Directory structure and organization.
- Creating a `pyproject.toml` file.
- Initializing a development environment with Hatch.

### 3. Adding Functionality

- Writing core modules: example implementation of factor data loading and factor analysis.
- Packaging datasets: including sample data with the package.
- Creating a command-line interface (CLI) for ease of use.

### 4. Testing and Quality Assurance

- Writing unit tests with `pytest`.
- Running tests with Hatch.
- Configuring type checking and linting.

### 5. Documenting the Package

- Writing a README file to introduce the package and explain its usage.
- Generating API documentation.

### 6. Publishing to PyPI

- Steps to register the package on PyPI.
- Uploading the package using Hatch.

## Case Study: Using `stockbeta`

### Loading Factor Data

Demonstrate how to load factor data using the library:

```python
import stockbeta

# Load all available daily factor data
factors = stockbeta.load_factors()
```

### Analyzing Stock Returns

Show how to analyze stock returns using both the CLI and the Python library interface:

#### CLI Example
```console
python -m stockbeta.cli --ticker AAPL --start 2020-01-01 --end 2023-12-31
```

#### Library Example
```python
import stockbeta
import yfinance as yf

# Get stock data
stock_data = yf.download("AAPL", start="2020-01-01", end="2023-12-31")
stock_returns = stock_data["Adj Close"].pct_change().dropna()

# Load factors and calculate exposures
factors = stockbeta.load_factors(start="2020-01-01", end="2023-12-31")
exposures = stockbeta.calculate_factor_exposures(stock_returns, factors)

print(exposures)
```

### Development Workflow with Hatch

Explain the development process:

1. Cloning the repository.
2. Activating the Hatch shell environment.
3. Running tests and making edits.
4. Formatting and linting code.
5. Deploying updates to PyPI.

## Conclusion

By the end of this chapter, you will understand the process of creating Python packages using Hatch and see how the `stockbeta` example applies these concepts. Writing Python libraries is a valuable skill that bridges the gap between technical programming and applied finance, enabling you to create tools that are both robust and impactful.