"""Command line: analyse a fault tree together with its evidence ledger.

    python3 -m pft.cli analyse MODEL.json LEDGER.json [--json OUT.json] [--mef OUT.xml]

The analysis is refused if any input lacks provenance. That refusal is the feature.
"""
from __future__ import annotations

import argparse
import json
import sys

from .cutsets import minimal_cut_sets
from .fmt import decimal
from .evidence import Ledger, LedgerError, evidence_report
from .mef import to_mef
from .model import ModelError, load_model
from .quant import top_probability


def _fmt(report: dict, top_p: float) -> str:
    lines = []
    lines.append(f"Top event probability : {decimal(top_p, 4)}")
    lines.append(f"Weakest evidence class carrying probability: {report['weakest_class_carrying_mass']}")
    if report["warning"]:
        lines.append(f"WARNING: {report['warning']}")
    lines.append("")
    lines.append("Minimal cut sets (probability, evidence class):")
    for row in report["cut_sets"]:
        lines.append(f"  {' AND '.join(row['cut_set']):<28} {decimal(row['probability']):<14}"
                     f"{row['evidence_class']}")
    lines.append("")
    lines.append("Probability mass by evidence class:")
    for cls, share in report["share_by_evidence_class"].items():
        if share:
            lines.append(f"  {cls:<13} {share:6.1%}")
    lines.append("")
    lines.append("Importance (Fussell-Vesely) against evidence:")
    for row in report["importance"]:
        lines.append(f"  {row['event']:<10} {row['fussell_vesely']:6.1%}  {row['evidence_class']:<12}"
                     f" {str(row['generation_method']):<10} by {row['authored_by']:<8} src: {row['origin']}")
    lines.append("")
    lines.append(f"Absence census ({len(report['absence_census'])} entries):")
    for row in report["absence_census"]:
        lines.append(f"  {row['event']:<10} {row['missing']}")
    lines.append("")
    lines.append("Tree authorship: " + ", ".join(f"{k}={v}" for k, v in sorted(report["structure_authorship"].items())))
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pft", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    an = sub.add_parser("analyse", help="analyse a model against its ledger")
    an.add_argument("model")
    an.add_argument("ledger")
    an.add_argument("--json", dest="json_out", help="write the full report as JSON")
    an.add_argument("--mef", dest="mef_out", help="write the model in Open-PSA format for SCRAM")
    args = ap.parse_args(argv)

    try:
        ft = load_model(args.model)
        ledger = Ledger.load(args.ledger)
        cuts = minimal_cut_sets(ft)
        report = evidence_report(ft, ledger, cuts)
    except (ModelError, LedgerError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2

    top_p = top_probability(cuts, ft)
    report["top_probability"] = top_p
    print(_fmt(report, top_p))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, default=list)
    if args.mef_out:
        with open(args.mef_out, "w", encoding="utf-8") as fh:
            fh.write(to_mef(ft))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
