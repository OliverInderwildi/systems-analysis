"""Minimal cut sets by top-down expansion (MOCUS).

Procedure as described in NUREG-0492 ch. VII: starting from the top event, replace each
gate by its inputs - an OR gate increases the number of cut sets (new rows), an AND gate
increases the size of a cut set (new columns) - then discard any set that contains another.
"""
from __future__ import annotations

from typing import FrozenSet, List, Set

from .model import FaultTree


def expand_steps(ft: FaultTree):
    """Yield the working set after each gate replacement.

    Used for teaching and for the animation in docs/: an OR gate adds rows, an AND gate
    adds columns, exactly as described in NUREG-0492 ch. VII.
    """
    working: List[Set[str]] = [{ft.top}]
    finished: List[Set[str]] = []
    yield {"replaced": None, "rule": "start", "sets": [set(s) for s in working + finished]}
    while working:
        current = working.pop()
        gate_id = next((x for x in current if x in ft.gates), None)
        if gate_id is None:
            finished.append(current)
            continue
        gate = ft.gates[gate_id]
        rest = current - {gate_id}
        if gate.type == "OR":
            for child in gate.inputs:
                working.append(rest | {child})
        else:
            working.append(rest | set(gate.inputs))
        yield {"replaced": gate_id, "rule": f"{gate.type} gate: " +
               ("one row per input" if gate.type == "OR" else "all inputs into one row"),
               "sets": [set(s) for s in working + finished]}
    yield {"replaced": None, "rule": "minimise: discard any set containing another",
           "sets": [set(s) for s in minimise([frozenset(s) for s in finished])]}


def _expand(ft: FaultTree) -> Set[FrozenSet[str]]:
    sets: List[Set[str]] = [{ft.top}]
    done: List[FrozenSet[str]] = []
    while sets:
        current = sets.pop()
        gate_id = next((x for x in current if x in ft.gates), None)
        if gate_id is None:
            done.append(frozenset(current))
            continue
        gate = ft.gates[gate_id]
        rest = current - {gate_id}
        if gate.type == "OR":
            for child in gate.inputs:
                sets.append(rest | {child})
        else:  # AND
            sets.append(rest | set(gate.inputs))
    return set(done)


def minimise(sets) -> List[FrozenSet[str]]:
    """Discard any set that is a superset of another (NUREG-0492 ch. VII)."""
    kept: List[FrozenSet[str]] = []
    for s in sorted(sets, key=len):
        if not any(k <= s for k in kept):
            kept.append(s)
    return sorted(kept, key=lambda s: (len(s), sorted(s)))


def minimal_cut_sets(ft: FaultTree) -> List[FrozenSet[str]]:
    return minimise(_expand(ft))
