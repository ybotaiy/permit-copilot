from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_eval_harness():
    harness_path = Path(__file__).resolve().parents[1] / "eval" / "eval_harness.py"
    spec = importlib.util.spec_from_file_location("eval_harness", harness_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_issues_extracts_expected_fields():
    harness = load_eval_harness()
    sample_text = harness.SAMPLE_PATH.read_text()

    issues = harness.parse_issues(sample_text)

    assert [issue.issue_number for issue in issues] == [1, 2, 3, 4]
    assert issues[0].cited_sections == ["§1004.1.2"]
    assert issues[1].cited_sections == ["§1020.4"]
    assert issues[3].cited_sections == ["§1104.3", "§404.2.3"]
    assert (
        issues[0].summary
        == "Provide occupant load calculations for the second-floor assembly area"
    )


def test_classify_issue_matches_ground_truth():
    harness = load_eval_harness()
    issues = harness.parse_issues(harness.SAMPLE_PATH.read_text())

    actual = {
        issue.issue_number: harness.classify_issue(issue.text)
        for issue in issues
    }

    assert actual == {
        1: "egress",
        2: "egress",
        3: "fire_resistance",
        4: "accessibility",
    }


def test_evaluate_fixture_passes():
    harness = load_eval_harness()

    result = harness.evaluate_fixture()

    assert result["count_match"] is True
    assert result["parse_accuracy"] == 1.0
    assert result["classification_accuracy"] == 1.0
    assert result["passed"] is True
