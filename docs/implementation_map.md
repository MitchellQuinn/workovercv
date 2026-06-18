# Implementation Map

Use the module paths below as code pointers. This page is not a conformance
matrix and does not define every runtime, schema, or configuration boundary.
Workflow outputs, schemas, and validation boundaries remain defined by
`workflows/workovercv.yml`, `schemas/*.schema.json`, `docs/runtime_contract.md`,
and `docs/validation_contract.md`.

| Runtime behavior or workflow stage | Implementation modules | Evidence notes |
| --- | --- | --- |
| CLI orchestration | `src/workovercv/cli.py` | Defines `discover`, `scan`, `collect`, `analyze`, `render`, and `validate`; handles exit codes and top-level errors. |
| GitHub profile discovery | `src/workovercv/github.py` | Parses GitHub profile URLs and reads public user/repository metadata with unauthenticated requests. |
| Scope manifest | `src/workovercv/manifest.py` | Writes and validates `review_scope.yml`; collection only processes selected repositories. |
| Run manifest | `src/workovercv/run_manifest.py` | Captures workflow identity, command history, output paths, warnings, and timestamps. |
| Repository materialization and corpus | `src/workovercv/collect.py` | Clones or reads selected repositories, inventories artifacts with canonical `artifact_type`, chunks text, writes schema-validated `review_corpus.jsonl`, collects bounded `work_chronology.json`, and cleans worktrees by default. |
| Deterministic analysis | `src/workovercv/analysis.py`, `src/workovercv/rubric.py` | Builds structured ledgers, behaviour signals, evidence gaps, role-family fit, gap follow-ups, and the v0.6 Work Behaviour Profile report; adds synthetic run-boundary artifacts when absence or chronology evidence needs an anchor. |
| Report rendering | `src/workovercv/render.py` | Renders audit-oriented `report.md`, human-facing `summary-report.md`, and `screening_brief.md` from v0.6 `report.json`, behaviour signals, role-family entries, gaps, and follow-ups. |
| Final validation | `src/workovercv/validation.py` | Checks required artifacts, record references, v0.6 report shape, gap follow-ups, role-family references and caveats, raw chronology leakage, red-team status, prohibited wording, hiring-decision language, and legacy heading regressions. |
| Workflow output contract | `workflows/workovercv.yml`, `src/workovercv/constants.py` | Lists canonical output paths and the current `REQUIRED_FINAL_ARTIFACTS` used by the final validation gate. |
| Schema references | `schemas/*.schema.json`, `src/workovercv/validation.py` | Provide machine-readable output shapes and the implementation mapping from final artifacts to schema validators. |
| Validation evidence map | `docs/validation_contract.md` | Links validation gates to implementation, schema, and test evidence, including complete-run validation tests. |

Agentic judgement stages are adapter-dependent in v0.6. The repository
documents the contract an adapter must follow in `skills/workovercv/SKILL.md`,
`docs/adapter_contract.md`, and adapter-specific README files; the shared
Python runtime does not execute those judgement stages directly. The
deterministic `analyze` command provides a local rubric path for smoke tests
without API calls.
