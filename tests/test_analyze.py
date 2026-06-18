from __future__ import annotations

import json
from pathlib import Path

from workovercv.cli import main
from workovercv.collect import collect_from_scope
from workovercv.io import write_json
from workovercv.manifest import write_review_scope


def test_analyze_command_writes_artifacts_and_manifest_provenance(tmp_path: Path) -> None:
    run_dir = _write_collected_fixture_run(tmp_path)

    exit_code = main(["analyze", "--run", str(run_dir)])

    assert exit_code == 0
    assert (run_dir / "report.json").exists()
    assert (run_dir / "signal_ledger.jsonl").exists()
    assert (run_dir / "role_family_fit.json").exists()
    report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
    assert report["title"] == "Work Behaviour Profile Report"
    assert "observed_work_behaviour_signals" in report
    assert "findings" not in report
    manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
    analyze_entry = manifest["command_history"][-1]
    assert analyze_entry["command"] == "analyze"
    assert analyze_entry["config"]["analysis_mode"] == "deterministic_rubric"
    assert "report.json" in analyze_entry["config"]["generated_artifacts"]
    assert analyze_entry["config"]["evidence_boundary"] == [
        "review_scope.yml",
        "repo_inventory.json",
        "artifact_inventory.json",
        "review_corpus.jsonl",
        "work_chronology.json",
    ]

    assert main(["analyze", "--run", str(run_dir)]) == 0
    inventory = json.loads((run_dir / "artifact_inventory.json").read_text(encoding="utf-8"))
    inventory_summaries = [
        artifact
        for artifact in inventory["artifacts"]
        if artifact["artifact_id"] == "run-artifact-inventory-summary"
    ]
    assert len(inventory_summaries) == 1
    chronology_artifacts = [
        artifact
        for artifact in inventory["artifacts"]
        if artifact["artifact_id"] == "run-artifact-work-chronology"
    ]
    assert len(chronology_artifacts) == 1


def _write_collected_fixture_run(tmp_path: Path) -> Path:
    fixture = Path("tests/fixtures/small_repo").resolve()
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    scope = {
        "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
        "repositories": [
            {
                "repo_id": "example-small",
                "name": "small",
                "url": "https://github.com/example/small",
                "local_path": str(fixture),
                "selected_for_review": True,
                "selection_reason": "fixture",
            }
        ],
    }
    write_json(
        run_dir / "repo_inventory.json",
        {
            "candidate": scope["candidate"],
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
    write_review_scope(run_dir / "review_scope.yml", scope)
    collect_from_scope(run_dir / "review_scope.yml", work_root=tmp_path / "work")
    return run_dir
