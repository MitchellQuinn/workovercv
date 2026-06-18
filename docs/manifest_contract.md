# Manifest Contract

`review_scope.yml` is the hard boundary for collection and downstream analysis.
Discovery may suggest repositories, but collection must only process entries
where `selected_for_review` is true.

## Shape

```yaml
candidate:
  type: github_profile
  url: https://github.com/example-user
  username: example-user

repositories:
  - repo_id: example-user-project
    name: project
    url: https://github.com/example-user/project
    clone_url: https://github.com/example-user/project.git
    default_branch: main
    selected_for_review: true
    selection_reason: non-fork repository with recent activity and reviewable metadata
```

The implementation also accepts `local_path` on repository entries for tests and
future materialization wrappers. Public discovery does not generate `local_path`
entries in v0.6.

## Rules

- Missing or invalid scope manifests fail before collection.
- Repositories with `selected_for_review: false` are not cloned or read.
- Forks may be selected only when the candidate contribution is clear.
- Generated scopes are starter selections, not exhaustive claims about the
  candidate's work.
- Default GitHub discovery excludes profile README repositories, forks,
  archived or disabled repositories, empty repositories, and very lightweight
  repositories from `selected_for_review`.
- Excluded repositories remain in `repo_inventory.json` and `review_scope.yml`
  with explicit `selection_reason` text so reviewers can opt in manually.
