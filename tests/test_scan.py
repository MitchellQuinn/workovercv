from __future__ import annotations

from pathlib import Path

from workovercv.scan import scan_local_path
from workovercv.validation import validate_run


def test_scan_local_path_writes_valid_run(tmp_path: Path) -> None:
    fixture = Path("tests/fixtures/small_repo").resolve()

    run_dir = scan_local_path(fixture, tmp_path / "output")
    result = validate_run(run_dir, update_manifest=False)

    assert result.ok, result.errors
    assert (run_dir / "report.md").exists()
    assert (run_dir / "summary-report.md").exists()
    assert (run_dir / "screening_brief.md").exists()
    assert (run_dir / "report.pdf").read_bytes().startswith(b"%PDF-")
    assert (run_dir / "summary-report.pdf").read_bytes().startswith(b"%PDF-")
    assert (run_dir / "screening_brief.pdf").read_bytes().startswith(b"%PDF-")
    assert (run_dir / "signal_ledger.jsonl").exists()
    assert (run_dir / "role_family_fit.json").exists()
    assert (run_dir / "work_chronology.json").exists()
    markdown = (run_dir / "report.md").read_text(encoding="utf-8")
    assert "# Work Behaviour Profile Report" in markdown
    assert "## Strengths" not in markdown
    summary_markdown = (run_dir / "summary-report.md").read_text(encoding="utf-8")
    assert "# Work Behaviour Profile Summary" in summary_markdown
    assert "## Top Observed Work Behaviour Signals" in summary_markdown
