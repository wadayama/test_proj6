"""
Central Limit Theorem Experimental Verification

This module implements an experiment to verify the Central Limit Theorem
by generating sums of uniform random variables and analyzing their distribution.
"""

import argparse
import logging
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml
from matplotlib.figure import Figure


def get_git_commit_hash() -> str:
    """
    Get the current Git repository commit hash.
    If there are uncommitted changes, append '-dirty' to the hash.

    Returns
    -------
    str
        Current commit hash, with '-dirty' suffix if there are uncommitted changes
    """
    try:
        # Get the latest commit hash
        commit_hash = (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .strip()
            .decode("utf-8")
        )

        # Check for uncommitted changes
        status = (
            subprocess.check_output(["git", "status", "--porcelain"])
            .strip()
            .decode("utf-8")
        )

        # If there are uncommitted changes, add '-dirty' suffix
        if status:
            return f"{commit_hash}-dirty"
        else:
            return commit_hash

    except (subprocess.CalledProcessError, FileNotFoundError):
        # Not a git repository or git command not found
        return "not-a-git-repo"


def calculate_uniform_sum(n: int, seed: int | None = None) -> float:
    """
    Calculate the sum of n uniform random numbers in [0,1].

    Parameters
    ----------
    n : int
        Number of uniform random variables to sum
    seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    float
        Sum of n uniform random variables
    """
    if seed is not None:
        np.random.seed(seed)

    random_numbers = np.random.uniform(0, 1, n)
    return np.sum(random_numbers)


def run_experiment(n: int, m: int, base_seed: int = 42) -> list[float]:
    """
    Run M trials of calculating the sum of n uniform random numbers.

    Parameters
    ----------
    n : int
        Number of uniform random variables to sum in each trial
    m : int
        Number of trials to perform
    base_seed : int, default=42
        Base seed for reproducibility

    Returns
    -------
    List[float]
        List of M sums from the trials
    """
    results = []

    for trial in range(m):
        # Use different seed for each trial to ensure independence
        trial_seed = base_seed + trial
        sum_result = calculate_uniform_sum(n, seed=trial_seed)
        results.append(sum_result)

    return results


def create_histogram(results: list[float], n: int, m: int, commit_hash: str) -> Figure:
    """
    Create histogram visualization of the experimental results.

    Parameters
    ----------
    results : list[float]
        List of sum results from trials
    n : int
        Number of random variables summed in each trial
    m : int
        Number of trials performed
    commit_hash : str
        Git commit hash for reproducibility tracking

    Returns
    -------
    Figure
        Matplotlib figure containing the histogram
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create histogram
    ax.hist(
        results,
        bins=30,
        density=True,
        alpha=0.7,
        color="lightgreen",
        edgecolor="black",
        label="Experimental Data",
    )

    # Theoretical normal distribution overlay
    # For sum of n uniform[0,1]: mean = n/2, variance = n/12
    theoretical_mean = n / 2
    theoretical_std = np.sqrt(n / 12)

    x = np.linspace(min(results), max(results), 100)
    theoretical_pdf = (1 / (theoretical_std * np.sqrt(2 * np.pi))) * np.exp(
        -0.5 * ((x - theoretical_mean) / theoretical_std) ** 2
    )

    ax.plot(
        x, theoretical_pdf, "r-", linewidth=2, label="Theoretical Normal Distribution"
    )

    # Calculate experimental statistics
    experimental_mean = np.mean(results)
    experimental_std = np.std(results, ddof=1)

    # Add labels and title
    ax.set_xlabel("Sum of Random Variables")
    ax.set_ylabel("Probability Density")
    ax.set_title(f"Central Limit Theorem Verification\nn={n} variables, M={m} trials")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add statistics text with commit hash
    stats_text = (
        f"Experimental: μ={experimental_mean:.3f}, σ={experimental_std:.3f}\n"
        f"Theoretical: μ={theoretical_mean:.3f}, σ={theoretical_std:.3f}\n"
        f"Git commit: {commit_hash[:8]}"
    )
    ax.text(
        0.02,
        0.98,
        stats_text,
        transform=ax.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    plt.tight_layout()
    return fig


def save_histogram_pdf(figure: Figure, output_path: Path) -> None:
    """
    Save the histogram figure as a PDF file.

    Parameters
    ----------
    figure : plt.Figure
        Matplotlib figure to save
    output_path : Path
        Path where to save the PDF file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(str(output_path), format="pdf", bbox_inches="tight", dpi=300)
    logging.info(f"Histogram saved to {output_path}")


def load_config(config_path: Path) -> dict:
    """
    Load experiment configuration from YAML file.

    Parameters
    ----------
    config_path : Path
        Path to the YAML configuration file

    Returns
    -------
    dict
        Configuration parameters
    """
    with open(config_path) as file:
        config = yaml.safe_load(file)
    return config


def find_config_files(config_dir: Path) -> list[Path]:
    """
    Find all YAML configuration files in the specified directory.

    Parameters
    ----------
    config_dir : Path
        Directory to search for configuration files

    Returns
    -------
    list[Path]
        List of YAML configuration file paths
    """
    if not config_dir.exists():
        return []

    yaml_files = list(config_dir.glob("*.yaml")) + list(config_dir.glob("*.yml"))
    return sorted(yaml_files)


def run_single_experiment(config_path: Path) -> None:
    """
    Run a single experiment with the given configuration file.

    Parameters
    ----------
    config_path : Path
        Path to the YAML configuration file
    """
    logging.info(f"Running experiment with config: {config_path}")

    # Get git commit hash for reproducibility tracking
    commit_hash = get_git_commit_hash()

    # Load configuration
    config = load_config(config_path)
    n = config["experiment"]["n"]
    m = config["experiment"]["m"]
    seed = config["experiment"]["seed"]
    output_dir = Path(config["output"]["directory"])

    logging.info(f"Experiment parameters: n={n}, M={m}, seed={seed}")

    # Run the experiment
    results = run_experiment(n, m, base_seed=seed)

    # Create histogram with commit hash
    figure = create_histogram(results, n, m, commit_hash)

    # Save results with commit hash and config name in filename
    commit_short = commit_hash[:8]
    config_name = config_path.stem
    output_path = (
        output_dir / f"central_limit_theorem_{config_name}_n{n}_m{m}_{commit_short}.pdf"
    )
    save_histogram_pdf(figure, output_path)

    # Close the figure to free memory
    plt.close(figure)

    logging.info(f"Experiment completed: {output_path}")


def main() -> None:
    """
    Main function to run the Central Limit Theorem experiment.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Central Limit Theorem Experimental Verification"
    )
    parser.add_argument(
        "-c", "--config", type=str, help="Path to specific configuration file"
    )
    parser.add_argument(
        "-b",
        "--batch",
        action="store_true",
        help="Run all experiments in config/experiments/ directory",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display histograms (only works with single experiment)",
    )
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Get git commit hash for reproducibility tracking
    commit_hash = get_git_commit_hash()
    logging.info(f"Experiment running on git commit: {commit_hash}")
    if commit_hash.endswith("-dirty"):
        logging.warning(
            "Working directory has uncommitted changes. "
            "Reproducibility might be compromised."
        )

    if args.batch:
        # Batch mode: run all experiments in config/experiments/ directory
        experiments_dir = Path("config/experiments")
        config_files = find_config_files(experiments_dir)

        if not config_files:
            logging.error(f"No configuration files found in {experiments_dir}")
            return

        logging.info(f"Found {len(config_files)} configuration files")
        for config_file in config_files:
            try:
                run_single_experiment(config_file)
            except Exception as e:
                logging.error(f"Failed to run experiment {config_file}: {e}")
                continue

        logging.info("All batch experiments completed!")

    elif args.config:
        # Single config mode
        config_path = Path(args.config)
        if not config_path.exists():
            logging.error(f"Configuration file not found: {config_path}")
            return

        run_single_experiment(config_path)

        # Display the histogram if requested
        if args.show:
            # Re-create and show the last figure
            config = load_config(config_path)
            n = config["experiment"]["n"]
            m = config["experiment"]["m"]
            seed = config["experiment"]["seed"]
            results = run_experiment(n, m, base_seed=seed)
            figure = create_histogram(results, n, m, commit_hash)
            plt.show()
            plt.close(figure)

    else:
        # Default mode: use config/experiment.yaml
        config_path = Path("config/experiment.yaml")
        if config_path.exists():
            run_single_experiment(config_path)

            # Display the histogram by default in single mode
            config = load_config(config_path)
            n = config["experiment"]["n"]
            m = config["experiment"]["m"]
            seed = config["experiment"]["seed"]
            results = run_experiment(n, m, base_seed=seed)
            figure = create_histogram(results, n, m, commit_hash)
            plt.show()
            plt.close(figure)

        else:
            logging.error(
                f"Default config file {config_path} not found. "
                "Use -c to specify a config file or -b for batch mode."
            )
            return

    logging.info("All experiments completed successfully!")


if __name__ == "__main__":
    main()
