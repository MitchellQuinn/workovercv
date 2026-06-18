from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import stat
from pathlib import Path
from typing import Any

from .io import relative_to_or_self, safe_slug, utc_now_iso, write_json, write_jsonl
from .manifest import load_review_scope, selected_repositories
from .run_manifest import update_run_manifest

TEXT_EXTENSIONS = {
    ".cfg",
    ".css",
    ".ini",
    ".ipynb",
    ".js",
    ".json",
    ".jsx",
    ".lock",
    ".md",
    ".py",
    ".rst",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

SOURCE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".rs", ".go", ".java", ".cs", ".cpp", ".c", ".h"}
SCRIPT_EXTENSIONS = SOURCE_EXTENSIONS | {".sh", ".ps1"}
STRUCTURED_EXTENSIONS = {".json", ".toml", ".yaml", ".yml", ".ini", ".cfg"}
EXCLUDED_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules", "dist", "build", "vendor"}
MAX_TEXT_ARTIFACT_BYTES = 200_000
MAX_NOTEBOOK_ARTIFACT_BYTES = 2_000_000
MAX_CHRONOLOGY_COMMITS = 50
CONFIG_FILE_NAMES = {
    ".python-version",
    "constraints.txt",
    "dev-requirements.txt",
    "environment.yml",
    "environment.yaml",
    "package-lock.json",
    "package.json",
    "packages-lock.json",
    "pipfile",
    "pipfile.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "pyproject.toml",
    "requirements-dev.txt",
    "requirements_dev.txt",
    "requirements-test.txt",
    "requirements_test.txt",
    "requirements.txt",
    "setup.cfg",
    "setup.py",
    "yarn.lock",
}
LOW_SIGNAL_DOC_NAMES = {
    "copyright.md",
    "license",
    "license.md",
    "notice",
    "notice.md",
    "notices.md",
    "third_party.md",
    "third_party_notices.md",
    "third-party-notices.md",
}


def collect_from_scope(
    scope_path: Path,
    *,
    work_root: Path | None = None,
    keep_worktrees: bool = False,
) -> Path:
    scope_path = scope_path.resolve()
    scope = load_review_scope(scope_path)
    run_dir = scope_path.parent
    candidate_username = str(scope["candidate"]["username"])
    root = (work_root or Path.home() / ".workovercv" / safe_slug(candidate_username) / "worktrees").resolve()
    root.mkdir(parents=True, exist_ok=True)

    artifacts: list[dict[str, Any]] = []
    corpus: list[dict[str, Any]] = []
    chronology: list[dict[str, Any]] = []
    materialized: list[dict[str, Any]] = []
    cleanup_paths: list[Path] = []
    warnings: list[str] = []
    repositories = selected_repositories(scope)

    try:
        for repo in repositories:
            repo_root, cleanup = _materialize_repository(repo, root)
            if cleanup:
                cleanup_paths.append(repo_root)
            materialized.append(
                {
                    "repo_id": repo["repo_id"],
                    "source": "local_path" if repo.get("local_path") else "git_clone",
                    "path": str(repo_root),
                    "cleanup": cleanup and not keep_worktrees,
                }
            )
            repo_artifacts, repo_corpus = _inventory_repository(repo["repo_id"], repo_root)
            artifacts.extend(repo_artifacts)
            corpus.extend(repo_corpus)
            chronology.append(_collect_work_chronology(repo, repo_root))
    except Exception:
        if not keep_worktrees:
            _cleanup_materialized_paths(cleanup_paths, root, warnings)
        raise

    write_json(
        run_dir / "artifact_inventory.json",
        {
            "generated_at": utc_now_iso(),
            "source_scope": scope_path.name,
            "artifacts": artifacts,
        },
    )
    write_jsonl(run_dir / "review_corpus.jsonl", corpus)
    write_json(
        run_dir / "work_chronology.json",
        {
            "generated_at": utc_now_iso(),
            "max_commits_per_repository": MAX_CHRONOLOGY_COMMITS,
            "repositories": chronology,
        },
    )
    write_json(
        run_dir / "materialization.json",
        {
            "generated_at": utc_now_iso(),
            "work_root": str(root),
            "keep_worktrees": keep_worktrees,
            "repositories": materialized,
        },
    )
    if not keep_worktrees:
        _cleanup_materialized_paths(cleanup_paths, root, warnings)
    if not repositories:
        warnings.append("No repositories selected for review in review_scope.yml")
    update_run_manifest(
        run_dir,
        command="collect",
        config={"scope": str(scope_path), "work_root": str(root), "keep_worktrees": keep_worktrees},
        warnings=warnings,
        status="partial",
    )
    return run_dir


def _materialize_repository(repo: dict[str, Any], work_root: Path) -> tuple[Path, bool]:
    if repo.get("local_path"):
        local_path = Path(str(repo["local_path"])).expanduser().resolve()
        if not local_path.exists() or not local_path.is_dir():
            raise RuntimeError(f"local_path for {repo['repo_id']} does not exist or is not a directory")
        return local_path, False

    clone_url = repo.get("clone_url")
    if not clone_url:
        raise RuntimeError(f"Selected repository {repo['repo_id']} has no clone_url")
    destination = (work_root / safe_slug(str(repo["repo_id"]))).resolve()
    if destination.exists():
        _remove_tree_inside(destination, work_root)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", str(clone_url), str(destination)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git clone failed for {repo['repo_id']}: {result.stderr.strip()}")
    return destination, True


def _inventory_repository(repo_id: str, repo_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    artifacts: list[dict[str, Any]] = []
    corpus: list[dict[str, Any]] = []
    artifact_index = 0
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file() or _is_excluded(path, repo_root):
            continue
        if not _is_supported_text_file(path):
            continue
        text = _read_artifact_text(path)
        if text is None:
            continue
        size = path.stat().st_size
        relative_path = relative_to_or_self(path, repo_root)
        artifact_index += 1
        artifact_type = classify_artifact(relative_path)
        artifact_id = f"{safe_slug(repo_id)}-{artifact_index:04d}"
        artifact = {
            "artifact_id": artifact_id,
            "repo_id": repo_id,
            "path": relative_path,
            "artifact_type": artifact_type,
            "size_bytes": size,
            "size_estimate": _size_estimate(size),
            "likely_signal_value": _likely_signal_value(artifact_type, relative_path),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "notes": _artifact_notes(artifact_type),
        }
        artifacts.append(artifact)
        corpus.extend(_chunk_artifact(repo_id, artifact, text))
    return artifacts, corpus


def _collect_work_chronology(repo: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    repo_id = str(repo["repo_id"])
    if not (repo_root / ".git").exists():
        return _unavailable_chronology(repo_id, "git history is not available for this materialized repository")

    result = subprocess.run(
        [
            "git",
            "-C",
            str(repo_root),
            "log",
            f"--max-count={MAX_CHRONOLOGY_COMMITS}",
            "--date=iso-strict",
            "--pretty=format:%H%x1f%aI%x1f%s",
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        return _unavailable_chronology(repo_id, "git log could not be read")

    entries: list[dict[str, Any]] = []
    for raw_line in result.stdout.splitlines():
        parts = raw_line.split("\x1f", 2)
        if len(parts) != 3:
            continue
        commit_hash, committed_at, subject = parts
        if not commit_hash or not committed_at:
            continue
        entries.append(
            {
                "commit_hash": commit_hash,
                "committed_at": committed_at,
                "subject": subject,
            }
        )
    if not entries:
        return _unavailable_chronology(repo_id, "git history contained no readable commits")

    dates = [entry["committed_at"] for entry in entries]
    return {
        "repo_id": repo_id,
        "available": True,
        "default_branch": repo.get("default_branch"),
        "commit_count": len(entries),
        "first_commit_at": min(dates),
        "last_commit_at": max(dates),
        "entries": entries,
    }


def _unavailable_chronology(repo_id: str, reason: str) -> dict[str, Any]:
    return {
        "repo_id": repo_id,
        "available": False,
        "reason_unavailable": reason,
        "default_branch": None,
        "commit_count": 0,
        "first_commit_at": None,
        "last_commit_at": None,
        "entries": [],
    }


def classify_artifact(relative_path: str) -> str:
    lower = relative_path.lower().replace("\\", "/")
    name = Path(lower).name
    stem = Path(lower).stem
    suffix = Path(lower).suffix
    if suffix == ".ipynb":
        return "notebook_source"
    if lower.startswith(".github/workflows/"):
        return "CI_workflow"
    if _is_test_fixture_path(lower):
        return _classify_fixture_artifact(lower, name, suffix)
    if _is_unity_metadata_path(lower, name):
        return "configuration_file"
    if _is_low_signal_doc_name(name):
        return "technical_writeup"
    if _is_readme_file(name, suffix):
        return "README"
    if "model_card" in lower or "model-card" in lower:
        return "model_card"
    if ("failure" in lower or "postmortem" in lower) and suffix in {".md", ".rst", ".txt"}:
        return "failure_analysis"
    if "architecture" in lower or "design" in lower:
        return "architecture_document"
    if _is_schema_path(lower, name):
        return "configuration_file"
    if _is_package_manifest_path(lower, name) or name in CONFIG_FILE_NAMES or name.endswith("-requirements.txt"):
        return "configuration_file"
    if "test" in lower or lower.startswith("tests/"):
        return "test_file"
    if suffix in SCRIPT_EXTENSIONS and "train" in stem:
        return "training_script"
    if suffix in SCRIPT_EXTENSIONS and ("infer" in stem or "predict" in stem):
        return "inference_script"
    if suffix in SCRIPT_EXTENSIONS and ("eval" in stem or "benchmark" in stem):
        return "evaluation_script"
    if suffix in STRUCTURED_EXTENSIONS and "manifest" in name and "run" in name:
        return "run_manifest"
    if suffix in STRUCTURED_EXTENSIONS and (
        "manifest" in name
        or "data" in name
        or "dataset" in name
        or "metric" in name
        or "metrics" in name
        or "history" in name
        or "summary" in name
    ):
        return "data_manifest"
    if suffix in STRUCTURED_EXTENSIONS:
        return "configuration_file"
    if suffix in SOURCE_EXTENSIONS:
        return "source_code"
    if lower.startswith("docs/") or suffix in {".md", ".rst"}:
        return "technical_writeup"
    return "technical_writeup"


def _is_test_fixture_path(lower_path: str) -> bool:
    parts = lower_path.split("/")
    return any(parts[index] == "tests" and parts[index + 1] == "fixtures" for index in range(len(parts) - 1))


def _classify_fixture_artifact(lower_path: str, name: str, suffix: str) -> str:
    if suffix in {".md", ".rst"}:
        return "technical_writeup"
    if "manifest" in name or "data" in lower_path or suffix in {".json", ".yml", ".yaml"}:
        return "data_manifest"
    if suffix in {".toml", ".ini", ".cfg"}:
        return "configuration_file"
    if suffix in SOURCE_EXTENSIONS:
        return "source_code"
    return "technical_writeup"


def _is_readme_file(name: str, suffix: str) -> bool:
    return name == "readme" or (Path(name).stem == "readme" and suffix in {".md", ".rst", ".txt"})


def _is_unity_metadata_path(lower_path: str, name: str) -> bool:
    return name.endswith((".asset", ".asset.meta", ".meta")) or "/packages/" in lower_path


def _is_package_manifest_path(lower_path: str, name: str) -> bool:
    return (
        "/packages/" in lower_path
        or name in {"manifest.json", "packages-lock.json", "package-lock.json", "package.json"}
        or name.endswith("-lock.json")
    )


def _is_schema_path(lower_path: str, name: str) -> bool:
    return name.endswith(".schema.json") or "/schemas/" in lower_path


def _is_low_signal_doc_name(name: str) -> bool:
    return name in LOW_SIGNAL_DOC_NAMES or name.startswith("license.") or name.startswith("notice.")


def _is_excluded(path: Path, repo_root: Path) -> bool:
    try:
        relative = path.relative_to(repo_root)
    except ValueError:
        return True
    return any(part in EXCLUDED_DIRS for part in relative.parts)


def _is_supported_text_file(path: Path) -> bool:
    name = path.name.lower()
    suffix = path.suffix.lower()
    return suffix in TEXT_EXTENSIONS or _is_readme_file(name, suffix) or name in CONFIG_FILE_NAMES


def _read_artifact_text(path: Path) -> str | None:
    if path.suffix.lower() == ".ipynb":
        return _read_notebook_source_only(path)
    if path.stat().st_size > MAX_TEXT_ARTIFACT_BYTES:
        return None
    return _read_text(path)


def _read_text(path: Path) -> str | None:
    raw = path.read_bytes()
    if b"\x00" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace")


def _read_notebook_source_only(path: Path) -> str | None:
    if path.stat().st_size > MAX_NOTEBOOK_ARTIFACT_BYTES:
        return None
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(notebook, dict):
        return None
    cells = notebook.get("cells", [])
    if not isinstance(cells, list):
        return None

    lines = [
        "# Notebook source-only projection",
        "# Outputs, execution counts, and notebook metadata were stripped by WorkOverCV.",
    ]
    for index, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            continue
        cell_type = cell.get("cell_type")
        if cell_type not in {"markdown", "code"}:
            continue
        source = _notebook_source_to_text(cell.get("source"))
        if not source.strip():
            continue
        lines.extend(["", f"# Cell {index} [{cell_type}]", source.rstrip()])
    if len(lines) == 2:
        return None
    return "\n".join(lines).rstrip() + "\n"


def _notebook_source_to_text(source: Any) -> str:
    if isinstance(source, str):
        return source
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return ""


def _size_estimate(size: int) -> str:
    if size < 20_000:
        return "small"
    if size < 100_000:
        return "medium"
    return "large"


def _likely_signal_value(artifact_type: str, relative_path: str) -> str:
    lower = relative_path.lower().replace("\\", "/")
    name = Path(lower).name
    if (
        _is_low_signal_doc_name(name)
        or _is_unity_metadata_path(lower, name)
        or _is_package_manifest_path(lower, name)
        or artifact_type in {"run_manifest", "data_manifest"}
    ):
        return "low"
    if artifact_type in {"README", "architecture_document", "model_card", "failure_analysis", "test_file", "CI_workflow"}:
        return "high"
    if artifact_type in {"technical_writeup", "source_code", "configuration_file", "evaluation_script", "notebook_source"}:
        return "medium"
    return "low"


def _artifact_notes(artifact_type: str) -> str:
    if artifact_type == "notebook_source":
        return "Notebook source-only projection; outputs, execution counts, and metadata stripped; never executed."
    return ""


def _chunk_artifact(repo_id: str, artifact: dict[str, Any], text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    if not lines:
        lines = [""]
    chunks: list[dict[str, Any]] = []
    chunk_size = 80
    for start in range(0, len(lines), chunk_size):
        chunk_lines = lines[start : start + chunk_size]
        line_start = start + 1
        line_end = start + len(chunk_lines)
        chunk_text = "\n".join(chunk_lines)
        chunk_id = f"{artifact['artifact_id']}-chunk-{len(chunks) + 1:03d}"
        chunks.append(
            {
                "chunk_id": chunk_id,
                "repo_id": repo_id,
                "artifact_id": artifact["artifact_id"],
                "path": artifact["path"],
                "artifact_type": artifact["artifact_type"],
                "locator": {"type": "line_range", "value": f"{line_start}-{line_end}"},
                "line_start": line_start,
                "line_end": line_end,
                "sha256": hashlib.sha256(chunk_text.encode("utf-8")).hexdigest(),
                "text": chunk_text,
            }
        )
    return chunks


def _cleanup_materialized_paths(paths: list[Path], root: Path, warnings: list[str]) -> None:
    for path in paths:
        try:
            _remove_tree_inside(path, root)
        except OSError as exc:
            warnings.append(f"Could not clean up worktree {path}: {exc}")


def _remove_tree_inside(target: Path, root: Path) -> None:
    target_abs = target.resolve()
    root_abs = root.resolve()
    if target_abs == root_abs or root_abs not in target_abs.parents:
        raise RuntimeError(f"Refusing to remove path outside work root: {target_abs}")
    if target_abs.exists():
        shutil.rmtree(target_abs, onerror=_make_writable_and_retry)


def _make_writable_and_retry(function: Any, path: str, _exc_info: Any) -> None:
    Path(path).chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    function(path)
