from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analysis import analyze_run
from .collect import collect_from_scope
from .github import GitHubError, discover_candidate
from .manifest import ManifestError
from .render import render_report
from .scan import scan_local_path
from .validation import validate_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="workovercv")
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser("discover", help="Discover public repositories for a GitHub profile")
    discover.add_argument("--candidate", required=True, help="Public GitHub profile URL")
    discover.add_argument("--out", default="output", help="Output root for timestamped run directories")

    scan = subparsers.add_parser("scan", help="Run an offline deterministic scan of a local repository path")
    scan.add_argument("path", help="Local repository path to scan")
    scan.add_argument("--out", default="output", help="Output root for timestamped run directories")
    scan.add_argument("--report-mode", choices=["summary", "audit"], default="audit", help="report.md rendering mode; Markdown and PDF outputs are generated")

    collect = subparsers.add_parser("collect", help="Collect artifacts from repositories selected in review_scope.yml")
    collect.add_argument("--scope", required=True, help="Path to review_scope.yml")
    collect.add_argument("--work-root", help="Controlled worktree root for cloned repositories")
    collect.add_argument("--keep-worktrees", action="store_true", help="Keep cloned worktrees after collection")

    analyze = subparsers.add_parser("analyze", help="Build deterministic analysis artifacts for a collected run")
    analyze.add_argument("--run", required=True, help="Run directory containing collected artifacts")

    render = subparsers.add_parser("render", help="Render Markdown and PDF reports from report.json")
    render.add_argument("--run", required=True, help="Run directory containing report.json")
    render.add_argument("--mode", choices=["summary", "audit"], default="audit", help="report.md rendering mode; Markdown and PDF outputs are generated")

    validate = subparsers.add_parser("validate", help="Validate a completed WorkOverCV run")
    validate.add_argument("--run", required=True, help="Run directory to validate")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "discover":
            run_dir = discover_candidate(args.candidate, Path(args.out))
            print(run_dir)
            return 0
        if args.command == "scan":
            run_dir = scan_local_path(Path(args.path), Path(args.out), report_mode=args.report_mode)
            print(run_dir)
            return 0
        if args.command == "collect":
            run_dir = collect_from_scope(
                Path(args.scope),
                work_root=Path(args.work_root).expanduser() if args.work_root else None,
                keep_worktrees=args.keep_worktrees,
            )
            print(run_dir)
            return 0
        if args.command == "analyze":
            run_dir = analyze_run(Path(args.run))
            print(run_dir)
            return 0
        if args.command == "render":
            report_path = render_report(Path(args.run), mode=args.mode)
            print(report_path)
            return 0
        if args.command == "validate":
            result = validate_run(Path(args.run))
            if result.ok:
                print("validation passed")
                return 0
            for error in result.errors:
                print(f"error: {error}", file=sys.stderr)
            return 3
    except ManifestError as exc:
        print(f"manifest error: {exc}", file=sys.stderr)
        return 2
    except (GitHubError, FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.error(f"Unhandled command: {args.command}")
    return 1
