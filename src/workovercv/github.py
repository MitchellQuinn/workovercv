from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

from .io import safe_slug, utc_now_iso, utc_timestamp
from .manifest import write_repo_inventory, write_review_scope
from .run_manifest import update_run_manifest

JsonFetcher = Callable[[str], Any]


class GitHubError(RuntimeError):
    """Raised when GitHub discovery fails."""


def parse_github_profile_url(candidate_url: str) -> str:
    parsed = urllib.parse.urlparse(candidate_url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise GitHubError("Candidate must be an http(s) GitHub profile URL")
    host = parsed.netloc.lower()
    if host not in {"github.com", "www.github.com"}:
        raise GitHubError("Candidate URL must point to github.com")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) != 1:
        raise GitHubError("Candidate URL must be a GitHub profile URL like https://github.com/user")
    username = parts[0]
    if username.startswith("-") or username.endswith("-") or len(username) > 39:
        raise GitHubError("GitHub username is not valid")
    return username


class GitHubClient:
    def __init__(self, fetch_json: JsonFetcher | None = None) -> None:
        self._fetch_json = fetch_json or self._fetch_json_from_url

    def get_user(self, username: str) -> dict[str, Any]:
        data = self._fetch_json(f"https://api.github.com/users/{urllib.parse.quote(username)}")
        if not isinstance(data, dict):
            raise GitHubError("GitHub user response was not an object")
        return data

    def get_repositories(self, username: str, max_pages: int = 10) -> list[dict[str, Any]]:
        repositories: list[dict[str, Any]] = []
        for page in range(1, max_pages + 1):
            url = (
                f"https://api.github.com/users/{urllib.parse.quote(username)}/repos"
                f"?per_page=100&page={page}&sort=updated&type=owner"
            )
            page_data = self._fetch_json(url)
            if not isinstance(page_data, list):
                raise GitHubError("GitHub repository response was not a list")
            repositories.extend(repo for repo in page_data if isinstance(repo, dict))
            if len(page_data) < 100:
                break
        return repositories

    @staticmethod
    def _fetch_json_from_url(url: str) -> Any:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "workovercv/0.1",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise GitHubError("GitHub profile was not found") from exc
            raise GitHubError(f"GitHub request failed with HTTP {exc.code}") from exc
        except urllib.error.URLError as exc:
            raise GitHubError(f"GitHub request failed: {exc.reason}") from exc


def discover_candidate(
    candidate_url: str,
    out_root: Path,
    *,
    client: GitHubClient | None = None,
) -> Path:
    username = parse_github_profile_url(candidate_url)
    github = client or GitHubClient()
    user = github.get_user(username)
    repositories = github.get_repositories(username)

    run_dir = out_root / f"{safe_slug(username)}-{utc_timestamp()}"
    run_dir.mkdir(parents=True, exist_ok=False)

    inventory_repos = _inventory_repositories(username, repositories)
    inventory = {
        "candidate": {
            "type": "github_profile",
            "url": f"https://github.com/{username}",
            "username": username,
            "display_name": user.get("name"),
            "public_repos": user.get("public_repos"),
        },
        "generated_at": utc_now_iso(),
        "source": {
            "type": "github_api",
            "authenticated": False,
        },
        "repositories": inventory_repos,
    }
    write_repo_inventory(run_dir / "repo_inventory.json", inventory)

    scope = {
        "candidate": inventory["candidate"],
        "generated_at": inventory["generated_at"],
        "source_inventory": "repo_inventory.json",
        "repositories": [
            {
                "repo_id": repo["repo_id"],
                "name": repo["name"],
                "url": repo["url"],
                "clone_url": repo["clone_url"],
                "default_branch": repo.get("default_branch"),
                "selected_for_review": repo["selected_for_review"],
                "selection_reason": repo["selection_reason"],
            }
            for repo in inventory_repos
        ],
    }
    write_review_scope(run_dir / "review_scope.yml", scope)
    update_run_manifest(
        run_dir,
        command="discover",
        config={"candidate": candidate_url, "out": str(out_root)},
        status="partial",
    )
    return run_dir


def _inventory_repositories(username: str, repositories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scored = [(_repository_score(username, repo), repo) for repo in repositories]
    selected_candidates = [
        _repo_id(username, repo)
        for _score, repo in sorted(scored, key=lambda item: item[0], reverse=True)
        if _is_default_review_candidate(username, repo)
    ][:5]
    selected_ids = set(selected_candidates)

    inventory: list[dict[str, Any]] = []
    for score, repo in sorted(scored, key=lambda item: item[0], reverse=True):
        repo_id = _repo_id(username, repo)
        selected = repo_id in selected_ids
        inventory.append(
            {
                "repo_id": repo_id,
                "name": repo.get("name") or repo_id,
                "url": repo.get("html_url") or f"https://github.com/{username}/{repo.get('name', repo_id)}",
                "clone_url": repo.get("clone_url"),
                "description": repo.get("description"),
                "primary_language": repo.get("language"),
                "visibility": repo.get("visibility") or "public",
                "selected_for_review": selected,
                "selection_reason": _selection_reason(username, repo, selected),
                "default_branch": repo.get("default_branch"),
                "last_updated": repo.get("pushed_at") or repo.get("updated_at"),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "watchers": repo.get("watchers_count", 0),
                "fork": bool(repo.get("fork")),
                "archived": bool(repo.get("archived")),
                "license": (repo.get("license") or {}).get("spdx_id") if isinstance(repo.get("license"), dict) else None,
                "release_status": "unknown",
                "readme_presence": "unknown",
                "test_presence": "unknown",
                "documentation_presence": "unknown",
                "selection_score": score,
            }
        )
    return inventory


def _repo_id(username: str, repo: dict[str, Any]) -> str:
    return safe_slug(f"{username}-{repo.get('name') or 'repo'}")


def _repository_score(username: str, repo: dict[str, Any]) -> int:
    score = 0
    if not repo.get("fork"):
        score += 50
    if repo.get("description"):
        score += 12
    if repo.get("language"):
        score += 8
    if repo.get("pushed_at") or repo.get("updated_at"):
        score += 5
    if int(repo.get("size") or 0) > 20:
        score += 5
    if _is_profile_readme_repo(username, repo):
        score -= 45
    if _is_empty_repo(repo):
        score -= 40
    if _is_very_lightweight_repo(repo):
        score -= 25
    if repo.get("archived"):
        score -= 30
    if repo.get("disabled"):
        score -= 50
    return score


def _is_default_review_candidate(username: str, repo: dict[str, Any]) -> bool:
    return not (
        repo.get("fork")
        or repo.get("archived")
        or repo.get("disabled")
        or _is_profile_readme_repo(username, repo)
        or _is_empty_repo(repo)
        or _is_very_lightweight_repo(repo)
    )


def _is_profile_readme_repo(username: str, repo: dict[str, Any]) -> bool:
    name = str(repo.get("name") or "")
    return bool(name) and name.casefold() == username.casefold()


def _is_empty_repo(repo: dict[str, Any]) -> bool:
    return int(repo.get("size") or 0) == 0


def _is_very_lightweight_repo(repo: dict[str, Any]) -> bool:
    return int(repo.get("size") or 0) < 20 and not repo.get("language") and not repo.get("description")


def _selection_reason(username: str, repo: dict[str, Any], selected: bool) -> str:
    if not selected:
        if repo.get("fork"):
            return "not selected by default because it is a fork"
        if repo.get("archived"):
            return "not selected by default because it is archived"
        if repo.get("disabled"):
            return "not selected by default because it is disabled"
        if _is_profile_readme_repo(username, repo):
            return "not selected by default because it is a profile README repository"
        if _is_empty_repo(repo):
            return "not selected by default because it appears empty from GitHub size metadata"
        if _is_very_lightweight_repo(repo):
            return "not selected by default because it appears very lightweight from GitHub metadata"
        return "not selected in the initial substantive five-repository review scope"
    reasons = ["selected for the starter review scope", "substantive default review candidate"]
    if not repo.get("fork"):
        reasons.append("non-fork")
    if repo.get("description"):
        reasons.append("has description")
    if repo.get("language"):
        reasons.append("has primary language metadata")
    if int(repo.get("size") or 0) > 0:
        reasons.append("has repository size metadata")
    if repo.get("pushed_at") or repo.get("updated_at"):
        reasons.append("has public update metadata")
    return "; ".join(reasons)
