# Runtime Contract

The Python CLI is the shared deterministic runtime surface. It gathers public
or local repository data, creates a review corpus, collects bounded chronology
input, renders Work Behaviour Profile Markdown, and validates artifacts written
by deterministic or agentic analysis.

The CLI does not call an LLM provider in v0.6. LLM judgement work is performed
by an agent adapter against the canonical workflow in `workflows/workovercv.yml`.

## Commands

```bash
workovercv discover \
  --candidate https://github.com/<user> \
  [--out output]
```

`discover` reads public GitHub profile and repository metadata without
authentication. It writes a timestamped run directory under `--out` containing
`repo_inventory.json`, `review_scope.yml`, and `run_manifest.json`.

```bash
workovercv collect \
  --scope /path/to/review_scope.yml \
  [--work-root ~/.workovercv/<candidate>/worktrees] \
  [--keep-worktrees]
```

`collect` only processes repositories where `selected_for_review` is true in the
scope manifest. It materializes selected repositories into the controlled work
root, inventories evidence-bearing artifacts, writes `artifact_inventory.json`,
`review_corpus.jsonl`, and `work_chronology.json` beside the scope file, and
deletes cloned worktrees unless `--keep-worktrees` is set.

Notebook files (`.ipynb`) are static evidence only. The collector parses them as
JSON, records a `notebook_source` artifact, and writes only markdown/code cell
source into `review_corpus.jsonl`. Outputs, execution counts, notebook metadata,
and cell metadata are stripped. WorkOverCV must never execute notebooks.

`work_chronology.json` is bounded analysis input. It records at most the
configured number of git commits per selected repository when readable history
is available, or an unavailable-chronology record when it is not. Raw commit
hashes, raw commit messages, and raw timelines must not be rendered into
`report.json`, `report.md`, or `summary-report.md`.

```bash
workovercv analyze --run /path/to/run_dir
```

`analyze` builds deterministic analysis artifacts for a collected run. It writes
structured ledgers, `role_family_fit.json`, compatibility `mitigations.jsonl`
gap follow-ups, and v0.6 `report.json`, then records deterministic analysis
provenance in `run_manifest.json`. Agent-authored analysis remains valid when
the required artifacts are written manually and pass validation.

`report.json` includes `analysis_model_information`. Deterministic rubric
analysis records that no LLM model was used; agent-authored analysis must record
the active model identity exposed by the host environment, or state that the
runtime did not disclose one.

Deterministic analysis may add synthetic run-boundary artifact records for
`artifact_inventory.json` and `work_chronology.json` so absence and cadence
evidence can cite explicit run-boundary artifacts.

```bash
workovercv render --run /path/to/run_dir
```

`render` converts v0.6 `report.json` into audit-oriented `report.md`, writes
human-facing `summary-report.md`, and writes `screening_brief.md`, a cautious
review guide derived from the validated report, role-family fit entries, signal
ledger, evidence map, gaps, and gap follow-ups.
The report scope includes `scope_and_evidence_base.candidate_url`, populated
from the workflow candidate URL or local scan URI.
The rendered `report.md` and `summary-report.md` include
`analysis_model_information` in their scope sections.
`audit` mode is the default for `report.md` and renders verbose evidence tables
for deeper inspection. The separate `summary-report.md` is always rendered with
concise repository/path evidence references and no evidence appendix.

```bash
workovercv validate --run /path/to/run_dir
```

`validate` checks required artifacts, structured records, cross references,
v0.6 report shape, allowed Markdown headings, role-family limits, gap follow-ups, red-team status,
prohibited wording, hiring-decision language, old-heading regressions, and raw
chronology leakage into final report outputs.

## Required Final Outputs

The following files must exist after a successful final run:

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

`run_manifest.json` includes itself in its `artifacts` array so the manifest
lists the complete final file set.

Artifact inventory and review corpus records use `artifact_type` as the
canonical artifact-category field. `candidate.type`, `source.type`, and
`locator.type` remain separate structural fields.

`discover` and `collect` produce partial runs. `validate` is the final gate.

## Exit Codes

- `0`: command completed successfully
- `1`: invalid arguments, missing paths, or runtime error
- `2`: manifest validation failed
- `3`: final artifact validation failed
