# /ingest

Build or refresh the version-controlled knowledge base in `data/knowledge/`.

## Purpose

Use this skill whenever the repository needs new source material in Markdown form. The output is a structured corpus that other skills can search directly with `Grep` and `Read`.

## Output Locations

- `data/knowledge/_index.md`
- `data/knowledge/nyc-building-code/*.md`
- `data/knowledge/<doc-type>/*.md` for any additional reference documents

## Required Output Format

Every generated knowledge file must use this frontmatter shape:

```yaml
---
source: "NYC Building Code 2022"
chapter: "10"
title: "Means of Egress"
doc_type: building_code
version: "2022"
url: "https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCbldgcode/0-0-0-10"
scraped_at: "2026-03-29"
---
```

The Markdown body must use `##` headings for each cited `§` section so later searches can jump directly to the right authority.

## Default Source Map

Use this seed source map when the user asks for the legacy references that were previously kept in `kb/manifest.yaml`:

- `plan-exam-page` → `https://www.nyc.gov/site/buildings/industry/permits-plan-exam.page`
- `obj-review-factsheet` → `https://www.nyc.gov/assets/buildings/pdf/obj_rev_factsheet.pdf`
- `second-review-factsheet` → `https://www.nyc.gov/assets/buildings/pdf/fact-sheet-review-of-objections.pdf`
- `dob-now-build-manual` → `https://www.nyc.gov/assets/buildings/pdf/dob_now_build_user_manual.pdf`
- `energy-objections-guide` → `https://www.nyc.gov/assets/buildings/pdf/dob_now_build_energy_appointments_objections_step_by_step_guide.pdf`
- `required-items-guide` → `https://www.nyc.gov/assets/buildings/pdf/req_items_ref_guide.pdf`
- `ndr-std-drawings` → `https://www.nyc.gov/assets/buildings/pdf/ndr_std_drawings.pdf`
- `jc-zra-zoning-page` → `https://www.jerseycitynj.gov/cityhall/housinganddevelopment/zoning`

If the user supplies NYC Building Code chapter URLs, save those chapter files under `data/knowledge/nyc-building-code/`.

## Workflow

1. Confirm the target sources.
2. For each web source, fetch it with `WebFetch`.
3. Normalize the content into Markdown with YAML frontmatter.
4. Preserve code citations exactly as published.
5. Turn each `§` section into a `##` heading when the source structure supports it.
6. Write the output file into the correct `data/knowledge/` subdirectory.
7. Rebuild `data/knowledge/_index.md` so it lists each file, title, source, and available sections.
8. Report what was created, how many sections were captured, and any failures or gaps.

## Local PDF Mode

If the user provides a local PDF path:

1. Read the PDF directly.
2. Extract the authoritative text without inventing missing content.
3. Choose the most appropriate `data/knowledge/<doc-type>/` destination.
4. Write a Markdown file with frontmatter and section headings.
5. Update `_index.md`.

## Guardrails

- Do not fabricate URLs, code language, or section numbers.
- Keep source wording faithful; clean formatting, not substance.
- If a chapter or PDF cannot be parsed cleanly, say so and note the failure in the summary.
- Do not write outside `data/knowledge/`.
