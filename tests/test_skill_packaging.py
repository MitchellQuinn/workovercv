from __future__ import annotations

from pathlib import Path


def test_workovercv_skill_payloads_are_in_sync() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    canonical = repo_root / "skills" / "workovercv"
    copies = [
        repo_root / ".agents" / "skills" / "workovercv",
        repo_root / "adapters" / "codex" / "plugin" / "workovercv" / "skills" / "workovercv",
    ]

    expected_files = _payload_files(canonical)
    assert "SKILL.md" in expected_files
    assert any(path.startswith("docs/") for path in expected_files)
    assert any(path.startswith("schemas/") for path in expected_files)
    assert any(path.startswith("workflows/") for path in expected_files)

    for copy in copies:
        assert _payload_files(copy) == expected_files
        for relative_path in expected_files:
            assert _read_payload_file(copy, relative_path) == _read_payload_file(canonical, relative_path)


def _payload_files(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


def _read_payload_file(root: Path, relative_path: str) -> str:
    return root.joinpath(*relative_path.split("/")).read_text(encoding="utf-8")
