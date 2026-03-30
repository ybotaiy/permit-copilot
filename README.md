# permit-copilot

Skill-native copilot for NYC DOB correction-letter response drafting.

## Architecture

This repo is built around Claude skills, not a Python processing pipeline.

- `/ingest` builds the local Markdown knowledge base in `data/knowledge/`
- `/search-codes` searches the checked-in corpus by section number or keyword
- `/analyze-letter` parses objection letters, retrieves support, and drafts cited responses

The local corpus is the only authority for drafting. If a citation is not found in `data/knowledge/`, it must not be invented.

## Repo Layout

```text
.claude/skills/      Skill definitions for ingest, search, and analysis
data/knowledge/      Version-controlled Markdown knowledge base
data/samples/        Sample objection-letter fixtures
eval/eval_harness.py Standalone parser/classifier evaluation script
tests/test_eval.py   Ground-truth tests for the eval harness
CLAUDE.md            Project guide for agents
```

## Working With The Skills

Use these slash commands inside Claude Code:

- `/ingest` to fetch and normalize source material into `data/knowledge/`
- `/search-codes` to look up code sections or topics in the local corpus
- `/analyze-letter` to turn a correction letter into issue-by-issue draft responses

## Development

```bash
# Install the project and dev tooling
uv sync --extra dev

# Run the standalone tests
uv run pytest tests -v

# Run the standalone eval harness
python eval/eval_harness.py
```

## Current State

The repository ships with a knowledge-base skeleton and a synthetic objection-letter fixture. Populate the actual corpus by running `/ingest`.
