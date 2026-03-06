"""Example analysis script.

This script demonstrates a typical analytics workflow:
  1. Load raw data (simulated here with random numbers)
  2. Clean / transform the data
  3. Compute summary statistics
  4. Export results

Run it from the project root:

    python scripts/example_analysis.py
"""

import random

from src.utils import format_number, log_step, timer

# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------


@timer
def load_data(n: int = 1_000) -> list[float]:
    """Simulate loading *n* rows of data."""
    log_step(f"Loading {n} rows of data …")
    return [random.gauss(mu=100, sigma=15) for _ in range(n)]


@timer
def clean_data(data: list[float]) -> list[float]:
    """Remove outliers (values outside µ ± 3σ)."""
    log_step("Cleaning data …")
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = variance**0.5
    lower, upper = mean - 3 * std, mean + 3 * std
    cleaned = [x for x in data if lower <= x <= upper]
    removed = len(data) - len(cleaned)
    log_step(f"Removed {removed} outlier(s). {len(cleaned)} rows remaining.")
    return cleaned


@timer
def compute_statistics(data: list[float]) -> dict[str, float]:
    """Return basic descriptive statistics for *data*."""
    log_step("Computing statistics …")
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std = variance**0.5
    sorted_data = sorted(data)
    median = sorted_data[n // 2]
    return {"count": n, "mean": mean, "std": std, "median": median}


def print_report(stats: dict[str, float]) -> None:
    """Pretty-print the statistics report."""
    log_step("Results")
    print("\n" + "=" * 40)
    print("  Analytics Report")
    print("=" * 40)
    print(f"  Count   : {format_number(stats['count'], decimals=0)}")
    print(f"  Mean    : {format_number(stats['mean'])}")
    print(f"  Std Dev : {format_number(stats['std'])}")
    print(f"  Median  : {format_number(stats['median'])}")
    print("=" * 40 + "\n")


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------


def main() -> None:
    data = load_data(n=2_000)
    data = clean_data(data)
    stats = compute_statistics(data)
    print_report(stats)


if __name__ == "__main__":
    main()
