# ─────────────────────────────────────────────────────────────────────────────
# Stage 1 — builder
#   Install uv and resolve/install all Python dependencies into an isolated
#   virtual environment.  This stage is discarded from the final image, so
#   build tools never end up in production.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12.9-slim AS builder

# Install uv (fast Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy dependency files first to leverage Docker layer cache:
# these layers are only rebuilt when pyproject.toml or uv.lock change.
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies into /app/.venv (no editable install yet)
RUN uv sync --frozen --no-install-project

# ─────────────────────────────────────────────────────────────────────────────
# Stage 2 — final image
#   Copy the pre-built virtual environment from the builder stage, then copy
#   the application source code.  Only the minimal runtime is included.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12.9-slim

WORKDIR /app

# Copy the resolved virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY src/ ./src/
COPY scripts/ ./scripts/

# Ensure the project package (src/) is installed in the venv
COPY pyproject.toml uv.lock .python-version ./
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
RUN uv sync --frozen

# Add the venv's bin directory to PATH so that `python` resolves to the venv
ENV PATH="/app/.venv/bin:$PATH"

# Default command: run the minimal entry-point script.
# Override at runtime to run any other script:
#   docker run --rm analytics-template python scripts/example_analysis.py
CMD ["python", "scripts/main.py"]
