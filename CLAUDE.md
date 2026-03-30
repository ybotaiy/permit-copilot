# Permit Copilot

Permit Copilot is a skill-native workspace for drafting responses to NYC DOB correction letters.

## Core Rules

- Skills are the product. Do not rebuild a Python processing pipeline.
- The authoritative local corpus lives in `data/knowledge/`.
- `data/knowledge/_index.md` is the manifest for what has been ingested.
- Never invent code citations, quotations, or section numbers.
- Only cite text you actually found in `data/knowledge/`.
- If the local corpus is insufficient, say so clearly and mark the result low confidence.

## Repo Map

- `.claude/skills/ingest.md`
  Builds or refreshes the Markdown knowledge base.
- `.claude/skills/search-codes.md`
  Searches `data/knowledge/` by section number, keyword, or topic.
- `.claude/skills/analyze-letter.md`
  Parses correction letters, retrieves supporting authority, and drafts responses.
- `data/knowledge/`
  Version-controlled Markdown corpus with YAML frontmatter.
- `data/samples/`
  Sample objection letters and fixtures for evaluation.
- `eval/eval_harness.py`
  Standalone parser/classifier evaluation script.
- `tests/test_eval.py`
  Ground-truth tests for the standalone eval harness.

## Knowledge File Format

Every knowledge file should contain:

1. YAML frontmatter with `source`, `chapter`, `title`, `doc_type`, `version`, `url`, and `scraped_at`.
2. A Markdown body that uses `##` headings for individual `§` sections when possible.
3. Faithful source text with formatting cleanup only.

## Skill Expectations

### /ingest

- Read external source material or local PDFs.
- Write normalized Markdown files into `data/knowledge/`.
- Rebuild `_index.md` after updates.

### /search-codes

- Use `Grep` and `Read` against `data/knowledge/`.
- Prefer exact section hits before keyword matches.
- Cite source files and section numbers in every answer.

### /analyze-letter

- Parse each numbered objection item from the user’s letter.
- Search the local corpus for supporting authority.
- Draft issue-by-issue responses with citations and confidence labels.
- Remind the user that outputs are drafts requiring human review.

## Evaluation

The only required Python that remains in this repo is the standalone eval harness.

- Run `uv run pytest tests -v` for the automated checks.
- Run `python eval/eval_harness.py` for a direct PASS or FAIL summary.

Keep the eval logic self-contained. Do not import any deleted `src/` package code.
