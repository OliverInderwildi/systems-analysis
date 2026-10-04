"""Command line: score an ACH matrix against its evidence ledger.

    python3 -m pach.cli analyse MATRIX.json LEDGER.json [--json OUT.json]
"""
from __future__ import annotations

import argparse
import json
import sys

from csakernel import Ledger, LedgerError

from .model import MatrixError, load_matrix
from .report import ach_report


def _fmt(rep: dict) -> str:
    out = ["Hypotheses, least inconsistent first (Heuer: the one hardest to reject):"]
    for row in rep["hypotheses_least_inconsistent_first"]:
        out.append(f"  {row['hypothesis']:<6} {row['weighted_inconsistency']:6.2f}  "
                   f"[{row['authored_by']}]  {row['text']}")
    out.append("")
    out.append("Evidence by diagnosticity (what actually separates the hypotheses):")
    for row in rep["evidence_by_diagnosticity"]:
        out.append(f"  {row['evidence']:<6} {row['diagnosticity']:5.2f}  "
                   f"{row['evidence_class']:<12} w={row['weight']:.2f}  {row['text'][:54]}")
    out.append("")
    out.append(f"Conclusion rests on evidence that is: {rep['conclusion_evidence_class']}")
    out.append("Authorship: " + ", ".join(f"{k}={v}" for k, v in sorted(rep["authorship"].items())))
    if rep["absence_census"]:
        out.append("")
        out.append(f"Absence census ({len(rep['absence_census'])}):")
        for row in rep["absence_census"]:
            out.append(f"  {row['item']:<6} {row['missing']}")
    for w in rep["warnings"]:
        out.append(f"WARNING: {w}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pach", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    an = sub.add_parser("analyse")
    an.add_argument("matrix")
    an.add_argument("ledger")
    an.add_argument("--json", dest="json_out")
    args = ap.parse_args(argv)
    try:
        m = load_matrix(args.matrix)
        led = Ledger.load(args.ledger)
        rep = ach_report(m, led)
    except (MatrixError, LedgerError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print(_fmt(rep))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
