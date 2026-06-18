# Claude Code Adapter

This adapter installs the WorkOverCV skill for Claude Code-style agents.

The canonical workflow remains `workflows/workovercv.yml`.
The shared runtime contract remains `docs/runtime_contract.md`.
The review scope boundary remains `docs/manifest_contract.md`.

Run GitHub-profile assessments with the shared CLI:

```bash
workovercv discover --candidate https://github.com/<user>
workovercv collect --scope output/<run>/review_scope.yml
```

From a source checkout without an installed console command, use
`PYTHONPATH=src python -m workovercv ...`; on PowerShell, set
`$env:PYTHONPATH = "src"` first.

After collection, the agent must write the required structured artifacts,
render the report, and validate:

```bash
workovercv render --run output/<run>
workovercv validate --run output/<run>
```

Status: untested. Do not claim Claude Code compatibility until an end-to-end
adapter run has been verified.
