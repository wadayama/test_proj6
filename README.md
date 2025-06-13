# Central Limit Theorem Experimental Verification

This project implements a numerical experiment to verify the Central Limit Theorem using Python. The experiment generates sums of uniform random variables and analyzes their distribution to demonstrate the convergence to a normal distribution.

The programgs in the repository was geneted by *Calaude code*. This is a trial for automtic generation of a program for scientific computing.

## Overview

The Central Limit Theorem states that the sum of a large number of independent random variables approaches a normal distribution, regardless of the underlying distribution of the individual variables. This experiment demonstrates this principle using uniform random variables in the range [0,1].

## Experiment Design

1. Generate n uniform random variables in the range [0,1]
2. Calculate their sum
3. Repeat this process M times to collect M sum values
4. Display the results as a histogram and compare with the theoretical normal distribution

## Installation

### Prerequisites

- Python ≥ 3.11
- [uv](https://docs.astral.sh/uv/) package manager
- Dependencies: numpy, matplotlib, pyyaml
- Development dependencies: pytest, ruff, pyright

### Setup

Install dependencies using uv:

```bash
# Sync dependencies from pyproject.toml and uv.lock
uv sync

# For exact reproduction of the development environment
uv sync --frozen
```

## Usage

### Basic Usage

Run the experiment with default parameters (uses `config/experiment.yaml`):

```bash
uv run python central_limit_experiment.py
```

### Multiple Experiment Configurations

This project supports running multiple experiment configurations:

#### 1. Single Experiment with Specific Configuration

Run a specific configuration file:

```bash
uv run python central_limit_experiment.py -c config/experiments/small_experiment.yaml
```

Display the histogram for a single experiment:

```bash
uv run python central_limit_experiment.py -c config/experiments/medium_experiment.yaml --show
```

#### 2. Batch Execution

Run all experiments in the `config/experiments/` directory:

```bash
uv run python central_limit_experiment.py -b
```

This will execute all `.yaml` and `.yml` files found in `config/experiments/` automatically.

### Configuration Files

#### Default Configuration
Modify experiment parameters in `config/experiment.yaml`:

```yaml
experiment:
  n: 10      # Number of uniform random variables per trial
  m: 1000    # Number of trials
  seed: 42   # Random seed for reproducibility

output:
  directory: "outputs"  # Output directory for PDF files
```

#### Multiple Experiment Setup
Create multiple configuration files in `config/experiments/` directory:

- `small_experiment.yaml` - Quick testing (n=5, m=100)
- `medium_experiment.yaml` - Medium scale (n=20, m=5000)  
- `large_experiment.yaml` - Large scale (n=50, m=10000)
- `comparison_low_n.yaml` - Low n comparison (n=3, m=2000)
- `comparison_high_n.yaml` - High n comparison (n=100, m=2000)

### Command Line Options

```bash
# Run default experiment
uv run python central_limit_experiment.py

# Run specific configuration
uv run python central_limit_experiment.py -c path/to/config.yaml

# Run specific configuration with histogram display
uv run python central_limit_experiment.py -c path/to/config.yaml --show

# Run all experiments in batch mode
uv run python central_limit_experiment.py -b

# Get help
uv run python central_limit_experiment.py -h
```

### Output

The experiment generates:
- A histogram visualization comparing experimental results with theoretical normal distribution
- PDF file saved to the outputs directory with filename format: `central_limit_theorem_{config_name}_n{n}_m{m}_{git_hash}.pdf`
- Git commit hash tracking for reproducibility
- Automatic output file organization by configuration name

## Testing

Run tests:

```bash
uv run pytest tests/
```

## Code Quality

Run linting and type checking:

```bash
uv run ruff format .
uv run ruff check .
uv run pyright
```

### Complete Development Workflow

Before committing changes, run the complete quality check:

```bash
uv run ruff format .
uv run ruff check .
uv run pyright
uv run pytest
```

## Project Structure

```
├── central_limit_experiment.py  # Main experiment implementation
├── config/
│   ├── experiment.yaml         # Default experiment configuration
│   └── experiments/            # Multiple experiment configurations
│       ├── small_experiment.yaml
│       ├── medium_experiment.yaml
│       ├── large_experiment.yaml
│       ├── comparison_low_n.yaml
│       └── comparison_high_n.yaml
├── tests/
│   └── test_central_limit_experiment.py  # Unit tests
├── outputs/                    # Generated histogram PDFs
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## Features

- **Multiple Experiment Configurations**: Support for running multiple experiment setups with different parameters
- **Batch Processing**: Execute all experiments in a directory with a single command
- **Command Line Interface**: Flexible CLI with options for single experiments, batch runs, and histogram display
- **Configurable Parameters**: Easy-to-modify YAML configuration files
- **Git Commit Hash Tracking**: Reproducibility tracking with automatic commit hash embedding
- **Statistical Analysis**: Comparison between experimental and theoretical results
- **Professional Visualization**: High-quality histogram plots with overlaid theoretical distributions
- **Comprehensive Testing**: Full test suite covering all functionality
- **Logging**: Detailed logging and error handling for debugging