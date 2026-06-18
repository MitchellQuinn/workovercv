from __future__ import annotations

import json
from pathlib import Path

from workovercv.run_manifest import update_run_manifest


def test_update_run_manifest_preserves_command_history(tmp_path: Path) -> None:
    (tmp_path / "repo_inventory.json").write_text("{}", encoding="utf-8")

    update_run_manifest(tmp_path, command="discover", config={"candidate": "https://github.com/example"})
    update_run_manifest(tmp_path, command="collect", config={"scope": "review_scope.yml"})

    manifest = json.loads((tmp_path / "run_manifest.json").read_text(encoding="utf-8"))

    assert manifest["tool_name"] == "workovercv"
    assert manifest["workflow_id"] == "workovercv.repository-employment-signal"
    assert manifest["workflow_version"] == "0.6.0"
    assert [entry["command"] for entry in manifest["command_history"]] == ["discover", "collect"]
    assert "repo_inventory.json" in manifest["artifacts"]
    assert "run_manifest.json" in manifest["artifacts"]
