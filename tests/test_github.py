from __future__ import annotations

import json
from pathlib import Path

import yaml

from workovercv.github import GitHubClient, GitHubError, discover_candidate, parse_github_profile_url


def test_parse_github_profile_url_accepts_profile() -> None:
    assert parse_github_profile_url("https://github.com/MitchellQuinn") == "MitchellQuinn"


def test_parse_github_profile_url_rejects_repo_url() -> None:
    try:
        parse_github_profile_url("https://github.com/MitchellQuinn/claimlint")
    except GitHubError as exc:
        assert "profile URL" in str(exc)
    else:
        raise AssertionError("expected GitHubError")


def test_discover_candidate_writes_inventory_and_scope(tmp_path: Path) -> None:
    repos = [
        _repo("example", size=10),
        _repo("alpha", language="Python", description="portfolio"),
        _repo("beta", language="TypeScript", description="tooling"),
        _repo("gamma", language="Python", description="docs"),
        _repo("delta", language="Go", description="service"),
        _repo("epsilon", language="Rust", description="systems"),
        _repo("zeta", language="Python", description="extra"),
        _repo("empty", language="Python", description="empty", size=0),
        _repo("tiny", size=10),
        _repo("forked", fork=True, description="fork"),
        _repo("archived", archived=True, description="old"),
    ]

    def fetch_json(url: str):
        if url.endswith("/users/example"):
            return {"login": "example", "name": "Example", "public_repos": len(repos)}
        if "/users/example/repos" in url:
            return repos
        raise AssertionError(url)

    run_dir = discover_candidate(
        "https://github.com/example",
        tmp_path,
        client=GitHubClient(fetch_json=fetch_json),
    )

    inventory = json.loads((run_dir / "repo_inventory.json").read_text(encoding="utf-8"))
    scope = yaml.safe_load((run_dir / "review_scope.yml").read_text(encoding="utf-8"))

    assert inventory["candidate"]["username"] == "example"
    assert len(inventory["repositories"]) == len(repos)
    assert sum(1 for repo in scope["repositories"] if repo["selected_for_review"]) == 5
    assert all(
        repo["name"] not in {"example", "empty", "tiny", "forked", "archived"}
        for repo in scope["repositories"]
        if repo["selected_for_review"]
    )
    by_name = {repo["name"]: repo for repo in scope["repositories"]}
    assert "profile README repository" in by_name["example"]["selection_reason"]
    assert "appears empty" in by_name["empty"]["selection_reason"]
    assert "very lightweight" in by_name["tiny"]["selection_reason"]
    assert "fork" in by_name["forked"]["selection_reason"]
    assert "archived" in by_name["archived"]["selection_reason"]
    assert (run_dir / "run_manifest.json").exists()


def _repo(
    name: str,
    *,
    language: str | None = None,
    description: str | None = None,
    fork: bool = False,
    archived: bool = False,
    size: int = 42,
) -> dict:
    return {
        "name": name,
        "html_url": f"https://github.com/example/{name}",
        "clone_url": f"https://github.com/example/{name}.git",
        "description": description,
        "language": language,
        "visibility": "public",
        "default_branch": "main",
        "pushed_at": "2026-06-01T00:00:00Z",
        "updated_at": "2026-06-01T00:00:00Z",
        "stargazers_count": 0,
        "forks_count": 0,
        "watchers_count": 0,
        "fork": fork,
        "archived": archived,
        "disabled": False,
        "size": size,
        "license": {"spdx_id": "Apache-2.0"},
    }
