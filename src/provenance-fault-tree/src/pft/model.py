"""Fault tree data model and JSON loading.

Structure follows NUREG-0492 ch. V: a top event, gates (AND/OR), and basic events.
Fields beyond that - ledger_ref on basic events, authored_by on every element - are ours.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List

GATE_TYPES = ("AND", "OR")
AUTHORS = ("source", "analyst", "model")  # who put this element in the tree


class ModelError(Exception):
    pass


@dataclass
class BasicEvent:
    id: str
    name: str = ""
    short: str = ""          # display label for figures; ids stay the machine names
    probability: float = 0.0
    ledger_ref: str = ""          # id of the row in the evidence ledger
    authored_by: str = "analyst"  # source | analyst | model


@dataclass
class Gate:
    id: str
    type: str
    inputs: List[str]
    name: str = ""
    short: str = ""
    authored_by: str = "analyst"


@dataclass
class FaultTree:
    top: str
    gates: Dict[str, Gate] = field(default_factory=dict)
    events: Dict[str, BasicEvent] = field(default_factory=dict)
    meta: dict = field(default_factory=dict)

    def validate(self) -> None:
        if self.top not in self.gates and self.top not in self.events:
            raise ModelError(f"top event '{self.top}' is not defined")
        for gid, g in self.gates.items():
            if g.type not in GATE_TYPES:
                raise ModelError(f"gate '{gid}': type must be one of {GATE_TYPES}, got '{g.type}'")
            if not g.inputs:
                raise ModelError(f"gate '{gid}' has no inputs")
            for i in g.inputs:
                if i not in self.gates and i not in self.events:
                    raise ModelError(f"gate '{gid}' refers to undefined element '{i}'")
            if g.authored_by not in AUTHORS:
                raise ModelError(f"gate '{gid}': authored_by must be one of {AUTHORS}")
        for eid, e in self.events.items():
            if not 0.0 <= e.probability <= 1.0:
                raise ModelError(f"event '{eid}': probability {e.probability} outside [0,1]")
            if e.authored_by not in AUTHORS:
                raise ModelError(f"event '{eid}': authored_by must be one of {AUTHORS}")
        self._check_acyclic()

    def _check_acyclic(self) -> None:
        state: Dict[str, int] = {}

        def walk(node: str, path: List[str]) -> None:
            if state.get(node) == 2:
                return
            if state.get(node) == 1:
                cycle = " -> ".join(path + [node])
                raise ModelError(f"cycle in tree: {cycle}")
            state[node] = 1
            for child in self.gates.get(node, Gate(node, "OR", [])).inputs:
                walk(child, path + [node])
            state[node] = 2

        walk(self.top, [])

    def reachable_events(self) -> List[str]:
        seen, out = set(), []

        def walk(node: str) -> None:
            if node in seen:
                return
            seen.add(node)
            if node in self.events:
                out.append(node)
                return
            for child in self.gates[node].inputs:
                walk(child)

        walk(self.top)
        return out


def load_model(path: str) -> FaultTree:
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    try:
        gates = {
            gid: Gate(id=gid, type=str(g["type"]).upper(), inputs=list(g["inputs"]),
                      name=g.get("name", ""), short=g.get("short", ""),
                      authored_by=g.get("authored_by", "analyst"))
            for gid, g in raw.get("gates", {}).items()
        }
        events = {
            eid: BasicEvent(id=eid, name=e.get("name", ""), short=e.get("short", ""),
                            probability=float(e.get("probability", 0.0)),
                            ledger_ref=e.get("ledger_ref", ""),
                            authored_by=e.get("authored_by", "analyst"))
            for eid, e in raw.get("events", {}).items()
        }
    except KeyError as exc:
        raise ModelError(f"malformed model: missing key {exc}") from exc
    ft = FaultTree(top=raw["top"], gates=gates, events=events, meta=raw.get("meta", {}))
    ft.validate()
    return ft
