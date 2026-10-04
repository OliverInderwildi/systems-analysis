"""The evidence ledger and the rule that nothing enters an analysis without one."""
from __future__ import annotations

import json
from typing import Dict, Iterable, List, Mapping

from .vocab import EVIDENCE_CLASSES, GENERATION_METHODS


class LedgerError(Exception):
    """Raised when an analysis would have to proceed on unsourced or malformed evidence."""


class Ledger:
    def __init__(self, rows: List[dict]):
        self.rows: Dict[str, dict] = {r["id"]: r for r in rows}
        if len(self.rows) != len(rows):
            raise LedgerError("duplicate ledger ids")

    @classmethod
    def load(cls, path: str) -> "Ledger":
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls(data.get("claims", data if isinstance(data, list) else []))

    def get(self, ref: str) -> dict:
        if ref not in self.rows:
            raise LedgerError(f"ledger has no row '{ref}'")
        return self.rows[ref]

    def provenance(self, ref: str) -> dict:
        return self.get(ref).get("provenance", {}) or {}

    def evidence_class(self, ref: str) -> str:
        cls = self.get(ref).get("evidence_class")
        if cls not in EVIDENCE_CLASSES:
            raise LedgerError(f"row '{ref}': evidence_class must be one of {EVIDENCE_CLASSES}")
        return cls

    def origin(self, ref: str) -> str:
        return str(self.provenance(ref).get("origin", ""))

    def generation_method(self, ref: str) -> str:
        return str(self.provenance(ref).get("generation_method", ""))

    def independent_origins(self, ref: str) -> int:
        try:
            return int(self.provenance(ref).get("independent_origins", 0) or 0)
        except (TypeError, ValueError):
            return 0


def require_sourced(refs: Mapping[str, str], ledger: Ledger, what: str = "input") -> None:
    """Refuse the analysis unless every item has a usable ledger row.

    refs maps the analysis's own item id (a basic event, a hypothesis, an element) to the
    ledger row id that sources it. Every problem found is reported at once, so a ledger is
    fixed in one pass rather than one error at a time.
    """
    problems: List[str] = []
    for item, ref in refs.items():
        if not ref:
            problems.append(f"{item}: no ledger reference ({what} has no source)")
            continue
        try:
            row = ledger.get(ref)
        except LedgerError as exc:
            problems.append(f"{item}: {exc}")
            continue
        prov = row.get("provenance", {}) or {}
        if not str(prov.get("origin", "")).strip():
            problems.append(f"{item} ({ref}): provenance.origin is empty")
        if prov.get("generation_method") not in GENERATION_METHODS:
            problems.append(f"{item} ({ref}): generation_method must be one of {GENERATION_METHODS}")
        if not str(row.get("excerpt", "")).strip():
            problems.append(f"{item} ({ref}): no verbatim excerpt locating the value in the source")
        if row.get("evidence_class") not in EVIDENCE_CLASSES:
            problems.append(f"{item} ({ref}): evidence_class missing or unknown")
    if problems:
        raise LedgerError("analysis refused; unsourced inputs:\n  - " + "\n  - ".join(problems))
