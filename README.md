# permit-copilot

AI copilot for building permit applications.

## Setup

```bash
uv sync
```

## Usage

```bash
# Show help
python -m src.main --help

# Or via package entry
python -m src --help

# Run the hello command
python -m src.main hello
```

## Knowledge Base

Download official NYC DOB documents into `kb/raw/`:

```bash
# Download all documents from the manifest
uv run python -m src.main ingest download

# Force re-download existing files
uv run python -m src.main ingest download --force
```

The manifest is defined in `kb/manifest.yaml`.

## Development

```bash
# Lint
uv run ruff check .

# Run tests
uv run pytest
```
