from __future__ import annotations

import json
from pathlib import Path

from workovercv.io import write_json
from workovercv.rubric import build_deterministic_assessment


def test_deterministic_assessment_prefers_stronger_evidence_artifacts(tmp_path: Path) -> None:
    _write_ranked_artifact_run(tmp_path)

    build_deterministic_assessment(tmp_path)

    evidence = [
        json.loads(line)
        for line in (tmp_path / "evidence_map.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    signals = [
        json.loads(line)
        for line in (tmp_path / "signal_ledger.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    evidence_by_id = {record["evidence_id"]: record for record in evidence}
    signal_by_category = {record["category"]: record for record in signals}

    documentation_paths = _paths_for_signal(signal_by_category["documentation_and_handoff"], evidence_by_id)
    assert documentation_paths[0] == "README.md"
    assert "docs/architecture.md" in documentation_paths

    implementation_paths = _paths_for_signal(signal_by_category["implementation_execution"], evidence_by_id)
    assert implementation_paths == ["src/example/cli.py"]
    assert "src/example/__init__.py" not in implementation_paths

    testing_paths = _paths_for_signal(signal_by_category["validation_and_reliability"], evidence_by_id)
    assert testing_paths == ["tests/test_cli.py"]
    assert "tests/fixtures/small_repo/input_manifest.yml" not in testing_paths

    maintainability_paths = _paths_for_signal(signal_by_category["maintainability"], evidence_by_id)
    assert "src/example/cli.py" in maintainability_paths

    architecture_paths = _paths_for_signal(signal_by_category["system_design"], evidence_by_id)
    assert "docs/architecture.md" in architecture_paths
    assert "Packages/manifest.json" not in architecture_paths

    product_paths = _paths_for_signal(signal_by_category["product_packaging"], evidence_by_id)
    assert "failure-analysis/incidents/incident-001/README.md" not in product_paths

    assert "development_cadence" not in signal_by_category
    assert "authorship_bounds" not in signal_by_category
    cadence = report["work_rhythm_and_development_cadence"]
    cadence_evidence = [evidence_by_id[evidence_id] for evidence_id in cadence["commit_history_signal"]["evidence_ids"]]
    assert cadence_evidence[0]["evidence_type"] == "absence"
    assert cadence_evidence[0]["locator"] == {"type": "inventory", "value": "work_chronology.json"}
    assert cadence_evidence[0]["artifact_id"] == "run-artifact-work-chronology"
    assert cadence_evidence[0]["path"] == "work_chronology.json"
    assert "raw commit hashes and subjects" in cadence_evidence[0]["notes"]

    artifact_inventory = json.loads((tmp_path / "artifact_inventory.json").read_text(encoding="utf-8"))
    inventory_summary = [
        artifact
        for artifact in artifact_inventory["artifacts"]
        if artifact["artifact_id"] == "run-artifact-inventory-summary"
    ]
    assert inventory_summary[0]["repo_id"] in {"example-api", "example-design", "example-docs", "example-repo", "example-research"}
    assert inventory_summary == [
        {
            "artifact_id": "run-artifact-inventory-summary",
            "repo_id": inventory_summary[0]["repo_id"],
            "path": "artifact_inventory.json",
            "artifact_type": "inventory_summary",
            "size_bytes": inventory_summary[0]["size_bytes"],
            "size_estimate": "small",
            "likely_signal_value": "medium",
            "notes": "Synthetic run-boundary artifact used to anchor inventory-level absence evidence across the collected artifact inventory.",
        }
    ]
    chronology_summary = [
        artifact
        for artifact in artifact_inventory["artifacts"]
        if artifact["artifact_id"] == "run-artifact-work-chronology"
    ]
    assert chronology_summary[0]["artifact_type"] == "work_chronology"

    assert "evidence bundle" in signal_by_category["documentation_and_handoff"]["evidence_summary"]
    assert signal_by_category["implementation_execution"]["confidence"] == "low"
    assert all(len(signal["evidence_ids"]) <= 5 for signal in signals)
    assert len(signal_by_category["documentation_and_handoff"]["evidence_ids"]) >= 2
    assert report["title"] == "Work Behaviour Profile Report"
    assert report["analysis_model_information"] == "Deterministic WorkOverCV rubric analysis; no LLM model used."
    assert "findings" not in report
    assert "Observed Work Behaviour Signals" not in json.dumps(report)
    assert any(signal["label"] == "Makes technical work inspectable for reviewers" for signal in signals)
    assert "observable work pattern is:" not in report["executive_work_profile"]
    assert "Makes technical work inspectable for reviewers, Externalises system boundaries" not in report["executive_work_profile"]
    assert "; and to " not in report["executive_work_profile"]
    assert "systems-oriented work made reviewable" in report["executive_work_profile"]
    assert "Public evidence remains weaker" in report["executive_work_profile"]
    signal_implications = {signal["implication"] for signal in signals}
    assert all(habit["description"] not in signal_implications for habit in report["engineering_habits"])
    assert "problem-solving style" in report["problem_solving_style"]["summary"]
    assert "research-adjacent engineering profile" in report["problem_solving_style"]["summary"]
    assert "ambiguous_problem_handling" not in json.dumps(report["problem_solving_style"])
    assert all(entry.get("likely_contribution") for entry in report["role_family_fit"])
    role_names = [entry["role_family"] for entry in report["role_family_fit"]]
    assert "AI Engineer" not in role_names
    role_text = json.dumps(report["role_family_fit"])
    assert "relevant behaviours connect" not in role_text
    if any(entry["role_family"] == "Software Engineer" for entry in report["role_family_fit"]):
        assert "implementation that is packaged with setup context" in role_text
    if any(entry["role_family"] == "Developer Tools Engineer" for entry in report["role_family_fit"]):
        assert "tool-shaped work" in role_text
    assert "low velocity" not in json.dumps(report).lower()


def test_artifact_chronology_supports_iteration_independent_of_commit_count(tmp_path: Path) -> None:
    _write_artifact_chronology_run(tmp_path)

    build_deterministic_assessment(tmp_path)

    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    signals = [
        json.loads(line)
        for line in (tmp_path / "signal_ledger.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    evidence = [
        json.loads(line)
        for line in (tmp_path / "evidence_map.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    evidence_by_id = {record["evidence_id"]: record for record in evidence}
    categories = {signal["category"] for signal in signals}
    signal_by_id = {signal["signal_id"]: signal for signal in signals}
    cadence = report["work_rhythm_and_development_cadence"]
    artifact_evidence = [
        evidence_by_id[evidence_id]
        for evidence_id in cadence["artifact_chronology_signal"]["evidence_ids"]
    ]

    assert "development_cadence" not in categories
    assert "authorship_bounds" not in categories
    assert cadence["commit_history_signal"]["confidence"] == "low"
    assert "curated snapshot" in cadence["commit_history_signal"]["description"]
    assert cadence["artifact_chronology_signal"]["confidence"] == "medium"
    assert "independent of commit count" in cadence["artifact_chronology_signal"]["description"]
    assert "staged iteration" in cadence["artifact_chronology_signal"]["description"]
    assert "benchmark progression" in cadence["artifact_chronology_signal"]["description"]
    assert artifact_evidence[0]["path"] == "models/20260319/training_history.json"
    role_names = [entry["role_family"] for entry in report["role_family_fit"]]
    assert "AI Engineer" in role_names
    assert role_names.index("AI Engineer") < role_names.index("Applied ML Engineer")
    ai_engineer = next(entry for entry in report["role_family_fit"] if entry["role_family"] == "AI Engineer")
    ai_supporting_categories = {
        signal_by_id[signal_id]["category"]
        for signal_id in ai_engineer["supporting_signal_ids"]
    }
    assert "implementation_execution" in ai_supporting_categories
    assert ai_supporting_categories & {"measurement_and_evaluation", "experimentation_and_learning"}
    assert "AI-adjacent systems" in ai_engineer["likely_contribution"]
    assert "weak work rhythm" not in json.dumps(report).lower()


def test_artifact_chronology_does_not_rely_on_staged_paths_alone(tmp_path: Path) -> None:
    _write_staged_path_only_run(tmp_path)

    build_deterministic_assessment(tmp_path)

    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    cadence = report["work_rhythm_and_development_cadence"]

    assert cadence["commit_history_signal"]["confidence"] == "low"
    assert cadence["artifact_chronology_signal"]["confidence"] == "low"
    assert "No dated or staged model, manifest, metric, benchmark, or failure-analysis artifacts" in cadence["artifact_chronology_signal"]["description"]
    assert "staged iteration" not in cadence["artifact_chronology_signal"]["description"]


def _paths_for_signal(signal: dict, evidence_by_id: dict[str, dict]) -> list[str]:
    return [evidence_by_id[evidence_id]["path"] for evidence_id in signal["evidence_ids"]]


def _write_ranked_artifact_run(run_dir: Path) -> None:
    write_json(
        run_dir / "repo_inventory.json",
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "generated_at": "2026-06-17T00:00:00Z",
            "repositories": [
                {
                    "repo_id": "example-repo",
                    "name": "repo",
                    "url": "https://github.com/example/repo",
                    "visibility": "public",
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                },
                {
                    "repo_id": "example-docs",
                    "name": "docs",
                    "url": "https://github.com/example/docs",
                    "visibility": "public",
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                },
                {
                    "repo_id": "example-design",
                    "name": "design",
                    "url": "https://github.com/example/design",
                    "visibility": "public",
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                },
                {
                    "repo_id": "example-api",
                    "name": "api",
                    "url": "https://github.com/example/api",
                    "visibility": "public",
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                },
                {
                    "repo_id": "example-research",
                    "name": "research",
                    "url": "https://github.com/example/research",
                    "visibility": "public",
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                },
            ],
        },
    )
    write_json(
        run_dir / "artifact_inventory.json",
        {
            "generated_at": "2026-06-17T00:00:00Z",
            "artifacts": [
                _artifact("art-adapter-readme", "adapters/codex/README.md", "README", 400),
                _artifact("art-root-readme", "README.md", "README", 400),
                _artifact("art-docs-handbook", "docs/handbook.md", "technical_writeup", 800, repo_id="example-docs"),
                _artifact("art-design", "docs/design.md", "architecture_document", 800, repo_id="example-design"),
                _artifact("art-api-guide", "docs/api-guide.md", "technical_writeup", 800, repo_id="example-api"),
                _artifact("art-research-readme", "research/README.md", "README", 800, repo_id="example-research"),
                _artifact("art-init", "src/example/__init__.py", "source_code", 1),
                _artifact("art-cli", "src/example/cli.py", "source_code", 800),
                _artifact("art-fixture-test", "tests/fixtures/small_repo/input_manifest.yml", "test_file", 400),
                _artifact("art-real-test", "tests/test_cli.py", "test_file", 800),
                _artifact("art-architecture", "docs/architecture.md", "architecture_document", 800),
                _artifact("art-package-manifest", "Packages/manifest.json", "configuration_file", 800),
                _artifact("art-incident-readme", "failure-analysis/incidents/incident-001/README.md", "README", 800),
            ],
        },
    )


def _write_artifact_chronology_run(run_dir: Path) -> None:
    write_json(
        run_dir / "repo_inventory.json",
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "generated_at": "2026-06-17T00:00:00Z",
            "repositories": [
                {
                    "repo_id": "example-ml",
                    "name": "ml",
                    "url": "https://github.com/example/ml",
                    "visibility": "public",
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
                _artifact("art-readme", "README.md", "README", 600, repo_id="example-ml"),
                _artifact("art-cli", "src/train_model.py", "training_script", 900, repo_id="example-ml"),
                _artifact("art-history", "models/20260319/training_history.json", "data_manifest", 900, repo_id="example-ml"),
                _artifact("art-model-card", "models/v0.2/model_card.md", "model_card", 900, repo_id="example-ml"),
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
                    "repo_id": "example-ml",
                    "available": True,
                    "default_branch": "main",
                    "commit_count": 1,
                    "first_commit_at": "2026-06-01T00:00:00Z",
                    "last_commit_at": "2026-06-01T00:00:00Z",
                    "entries": [
                        {
                            "commit_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "committed_at": "2026-06-01T00:00:00Z",
                            "subject": "Initial public snapshot",
                        }
                    ],
                }
            ],
        },
    )


def _write_staged_path_only_run(run_dir: Path) -> None:
    write_json(
        run_dir / "repo_inventory.json",
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "generated_at": "2026-06-17T00:00:00Z",
            "repositories": [
                {
                    "repo_id": "example-staged",
                    "name": "staged",
                    "url": "https://github.com/example/staged",
                    "visibility": "public",
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
                _artifact("art-readme", "README.md", "README", 600, repo_id="example-staged"),
                _artifact("art-script", "experiments/v0.2/train.py", "training_script", 900, repo_id="example-staged"),
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
                    "repo_id": "example-staged",
                    "available": True,
                    "default_branch": "main",
                    "commit_count": 1,
                    "first_commit_at": "2026-06-01T00:00:00Z",
                    "last_commit_at": "2026-06-01T00:00:00Z",
                    "entries": [
                        {
                            "commit_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "committed_at": "2026-06-01T00:00:00Z",
                            "subject": "Initial public snapshot",
                        }
                    ],
                }
            ],
        },
    )


def _artifact(artifact_id: str, path: str, artifact_type: str, size_bytes: int, *, repo_id: str = "example-repo") -> dict:
    return {
        "artifact_id": artifact_id,
        "repo_id": repo_id,
        "path": path,
        "artifact_type": artifact_type,
        "size_bytes": size_bytes,
        "size_estimate": "small",
        "likely_signal_value": "high",
    }
