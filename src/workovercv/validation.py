from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .constants import (
    CONFIDENCE_LEVELS,
    DISALLOWED_REPORT_PHRASES,
    OLD_REPORT_HEADINGS,
    PDF_ARTIFACTS,
    REPORT_HEADINGS,
    PROTECTED_TRAIT_TERMS,
    REQUIRED_FINAL_ARTIFACTS,
    SCREENING_BRIEF_ARTIFACT,
    SIGNAL_CATEGORY_IDS,
    SUMMARY_REPORT_ARTIFACT,
    SUMMARY_REPORT_HEADINGS,
)
from .io import read_json, read_jsonl
from .manifest import ManifestError, validate_review_scope
from .run_manifest import update_run_manifest


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


JSON_ARTIFACT_SCHEMAS = {
    "repo_inventory.json": "repo_inventory.schema.json",
    "artifact_inventory.json": "artifact_inventory.schema.json",
    "report.json": "report.schema.json",
    "role_family_fit.json": "role_family_fit.schema.json",
    "work_chronology.json": "work_chronology.schema.json",
    "red_team_review.json": "red_team_review.schema.json",
    "run_manifest.json": "run_manifest.schema.json",
}

JSONL_ARTIFACT_SCHEMAS = {
    "review_corpus.jsonl": "review_corpus.schema.json",
    "explicit_claims.jsonl": "explicit_claim.schema.json",
    "signal_ledger.jsonl": "signal.schema.json",
    "evidence_map.jsonl": "evidence.schema.json",
    "gap_register.jsonl": "gap.schema.json",
    "mitigations.jsonl": "mitigation.schema.json",
}


@dataclass
class BoundaryIndex:
    repo_ids: set[str]
    artifact_ids: set[str]
    artifact_repo_by_id: dict[str, str]
    artifact_paths_by_id: dict[str, set[str]]
    artifact_type_by_id: dict[str, str]


def validate_run(run_dir: Path, *, update_manifest: bool = True) -> ValidationResult:
    run_dir = run_dir.resolve()
    result = ValidationResult()
    _check_required_files(run_dir, result)
    if result.errors:
        return result
    _validate_pdf_artifacts(run_dir, result)
    if result.errors:
        return result

    _validate_review_scope_file(run_dir / "review_scope.yml", result)

    try:
        repo_inventory = read_json(run_dir / "repo_inventory.json")
        artifact_inventory = read_json(run_dir / "artifact_inventory.json")
        report = read_json(run_dir / "report.json")
        evidence = read_jsonl(run_dir / "evidence_map.jsonl")
        signals = read_jsonl(run_dir / "signal_ledger.jsonl")
        gaps = read_jsonl(run_dir / "gap_register.jsonl")
        mitigations = read_jsonl(run_dir / "mitigations.jsonl")
        claims = read_jsonl(run_dir / "explicit_claims.jsonl")
        role_family_fit = read_json(run_dir / "role_family_fit.json")
        work_chronology = read_json(run_dir / "work_chronology.json")
        red_team = read_json(run_dir / "red_team_review.json")
        run_manifest = read_json(run_dir / "run_manifest.json")
        review_corpus = read_jsonl(run_dir / "review_corpus.jsonl") if (run_dir / "review_corpus.jsonl").exists() else []
    except Exception as exc:
        result.errors.append(str(exc))
        return result

    loaded_json = {
        "repo_inventory.json": repo_inventory,
        "artifact_inventory.json": artifact_inventory,
        "report.json": report,
        "role_family_fit.json": role_family_fit,
        "work_chronology.json": work_chronology,
        "red_team_review.json": red_team,
        "run_manifest.json": run_manifest,
    }
    loaded_jsonl = {
        "review_corpus.jsonl": review_corpus,
        "explicit_claims.jsonl": claims,
        "signal_ledger.jsonl": signals,
        "evidence_map.jsonl": evidence,
        "gap_register.jsonl": gaps,
        "mitigations.jsonl": mitigations,
    }
    _validate_artifact_schemas(loaded_json, loaded_jsonl, result)

    _validate_repo_inventory(repo_inventory, result)
    boundary = _build_boundary_index(repo_inventory, artifact_inventory, review_corpus, result)
    _validate_artifact_inventory(artifact_inventory, boundary, result)
    _validate_review_corpus(review_corpus, boundary, result)
    _validate_required_fields(claims, "explicit_claims.jsonl", ["claim_id", "repo_id", "artifact_id", "claim_text", "claim_type", "scope", "risk_of_overclaim"], result)
    _validate_required_fields(signals, "signal_ledger.jsonl", ["signal_id", "category", "label", "evidence_ids", "evidence_summary", "implication", "confidence", "confidence_reason", "caveats"], result)
    _validate_required_fields(evidence, "evidence_map.jsonl", ["evidence_id", "repo_id", "artifact_id", "path", "locator", "evidence_type", "excerpt_or_summary", "supports", "evidence_strength"], result)
    _validate_required_fields(gaps, "gap_register.jsonl", ["gap_id", "repo_id", "category", "description", "impact_on_report", "related_signal_ids", "suggested_follow_up"], result)
    _validate_required_fields(mitigations, "mitigations.jsonl", ["mitigation_id", "related_gap_id", "related_signal_ids", "mitigation_type", "recommendation", "rationale"], result)

    ids = {
        "evidence": _id_set(evidence, "evidence_id", result, "evidence_map.jsonl"),
        "signals": _id_set(signals, "signal_id", result, "signal_ledger.jsonl"),
        "gaps": _id_set(gaps, "gap_id", result, "gap_register.jsonl"),
        "claims": _id_set(claims, "claim_id", result, "explicit_claims.jsonl"),
    }
    _validate_closed_signal_enums(signals, result)
    _validate_claims(claims, ids, boundary, result)
    _validate_signals(signals, ids, result)
    _validate_evidence(evidence, ids, boundary, result)
    _validate_gaps(gaps, ids, boundary, result)
    _validate_report(report, ids, result)
    _validate_mitigations(mitigations, ids, result)
    _validate_role_family_fit(role_family_fit, ids, result)
    _validate_report_role_family_fit(report, ids, result)
    _validate_no_raw_chronology_in_report(
        report,
        [run_dir / "report.md", run_dir / SUMMARY_REPORT_ARTIFACT],
        work_chronology,
        result,
    )
    _validate_red_team(red_team, result)
    _validate_prohibited_wording(
        report,
        run_dir / "report.md",
        run_dir / SUMMARY_REPORT_ARTIFACT,
        run_dir / SCREENING_BRIEF_ARTIFACT,
        signals=signals,
        evidence=evidence,
        gaps=gaps,
        mitigations=mitigations,
        role_family_fit=role_family_fit,
        red_team=red_team,
        result=result,
    )
    _validate_no_hiring_decisions(
        report,
        run_dir / "report.md",
        run_dir / SUMMARY_REPORT_ARTIFACT,
        run_dir / SCREENING_BRIEF_ARTIFACT,
        signals=signals,
        evidence=evidence,
        gaps=gaps,
        mitigations=mitigations,
        role_family_fit=role_family_fit,
        red_team=red_team,
        result=result,
    )

    if update_manifest and result.ok:
        update_run_manifest(run_dir, command="validate", config={"run": str(run_dir)}, status="complete")
    return result


def _check_required_files(run_dir: Path, result: ValidationResult) -> None:
    for artifact in REQUIRED_FINAL_ARTIFACTS:
        if not (run_dir / artifact).exists():
            result.errors.append(f"Missing required artifact: {artifact}")


def _validate_pdf_artifacts(run_dir: Path, result: ValidationResult) -> None:
    for artifact in PDF_ARTIFACTS:
        path = run_dir / artifact
        try:
            if path.stat().st_size == 0:
                result.errors.append(f"{artifact}: PDF artifact is empty")
                continue
            with path.open("rb") as handle:
                header = handle.read(5)
        except OSError as exc:
            result.errors.append(f"{artifact}: cannot read PDF artifact: {exc}")
            continue
        if header != b"%PDF-":
            result.errors.append(f"{artifact}: PDF artifact does not start with %PDF-")


def _schema_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "schemas"


def _validate_review_scope_file(path: Path, result: ValidationResult) -> None:
    try:
        scope = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        result.errors.append(f"review_scope.yml: invalid YAML: {exc}")
        return
    except OSError as exc:
        result.errors.append(f"review_scope.yml: cannot read review scope: {exc}")
        return

    error_count = len(result.errors)
    _validate_schema(scope, "review_scope.schema.json", "review_scope.yml", result)
    if len(result.errors) != error_count:
        return
    if not isinstance(scope, dict):
        return

    try:
        validate_review_scope(scope)
    except ManifestError as exc:
        result.errors.append(f"review_scope.yml: manifest violation: {exc}")


def _validate_artifact_schemas(
    json_artifacts: dict[str, Any],
    jsonl_artifacts: dict[str, list[dict[str, Any]]],
    result: ValidationResult,
) -> None:
    for label, value in json_artifacts.items():
        _validate_schema(value, JSON_ARTIFACT_SCHEMAS[label], label, result)
    for label, records in jsonl_artifacts.items():
        schema_name = JSONL_ARTIFACT_SCHEMAS[label]
        for index, record in enumerate(records, start=1):
            _validate_schema(record, schema_name, f"{label}:{index}", result)


def _validate_schema(value: Any, schema_name: str, label: str, result: ValidationResult) -> None:
    schema_path = _schema_dir() / schema_name
    if not schema_path.exists():
        result.errors.append(f"{label}: missing schema {schema_name}")
        return
    try:
        schema = read_json(schema_path)
    except Exception as exc:
        result.errors.append(f"{label}: cannot load schema {schema_name}: {exc}")
        return
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        result.errors.append(f"{label}: schema violation at {location}: {error.message}")


def _id_set(records: list[dict[str, Any]], field: str, result: ValidationResult, label: str) -> set[str]:
    ids: set[str] = set()
    for index, record in enumerate(records, start=1):
        value = record.get(field)
        if not isinstance(value, str) or not value:
            result.errors.append(f"{label}:{index}: missing {field}")
            continue
        if value in ids:
            result.errors.append(f"{label}:{index}: duplicate {field}: {value}")
        ids.add(value)
    return ids


def _validate_required_fields(records: list[dict[str, Any]], label: str, fields: list[str], result: ValidationResult) -> None:
    for index, record in enumerate(records, start=1):
        for field_name in fields:
            if field_name not in record or record.get(field_name) in (None, ""):
                result.errors.append(f"{label}:{index}: missing required field {field_name}")


def _validate_repo_inventory(repo_inventory: dict[str, Any], result: ValidationResult) -> None:
    if not isinstance(repo_inventory.get("candidate"), dict):
        result.errors.append("repo_inventory.json requires candidate object")
    repositories = repo_inventory.get("repositories")
    if not isinstance(repositories, list):
        result.errors.append("repo_inventory.json requires repositories list")
        return
    seen: set[str] = set()
    for index, repo in enumerate(repositories, start=1):
        for field_name in ("repo_id", "name", "url", "visibility", "selected_for_review", "selection_reason"):
            if field_name not in repo or repo.get(field_name) in (None, ""):
                result.errors.append(f"repo_inventory.json repositories[{index}] missing {field_name}")
        repo_id = repo.get("repo_id")
        if isinstance(repo_id, str):
            if repo_id in seen:
                result.errors.append(f"repo_inventory.json duplicate repo_id: {repo_id}")
            seen.add(repo_id)


def _build_boundary_index(
    repo_inventory: dict[str, Any],
    artifact_inventory: dict[str, Any],
    review_corpus: list[dict[str, Any]],
    result: ValidationResult,
) -> BoundaryIndex:
    repo_ids = {
        repo.get("repo_id")
        for repo in repo_inventory.get("repositories", [])
        if isinstance(repo, dict) and isinstance(repo.get("repo_id"), str) and repo.get("repo_id")
    }
    artifact_ids: set[str] = set()
    artifact_repo_by_id: dict[str, str] = {}
    artifact_paths_by_id: dict[str, set[str]] = {}
    artifact_type_by_id: dict[str, str] = {}

    for artifact in artifact_inventory.get("artifacts", []) if isinstance(artifact_inventory.get("artifacts"), list) else []:
        artifact_id = artifact.get("artifact_id")
        repo_id = artifact.get("repo_id")
        path = artifact.get("path")
        artifact_type = artifact.get("artifact_type")
        if isinstance(artifact_id, str) and artifact_id:
            artifact_ids.add(artifact_id)
            if isinstance(repo_id, str) and repo_id:
                artifact_repo_by_id.setdefault(artifact_id, repo_id)
            if isinstance(path, str) and path:
                artifact_paths_by_id.setdefault(artifact_id, set()).add(path)
            if isinstance(artifact_type, str) and artifact_type:
                artifact_type_by_id.setdefault(artifact_id, artifact_type)

    for record in review_corpus:
        artifact_id = record.get("artifact_id")
        repo_id = record.get("repo_id")
        path = record.get("path")
        artifact_type = record.get("artifact_type")
        if isinstance(artifact_id, str) and artifact_id:
            artifact_ids.add(artifact_id)
            if isinstance(repo_id, str) and repo_id:
                artifact_repo_by_id.setdefault(artifact_id, repo_id)
            if isinstance(path, str) and path:
                artifact_paths_by_id.setdefault(artifact_id, set()).add(path)
            if isinstance(artifact_type, str) and artifact_type:
                artifact_type_by_id.setdefault(artifact_id, artifact_type)

    if not repo_ids:
        result.errors.append("repo_inventory.json contains no known repositories")
    return BoundaryIndex(
        repo_ids=repo_ids,
        artifact_ids=artifact_ids,
        artifact_repo_by_id=artifact_repo_by_id,
        artifact_paths_by_id=artifact_paths_by_id,
        artifact_type_by_id=artifact_type_by_id,
    )


def _validate_artifact_inventory(artifact_inventory: dict[str, Any], boundary: BoundaryIndex, result: ValidationResult) -> None:
    artifacts = artifact_inventory.get("artifacts")
    if not isinstance(artifacts, list):
        result.errors.append("artifact_inventory.json requires artifacts list")
        return
    seen: set[str] = set()
    for index, artifact in enumerate(artifacts, start=1):
        for field_name in ("artifact_id", "repo_id", "path", "artifact_type", "size_estimate", "likely_signal_value"):
            if field_name not in artifact or artifact.get(field_name) in (None, ""):
                result.errors.append(f"artifact_inventory.json artifacts[{index}] missing {field_name}")
        artifact_id = artifact.get("artifact_id")
        if isinstance(artifact_id, str):
            if artifact_id in seen:
                result.errors.append(f"artifact_inventory.json duplicate artifact_id: {artifact_id}")
            seen.add(artifact_id)
        repo_id = artifact.get("repo_id")
        if isinstance(repo_id, str) and repo_id not in boundary.repo_ids:
            result.errors.append(f"Artifact {artifact_id} references unknown repo_id {repo_id}")


def _validate_review_corpus(review_corpus: list[dict[str, Any]], boundary: BoundaryIndex, result: ValidationResult) -> None:
    seen_chunks: set[str] = set()
    for index, record in enumerate(review_corpus, start=1):
        for field_name in ("chunk_id", "repo_id", "artifact_id", "path", "artifact_type", "locator", "text"):
            if field_name not in record or record.get(field_name) in (None, ""):
                result.errors.append(f"review_corpus.jsonl:{index}: missing required field {field_name}")
        chunk_id = record.get("chunk_id")
        if isinstance(chunk_id, str):
            if chunk_id in seen_chunks:
                result.errors.append(f"review_corpus.jsonl:{index}: duplicate chunk_id {chunk_id}")
            seen_chunks.add(chunk_id)
        repo_id = record.get("repo_id")
        artifact_id = record.get("artifact_id")
        path = record.get("path")
        if isinstance(repo_id, str) and repo_id not in boundary.repo_ids:
            result.errors.append(f"Corpus chunk {chunk_id} references unknown repo_id {repo_id}")
        if isinstance(artifact_id, str) and artifact_id not in boundary.artifact_ids:
            result.errors.append(f"Corpus chunk {chunk_id} references unknown artifact_id {artifact_id}")
        if isinstance(artifact_id, str) and isinstance(repo_id, str):
            known_repo = boundary.artifact_repo_by_id.get(artifact_id)
            if known_repo and known_repo != repo_id:
                result.errors.append(f"Corpus chunk {chunk_id} artifact {artifact_id} belongs to repo_id {known_repo}, not {repo_id}")
        if isinstance(artifact_id, str) and isinstance(path, str):
            known_paths = boundary.artifact_paths_by_id.get(artifact_id, set())
            if known_paths and path not in known_paths:
                result.errors.append(f"Corpus chunk {chunk_id} path {path} is not known for artifact_id {artifact_id}")
        artifact_type = record.get("artifact_type")
        if isinstance(artifact_id, str) and isinstance(artifact_type, str):
            known_type = boundary.artifact_type_by_id.get(artifact_id)
            if known_type and known_type != artifact_type:
                result.errors.append(
                    f"Corpus chunk {chunk_id} artifact {artifact_id} has artifact_type {artifact_type}, not {known_type}"
                )


def _validate_closed_signal_enums(signals: list[dict[str, Any]], result: ValidationResult) -> None:
    for signal in signals:
        signal_id = signal.get("signal_id")
        category = signal.get("category")
        if category not in SIGNAL_CATEGORY_IDS:
            result.errors.append(f"Signal {signal_id} has invalid category {category}")
        if signal.get("confidence") not in CONFIDENCE_LEVELS:
            result.errors.append(f"Signal {signal_id} has invalid confidence {signal.get('confidence')}")


def _validate_claims(
    claims: list[dict[str, Any]],
    ids: dict[str, set[str]],
    boundary: BoundaryIndex,
    result: ValidationResult,
) -> None:
    for claim in claims:
        _validate_repo_artifact_reference("Claim", claim.get("claim_id"), claim, boundary, result)
        for evidence_id in claim.get("evidence_ids", []) or []:
            if evidence_id not in ids["evidence"]:
                result.errors.append(f"Claim {claim.get('claim_id')} references unknown evidence_id {evidence_id}")


def _validate_signals(signals: list[dict[str, Any]], ids: dict[str, set[str]], result: ValidationResult) -> None:
    for signal in signals:
        if not signal.get("evidence_ids"):
            result.errors.append(f"Signal {signal.get('signal_id')} requires at least one evidence_id")
        for evidence_id in signal.get("evidence_ids", []) or []:
            if evidence_id not in ids["evidence"]:
                result.errors.append(f"Signal {signal.get('signal_id')} references unknown evidence_id {evidence_id}")


def _validate_evidence(
    evidence: list[dict[str, Any]],
    ids: dict[str, set[str]],
    boundary: BoundaryIndex,
    result: ValidationResult,
) -> None:
    for item in evidence:
        _validate_repo_artifact_reference("Evidence", item.get("evidence_id"), item, boundary, result)
        artifact_id = item.get("artifact_id")
        path = item.get("path")
        if isinstance(artifact_id, str) and isinstance(path, str):
            known_paths = boundary.artifact_paths_by_id.get(artifact_id, set())
            if not known_paths or path not in known_paths:
                result.errors.append(f"Evidence {item.get('evidence_id')} references unknown path {path} for artifact_id {artifact_id}")
        supports = item.get("supports", []) or []
        if not isinstance(supports, list):
            result.errors.append(f"Evidence {item.get('evidence_id')} supports must be a list")
            continue
        for support_id in supports:
            if support_id not in ids["claims"] and support_id not in ids["signals"]:
                result.errors.append(f"Evidence {item.get('evidence_id')} supports unknown id {support_id}")


def _validate_repo_artifact_reference(
    label: str,
    record_id: Any,
    record: dict[str, Any],
    boundary: BoundaryIndex,
    result: ValidationResult,
) -> None:
    repo_id = record.get("repo_id")
    artifact_id = record.get("artifact_id")
    if isinstance(repo_id, str) and repo_id not in boundary.repo_ids:
        result.errors.append(f"{label} {record_id} references unknown repo_id {repo_id}")
    if isinstance(artifact_id, str) and artifact_id not in boundary.artifact_ids:
        result.errors.append(f"{label} {record_id} references unknown artifact_id {artifact_id}")
    if isinstance(artifact_id, str) and isinstance(repo_id, str):
        known_repo = boundary.artifact_repo_by_id.get(artifact_id)
        if known_repo and known_repo != repo_id:
            result.errors.append(f"{label} {record_id} artifact {artifact_id} belongs to repo_id {known_repo}, not {repo_id}")


def _validate_gaps(gaps: list[dict[str, Any]], ids: dict[str, set[str]], boundary: BoundaryIndex, result: ValidationResult) -> None:
    for gap in gaps:
        repo_id = gap.get("repo_id")
        if isinstance(repo_id, str) and repo_id not in boundary.repo_ids:
            result.errors.append(f"Gap {gap.get('gap_id')} references unknown repo_id {repo_id}")
        for signal_id in gap.get("related_signal_ids", []) or []:
            if signal_id not in ids["signals"]:
                result.errors.append(f"Gap {gap.get('gap_id')} references unknown signal_id {signal_id}")


def _validate_report(
    report: dict[str, Any],
    ids: dict[str, set[str]],
    result: ValidationResult,
) -> None:
    if report.get("title") != "Work Behaviour Profile Report":
        result.errors.append("report.json title must be Work Behaviour Profile Report")
    if "summary" in report or "findings" in report:
        result.errors.append("report.json must not contain legacy summary/findings fields")
    report_signals = report.get("observed_work_behaviour_signals", [])
    if not isinstance(report_signals, list) or not report_signals:
        result.errors.append("report.json requires observed_work_behaviour_signals")
    for signal in report_signals if isinstance(report_signals, list) else []:
        signal_id = signal.get("signal_id") if isinstance(signal, dict) else None
        if not isinstance(signal, dict):
            result.errors.append("Report signal entry must be an object")
            continue
        if signal_id not in ids["signals"]:
            result.errors.append(f"Report signal references unknown signal_id {signal_id}")
        if signal.get("category") in {"authorship_bounds", "development_cadence"}:
            result.errors.append(f"Report signal {signal_id} uses meta category {signal.get('category')} as an observed behaviour signal")
        for evidence_id in (signal.get("evidence_ids", []) if isinstance(signal, dict) else []) or []:
            if evidence_id not in ids["evidence"]:
                result.errors.append(f"Report signal {signal_id} references unknown evidence_id {evidence_id}")
    for habit in report.get("engineering_habits", []) or []:
        if isinstance(habit, dict):
            _validate_report_linked_record("Report engineering habit", habit.get("habit_id"), habit, ids, result)
    problem_solving = report.get("problem_solving_style")
    if isinstance(problem_solving, dict):
        _validate_report_linked_record("Report problem-solving style", "problem_solving_style", problem_solving, ids, result)
    cadence = report.get("work_rhythm_and_development_cadence")
    if isinstance(cadence, dict):
        for key in ("commit_history_signal", "artifact_chronology_signal"):
            section = cadence.get(key)
            if isinstance(section, dict):
                for evidence_id in section.get("evidence_ids", []) or []:
                    if evidence_id not in ids["evidence"]:
                        result.errors.append(f"Report cadence {key} references unknown evidence_id {evidence_id}")
    for gap in report.get("evidence_gaps_and_follow_up_questions", []) or []:
        if not isinstance(gap, dict):
            continue
        gap_id = gap.get("gap_id")
        if gap_id not in ids["gaps"]:
            result.errors.append(f"Report evidence gap references unknown gap_id {gap_id}")


def _validate_report_linked_record(
    label: str,
    record_id: Any,
    record: dict[str, Any],
    ids: dict[str, set[str]],
    result: ValidationResult,
) -> None:
    for signal_id in record.get("supporting_signal_ids", []) or []:
        if signal_id not in ids["signals"]:
            result.errors.append(f"{label} {record_id} references unknown signal_id {signal_id}")
    for evidence_id in record.get("evidence_ids", []) or []:
        if evidence_id not in ids["evidence"]:
            result.errors.append(f"{label} {record_id} references unknown evidence_id {evidence_id}")


def _validate_mitigations(mitigations: list[dict[str, Any]], ids: dict[str, set[str]], result: ValidationResult) -> None:
    for mitigation in mitigations:
        gap_id = mitigation.get("related_gap_id")
        if gap_id not in ids["gaps"]:
            result.errors.append(f"Mitigation {mitigation.get('mitigation_id')} references unknown gap_id {gap_id}")
        for signal_id in mitigation.get("related_signal_ids", []) or []:
            if signal_id not in ids["signals"]:
                result.errors.append(f"Mitigation {mitigation.get('mitigation_id')} references unknown signal_id {signal_id}")
    mitigated_gap_ids = {
        mitigation.get("related_gap_id")
        for mitigation in mitigations
        if isinstance(mitigation.get("related_gap_id"), str)
    }
    for gap_id in ids["gaps"]:
        if gap_id not in mitigated_gap_ids:
            result.errors.append(f"Evidence gap {gap_id} has no follow-up record in mitigations.jsonl")


def _validate_role_family_fit(role_family_fit: dict[str, Any], ids: dict[str, set[str]], result: ValidationResult) -> None:
    entries = role_family_fit.get("role_family_fit")
    if not isinstance(entries, list):
        result.errors.append("role_family_fit.json requires role_family_fit list")
        return
    if not entries:
        result.errors.append("role_family_fit.json requires at least one role-family entry")
    for index, entry in enumerate(entries, start=1):
        role = entry.get("role_family") or f"entry {index}"
        for field_name in ("role_family", "why_discuss", "behaviour_fit", "likely_contribution", "interview_probes", "confidence", "caveats", "supporting_signal_ids", "limiting_gap_ids"):
            if field_name not in entry or entry.get(field_name) in (None, ""):
                result.errors.append(f"Role-family fit {role} missing {field_name}")
        supporting = entry.get("supporting_signal_ids", []) or []
        limiting = entry.get("limiting_gap_ids", []) or []
        if not supporting:
            result.errors.append(f"Role-family fit {role} requires supporting_signal_ids")
        probes = entry.get("interview_probes", []) or []
        if not probes:
            result.errors.append(f"Role-family fit {role} requires interview_probes")
        for signal_id in supporting:
            if signal_id not in ids["signals"]:
                result.errors.append(f"Role-family fit {role} references unknown signal_id {signal_id}")
        for gap_id in limiting:
            if gap_id not in ids["gaps"]:
                result.errors.append(f"Role-family fit {role} references unknown gap_id {gap_id}")


def _validate_report_role_family_fit(report: dict[str, Any], ids: dict[str, set[str]], result: ValidationResult) -> None:
    entries = report.get("role_family_fit", [])
    if not isinstance(entries, list):
        result.errors.append("report.json requires role_family_fit list")
        return
    if not entries:
        result.errors.append("report.json requires at least one role-family entry")
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        role = entry.get("role_family") or "entry"
        for signal_id in entry.get("supporting_signal_ids", []) or []:
            if signal_id not in ids["signals"]:
                result.errors.append(f"Report role-family fit {role} references unknown signal_id {signal_id}")
        for gap_id in entry.get("limiting_gap_ids", []) or []:
            if gap_id not in ids["gaps"]:
                result.errors.append(f"Report role-family fit {role} references unknown gap_id {gap_id}")


def _validate_no_raw_chronology_in_report(
    report: dict[str, Any],
    markdown_paths: list[Path],
    work_chronology: dict[str, Any],
    result: ValidationResult,
) -> None:
    values = _report_text_values(report)
    for markdown_path in markdown_paths:
        if markdown_path.exists():
            values.append(markdown_path.read_text(encoding="utf-8"))
    text = "\n".join(values)
    if re.search(r"\b[0-9a-f]{40}\b", text, flags=re.IGNORECASE):
        result.errors.append("report output contains raw commit hash from chronology input")
    subjects = _chronology_subjects(work_chronology)
    lower_text = text.lower()
    for subject in subjects:
        if len(subject) >= 12 and subject.lower() in lower_text:
            result.errors.append("report output contains raw commit subject from chronology input")
            break


def _chronology_subjects(work_chronology: dict[str, Any]) -> list[str]:
    subjects: list[str] = []
    repositories = work_chronology.get("repositories", [])
    if not isinstance(repositories, list):
        return subjects
    for repo in repositories:
        if not isinstance(repo, dict):
            continue
        entries = repo.get("entries", [])
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, dict) and isinstance(entry.get("subject"), str):
                subjects.append(entry["subject"])
    return subjects


def _validate_red_team(red_team: dict[str, Any], result: ValidationResult) -> None:
    if red_team.get("pass") is not True:
        result.errors.append("red_team_review.json must have pass: true")
    issues = red_team.get("issues", []) or []
    if not isinstance(issues, list):
        result.errors.append("red_team_review.json issues must be a list")
        return
    for index, issue in enumerate(issues, start=1):
        for field_name in ("issue_id", "severity", "description", "required_change"):
            if field_name not in issue or issue.get(field_name) in (None, ""):
                result.errors.append(f"red_team_review.json issues[{index}] missing {field_name}")
        if issue.get("severity") == "high":
            result.errors.append(f"High-severity red-team issue is unresolved: {issue.get('description')}")


def _validate_prohibited_wording(
    report: dict[str, Any],
    report_md_path: Path,
    summary_report_path: Path,
    screening_brief_path: Path,
    *,
    signals: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    mitigations: list[dict[str, Any]],
    role_family_fit: dict[str, Any],
    red_team: dict[str, Any],
    result: ValidationResult,
) -> None:
    _check_prohibited_text("report.json", _report_text_values(report), result)

    if report_md_path.exists():
        report_md = report_md_path.read_text(encoding="utf-8")
        _check_prohibited_text("report.md", [report_md], result)
        _check_old_report_headings("report.md", report_md, result)
        _check_report_headings("report.md", report_md, result)
    if summary_report_path.exists():
        summary_report = summary_report_path.read_text(encoding="utf-8")
        _check_prohibited_text(SUMMARY_REPORT_ARTIFACT, [summary_report], result)
        _check_old_report_headings(SUMMARY_REPORT_ARTIFACT, summary_report, result)
        _check_summary_report_headings(SUMMARY_REPORT_ARTIFACT, summary_report, result)
        if "| Evidence ID | Repository | Path | Artifact type | Why it matters |" in summary_report:
            result.errors.append(f"{SUMMARY_REPORT_ARTIFACT}: full evidence table header is not allowed")
    if screening_brief_path.exists():
        screening_brief = screening_brief_path.read_text(encoding="utf-8")
        _check_prohibited_text(
            SCREENING_BRIEF_ARTIFACT,
            [screening_brief],
            result,
        )
        _check_old_report_headings(SCREENING_BRIEF_ARTIFACT, screening_brief, result)

    _check_prohibited_text(
        "signal_ledger.jsonl",
        (
            signal.get(field_name)
            for signal in signals
            for field_name in ("label", "evidence_summary", "implication", "confidence_reason", "caveats")
        ),
        result,
    )
    _check_prohibited_text(
        "evidence_map.jsonl",
        (
            item.get(field_name)
            for item in evidence
            for field_name in ("excerpt_or_summary", "notes")
        ),
        result,
    )
    _check_prohibited_text(
        "gap_register.jsonl",
        (
            gap.get(field_name)
            for gap in gaps
            for field_name in ("category", "description", "suggested_follow_up")
        ),
        result,
    )
    _check_prohibited_text(
        "mitigations.jsonl",
        (
            mitigation.get(field_name)
            for mitigation in mitigations
            for field_name in ("recommendation", "rationale")
        ),
        result,
    )
    _check_prohibited_text(
        "role_family_fit.json",
        (
            entry.get(field_name)
            for entry in role_family_fit.get("role_family_fit", [])
            if isinstance(entry, dict)
            for field_name in ("role_family", "why_discuss", "behaviour_fit", "likely_contribution", "caveats")
        ),
        result,
    )
    _check_prohibited_text(
        "red_team_review.json",
        (
            issue.get(field_name)
            for issue in red_team.get("issues", [])
            if isinstance(issue, dict)
            for field_name in ("description", "required_change")
        ),
        result,
    )


HIRING_DECISION_PATTERNS = [
    r"\brecommended decision\s*:\s*(hire|reject|do not hire|shortlist|offer|make an offer)\b",
    r"\b(recommend|recommended|recommendation is to)\s+(hire|reject|shortlist|make an offer|extend an offer)\b",
    r"\b(hire|reject|shortlist)\s+(the\s+)?candidate\b",
    r"\bdo not hire\b",
    r"\b(make|extend)\s+(an?\s+)?offer\b",
    r"\bshould\s+(not\s+)?be\s+hired\b",
    r"\b(did\s+not|didn't|do\s+not|does\s+not|won't|will\s+not|not)\s+get\s+hired\b",
]


def _validate_no_hiring_decisions(
    report: dict[str, Any],
    report_md_path: Path,
    summary_report_path: Path,
    screening_brief_path: Path,
    *,
    signals: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    mitigations: list[dict[str, Any]],
    role_family_fit: dict[str, Any],
    red_team: dict[str, Any],
    result: ValidationResult,
) -> None:
    _check_hiring_decision_text("report.json", _report_text_values(report), result)
    if report_md_path.exists():
        _check_hiring_decision_text("report.md", [report_md_path.read_text(encoding="utf-8")], result)
    if summary_report_path.exists():
        _check_hiring_decision_text(
            SUMMARY_REPORT_ARTIFACT,
            [summary_report_path.read_text(encoding="utf-8")],
            result,
        )
    if screening_brief_path.exists():
        _check_hiring_decision_text(
            SCREENING_BRIEF_ARTIFACT,
            [screening_brief_path.read_text(encoding="utf-8")],
            result,
        )
    _check_hiring_decision_text(
        "signal_ledger.jsonl",
        (
            signal.get(field_name)
            for signal in signals
            for field_name in ("label", "evidence_summary", "implication", "confidence_reason", "caveats")
        ),
        result,
    )
    _check_hiring_decision_text(
        "evidence_map.jsonl",
        (
            item.get(field_name)
            for item in evidence
            for field_name in ("excerpt_or_summary", "notes")
        ),
        result,
    )
    _check_hiring_decision_text(
        "gap_register.jsonl",
        (
            gap.get(field_name)
            for gap in gaps
            for field_name in ("category", "description", "suggested_follow_up")
        ),
        result,
    )
    _check_hiring_decision_text(
        "mitigations.jsonl",
        (
            mitigation.get(field_name)
            for mitigation in mitigations
            for field_name in ("recommendation", "rationale")
        ),
        result,
    )
    _check_hiring_decision_text(
        "role_family_fit.json",
        (
            entry.get(field_name)
            for entry in role_family_fit.get("role_family_fit", [])
            if isinstance(entry, dict)
            for field_name in ("role_family", "why_discuss", "behaviour_fit", "likely_contribution", "caveats")
        ),
        result,
    )
    _check_hiring_decision_text(
        "red_team_review.json",
        (
            issue.get(field_name)
            for issue in red_team.get("issues", [])
            if isinstance(issue, dict)
            for field_name in ("description", "required_change")
        ),
        result,
    )


def _report_text_values(report: dict[str, Any]) -> list[str]:
    return list(_walk_text_values(report))


def _walk_text_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        values: list[str] = []
        for item in value.values():
            values.extend(_walk_text_values(item))
        return values
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(_walk_text_values(item))
        return values
    return []


def _check_hiring_decision_text(label: str, values: Any, result: ValidationResult) -> None:
    text = "\n".join(str(value) for value in values if value not in (None, "")).lower()
    for pattern in HIRING_DECISION_PATTERNS:
        if re.search(pattern, text):
            result.errors.append(f"{label}: Hiring decision language found: {pattern}")


def _check_prohibited_text(label: str, values: Any, result: ValidationResult) -> None:
    text = "\n".join(str(value) for value in values if value not in (None, "")).lower()
    for phrase in DISALLOWED_REPORT_PHRASES:
        if phrase in text:
            result.errors.append(f"{label}: Disallowed report phrase found: {phrase}")
    for term in PROTECTED_TRAIT_TERMS:
        pattern = r"\b" + re.escape(term.lower()) + r"\b"
        if re.search(pattern, text):
            result.errors.append(f"{label}: Protected/private trait term found: {term}")


def _check_old_report_headings(label: str, text: str, result: ValidationResult) -> None:
    for heading in OLD_REPORT_HEADINGS:
        if heading in text:
            result.errors.append(f"{label}: legacy report heading found: {heading}")


def _check_report_headings(label: str, text: str, result: ValidationResult) -> None:
    allowed = set(REPORT_HEADINGS)
    for match in re.finditer(r"^## ([^\n#].*)$", text, flags=re.MULTILINE):
        heading = match.group(1).strip()
        if heading not in allowed:
            result.errors.append(f"{label}: unknown report heading found: ## {heading}")


def _check_summary_report_headings(label: str, text: str, result: ValidationResult) -> None:
    if "# Work Behaviour Profile Summary" not in text:
        result.errors.append(f"{label}: missing title # Work Behaviour Profile Summary")
    allowed = set(SUMMARY_REPORT_HEADINGS)
    for match in re.finditer(r"^## ([^\n#].*)$", text, flags=re.MULTILINE):
        heading = match.group(1).strip()
        if heading not in allowed:
            result.errors.append(f"{label}: unknown summary heading found: ## {heading}")
