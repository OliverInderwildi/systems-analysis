"""The provenance layer - this part is ours.

Rules enforced here (none of them are in NUREG-0492, which is silent on where numbers
come from):

  P1  No basic event may enter an analysis without a row in the evidence ledger, and that
      row must name an origin and carry a verbatim excerpt locating the number in it.
  P2  Every minimal cut set inherits the WEAKEST evidence class among its basic events.
  P3  The top result is reported as a distribution of probability mass over evidence
      classes, never as a single number standing alone.
  P4  An absence census lists what has no source at all, as a first-class output.
  P5  Importance is reported against evidence class, so that an event which drives the
      result on an asserted number is visible.
  P6  Every element of the tree records who put it there: source, analyst or model.

The rules themselves live in `csakernel`, which every module in this family shares; this
file applies them to fault trees. Vocabularies (generation_method, evidence_class) come from
the Provenance-Based Evidence Audit, so ledgers stay interoperable between modules.
"""
from __future__ import annotations

from typing import Dict, FrozenSet, List

from . import _kernel  # noqa: F401  (puts csakernel on the path if it is a sibling checkout)
from csakernel import (EVIDENCE_CLASSES, GENERATION_METHODS, Ledger, LedgerError,  # noqa: F401
                       absence_census as _kernel_census, require_sourced, weakest)

from .model import FaultTree
from .quant import cutset_probability, fussell_vesely


def _refs(ft: FaultTree) -> Dict[str, str]:
    """The map the kernel works on: each basic event used by the tree -> its ledger row."""
    return {eid: ft.events[eid].ledger_ref for eid in ft.reachable_events()}


def check_provenance(ft: FaultTree, ledger: Ledger) -> None:
    """P1, delegated to the kernel."""
    require_sourced(_refs(ft), ledger, what="basic event")


def absence_census(ft: FaultTree, ledger: Ledger) -> List[dict]:
    """P4, delegated to the kernel; renamed 'item' -> 'event' for this module's readers."""
    return [{**{"event": row["item"]}, **{k: v for k, v in row.items() if k != "item"}}
            for row in _kernel_census(_refs(ft), ledger)]


def evidence_report(ft: FaultTree, ledger: Ledger, cuts: List[FrozenSet[str]]) -> dict:
    check_provenance(ft, ledger)

    per_cut = []
    mass: Dict[str, float] = {c: 0.0 for c in EVIDENCE_CLASSES}
    for cut in cuts:
        classes = [ledger.evidence_class(ft.events[e].ledger_ref) for e in cut]
        cls = weakest(classes)
        p = cutset_probability(sorted(cut), ft)
        per_cut.append({"cut_set": sorted(cut), "probability": p, "evidence_class": cls,
                        "weakest_input": sorted(cut)[classes.index(cls)] if cls in classes else None})
        mass[cls] += p
    total = sum(mass.values()) or 1.0
    share = {k: v / total for k, v in mass.items()}

    fv = fussell_vesely(cuts, ft)
    importance = [
        {"event": eid,
         "fussell_vesely": val,
         "evidence_class": ledger.evidence_class(ft.events[eid].ledger_ref),
         "generation_method": (ledger.get(ft.events[eid].ledger_ref).get("provenance", {}) or {}).get("generation_method"),
         "origin": (ledger.get(ft.events[eid].ledger_ref).get("provenance", {}) or {}).get("origin"),
         "authored_by": ft.events[eid].authored_by}
        for eid, val in fv.items()
    ]

    authorship: Dict[str, int] = {}
    for element in list(ft.gates.values()) + [ft.events[e] for e in ft.reachable_events()]:
        authorship[element.authored_by] = authorship.get(element.authored_by, 0) + 1

    # P5: the headline warning - what drives the result, and on what evidence
    driver = importance[0] if importance else None
    warning = None
    if driver and driver["evidence_class"] in ("asserted", "modelled"):
        warning = (f"the result is driven by {driver['event']} "
                   f"({driver['fussell_vesely']:.0%} of cut-set probability), whose value is "
                   f"{driver['evidence_class']} ({driver['generation_method']}) from {driver['origin']}")

    return {
        "cut_sets": sorted(per_cut, key=lambda r: -r["probability"]),
        "probability_mass_by_evidence_class": mass,
        "share_by_evidence_class": share,
        "weakest_class_carrying_mass": weakest([k for k, v in mass.items() if v > 0]),
        "importance": importance,
        "absence_census": absence_census(ft, ledger),
        "structure_authorship": authorship,
        "warning": warning,
    }
