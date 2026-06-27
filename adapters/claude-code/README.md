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

PDF rendering uses WeasyPrint. Verify the active environment with
`python -m weasyprint --info`; on Windows, native Pango/GObject libraries such
as MSYS2 `mingw-w64-x86_64-pango` must be available on `PATH`.

From a source checkout without an installed console command, use
`PYTHONPATH=src python -m workovercv ...`; on PowerShell, set
`$env:PYTHONPATH = "src"` first.

After collection, the agent must write the required structured artifacts,
render the report, and validate:

```bash
workovercv render --run output/<run>
workovercv validate --run output/<run>
```

`render` writes `report.md`, `summary-report.md`, `screening_brief.md`, and the
matching `report.pdf`, `summary-report.pdf`, and `screening_brief.pdf` files.

Status: untested. Do not claim Claude Code compatibility until an end-to-end
adapter run has been verified.
