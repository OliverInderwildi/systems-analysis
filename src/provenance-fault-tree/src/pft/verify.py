"""An independent check on the cut-set arithmetic.

The main path is the one in the handbook: expand the tree into minimal cut sets, then take the
probability of their union. This module computes the same number by a different route - it
evaluates the tree's structure function over every combination of basic-event states and sums
the probabilities of the states in which the top event occurs.

The two routes share no code beyond the model itself, so agreement is real evidence and
disagreement is a bug. Exhaustive enumeration is exponential, so this is for small models
(<= 22 basic events by default) and for tests, not for production runs.
"""
from __future__ import annotations

from itertools import product
from typing import Dict, List

from .model import FaultTree

MAX_EVENTS = 22


def evaluate(ft: FaultTree, state: Dict[str, bool]) -> bool:
    """True if the top event occurs when the basic events take the given states."""

    def node(nid: str) -> bool:
        if nid in ft.events:
            return state[nid]
        gate = ft.gates[nid]
        if gate.type == "AND":
            return all(node(c) for c in gate.inputs)
        return any(node(c) for c in gate.inputs)

    return node(ft.top)


def exact_top_probability(ft: FaultTree) -> float:
    """Sum the probabilities of every state in which the top event occurs."""
    events: List[str] = ft.reachable_events()
    if len(events) > MAX_EVENTS:
        raise ValueError(f"{len(events)} basic events is too many for exhaustive checking "
                         f"(limit {MAX_EVENTS}); use the cut-set path or SCRAM")
    total = 0.0
    for combo in product((False, True), repeat=len(events)):
        state = dict(zip(events, combo))
        if not evaluate(ft, state):
            continue
        p = 1.0
        for eid, on in state.items():
            pe = ft.events[eid].probability
            p *= pe if on else (1.0 - pe)
        total += p
    return total
