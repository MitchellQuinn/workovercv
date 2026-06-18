from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .io import read_json, read_jsonl, write_json, write_jsonl


INVENTORY_SUMMARY_ARTIFACT_ID = "run-artifact-inventory-summary"
INVENTORY_SUMMARY_PATH = "artifact_inventory.json"
INVENTORY_SUMMARY_TYPE = "inventory_summary"
CHRONOLOGY_ARTIFACT_ID = "run-artifact-work-chronology"
CHRONOLOGY_PATH = "work_chronology.json"
CHRONOLOGY_TYPE = "work_chronology"
META_SIGNAL_CATEGORIES = {"authorship_bounds", "development_cadence"}
ARTIFACT_CHRONOLOGY_TYPES = {
    "model_card",
    "run_manifest",
    "data_manifest",
    "failure_analysis",
    "technical_writeup",
}
ARTIFACT_CHRONOLOGY_MARKER_RE = re.compile(
    r"(?<!\d)(20\d{2}[-_/]?\d{0,4}|v\d+(?:[._-]\d+)+|stage[-_/]?\d+|phase[-_/]?\d+|iteration[-_/]?\d+|run[-_/]?\d+|metrics?|history|benchmark|failure|postmortem)(?!\d)",
    flags=re.IGNORECASE,
)


@dataclass(frozen=True)
class SignalSpec:
    key: str
    category: str
    label: str
    artifact_types: list[str]
    evidence_summary: str
    implication: str
    claim_text: str
    caveats: str
    max_items: int = 5
    max_per_repo: int = 2


SIGNAL_SPECS = [
    SignalSpec(
        key="documentation-reviewer-context",
        category="documentation_and_handoff",
        label="Makes technical work inspectable for reviewers",
        artifact_types=["README", "technical_writeup", "architecture_document"],
        evidence_summary="Reviewer-facing documentation explains purpose, usage, boundaries, or operating assumptions.",
        implication="This suggests a working style that values external legibility, explicit context, and reviewer handoff.",
        claim_text="The reviewed repositories include reviewer-facing documentation.",
        caveats="Public documentation does not directly prove workplace team handoff behavior.",
    ),
    SignalSpec(
        key="architecture-explicit-boundaries",
        category="system_design",
        label="Externalises system boundaries and contracts",
        artifact_types=["architecture_document", "technical_writeup", "configuration_file"],
        evidence_summary="Architecture, contract, and configuration artifacts expose design intent, workflow boundaries, or runtime interfaces.",
        implication="This suggests a tendency to make system shape and operating constraints explicit before or during implementation.",
        claim_text="The reviewed repositories include architecture or design-boundary evidence.",
        caveats="Repository artifacts show documented boundaries but do not prove how these decisions were negotiated in a team.",
    ),
    SignalSpec(
        key="implementation-inspectable-runtime",
        category="implementation_execution",
        label="Translates ideas into runnable, inspectable systems",
        artifact_types=["source_code", "inference_script", "training_script", "evaluation_script"],
        evidence_summary="Implementation artifacts expose concrete runtime behavior rather than only project descriptions.",
        implication="This suggests a working style oriented toward executable artifacts that reviewers can inspect and run.",
        claim_text="The reviewed repositories include inspectable implementation artifacts.",
        caveats="Static source inspection does not prove production runtime reliability or operational ownership.",
    ),
    SignalSpec(
        key="testing-validation-gates",
        category="validation_and_reliability",
        label="Adds validation gates around technical claims and runtime behaviour",
        artifact_types=["test_file", "CI_workflow"],
        evidence_summary="Test and CI artifacts provide direct evidence of reliability checks and validation gates.",
        implication="This suggests a habit of surrounding implementation work with repeatable checks.",
        claim_text="The reviewed repositories include test or CI evidence.",
        caveats="Repository tests show public validation behavior, not the full reliability practices used in private or deployed systems.",
    ),
    SignalSpec(
        key="evaluation-measurement-artifacts",
        category="measurement_and_evaluation",
        label="Prefers measured evidence over assertion",
        artifact_types=["evaluation_script", "model_card", "run_manifest", "data_manifest"],
        evidence_summary="Evaluation, model, run, or data manifest artifacts make measurement workflow and benchmark context inspectable.",
        implication="This suggests a tendency to support technical claims with measurement artifacts and reproducibility context.",
        claim_text="The reviewed repositories include evaluation or benchmark artifacts.",
        caveats="Metric artifacts need domain review before being treated as proof of model or system quality.",
    ),
    SignalSpec(
        key="maintainability-project-structure",
        category="maintainability",
        label="Structures projects for modification and handoff",
        artifact_types=["configuration_file", "source_code", "technical_writeup", "architecture_document"],
        evidence_summary="Configuration, source organization, and supporting documentation expose maintainability-relevant project structure.",
        implication="This suggests attention to project shape, repeatable setup, and future modification.",
        claim_text="The reviewed repositories include maintainability-relevant implementation structure.",
        caveats="Public structure does not prove long-term maintenance in a production organization.",
    ),
    SignalSpec(
        key="research-experimentation-trace",
        category="experimentation_and_learning",
        label="Explores uncertain technical spaces while preserving traceability",
        artifact_types=["failure_analysis", "model_card", "training_script", "notebook_source", "data_manifest"],
        evidence_summary="Research, experiment, model-card, notebook-source, or failure-analysis artifacts expose exploratory workflow and tradeoff records.",
        implication="This suggests comfort with uncertain technical spaces when there is a visible trail of experiments and tradeoffs.",
        claim_text="The reviewed repositories include research, training, or failure-analysis artifacts.",
        caveats="Notebook source and experiment traces are static evidence; WorkOverCV does not execute them or validate omitted outputs.",
    ),
    SignalSpec(
        key="product-reviewer-positioning",
        category="product_packaging",
        label="Packages technical work so other people can understand and interrogate it",
        artifact_types=["README", "technical_writeup", "configuration_file"],
        evidence_summary="Product or reviewer-positioning artifacts show how the work is packaged, explained, or made usable by others.",
        implication="This suggests attention to audience, usage context, and public inspectability.",
        claim_text="The reviewed repositories include product or reviewer positioning material.",
        caveats="Public packaging does not by itself prove user adoption or product-market fit.",
    ),
]


CATEGORY_REVIEW_LENS = {
    "system_design": "technical reviewers can probe design tradeoffs and ownership boundaries",
    "implementation_execution": "technical reviewers can inspect how ideas are translated into runnable code",
    "validation_and_reliability": "reviewers can route the conversation toward validation habits instead of relying on repository size",
    "documentation_and_handoff": "reviewers can quickly understand purpose, setup, and stated limits",
    "measurement_and_evaluation": "applied-ML reviewers can ask targeted questions about metric validity and evaluation design",
    "maintainability": "founders can inspect whether the work is organized for handoff and repeated modification",
    "experimentation_and_learning": "research-oriented reviewers can discuss experiment design, iteration, and failure analysis",
    "product_packaging": "reviewers can identify whether the work is framed for users, reviewers, or adapter consumers",
    "development_cadence": "reviewers can discuss public work rhythm without treating speed as competence",
    "authorship_bounds": "reviewers should keep authorship claims bounded to public repository evidence",
}


ROLE_SPECS = [
    (
        "Software Engineer",
        [
            "implementation_execution",
            "system_design",
            "validation_and_reliability",
            "maintainability",
            "documentation_and_handoff",
        ],
        ["implementation_execution"],
    ),
    (
        "Applied ML Engineer",
        [
            "measurement_and_evaluation",
            "experimentation_and_learning",
            "implementation_execution",
            "documentation_and_handoff",
        ],
        ["measurement_and_evaluation", "experimentation_and_learning"],
    ),
    (
        "Research Engineer",
        [
            "experimentation_and_learning",
            "measurement_and_evaluation",
            "system_design",
            "documentation_and_handoff",
        ],
        ["experimentation_and_learning"],
    ),
    (
        "AI Evaluation Engineer",
        [
            "measurement_and_evaluation",
            "validation_and_reliability",
            "documentation_and_handoff",
            "experimentation_and_learning",
        ],
        ["measurement_and_evaluation"],
    ),
    (
        "Developer Tools Engineer",
        [
            "product_packaging",
            "documentation_and_handoff",
            "implementation_execution",
            "validation_and_reliability",
            "maintainability",
        ],
        ["product_packaging"],
    ),
]

ROLE_NARRATIVES = {
    "Software Engineer": {
        "focus": "runnable systems, explicit interfaces, validation gates, and maintainable project structure",
        "why": "Software-engineering fit is worth discussing when runnable code, explicit interfaces, validation checks, and project structure appear together in the public artifacts",
        "behaviour": "The observable match is implementation that is packaged with setup context, bounded interfaces, and checks another engineer can inspect or extend.",
        "contribution": "contribute inspectable implementation work with clear setup context, bounded interfaces, and reviewable maintenance paths",
        "probe": "Ask for a code walkthrough that covers interfaces, error handling, validation, and maintenance tradeoffs.",
    },
    "Applied ML Engineer": {
        "focus": "representation design, evaluation artifacts, benchmark context, model cards, and data or run manifests",
        "why": "Applied-ML fit is worth discussing when model, data, run, or evaluation artifacts make representation choices and measurement context visible",
        "behaviour": "The observable match is ML-adjacent work that connects implementation to metrics, manifests, model cards, and stated limitations.",
        "contribution": "turn model or data work into reproducible engineering artifacts with measurable claims and reviewer-visible assumptions",
        "probe": "Ask how one metric, dataset, or model-card claim was chosen, validated, and revised.",
    },
    "Research Engineer": {
        "focus": "ambiguous problem decomposition, experiment traces, bounded claims, and technical writeups",
        "why": "Research-engineering fit is worth discussing when exploratory artifacts preserve assumptions, rejected paths, experiment traces, or bounded technical claims",
        "behaviour": "The observable match is exploratory engineering that turns ambiguity into documented hypotheses, runnable prototypes, and evidence that can be challenged.",
        "contribution": "move exploratory technical ideas toward runnable, traceable prototypes without losing evidence boundaries",
        "probe": "Ask for an experiment walkthrough that covers the uncertainty, rejected paths, and evidence that changed direction.",
    },
    "AI Evaluation Engineer": {
        "focus": "evidence discipline, validation gates, metrics, reproducibility context, and claims auditing",
        "why": "AI-evaluation fit is worth discussing when claims are paired with metrics, checks, reproducibility context, or explicit evidence limits",
        "behaviour": "The observable match is a claims-auditing style: evidence records, validation gates, and metric context are available for review instead of being left as assertion.",
        "contribution": "make evaluation work auditable by connecting claims to metrics, manifests, checks, and explicit limitations",
        "probe": "Ask for a claims-audit walkthrough that traces an evaluation result back to source evidence and limitations.",
    },
    "Developer Tools Engineer": {
        "focus": "CLI or workflow packaging, adapter contracts, documentation, and user or reviewer context",
        "why": "Developer-tools fit is worth discussing when workflows are packaged with command surfaces, adapter contracts, setup documentation, or reviewer context",
        "behaviour": "The observable match is tool-shaped work that exposes installation, invocation, extension points, and failure surfaces for other engineers.",
        "contribution": "package technical workflows so other engineers can install, inspect, run, and extend them with less hidden context",
        "probe": "Ask for a tool-user walkthrough that covers setup friction, extension points, and failure modes.",
    },
}


def build_deterministic_assessment(run_dir: Path) -> None:
    run_dir = run_dir.resolve()
    repo_inventory = read_json(run_dir / "repo_inventory.json")
    artifact_inventory = read_json(run_dir / "artifact_inventory.json")
    work_chronology = read_json(run_dir / CHRONOLOGY_PATH) if (run_dir / CHRONOLOGY_PATH).exists() else _empty_chronology()
    review_corpus = read_jsonl(run_dir / "review_corpus.jsonl") if (run_dir / "review_corpus.jsonl").exists() else []
    artifact_records = artifact_inventory.get("artifacts", [])
    artifacts = _review_artifacts(artifact_records)
    if not artifacts:
        raise RuntimeError("Cannot build deterministic assessment without collected artifacts")
    inventory_summary_artifact = _ensure_inventory_summary_artifact(
        artifact_inventory,
        repo_inventory,
        artifacts,
        run_dir,
    )
    chronology_artifact = _ensure_chronology_artifact(
        artifact_inventory,
        repo_inventory,
        artifacts,
        run_dir,
    )
    write_json(run_dir / "artifact_inventory.json", artifact_inventory)

    corpus_by_artifact = _first_corpus_chunk_by_artifact(review_corpus)
    builder = _AssessmentBuilder(artifacts, corpus_by_artifact, inventory_summary_artifact, chronology_artifact)

    for spec in SIGNAL_SPECS:
        builder.add_signal_for_spec(spec)

    if not builder.has_category("validation_and_reliability"):
        builder.add_absence_signal(
            key="testing-validation-gap",
            category="validation_and_reliability",
            label="Validation evidence is bounded by missing public test or CI artifacts",
            strength="moderate",
            confidence="medium",
            evidence_summary="Artifact inventory review did not find direct test_file or CI_workflow artifacts in the collected corpus.",
            implication="This means reliability practices should be discussed through follow-up rather than inferred from repository contents.",
            confidence_reason="The conclusion is based on an inventory-level absence check over the collected artifacts.",
            caveats="Missing public test or CI evidence is uncertainty, not proof that testing did not happen elsewhere.",
            claim_text="The collected corpus lacks direct test or CI artifacts.",
        )

    cadence_evidence = {
        "commit_history_evidence_ids": builder.add_commit_history_evidence(work_chronology),
        "artifact_chronology": builder.add_artifact_chronology_evidence(),
    }

    gaps = _gaps_from_context(builder.signals, builder.evidence, work_chronology)
    mitigations = _mitigations_from_gaps(gaps)
    role_family_fit = _role_family_fit_from_signals(builder.signals, gaps)
    report = build_report_from_signals(
        repo_inventory=repo_inventory,
        signals=builder.signals,
        evidence=builder.evidence,
        gaps=gaps,
        mitigations=mitigations,
        role_family_fit=role_family_fit,
        work_chronology=work_chronology,
        cadence_evidence=cadence_evidence,
        artifact_count=len(artifacts),
        evidence_count=len(builder.evidence),
        repo_count=len({artifact["repo_id"] for artifact in artifacts}),
    )

    write_jsonl(run_dir / "evidence_map.jsonl", builder.evidence)
    write_jsonl(run_dir / "explicit_claims.jsonl", builder.claims)
    write_jsonl(run_dir / "signal_ledger.jsonl", builder.signals)
    write_jsonl(run_dir / "gap_register.jsonl", gaps)
    write_jsonl(run_dir / "mitigations.jsonl", mitigations)
    write_json(run_dir / "role_family_fit.json", role_family_fit)
    write_json(run_dir / "red_team_review.json", {"pass": True, "issues": []})
    write_json(run_dir / "report.json", report)


def build_report_from_signals(
    *,
    repo_inventory: dict[str, Any],
    signals: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    mitigations: list[dict[str, Any]],
    role_family_fit: dict[str, Any],
    work_chronology: dict[str, Any],
    cadence_evidence: dict[str, Any],
    artifact_count: int,
    evidence_count: int,
    repo_count: int,
) -> dict[str, Any]:
    if not signals or not evidence:
        raise RuntimeError("Cannot build report without validated signals and evidence")

    repository_names = _reviewed_repository_names(repo_inventory)
    reportable_signals = _reportable_signals(signals)
    cadence = _cadence_section(work_chronology, cadence_evidence)
    role_entries = role_family_fit.get("role_family_fit", []) if isinstance(role_family_fit, dict) else []
    return {
        "title": "Work Behaviour Profile Report",
        "analysis_model_information": "Deterministic WorkOverCV rubric analysis; no LLM model used.",
        "scope_and_evidence_base": {
            "candidate_url": _candidate_url(repo_inventory),
            "repository_count": repo_count,
            "artifact_count": artifact_count,
            "repository_names": repository_names,
            "evidence_note": (
                f"The report is based on {artifact_count} collected artifact(s), "
                f"{evidence_count} evidence record(s), and bounded chronology inputs from public or local repositories."
            ),
            "non_decision_note": "This is not a hiring decision record, ranking, background check, or pass/fail assessment.",
            "private_work_note": "Private, company, and uncollected work may not be visible in the reviewed repository evidence.",
        },
        "executive_work_profile": _executive_work_profile(reportable_signals, gaps, artifact_count, repo_count),
        "observed_work_behaviour_signals": [_report_signal(signal) for signal in reportable_signals],
        "engineering_habits": _engineering_habits(reportable_signals),
        "problem_solving_style": _problem_solving_style(reportable_signals),
        "work_rhythm_and_development_cadence": cadence,
        "environment_fit": _environment_fit(reportable_signals, gaps),
        "role_family_fit": role_entries,
        "evidence_gaps_and_follow_up_questions": [_report_gap(gap) for gap in gaps],
        "confidence_and_uncertainty_notes": _confidence_notes(reportable_signals, gaps, repo_count, artifact_count),
    }


def _review_artifacts(artifacts: Any) -> list[dict[str, Any]]:
    if not isinstance(artifacts, list):
        return []
    return [
        artifact
        for artifact in artifacts
        if isinstance(artifact, dict)
        and artifact.get("artifact_id") not in {INVENTORY_SUMMARY_ARTIFACT_ID, CHRONOLOGY_ARTIFACT_ID}
    ]


def _ensure_inventory_summary_artifact(
    artifact_inventory: dict[str, Any],
    repo_inventory: dict[str, Any],
    artifacts: list[dict[str, Any]],
    run_dir: Path,
) -> dict[str, Any]:
    artifact_records = artifact_inventory.setdefault("artifacts", [])
    if not isinstance(artifact_records, list):
        artifact_records = []
        artifact_inventory["artifacts"] = artifact_records

    summary_artifact = {
        "artifact_id": INVENTORY_SUMMARY_ARTIFACT_ID,
        "repo_id": _inventory_anchor_repo_id(repo_inventory, artifacts),
        "path": INVENTORY_SUMMARY_PATH,
        "artifact_type": INVENTORY_SUMMARY_TYPE,
        "size_bytes": _file_size(run_dir / INVENTORY_SUMMARY_PATH),
        "size_estimate": "small",
        "likely_signal_value": "medium",
        "notes": "Synthetic run-boundary artifact used to anchor inventory-level absence evidence across the collected artifact inventory.",
    }
    for index, artifact in enumerate(artifact_records):
        if isinstance(artifact, dict) and artifact.get("artifact_id") == INVENTORY_SUMMARY_ARTIFACT_ID:
            artifact_records[index] = summary_artifact
            return summary_artifact
    artifact_records.append(summary_artifact)
    return summary_artifact


def _ensure_chronology_artifact(
    artifact_inventory: dict[str, Any],
    repo_inventory: dict[str, Any],
    artifacts: list[dict[str, Any]],
    run_dir: Path,
) -> dict[str, Any]:
    artifact_records = artifact_inventory.setdefault("artifacts", [])
    if not isinstance(artifact_records, list):
        artifact_records = []
        artifact_inventory["artifacts"] = artifact_records

    chronology_artifact = {
        "artifact_id": CHRONOLOGY_ARTIFACT_ID,
        "repo_id": _inventory_anchor_repo_id(repo_inventory, artifacts),
        "path": CHRONOLOGY_PATH,
        "artifact_type": CHRONOLOGY_TYPE,
        "size_bytes": _file_size(run_dir / CHRONOLOGY_PATH),
        "size_estimate": "small",
        "likely_signal_value": "medium",
        "notes": "Synthetic run-boundary artifact used to anchor bounded chronology-derived cadence evidence.",
    }
    for index, artifact in enumerate(artifact_records):
        if isinstance(artifact, dict) and artifact.get("artifact_id") == CHRONOLOGY_ARTIFACT_ID:
            artifact_records[index] = chronology_artifact
            return chronology_artifact
    artifact_records.append(chronology_artifact)
    return chronology_artifact


def _empty_chronology() -> dict[str, Any]:
    return {
        "generated_at": "",
        "max_commits_per_repository": 50,
        "repositories": [],
    }


def _inventory_anchor_repo_id(repo_inventory: dict[str, Any], artifacts: list[dict[str, Any]]) -> str:
    repositories = repo_inventory.get("repositories", [])
    if isinstance(repositories, list):
        selected_repo_ids = [
            repo.get("repo_id")
            for repo in repositories
            if isinstance(repo, dict) and repo.get("selected_for_review") is True and isinstance(repo.get("repo_id"), str)
        ]
        if selected_repo_ids:
            return sorted(selected_repo_ids)[0]
        repo_ids = [repo.get("repo_id") for repo in repositories if isinstance(repo, dict) and isinstance(repo.get("repo_id"), str)]
        if repo_ids:
            return sorted(repo_ids)[0]
    artifact_repo_ids = [artifact.get("repo_id") for artifact in artifacts if isinstance(artifact.get("repo_id"), str)]
    if artifact_repo_ids:
        return sorted(set(artifact_repo_ids))[0]
    raise RuntimeError("Cannot create inventory-summary evidence without a known repository id")


def _file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


class _AssessmentBuilder:
    def __init__(
        self,
        artifacts: list[dict[str, Any]],
        corpus_by_artifact: dict[str, dict[str, Any]],
        inventory_summary_artifact: dict[str, Any],
        chronology_artifact: dict[str, Any],
    ) -> None:
        self.artifacts = artifacts
        self.corpus_by_artifact = corpus_by_artifact
        self.inventory_summary_artifact = inventory_summary_artifact
        self.chronology_artifact = chronology_artifact
        self.evidence: list[dict[str, Any]] = []
        self.claims: list[dict[str, Any]] = []
        self.signals: list[dict[str, Any]] = []

    def has_category(self, category: str) -> bool:
        return any(signal["category"] == category for signal in self.signals)

    def add_signal_for_spec(
        self,
        spec: SignalSpec,
        *,
        strength: str | None = None,
        confidence: str | None = None,
    ) -> None:
        bundle = self._evidence_bundle(spec)
        if not bundle:
            return
        resolved_strength = strength or _strength_for_bundle(bundle)
        resolved_confidence = confidence or _confidence_for_bundle(bundle)
        evidence_summary = _bundle_evidence_summary(spec.category, spec.evidence_summary, bundle)
        self._add_signal(
            key=spec.key,
            category=spec.category,
            label=spec.label,
            strength=resolved_strength,
            confidence=resolved_confidence,
            evidence_summary=evidence_summary,
            implication=spec.implication,
            confidence_reason=_confidence_reason_for_bundle(bundle, resolved_confidence),
            caveats=spec.caveats,
            claim_text=spec.claim_text,
            artifacts=bundle,
            evidence_type="direct",
        )

    def add_absence_signal(
        self,
        *,
        key: str,
        category: str,
        label: str,
        strength: str,
        confidence: str,
        evidence_summary: str,
        implication: str,
        confidence_reason: str,
        caveats: str,
        claim_text: str,
    ) -> None:
        anchor = self._absence_anchor_artifact()
        self._add_signal(
            key=key,
            category=category,
            label=label,
            strength=strength,
            confidence=confidence,
            evidence_summary=evidence_summary,
            implication=implication,
            confidence_reason=confidence_reason,
            caveats=caveats,
            claim_text=claim_text,
            artifacts=[anchor],
            evidence_type="absence",
            locator={"type": "inventory", "value": INVENTORY_SUMMARY_PATH},
            evidence_summary_override=evidence_summary,
            evidence_notes=(
                "absence_kind=corpus_absence; absence_result=no_matching_artifacts_found; "
                "scan_scope=artifact_inventory.json across the collected review corpus; "
                "not evidence from a single repository file."
            ),
        )

    def add_commit_history_evidence(self, work_chronology: dict[str, Any]) -> list[str]:
        summary = _chronology_signal_summary(work_chronology)
        evidence_id = self._add_run_boundary_evidence(
            key="commit-history-signal",
            claim_text="The collected chronology supports only bounded public work-rhythm interpretation.",
            claim_type="process",
            artifact=self.chronology_artifact,
            evidence_type="indirect" if summary["available"] else "absence",
            evidence_strength="weak" if summary["confidence"] == "low" else "moderate",
            locator={"type": "inventory", "value": CHRONOLOGY_PATH},
            excerpt_or_summary=summary["evidence_summary"],
            notes=(
                "chronology_kind=bounded_git_history; raw commit hashes and subjects are collected for analysis input "
                "but must not be rendered into the final report."
            ),
        )
        return [evidence_id]

    def add_artifact_chronology_evidence(self) -> dict[str, Any]:
        artifacts = _artifact_chronology_artifacts(self.artifacts)
        if not artifacts:
            evidence_id = self._add_run_boundary_evidence(
                key="artifact-chronology-signal",
                claim_text="The artifact inventory provides limited visible staged-output chronology.",
                claim_type="process",
                artifact=self.inventory_summary_artifact,
                evidence_type="absence",
                evidence_strength="weak",
                locator={"type": "inventory", "value": INVENTORY_SUMMARY_PATH},
                excerpt_or_summary="Artifact inventory did not contain dated or staged model, manifest, metric, benchmark, or failure-analysis artifacts.",
                notes="artifact_chronology_kind=inventory_absence; uses artifact paths and types, not filesystem modification times.",
            )
            return {
                "available": False,
                "evidence_ids": [evidence_id],
                "confidence": "low",
                "description": "No dated or staged model, manifest, metric, benchmark, or failure-analysis artifacts were detected in the collected artifact inventory.",
                "caveats": "Absence of public staged artifacts is an evidence limit, not evidence of weak iteration.",
            }

        evidence_ids: list[str] = []
        for artifact in artifacts[:5]:
            evidence_ids.append(
                self._add_run_boundary_evidence(
                    key=f"artifact-chronology-signal-{len(evidence_ids) + 1:02d}",
                    claim_text="Dated or staged artifacts can support a bounded artifact-chronology discussion.",
                    claim_type="process",
                    artifact=artifact,
                    evidence_type="indirect",
                    evidence_strength="moderate",
                    locator={"type": "file", "value": artifact["path"]},
                    excerpt_or_summary=(
                        f"{artifact['artifact_type']} path {artifact['path']} contains dated, staged, metric, "
                        "benchmark, run, or failure-analysis context visible in the collected inventory."
                    ),
                    notes="artifact_chronology_kind=dated_or_staged_path; uses artifact paths and types, not filesystem modification times.",
                )
            )
        paths = [artifact["path"] for artifact in artifacts[:3]]
        modes = _artifact_chronology_modes(artifacts)
        return {
            "available": True,
            "evidence_ids": evidence_ids,
            "confidence": "medium",
            "description": (
                f"Dated or staged artifact paths such as {_list_phrase(paths)} provide artifact-chronology evidence independent of commit count. "
                f"The visible staged-output modes are {_list_phrase(modes)}."
            ),
            "caveats": "Artifact chronology is inferred from inventory paths and artifact types; it does not show the full private work process.",
        }

    def _evidence_bundle(self, spec: SignalSpec) -> list[dict[str, Any]]:
        type_rank = {artifact_type: index for index, artifact_type in enumerate(spec.artifact_types)}
        all_candidates = [artifact for artifact in self.artifacts if artifact.get("artifact_type") in type_rank]
        candidates = [
            artifact
            for artifact in all_candidates
            if not _is_bundle_filler(artifact) and _fits_signal_category(artifact, spec.category)
        ]
        if not candidates:
            candidates = [artifact for artifact in all_candidates if not _is_bundle_filler(artifact)]
        if not candidates:
            candidates = all_candidates
        if not candidates:
            return []
        ranked = sorted(candidates, key=lambda artifact: _artifact_rank(artifact, type_rank, spec.category))
        selected: list[dict[str, Any]] = []
        selected_ids: set[str] = set()
        repo_counts: Counter[str] = Counter()

        for artifact in ranked:
            if len(selected) >= spec.max_items:
                break
            artifact_type = str(artifact.get("artifact_type") or "")
            if any(existing.get("artifact_type") == artifact_type for existing in selected):
                continue
            if _can_select_artifact(artifact, repo_counts, spec.max_per_repo):
                selected.append(artifact)
                selected_ids.add(artifact["artifact_id"])
                repo_counts[str(artifact.get("repo_id") or "")] += 1

        for artifact in ranked:
            if len(selected) >= spec.max_items:
                break
            if artifact.get("artifact_id") in selected_ids:
                continue
            if _can_select_artifact(artifact, repo_counts, spec.max_per_repo):
                selected.append(artifact)
                selected_ids.add(artifact["artifact_id"])
                repo_counts[str(artifact.get("repo_id") or "")] += 1

        return selected

    def _absence_anchor_artifact(self) -> dict[str, Any]:
        return self.inventory_summary_artifact

    def _add_signal(
        self,
        *,
        key: str,
        category: str,
        label: str,
        strength: str,
        confidence: str,
        evidence_summary: str,
        implication: str,
        confidence_reason: str,
        caveats: str,
        claim_text: str,
        artifacts: list[dict[str, Any]],
        evidence_type: str,
        locator: dict[str, str] | None = None,
        evidence_summary_override: str | None = None,
        evidence_notes: str = "",
    ) -> None:
        sequence = len(self.signals) + 1
        signal_id = f"sig-{sequence:03d}-{key}"
        claim_id = f"claim-{sequence:03d}-{key}"
        evidence_ids: list[str] = []

        for evidence_index, artifact in enumerate(artifacts, start=1):
            evidence_id = f"ev-{sequence:03d}-{key}-{evidence_index:02d}"
            evidence_ids.append(evidence_id)
            chunk = self.corpus_by_artifact.get(artifact["artifact_id"])
            evidence_locator = locator or (chunk.get("locator") if chunk else {"type": "file", "value": artifact["path"]})
            evidence_strength = _evidence_strength_for_artifact(artifact, strength, evidence_type)
            self.evidence.append(
                {
                    "evidence_id": evidence_id,
                    "repo_id": artifact["repo_id"],
                    "artifact_id": artifact["artifact_id"],
                    "path": artifact["path"],
                    "locator": evidence_locator,
                    "evidence_type": evidence_type,
                    "excerpt_or_summary": evidence_summary_override or _artifact_evidence_summary(artifact, chunk),
                    "supports": [claim_id, signal_id],
                    "evidence_strength": evidence_strength,
                    "notes": evidence_notes,
                }
            )

        anchor = artifacts[0]
        self.claims.append(
            {
                "claim_id": claim_id,
                "repo_id": anchor["repo_id"],
                "artifact_id": anchor["artifact_id"],
                "claim_text": claim_text,
                "claim_type": _claim_type_for_category(category),
                "scope": "narrow",
                "risk_of_overclaim": "low" if evidence_type == "direct" else "medium",
                "evidence_ids": evidence_ids,
            }
        )
        self.signals.append(
            {
                "signal_id": signal_id,
                "category": category,
                "evidence_ids": evidence_ids,
                "label": label,
                "evidence_summary": evidence_summary,
                "implication": implication,
                "confidence": confidence,
                "confidence_reason": confidence_reason,
                "caveats": caveats,
            }
        )

    def _add_run_boundary_evidence(
        self,
        *,
        key: str,
        claim_text: str,
        claim_type: str,
        artifact: dict[str, Any],
        evidence_type: str,
        evidence_strength: str,
        locator: dict[str, str],
        excerpt_or_summary: str,
        notes: str,
    ) -> str:
        sequence = len(self.claims) + 1
        claim_id = f"claim-{sequence:03d}-{key}"
        evidence_id = f"ev-{sequence:03d}-{key}"
        self.evidence.append(
            {
                "evidence_id": evidence_id,
                "repo_id": artifact["repo_id"],
                "artifact_id": artifact["artifact_id"],
                "path": artifact["path"],
                "locator": locator,
                "evidence_type": evidence_type,
                "excerpt_or_summary": excerpt_or_summary,
                "supports": [claim_id],
                "evidence_strength": evidence_strength,
                "notes": notes,
            }
        )
        self.claims.append(
            {
                "claim_id": claim_id,
                "repo_id": artifact["repo_id"],
                "artifact_id": artifact["artifact_id"],
                "claim_text": claim_text,
                "claim_type": claim_type,
                "scope": "narrow",
                "risk_of_overclaim": "medium" if evidence_type in {"indirect", "absence"} else "low",
                "evidence_ids": [evidence_id],
            }
        )
        return evidence_id


def _first_corpus_chunk_by_artifact(review_corpus: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    chunks: dict[str, dict[str, Any]] = {}
    for chunk in review_corpus:
        artifact_id = chunk.get("artifact_id")
        if isinstance(artifact_id, str) and artifact_id not in chunks and _has_meaningful_text(chunk):
            chunks[artifact_id] = chunk
    return chunks


def _has_meaningful_text(chunk: dict[str, Any]) -> bool:
    return bool(_first_meaningful_text(str(chunk.get("text") or "")))


def _bundle_evidence_summary(category: str, base_summary: str, artifacts: list[dict[str, Any]]) -> str:
    artifact_count = len(artifacts)
    repo_count = len({artifact.get("repo_id") for artifact in artifacts})
    type_text = _artifact_type_phrase(artifact.get("artifact_type") for artifact in artifacts)
    lens = CATEGORY_REVIEW_LENS[category]
    repo_phrase = f"{repo_count} repository" if repo_count == 1 else f"{repo_count} repositories"
    artifact_phrase = "artifact" if artifact_count == 1 else "artifacts"
    return (
        f"{base_summary} The evidence bundle contains {artifact_count} {artifact_phrase} "
        f"across {repo_phrase}, including {type_text}; {lens}."
    )


def _confidence_reason_for_bundle(artifacts: list[dict[str, Any]], confidence: str) -> str:
    repo_count = len({artifact.get("repo_id") for artifact in artifacts})
    type_count = len({artifact.get("artifact_type") for artifact in artifacts})
    if confidence == "high":
        return "Evidence appears across multiple repositories and artifact types, with direct non-notebook artifacts present."
    if confidence == "medium":
        return f"Evidence is relevant but bounded to {len(artifacts)} artifact(s), {repo_count} repository record(s), and {type_count} artifact type(s)."
    return "Evidence is narrow or indirect, so this signal should be used as a prompt for follow-up."


def _artifact_type_phrase(values: Iterable[Any]) -> str:
    labels = [_category_label(str(value)) for value in _unique(str(value) for value in values if value)]
    if not labels:
        return "repository artifacts"
    if len(labels) == 1:
        return labels[0].lower()
    if len(labels) == 2:
        return f"{labels[0].lower()} and {labels[1].lower()}"
    return f"{', '.join(label.lower() for label in labels[:-1])}, and {labels[-1].lower()}"


def _artifact_evidence_summary(artifact: dict[str, Any], chunk: dict[str, Any] | None) -> str:
    path = str(artifact.get("path") or "artifact")
    artifact_type = str(artifact.get("artifact_type") or "artifact")
    if not chunk:
        return f"{path} is collected as {artifact_type} evidence."
    locator = chunk.get("locator", {})
    locator_value = locator.get("value") if isinstance(locator, dict) else None
    prefix = f"{path}"
    if locator_value:
        prefix += f" lines {locator_value}"
    text = _first_meaningful_text(str(chunk.get("text") or ""))
    if not text:
        return f"{prefix} is collected as {artifact_type} evidence."
    return f"{prefix} includes {artifact_type} content: {_truncate(text, 220)}"


def _first_meaningful_text(text: str) -> str:
    for line in text.splitlines():
        cleaned = line.strip().strip("#").strip()
        if cleaned and not cleaned.startswith("```"):
            return cleaned
    return ""


def _truncate(text: str, max_length: int) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[: max_length - 1].rstrip() + "..."


def _can_select_artifact(artifact: dict[str, Any], repo_counts: Counter[str], max_per_repo: int) -> bool:
    repo_id = str(artifact.get("repo_id") or "")
    return repo_counts[repo_id] < max_per_repo


def _strength_for_bundle(artifacts: list[dict[str, Any]]) -> str:
    repo_count = len({artifact.get("repo_id") for artifact in artifacts})
    type_count = len({artifact.get("artifact_type") for artifact in artifacts})
    if len(artifacts) >= 4 and (repo_count >= 2 or type_count >= 3):
        return "strong"
    if len(artifacts) >= 2:
        return "moderate"
    return "weak"


def _confidence_for_bundle(artifacts: list[dict[str, Any]]) -> str:
    repo_count = len({artifact.get("repo_id") for artifact in artifacts})
    type_count = len({artifact.get("artifact_type") for artifact in artifacts})
    has_direct_non_notebook = any(artifact.get("artifact_type") != "notebook_source" for artifact in artifacts)
    if len(artifacts) >= 5 and repo_count >= 2 and type_count >= 3 and has_direct_non_notebook:
        return "high"
    if len(artifacts) >= 2 and has_direct_non_notebook:
        return "medium"
    return "low"


def _evidence_strength_for_artifact(artifact: dict[str, Any], signal_strength: str, evidence_type: str) -> str:
    if evidence_type == "absence":
        return "weak"
    likely_value = artifact.get("likely_signal_value")
    if signal_strength == "strong" and likely_value == "high":
        return "strong"
    if likely_value == "low":
        return "weak"
    return "moderate"


def _artifact_rank(artifact: dict[str, Any], type_rank: dict[str, int], category: str) -> tuple[int, int, int, int, int, str]:
    artifact_type = str(artifact.get("artifact_type") or "")
    path = str(artifact.get("path") or "").replace("\\", "/").lower()
    return (
        type_rank.get(artifact_type, 999),
        _category_path_penalty(category, artifact_type, path),
        _artifact_quality_penalty(artifact_type, path),
        _artifact_signal_penalty(artifact),
        path.count("/"),
        path,
    )


def _category_path_penalty(category: str, artifact_type: str, path: str) -> int:
    penalty = 20
    if category == "documentation_and_handoff" and (path == "readme.md" or "/docs/" in f"/{path}"):
        penalty -= 10
    if category == "system_design" and any(token in path for token in ("architecture", "contract", "workflow", "manifest")):
        penalty -= 10
    if category == "implementation_execution" and (
        path.startswith(("src/", "scripts/")) or any(token in path for token in ("inference", "train", "evaluate"))
    ):
        penalty -= 8
    if category == "validation_and_reliability" and _looks_like_test_implementation(path):
        penalty -= 10
    if category == "measurement_and_evaluation" and any(token in path for token in ("eval", "metric", "model_card", "run_manifest")):
        penalty -= 10
    if category == "maintainability" and any(token in path for token in ("pyproject", "schema", "config", "src/", "docs/")):
        penalty -= 8
    if category == "experimentation_and_learning" and any(token in path for token in ("failure", "model_card", "notebook", "train", "experiment")):
        penalty -= 8
    if category == "product_packaging" and any(token in path for token in ("readme", "adapter", "plugin", "skill")):
        penalty -= 8
    if artifact_type == "notebook_source":
        penalty += 4
    return penalty


def _fits_signal_category(artifact: dict[str, Any], category: str) -> bool:
    artifact_type = str(artifact.get("artifact_type") or "")
    path = str(artifact.get("path") or "").replace("\\", "/").lower()
    if _is_globally_low_signal_path(path):
        return False
    if artifact_type == "README" and not (
        path == "readme"
        or path.endswith(("readme.md", "readme.txt", "readme.rst"))
        or path.endswith(("/readme.md", "/readme.txt", "/readme.rst"))
    ):
        return False
    if artifact_type in {"training_script", "inference_script", "evaluation_script"} and not path.endswith(
        (".py", ".sh", ".ps1")
    ):
        return False
    if category == "system_design":
        return artifact_type == "architecture_document" or any(
            token in path for token in ("architecture", "contract", "workflow", "schema")
        )
    if category == "measurement_and_evaluation":
        if artifact_type == "run_manifest" and path.startswith("schemas/"):
            return False
        if artifact_type == "data_manifest" and not any(
            token in path for token in ("data", "dataset", "metric", "model", "train", "preprocess", "eval")
        ):
            return False
        return any(token in path for token in ("eval", "metric", "model_card", "run_manifest", "dataset", "manifest"))
    if category == "product_packaging":
        if artifact_type == "README":
            return _is_product_readme_path(path)
        return any(token in path for token in ("adapter", "plugin", "skill", "readme"))
    if category == "maintainability":
        if any(token in path for token in ("copyright", "third_party", "notice", "license")):
            return False
        if artifact_type == "technical_writeup" and not any(
            token in path for token in ("adapter", "architecture", "contract", "design", "docs/")
        ):
            return False
        return artifact_type != "configuration_file" or any(
            token in path for token in ("pyproject", "schema", "config", "manifest", "workflow")
        )
    if category == "experimentation_and_learning":
        if artifact_type == "data_manifest" and not any(
            token in path for token in ("data", "dataset", "model", "train", "preprocess", "experiment", "eval")
        ):
            return False
        return True
    return True


def _is_globally_low_signal_path(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    return (
        "/packages/" in f"/{path}"
        or name in {"copyright.md", "third_party.md", "third_party_notices.md", "license", "license.md"}
        or name.endswith((".asset", ".asset.meta", ".meta"))
    )


def _is_product_readme_path(path: str) -> bool:
    if "failure-analysis/incidents/" in path:
        return False
    return path == "readme.md" or path.endswith(("/readme.md", "/readme.rst", "/readme.txt"))


def _artifact_quality_penalty(artifact_type: str, path: str) -> int:
    penalty = 0
    if "/tests/fixtures/" in f"/{path}" or "/fixtures/" in f"/{path}":
        penalty += 50
    if "/__pycache__/" in f"/{path}" or "/tmp/" in f"/{path}":
        penalty += 30
    if artifact_type == "README" and "/" in path:
        penalty += 10
    if artifact_type == "source_code" and path.endswith("/__init__.py"):
        penalty += 20
    if artifact_type == "test_file" and not _looks_like_test_implementation(path):
        penalty += 20
    if path.endswith((".png", ".jpg", ".jpeg", ".gif", ".bin", ".pkl")):
        penalty += 40
    return penalty


def _is_bundle_filler(artifact: dict[str, Any]) -> bool:
    artifact_type = str(artifact.get("artifact_type") or "")
    path = str(artifact.get("path") or "").replace("\\", "/").lower()
    size = artifact.get("size_bytes")
    if "/tests/fixtures/" in f"/{path}" or "/fixtures/" in f"/{path}":
        return True
    if "/__pycache__/" in f"/{path}" or "/tmp/" in f"/{path}":
        return True
    if artifact_type == "source_code" and path.endswith("/__init__.py"):
        return True
    if isinstance(size, int) and size <= 20:
        return True
    return False


def _artifact_signal_penalty(artifact: dict[str, Any]) -> int:
    likely_value = artifact.get("likely_signal_value")
    if likely_value == "high":
        return 0
    if likely_value == "medium":
        return 5
    return 10


def _artifact_chronology_artifacts(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [
        artifact
        for artifact in artifacts
        if artifact.get("artifact_type") in ARTIFACT_CHRONOLOGY_TYPES
        and _path_has_artifact_chronology_marker(str(artifact.get("path") or ""))
        and _has_strong_artifact_chronology_basis(artifact)
    ]
    return sorted(candidates, key=lambda artifact: (_artifact_signal_penalty(artifact), str(artifact.get("path") or "")))


def _has_strong_artifact_chronology_basis(artifact: dict[str, Any]) -> bool:
    artifact_type = str(artifact.get("artifact_type") or "")
    path = str(artifact.get("path") or "").replace("\\", "/").lower()
    notes = str(artifact.get("notes") or "").lower()
    text = f"{path} {notes}"
    if artifact_type in {"model_card", "run_manifest", "failure_analysis"}:
        return True
    if artifact_type == "data_manifest":
        return any(token in text for token in ("metric", "training_history", "history", "benchmark", "run_manifest", "model_card"))
    if artifact_type == "technical_writeup":
        return any(token in text for token in ("failure", "postmortem", "release", "changelog", "version", "progression", "history"))
    return False


def _artifact_chronology_modes(artifacts: list[dict[str, Any]]) -> list[str]:
    modes: list[str] = []
    for artifact in artifacts:
        artifact_type = str(artifact.get("artifact_type") or "")
        path = str(artifact.get("path") or "").replace("\\", "/").lower()
        if re.search(r"stage[-_/]?\d+|phase[-_/]?\d+|iteration[-_/]?\d+|v\d+(?:[._-]\d+)+|20\d{2}", path):
            modes.append("staged iteration")
        if artifact_type in {"model_card", "run_manifest"} or "run" in path:
            modes.append("release or run curation")
        if artifact_type in {"data_manifest", "evaluation_script"} or "metric" in path or "benchmark" in path:
            modes.append("benchmark progression")
        if artifact_type == "failure_analysis" or "failure" in path or "postmortem" in path:
            modes.append("failure-analysis progression")
        if artifact_type in {"training_script", "notebook_source"}:
            modes.append("experiment progression")
    return _unique(modes) or ["bounded staged refinement"]


def _path_has_artifact_chronology_marker(path: str) -> bool:
    return bool(ARTIFACT_CHRONOLOGY_MARKER_RE.search(path.replace("\\", "/")))


def _artifact_size_penalty(artifact: dict[str, Any]) -> int:
    size = artifact.get("size_bytes")
    if not isinstance(size, int):
        return 5
    if size <= 20:
        return 10
    if size <= 200:
        return 5
    return 0


def _looks_like_test_implementation(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    return (
        name.startswith("test_")
        or "_test." in name
        or ".test." in name
        or ".spec." in name
        or path.startswith(".github/workflows/")
    )


def _claim_type_for_category(category: str) -> str:
    return {
        "documentation_and_handoff": "process",
        "system_design": "architecture",
        "implementation_execution": "capability",
        "validation_and_reliability": "process",
        "measurement_and_evaluation": "metric",
        "maintainability": "process",
        "experimentation_and_learning": "reproducibility",
        "product_packaging": "employment_positioning",
        "development_cadence": "process",
        "authorship_bounds": "limitation",
    }[category]


def _gaps_from_context(
    signals: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    work_chronology: dict[str, Any],
) -> list[dict[str, Any]]:
    evidence_by_id = {record["evidence_id"]: record for record in evidence}
    gaps: list[dict[str, Any]] = []

    def add_gap(
        *,
        category: str,
        description: str,
        related_signal_ids: list[str],
        suggested_follow_up: str,
        impact_on_report: str = "requires_follow_up",
    ) -> None:
        repo_id = _repo_id_for_gap(related_signal_ids, signals, evidence_by_id)
        gaps.append(
            {
                "gap_id": f"gap-{len(gaps) + 1:03d}-{category}",
                "repo_id": repo_id,
                "category": category,
                "description": description,
                "impact_on_report": impact_on_report,
                "related_signal_ids": related_signal_ids,
                "suggested_follow_up": suggested_follow_up,
            }
        )

    validation_signal = _first_signal_by_category(signals, "validation_and_reliability")
    if validation_signal and _all_signal_evidence_type(validation_signal, evidence_by_id, "absence"):
        add_gap(
            category="validation_and_reliability_gap",
            description="The collected public artifacts do not include direct test or CI evidence; this limits what can be inferred about reliability habits from the repository sample.",
            related_signal_ids=[validation_signal["signal_id"]],
            suggested_follow_up="Ask for the test strategy, CI expectations, or reliability checks used outside the collected corpus.",
            impact_on_report="lowers_confidence",
        )

    handoff_ids = [
        signal["signal_id"]
        for signal in signals
        if signal.get("category") in {"documentation_and_handoff", "product_packaging"}
    ][:2]
    if handoff_ids:
        add_gap(
            category="collaboration_visibility_gap",
            description="Public repository evidence can show documentation and packaging, but it does not directly show team review, pull-request discussion, or workplace collaboration.",
            related_signal_ids=handoff_ids,
            suggested_follow_up="Ask for an example of reviewed team work, handoff notes, or pull request discussion.",
            impact_on_report="bounds_interpretation",
        )

    anchor_signal_ids = [signal["signal_id"] for signal in signals[:2]]
    add_gap(
        category="private_and_company_work_visibility_gap",
        description="The reviewed corpus is public repository evidence and may omit private, company, or collaborative work that would materially change interpretation.",
        related_signal_ids=anchor_signal_ids,
        suggested_follow_up="Ask which private or workplace projects best represent the same working behaviours.",
        impact_on_report="bounds_interpretation",
    )

    if _chronology_is_shallow(work_chronology):
        add_gap(
            category="development_cadence_visibility_gap",
            description="Readable git chronology was unavailable or shallow, so public commit cadence cannot support a confident work-rhythm interpretation.",
            related_signal_ids=[],
            suggested_follow_up="Ask the person to walk through a representative project timeline and explain major iteration points.",
            impact_on_report="lowers_confidence",
        )

    return gaps


def _mitigations_from_gaps(gaps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mitigations: list[dict[str, Any]] = []
    for gap in gaps:
        sequence = len(mitigations) + 1
        mitigations.append(
            {
                "mitigation_id": f"mit-{sequence:03d}",
                "related_gap_id": gap["gap_id"],
                "related_signal_ids": gap.get("related_signal_ids", []),
                "mitigation_type": "interview_probe",
                "recommendation": gap["suggested_follow_up"],
                "rationale": "This follow-up targets an evidence gap in the collected repository corpus without treating missing public evidence as inability.",
            }
        )
    return mitigations


def _role_family_fit_from_signals(signals: list[dict[str, Any]], gaps: list[dict[str, Any]]) -> dict[str, Any]:
    gap_ids = [gap["gap_id"] for gap in gaps]
    by_category = _signals_by_category(signals)
    role_family_fit: list[dict[str, Any]] = []
    for role, categories, required_any in ROLE_SPECS:
        category_signals = [
            signal
            for category in categories
            for signal in by_category.get(category, [])
        ]
        if not any(
            by_category.get(category)
            for category in required_any
        ):
            continue
        if not category_signals:
            continue
        supporting = category_signals[:6]
        role_family_fit.append(
            {
                "role_family": role,
                "why_discuss": _role_why_discuss(role, supporting),
                "behaviour_fit": _role_behaviour_fit(role, supporting),
                "likely_contribution": _role_likely_contribution(role),
                "interview_probes": _role_interview_probes(role, supporting, gaps),
                "confidence": _confidence(category_signals),
                "supporting_signal_ids": _signal_ids(category_signals[:6]),
                "limiting_gap_ids": gap_ids,
                "caveats": _role_caveats(gap_ids),
            }
        )
    if not role_family_fit:
        first_signal = signals[0]
        role_family_fit.append(
            {
                "role_family": "Software Engineer",
                "why_discuss": "Repository evidence supports only a bounded software-engineering conversation.",
                "behaviour_fit": first_signal["implication"],
                "likely_contribution": _role_likely_contribution("Software Engineer"),
                "interview_probes": ["Ask for a walkthrough of one representative artifact and the tradeoffs behind it."],
                "confidence": first_signal["confidence"],
                "supporting_signal_ids": [first_signal["signal_id"]],
                "limiting_gap_ids": gap_ids,
                "caveats": _role_caveats(gap_ids),
            }
        )
    return {"role_family_fit": role_family_fit}


def _role_why_discuss(role: str, signals: list[dict[str, Any]]) -> str:
    narrative = ROLE_NARRATIVES.get(role, {})
    base = narrative.get("why")
    if base:
        return f"{base}. Supporting evidence covers {_role_evidence_phrase(signals)}."
    return f"Repository evidence supports a bounded {role} discussion through {_role_evidence_phrase(signals)}."


def _role_behaviour_fit(role: str, signals: list[dict[str, Any]]) -> str:
    narrative = ROLE_NARRATIVES.get(role, {})
    behaviour = narrative.get("behaviour")
    if behaviour:
        return f"{behaviour} Evidence basis: {_role_evidence_phrase(signals)}."
    return f"The observable fit is bounded to {_role_evidence_phrase(signals)}."


def _role_likely_contribution(role: str) -> str:
    contribution = ROLE_NARRATIVES.get(role, {}).get(
        "contribution",
        "anchor a bounded technical discussion in inspectable public repository artifacts",
    )
    return f"The person would likely {contribution}, subject to the recorded evidence gaps."


def _role_interview_probes(role: str, signals: list[dict[str, Any]], gaps: list[dict[str, Any]]) -> list[str]:
    narrative_probe = ROLE_NARRATIVES.get(role, {}).get("probe")
    probes = [narrative_probe] if narrative_probe else []
    probes.extend(
        f"Ask for a walkthrough of one artifact that demonstrates {_category_label(signal['category']).lower()}."
        for signal in signals[:2]
    )
    probes.extend(gap["suggested_follow_up"] for gap in gaps[:2])
    return _unique(probes) or [f"Ask for a representative {role} work-sample walkthrough."]


def _role_caveats(gap_ids: list[str]) -> str:
    if gap_ids:
        return f"Interpret role-family fit with the recorded evidence gaps in view: {', '.join(gap_ids)}."
    return "Role-family fit is a discussion route based on public repository evidence, not a hiring recommendation."


def _role_evidence_phrase(signals: list[dict[str, Any]]) -> str:
    category_phrases = {
        "documentation_and_handoff": "reviewer-facing documentation",
        "system_design": "system-boundary artifacts",
        "implementation_execution": "runnable implementation artifacts",
        "validation_and_reliability": "tests or validation gates",
        "measurement_and_evaluation": "measurement and evaluation records",
        "maintainability": "maintainability-oriented project structure",
        "experimentation_and_learning": "experiment or failure-analysis traces",
        "product_packaging": "packaging and usage context",
    }
    categories = _unique(signal["category"] for signal in signals if signal.get("category") in category_phrases)
    phrases = [category_phrases[category] for category in categories[:5]]
    return _list_phrase(phrases) if phrases else "bounded repository evidence"


def _reviewed_repository_names(repo_inventory: dict[str, Any]) -> list[str]:
    repositories = repo_inventory.get("repositories", [])
    if not isinstance(repositories, list):
        return []
    names = [
        str(repo.get("name") or repo.get("repo_id"))
        for repo in repositories
        if isinstance(repo, dict) and repo.get("selected_for_review") is True
    ]
    return _unique(name for name in names if name)


def _candidate_url(repo_inventory: dict[str, Any]) -> str:
    candidate = repo_inventory.get("candidate", {})
    if isinstance(candidate, dict) and candidate.get("url"):
        return str(candidate["url"])
    return "not recorded"


def _executive_work_profile(
    signals: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    artifact_count: int,
    repo_count: int,
) -> str:
    categories = {signal["category"] for signal in signals}
    opening = (
        f"Across {artifact_count} collected artifact(s) from {repo_count} repository record(s), "
        "the reviewed work suggests an engineer who tends to make technical work inspectable"
    )
    if categories & {"documentation_and_handoff", "system_design", "product_packaging"}:
        opening += ": project purpose, boundaries, reviewer context, and packaging are repeatedly externalised into durable artifacts"
    else:
        opening += " within the limits of the selected public repository evidence"
    opening += "."

    evidence_patterns: list[str] = []
    if "implementation_execution" in categories:
        evidence_patterns.append("runnable code surfaces")
    if categories & {"validation_and_reliability", "measurement_and_evaluation"}:
        evidence_patterns.append("tests, metrics, manifests, or evaluation records")
    if "maintainability" in categories:
        evidence_patterns.append("project structure that supports later modification")
    if "experimentation_and_learning" in categories:
        evidence_patterns.append("experiment, model, notebook, or failure-analysis traces")
    pattern_sentence = (
        f"The strongest pattern is systems-oriented work made reviewable through {_list_phrase(evidence_patterns)}."
        if evidence_patterns
        else "The strongest pattern is bounded public work that can anchor a technical discussion."
    )

    confidence_sentence = _executive_confidence_sentence(signals)
    gap_sentence = (
        f"Evidence gaps are explicit: {len(gaps)} follow-up area(s) bound interpretation rather than serving as adverse conclusions."
        if gaps
        else "The usual limits of public repository evidence still apply, even where no additional gaps were recorded."
    )
    return f"{opening} {pattern_sentence} {confidence_sentence} {gap_sentence}"


def _executive_confidence_sentence(signals: list[dict[str, Any]]) -> str:
    confidence_by_theme = {
        "documentation_and_handoff": "documentation and handoff habits",
        "system_design": "system-boundary habits",
        "implementation_execution": "implementation habits",
        "validation_and_reliability": "validation habits",
        "measurement_and_evaluation": "measurement habits",
        "maintainability": "maintainability habits",
        "experimentation_and_learning": "experimentation habits",
        "product_packaging": "technical packaging habits",
    }
    strongest = [
        confidence_by_theme[signal["category"]]
        for signal in signals
        if signal.get("category") in confidence_by_theme and signal.get("confidence") in {"high", "medium"}
    ][:4]
    lower = [
        confidence_by_theme[signal["category"]]
        for signal in signals
        if signal.get("category") in confidence_by_theme and signal.get("confidence") == "low"
    ][:3]
    if not strongest:
        return "Confidence remains tentative because the selected public corpus is narrow."
    sentence = f"Confidence is strongest for {_list_phrase(strongest)}."
    if lower:
        sentence += f" Confidence is lower for {_list_phrase(lower)}."
    sentence += " Public evidence remains weaker for live collaboration, operational pressure, and private or company work unless those traces are present in the collected corpus."
    return sentence


def _reportable_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [signal for signal in signals if signal.get("category") not in META_SIGNAL_CATEGORIES]


def _report_signal(signal: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_id": signal["signal_id"],
        "category": signal["category"],
        "label": signal["label"],
        "evidence_summary": signal["evidence_summary"],
        "implication": signal["implication"],
        "confidence": signal["confidence"],
        "caveats": signal["caveats"],
        "evidence_ids": signal["evidence_ids"],
    }


def _report_gap(gap: dict[str, Any]) -> dict[str, Any]:
    return {
        "gap_id": gap["gap_id"],
        "label": _category_label(gap["category"]),
        "what_was_observed": gap["description"],
        "why_uncertain": "The repository corpus is a public evidence sample and does not expose every work context.",
        "suggested_follow_up": gap["suggested_follow_up"],
        "confidence": "medium" if gap["impact_on_report"] == "bounds_interpretation" else "low",
        "scope": "collected public repository evidence",
    }


def _engineering_habits(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    group_specs = [
        (
            "externalising_context_and_boundaries",
            "Externalising context and boundaries",
            ["documentation_and_handoff", "system_design"],
            "Documentation and design-boundary evidence point to a habit of moving context out of private assumptions and into artifacts that reviewers can inspect.",
        ),
        (
            "building_inspectable_runnable_artifacts",
            "Building inspectable runnable artifacts",
            ["implementation_execution"],
            "Implementation evidence shows ideas being converted into code surfaces that can be inspected, run, or traced by another technical reader.",
        ),
        (
            "validating_claims_through_records",
            "Validating claims through tests, manifests, metrics, or run records",
            ["validation_and_reliability", "measurement_and_evaluation"],
            "Validation and measurement evidence shows technical claims being surrounded by checks, benchmark context, manifests, or reproducibility records.",
        ),
        (
            "structuring_for_modification_and_review",
            "Structuring work for modification and review",
            ["maintainability", "system_design", "validation_and_reliability"],
            "Project structure, configuration, boundaries, and checks create surfaces for later modification and focused technical review.",
        ),
        (
            "packaging_for_technical_readers",
            "Packaging work for technical readers",
            ["product_packaging", "documentation_and_handoff"],
            "Packaging and documentation evidence frames the work for readers who need setup context, usage paths, and points to interrogate.",
        ),
    ]
    habits: list[dict[str, Any]] = []
    for habit_id, label, categories, description in group_specs:
        supporting = _signals_for_categories(signals, categories)
        if not supporting:
            continue
        habits.append(
            {
                "habit_id": habit_id,
                "label": label,
                "description": description,
                "supporting_signal_ids": _signal_ids(supporting),
                "evidence_ids": _evidence_for(supporting),
                "confidence": _confidence(supporting),
                "caveats": _synthesized_caveats(supporting),
            }
        )
    if not habits and signals:
        first_signal = signals[0]
        habits.append(
            {
                "habit_id": "bounded_public_repository_review",
                "label": "Working from bounded public repository evidence",
                "description": "The collected artifacts provide a narrow but inspectable basis for a technical conversation.",
                "supporting_signal_ids": [first_signal["signal_id"]],
                "evidence_ids": list(first_signal["evidence_ids"]),
                "confidence": first_signal["confidence"],
                "caveats": first_signal["caveats"],
            }
        )
    return habits


def _problem_solving_style(signals: list[dict[str, Any]]) -> dict[str, Any]:
    supporting = _signals_for_categories(
        signals,
        [
            "system_design",
            "experimentation_and_learning",
            "measurement_and_evaluation",
            "implementation_execution",
            "validation_and_reliability",
            "maintainability",
        ],
    ) or signals[:1]
    categories = {signal["category"] for signal in supporting}
    mechanisms: list[str] = []
    if "system_design" in categories:
        mechanisms.append("explicit boundaries")
    if "implementation_execution" in categories:
        mechanisms.append("runnable implementations")
    if categories & {"validation_and_reliability", "measurement_and_evaluation"}:
        mechanisms.append("checks, metrics, or reproducibility records")
    if "experimentation_and_learning" in categories:
        mechanisms.append("experiment or failure-analysis traces")
    mechanism_sentence = (
        f"Ambiguity is narrowed through {_list_phrase(mechanisms)}."
        if mechanisms
        else "Ambiguity is interpreted only through the bounded public artifacts available in the corpus."
    )
    iteration_sentence = (
        "Where exploratory artifacts are present, the work leaves assumptions, failure modes, or measurement context available for review rather than relying on broad unsupported claims."
        if categories & {"experimentation_and_learning", "measurement_and_evaluation", "validation_and_reliability"}
        else "The available public evidence is too narrow to make a strong claim about experimentation or iteration style."
    )
    summary = (
        "The reviewed work suggests a problem-solving style that turns uncertain technical spaces into bounded, inspectable systems. "
        f"{mechanism_sentence} {iteration_sentence} "
        "This supports a research-adjacent engineering profile: exploratory, but biased toward traceability and falsifiable evidence."
    )
    return {
        "summary": summary,
        "supporting_signal_ids": _signal_ids(supporting),
        "evidence_ids": _evidence_for(supporting),
        "confidence": _confidence(supporting),
        "caveats": (
            "Static repositories do not show live decision-making, WorkOverCV does not execute notebook artifacts, "
            "and public evidence cannot fully show collaboration or operational pressure."
        ),
    }


def _cadence_section(work_chronology: dict[str, Any], cadence_evidence: dict[str, Any]) -> dict[str, Any]:
    summary = _chronology_signal_summary(work_chronology)
    artifact = cadence_evidence.get("artifact_chronology", {}) if isinstance(cadence_evidence, dict) else {}
    commit_evidence_ids = cadence_evidence.get("commit_history_evidence_ids", []) if isinstance(cadence_evidence, dict) else []
    artifact_evidence_ids = artifact.get("evidence_ids", []) if isinstance(artifact, dict) else []
    return {
        "summary": (
            f"Commit-history evidence and artifact-chronology evidence are interpreted separately. "
            f"{summary['evidence_summary']} {artifact.get('description', 'Artifact chronology was not recorded.')}"
        ),
        "commit_history_signal": {
            "description": f"{summary['evidence_summary']} {summary['implication']}",
            "evidence_ids": commit_evidence_ids or [],
            "confidence": summary["confidence"],
            "caveats": summary["caveats"],
        },
        "artifact_chronology_signal": {
            "description": artifact.get("description") or "Artifact chronology was not recorded.",
            "evidence_ids": artifact_evidence_ids or [],
            "confidence": artifact.get("confidence") or "low",
            "caveats": artifact.get("caveats") or "Artifact chronology was unavailable in the collected inventory.",
        },
        "public_history_limitations": (
            "Public repositories may be curated snapshots of a larger work process. Commit counts, commit velocity, "
            "and shallow history are not treated as competence or productivity measures."
        ),
        "confidence": _confidence_from_levels([summary["confidence"], artifact.get("confidence") or "low"]),
        "caveats": (
            "Raw commit hashes, commit subjects, and raw timelines remain analysis input only. "
            "Dated artifact paths can suggest staged refinement but cannot prove the full work rhythm."
        ),
    }


def _environment_fit(signals: list[dict[str, Any]], gaps: list[dict[str, Any]]) -> dict[str, list[str]]:
    categories = {signal["category"] for signal in signals}
    may_fit = []
    if "measurement_and_evaluation" in categories:
        may_fit.append("Applied ML, evaluation-heavy, or measurement-oriented teams.")
    if "experimentation_and_learning" in categories:
        may_fit.append("Research-adjacent engineering or ambiguous technical problem spaces.")
    if "product_packaging" in categories or "documentation_and_handoff" in categories:
        may_fit.append("Tool-building contexts that value documentation, boundaries, and inspectability.")
    if "implementation_execution" in categories:
        may_fit.append("Engineering contexts where runnable artifacts and concrete implementation are important.")
    may_require_care = [
        "Roles where private/company work, live collaboration, or production operation history is essential should probe beyond public repositories."
    ]
    if gaps:
        may_require_care.append("Recorded evidence gaps should be handled as interview prompts, not adverse conclusions.")
    return {"may_fit_well": may_fit or ["Bounded technical roles where repository evidence can anchor discussion."], "may_require_care": may_require_care}


def _confidence_notes(
    signals: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    repo_count: int,
    artifact_count: int,
) -> dict[str, str]:
    confidence_counts = Counter(signal["confidence"] for signal in signals)
    return {
        "evidence_density": f"{artifact_count} artifact(s) and {len(signals)} behaviour signal(s) were selected for analysis.",
        "cross_repository_consistency": f"Signals are drawn from {repo_count} repository record(s); cross-repository confidence depends on how many repositories contain matching artifact types.",
        "authorship_bounds": "Authorship interpretation is bounded to collected public repository evidence and should be verified through discussion when it materially affects interpretation.",
        "public_repository_limitations": "GitHub evidence is a sample of public work, not a complete employment history.",
        "private_work_limitations": "Private and company work may be absent from the corpus and should be treated as unknown.",
        "confidence_summary": f"Signal confidence distribution: high={confidence_counts['high']}, medium={confidence_counts['medium']}, low={confidence_counts['low']}; evidence gaps recorded: {len(gaps)}.",
    }


def _repo_id_for_gap(
    related_signal_ids: list[str],
    signals: list[dict[str, Any]],
    evidence_by_id: dict[str, dict[str, Any]],
) -> str:
    for signal_id in related_signal_ids:
        signal = _signal_by_id(signals, signal_id)
        if not signal:
            continue
        for evidence_id in signal.get("evidence_ids", []) or []:
            evidence = evidence_by_id.get(evidence_id)
            if evidence and isinstance(evidence.get("repo_id"), str):
                return evidence["repo_id"]
    for evidence in evidence_by_id.values():
        if isinstance(evidence.get("repo_id"), str):
            return evidence["repo_id"]
    return "unknown"


def _first_signal_by_category(signals: list[dict[str, Any]], category: str) -> dict[str, Any] | None:
    for signal in signals:
        if signal.get("category") == category:
            return signal
    return None


def _all_signal_evidence_type(
    signal: dict[str, Any],
    evidence_by_id: dict[str, dict[str, Any]],
    evidence_type: str,
) -> bool:
    records = [
        evidence_by_id.get(evidence_id)
        for evidence_id in signal.get("evidence_ids", []) or []
        if isinstance(evidence_by_id.get(evidence_id), dict)
    ]
    return bool(records) and all(record.get("evidence_type") == evidence_type for record in records)


def _chronology_signal_summary(work_chronology: dict[str, Any]) -> dict[str, Any]:
    available_repo_count = _chronology_available_repo_count(work_chronology)
    total_commits = _chronology_commit_count(work_chronology)
    if available_repo_count == 0 or total_commits == 0:
        return {
            "available": False,
            "confidence": "low",
            "evidence_summary": "Readable git chronology was unavailable in the collected materialization.",
            "implication": "Public development cadence should be treated as unknown and discussed directly if it matters.",
            "confidence_reason": "No readable commit chronology was available for the selected repositories.",
            "caveats": "Cadence evidence is missing public data, not evidence of work speed or consistency.",
        }
    if total_commits <= available_repo_count:
        return {
            "available": True,
            "confidence": "low",
            "evidence_summary": f"Bounded chronology contains {total_commits} readable public commit record(s) across {available_repo_count} repository record(s).",
            "implication": "The public history may represent a curated snapshot rather than the whole work process, so commit cadence should be treated as low-confidence evidence.",
            "confidence_reason": "The collected chronology is too shallow for a confident rhythm pattern.",
            "caveats": "Do not equate shallow public history, commit count, or velocity with competence or productivity.",
        }
    confidence = "medium" if total_commits < 20 else "high"
    return {
        "available": True,
        "confidence": confidence,
        "evidence_summary": f"Bounded chronology contains {total_commits} readable public commit record(s) across {available_repo_count} repository record(s).",
        "implication": "This supports a bounded discussion of public work rhythm and iteration shape.",
        "confidence_reason": "Chronology is available across selected repositories but remains capped and public-only.",
        "caveats": "Raw commit hashes, messages, and timelines are analysis input only and are not rendered into the report.",
    }


def _chronology_available(work_chronology: dict[str, Any]) -> bool:
    return _chronology_available_repo_count(work_chronology) > 0 and _chronology_commit_count(work_chronology) > 0


def _chronology_is_shallow(work_chronology: dict[str, Any]) -> bool:
    available_repo_count = _chronology_available_repo_count(work_chronology)
    return available_repo_count == 0 or _chronology_commit_count(work_chronology) <= available_repo_count


def _chronology_available_repo_count(work_chronology: dict[str, Any]) -> int:
    repositories = work_chronology.get("repositories", [])
    if not isinstance(repositories, list):
        return 0
    return len(
        [
            repo
            for repo in repositories
            if isinstance(repo, dict) and repo.get("available") is True and int(repo.get("commit_count") or 0) > 0
        ]
    )


def _chronology_commit_count(work_chronology: dict[str, Any]) -> int:
    repositories = work_chronology.get("repositories", [])
    if not isinstance(repositories, list):
        return 0
    return sum(
        int(repo.get("commit_count") or 0)
        for repo in repositories
        if isinstance(repo, dict) and repo.get("available") is True
    )


def _signal_label_phrase(signals: list[dict[str, Any]]) -> str:
    labels = [_category_label(signal["category"]).lower() for signal in signals]
    labels = _unique(labels)
    if not labels:
        return "bounded repository evidence"
    if len(labels) == 1:
        return labels[0]
    if len(labels) == 2:
        return f"{labels[0]} and {labels[1]}"
    return f"{', '.join(labels[:-1])}, and {labels[-1]}"


def _category_label(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def _gaps_by_signal(gaps: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = {}
    for gap in gaps:
        for signal_id in gap.get("related_signal_ids", []) or []:
            output.setdefault(signal_id, []).append(gap)
    return output


def _signal_by_id(signals: list[dict[str, Any]], signal_id: str) -> dict[str, Any] | None:
    for signal in signals:
        if signal.get("signal_id") == signal_id:
            return signal
    return None


def _signals_by_category(signals: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = {}
    for signal in signals:
        category = signal.get("category")
        if isinstance(category, str):
            output.setdefault(category, []).append(signal)
    return output


def _finding(
    finding_id: str,
    section: str,
    title: str,
    text: str,
    basis: str,
    confidence: str,
    evidence_ids: list[str],
    signal_ids: list[str],
    gap_ids: list[str],
) -> dict[str, Any]:
    return {
        "finding_id": finding_id,
        "section": section,
        "title": title,
        "text": text,
        "basis": basis,
        "confidence": confidence,
        "supporting_evidence_ids": evidence_ids,
        "related_signal_ids": signal_ids,
        "related_gap_ids": gap_ids,
    }


def _confidence(signals: list[dict[str, Any]]) -> str:
    levels = [signal["confidence"] for signal in signals]
    if "low" in levels:
        return "low"
    if "medium" in levels:
        return "medium"
    return "high"


def _confidence_from_levels(levels: Iterable[Any]) -> str:
    normalized = [level for level in levels if level in {"low", "medium", "high"}]
    if not normalized:
        return "low"
    if "medium" in normalized:
        return "medium"
    if "high" in normalized:
        return "high"
    return "low"


def _signal_ids(signals: list[dict[str, Any]]) -> list[str]:
    return [signal["signal_id"] for signal in signals]


def _evidence_for(signals: list[dict[str, Any]]) -> list[str]:
    return _unique(evidence_id for signal in signals for evidence_id in signal["evidence_ids"])


def _signals_for_categories(signals: list[dict[str, Any]], categories: list[str]) -> list[dict[str, Any]]:
    category_set = set(categories)
    return [signal for signal in signals if signal.get("category") in category_set]


def _synthesized_caveats(signals: list[dict[str, Any]]) -> str:
    caveats = _unique(signal["caveats"] for signal in signals if signal.get("caveats"))
    if not caveats:
        return "Interpret this habit within the limits of the collected public repository evidence."
    return " ".join(caveats[:2])


def _follow_up_for_category(category: str) -> str:
    return {
        "testing_and_reliability": "Ask for the test strategy, CI expectations, or reliability checks used outside the collected corpus.",
        "collaboration_or_handoff": "Ask for an example of reviewed team work, handoff notes, or pull request discussion.",
    }.get(category, f"Ask for additional evidence about {category}.")


def _list_phrase(values: Iterable[str]) -> str:
    items = [value for value in values if value]
    if not items:
        return "not recorded"
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def _unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            output.append(value)
    return output
