"""Scoring, after Heuer: hypotheses are judged by the evidence against them, not for them.

  inconsistency score : weighted sum of the disconfirming ratings for each hypothesis
                        (II counts 2, I counts 1, everything else 0)
  ranking             : least inconsistency first - the hypothesis hardest to reject
  diagnosticity       : evidence that rates differently across hypotheses discriminates;
                        evidence consistent with everything does no work

OUR ADAPTATION: Heuer has the analyst assign each item of evidence a credibility weight by
judgement. Here the weight comes from the evidence class in the ledger, so that the weighting
is traceable to a source rather than to an opinion. Set weights explicitly to override.
"""
from __future__ import annotations

from typing import Dict, Mapping

from .model import Matrix

INCONSISTENCY = {"II": 2.0, "I": 1.0, "N": 0.0, "C": 0.0, "CC": 0.0, "NA": 0.0}

# our adaptation: ledger evidence class -> weight
CLASS_WEIGHT = {"established": 1.0, "demonstrated": 0.8, "modelled": 0.5, "asserted": 0.25}


def inconsistency_scores(m: Matrix, weights: Mapping[str, float] | None = None) -> Dict[str, float]:
    weights = weights or {eid: 1.0 for eid in m.evidence}
    out: Dict[str, float] = {}
    for hid in m.hypotheses:
        total = 0.0
        for eid, row in m.ratings.items():
            total += INCONSISTENCY[row[hid]] * float(weights.get(eid, 1.0))
        out[hid] = total
    return out


def rank_hypotheses(m: Matrix, weights: Mapping[str, float] | None = None):
    """Least inconsistent first. Ties are kept as ties, not broken silently."""
    scores = inconsistency_scores(m, weights)
    return sorted(scores.items(), key=lambda kv: (kv[1], kv[0]))


def diagnosticity(m: Matrix, weights: Mapping[str, float] | None = None) -> Dict[str, float]:
    """How much an item of evidence separates the hypotheses.

    Zero when every hypothesis gets the same rating (the evidence is consistent with
    everything and therefore tells you nothing); larger as the ratings spread.
    """
    weights = weights or {eid: 1.0 for eid in m.evidence}
    out: Dict[str, float] = {}
    for eid, row in m.ratings.items():
        values = [INCONSISTENCY[row[hid]] for hid in m.hypotheses]
        spread = max(values) - min(values)
        distinct = len(set(values)) - 1
        out[eid] = (spread + distinct) / 2.0 * float(weights.get(eid, 1.0))
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def weights_from_ledger(m: Matrix, ledger) -> Dict[str, float]:
    return {eid: CLASS_WEIGHT[ledger.evidence_class(ev.ledger_ref)]
            for eid, ev in m.evidence.items()}
