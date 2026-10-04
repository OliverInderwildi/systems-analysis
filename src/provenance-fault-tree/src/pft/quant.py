"""Quantitative evaluation of a fault tree from its minimal cut sets.

Follows NUREG-0492 ch. XI. Basic events are treated as independent.

  cut set probability  : product of the probabilities of its basic events
  top probability      : probability of the union of the cut sets
                         - exact by inclusion-exclusion when the number of cut sets is small
                         - otherwise the rare-event approximation (sum), which is an upper bound
  Fussell-Vesely       : share of the top probability carried by cut sets containing an event
"""
from __future__ import annotations

from itertools import combinations
from typing import Dict, FrozenSet, List, Sequence

from .model import FaultTree

EXACT_LIMIT = 16  # above this many cut sets, inclusion-exclusion is not worth the terms


def cutset_probability(cut: Sequence[str], ft: FaultTree) -> float:
    p = 1.0
    for eid in cut:
        p *= ft.events[eid].probability
    return p


def top_probability(cuts: List[FrozenSet[str]], ft: FaultTree, exact: bool | None = None) -> float:
    if not cuts:
        return 0.0
    use_exact = (len(cuts) <= EXACT_LIMIT) if exact is None else exact
    if not use_exact:
        return min(1.0, sum(cutset_probability(c, ft) for c in cuts))
    total = 0.0
    for k in range(1, len(cuts) + 1):
        sign = 1.0 if k % 2 else -1.0
        for combo in combinations(cuts, k):
            union: set = set()
            for c in combo:
                union |= c
            total += sign * cutset_probability(sorted(union), ft)
    return max(0.0, min(1.0, total))


def fussell_vesely(cuts: List[FrozenSet[str]], ft: FaultTree) -> Dict[str, float]:
    denom = sum(cutset_probability(c, ft) for c in cuts)
    if denom <= 0.0:
        return {e: 0.0 for e in ft.reachable_events()}
    out: Dict[str, float] = {}
    for eid in ft.reachable_events():
        num = sum(cutset_probability(c, ft) for c in cuts if eid in c)
        out[eid] = num / denom
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))
