"""
Central Limit Theorem Experimental Verification

This module implements an experiment to verify the Central Limit Theorem
by generating sums of uniform random variables and analyzing their distribution.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml
from matplotlib.figure import Figure


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


def create_histogram(results: list[float], n: int, m: int) -> Figure:
    """
    Create histogram visualization of the experimental results.

    Parameters
    ----------
    results : List[float]
        List of sum results from trials
    n : int
        Number of random variables summed in each trial
    m : int
        Number of trials performed

    Returns
    -------
    plt.Figure
        Matplotlib figure containing the histogram
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create histogram
    ax.hist(
        results,
        bins=30,
        density=True,
        alpha=0.7,
        color="skyblue",
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
    ax.set_title(f"Central Limit Theorem Verification\\nn={n} variables, M={m} trials")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add statistics text
    stats_text = (
        f"Experimental: μ={experimental_mean:.3f}, σ={experimental_std:.3f}\\n"
        f"Theoretical: μ={theoretical_mean:.3f}, σ={theoretical_std:.3f}"
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
    figure.savefig(output_path, format="pdf", bbox_inches="tight", dpi=300)
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


def main() -> None:
    """
    Main function to run the Central Limit Theorem experiment.
    """
    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Load configuration
    config_path = Path("config/experiment.yaml")
    if config_path.exists():
        config = load_config(config_path)
        n = config["experiment"]["n"]
        m = config["experiment"]["m"]
        seed = config["experiment"]["seed"]
        output_dir = Path(config["output"]["directory"])
    else:
        # Default parameters if no config file
        n = 10
        m = 1000
        seed = 42
        output_dir = Path("outputs")
        logging.warning(
            f"Config file {config_path} not found. Using default parameters."
        )

    logging.info(f"Starting experiment with n={n}, M={m}, seed={seed}")

    # Run the experiment
    results = run_experiment(n, m, base_seed=seed)

    # Create histogram
    figure = create_histogram(results, n, m)

    # Save results
    output_path = output_dir / f"central_limit_theorem_n{n}_m{m}.pdf"
    save_histogram_pdf(figure, output_path)

    # Display the histogram
    plt.show()

    logging.info("Experiment completed successfully!")


if __name__ == "__main__":
    main()
