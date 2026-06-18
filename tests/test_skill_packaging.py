from __future__ import annotations

from pathlib import Path


def test_workovercv_skill_copies_are_in_sync() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    canonical = repo_root / "skills" / "workovercv" / "SKILL.md"
    copies = [
        repo_root / ".agents" / "skills" / "workovercv" / "SKILL.md",
        repo_root / "adapters" / "codex" / "plugin" / "workovercv" / "skills" / "workovercv" / "SKILL.md",
    ]

    canonical_text = canonical.read_text(encoding="utf-8")
    for copy in copies:
        assert copy.read_text(encoding="utf-8") == canonical_text
