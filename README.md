# WorkOverCV

WorkOverCV is an agentic workflow for producing evidence-bounded work
behaviour profile reports from public technical repositories.

It asks one narrow question:

> What kind of employee or engineer would this person likely be, based on
> observable repository work?

WorkOverCV does not make hiring decisions, certify competence, infer protected
or private traits, or treat popularity metrics as competence metrics. It turns
public repository artifacts into reviewable evidence, behaviour signals,
evidence gaps, role-family discussion routes, and follow-up questions.

## V0.6 Shape

The canonical workflow is `workflows/workovercv.yml`. The shared runtime surface
is documented in `docs/runtime_contract.md`. Agent adapters under `adapters/`
must point to those contracts rather than redefining the workflow.

The Python CLI handles deterministic data gathering, local deterministic scans,
Markdown/PDF rendering, and strict validation:

```bash
python -m pip install -e ".[test]"
workovercv scan /path/to/local/repository
```

PDF rendering uses WeasyPrint. After installing dependencies, run
`python -m weasyprint --info` to verify native PDF libraries. On Windows, this
requires Pango/GObject libraries such as the MSYS2
`mingw-w64-x86_64-pango` package, with `C:\msys64\mingw64\bin` available on
`PATH`.

After installation, the console entry point is:

```bash
workovercv scan <path>
workovercv discover --candidate https://github.com/example-user
workovercv collect --scope output/example-user-YYYYMMDD-HHMMZ/review_scope.yml
workovercv analyze --run output/example-user-YYYYMMDD-HHMMZ
workovercv render --run output/example-user-YYYYMMDD-HHMMZ
workovercv validate --run output/example-user-YYYYMMDD-HHMMZ
```

For development without installing the package, use:

```bash
PYTHONPATH=src python -m workovercv scan <path>
PYTHONPATH=src python -m workovercv validate --run output/example-run
```

On PowerShell, set the path first:

```bash
$env:PYTHONPATH = "src"
python -m workovercv scan <path>
```

`scan <path>` is offline. It creates a local run, collects repository artifacts
and bounded git chronology, generates behaviour signals and role-family
discussion routes, renders `report.md`, `summary-report.md`, and a cautious
`screening_brief.md` review guide plus matching PDFs, and runs validation. It
does not fetch GitHub data and does not call an LLM.

`render` defaults to audit-oriented `report.md` and also writes
`summary-report.md`, a shorter human-facing conversation guide with concise
evidence path references and no evidence appendix. It also writes
`report.pdf`, `summary-report.pdf`, and `screening_brief.pdf` from the generated
Markdown files.

Notebook files are read statically. WorkOverCV records `.ipynb` files as
`notebook_source` artifacts and collects only markdown/code cell source. It
strips outputs, execution counts, and notebook metadata, and it never executes
notebook code.

For `discover` and `collect` workflows, an agent may still write the structured
ledgers and final report JSON, but validation is fail-closed. WorkOverCV
includes validation gates for JSON Schema conformance, closed enum values,
evidence boundaries, role-family references, gap follow-up structure,
old-heading regressions, and safety wording checks. See
`docs/validation_contract.md` for the implementation/test mapping.
Agent-authored `report.json` must include `analysis_model_information` with the
active model identity exposed by the host environment, or a statement that the
runtime did not disclose one. Deterministic local analysis records that no LLM
model was used.

## Required Final Artifacts

A valid final run contains:

- `report.md`
- `summary-report.md`
- `screening_brief.md`
- `report.pdf`
- `summary-report.pdf`
- `screening_brief.pdf`
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

`work_chronology.json` is an analysis input. It may contain bounded git commit
metadata, but raw commit hashes, raw commit messages, and raw timelines must not
be emitted in `report.json`, `report.md`, or `summary-report.md`. The PDF
outputs are deterministic renderings of those validated Markdown files.

## Strict Validation

Validation rejects:

- unsupported signal confidence or category values
- old v0.3 signal fields such as `polarity`, `strength`, or `explanation`
- old `report.json` shapes containing `summary`, `findings`, or section IDs
- `report.json` missing `analysis_model_information`
- generated Markdown containing `Strengths`, `Weaknesses`, `Opportunities`, or
  `Mitigations of Weaknesses`
- unknown extra fields in strict schema-controlled artifacts
- evidence records referencing missing repositories, artifacts, or file paths
- signal, claim, gap, mitigation, or role-family references that do not resolve
- evidence gaps without a follow-up record in `mitigations.jsonl`
- raw chronology data leaking into final report outputs
- missing, empty, or non-PDF generated PDF artifacts
- prohibited generated-output phrasing such as "red flag" framing
- hiring-decision language in `report.md`, `summary-report.md`,
  `screening_brief.md`, or structured ledgers

A valid final report renders as:

- `# Work Behaviour Profile Report`
- `## Scope and Evidence Base`
- `## How to Use This Report`
- `## Executive Work Profile`
- `## Observed Work Behaviour Signals`
- `## Engineering Habits`
- `## Problem-Solving Style`
- `## Work Rhythm and Development Cadence`
- `## Environment Fit`
- `## Role-Family Fit`
- `## Evidence Gaps and Follow-Up Questions`
- `## Confidence and Uncertainty Notes`
- `## Evidence Appendix`

## Status

V0.6 is a local proof of concept. GitHub discovery is public and
unauthenticated. Private repositories, authenticated GitHub access, hosted
services, web UI, live GitHub fetching during local scans, and API-backed LLM
execution are out of scope for v0.6.
