# Codex Adapter Smoke Verification

## Historical 2026-06-17 GitHub Profile Smoke

This run predates the v0.6 Work Behaviour Profile report-shape and output-quality contract. Use it
as historical adapter evidence only; rerun `adapters/codex/VERIFY.md` before
marking v0.6 adapter compatibility as tested.

This smoke run verifies that Codex can apply the WorkOverCV adapter
instructions, run the shared CLI, perform the agent-authored artifact pass, and
validate the required outputs without redefining the workflow.

Environment:

- Codex session workspace: `C:\Development\agentic-skills\workovercv`
- Verification procedure: `adapters/codex/VERIFY.md`
- Runtime: `PYTHONPATH=src python -m workovercv`
- Candidate: `https://github.com/MitchellQuinn`

Commands run by Codex:

```powershell
$env:PYTHONPATH = "src"
python -m workovercv discover --candidate https://github.com/MitchellQuinn --out output\test-github
python -m workovercv collect --scope output\test-github\mitchellquinn-20260617-1325Z\review_scope.yml --work-root output\test-github-worktrees-keep --keep-worktrees
python -m workovercv analyze --run output\test-github\mitchellquinn-20260617-1325Z
python -m workovercv render --run output\test-github\mitchellquinn-20260617-1325Z --mode summary
python -m workovercv validate --run output\test-github\mitchellquinn-20260617-1325Z
```

Report-shape correction note: deterministic GitHub-profile smoke runs must
include `analyze` between `collect` and `render` so the structured ledgers and
spec-shaped `report.json` are produced by the shared CLI path.
Current reruns should use `python -m workovercv render --run <run>` so
`report.md`, `summary-report.md`, and `screening_brief.md` are generated with
the current defaults.

Output directory:

```text
output/test-github/mitchellquinn-20260617-1325Z
```

Current v0.6 required outputs to verify on the next smoke run:

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

Run manifest fields verified:

- `tool_name`: `workovercv`
- `workflow_id`: `workovercv.repository-employment-signal`
- final `status`: `complete`

Result: passed.

Scope note: this records the Codex GitHub-profile adapter smoke. It is a
compact end-to-end report over a large corpus, not an exhaustive employment
assessment.
