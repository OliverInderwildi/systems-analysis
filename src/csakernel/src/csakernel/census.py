"""The absence census: what the corpus does not supply, reported rather than defaulted."""
from __future__ import annotations

from typing import Dict, List, Mapping

from .ledger import Ledger


def absence_census(refs: Mapping[str, str], ledger: Ledger) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for item, ref in refs.items():
        if not ref:
            out.append({"item": item, "missing": "no ledger row at all"})
            continue
        row = ledger.rows.get(ref, {})
        prov = row.get("provenance", {}) or {}
        gaps: List[str] = []
        if not str(prov.get("origin", "")).strip():
            gaps.append("origin")
        if not str(row.get("excerpt", "")).strip():
            gaps.append("excerpt")
        if prov.get("generation_method") == "asserted":
            gaps.append("value is asserted, not derived from data")
        elif row.get("evidence_class") == "asserted":
            gaps.append("evidence class is asserted")
        try:
            independent = int(prov.get("independent_origins", 0) or 0)
        except (TypeError, ValueError):
            independent = 0
        if independent < 2:
            gaps.append("single origin (no independent confirmation)")
        if gaps:
            out.append({"item": item, "ledger_ref": ref, "missing": ", ".join(gaps)})
    return out
