# Codex Adapter Verification

This procedure verifies that Codex can apply the WorkOverCV skill, run the
shared CLI, perform the agentic analysis pass, and validate required outputs
without redefining the workflow.

## Preconditions

- WorkOverCV is installed or available in the active Python environment.
- The repository is opened at the WorkOverCV root.
- The Codex adapter plugin has been installed from the personal marketplace, or
  the plugin package is available from `adapters/codex/plugin/workovercv`.

## Smoke Prompt

Ask Codex:

```text
Use the WorkOverCV skill to assess https://github.com/<public-user>.
Use default output paths. Run discover, inspect review_scope.yml, run collect,
write the required ledgers and report JSON, render the report, and validate the
run.
```

Expected deterministic commands:

```bash
workovercv discover --candidate https://github.com/<public-user>
workovercv collect --scope output/<run>/review_scope.yml
workovercv analyze --run output/<run>
workovercv render --run output/<run>
workovercv validate --run output/<run>
```

If the package is not installed, run the same commands from the repository root
with `PYTHONPATH=src python -m workovercv ...`. On PowerShell, set
`$env:PYTHONPATH = "src"` before calling `python -m workovercv`.

## Required Evidence

Record the output directory and confirm these files exist:

- `report.md`
- `summary-report.md`
- `screening_brief.md`
- `report.json`
- `repo_inventory.json`
- `review_scope.yml`
- `artifact_inventory.json`
- `review_corpus.jsonl`
- `work_chronology.json`
- `explicit_claims.jsonl`
- `signal_ledger.jsonl`
- `evidence_map.jsonl`
- `gap_register.jsonl`
- `role_family_fit.json`
- `mitigations.jsonl`
- `red_team_review.json`
- `run_manifest.json`

Also confirm `run_manifest.json` reports:

- `tool_name`: `workovercv`
- `workflow_id`: `workovercv.repository-employment-signal`
- final `status`: `complete`

## Status Update Rule

Only update `adapters/status.yml` from `untested` after the Codex smoke prompt
succeeds end to end in an actual Codex session. A direct CLI test is
implementation evidence, not adapter compatibility evidence.
