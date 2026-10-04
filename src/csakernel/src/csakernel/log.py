"""The evolution log: an append-only record of what changed in an analysis and why."""
from __future__ import annotations

import json
from datetime import date
from typing import List


class EvolutionLog:
    def __init__(self, entries: List[dict] | None = None):
        self.entries = list(entries or [])

    @classmethod
    def load(cls, path: str) -> "EvolutionLog":
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return cls(json.load(fh).get("entries", []))
        except FileNotFoundError:
            return cls([])

    def record(self, what: str, why: str, by: str, when: str | None = None) -> dict:
        entry = {"when": when or date.today().isoformat(), "what": what, "why": why, "by": by}
        self.entries.append(entry)
        return entry

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"entries": self.entries}, fh, indent=2)

    def __len__(self) -> int:
        return len(self.entries)
