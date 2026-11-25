"""The `axiom-knowledge` CLI.

No packaging/console-script entry point exists yet
(`planning/phase-02-adoption-design.md` SS5 defers packaging until a second
real consumer exists) -- invoked exactly like `axiom_validator`'s own CLI,
via `python3 -m axiom_knowledge <args>` with `src/` on PYTHONPATH. Every
reference to `axiom-knowledge <op> ...` in the planning documents refers to
this invocation.
"""
from __future__ import annotations

import argparse
import json
import sys

from . import api
from .errors import AxiomKnowledgeError


def _print_json(obj) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True))


def _print_error(exc: Exception) -> None:
    print(
        json.dumps({"error": type(exc).__name__, "message": str(exc)}, sort_keys=True),
        file=sys.stderr,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="axiom-knowledge")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Explicit repository root. Must contain knowledge/README.md. "
        "Defaults to walking up from the current working directory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    get_parser = subparsers.add_parser("get", help="Retrieve one claim by exact ID.")
    get_parser.add_argument("claim_id")
    get_parser.add_argument("--task-id", default=None)

    find_parser = subparsers.add_parser("find", help="Deterministic claim search.")
    find_parser.add_argument("query")
    find_parser.add_argument("--task-id", default=None)

    task_start_parser = subparsers.add_parser(
        "task-start", help="Record the start of a bounded Axiom-guided unit of work."
    )
    task_start_parser.add_argument("--task-id", required=True)

    task_accepted_parser = subparsers.add_parser(
        "task-accepted", help="Record that a task's acceptance criteria were confirmed met."
    )
    task_accepted_parser.add_argument("--task-id", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "get":
            result = api.get(args.repo_root, args.claim_id, task_id=args.task_id)
            _print_json(result)
            return 0

        if args.command == "find":
            results = api.find(args.repo_root, args.query, task_id=args.task_id)
            _print_json(results)
            return 0

        if args.command == "task-start":
            api.task_start(args.repo_root, args.task_id)
            _print_json({"event": "task_start", "task_id": args.task_id})
            return 0

        if args.command == "task-accepted":
            api.task_accepted(args.repo_root, args.task_id)
            _print_json({"event": "task_accepted", "task_id": args.task_id})
            return 0

        parser.error(f"unknown command '{args.command}'")
        return 2
    except AxiomKnowledgeError as exc:
        _print_error(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
