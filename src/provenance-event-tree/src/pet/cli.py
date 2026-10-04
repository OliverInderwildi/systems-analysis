"""Command line: run an event tree against its evidence ledger.

    python3 -m pet.cli analyse MODEL.json LEDGER.json [--json OUT.json]

Refused if any input lacks provenance. That refusal is the feature.
"""
from __future__ import annotations

import argparse
import json
import sys

from csakernel import Ledger, LedgerError

from .fmt import decimal

from .evidence import event_tree_report
from .model import ModelError, load_model


def _fmt(rep: dict) -> str:
    ini = rep["initiator"]
    out = [f"Initiating event : {ini['label']}  {decimal(ini['frequency'])} per period "
           f"({ini['evidence_class']})", ""]
    out.append("End states, most severe first:")
    for state, freq in rep["end_state_frequencies"].items():
        by = rep["end_state_evidence"].get(state, {})
        worst = min(by, key=lambda c: ["asserted", "modelled", "demonstrated",
                                       "established"].index(c)) if by else "-"
        out.append(f"  {state:<38} {decimal(freq):<14} weakest: {worst}")
    out.append("")
    out.append(f"Paths to '{rep['worst_end_state']}':")
    for row in rep["paths_to_worst"]:
        failed = ", ".join(row["failed"]) or "-"
        out.append(f"  {row['sequence']}  {row['pattern']}  {decimal(row['frequency']):<14}"
                   f"{row['evidence_class']:<13} failed: {failed}")
    out.append("")
    out.append("All sequences:")
    for row in rep["sequences"]:
        out.append(f"  {row['sequence']}  {row['pattern']}  {decimal(row['frequency']):<14}"
                   f"{row['evidence_class']:<13} {row['end_state']}")
    out.append("")
    out.append(f"Closure check: paths sum to {1 + rep['closure_error']:.9f} (should be 1)")
    if rep["absence_census"]:
        out.append("")
        out.append(f"Absence census ({len(rep['absence_census'])}):")
        for row in rep["absence_census"]:
            out.append(f"  {row['item']:<10} {row['missing']}")
    out.append("")
    out.append("Authorship: " + ", ".join(f"{k}={v}" for k, v in sorted(rep["authorship"].items())))
    for w in rep["warnings"]:
        out.append(f"WARNING: {w}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pet", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    an = sub.add_parser("analyse")
    an.add_argument("model")
    an.add_argument("ledger")
    an.add_argument("--json", dest="json_out")
    args = ap.parse_args(argv)
    try:
        tree = load_model(args.model)
        ledger = Ledger.load(args.ledger)
        rep = event_tree_report(tree, ledger)
    except (ModelError, LedgerError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print(_fmt(rep))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
