from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from .constants import (
    PDF_ARTIFACTS,
    REPORT_PDF_ARTIFACT,
    SCREENING_BRIEF_ARTIFACT,
    SCREENING_BRIEF_PDF_ARTIFACT,
    SUMMARY_REPORT_ARTIFACT,
    SUMMARY_REPORT_PDF_ARTIFACT,
)
from .io import read_json, read_jsonl
from .pdf import write_pdf_from_markdown
from .run_manifest import update_run_manifest

ReportMode = Literal["summary", "audit"]


@dataclass(frozen=True)
class _RenderContext:
    evidence: list[dict[str, Any]]
    artifacts: list[dict[str, Any]]

    @property
    def evidence_by_id(self) -> dict[str, dict[str, Any]]:
        return {item.get("evidence_id"): item for item in self.evidence if isinstance(item.get("evidence_id"), str)}

    @property
    def artifact_type_by_id(self) -> dict[str, str]:
        return {
            item.get("artifact_id"): item.get("artifact_type")
            for item in self.artifacts
            if isinstance(item.get("artifact_id"), str) and isinstance(item.get("artifact_type"), str)
        }


def render_report(run_dir: Path, *, mode: ReportMode = "audit") -> Path:
    run_dir = run_dir.resolve()
    if mode not in {"summary", "audit"}:
        raise ValueError("report mode must be 'summary' or 'audit'")
    report_json_path = run_dir / "report.json"
    if not report_json_path.exists():
        raise FileNotFoundError(f"Missing report.json in {run_dir}")
    report = read_json(report_json_path)
    evidence = _read_jsonl_if_exists(run_dir / "evidence_map.jsonl")
    artifact_inventory = _read_json_if_exists(run_dir / "artifact_inventory.json", {"artifacts": []})
    artifacts = artifact_inventory.get("artifacts", []) if isinstance(artifact_inventory, dict) else []
    markdown = render_report_markdown(report, evidence=evidence, artifacts=artifacts, mode=mode)
    summary_report_markdown = render_summary_report_markdown(report, evidence=evidence, artifacts=artifacts)
    role_family_fit = _read_json_if_exists(run_dir / "role_family_fit.json", {"role_family_fit": []})
    signals = _read_jsonl_if_exists(run_dir / "signal_ledger.jsonl")
    gaps = _read_jsonl_if_exists(run_dir / "gap_register.jsonl")
    mitigations = _read_jsonl_if_exists(run_dir / "mitigations.jsonl")
    screening_brief_markdown = render_screening_brief_markdown(
        report,
        role_family_fit=role_family_fit,
        signals=signals,
        evidence=evidence,
        gaps=gaps,
        mitigations=mitigations,
    )
    report_path = run_dir / "report.md"
    report_path.write_text(markdown, encoding="utf-8", newline="\n")
    summary_report_path = run_dir / SUMMARY_REPORT_ARTIFACT
    summary_report_path.write_text(summary_report_markdown, encoding="utf-8", newline="\n")
    screening_brief_path = run_dir / SCREENING_BRIEF_ARTIFACT
    screening_brief_path.write_text(screening_brief_markdown, encoding="utf-8", newline="\n")
    write_pdf_from_markdown(
        markdown,
        run_dir / REPORT_PDF_ARTIFACT,
        title="Work Behaviour Profile Report",
    )
    write_pdf_from_markdown(
        summary_report_markdown,
        run_dir / SUMMARY_REPORT_PDF_ARTIFACT,
        title="Work Behaviour Profile Summary",
    )
    write_pdf_from_markdown(
        screening_brief_markdown,
        run_dir / SCREENING_BRIEF_PDF_ARTIFACT,
        title="Repository Review Guide",
    )
    update_run_manifest(
        run_dir,
        command="render",
        config={
            "run": str(run_dir),
            "report_mode": mode,
            "summary_report": SUMMARY_REPORT_ARTIFACT,
            "pdf_outputs": PDF_ARTIFACTS,
        },
        status="partial",
    )
    return report_path


def render_report_markdown(
    report: dict[str, Any],
    *,
    evidence: list[dict[str, Any]] | None = None,
    artifacts: list[dict[str, Any]] | None = None,
    mode: ReportMode = "summary",
) -> str:
    if mode not in {"summary", "audit"}:
        raise ValueError("report mode must be 'summary' or 'audit'")
    title = _validated_report_title(report)

    context = _RenderContext(evidence or [], artifacts or [])
    if mode == "audit":
        return _render_audit_report_markdown(report, context, title)
    return _render_compact_report_markdown(report, context, title)


def render_full_report_markdown(
    report: dict[str, Any],
    *,
    evidence: list[dict[str, Any]] | None = None,
    artifacts: list[dict[str, Any]] | None = None,
) -> str:
    title = _validated_report_title(report)
    context = _RenderContext(evidence or [], artifacts or [])
    return _render_audit_report_markdown(report, context, title)


def render_summary_report_markdown(
    report: dict[str, Any],
    *,
    evidence: list[dict[str, Any]] | None = None,
    artifacts: list[dict[str, Any]] | None = None,
) -> str:
    _validated_report_title(report)
    context = _RenderContext(evidence or [], artifacts or [])
    lines: list[str] = ["# Work Behaviour Profile Summary", ""]
    _render_summary_scope(lines, report.get("scope_and_evidence_base"), report.get("analysis_model_information"))
    _render_summary_executive_profile(lines, report, context)
    _render_summary_top_signals(lines, report.get("observed_work_behaviour_signals"), context)
    _render_summary_problem_solving_style(lines, report.get("problem_solving_style"))
    _render_summary_environment_fit(lines, report.get("environment_fit"), report.get("evidence_gaps_and_follow_up_questions"))
    _render_summary_role_family_routes(lines, report.get("role_family_fit"), report.get("evidence_gaps_and_follow_up_questions"))
    _render_summary_evidence_gaps(lines, report.get("evidence_gaps_and_follow_up_questions"))
    _render_summary_confidence_notes(lines, report)
    return "\n".join(lines).rstrip() + "\n"


def _validated_report_title(report: dict[str, Any]) -> str:
    if "findings" in report or "summary" in report:
        raise ValueError("v0.6 report.json must not contain legacy summary/findings fields")
    title = str(report.get("title") or "Work Behaviour Profile Report")
    if title != "Work Behaviour Profile Report":
        raise ValueError("report.json title must be Work Behaviour Profile Report")
    return title


def _render_compact_report_markdown(report: dict[str, Any], context: _RenderContext, title: str) -> str:
    lines: list[str] = [f"# {title}", ""]
    _render_scope(lines, report.get("scope_and_evidence_base"), report.get("analysis_model_information"))
    _render_how_to_use(lines)
    _render_text_section(lines, "Executive Work Profile", report.get("executive_work_profile"))
    _render_observed_signals_summary(lines, report.get("observed_work_behaviour_signals"), context)
    _render_engineering_habits_summary(lines, report.get("engineering_habits"), context)
    _render_problem_solving_style_summary(lines, report.get("problem_solving_style"), context)
    _render_cadence_summary(lines, report.get("work_rhythm_and_development_cadence"), context)
    _render_environment_fit(lines, report.get("environment_fit"))
    _render_role_family_fit_summary(lines, report.get("role_family_fit"), report.get("evidence_gaps_and_follow_up_questions"))
    _render_evidence_gaps(lines, report.get("evidence_gaps_and_follow_up_questions"))
    _render_mapping_section(lines, "Confidence and Uncertainty Notes", report.get("confidence_and_uncertainty_notes"))
    _render_evidence_appendix(lines, context, _report_evidence_ids(report), limit=40)
    return "\n".join(lines).rstrip() + "\n"


def _render_audit_report_markdown(report: dict[str, Any], context: _RenderContext, title: str) -> str:
    lines: list[str] = [f"# {title}", ""]
    _render_scope(lines, report.get("scope_and_evidence_base"), report.get("analysis_model_information"))
    _render_how_to_use(lines)
    _render_text_section(lines, "Executive Work Profile", report.get("executive_work_profile"))
    _render_observed_signals(lines, report.get("observed_work_behaviour_signals"), context)
    _render_engineering_habits(lines, report.get("engineering_habits"), context)
    _render_problem_solving_style(lines, report.get("problem_solving_style"), context)
    _render_cadence(lines, report.get("work_rhythm_and_development_cadence"), context)
    _render_environment_fit(lines, report.get("environment_fit"))
    _render_role_family_fit(lines, report.get("role_family_fit"))
    _render_evidence_gaps(lines, report.get("evidence_gaps_and_follow_up_questions"))
    _render_mapping_section(lines, "Confidence and Uncertainty Notes", report.get("confidence_and_uncertainty_notes"))
    _render_evidence_appendix(lines, context, _report_evidence_ids(report), limit=None)
    return "\n".join(lines).rstrip() + "\n"


def _render_summary_scope(lines: list[str], scope: Any, analysis_model_information: Any) -> None:
    lines.extend(["## Scope", ""])
    if not isinstance(scope, dict):
        lines.extend(
            [
                "- Candidate URL: not recorded",
                "- Repositories reviewed: not recorded",
                "- Artifacts reviewed: not recorded",
                f"- Analysis model information: {_analysis_model_information(analysis_model_information)}",
                "- Limitation note: Public GitHub evidence is incomplete; this is not a hiring decision record; private/company work may not be visible.",
                "",
            ]
        )
        return

    repo_names = scope.get("repository_names", [])
    repo_text = ""
    if isinstance(repo_names, list) and repo_names:
        repo_text = " (" + ", ".join(str(name) for name in repo_names[:6]) + ")"
    lines.append(f"- Candidate URL: {_brief_text(scope.get('candidate_url')) or 'not recorded'}")
    lines.append(f"- Repositories reviewed: {scope.get('repository_count', 'not recorded')}{repo_text}")
    lines.append(f"- Artifacts reviewed: {scope.get('artifact_count', 'not recorded')}")
    lines.append(f"- Analysis model information: {_analysis_model_information(analysis_model_information)}")
    lines.append(
        "- Limitation note: Public GitHub evidence is incomplete; this is not a hiring decision record; private/company work may not be visible."
    )
    lines.append("")


def _render_summary_executive_profile(lines: list[str], report: dict[str, Any], context: _RenderContext) -> None:
    lines.extend(["## Executive Work Profile", ""])
    signals = _top_summary_signals(report.get("observed_work_behaviour_signals"), limit=3)
    executive = _brief_text(report.get("executive_work_profile")) or "The reviewed public work did not include an executive synthesis."

    lines.append(executive)
    lines.append("")

    refs = _summary_profile_refs(signals, context)
    second_parts = []
    if refs:
        second_parts.append("Representative evidence paths include " + ", ".join(f"`{ref}`" for ref in refs) + ".")
    second_parts.append("Use the evidence gaps below to clarify what the public corpus cannot show.")
    lines.append(" ".join(second_parts))
    lines.append("")


def _render_summary_top_signals(lines: list[str], signals: Any, context: _RenderContext, *, limit: int = 6) -> None:
    lines.extend(["## Top Observed Work Behaviour Signals", ""])
    top_signals = _top_summary_signals(signals, limit=limit)
    if not top_signals:
        lines.append("No behaviour signals were recorded.")
        lines.append("")
        return

    for signal in top_signals:
        label = _brief_text(signal.get("label")) or "Behaviour signal"
        lines.extend([f"### {label}", ""])
        lines.append(f"- Evidence: {_brief_text(signal.get('evidence_summary')) or 'not recorded'}")
        lines.append(f"- Implication: {_brief_text(signal.get('implication')) or 'not recorded'}")
        lines.append(f"- Confidence: {_brief_text(signal.get('confidence')) or 'not_recorded'}")
        refs = _evidence_path_refs(signal.get("evidence_ids", []) or [], context, limit=2)
        if refs:
            lines.append("- Example evidence paths: " + "; ".join(f"`{ref}`" for ref in refs))
        else:
            lines.append("- Example evidence paths: not recorded")
        lines.append("")


def _render_summary_problem_solving_style(lines: list[str], style: Any) -> None:
    lines.extend(["## Problem-Solving Style", ""])
    if not isinstance(style, dict) or not style:
        lines.append("Not recorded.")
        lines.append("")
        return
    summary = _brief_text(style.get("summary")) or "No problem-solving synthesis recorded."
    confidence = _brief_text(style.get("confidence"))
    caveats = _brief_text(style.get("caveats"))
    parts = [summary]
    if confidence:
        parts.append(f"Confidence: {confidence}.")
    if caveats:
        parts.append(f"Caveats: {caveats}")
    lines.append(" ".join(parts))
    lines.append("")


def _render_summary_environment_fit(lines: list[str], fit: Any, gaps: Any) -> None:
    lines.extend(["## Environment Fit", ""])
    may_fit = fit.get("may_fit_well", []) if isinstance(fit, dict) else []
    follow_up = fit.get("may_require_care", []) if isinstance(fit, dict) else []
    if not isinstance(follow_up, list):
        follow_up = []
    if not follow_up and isinstance(gaps, list):
        follow_up = [
            _brief_text(gap.get("label") or gap.get("description"))
            for gap in gaps
            if isinstance(gap, dict) and _brief_text(gap.get("label") or gap.get("description"))
        ]

    lines.append("May fit well:")
    _render_summary_bullets(lines, may_fit, fallback="Not recorded.", limit=3)
    lines.append("")
    lines.append("May require follow-up:")
    _render_summary_bullets(lines, follow_up, fallback="Not recorded.", limit=3)
    lines.append("")


def _render_summary_role_family_routes(lines: list[str], entries: Any, gaps: Any, *, limit: int = 6) -> None:
    lines.extend(["## Role-Family Discussion Routes", ""])
    lines.append(
        "These are role-family conversation routes, not hiring recommendations. Read them with the shared evidence gaps below, especially where public repositories do not show team review, private/company work, or full ownership context."
    )
    lines.append("")
    if not isinstance(entries, list) or not entries:
        lines.append("No role-family entries were recorded.")
        lines.append("")
        return

    gap_labels = []
    if isinstance(gaps, list):
        gap_labels = [
            _brief_text(gap.get("label"))
            for gap in gaps
            if isinstance(gap, dict) and _brief_text(gap.get("label"))
        ][:4]
    if gap_labels:
        lines.append("Shared uncertainty context: " + _list_text(gap_labels) + ".")
        lines.append("")

    for entry in [item for item in entries if isinstance(item, dict)][:limit]:
        role = _brief_text(entry.get("role_family")) or "Role family"
        lines.extend([f"### {role}", ""])
        lines.append(f"- Why it is worth discussing: {_brief_text(entry.get('why_discuss')) or 'not recorded'}")
        lines.append(f"- Likely contribution: {_brief_text(entry.get('likely_contribution')) or 'not recorded'}")
        probe = _summary_role_probes(entry.get("interview_probes", []), limit=1)
        lines.append(f"- Role-specific probe: {probe[0] if probe else 'Ask for a walkthrough of one representative artifact.'}")
        lines.append("")


def _render_summary_evidence_gaps(lines: list[str], gaps: Any) -> None:
    lines.extend(["## Evidence Gaps to Clarify", ""])
    if not isinstance(gaps, list) or not gaps:
        lines.append("No evidence gaps were recorded.")
        lines.append("")
        return
    for gap in [item for item in gaps if isinstance(item, dict)]:
        label = _brief_text(gap.get("label")) or "Evidence gap"
        lines.extend([f"### {label}", ""])
        lines.append(f"- Why uncertain: {_brief_text(gap.get('why_uncertain')) or _brief_text(gap.get('description')) or 'not recorded'}")
        lines.append(f"- Follow-up question: {_brief_text(gap.get('suggested_follow_up')) or 'not recorded'}")
        lines.append("")


def _render_summary_confidence_notes(lines: list[str], report: dict[str, Any]) -> None:
    lines.extend(["## Confidence Notes", ""])
    notes = report.get("confidence_and_uncertainty_notes")
    notes = notes if isinstance(notes, dict) else {}
    signals = _top_summary_signals(report.get("observed_work_behaviour_signals"), limit=6)
    stronger = [
        _brief_text(signal.get("label"))
        for signal in signals
        if _brief_text(signal.get("confidence")).lower() in {"high", "medium"} and _brief_text(signal.get("label"))
    ]
    weaker = [
        _brief_text(signal.get("label"))
        for signal in signals
        if _brief_text(signal.get("confidence")).lower() == "low" and _brief_text(signal.get("label"))
    ]
    strongest_text = _list_text(stronger[:3]) if stronger else _brief_text(notes.get("evidence_density"))
    weaker_text = _list_text(weaker[:3]) if weaker else _brief_text(notes.get("cross_repository_consistency"))
    lines.append(f"- Strongest confidence areas: {strongest_text or 'Direct repository/path-backed signals are the clearest basis for discussion.'}")
    lines.append(f"- Weaker confidence areas: {weaker_text or 'Cross-context behaviour remains less visible in public repository evidence.'}")
    lines.append(f"- Public evidence limitations: {_brief_text(notes.get('public_repository_limitations')) or 'Public GitHub evidence is incomplete.'}")
    lines.append(f"- Private/company work limitations: {_brief_text(notes.get('private_work_limitations')) or 'Private/company work may not be visible.'}")
    lines.append("")


def render_screening_brief_markdown(
    report: dict[str, Any],
    *,
    role_family_fit: dict[str, Any] | None = None,
    signals: list[dict[str, Any]] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    gaps: list[dict[str, Any]] | None = None,
    mitigations: list[dict[str, Any]] | None = None,
) -> str:
    role_family_fit = role_family_fit or {"role_family_fit": []}
    signals = signals or []
    evidence = evidence or []
    gaps = gaps or []
    mitigations = mitigations or []
    evidence_by_id = {item.get("evidence_id"): item for item in evidence if isinstance(item.get("evidence_id"), str)}

    lines = [
        "# Repository Review Guide",
        "",
        "This guide translates validated repository evidence into behaviour-based discussion prompts. It is not a decision record, ranking, background check, or pass/fail assessment.",
        "Use missing or limited public evidence as a prompt for follow-up, not as proof of inability.",
        "",
        "## Behaviour Signals To Discuss",
        "",
    ]
    reportable_signals = _reportable_signals(signals)
    if reportable_signals:
        for signal in reportable_signals[:8]:
            label = _brief_text(signal.get("label")) or "Untitled behaviour signal"
            implication = _brief_text(signal.get("implication")) or "Implication was not recorded."
            confidence = _brief_text(signal.get("confidence")) or "not_recorded"
            refs = _evidence_reference_summary(signal.get("evidence_ids", []) or [], evidence_by_id)
            suffix = f" Evidence: {refs}." if refs else ""
            lines.append(f"- {label}: {implication} Confidence: {confidence}.{suffix}")
    else:
        lines.append("- No behaviour signals were recorded.")

    lines.extend(["", "## Role-Family Discussion Routes", ""])
    entries = role_family_fit.get("role_family_fit", [])
    if isinstance(entries, list) and entries:
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            role = _brief_text(entry.get("role_family")) or "Role family"
            confidence = _brief_text(entry.get("confidence")) or "not_recorded"
            why = _brief_text(entry.get("why_discuss")) or "No rationale recorded."
            contribution = _brief_text(entry.get("likely_contribution"))
            caveats = _brief_text(entry.get("caveats")) or "No caveats recorded."
            contribution_text = f" Likely contribution: {contribution}." if contribution else ""
            lines.append(f"- {role}: {why}{contribution_text} Confidence: {confidence}. Caveats: {caveats}")
    else:
        lines.append("- No role-family entries were recorded.")

    lines.extend(["", "## Evidence Gaps To Verify", ""])
    if gaps:
        for gap in gaps[:8]:
            description = _brief_text(gap.get("description")) or "Evidence gap was not described."
            follow_up = _brief_text(gap.get("suggested_follow_up"))
            lines.append(f"- {description} Follow-up: {follow_up}" if follow_up else f"- {description}")
    else:
        lines.append("- No evidence gaps were recorded.")

    prompts = _dedupe_brief_items(
        [
            *[str(gap.get("suggested_follow_up")) for gap in gaps if isinstance(gap, dict) and gap.get("suggested_follow_up")],
            *[
                str(mitigation.get("recommendation"))
                for mitigation in mitigations
                if isinstance(mitigation, dict) and mitigation.get("recommendation")
            ],
        ]
    )
    lines.extend(["", "## Follow-Up Prompts", ""])
    if prompts:
        for prompt in prompts[:8]:
            lines.append(f"- {prompt}")
    else:
        lines.append("- Ask the person to walk through one representative artifact and explain the tradeoffs behind it.")

    lines.extend(
        [
            "",
            "## Use Boundaries",
            "",
            "- Treat repository artifacts as bounded public evidence.",
            "- Treat absence or limited visibility as a reason to ask a narrower question.",
            "- Keep this guide attached to the validated run artifacts so every prompt can be traced back to evidence.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _render_scope(lines: list[str], scope: Any, analysis_model_information: Any) -> None:
    lines.extend(["## Scope and Evidence Base", ""])
    if not isinstance(scope, dict):
        lines.append("Scope was not recorded.")
        lines.append(f"Analysis model information: {_analysis_model_information(analysis_model_information)}")
        lines.append("")
        return
    repo_names = scope.get("repository_names", [])
    if not isinstance(repo_names, list):
        repo_names = []
    candidate_url = _brief_text(scope.get("candidate_url"))
    if candidate_url:
        lines.append(f"Candidate URL: {candidate_url}")
    lines.append(f"Repositories reviewed: {scope.get('repository_count', 0)}")
    lines.append(f"Artifacts reviewed: {scope.get('artifact_count', 0)}")
    lines.append("Repository names: " + (", ".join(str(name) for name in repo_names) if repo_names else "not recorded"))
    for key in ("evidence_note", "non_decision_note", "private_work_note"):
        value = _brief_text(scope.get(key))
        if value:
            lines.append(value)
    lines.append(f"Analysis model information: {_analysis_model_information(analysis_model_information)}")
    lines.append("")


def _render_text_section(lines: list[str], heading: str, value: Any) -> None:
    lines.extend([f"## {heading}", "", _brief_text(value) or "Not recorded.", ""])


def _render_how_to_use(lines: list[str]) -> None:
    lines.extend(
        [
            "## How to Use This Report",
            "",
            "Use this report as a conversation guide, not a hiring decision record. The strongest use is to identify what to ask about: which artifacts to inspect, which working behaviours appear repeatedly, and which evidence gaps should be clarified through discussion.",
            "",
        ]
    )


def _render_observed_signals_summary(lines: list[str], signals: Any, context: _RenderContext, *, limit: int = 8) -> None:
    lines.extend(["## Observed Work Behaviour Signals", ""])
    if not isinstance(signals, list) or not signals:
        lines.append("No behaviour signals recorded.")
        lines.append("")
        return
    for index, signal in enumerate([item for item in signals if isinstance(item, dict)][:limit], start=1):
        lines.extend([f"### {index}. {_brief_text(signal.get('label')) or 'Behaviour signal'}", ""])
        lines.append(f"Category: {_brief_text(signal.get('category')) or 'not_recorded'}")
        lines.append(f"Evidence: {_brief_text(signal.get('evidence_summary')) or 'not recorded'}")
        lines.append(f"Implication: {_brief_text(signal.get('implication')) or 'not recorded'}")
        lines.append(f"Confidence: {_brief_text(signal.get('confidence')) or 'not_recorded'}")
        lines.append(f"Caveats: {_brief_text(signal.get('caveats')) or 'not recorded'}")
        refs = _evidence_path_refs(signal.get("evidence_ids", []) or [], context, limit=3)
        if refs:
            lines.append("Example evidence: " + "; ".join(f"`{ref}`" for ref in refs) + ".")
        lines.append("")
    if len(signals) > limit:
        lines.append(f"{len(signals) - limit} additional signal(s) are available in audit mode and JSON.")
        lines.append("")


def _render_observed_signals(lines: list[str], signals: Any, context: _RenderContext) -> None:
    lines.extend(["## Observed Work Behaviour Signals", ""])
    if not isinstance(signals, list) or not signals:
        lines.append("No behaviour signals recorded.")
        lines.append("")
        return
    for index, signal in enumerate(signals, start=1):
        if not isinstance(signal, dict):
            continue
        lines.extend([f"### {index}. {_brief_text(signal.get('label')) or 'Behaviour signal'}", ""])
        lines.append(f"Category: {_brief_text(signal.get('category')) or 'not_recorded'}")
        lines.append(f"Evidence: {_brief_text(signal.get('evidence_summary')) or 'not recorded'}")
        lines.append(f"Implication: {_brief_text(signal.get('implication')) or 'not recorded'}")
        lines.append(f"Confidence: {_brief_text(signal.get('confidence')) or 'not_recorded'}")
        lines.append(f"Caveats: {_brief_text(signal.get('caveats')) or 'not recorded'}")
        evidence_ids = signal.get("evidence_ids", [])
        if isinstance(evidence_ids, list) and evidence_ids:
            lines.append("Evidence references: " + ", ".join(str(evidence_id) for evidence_id in evidence_ids))
            _render_evidence_details(lines, evidence_ids, context)
        lines.append("")


def _render_engineering_habits_summary(lines: list[str], habits: Any, context: _RenderContext) -> None:
    lines.extend(["## Engineering Habits", ""])
    if not isinstance(habits, list) or not habits:
        lines.append("Not recorded.")
        lines.append("")
        return
    for index, habit in enumerate([item for item in habits if isinstance(item, dict)], start=1):
        lines.extend([f"### {index}. {_brief_text(habit.get('label')) or 'Engineering habit'}", ""])
        lines.append(_brief_text(habit.get("description")) or "No habit description recorded.")
        lines.append(f"Confidence: {_brief_text(habit.get('confidence')) or 'not_recorded'}")
        caveats = _brief_text(habit.get("caveats"))
        if caveats:
            lines.append(f"Caveats: {caveats}")
        refs = _evidence_path_refs(habit.get("evidence_ids", []) or [], context, limit=3)
        if refs:
            lines.append("Evidence basis: " + "; ".join(f"`{ref}`" for ref in refs) + ".")
        lines.append("")


def _render_engineering_habits(lines: list[str], habits: Any, context: _RenderContext) -> None:
    lines.extend(["## Engineering Habits", ""])
    if not isinstance(habits, list) or not habits:
        lines.append("Not recorded.")
        lines.append("")
        return
    for index, habit in enumerate(habits, start=1):
        if not isinstance(habit, dict):
            continue
        lines.extend([f"### {index}. {_brief_text(habit.get('label')) or 'Engineering habit'}", ""])
        lines.append(_brief_text(habit.get("description")) or "No habit description recorded.")
        signal_ids = habit.get("supporting_signal_ids", [])
        if isinstance(signal_ids, list) and signal_ids:
            lines.append("Supporting signals: " + ", ".join(str(signal_id) for signal_id in signal_ids))
        lines.append(f"Confidence: {_brief_text(habit.get('confidence')) or 'not_recorded'}")
        lines.append(f"Caveats: {_brief_text(habit.get('caveats')) or 'not recorded'}")
        evidence_ids = habit.get("evidence_ids", [])
        if isinstance(evidence_ids, list) and evidence_ids:
            _render_evidence_details(lines, evidence_ids, context)
        lines.append("")


def _render_problem_solving_style_summary(lines: list[str], style: Any, context: _RenderContext) -> None:
    lines.extend(["## Problem-Solving Style", ""])
    if not isinstance(style, dict) or not style:
        lines.append("Not recorded.")
        lines.append("")
        return
    lines.append(_brief_text(style.get("summary")) or "No problem-solving synthesis recorded.")
    lines.append(f"Confidence: {_brief_text(style.get('confidence')) or 'not_recorded'}")
    lines.append(f"Caveats: {_brief_text(style.get('caveats')) or 'not recorded'}")
    refs = _evidence_path_refs(style.get("evidence_ids", []) or [], context, limit=3)
    if refs:
        lines.append("Evidence basis: " + "; ".join(f"`{ref}`" for ref in refs) + ".")
    lines.append("")


def _render_problem_solving_style(lines: list[str], style: Any, context: _RenderContext) -> None:
    lines.extend(["## Problem-Solving Style", ""])
    if not isinstance(style, dict) or not style:
        lines.append("Not recorded.")
        lines.append("")
        return
    lines.append(_brief_text(style.get("summary")) or "No problem-solving synthesis recorded.")
    signal_ids = style.get("supporting_signal_ids", [])
    if isinstance(signal_ids, list) and signal_ids:
        lines.append("Supporting signals: " + ", ".join(str(signal_id) for signal_id in signal_ids))
    lines.append(f"Confidence: {_brief_text(style.get('confidence')) or 'not_recorded'}")
    lines.append(f"Caveats: {_brief_text(style.get('caveats')) or 'not recorded'}")
    evidence_ids = style.get("evidence_ids", [])
    if isinstance(evidence_ids, list) and evidence_ids:
        _render_evidence_details(lines, evidence_ids, context)
    lines.append("")


def _render_mapping_section(lines: list[str], heading: str, mapping: Any) -> None:
    lines.extend([f"## {heading}", ""])
    if not isinstance(mapping, dict) or not mapping:
        lines.append("Not recorded.")
        lines.append("")
        return
    for key, value in mapping.items():
        lines.append(f"- {_humanize_id(key)}: {_brief_text(value) or 'Not recorded.'}")
    lines.append("")


def _render_cadence_summary(lines: list[str], cadence: Any, context: _RenderContext) -> None:
    lines.extend(["## Work Rhythm and Development Cadence", ""])
    if not isinstance(cadence, dict):
        lines.append("Cadence was not recorded.")
        lines.append("")
        return
    lines.append(_brief_text(cadence.get("summary")) or "No cadence summary recorded.")
    for heading, key in (("Commit-history evidence", "commit_history_signal"), ("Artifact-chronology evidence", "artifact_chronology_signal")):
        section = cadence.get(key)
        if not isinstance(section, dict):
            continue
        lines.extend(["", f"{heading}:"])
        lines.append(_brief_text(section.get("description")) or "Not recorded.")
        lines.append(f"Confidence: {_brief_text(section.get('confidence')) or 'not_recorded'}")
        caveats = _brief_text(section.get("caveats"))
        if caveats:
            lines.append(f"Caveats: {caveats}")
        refs = _evidence_path_refs(section.get("evidence_ids", []) or [], context, limit=3)
        if refs:
            lines.append("Example evidence: " + "; ".join(f"`{ref}`" for ref in refs) + ".")
    limitation = _brief_text(cadence.get("public_history_limitations"))
    if limitation:
        lines.extend(["", f"Public history limitations: {limitation}"])
    lines.append(f"Confidence: {_brief_text(cadence.get('confidence')) or 'not_recorded'}")
    lines.append(f"Caveats: {_brief_text(cadence.get('caveats')) or 'not recorded'}")
    lines.append("")


def _render_cadence(lines: list[str], cadence: Any, context: _RenderContext) -> None:
    lines.extend(["## Work Rhythm and Development Cadence", ""])
    if not isinstance(cadence, dict):
        lines.append("Cadence was not recorded.")
        lines.append("")
        return
    lines.append(_brief_text(cadence.get("summary")) or "No cadence summary recorded.")
    for heading, key in (("Commit-history evidence", "commit_history_signal"), ("Artifact-chronology evidence", "artifact_chronology_signal")):
        section = cadence.get(key)
        if not isinstance(section, dict):
            continue
        lines.extend(["", f"{heading}:"])
        lines.append(_brief_text(section.get("description")) or "Not recorded.")
        lines.append(f"Confidence: {_brief_text(section.get('confidence')) or 'not_recorded'}")
        lines.append(f"Caveats: {_brief_text(section.get('caveats')) or 'not recorded'}")
        evidence_ids = section.get("evidence_ids", [])
        if isinstance(evidence_ids, list) and evidence_ids:
            _render_evidence_details(lines, evidence_ids, context)
    lines.append("")
    limitation = _brief_text(cadence.get("public_history_limitations"))
    if limitation:
        lines.append(f"Public history limitations: {limitation}")
    lines.append(f"Confidence: {_brief_text(cadence.get('confidence')) or 'not_recorded'}")
    lines.append(f"Caveats: {_brief_text(cadence.get('caveats')) or 'not recorded'}")
    lines.append("")


def _render_environment_fit(lines: list[str], fit: Any) -> None:
    lines.extend(["## Environment Fit", ""])
    if not isinstance(fit, dict):
        lines.append("Environment fit was not recorded.")
        lines.append("")
        return
    for heading, key in (("May fit well", "may_fit_well"), ("May require care", "may_require_care")):
        lines.append(f"{heading}:")
        values = fit.get(key, [])
        if isinstance(values, list) and values:
            for value in values:
                lines.append(f"- {value}")
        else:
            lines.append("- Not recorded.")
        lines.append("")


def _render_role_family_fit_summary(lines: list[str], entries: Any, gaps: Any) -> None:
    lines.extend(["## Role-Family Fit", ""])
    if not isinstance(entries, list) or not entries:
        lines.append("No role-family entries recorded.")
        lines.append("")
        return
    if isinstance(gaps, list) and gaps:
        gap_labels = [
            _brief_text(gap.get("label"))
            for gap in gaps
            if isinstance(gap, dict) and _brief_text(gap.get("label"))
        ]
        if gap_labels:
            lines.append(
                "All role-family fit statements should be read with the evidence gaps in mind: "
                + _list_text(gap_labels[:4])
                + "."
            )
        else:
            lines.append(
                "All role-family fit statements should be read with the recorded evidence gaps in mind."
            )
        lines.append("")
    for index, entry in enumerate([item for item in entries if isinstance(item, dict)], start=1):
        lines.extend([f"### {index}. {_brief_text(entry.get('role_family')) or 'Role family'}", ""])
        paragraph_parts = [
            _brief_text(entry.get("why_discuss")),
            _brief_text(entry.get("behaviour_fit")),
            _brief_text(entry.get("likely_contribution")),
        ]
        lines.append(" ".join(part for part in paragraph_parts if part) or "Role-family fit was not recorded.")
        lines.append(f"Confidence: {_brief_text(entry.get('confidence')) or 'not_recorded'}")
        probes = _summary_role_probes(entry.get("interview_probes", []))
        if probes:
            lines.append("Role-specific probes:")
            for probe in probes:
                lines.append(f"- {probe}")
        lines.append("")


def _render_role_family_fit(lines: list[str], entries: Any) -> None:
    lines.extend(["## Role-Family Fit", ""])
    if not isinstance(entries, list) or not entries:
        lines.append("No role-family entries recorded.")
        lines.append("")
        return
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            continue
        lines.extend([f"### {index}. {_brief_text(entry.get('role_family')) or 'Role family'}", ""])
        lines.append(f"Why discuss: {_brief_text(entry.get('why_discuss')) or 'not recorded'}")
        lines.append(f"Behaviour fit: {_brief_text(entry.get('behaviour_fit')) or 'not recorded'}")
        lines.append(f"Likely contribution: {_brief_text(entry.get('likely_contribution')) or 'not recorded'}")
        lines.append(f"Confidence: {_brief_text(entry.get('confidence')) or 'not_recorded'}")
        lines.append(f"Caveats: {_brief_text(entry.get('caveats')) or 'not recorded'}")
        probes = entry.get("interview_probes", [])
        if isinstance(probes, list) and probes:
            lines.append("Interview probes:")
            for probe in probes:
                lines.append(f"- {probe}")
        lines.append("")


def _render_evidence_gaps(lines: list[str], gaps: Any) -> None:
    lines.extend(["## Evidence Gaps and Follow-Up Questions", ""])
    if not isinstance(gaps, list) or not gaps:
        lines.append("No evidence gaps recorded.")
        lines.append("")
        return
    for index, gap in enumerate(gaps, start=1):
        if not isinstance(gap, dict):
            continue
        lines.extend([f"### {index}. {_brief_text(gap.get('label')) or 'Evidence gap'}", ""])
        lines.append(f"Observed: {_brief_text(gap.get('what_was_observed')) or 'not recorded'}")
        lines.append(f"Why uncertain: {_brief_text(gap.get('why_uncertain')) or 'not recorded'}")
        lines.append(f"Follow-up: {_brief_text(gap.get('suggested_follow_up')) or 'not recorded'}")
        lines.append(f"Confidence: {_brief_text(gap.get('confidence')) or 'not_recorded'}")
        lines.append(f"Scope: {_brief_text(gap.get('scope')) or 'not recorded'}")
        lines.append("")


def _top_summary_signals(signals: Any, *, limit: int) -> list[dict[str, Any]]:
    if not isinstance(signals, list):
        return []
    reportable = [signal for signal in _reportable_signals(signals) if isinstance(signal, dict)]
    confidence_rank = {"high": 0, "medium": 1, "low": 2}
    ranked = sorted(
        enumerate(reportable),
        key=lambda item: (confidence_rank.get(_brief_text(item[1].get("confidence")).lower(), 3), item[0]),
    )
    return [signal for _, signal in ranked[:limit]]


def _summary_profile_refs(signals: list[dict[str, Any]], context: _RenderContext) -> list[str]:
    refs: list[str] = []
    for signal in signals:
        refs.extend(_evidence_path_refs(signal.get("evidence_ids", []) or [], context, limit=2))
    return _dedupe_brief_items(refs)[:3]


def _render_summary_bullets(lines: list[str], values: Any, *, fallback: str, limit: int) -> None:
    if isinstance(values, list) and values:
        for value in _dedupe_brief_items([_brief_text(item) for item in values])[:limit]:
            lines.append(f"- {value}")
        return
    lines.append(f"- {fallback}")


def _read_json_if_exists(path: Path, default: Any) -> Any:
    if path.exists():
        return read_json(path)
    return default


def _read_jsonl_if_exists(path: Path) -> list[dict[str, Any]]:
    if path.exists():
        return read_jsonl(path)
    return []


def _analysis_model_information(value: Any) -> str:
    return _brief_text(value) or "not recorded"


def _brief_text(value: Any) -> str:
    return " ".join(str(value or "").split())


def _reportable_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        signal
        for signal in signals
        if isinstance(signal, dict) and signal.get("category") not in {"authorship_bounds", "development_cadence"}
    ]


def _humanize_id(value: Any) -> str:
    text = _brief_text(value)
    if not text:
        return "Uncategorized"
    return text.replace("_", " ").replace("-", " ").title()


def _render_evidence_details(lines: list[str], evidence_ids: list[Any], context: _RenderContext, *, limit: int = 5) -> None:
    details = _evidence_detail_rows(evidence_ids, context, limit=limit)
    if not details:
        return
    lines.append("")
    lines.append("| Evidence ID | Repository | Path | Artifact type | Why it matters |")
    lines.append("| ----------- | ---------- | ---- | ------------- | -------------- |")
    for row in details:
        lines.append(
            "| "
            + " | ".join(
                _table_cell(row[key])
                for key in ("evidence_id", "repo_id", "path", "artifact_type", "reason")
            )
            + " |"
        )


def _evidence_detail_rows(evidence_ids: list[Any], context: _RenderContext, *, limit: int) -> list[dict[str, str]]:
    evidence_by_id = context.evidence_by_id
    artifact_type_by_id = context.artifact_type_by_id
    rows: list[dict[str, str]] = []
    for evidence_id in evidence_ids:
        item = evidence_by_id.get(str(evidence_id))
        if not item:
            continue
        artifact_id = _brief_text(item.get("artifact_id"))
        rows.append(
            {
                "evidence_id": _brief_text(item.get("evidence_id")),
                "repo_id": _brief_text(item.get("repo_id")) or "not recorded",
                "path": _brief_text(item.get("path")) or "not recorded",
                "artifact_type": _brief_text(artifact_type_by_id.get(artifact_id) or item.get("artifact_type")) or "not recorded",
                "reason": _evidence_review_reason(item, artifact_type_by_id.get(artifact_id) or item.get("artifact_type")),
            }
        )
        if len(rows) >= limit:
            break
    return rows


def _render_evidence_appendix(
    lines: list[str],
    context: _RenderContext,
    evidence_ids: list[Any],
    *,
    limit: int | None,
) -> None:
    lines.extend(["## Evidence Appendix", ""])
    rows = _evidence_detail_rows_unlimited(evidence_ids, context, limit=limit)
    if not rows:
        lines.append("No evidence details available.")
        lines.append("")
        return
    if limit is not None and len(_dedupe_brief_items([str(evidence_id) for evidence_id in evidence_ids])) > limit:
        lines.append(f"Capped to {limit} evidence record(s). Full evidence mapping remains available in JSON.")
        lines.append("")
    else:
        lines.append("Evidence IDs are included here for audit traceability; human-facing sections use repository/path references.")
        lines.append("")
    lines.append("| Evidence ID | Repository | Path | Artifact type | Why it matters |")
    lines.append("| ----------- | ---------- | ---- | ------------- | -------------- |")
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                _table_cell(row[key])
                for key in ("evidence_id", "repo_id", "path", "artifact_type", "reason")
            )
            + " |"
        )
    lines.append("")


def _evidence_detail_rows_unlimited(
    evidence_ids: list[Any],
    context: _RenderContext,
    *,
    limit: int | None,
) -> list[dict[str, str]]:
    if limit is None:
        return _evidence_detail_rows(evidence_ids, context, limit=len(evidence_ids) or len(context.evidence))
    return _evidence_detail_rows(evidence_ids, context, limit=limit)


def _report_evidence_ids(report: dict[str, Any]) -> list[Any]:
    evidence_ids: list[Any] = []

    def add_from(value: Any) -> None:
        if isinstance(value, dict):
            ids = value.get("evidence_ids")
            if isinstance(ids, list):
                evidence_ids.extend(ids)
            for child in value.values():
                add_from(child)
        elif isinstance(value, list):
            for child in value:
                add_from(child)

    add_from(report)
    return _dedupe_brief_items([str(evidence_id) for evidence_id in evidence_ids if evidence_id])


def _evidence_path_refs(evidence_ids: list[Any], context: _RenderContext, *, limit: int) -> list[str]:
    refs: list[str] = []
    evidence_by_id = context.evidence_by_id
    for evidence_id in evidence_ids:
        item = evidence_by_id.get(str(evidence_id))
        if not item:
            continue
        repo_id = _brief_text(item.get("repo_id"))
        path = _brief_text(item.get("path"))
        if not path:
            continue
        refs.append(f"{repo_id}/{path}" if repo_id else path)
        if len(_dedupe_brief_items(refs)) >= limit:
            break
    return _dedupe_brief_items(refs)[:limit]


def _summary_role_probes(probes: Any, *, limit: int = 3) -> list[str]:
    if not isinstance(probes, list):
        return []
    filtered: list[str] = []
    for probe in probes:
        text = _brief_text(probe)
        lower = text.lower()
        if not text:
            continue
        if "reviewed team work" in lower or "private or workplace" in lower or "project timeline" in lower:
            continue
        if "walkthrough of one artifact that demonstrates" in lower:
            continue
        filtered.append(text)
    selected = filtered or [_brief_text(probe) for probe in probes if _brief_text(probe)]
    return _dedupe_brief_items(selected)[:limit]


def _evidence_review_reason(item: dict[str, Any], artifact_type: Any) -> str:
    evidence_id = _brief_text(item.get("evidence_id")).lower()
    evidence_type = _brief_text(item.get("evidence_type")).lower()
    normalized_type = _brief_text(artifact_type).lower()
    notes = _brief_text(item.get("notes")).lower()

    if evidence_type == "absence":
        if "artifact_chronology" in notes:
            return "Anchors an artifact-chronology evidence limit without treating missing staged artifacts as weak rhythm."
        if "chronology" in notes:
            return "Anchors a public-history limitation without rendering raw commit data."
        return "Anchors a corpus-level evidence gap so missing public artifacts are treated as uncertainty."
    if "commit-history-signal" in evidence_id:
        return "Anchors bounded commit-history interpretation without exposing raw commit subjects or hashes."
    if "artifact-chronology-signal" in evidence_id:
        return "Shows dated or staged artifact chronology that can be read separately from commit count."
    if "documentation-reviewer-context" in evidence_id:
        return "Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context."
    if "architecture-explicit-boundaries" in evidence_id:
        return "Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions."
    if "implementation-inspectable-runtime" in evidence_id:
        return "Selected because it provides runnable or inspectable implementation evidence."
    if "testing-validation-gates" in evidence_id:
        return "Selected because it shows repeatable checks around runtime behavior or technical claims."
    if "evaluation-measurement-artifacts" in evidence_id:
        return "Selected because it exposes measurement, benchmark, model, data, or run context."
    if "maintainability-project-structure" in evidence_id:
        return "Selected because it helps reviewers inspect project structure, setup, or modification boundaries."
    if "research-experimentation-trace" in evidence_id:
        return "Selected because it preserves experiment, notebook, model-card, or failure-analysis context."
    if "product-reviewer-positioning" in evidence_id:
        return "Selected because it packages the work for technical readers, users, or adapter reviewers."
    if normalized_type == "readme":
        return "Selected because it exposes reviewer-facing purpose, setup, boundaries, or usage context."
    if normalized_type == "architecture_document":
        return "Selected because it exposes system boundaries, contracts, architecture, or runtime assumptions."
    if normalized_type in {"source_code", "inference_script", "training_script"}:
        return "Selected because it provides runnable or inspectable implementation evidence."
    if normalized_type in {"test_file", "ci_workflow"}:
        return "Selected because it shows repeatable checks around runtime behavior or technical claims."
    if normalized_type in {"evaluation_script", "model_card", "run_manifest", "data_manifest"}:
        return "Selected because it exposes measurement, benchmark, model, data, or run context."
    if normalized_type == "configuration_file":
        return "Selected because it helps reviewers inspect project structure, setup, or modification boundaries."
    if normalized_type in {"failure_analysis", "notebook_source"}:
        return "Selected because it preserves experiment, notebook, model-card, or failure-analysis context."
    return _truncate(_brief_text(item.get("excerpt_or_summary")) or _brief_text(item.get("notes")) or "Selected evidence.", 140)


def _table_cell(value: str) -> str:
    text = _brief_text(value).replace("|", "\\|")
    return text or "not recorded"


def _truncate(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rstrip() + "..."


def _strip_terminal_period(text: str) -> str:
    return _brief_text(text).rstrip(".")


def _evidence_reference_summary(evidence_ids: list[Any], evidence_by_id: dict[str, dict[str, Any]]) -> str:
    refs: list[str] = []
    for evidence_id in evidence_ids:
        item = evidence_by_id.get(evidence_id)
        if not item:
            continue
        path = _brief_text(item.get("path"))
        locator = item.get("locator")
        locator_value = ""
        if isinstance(locator, dict):
            locator_value = _brief_text(locator.get("value"))
        ref = path
        if locator_value:
            ref = f"{ref} ({locator_value})"
        if ref:
            refs.append(ref)
    return ", ".join(_dedupe_brief_items(refs[:4]))


def _dedupe_brief_items(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        text = _brief_text(item)
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(text)
    return deduped


def _list_text(values: list[str]) -> str:
    items = [value for value in values if value]
    if not items:
        return "not recorded"
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"
