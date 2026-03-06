"""Utility helpers shared across all analytics scripts."""

import logging
import time
from functools import wraps
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------


def log_step(message: str) -> None:
    """Log a high-level pipeline step."""
    logger.info("▶ %s", message)


# ---------------------------------------------------------------------------
# Timing decorator
# ---------------------------------------------------------------------------


def timer(func):
    """Decorator that logs the execution time of *func*."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("✓ %s finished in %.2fs", func.__name__, elapsed)
        return result

    return wrapper


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def format_number(value: float, decimals: int = 2) -> str:
    """Return a human-readable string for *value* with thousand separators.

    Examples
    --------
    >>> format_number(1234567.891)
    '1,234,567.89'
    """
    return f"{value:,.{decimals}f}"


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------


def load_config(path: str) -> dict[str, Any]:
    """Load a JSON or TOML configuration file and return it as a dict.

    Parameters
    ----------
    path:
        Absolute or relative path to a ``.json`` or ``.toml`` file.

    Raises
    ------
    ValueError
        If the file extension is not ``.json`` or ``.toml``.
    FileNotFoundError
        If *path* does not exist.
    """
    import json
    from pathlib import Path

    file = Path(path)
    if not file.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    if file.suffix == ".json":
        with file.open() as fh:
            return json.load(fh)

    if file.suffix == ".toml":
        try:
            import tomllib  # Python ≥ 3.11
        except ImportError:
            import tomli as tomllib  # type: ignore[no-redef]
        with file.open("rb") as fh:
            return tomllib.load(fh)

    raise ValueError(f"Unsupported config format: {file.suffix!r}. Use .json or .toml")
