from __future__ import annotations

from pathlib import Path
from typing import Any

from . import __version__
from .constants import TOOL_NAME, WORKFLOW_ID, WORKFLOW_VERSION
from .io import read_json, utc_now_iso, write_json


def update_run_manifest(
    run_dir: Path,
    *,
    command: str,
    config: dict[str, Any] | None = None,
    warnings: list[str] | None = None,
    status: str = "partial",
) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "run_manifest.json"
    if manifest_path.exists():
        manifest = read_json(manifest_path)
    else:
        manifest = {
            "tool_name": TOOL_NAME,
            "tool_version": __version__,
            "workflow_id": WORKFLOW_ID,
            "workflow_version": WORKFLOW_VERSION,
            "created_at": utc_now_iso(),
            "command_history": [],
            "warnings": [],
        }

    command_entry = {
        "command": command,
        "completed_at": utc_now_iso(),
        "config": config or {},
    }
    manifest.setdefault("command_history", []).append(command_entry)
    manifest["updated_at"] = utc_now_iso()
    manifest["status"] = status
    manifest["output_dir"] = str(run_dir)

    if warnings:
        existing = manifest.setdefault("warnings", [])
        for warning in warnings:
            if warning not in existing:
                existing.append(warning)

    artifact_names = {path.name for path in run_dir.iterdir() if path.is_file()}
    artifact_names.add("run_manifest.json")
    manifest["artifacts"] = sorted(artifact_names)
    write_json(manifest_path, manifest)
    return manifest
