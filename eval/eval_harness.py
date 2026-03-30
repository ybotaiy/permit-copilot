from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

try:
    import pandas as pd
except ImportError:  # pragma: no cover - optional for plain `python` runs
    pd = None

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "samples" / "sample_objection_sheet.txt"

ISSUE_PATTERN = re.compile(r"(?ms)^\s*(\d+)\.\s+(.*?)(?=^\s*\d+\.\s+|\Z)")
SECTION_PATTERN = re.compile(r"§\s*\d{3,4}(?:\.\d+)+")

CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "egress": (
        "occupant load",
        "egress",
        "exit",
        "corridor",
        "dead-end",
        "stair",
        "travel distance",
    ),
    "fire_resistance": (
        "fire-resistance",
        "fire resistance",
        "shaft",
        "rated",
        "assembly",
        "fire rating",
    ),
    "accessibility": (
        "accessible",
        "accessibility",
        "clear floor space",
        "maneuvering clearance",
        "a117.1",
    ),
    "zoning": ("zoning", "use group", "floor area", "lot coverage", "setback"),
}

GROUND_TRUTH: dict[int, dict[str, object]] = {
    1: {
        "category": "egress",
        "sections": ["§1004.1.2"],
    },
    2: {
        "category": "egress",
        "sections": ["§1020.4"],
    },
    3: {
        "category": "fire_resistance",
        "sections": ["§713.4"],
    },
    4: {
        "category": "accessibility",
        "sections": ["§1104.3", "§404.2.3"],
    },
}


@dataclass(frozen=True)
class ParsedIssue:
    issue_number: int
    text: str
    cited_sections: list[str]
    summary: str


def parse_issues(text: str) -> list[ParsedIssue]:
    issues: list[ParsedIssue] = []

    for match in ISSUE_PATTERN.finditer(text):
        issue_number = int(match.group(1))
        issue_text = " ".join(match.group(2).split())
        issues.append(
            ParsedIssue(
                issue_number=issue_number,
                text=issue_text,
                cited_sections=SECTION_PATTERN.findall(issue_text),
                summary=summarize_issue(issue_text),
            )
        )

    return issues


def summarize_issue(issue_text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", issue_text.strip(), maxsplit=1)
    return sentences[0].rstrip(".")


def classify_issue(issue_text: str) -> str:
    lowered = issue_text.lower()
    best_category = "other"
    best_score = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in lowered)
        if score > best_score:
            best_category = category
            best_score = score

    return best_category


def evaluate_fixture(sample_path: Path = SAMPLE_PATH) -> dict[str, object]:
    parsed_issues = parse_issues(sample_path.read_text())
    actual_by_number = {issue.issue_number: issue for issue in parsed_issues}
    rows: list[dict[str, object]] = []

    for issue_number, expected in GROUND_TRUTH.items():
        actual = actual_by_number.get(issue_number)
        actual_category = classify_issue(actual.text) if actual else "missing"
        actual_sections = actual.cited_sections if actual else []

        rows.append(
            {
                "issue_number": issue_number,
                "found": actual is not None,
                "expected_category": expected["category"],
                "actual_category": actual_category,
                "expected_sections": ", ".join(expected["sections"]),
                "actual_sections": ", ".join(actual_sections),
                "category_match": actual_category == expected["category"],
                "sections_match": actual_sections == expected["sections"],
            }
        )

    count_match = len(parsed_issues) == len(GROUND_TRUTH)
    parse_accuracy = sum(row["sections_match"] for row in rows) / len(rows)
    classification_accuracy = sum(row["category_match"] for row in rows) / len(rows)
    passed = count_match and parse_accuracy == 1.0 and classification_accuracy == 1.0

    return {
        "parsed_issues": parsed_issues,
        "rows": rows,
        "count_match": count_match,
        "parse_accuracy": parse_accuracy,
        "classification_accuracy": classification_accuracy,
        "passed": passed,
    }


def _format_rows(rows: list[dict[str, object]]) -> str:
    if pd is not None:
        return pd.DataFrame(rows).to_string(index=False)

    headers = (
        "issue_number",
        "found",
        "expected_category",
        "actual_category",
        "expected_sections",
        "actual_sections",
        "category_match",
        "sections_match",
    )
    widths = {
        header: max(
            len(header),
            *(len(str(row[header])) for row in rows),
        )
        for header in headers
    }
    lines = [
        " ".join(header.ljust(widths[header]) for header in headers),
        " ".join("-" * widths[header] for header in headers),
    ]

    for row in rows:
        lines.append(
            " ".join(
                str(row[header]).ljust(widths[header]) for header in headers
            )
        )

    return "\n".join(lines)


def main() -> int:
    result = evaluate_fixture()

    print(f"Fixture: {SAMPLE_PATH}")
    print(_format_rows(result["rows"]))
    print(f"Count match: {result['count_match']}")
    print(f"Parse accuracy: {result['parse_accuracy']:.0%}")
    print(f"Classification accuracy: {result['classification_accuracy']:.0%}")

    status = "PASS" if result["passed"] else "FAIL"
    print(status)

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
