from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .io import write_json


class ManifestError(ValueError):
    """Raised when a review scope manifest is invalid."""


def write_review_scope(path: Path, scope: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(scope, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def load_review_scope(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ManifestError(f"Review scope not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ManifestError("Review scope must be a YAML mapping")
    validate_review_scope(data)
    return data


def validate_review_scope(scope: dict[str, Any]) -> None:
    candidate = scope.get("candidate")
    if not isinstance(candidate, dict):
        raise ManifestError("Review scope requires a candidate mapping")
    if candidate.get("type") not in {"github_profile", "local_path"}:
        raise ManifestError("candidate.type must be github_profile or local_path")
    if not candidate.get("url") or not candidate.get("username"):
        raise ManifestError("candidate.url and candidate.username are required")

    repositories = scope.get("repositories")
    if not isinstance(repositories, list):
        raise ManifestError("Review scope requires a repositories list")

    repo_ids: set[str] = set()
    for index, repo in enumerate(repositories):
        if not isinstance(repo, dict):
            raise ManifestError(f"repositories[{index}] must be a mapping")
        for field in ("repo_id", "name", "url", "selected_for_review"):
            if field not in repo:
                raise ManifestError(f"repositories[{index}].{field} is required")
        repo_id = str(repo["repo_id"])
        if repo_id in repo_ids:
            raise ManifestError(f"Duplicate repo_id in review scope: {repo_id}")
        repo_ids.add(repo_id)
        if repo.get("selected_for_review") is True and not (repo.get("clone_url") or repo.get("local_path")):
            raise ManifestError(f"Selected repository {repo_id} requires clone_url or local_path")


def selected_repositories(scope: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        repo
        for repo in scope.get("repositories", [])
        if repo.get("selected_for_review") is True
    ]


def write_repo_inventory(path: Path, inventory: dict[str, Any]) -> None:
    write_json(path, inventory)
