# Codex Adapter

This adapter makes WorkOverCV discoverable to Codex-style agents without
changing the WorkOverCV workflow or CLI.

The canonical workflow remains `workflows/workovercv.yml`. The shared runtime
contract remains `docs/runtime_contract.md`. The review scope boundary remains
`docs/manifest_contract.md`.

## Personal Plugin Install

Install WorkOverCV as a personal Codex plugin. The plugin package lives at
`adapters/codex/plugin/workovercv` and bundles the WorkOverCV skill plus the
workflow, runtime contract, manifest contract, safety guidance, and schemas
that the skill reads at runtime.

From the repository root:

```bash
./adapters/codex/install.sh
```

On Windows PowerShell:

```powershell
.\adapters\codex\install.ps1
```

If PowerShell blocks unsigned scripts, run the script with a one-time process
bypass:

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\codex\install.ps1
```

The install scripts copy the local plugin source to:

```text
~/plugins/workovercv
```

They also create or update the default personal marketplace file:

```text
~/.agents/plugins/marketplace.json
```

Then install from the personal marketplace:

```powershell
codex plugin add workovercv@personal
```

Start a new Codex thread after installing so Codex picks up the plugin-provided
skill.

## Runtime Install

Install the shared WorkOverCV CLI in the active Python environment:

```powershell
python -m pip install -e C:\Development\agentic-skills\workovercv
```

Verify:

```powershell
where workovercv
workovercv --help
python -m weasyprint --info
```

PDF rendering uses WeasyPrint. On Windows, install native Pango/GObject
libraries such as MSYS2 `mingw-w64-x86_64-pango` and make
`C:\msys64\mingw64\bin` available on `PATH`.

## Required Behavior

Codex must use the shared CLI for deterministic data gathering:

```bash
workovercv discover --candidate https://github.com/<user>
workovercv collect --scope output/<run>/review_scope.yml
```

When working from a source checkout without installing the package, use the same
arguments through the module entry point:

```bash
PYTHONPATH=src python -m workovercv discover --candidate https://github.com/<user>
PYTHONPATH=src python -m workovercv collect --scope output/<run>/review_scope.yml
```

On PowerShell, set `$env:PYTHONPATH = "src"` once, then run
`python -m workovercv ...`.

After collection, Codex may run deterministic rubric analysis:

```bash
workovercv analyze --run output/<run>
```

For agent-authored analysis, Codex performs the judgement stages using only the
review scope, inventories, and `review_corpus.jsonl` unless the user explicitly
runs discovery or collection again.

Codex must write:

- `explicit_claims.jsonl`
- `signal_ledger.jsonl`
- `evidence_map.jsonl`
- `gap_register.jsonl`
- `role_family_fit.json`
- `mitigations.jsonl`
- `red_team_review.json`
- `report.json`

When `report.json` is complete, Codex must run:

```bash
workovercv render --run output/<run>
workovercv validate --run output/<run>
```

`render` writes `report.md`, `summary-report.md`, `screening_brief.md`, and the
matching `report.pdf`, `summary-report.pdf`, and `screening_brief.pdf` files.

## Boundaries

The adapter must not:

- redefine the workflow
- use repositories not selected in `review_scope.yml`
- silently change output paths
- embed a separate LLM API runtime
- infer protected/private traits
- make a hiring recommendation
- treat stars, forks, watchers, or followers as competence metrics

## Plugin Package

`adapters/codex/plugin/workovercv` contains a local Codex plugin package that
bundles the WorkOverCV skill with the workflow docs and schemas needed for
progressive disclosure. This is packaging only; the canonical workflow and
runtime contract remain in the WorkOverCV repository root.

## Verification

Use `adapters/codex/VERIFY.md` for the Codex smoke-test procedure. The recorded
GitHub-profile smoke in `adapters/codex/SMOKE.md` predates the v0.6 report-shape
and output-quality contract and should be rerun before claiming v0.6 adapter compatibility. A valid
final run verifies the required WorkOverCV artifacts and a `run_manifest.json`
with:

- `tool_name`: `workovercv`
- `workflow_id`: `workovercv.repository-employment-signal`
- final `status`: `complete`

Status: v0.6 retest required for the GitHub-profile Codex adapter smoke. Do not
claim a separate Codex plugin-install smoke unless one is separately recorded.
