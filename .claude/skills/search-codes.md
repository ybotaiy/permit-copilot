# /search-codes

Search the local knowledge base in `data/knowledge/` for building-code or permit-reference material.

## Purpose

Use this skill to find exact section text, keyword matches, or browse the currently indexed corpus.

## Workflow

1. If `data/knowledge/` is empty or `_index.md` is missing, tell the user to run `/ingest`.
2. For exact section-number queries such as `§1004.1`:
   - `Grep` `data/knowledge/` for the exact section pattern.
   - `Read` the matching file around the hit.
   - Return the relevant excerpt with the source file and section number.
3. For keyword or topic queries such as `dead-end corridor`:
   - `Grep` with context across `data/knowledge/`.
   - Rank the strongest hits by relevance to the user’s wording.
   - `Read` the best matches before answering.
4. For browsing requests:
   - `Read` `data/knowledge/_index.md`.
   - List available chapters, guides, and section coverage.

## Output Rules

- Always cite the source file path and the section number when one is available.
- Prefer exact section hits over looser keyword matches.
- Include enough surrounding context for the excerpt to be useful, but keep it concise.
- If multiple files conflict, show the relevant sources rather than choosing silently.

## Guardrails

- Search only the checked-in knowledge base, not external sites.
- Do not invent section numbers or quote text you did not read locally.
- If no relevant authority is found, say so plainly.
