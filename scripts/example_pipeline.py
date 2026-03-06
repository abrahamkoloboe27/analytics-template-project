"""Example pipeline script.

This script shows how to build a multi-step data pipeline by chaining
discrete, testable functions.  Each step is timed automatically via the
``@timer`` decorator from ``src.utils``.

Run it from the project root:

    python scripts/example_pipeline.py
"""

import random
from dataclasses import dataclass

from src.utils import log_step, timer

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Record:
    id: int
    value: float
    label: str = ""
    is_valid: bool = True


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------


@timer
def extract(n: int = 500) -> list[Record]:
    """Simulate extracting records from a data source."""
    log_step(f"Extracting {n} records …")
    return [Record(id=i, value=random.uniform(0, 1_000)) for i in range(n)]


@timer
def validate(records: list[Record]) -> list[Record]:
    """Mark records with negative or zero values as invalid."""
    log_step("Validating records …")
    for record in records:
        record.is_valid = record.value > 0
    invalid = sum(1 for r in records if not r.is_valid)
    log_step(f"{invalid} invalid record(s) found.")
    return records


@timer
def transform(records: list[Record]) -> list[Record]:
    """Apply a label based on value thresholds (only valid records)."""
    log_step("Transforming records …")
    for record in records:
        if not record.is_valid:
            continue
        if record.value < 250:
            record.label = "low"
        elif record.value < 750:
            record.label = "medium"
        else:
            record.label = "high"
    return records


@timer
def load(records: list[Record]) -> dict[str, list[Record]]:
    """Group records by label and 'load' them into a destination store.

    In a real pipeline this would write to a database, data-lake, etc.
    Here we simply group them in-memory and print a summary.
    """
    log_step("Loading records into destination …")
    groups: dict[str, list[Record]] = {}
    for record in records:
        groups.setdefault(record.label, []).append(record)

    print("\n" + "=" * 40)
    print("  Pipeline Summary")
    print("=" * 40)
    for label, group in sorted(groups.items()):
        print(f"  {label:<10}: {len(group):>5} records")
    print("=" * 40 + "\n")

    return groups


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------


def run_pipeline(n: int = 500) -> dict[str, list[Record]]:
    records = extract(n=n)
    records = validate(records)
    records = transform(records)
    return load(records)


if __name__ == "__main__":
    run_pipeline()
