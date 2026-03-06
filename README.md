# Analytics Template Project

> A ready-to-use Python analytics project template powered by **[uv](https://docs.astral.sh/uv/)** and **[ruff](https://docs.astral.sh/ruff/)**.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Prerequisites](#prerequisites)
3. [Getting Started](#getting-started)
   - [1 · Clone the repository](#1--clone-the-repository)
   - [2 · Install uv](#2--install-uv)
   - [3 · Install dependencies](#3--install-dependencies)
   - [4 · Activate the virtual environment](#4--activate-the-virtual-environment)
4. [Running Scripts](#running-scripts)
5. [Code Quality with Ruff](#code-quality-with-ruff)
   - [Format](#format)
   - [Lint / Check](#lint--check)
   - [Pre-push checklist](#pre-push-checklist)
6. [Development Workflow](#development-workflow)
7. [Adding New Scripts and Utilities](#adding-new-scripts-and-utilities)

---

## Project Structure

```
analytics-template-project/
├── pyproject.toml              # Project metadata, dependencies, ruff config
├── uv.lock                     # Locked dependency graph (committed to git)
├── .python-version             # Python version pin used by uv
├── .gitignore
│
├── scripts/                    # ← Entry-point scripts (one file = one job)
│   ├── main.py                 #   Minimal hello-world entry point
│   ├── example_analysis.py     #   Example: descriptive statistics pipeline
│   └── example_pipeline.py     #   Example: multi-step ETL pipeline
│
└── src/                        # ← Re-usable source packages
    └── utils/
        ├── __init__.py         #   Public re-exports
        └── helpers.py          #   Logging, timing, formatting, config helpers
```

**Convention:**

| Location | What goes there |
|---|---|
| `scripts/` | Runnable scripts with a `main()` function and an `if __name__ == "__main__"` guard |
| `src/utils/` | Re-usable helpers imported by multiple scripts |
| `src/<domain>/` | Domain-specific modules (e.g. `src/models/`, `src/data/`) – add as needed |

---

## Prerequisites

| Tool | Minimum version | Notes |
|---|---|---|
| **Python** | 3.12 | Managed automatically by uv |
| **uv** | 0.4+ | Fast Python package & project manager |
| **git** | any | |

---

## Getting Started

### 1 · Clone the repository

```bash
git clone https://github.com/<your-org>/analytics-template-project.git
cd analytics-template-project
```

### 2 · Install uv

```bash
# macOS / Linux (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip (works everywhere Python is already installed)
pip install uv
```

Verify the installation:

```bash
uv --version
```

### 3 · Install dependencies

`uv sync` reads `pyproject.toml` and `uv.lock` and creates a local `.venv` with all dependencies pinned:

```bash
uv sync
```

> **Tip:** `uv sync` also installs the correct Python version automatically if it is not already present on your machine, thanks to the `.python-version` file.

### 4 · Activate the virtual environment

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (cmd)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Your prompt will change to show `(gozem-analytics-template)` (or similar), confirming the environment is active.

> **Tip:** you can also run any command *without* activating the environment by prefixing it with `uv run`:
> ```bash
> uv run python scripts/example_analysis.py
> ```

---

## Running Scripts

All scripts live in `scripts/` and must be run **from the project root** so that the `src` package is importable:

```bash
# Minimal entry point
python scripts/main.py

# Example: descriptive statistics on simulated data
python scripts/example_analysis.py

# Example: multi-step ETL pipeline
python scripts/example_pipeline.py
```

Expected output for `example_analysis.py`:

```
2026-01-01 12:00:00 [INFO] ▶ Loading 2000 rows of data …
2026-01-01 12:00:00 [INFO] ✓ load_data finished in 0.01s
2026-01-01 12:00:00 [INFO] ▶ Cleaning data …
2026-01-01 12:00:00 [INFO] ▶ Removed 4 outlier(s). 1996 rows remaining.
2026-01-01 12:00:00 [INFO] ✓ clean_data finished in 0.00s
...
========================================
  Analytics Report
========================================
  Count   : 1,996
  Mean    : 100.12
  Std Dev :  14.87
  Median  : 100.34
========================================
```

---

## Code Quality with Ruff

[**Ruff**](https://docs.astral.sh/ruff/) is an extremely fast Python linter and formatter (written in Rust). It replaces `flake8`, `isort`, `pyupgrade`, and `black` in a single tool.

The project's ruff configuration lives in `pyproject.toml` under `[tool.ruff]`.

### Format

Auto-format all Python files to match the project style:

```bash
ruff format .
```

Check what *would* change without actually writing files:

```bash
ruff format --check .
```

### Lint / Check

Run all configured lint rules and report issues:

```bash
ruff check .
```

Auto-fix safe issues (imports, unused variables, etc.):

```bash
ruff check --fix .
```

### Pre-push checklist

Run both commands before every `git push` to keep the codebase clean:

```bash
ruff format .       # 1. Auto-format
ruff check --fix .  # 2. Auto-fix lint issues
ruff check .        # 3. Confirm no remaining issues
git add -u
git commit -m "style: ruff format & check"
git push
```

> **Automate it:** add a [pre-commit](https://pre-commit.com/) hook or a CI step that runs `ruff format --check . && ruff check .` to enforce quality on every pull request.

---

## Development Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  git clone → cd project → uv sync → source .venv/bin/activate  │
│                                                                  │
│  ┌─────────────┐     ┌─────────────┐     ┌───────────────────┐ │
│  │  Write code │ ──▶ │  Run script │ ──▶ │  ruff format .    │ │
│  │  in scripts/│     │  python     │     │  ruff check .     │ │
│  │  or src/    │     │  scripts/…  │     │                   │ │
│  └─────────────┘     └─────────────┘     └────────┬──────────┘ │
│                                                    │            │
│                                               git push          │
└────────────────────────────────────────────────────────────────-┘
```

1. **Create a feature branch** – `git checkout -b feature/my-analysis`
2. **Write / edit code** in `scripts/` (new job) or `src/` (reusable utility)
3. **Run your script** – `python scripts/my_analysis.py`
4. **Format & lint** – `ruff format . && ruff check --fix .`
5. **Commit** – `git add . && git commit -m "feat: add my-analysis script"`
6. **Push** – `git push origin feature/my-analysis`
7. **Open a Pull Request**

---

## Adding New Scripts and Utilities

### New script

```bash
# Create the file
touch scripts/my_new_script.py
```

Minimal template:

```python
"""One-line description of what this script does."""

from src.utils import log_step, timer


@timer
def run() -> None:
    log_step("Starting …")
    # your logic here


if __name__ == "__main__":
    run()
```

### New utility module

```bash
# Example: add a data-loading module
touch src/data/__init__.py
touch src/data/loaders.py
```

Import it from any script:

```python
from src.data.loaders import load_csv
```

### Adding a new dependency

```bash
uv add <package-name>          # adds to pyproject.toml + updates uv.lock
uv add --dev <package-name>    # development-only dependency
```

Always commit both `pyproject.toml` **and** `uv.lock` so that every team member gets exactly the same environment.
