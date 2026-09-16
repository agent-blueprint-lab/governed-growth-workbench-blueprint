from __future__ import annotations

import argparse
import sys
import sysconfig
from pathlib import Path

from .engine import evaluate
from .io import load_json, write_json
from .safety import scan
from .synthetic import generate_profiles
from .validation import validate_instance, validate_many


def _schema_dir(path: str | None) -> Path:
    if path:
        return Path(path).resolve()
    checkout_schemas = Path.cwd() / "schemas"
    if checkout_schemas.is_dir():
        return checkout_schemas
    return Path(sysconfig.get_path("data")) / "share" / "governed_growth_workbench" / "schemas"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ggw", description="Governed Growth Workbench synthetic reference CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="evaluate synthetic profiles")
    run_parser.add_argument("--profiles", required=True)
    run_parser.add_argument("--rules", required=True)
    run_parser.add_argument("--output", required=True)
    run_parser.add_argument("--audit-output", required=True)
    run_parser.add_argument("--schema-dir", help="schema directory; defaults to checkout or installed data")

    generate_parser = subparsers.add_parser("generate-synthetic", help="create synthetic profiles")
    generate_parser.add_argument("--output", required=True)
    generate_parser.add_argument("--count", type=int, default=12)
    generate_parser.add_argument("--seed", type=int, default=7)
    generate_parser.add_argument("--snapshot-date", default="2026-01-15")
    generate_parser.add_argument("--schema-dir", help="schema directory; defaults to checkout or installed data")

    validate_parser = subparsers.add_parser("validate", help="validate a JSON document")
    validate_parser.add_argument(
        "--kind", choices=("profile", "opportunity", "audit-event", "ruleset"), required=True
    )
    validate_parser.add_argument("--input", required=True)
    validate_parser.add_argument("--schema-dir", help="schema directory; defaults to checkout or installed data")

    scan_parser = subparsers.add_parser(
        "verify-publication", help="scan public files for common sensitive-data patterns"
    )
    scan_parser.add_argument("--root", default=".")
    return parser


def _run(args: argparse.Namespace) -> None:
    profiles = load_json(Path(args.profiles))
    ruleset = load_json(Path(args.rules))
    opportunities, audit_events = evaluate(profiles, ruleset, _schema_dir(args.schema_dir))
    write_json(Path(args.output), opportunities)
    write_json(Path(args.audit_output), audit_events)
    print(f"wrote {len(opportunities)} opportunities and {len(audit_events)} audit events")


def _generate(args: argparse.Namespace) -> None:
    profiles = generate_profiles(args.count, args.seed, args.snapshot_date)
    validate_many(profiles, _schema_dir(args.schema_dir) / "profile-snapshot.schema.json", "profiles")
    write_json(Path(args.output), profiles)
    print(f"wrote {len(profiles)} synthetic profiles")


def _validate(args: argparse.Namespace) -> None:
    schema_name = {
        "profile": "profile-snapshot.schema.json",
        "opportunity": "opportunity.schema.json",
        "audit-event": "audit-event.schema.json",
        "ruleset": "ruleset.schema.json",
    }[args.kind]
    value = load_json(Path(args.input))
    if isinstance(value, list):
        validate_many(value, _schema_dir(args.schema_dir) / schema_name, args.kind)
    else:
        validate_instance(value, _schema_dir(args.schema_dir) / schema_name, args.kind)
    print("valid")


def _scan(args: argparse.Namespace) -> None:
    findings = scan(Path(args.root))
    if findings:
        for finding in findings:
            print(f"{finding.path}:{finding.line}: {finding.rule}", file=sys.stderr)
        raise SystemExit(1)
    print("publication scan passed")


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        {
            "run": _run,
            "generate-synthetic": _generate,
            "validate": _validate,
            "verify-publication": _scan,
        }[args.command](args)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    return 0
