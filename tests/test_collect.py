from __future__ import annotations

import json
from pathlib import Path

import workovercv.collect as collect_module
from workovercv.collect import classify_artifact, collect_from_scope
from workovercv.manifest import write_review_scope


def test_classify_artifact_types() -> None:
    assert classify_artifact("README.md") == "README"
    assert classify_artifact("README") == "README"
    assert classify_artifact("01_rb_synthetic-data_3/Assets/Readme.asset") == "configuration_file"
    assert classify_artifact("01_rb_synthetic-data_3/Assets/Readme.asset.meta") == "configuration_file"
    assert classify_artifact(".github/workflows/ci.yml") == "CI_workflow"
    assert classify_artifact("docs/architecture.md") == "architecture_document"
    assert classify_artifact("docs/manifest_contract.md") == "technical_writeup"
    assert classify_artifact("tests/test_app.py") == "test_file"
    assert classify_artifact("tests/fixtures/small_repo/input_manifest.yml") == "data_manifest"
    assert classify_artifact("tests/fixtures/small_repo/docs/technical_notes.md") == "technical_writeup"
    assert classify_artifact("src/train_model.py") == "training_script"
    assert classify_artifact("models/20260319/training_history.json") == "data_manifest"
    assert classify_artifact("documents/inference_v0_4_ts_integration_plan.md") == "technical_writeup"
    assert classify_artifact("notebooks/train_model.ipynb") == "notebook_source"
    assert classify_artifact("requirements.txt") == "configuration_file"
    assert classify_artifact("requirements-test.txt") == "configuration_file"
    assert classify_artifact("package-lock.json") == "configuration_file"
    assert classify_artifact("01_rb_synthetic-data_3/Packages/manifest.json") == "configuration_file"
    assert classify_artifact("schemas/run_manifest.schema.json") == "configuration_file"
    assert classify_artifact("models/run_manifest.json") == "run_manifest"
    assert classify_artifact("environment.yml") == "configuration_file"
    assert classify_artifact("COPYRIGHT.md") == "technical_writeup"
    assert classify_artifact("THIRD_PARTY_NOTICES.md") == "technical_writeup"
    assert classify_artifact("notes.txt") == "technical_writeup"


def test_collect_downranks_low_signal_metadata_and_legal_docs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "Assets").mkdir(parents=True)
    (repo / "Packages").mkdir()
    (repo / "schemas").mkdir()
    (repo / "docs").mkdir()
    (repo / "models").mkdir()
    repo.joinpath("README.md").write_text("# Project\n\nUsable overview.", encoding="utf-8")
    repo.joinpath("COPYRIGHT.md").write_text("# Copyright\n\nLegal notice.", encoding="utf-8")
    repo.joinpath("THIRD_PARTY_NOTICES.md").write_text("# Notices\n\nDependency notices.", encoding="utf-8")
    repo.joinpath("Assets", "Readme.asset").write_text("%YAML 1.1\nasset metadata", encoding="utf-8")
    repo.joinpath("Packages", "manifest.json").write_text('{"dependencies": {}}', encoding="utf-8")
    repo.joinpath("schemas", "run_manifest.schema.json").write_text('{"type": "object"}', encoding="utf-8")
    repo.joinpath("docs", "manifest_contract.md").write_text("# Manifest Contract\n\nWorkflow docs.", encoding="utf-8")
    repo.joinpath("models", "run_manifest.json").write_text('{"run_id": "run1"}', encoding="utf-8")

    scope_path = tmp_path / "review_scope.yml"
    write_review_scope(
        scope_path,
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "repositories": [
                {
                    "repo_id": "example-noisy",
                    "name": "noisy",
                    "url": "https://github.com/example/noisy",
                    "local_path": str(repo),
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                }
            ],
        },
    )

    run_dir = collect_from_scope(scope_path, work_root=tmp_path / "work")

    inventory = json.loads((run_dir / "artifact_inventory.json").read_text(encoding="utf-8"))
    by_path = {artifact["path"]: artifact for artifact in inventory["artifacts"]}
    assert "Assets/Readme.asset" not in by_path
    assert by_path["README.md"]["artifact_type"] == "README"
    assert by_path["README.md"]["likely_signal_value"] == "high"
    assert by_path["COPYRIGHT.md"]["artifact_type"] == "technical_writeup"
    assert by_path["COPYRIGHT.md"]["likely_signal_value"] == "low"
    assert by_path["THIRD_PARTY_NOTICES.md"]["likely_signal_value"] == "low"
    assert by_path["Packages/manifest.json"]["artifact_type"] == "configuration_file"
    assert by_path["Packages/manifest.json"]["likely_signal_value"] == "low"
    assert by_path["schemas/run_manifest.schema.json"]["artifact_type"] == "configuration_file"
    assert by_path["docs/manifest_contract.md"]["artifact_type"] == "technical_writeup"
    assert by_path["models/run_manifest.json"]["artifact_type"] == "run_manifest"
    assert by_path["models/run_manifest.json"]["likely_signal_value"] == "low"


def test_collect_from_scope_writes_artifacts_and_corpus(tmp_path: Path) -> None:
    fixture = Path("tests/fixtures/small_repo").resolve()
    scope_path = tmp_path / "review_scope.yml"
    write_review_scope(
        scope_path,
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "repositories": [
                {
                    "repo_id": "example-small",
                    "name": "small",
                    "url": "https://github.com/example/small",
                    "local_path": str(fixture),
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                },
                {
                    "repo_id": "example-skip",
                    "name": "skip",
                    "url": "https://github.com/example/skip",
                    "local_path": str(tmp_path / "missing"),
                    "selected_for_review": False,
                    "selection_reason": "not selected",
                },
            ],
        },
    )

    run_dir = collect_from_scope(scope_path, work_root=tmp_path / "work")

    inventory = json.loads((run_dir / "artifact_inventory.json").read_text(encoding="utf-8"))
    corpus_lines = (run_dir / "review_corpus.jsonl").read_text(encoding="utf-8").splitlines()

    paths = {artifact["path"] for artifact in inventory["artifacts"]}
    types = {artifact["artifact_type"] for artifact in inventory["artifacts"]}
    assert "README.md" in paths
    assert "docs/architecture.md" in paths
    assert "README" in types
    assert "CI_workflow" in types
    assert "test_file" in types
    assert corpus_lines
    assert "example-skip" not in (run_dir / "review_corpus.jsonl").read_text(encoding="utf-8")
    assert (run_dir / "materialization.json").exists()
    chronology = json.loads((run_dir / "work_chronology.json").read_text(encoding="utf-8"))
    assert chronology["max_commits_per_repository"] == 50
    assert chronology["repositories"][0]["repo_id"] == "example-small"
    assert chronology["repositories"][0]["available"] is False


def test_collect_writes_outputs_when_cleanup_fails(tmp_path: Path, monkeypatch) -> None:
    fixture = Path("tests/fixtures/small_repo").resolve()
    scope_path = tmp_path / "review_scope.yml"
    write_review_scope(
        scope_path,
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "repositories": [
                {
                    "repo_id": "example-small",
                    "name": "small",
                    "url": "https://github.com/example/small",
                    "clone_url": "https://github.com/example/small.git",
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                }
            ],
        },
    )

    def fake_materialize(_repo: dict, _work_root: Path) -> tuple[Path, bool]:
        return fixture, True

    def fail_cleanup(_path: Path, _root: Path) -> None:
        raise PermissionError("locked test worktree")

    monkeypatch.setattr(collect_module, "_materialize_repository", fake_materialize)
    monkeypatch.setattr(collect_module, "_remove_tree_inside", fail_cleanup)

    run_dir = collect_module.collect_from_scope(scope_path, work_root=tmp_path / "work")

    assert (run_dir / "artifact_inventory.json").exists()
    assert (run_dir / "review_corpus.jsonl").exists()
    assert (run_dir / "work_chronology.json").exists()
    assert (run_dir / "materialization.json").exists()
    manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
    assert any("Could not clean up worktree" in warning for warning in manifest["warnings"])


def test_collect_notebook_source_only_strips_outputs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    notebook = {
        "metadata": {"kernelspec": {"name": "python3"}, "secret": "METADATA_SHOULD_NOT_APPEAR"},
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {"tags": ["hide"]},
                "source": ["# Experiment plan\n", "Evaluate preprocessing choices."],
            },
            {
                "cell_type": "code",
                "execution_count": 7,
                "metadata": {"trusted": True},
                "source": ["def build_features(x):\n", "    return x * 2\n"],
                "outputs": [
                    {
                        "output_type": "stream",
                        "name": "stdout",
                        "text": "OUTPUT_SHOULD_NOT_APPEAR\n",
                    },
                    {
                        "output_type": "display_data",
                        "data": {"image/png": "IMAGE_SHOULD_NOT_APPEAR"},
                    },
                ],
            },
        ],
    }
    (repo / "analysis.ipynb").write_text(json.dumps(notebook), encoding="utf-8")
    scope_path = tmp_path / "review_scope.yml"
    write_review_scope(
        scope_path,
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "repositories": [
                {
                    "repo_id": "example-notebook",
                    "name": "notebook",
                    "url": "https://github.com/example/notebook",
                    "local_path": str(repo),
                    "selected_for_review": True,
                    "selection_reason": "fixture",
                }
            ],
        },
    )

    run_dir = collect_from_scope(scope_path, work_root=tmp_path / "work")

    inventory = json.loads((run_dir / "artifact_inventory.json").read_text(encoding="utf-8"))
    artifact = inventory["artifacts"][0]
    corpus_text = "\n".join(
        json.loads(line)["text"] for line in (run_dir / "review_corpus.jsonl").read_text(encoding="utf-8").splitlines()
    )

    assert artifact["path"] == "analysis.ipynb"
    assert artifact["artifact_type"] == "notebook_source"
    assert "source-only projection" in artifact["notes"]
    assert "# Cell 1 [markdown]" in corpus_text
    assert "# Experiment plan" in corpus_text
    assert "# Cell 2 [code]" in corpus_text
    assert "def build_features" in corpus_text
    assert "OUTPUT_SHOULD_NOT_APPEAR" not in corpus_text
    assert "IMAGE_SHOULD_NOT_APPEAR" not in corpus_text
    assert "METADATA_SHOULD_NOT_APPEAR" not in corpus_text
    assert "execution_count" not in corpus_text
