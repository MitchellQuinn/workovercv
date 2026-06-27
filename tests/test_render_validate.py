from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import pytest

from workovercv.io import write_json, write_jsonl
from workovercv.manifest import write_review_scope
from workovercv.render import render_report, render_report_markdown
from workovercv.validation import validate_run


NEW_REPORT_HEADINGS = [
    "# Work Behaviour Profile Report",
    "## Scope and Evidence Base",
    "## How to Use This Report",
    "## Executive Work Profile",
    "## Observed Work Behaviour Signals",
    "## Engineering Habits",
    "## Problem-Solving Style",
    "## Work Rhythm and Development Cadence",
    "## Environment Fit",
    "## Role-Family Fit",
    "## Evidence Gaps and Follow-Up Questions",
    "## Confidence and Uncertainty Notes",
    "## Evidence Appendix",
]

SUMMARY_REPORT_HEADINGS = [
    "# Work Behaviour Profile Summary",
    "## Scope",
    "## Executive Work Profile",
    "## Top Observed Work Behaviour Signals",
    "## Problem-Solving Style",
    "## Environment Fit",
    "## Role-Family Discussion Routes",
    "## Evidence Gaps to Clarify",
    "## Confidence Notes",
]


def test_render_report_outputs_full_and_summary_reports_without_legacy_sections(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    report_path = render_report(tmp_path)

    markdown = report_path.read_text(encoding="utf-8")
    for earlier, later in zip(NEW_REPORT_HEADINGS, NEW_REPORT_HEADINGS[1:]):
        assert markdown.index(earlier) < markdown.index(later)
    for legacy in ("## Strengths", "## Weaknesses", "## Opportunities", "## Mitigations of Weaknesses"):
        assert legacy not in markdown
    assert "## Evidence Details" not in markdown
    assert "Use this report as a conversation guide" in markdown
    assert "## Evidence Appendix" in markdown
    assert "Analysis model information: Test fixture model information." in markdown

    summary_report = (tmp_path / "summary-report.md").read_text(encoding="utf-8")
    for earlier, later in zip(SUMMARY_REPORT_HEADINGS, SUMMARY_REPORT_HEADINGS[1:]):
        assert summary_report.index(earlier) < summary_report.index(later)
    assert "this is not a hiring decision record" in summary_report
    assert "- Analysis model information: Test fixture model information." in summary_report
    assert "Evidence \u2192 Implication \u2192 Confidence: Evidence:" not in summary_report
    assert "## Top Observed Work Behaviour Signals" in summary_report
    assert "Example evidence paths: `example-small/README.md`" in summary_report
    assert "pass/fail" not in summary_report
    assert "| Evidence ID | Repository | Path | Artifact type | Why it matters |" not in summary_report
    for legacy in ("Strengths", "Weaknesses", "Opportunities", "Mitigations of Weaknesses"):
        assert legacy not in summary_report

    screening_brief = (tmp_path / "screening_brief.md").read_text(encoding="utf-8")
    assert "# Repository Review Guide" in screening_brief
    assert "## Behaviour Signals To Discuss" in screening_brief
    assert "## Evidence Gaps To Verify" in screening_brief
    assert "red flag" not in screening_brief.lower()
    _assert_pdf_artifact(tmp_path / "report.pdf")
    _assert_pdf_artifact(tmp_path / "summary-report.pdf")
    _assert_pdf_artifact(tmp_path / "screening_brief.pdf")


def test_summary_report_uses_path_references_without_full_evidence_tables(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    report_path = render_report(tmp_path)

    markdown = report_path.read_text(encoding="utf-8")
    summary_report = (tmp_path / "summary-report.md").read_text(encoding="utf-8")

    assert "| Evidence ID | Repository | Path | Artifact type | Why it matters |" in markdown
    assert markdown.count("| Evidence ID | Repository | Path | Artifact type | Why it matters |") > 1
    assert "| ev1 | example-small | README.md | README | Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context. |" in markdown
    assert "Evidence references: ev1" in markdown
    assert "Example evidence paths: `example-small/README.md`" in summary_report
    assert "| Evidence ID | Repository | Path | Artifact type | Why it matters |" not in summary_report


def test_render_report_audit_mode_keeps_full_evidence_tables(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    report_path = render_report(tmp_path, mode="audit")

    markdown = report_path.read_text(encoding="utf-8")

    assert markdown.count("| Evidence ID | Repository | Path | Artifact type | Why it matters |") > 1
    assert "Evidence references: ev1" in markdown
    assert "## Evidence Appendix" in markdown


def test_summary_report_role_routes_use_shared_gap_note(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)

    summary_report = (tmp_path / "summary-report.md").read_text(encoding="utf-8")
    role_section = summary_report.split("## Role-Family Discussion Routes", 1)[1].split("## Evidence Gaps to Clarify", 1)[0]

    assert "Shared uncertainty context: Collaboration Visibility Gap." in role_section
    assert "Role-specific probe:" in role_section
    assert role_section.count("Ask for a code review walkthrough.") == 1
    assert role_section.count("Ask for an example of reviewed team work.") == 0


def test_summary_report_can_show_six_role_routes(tmp_path: Path) -> None:
    role_names = [
        "Software Engineer",
        "AI Engineer",
        "Applied ML Engineer",
        "Research Engineer",
        "AI Evaluation Engineer",
        "Developer Tools Engineer",
    ]
    role_family_fit = {
        "role_family_fit": [
            {
                "role_family": role_name,
                "why_discuss": f"{role_name} is worth discussing from bounded repository evidence.",
                "behaviour_fit": "The repository evidence supports reviewer-facing technical work.",
                "likely_contribution": "The person would likely anchor technical discussion in inspectable public artifacts.",
                "interview_probes": [f"Ask for a {role_name} work-sample walkthrough."],
                "confidence": "medium",
                "caveats": "Interpret with the recorded collaboration evidence gap.",
                "supporting_signal_ids": ["sig-docs"],
                "limiting_gap_ids": ["gap1"],
            }
            for role_name in role_names
        ]
    }
    _write_complete_run(tmp_path, role_family_fit=role_family_fit)
    render_report(tmp_path)

    summary_report = (tmp_path / "summary-report.md").read_text(encoding="utf-8")
    role_section = summary_report.split("## Role-Family Discussion Routes", 1)[1].split("## Evidence Gaps to Clarify", 1)[0]

    for role_name in role_names:
        assert f"### {role_name}" in role_section


def test_render_report_includes_candidate_url(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    report_path = render_report(tmp_path)

    markdown = report_path.read_text(encoding="utf-8")
    summary_report = (tmp_path / "summary-report.md").read_text(encoding="utf-8")

    assert "Candidate URL: https://github.com/example" in markdown
    assert "- Candidate URL: https://github.com/example" in summary_report


def test_validate_run_accepts_complete_run(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)

    result = validate_run(tmp_path)

    assert result.ok, result.errors
    manifest = json.loads((tmp_path / "run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "complete"
    assert "report.pdf" in manifest["artifacts"]
    render_entry = next(entry for entry in manifest["command_history"] if entry["command"] == "render")
    assert render_entry["config"]["pdf_outputs"] == ["report.pdf", "summary-report.pdf", "screening_brief.pdf"]


def test_validate_run_rejects_gap_without_follow_up_record(tmp_path: Path) -> None:
    _write_complete_run(tmp_path, mitigations=[])
    render_report(tmp_path)

    result = validate_run(tmp_path, update_manifest=False)

    assert any("has no follow-up record" in error for error in result.errors)


def test_validate_run_rejects_role_family_without_caveats(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_json(tmp_path / "role_family_fit.json", lambda data: data["role_family_fit"][0].pop("caveats"))

    result = validate_run(tmp_path, update_manifest=False)

    assert any("caveats" in error for error in result.errors)


def test_validate_run_rejects_empty_role_family_fit(tmp_path: Path) -> None:
    _write_complete_run(tmp_path, role_family_fit={"role_family_fit": []})
    render_report(tmp_path)

    result = validate_run(tmp_path, update_manifest=False)

    assert any("role_family_fit" in error and ("non-empty" in error or "at least one" in error) for error in result.errors)
    assert any("report.json" in error and ("non-empty" in error or "at least one" in error) for error in result.errors)


def test_validate_run_rejects_role_family_unknown_signal_reference(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_json(
        tmp_path / "role_family_fit.json",
        lambda data: data["role_family_fit"][0].update({"supporting_signal_ids": ["missing-sig"]}),
    )

    result = validate_run(tmp_path, update_manifest=False)

    assert any("Role-family fit Software Engineer references unknown signal_id missing-sig" in error for error in result.errors)


def test_validate_run_rejects_role_family_unknown_gap_reference(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_json(
        tmp_path / "role_family_fit.json",
        lambda data: data["role_family_fit"][0].update({"limiting_gap_ids": ["missing-gap"]}),
    )

    result = validate_run(tmp_path, update_manifest=False)

    assert any("Role-family fit Software Engineer references unknown gap_id missing-gap" in error for error in result.errors)


def test_validate_run_rejects_high_red_team_issue(tmp_path: Path) -> None:
    _write_complete_run(
        tmp_path,
        red_team={
            "pass": True,
            "issues": [
                {
                    "issue_id": "rt1",
                    "severity": "high",
                    "description": "Unsupported claim",
                    "required_change": "Remove it",
                }
            ],
        },
    )
    render_report(tmp_path)

    result = validate_run(tmp_path, update_manifest=False)

    assert any("High-severity" in error for error in result.errors)


def test_validate_run_rejects_disallowed_wording(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    _mutate_json(tmp_path / "report.json", lambda report: report.update({"executive_work_profile": "The candidate is unreliable."}))
    render_report(tmp_path)

    result = validate_run(tmp_path, update_manifest=False)

    assert any("Disallowed report phrase" in error for error in result.errors)


def test_validate_run_rejects_hiring_decision_language(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    _mutate_json(tmp_path / "report.json", lambda report: report.update({"executive_work_profile": "Recommended decision: hire for the role."}))
    render_report(tmp_path)

    result = validate_run(tmp_path, update_manifest=False)

    assert any("Hiring decision language" in error for error in result.errors)


def test_validate_run_rejects_disallowed_screening_brief_wording(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "screening_brief.md").write_text("This is a red flag.\n", encoding="utf-8")

    result = validate_run(tmp_path, update_manifest=False)

    assert any("screening_brief.md" in error and "Disallowed report phrase" in error for error in result.errors)


def test_validate_run_rejects_disallowed_summary_report_wording(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "summary-report.md").write_text("This is a red flag.\n", encoding="utf-8")

    result = validate_run(tmp_path, update_manifest=False)

    assert any("summary-report.md" in error and "Disallowed report phrase" in error for error in result.errors)


def test_validate_run_rejects_screening_brief_hiring_language(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "screening_brief.md").write_text("Recommended decision: hire for the role.\n", encoding="utf-8")

    result = validate_run(tmp_path, update_manifest=False)

    assert any("screening_brief.md" in error and "Hiring decision language" in error for error in result.errors)


def test_validate_run_rejects_summary_report_hiring_language(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "summary-report.md").write_text("Recommended decision: hire for the role.\n", encoding="utf-8")

    result = validate_run(tmp_path, update_manifest=False)

    assert any("summary-report.md" in error and "Hiring decision language" in error for error in result.errors)


def test_validate_run_rejects_disallowed_signal_wording(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_jsonl(
        tmp_path / "signal_ledger.jsonl",
        lambda records: records[0].update({"implication": "The candidate is unreliable."}),
    )

    result = validate_run(tmp_path, update_manifest=False)

    assert any("signal_ledger.jsonl" in error and "Disallowed report phrase" in error for error in result.errors)


def test_validate_run_rejects_protected_evidence_summary(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_jsonl(
        tmp_path / "evidence_map.jsonl",
        lambda records: records[0].update({"excerpt_or_summary": "This makes an inference about financial status."}),
    )

    result = validate_run(tmp_path, update_manifest=False)

    assert any("evidence_map.jsonl" in error and "Protected/private trait" in error for error in result.errors)


def test_validate_run_rejects_invalid_signal_category(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_jsonl(tmp_path / "signal_ledger.jsonl", lambda records: records[0].update({"category": "communication"}))

    result = validate_run(tmp_path, update_manifest=False)

    assert any("category" in error for error in result.errors)


def test_validate_run_rejects_legacy_signal_field(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_jsonl(tmp_path / "signal_ledger.jsonl", lambda records: records[0].update({"polarity": "positive"}))

    result = validate_run(tmp_path, update_manifest=False)

    assert any("signal_ledger.jsonl" in error and "Additional properties" in error for error in result.errors)


def test_validate_run_rejects_invalid_confidence(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_jsonl(tmp_path / "signal_ledger.jsonl", lambda records: records[0].update({"confidence": "certain"}))

    result = validate_run(tmp_path, update_manifest=False)

    assert any("confidence" in error for error in result.errors)


def test_validate_run_rejects_legacy_report_findings(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_json(
        tmp_path / "report.json",
        lambda report: report.update({"summary": "legacy", "findings": [{"section": "strengths"}]}),
    )

    result = validate_run(tmp_path, update_manifest=False)

    assert any("summary/findings" in error or "Additional properties" in error for error in result.errors)


def test_validate_run_rejects_legacy_markdown_heading(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "report.md").write_text("# Work Behaviour Profile Report\n\n## Strengths\n", encoding="utf-8")

    result = validate_run(tmp_path, update_manifest=False)

    assert any("legacy report heading" in error for error in result.errors)


def test_validate_run_rejects_legacy_summary_report_heading(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "summary-report.md").write_text("# Work Behaviour Profile Summary\n\n## Strengths\n", encoding="utf-8")

    result = validate_run(tmp_path, update_manifest=False)

    assert any("summary-report.md" in error and "legacy report heading" in error for error in result.errors)


def test_validate_run_rejects_unknown_report_heading(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "report.md").write_text("# Work Behaviour Profile Report\n\n## Evidence Details\n", encoding="utf-8")

    result = validate_run(tmp_path, update_manifest=False)

    assert any("unknown report heading" in error and "Evidence Details" in error for error in result.errors)


def test_validate_run_rejects_raw_chronology_leak(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    _mutate_json(
        tmp_path / "report.json",
        lambda report: report.update({"executive_work_profile": "Refactor parser edge case handling."}),
    )
    render_report(tmp_path)

    result = validate_run(tmp_path, update_manifest=False)

    assert any("raw commit subject" in error for error in result.errors)


def test_validate_run_rejects_missing_repo_reference(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_jsonl(tmp_path / "evidence_map.jsonl", lambda records: records[0].update({"repo_id": "missing-repo"}))

    result = validate_run(tmp_path, update_manifest=False)

    assert any("unknown repo_id missing-repo" in error for error in result.errors)


def test_validate_run_rejects_missing_artifact_reference(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_jsonl(tmp_path / "evidence_map.jsonl", lambda records: records[0].update({"artifact_id": "missing-artifact"}))

    result = validate_run(tmp_path, update_manifest=False)

    assert any("unknown artifact_id missing-artifact" in error for error in result.errors)


def test_validate_run_rejects_missing_file_path(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_jsonl(tmp_path / "evidence_map.jsonl", lambda records: records[0].update({"path": "missing.py"}))

    result = validate_run(tmp_path, update_manifest=False)

    assert any("unknown path missing.py" in error for error in result.errors)


def test_validate_run_rejects_missing_evidence_reference(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    _mutate_jsonl(tmp_path / "signal_ledger.jsonl", lambda records: records[0].update({"evidence_ids": ["missing-ev"]}))

    result = validate_run(tmp_path, update_manifest=False)

    assert any("unknown evidence_id missing-ev" in error for error in result.errors)


def test_validate_run_rejects_meta_category_as_observed_signal(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    _mutate_json(
        tmp_path / "report.json",
        lambda report: report["observed_work_behaviour_signals"][0].update({"category": "development_cadence"}),
    )
    render_report(tmp_path)

    result = validate_run(tmp_path, update_manifest=False)

    assert any("uses meta category development_cadence" in error for error in result.errors)


@pytest.mark.parametrize("artifact_name", ["review_scope.yml", "review_corpus.jsonl", "work_chronology.json"])
def test_validate_run_rejects_missing_boundary_artifact(tmp_path: Path, artifact_name: str) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / artifact_name).unlink()

    result = validate_run(tmp_path, update_manifest=False)

    assert f"Missing required artifact: {artifact_name}" in result.errors


def test_validate_run_rejects_malformed_review_scope(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "review_scope.yml").write_text("candidate: [\n", encoding="utf-8")

    result = validate_run(tmp_path, update_manifest=False)

    assert any("review_scope.yml" in error and "invalid YAML" in error for error in result.errors)


def test_validate_run_rejects_schema_invalid_review_scope(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    write_review_scope(
        tmp_path / "review_scope.yml",
        {
            "candidate": "not-a-mapping",
            "repositories": "not-a-list",
        },
    )

    result = validate_run(tmp_path, update_manifest=False)

    assert any("review_scope.yml" in error and "schema violation" in error for error in result.errors)


def test_validate_run_rejects_manifest_invalid_review_scope(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    write_review_scope(
        tmp_path / "review_scope.yml",
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "repositories": [
                {
                    "repo_id": "example-small",
                    "name": "small",
                    "url": "https://github.com/example/small",
                    "selected_for_review": True,
                }
            ],
        },
    )

    result = validate_run(tmp_path, update_manifest=False)

    assert any("review_scope.yml" in error and "requires clone_url or local_path" in error for error in result.errors)


def test_validate_run_rejects_missing_screening_brief(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "screening_brief.md").unlink()

    result = validate_run(tmp_path, update_manifest=False)

    assert "Missing required artifact: screening_brief.md" in result.errors


def test_validate_run_rejects_missing_summary_report(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "summary-report.md").unlink()

    result = validate_run(tmp_path, update_manifest=False)

    assert "Missing required artifact: summary-report.md" in result.errors


@pytest.mark.parametrize("artifact_name", ["report.pdf", "summary-report.pdf", "screening_brief.pdf"])
def test_validate_run_rejects_missing_pdf_artifact(tmp_path: Path, artifact_name: str) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / artifact_name).unlink()

    result = validate_run(tmp_path, update_manifest=False)

    assert f"Missing required artifact: {artifact_name}" in result.errors


def test_validate_run_rejects_invalid_pdf_artifact(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    render_report(tmp_path)
    (tmp_path / "report.pdf").write_bytes(b"not a pdf")

    result = validate_run(tmp_path, update_manifest=False)

    assert "report.pdf: PDF artifact does not start with %PDF-" in result.errors


def test_renderer_refuses_legacy_report_shape(tmp_path: Path) -> None:
    _write_complete_run(tmp_path)
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    report["findings"] = []

    with pytest.raises(ValueError, match="legacy"):
        render_report_markdown(report)


def _write_complete_run(
    run_dir: Path,
    *,
    mitigations: list[dict[str, Any]] | None = None,
    role_family_fit: dict[str, Any] | None = None,
    red_team: dict[str, Any] | None = None,
) -> None:
    write_json(
        run_dir / "repo_inventory.json",
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "generated_at": "2026-06-17T00:00:00Z",
            "repositories": [
                {
                    "repo_id": "example-small",
                    "name": "small",
                    "url": "https://github.com/example/small",
                    "visibility": "public",
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                }
            ],
        },
    )
    write_review_scope(
        run_dir / "review_scope.yml",
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "generated_at": "2026-06-17T00:00:00Z",
            "source_inventory": "repo_inventory.json",
            "repositories": [
                {
                    "repo_id": "example-small",
                    "name": "small",
                    "url": "https://github.com/example/small",
                    "local_path": str(run_dir),
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                }
            ],
        },
    )
    write_json(
        run_dir / "artifact_inventory.json",
        {
            "generated_at": "2026-06-17T00:00:00Z",
            "artifacts": [
                {
                    "artifact_id": "art1",
                    "repo_id": "example-small",
                    "path": "README.md",
                    "artifact_type": "README",
                    "size_estimate": "small",
                    "likely_signal_value": "high",
                },
                {
                    "artifact_id": "art-chronology",
                    "repo_id": "example-small",
                    "path": "work_chronology.json",
                    "artifact_type": "work_chronology",
                    "size_estimate": "small",
                    "likely_signal_value": "medium",
                },
            ],
        },
    )
    write_json(
        run_dir / "work_chronology.json",
        {
            "generated_at": "2026-06-17T00:00:00Z",
            "max_commits_per_repository": 50,
            "repositories": [
                {
                    "repo_id": "example-small",
                    "available": True,
                    "default_branch": "main",
                    "commit_count": 1,
                    "first_commit_at": "2026-06-01T00:00:00Z",
                    "last_commit_at": "2026-06-01T00:00:00Z",
                    "entries": [
                        {
                            "commit_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "committed_at": "2026-06-01T00:00:00Z",
                            "subject": "Refactor parser edge case handling",
                        }
                    ],
                }
            ],
        },
    )
    write_jsonl(
        run_dir / "explicit_claims.jsonl",
        [
            {
                "claim_id": "claim1",
                "repo_id": "example-small",
                "artifact_id": "art1",
                "claim_text": "The project has a reviewer-facing example.",
                "claim_type": "process",
                "scope": "narrow",
                "risk_of_overclaim": "low",
                "evidence_ids": ["ev1"],
            }
        ],
    )
    write_jsonl(
        run_dir / "signal_ledger.jsonl",
        [
            {
                "signal_id": "sig-docs",
                "category": "documentation_and_handoff",
                "label": "Makes technical work inspectable for reviewers",
                "evidence_ids": ["ev1"],
                "evidence_summary": "README describes purpose and review context.",
                "implication": "This suggests a working style that values external legibility.",
                "confidence": "medium",
                "confidence_reason": "Evidence is direct but narrow.",
                "caveats": "Public documentation does not prove workplace handoff behavior.",
            },
            {
                "signal_id": "sig-cadence",
                "category": "development_cadence",
                "label": "Public cadence is bounded by available chronology",
                "evidence_ids": ["ev2"],
                "evidence_summary": "Bounded chronology contains one readable public commit record.",
                "implication": "Work rhythm should be treated as lightly evidenced.",
                "confidence": "low",
                "confidence_reason": "Chronology is shallow.",
                "caveats": "Do not equate commit count or velocity with competence.",
            },
        ],
    )
    write_jsonl(
        run_dir / "evidence_map.jsonl",
        [
            {
                "evidence_id": "ev1",
                "repo_id": "example-small",
                "artifact_id": "art1",
                "path": "README.md",
                "locator": {"type": "line_range", "value": "1-5"},
                "evidence_type": "direct",
                "excerpt_or_summary": "README describes a reviewer-facing example and limitation.",
                "supports": ["claim1", "sig-docs"],
                "evidence_strength": "moderate",
                "notes": "",
            },
            {
                "evidence_id": "ev2",
                "repo_id": "example-small",
                "artifact_id": "art-chronology",
                "path": "work_chronology.json",
                "locator": {"type": "inventory", "value": "work_chronology.json"},
                "evidence_type": "indirect",
                "excerpt_or_summary": "Chronology summary is available for analysis without exposing raw commit data.",
                "supports": ["sig-cadence"],
                "evidence_strength": "weak",
                "notes": "chronology_kind=bounded_git_history",
            },
        ],
    )
    write_jsonl(
        run_dir / "gap_register.jsonl",
        [
            {
                "gap_id": "gap1",
                "repo_id": "example-small",
                "category": "collaboration_visibility_gap",
                "description": "No pull request review evidence was present in the collected corpus.",
                "impact_on_report": "bounds_interpretation",
                "related_signal_ids": ["sig-docs"],
                "suggested_follow_up": "Ask for an example of reviewed team work.",
            }
        ],
    )
    write_jsonl(
        run_dir / "mitigations.jsonl",
        mitigations
        if mitigations is not None
        else [
            {
                "mitigation_id": "mit1",
                "related_gap_id": "gap1",
                "related_signal_ids": ["sig-docs"],
                "mitigation_type": "interview_probe",
                "recommendation": "Ask for a code review walkthrough.",
                "rationale": "This probes collaboration evidence that the repositories cannot show.",
            }
        ],
    )
    role_data = role_family_fit if role_family_fit is not None else _role_family_fixture()
    write_json(run_dir / "role_family_fit.json", role_data)
    write_jsonl(
        run_dir / "review_corpus.jsonl",
        [
            {
                "chunk_id": "chunk1",
                "repo_id": "example-small",
                "artifact_id": "art1",
                "path": "README.md",
                "artifact_type": "README",
                "locator": {"type": "line_range", "value": "1-5"},
                "line_start": 1,
                "line_end": 5,
                "sha256": "fixture",
                "text": "README describes a reviewer-facing example and limitation.",
            }
        ],
    )
    write_json(run_dir / "red_team_review.json", red_team if red_team is not None else {"pass": True, "issues": []})
    write_json(run_dir / "report.json", _report_fixture(role_data["role_family_fit"]))


def _role_family_fixture() -> dict[str, Any]:
    return {
        "role_family_fit": [
            {
                "role_family": "Software Engineer",
                "why_discuss": "Evidence supports a bounded software engineering discussion.",
                "behaviour_fit": "The repository evidence supports reviewer-facing documentation.",
                "likely_contribution": "The person would likely contribute inspectable implementation work with clear review context.",
                "interview_probes": ["Ask for a code review walkthrough."],
                "confidence": "medium",
                "caveats": "Interpret with the recorded collaboration evidence gap.",
                "supporting_signal_ids": ["sig-docs"],
                "limiting_gap_ids": ["gap1"],
            }
        ]
    }


def _report_fixture(role_family_entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "title": "Work Behaviour Profile Report",
        "analysis_model_information": "Test fixture model information.",
        "scope_and_evidence_base": {
            "candidate_url": "https://github.com/example",
            "repository_count": 1,
            "artifact_count": 2,
            "repository_names": ["small"],
            "evidence_note": "Public repository evidence is incomplete.",
            "non_decision_note": "This is not a hiring decision record.",
            "private_work_note": "Private/company work may not be visible.",
        },
        "executive_work_profile": "The observable pattern is reviewer-facing documentation with bounded cadence evidence.",
        "observed_work_behaviour_signals": [
            {
                "signal_id": "sig-docs",
                "category": "documentation_and_handoff",
                "label": "Makes technical work inspectable for reviewers",
                "evidence_summary": "README describes purpose and review context.",
                "implication": "This suggests a working style that values external legibility.",
                "confidence": "medium",
                "caveats": "Public documentation does not prove workplace handoff behavior.",
                "evidence_ids": ["ev1"],
            },
        ],
        "engineering_habits": [
            {
                "habit_id": "externalising_context_and_boundaries",
                "label": "Externalising context and boundaries",
                "description": "README evidence makes project purpose and review context available.",
                "supporting_signal_ids": ["sig-docs"],
                "evidence_ids": ["ev1"],
                "confidence": "medium",
                "caveats": "Public documentation does not prove workplace handoff behavior.",
            }
        ],
        "problem_solving_style": {
            "summary": "The reviewed work suggests a problem-solving style that makes a narrow repository example inspectable.",
            "supporting_signal_ids": ["sig-docs"],
            "evidence_ids": ["ev1"],
            "confidence": "medium",
            "caveats": "Static repositories do not show live decision-making.",
        },
        "work_rhythm_and_development_cadence": {
            "summary": "Commit-history evidence and artifact-chronology evidence are interpreted separately.",
            "commit_history_signal": {
                "description": "Bounded chronology contains one readable public commit record and may represent a curated snapshot.",
                "evidence_ids": ["ev2"],
                "confidence": "low",
                "caveats": "Do not equate shallow public history, commit count, or velocity with competence or productivity.",
            },
            "artifact_chronology_signal": {
                "description": "No dated or staged artifact chronology was detected in the fixture.",
                "evidence_ids": ["ev2"],
                "confidence": "low",
                "caveats": "Absence of staged public artifacts is an evidence limit.",
            },
            "public_history_limitations": "Public repositories may be curated snapshots and commit velocity is not treated as competence.",
            "confidence": "low",
            "caveats": "Raw commit data is not rendered.",
        },
        "environment_fit": {
            "may_fit_well": ["Teams that value inspectable documentation."],
            "may_require_care": ["Collaboration evidence should be discussed directly."],
        },
        "role_family_fit": role_family_entries,
        "evidence_gaps_and_follow_up_questions": [
            {
                "gap_id": "gap1",
                "label": "Collaboration Visibility Gap",
                "what_was_observed": "No pull request review evidence was present in the collected corpus.",
                "why_uncertain": "Public repository evidence does not show every work context.",
                "suggested_follow_up": "Ask for an example of reviewed team work.",
                "confidence": "medium",
                "scope": "collected public repository evidence",
            }
        ],
        "confidence_and_uncertainty_notes": {
            "evidence_density": "Fixture evidence is narrow.",
            "cross_repository_consistency": "Single repository fixture.",
            "authorship_bounds": "Authorship is bounded to public evidence.",
            "public_repository_limitations": "Public repository evidence is incomplete.",
            "private_work_limitations": "Private/company work may not be visible.",
            "confidence_summary": "Mixed confidence fixture.",
        },
    }


def _mutate_json(path: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def _mutate_jsonl(path: Path, mutate: Callable[[list[dict[str, Any]]], None]) -> None:
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    mutate(records)
    path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")


def _assert_pdf_artifact(path: Path) -> None:
    assert path.exists()
    assert path.stat().st_size > 0
    assert path.read_bytes().startswith(b"%PDF-")
