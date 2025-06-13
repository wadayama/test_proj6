# Central Limit Theorem Experimental Verification

This project implements a numerical experiment to verify the Central Limit Theorem using Python. The experiment generates sums of uniform random variables and analyzes their distribution to demonstrate the convergence to a normal distribution.

## Overview

The Central Limit Theorem states that the sum of a large number of independent random variables approaches a normal distribution, regardless of the underlying distribution of the individual variables. This experiment demonstrates this principle using uniform random variables in the range [0,1].

## Experiment Design

1. Generate n uniform random variables in the range [0,1]
2. Calculate their sum
3. Repeat this process M times to collect M sum values
4. Display the results as a histogram and compare with the theoretical normal distribution

## Requirements

- Python ≥ 3.11
- Dependencies: numpy, matplotlib, pyyaml
- Development dependencies: pytest, ruff, pyright

## Installation

Install dependencies using uv:

```bash
uv sync
```

## Usage

### Basic Usage

Run the experiment with default parameters:

```bash
python central_limit_experiment.py
```

### Configuration

Modify experiment parameters in `config/experiment.yaml`:

```yaml
experiment:
  n: 10      # Number of uniform random variables per trial
  m: 1000    # Number of trials
  seed: 42   # Random seed for reproducibility

output:
  directory: "outputs"  # Output directory for PDF files
```

### Output

The experiment generates:
- A histogram visualization comparing experimental results with theoretical normal distribution
- PDF file saved to the outputs directory with filename format: `central_limit_theorem_n{n}_m{m}_{git_hash}.pdf`
- Git commit hash tracking for reproducibility

## Testing

Run tests:

```bash
pytest tests/
```

## Code Quality

Run linting and type checking:

```bash
ruff check .
pyright
```

## Project Structure

```
├── central_limit_experiment.py  # Main experiment implementation
├── config/
│   └── experiment.yaml         # Experiment configuration
├── tests/
│   └── test_central_limit_experiment.py  # Unit tests
├── outputs/                    # Generated histogram PDFs
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## Features

- Configurable experiment parameters
- Git commit hash tracking for reproducibility
- Statistical comparison between experimental and theoretical results
- Professional histogram visualization with overlaid theoretical distribution
- Comprehensive logging and error handling