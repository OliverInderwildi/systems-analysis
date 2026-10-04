"""The ACH matrix: hypotheses across the top, evidence down the side.

Ratings follow Heuer's scale. Fields beyond the matrix - ledger_ref on every item of
evidence, authored_by on hypotheses and evidence - are ours.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List

# very consistent, consistent, neutral, inconsistent, very inconsistent, not applicable
RATINGS = ("CC", "C", "N", "I", "II", "NA")
AUTHORS = ("source", "analyst", "model")


class MatrixError(Exception):
    pass


@dataclass
class Hypothesis:
    id: str
    text: str
    authored_by: str = "analyst"


@dataclass
class Evidence:
    id: str
    text: str
    ledger_ref: str = ""
    authored_by: str = "analyst"


@dataclass
class Matrix:
    hypotheses: Dict[str, Hypothesis] = field(default_factory=dict)
    evidence: Dict[str, Evidence] = field(default_factory=dict)
    ratings: Dict[str, Dict[str, str]] = field(default_factory=dict)  # evidence -> hypothesis -> rating
    meta: dict = field(default_factory=dict)

    def validate(self) -> None:
        if len(self.hypotheses) < 2:
            raise MatrixError("ACH needs at least two hypotheses; one hypothesis is not analysis")
        if not self.evidence:
            raise MatrixError("no evidence")
        for eid, row in self.ratings.items():
            if eid not in self.evidence:
                raise MatrixError(f"ratings refer to unknown evidence '{eid}'")
            for hid, rating in row.items():
                if hid not in self.hypotheses:
                    raise MatrixError(f"evidence '{eid}' rated against unknown hypothesis '{hid}'")
                if rating not in RATINGS:
                    raise MatrixError(f"evidence '{eid}' vs '{hid}': rating must be one of {RATINGS}")
        missing = [(e, h) for e in self.evidence for h in self.hypotheses
                   if h not in self.ratings.get(e, {})]
        if missing:
            pairs = ", ".join(f"{e}x{h}" for e, h in missing[:6])
            raise MatrixError(f"{len(missing)} cell(s) unrated ({pairs}"
                              f"{'...' if len(missing) > 6 else ''}); rate every cell or mark it NA")
        for item in list(self.hypotheses.values()) + list(self.evidence.values()):
            if item.authored_by not in AUTHORS:
                raise MatrixError(f"'{item.id}': authored_by must be one of {AUTHORS}")


def load_matrix(path: str) -> Matrix:
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    m = Matrix(
        hypotheses={hid: Hypothesis(hid, h["text"], h.get("authored_by", "analyst"))
                    for hid, h in raw.get("hypotheses", {}).items()},
        evidence={eid: Evidence(eid, e["text"], e.get("ledger_ref", ""),
                                e.get("authored_by", "analyst"))
                  for eid, e in raw.get("evidence", {}).items()},
        ratings={eid: dict(row) for eid, row in raw.get("ratings", {}).items()},
        meta=raw.get("meta", {}),
    )
    m.validate()
    return m
