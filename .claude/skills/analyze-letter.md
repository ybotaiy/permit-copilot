# /analyze-letter

Analyze a DOB correction letter or objection sheet and draft response language backed only by the local knowledge base.

## Inputs

- A local file path to a PDF or text file
- Pasted correction-letter text

## Workflow

1. Read the correction letter.
2. Parse each numbered objection item.
3. For each issue, extract:
   - issue number
   - full objection text
   - any cited code sections
   - a one-line summary
   - a category such as `egress`, `fire`, `accessibility`, `zoning`, or `other`
4. Retrieve support from `data/knowledge/`:
   - `Grep` exact code sections first
   - `Grep` key terms from the objection text second
   - `Read` the strongest matching sections before drafting
5. Draft a response for each issue that:
   - cites only authority found in `data/knowledge/`
   - uses bracketed citations such as `[NYC BC §1004.1.2]`
   - suggests plan-note, drawing, or filing-language updates when supported
   - identifies missing facts, documents, or consultant input still needed
6. Present the results issue by issue.
7. Write an export Markdown file when the user asks for one.

## Required Output Shape

For each issue, provide:

- `Examiner objection`
- `Category`
- `Draft response`
- `Citations`
- `Confidence`

Confidence levels:

- `high` when the local knowledge base clearly addresses the issue
- `medium` when the authority is relevant but incomplete
- `low` when evidence is sparse or indirect

## Export Rules

When exporting, write a Markdown checklist with one section per issue and a reminder that all responses require human review before submission.

## Guardrails

- You must NOT invent code sections.
- Cite only text you actually found by grepping and reading `data/knowledge/`.
- If you cannot find relevant authority, say so and mark confidence as `low`.
- Do not imply legal or filing certainty beyond what the knowledge base supports.
