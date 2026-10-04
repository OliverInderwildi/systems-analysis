"""Applying the kernel's recording rules to an ACH matrix."""
from __future__ import annotations

import os
import sys
from typing import Dict, List

try:
    import csakernel  # noqa: F401
except ImportError:  # sibling checkout
    _here = os.path.dirname(__file__)
    for _sib in (os.path.abspath(os.path.join(_here, "..", "..", "..", "csakernel", "src")),
                 os.path.abspath(os.path.join(_here, "..", "..", "..", "CSAKernel", "src"))):
        if os.path.isdir(_sib):
            sys.path.insert(0, _sib)
            break
    else:
        raise

from csakernel import Ledger, absence_census, require_sourced, weakest  # noqa: E402

from .model import Matrix  # noqa: E402
from .score import diagnosticity, rank_hypotheses, weights_from_ledger  # noqa: E402


def ach_report(m: Matrix, ledger: Ledger) -> dict:
    refs = {eid: ev.ledger_ref for eid, ev in m.evidence.items()}
    require_sourced(refs, ledger, what="item of evidence")   # P1

    weights = weights_from_ledger(m, ledger)
    ranked = rank_hypotheses(m, weights)
    diag = diagnosticity(m, weights)

    # P2: the conclusion inherits the weakest evidence among the items that did the work
    workers = [eid for eid, d in diag.items() if d > 0]
    conclusion_class = weakest([ledger.evidence_class(m.evidence[e].ledger_ref) for e in workers])

    top_scores = [s for _, s in ranked]
    tie = len(top_scores) > 1 and abs(top_scores[0] - top_scores[1]) < 1e-9

    hypotheses = [{
        "hypothesis": hid,
        "text": m.hypotheses[hid].text,
        "weighted_inconsistency": score,
        "authored_by": m.hypotheses[hid].authored_by,
    } for hid, score in ranked]

    evidence = [{
        "evidence": eid,
        "text": m.evidence[eid].text,
        "diagnosticity": diag[eid],
        "weight": weights[eid],
        "evidence_class": ledger.evidence_class(m.evidence[eid].ledger_ref),
        "origin": ledger.origin(m.evidence[eid].ledger_ref),
        "authored_by": m.evidence[eid].authored_by,
    } for eid in diag]

    authorship: Dict[str, int] = {}
    for item in list(m.hypotheses.values()) + list(m.evidence.values()):
        authorship[item.authored_by] = authorship.get(item.authored_by, 0) + 1

    warnings: List[str] = []
    if tie:
        warnings.append(f"{hypotheses[0]['hypothesis']} and {hypotheses[1]['hypothesis']} are "
                        "equally hard to reject; the matrix does not separate them")
    inert = [eid for eid, d in diag.items() if d == 0]
    if inert:
        warnings.append(f"{len(inert)} item(s) of evidence do no work ({', '.join(inert)}): "
                        "consistent with every hypothesis")
    if conclusion_class in ("asserted", "modelled"):
        warnings.append(f"the discriminating evidence is only {conclusion_class}")
    if authorship.get("model"):
        warnings.append(f"{authorship['model']} element(s) of this matrix were proposed by a "
                        "language model, not found in a source")

    return {
        "hypotheses_least_inconsistent_first": hypotheses,
        "evidence_by_diagnosticity": evidence,
        "conclusion_evidence_class": conclusion_class,
        "authorship": authorship,
        "absence_census": absence_census(refs, ledger),   # P4
        "warnings": warnings,
    }
