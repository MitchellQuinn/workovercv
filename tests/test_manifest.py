from __future__ import annotations

from pathlib import Path

import pytest

from workovercv.manifest import ManifestError, load_review_scope, selected_repositories, write_review_scope


def test_review_scope_requires_candidate(tmp_path: Path) -> None:
    scope_path = tmp_path / "review_scope.yml"
    write_review_scope(scope_path, {"repositories": []})

    with pytest.raises(ManifestError):
        load_review_scope(scope_path)


def test_selected_repository_requires_materialization_source(tmp_path: Path) -> None:
    scope_path = tmp_path / "review_scope.yml"
    write_review_scope(
        scope_path,
        {
            "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
            "repositories": [
                {
                    "repo_id": "example-alpha",
                    "name": "alpha",
                    "url": "https://github.com/example/alpha",
                    "selected_for_review": True,
                }
            ],
        },
    )

    with pytest.raises(ManifestError):
        load_review_scope(scope_path)


def test_selected_repositories_filters_unselected(tmp_path: Path) -> None:
    fixture = Path("tests/fixtures/small_repo").resolve()
    scope = {
        "candidate": {"type": "github_profile", "url": "https://github.com/example", "username": "example"},
        "repositories": [
            {
                "repo_id": "example-small",
                "name": "small",
                "url": "https://github.com/example/small",
                "local_path": str(fixture),
                "selected_for_review": True,
            },
            {
                "repo_id": "example-skip",
                "name": "skip",
                "url": "https://github.com/example/skip",
                "selected_for_review": False,
            },
        ],
    }

    assert [repo["repo_id"] for repo in selected_repositories(scope)] == ["example-small"]
