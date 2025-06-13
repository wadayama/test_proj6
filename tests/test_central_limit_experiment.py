"""
Tests for Central Limit Theorem experiment functions.
"""

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from central_limit_experiment import (
    calculate_uniform_sum,
    create_histogram,
    find_config_files,
    get_git_commit_hash,
    load_config,
    run_experiment,
    run_single_experiment,
    save_histogram_pdf,
)


class TestCalculateUniformSum:
    """Test cases for calculate_uniform_sum function."""

    def test_reproducibility_with_seed(self):
        """Test that results are reproducible when using the same seed."""
        n = 5
        seed = 123
        result1 = calculate_uniform_sum(n, seed=seed)
        result2 = calculate_uniform_sum(n, seed=seed)
        assert result1 == result2

    def test_different_seeds_produce_different_results(self):
        """Test that different seeds produce different results."""
        n = 10
        result1 = calculate_uniform_sum(n, seed=1)
        result2 = calculate_uniform_sum(n, seed=2)
        assert result1 != result2

    def test_sum_bounds(self):
        """Test that sum is within expected bounds [0, n]."""
        n = 100
        result = calculate_uniform_sum(n, seed=42)
        assert 0 <= result <= n

    def test_single_variable(self):
        """Test behavior with n=1."""
        result = calculate_uniform_sum(1, seed=42)
        assert 0 <= result <= 1


class TestRunExperiment:
    """Test cases for run_experiment function."""

    def test_correct_number_of_trials(self):
        """Test that the correct number of trials is performed."""
        n, m = 5, 10
        results = run_experiment(n, m, base_seed=42)
        assert len(results) == m

    def test_reproducibility(self):
        """Test that experiments are reproducible with same parameters."""
        n, m = 3, 5
        base_seed = 123
        results1 = run_experiment(n, m, base_seed=base_seed)
        results2 = run_experiment(n, m, base_seed=base_seed)
        assert results1 == results2

    def test_all_results_within_bounds(self):
        """Test that all results are within expected bounds."""
        n, m = 10, 50
        results = run_experiment(n, m, base_seed=42)
        for result in results:
            assert 0 <= result <= n


class TestGetGitCommitHash:
    """Test cases for get_git_commit_hash function."""

    def test_git_commit_hash_format(self):
        """Test that git commit hash is returned in expected format."""
        commit_hash = get_git_commit_hash()
        # Should return either a valid hash, hash with -dirty, or not-a-git-repo
        assert isinstance(commit_hash, str)
        assert len(commit_hash) > 0


class TestCreateHistogram:
    """Test cases for create_histogram function."""

    def test_figure_creation(self):
        """Test that a matplotlib figure is created."""
        results = [1.0, 2.0, 3.0, 4.0, 5.0]
        n, m = 5, 5
        commit_hash = "test12345"
        figure = create_histogram(results, n, m, commit_hash)
        assert isinstance(figure, Figure)
        plt.close(figure)  # Clean up

    def test_histogram_title_content(self):
        """Test that histogram contains expected title."""
        results = [2.5, 3.0, 2.8, 3.2, 2.9]
        n, m = 5, 5
        commit_hash = "test12345"
        figure = create_histogram(results, n, m, commit_hash)

        # Get the axis and check title
        ax = figure.axes[0]
        title = ax.get_title()
        assert f"n={n}" in title
        assert f"M={m}" in title

        plt.close(figure)  # Clean up


class TestSaveHistogramPdf:
    """Test cases for save_histogram_pdf function."""

    def test_pdf_file_creation(self):
        """Test that PDF file is created successfully."""
        # Create a simple figure
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 2])

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_histogram.pdf"
            save_histogram_pdf(fig, output_path)

            assert output_path.exists()
            assert output_path.suffix == ".pdf"

        plt.close(fig)  # Clean up

    def test_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 2])

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "subdir" / "test_histogram.pdf"
            save_histogram_pdf(fig, output_path)

            assert output_path.parent.exists()
            assert output_path.exists()

        plt.close(fig)  # Clean up


class TestLoadConfig:
    """Test cases for load_config function."""

    def test_config_loading(self):
        """Test that YAML configuration is loaded correctly."""
        config_content = """
experiment:
  n: 15
  m: 2000
  seed: 999
output:
  directory: "test_outputs"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(config_content)
            config_path = Path(f.name)

        try:
            config = load_config(config_path)

            assert config["experiment"]["n"] == 15
            assert config["experiment"]["m"] == 2000
            assert config["experiment"]["seed"] == 999
            assert config["output"]["directory"] == "test_outputs"
        finally:
            config_path.unlink()  # Clean up temp file


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_complete_workflow(self):
        """Test the complete experimental workflow."""
        # Small scale test
        n, m = 3, 10
        base_seed = 42

        # Run experiment
        results = run_experiment(n, m, base_seed=base_seed)

        # Verify results
        assert len(results) == m
        assert all(0 <= result <= n for result in results)

        # Create histogram
        commit_hash = "test12345"
        figure = create_histogram(results, n, m, commit_hash)
        assert isinstance(figure, Figure)

        # Test PDF saving
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "integration_test.pdf"
            save_histogram_pdf(figure, output_path)
            assert output_path.exists()

        plt.close(figure)  # Clean up


class TestFindConfigFiles:
    """Test cases for find_config_files function."""

    def test_find_yaml_files(self):
        """Test finding YAML files in a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir)

            # Create some test files
            (config_dir / "config1.yaml").write_text("test: 1")
            (config_dir / "config2.yml").write_text("test: 2")
            (config_dir / "not_config.txt").write_text("test: 3")

            found_files = find_config_files(config_dir)

            assert len(found_files) == 2
            assert any(f.name == "config1.yaml" for f in found_files)
            assert any(f.name == "config2.yml" for f in found_files)
            assert not any(f.name == "not_config.txt" for f in found_files)

    def test_empty_directory(self):
        """Test behavior with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir)
            found_files = find_config_files(config_dir)
            assert found_files == []

    def test_nonexistent_directory(self):
        """Test behavior with non-existent directory."""
        nonexistent_dir = Path("/nonexistent/directory")
        found_files = find_config_files(nonexistent_dir)
        assert found_files == []


class TestRunSingleExperiment:
    """Test cases for run_single_experiment function."""

    def test_single_experiment_execution(self):
        """Test that single experiment runs without errors."""
        config_content = """
experiment:
  n: 3
  m: 5
  seed: 42
output:
  directory: "test_outputs"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(config_content)
            config_path = Path(f.name)

        try:
            # This should run without raising an exception
            run_single_experiment(config_path)

            # Check that output file was created
            expected_output_dir = Path("test_outputs")
            if expected_output_dir.exists():
                pdf_files = list(expected_output_dir.glob("*.pdf"))
                assert len(pdf_files) > 0

                # Clean up output files
                for pdf_file in pdf_files:
                    pdf_file.unlink()
                expected_output_dir.rmdir()

        finally:
            config_path.unlink()  # Clean up temp file
