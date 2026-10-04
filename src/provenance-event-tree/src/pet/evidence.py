"""The provenance layer, applied to event trees.

The rules live in csakernel and are shared with the other tools; this file says what they mean
here: which items must be sourced (the initiating frequency and every barrier probability),
and how weak evidence propagates (through the barriers that actually failed on a path).
"""
from __future__ import annotations

from typing import Dict, List

from . import _kernel  # noqa: F401
from csakernel import Ledger, absence_census as _census, require_sourced, weakest  # noqa: E402

from .model import EventTree
from .fmt import decimal
from .quant import closure_error, end_state_frequencies
from .sequences import Sequence, sequences


def _refs(tree: EventTree) -> Dict[str, str]:
    refs = {tree.initiator.id: tree.initiator.ledger_ref}
    refs.update({b.id: b.ledger_ref for b in tree.barriers})
    return refs


def check_provenance(tree: EventTree, ledger: Ledger) -> None:
    """P1: no path may be quantified on an unsourced number."""
    require_sourced(_refs(tree), ledger, what="event tree input")


def sequence_evidence(tree: EventTree, ledger: Ledger, seq: Sequence) -> str:
    """P2, our reading of it for this method.

    A path's weakest class is taken over the initiating event and the barriers that FAILED on
    it - the numbers that carry the path's probability. Barriers that held contribute their
    complement, which is insensitive to the same degree of error, so including them would
    flatten every sequence to the same class and say nothing.
    """
    refs = [tree.initiator.ledger_ref]
    refs += [b.ledger_ref for b in tree.barriers if b.id in seq.failed]
    return weakest([ledger.evidence_class(r) for r in refs])


def event_tree_report(tree: EventTree, ledger: Ledger) -> dict:
    check_provenance(tree, ledger)
    seqs = sequences(tree)
    totals = end_state_frequencies(tree, seqs)

    rows = []
    for s in seqs:
        cls = sequence_evidence(tree, ledger, s)
        rows.append({
            "sequence": s.id, "pattern": s.pattern, "end_state": s.end_state,
            "frequency": s.frequency, "conditional": s.conditional,
            "failed": [tree.label(b) for b in tree.barriers if b.id in s.failed],
            "evidence_class": cls,
        })

    mass: Dict[str, Dict[str, float]] = {}
    for row, s in zip(rows, seqs):
        by_class = mass.setdefault(s.end_state, {})
        by_class[row["evidence_class"]] = by_class.get(row["evidence_class"], 0.0) + s.frequency

    worst = max(totals, key=lambda st: (tree.severity.get(st, 0), totals[st])) if totals else ""
    to_worst = sorted((r for r in rows if r["end_state"] == worst),
                      key=lambda r: -r["frequency"])

    authorship: Dict[str, int] = {}
    for item in [tree.initiator] + list(tree.barriers):
        authorship[item.authored_by] = authorship.get(item.authored_by, 0) + 1

    warnings: List[str] = []
    err = closure_error(tree, seqs)
    if err > 1e-9:
        warnings.append(f"paths do not close: conditional probabilities sum to "
                        f"{1 + err:.6f}, not 1")
    if to_worst:
        lead = to_worst[0]
        if lead["evidence_class"] in ("asserted", "modelled"):
            warnings.append(f"the leading path to '{worst}' ({lead['sequence']}, "
                            f"{decimal(lead['frequency'])} per period) rests on {lead['evidence_class']} "
                            "evidence")
    coupled = [b for b in tree.barriers if b.from_fault_tree]
    if coupled:
        warnings.append(f"{len(coupled)} barrier probability(ies) come from a fault tree; the "
                        "evidence class shown is that of the fault tree's weakest input")
    if authorship.get("model"):
        warnings.append(f"{authorship['model']} element(s) of this tree were proposed by a "
                        "language model, not found in a source")

    return {
        "initiator": {"id": tree.initiator.id, "label": tree.label(tree.initiator),
                      "frequency": tree.initiator.frequency,
                      "evidence_class": ledger.evidence_class(tree.initiator.ledger_ref)},
        "sequences": rows,
        "end_state_frequencies": totals,
        "end_state_evidence": mass,
        "worst_end_state": worst,
        "paths_to_worst": to_worst,
        "closure_error": err,
        "absence_census": [{**{"item": r["item"]}, **{k: v for k, v in r.items() if k != "item"}}
                           for r in _census(_refs(tree), ledger)],
        "authorship": authorship,
        "warnings": warnings,
    }
