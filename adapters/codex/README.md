# Codex Adapter

This adapter makes WorkOverCV discoverable to Codex-style agents without
changing the WorkOverCV workflow or CLI.

The canonical workflow remains `workflows/workovercv.yml`. The shared runtime
contract remains `docs/runtime_contract.md`. The review scope boundary remains
`docs/manifest_contract.md`.

## Personal Skill Install

For a user-wide Codex skill, copy `skills/workovercv` to your personal Codex
skills directory:

```cmd
mkdir "%USERPROFILE%\.agents\skills\workovercv"
xcopy /E /I /Y "C:\Development\agentic-skills\workovercv\skills\workovercv" "%USERPROFILE%\.agents\skills\workovercv"
```

Or copy the folder manually in Explorer:

- from: `C:\Development\agentic-skills\workovercv\skills\workovercv`
- to: `C:\Users\Mitch\.agents\skills\workovercv`

Restart Codex or start a new Codex thread after copying the skill.

## Repo Skill Install

From the repository root, install the repo-scoped Codex skill:

```bash
./adapters/codex/install.sh
```

On Windows PowerShell:

```powershell
.\adapters\codex\install.ps1
```

If PowerShell blocks unsigned scripts, either run the script with a one-time
process bypass:

```powershell
powershell -ExecutionPolicy Bypass -File .\adapters\codex\install.ps1
```

Or install the skill manually:

```powershell
New-Item -ItemType Directory -Force -Path .\.agents\skills\workovercv
Copy-Item -Path .\skills\workovercv\* -Destination .\.agents\skills\workovercv -Recurse -Force
```

The install scripts copy `skills/workovercv` to
`.agents/skills/workovercv`, which is the Codex repo-skill discovery location.
They do not install Python dependencies or alter the WorkOverCV runtime.

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

## Boundaries

The adapter must not:

- redefine the workflow
- use repositories not selected in `review_scope.yml`
- silently change output paths
- embed a separate LLM API runtime
- infer protected/private traits
- make a hiring recommendation
- treat stars, forks, watchers, or followers as competence metrics

## Optional Plugin Package

`adapters/codex/plugin/workovercv` contains a local Codex plugin package that
bundles the same WorkOverCV skill. This is packaging only; the canonical
workflow and runtime contract remain in the WorkOverCV repository.

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
