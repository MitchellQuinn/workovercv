from __future__ import annotations

from pathlib import Path

from .constants import ANALYSIS_ARTIFACTS, EVIDENCE_BOUNDARY_ARTIFACTS
from .rubric import build_deterministic_assessment
from .run_manifest import update_run_manifest


def analyze_run(run_dir: Path, *, command: str = "analyze") -> Path:
    run_dir = run_dir.resolve()
    build_deterministic_assessment(run_dir)
    update_run_manifest(
        run_dir,
        command=command,
        config={
            "run": str(run_dir),
            "analysis_mode": "deterministic_rubric",
            "generated_artifacts": _existing_artifacts(run_dir, ANALYSIS_ARTIFACTS),
            "evidence_boundary": _existing_artifacts(run_dir, EVIDENCE_BOUNDARY_ARTIFACTS),
        },
        status="partial",
    )
    return run_dir


def _existing_artifacts(run_dir: Path, artifact_names: list[str]) -> list[str]:
    return [artifact_name for artifact_name in artifact_names if (run_dir / artifact_name).exists()]
