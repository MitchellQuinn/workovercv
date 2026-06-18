from __future__ import annotations

from pathlib import Path

from .analysis import analyze_run
from .collect import collect_from_scope
from .io import safe_slug, utc_now_iso, utc_timestamp, write_json
from .manifest import write_review_scope
from .render import ReportMode, render_report
from .run_manifest import update_run_manifest
from .validation import validate_run


def scan_local_path(path: Path, out_root: Path, *, report_mode: ReportMode = "audit") -> Path:
    repo_path = path.expanduser().resolve()
    if not repo_path.exists() or not repo_path.is_dir():
        raise RuntimeError(f"scan path does not exist or is not a directory: {repo_path}")

    repo_name = repo_path.name or "local-repo"
    repo_id = safe_slug(f"local-{repo_name}")
    timestamp = utc_timestamp()
    run_dir = out_root / f"{safe_slug(repo_name)}-{timestamp}"
    counter = 2
    while run_dir.exists():
        run_dir = out_root / f"{safe_slug(repo_name)}-{timestamp}-{counter}"
        counter += 1
    run_dir.mkdir(parents=True, exist_ok=False)

    candidate = {
        "type": "local_path",
        "url": repo_path.as_uri(),
        "username": safe_slug(repo_name),
        "path": str(repo_path),
    }
    repo_record = {
        "repo_id": repo_id,
        "name": repo_name,
        "url": repo_path.as_uri(),
        "local_path": str(repo_path),
        "visibility": "local",
        "selected_for_review": True,
        "selection_reason": "local scan path",
    }
    write_json(
        run_dir / "repo_inventory.json",
        {
            "candidate": candidate,
            "generated_at": utc_now_iso(),
            "source": {"type": "local_path", "path": str(repo_path)},
            "repositories": [repo_record],
        },
    )
    write_review_scope(
        run_dir / "review_scope.yml",
        {
            "candidate": candidate,
            "generated_at": utc_now_iso(),
            "source_inventory": "repo_inventory.json",
            "repositories": [
                {
                    "repo_id": repo_id,
                    "name": repo_name,
                    "url": repo_path.as_uri(),
                    "local_path": str(repo_path),
                    "selected_for_review": True,
                    "selection_reason": "local scan path",
                }
            ],
        },
    )
    update_run_manifest(run_dir, command="scan:init", config={"path": str(repo_path), "out": str(out_root)}, status="partial")
    collect_from_scope(run_dir / "review_scope.yml", work_root=run_dir / "worktrees")
    analyze_run(run_dir, command="scan:analyze")
    render_report(run_dir, mode=report_mode)
    result = validate_run(run_dir)
    if not result.ok:
        raise RuntimeError("scan validation failed: " + "; ".join(result.errors))
    return run_dir
