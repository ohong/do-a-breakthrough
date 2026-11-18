#!/usr/bin/env python3
"""CLI for exact hypercube permutation-routing feasibility."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from routing import RoutingResult, solve_routing


def _result_json(result: RoutingResult) -> dict[str, object]:
    return {
        "status": result.status,
        "dimension": result.dimension,
        "shortest_only": result.shortest_only,
        "elapsed_seconds": result.elapsed_seconds,
        "permutation": list(result.permutation),
        "paths": (
            {str(source): list(path) for source, path in result.paths.items()}
            if result.paths is not None
            else None
        ),
        "reason_unknown": result.reason_unknown,
        "solver_statistics": result.solver_statistics,
        "z3_version": __import__("z3").get_version_string(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check directed arc-disjoint routing in Q_d"
    )
    parser.add_argument("instance", type=Path, help="JSON instance file")
    parser.add_argument(
        "--shortest-only",
        action="store_true",
        help="calibration control: allow only distance-decreasing arcs",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=240.0,
        help="Z3 timeout, default 240 seconds",
    )
    parser.add_argument("--output", type=Path, help="write result JSON here")
    parser.add_argument(
        "--smt2",
        type=Path,
        help="also preserve the exact SMT-LIB instance",
    )
    args = parser.parse_args()
    if args.timeout_seconds <= 0 or args.timeout_seconds > 295:
        parser.error("timeout must be in (0, 295] seconds")

    payload = json.loads(args.instance.read_text())
    result = solve_routing(
        payload["dimension"],
        payload["permutation"],
        shortest_only=args.shortest_only,
        timeout_ms=round(args.timeout_seconds * 1000),
        include_smt2=args.smt2 is not None,
    )
    rendered = json.dumps(_result_json(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        sys.stdout.write(rendered)
    if args.smt2:
        if result.smt2 is None:
            raise RuntimeError("SMT-LIB output was not retained")
        args.smt2.parent.mkdir(parents=True, exist_ok=True)
        args.smt2.write_text(result.smt2)
    return 0 if result.status != "unknown" else 2


if __name__ == "__main__":
    raise SystemExit(main())
