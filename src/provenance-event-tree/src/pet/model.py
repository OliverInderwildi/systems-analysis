"""The event tree: an initiating event, the barriers in order, and the outcome of each path.

Structure follows NUREG-0492 ch. III and the event-tree literature that grew out of WASH-1400:
barriers are asked in the order they would actually act, each with a probability of failing on
demand. Fields beyond that - ledger_ref, authored_by - are ours.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List

AUTHORS = ("source", "analyst", "model")


class ModelError(Exception):
    pass


@dataclass
class Initiator:
    id: str
    name: str = ""
    short: str = ""
    frequency: float = 0.0          # per period, or per demand
    ledger_ref: str = ""
    authored_by: str = "analyst"


@dataclass
class Barrier:
    id: str
    name: str = ""
    short: str = ""
    failure_probability: float = 0.0     # probability it does NOT do its job, given the demand
    ledger_ref: str = ""
    authored_by: str = "analyst"
    from_fault_tree: str = ""            # optional: the model whose top event this is


@dataclass
class EventTree:
    initiator: Initiator
    barriers: List[Barrier] = field(default_factory=list)
    outcomes: Dict[str, str] = field(default_factory=dict)   # pattern of S/F -> end state
    default_outcome: str = ""
    severity: Dict[str, int] = field(default_factory=dict)   # end state -> rank, 0 = benign
    meta: dict = field(default_factory=dict)

    def validate(self) -> None:
        if not self.barriers:
            raise ModelError("an event tree needs at least one barrier")
        if not 0.0 <= self.initiator.frequency <= 1.0:
            raise ModelError(f"initiator frequency {self.initiator.frequency} outside [0,1]")
        seen = set()
        for b in self.barriers:
            if b.id in seen:
                raise ModelError(f"duplicate barrier id '{b.id}'")
            seen.add(b.id)
            if not 0.0 <= b.failure_probability <= 1.0:
                raise ModelError(f"barrier '{b.id}': probability {b.failure_probability} "
                                 "outside [0,1]")
            if b.authored_by not in AUTHORS:
                raise ModelError(f"barrier '{b.id}': authored_by must be one of {AUTHORS}")
        width = len(self.barriers)
        for pattern in self.outcomes:
            if len(pattern) != width or set(pattern) - set("SF"):
                raise ModelError(f"outcome pattern '{pattern}' must be {width} characters of "
                                 "S (barrier works) and F (barrier fails)")
        if not self.default_outcome and len(self.outcomes) < 2 ** width:
            raise ModelError("not every path has an outcome and no default_outcome is given")

    def label(self, item) -> str:
        return item.short or item.name or item.id


def load_model(path: str) -> EventTree:
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    try:
        ini = raw["initiator"]
        tree = EventTree(
            initiator=Initiator(id=ini["id"], name=ini.get("name", ""), short=ini.get("short", ""),
                                frequency=float(ini.get("frequency", 0.0)),
                                ledger_ref=ini.get("ledger_ref", ""),
                                authored_by=ini.get("authored_by", "analyst")),
            barriers=[Barrier(id=b["id"], name=b.get("name", ""), short=b.get("short", ""),
                              failure_probability=float(b.get("failure_probability", 0.0)),
                              ledger_ref=b.get("ledger_ref", ""),
                              authored_by=b.get("authored_by", "analyst"),
                              from_fault_tree=b.get("from_fault_tree", ""))
                      for b in raw.get("barriers", [])],
            outcomes=dict(raw.get("outcomes", {})),
            default_outcome=raw.get("default_outcome", ""),
            severity=dict(raw.get("severity", {})),
            meta=raw.get("meta", {}),
        )
    except KeyError as exc:
        raise ModelError(f"malformed model: missing key {exc}") from exc
    tree.validate()
    return tree
