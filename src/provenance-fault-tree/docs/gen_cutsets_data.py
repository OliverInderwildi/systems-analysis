"""Generate docs/cutsets-data.js for the designed animation, from the engine itself.

The page is hand-designed; its *content* is not. Every row, every gate replacement and the
discarded row come from pft.cutsets.expand_steps run on the two example models, so the
picture cannot drift from the code. Run:

    PYTHONPATH=src python3 docs/gen_cutsets_data.py
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from pft.cutsets import expand_steps, minimal_cut_sets   # noqa: E402
from pft.model import load_model                          # noqa: E402

EX = os.path.join(HERE, "..", "examples")

# Layout kept as the design tuned it; ids below must match these keys.
AFTER_POS = {"top": [208, 0], "supply": [90, 100], "hw": [340, 100], "grid": [10, 200],
             "backup": [180, 200], "gen": [40, 300], "fuel": [180, 300], "ups": [320, 300],
             "batt": [250, 400], "hw2": [400, 400]}
BEFORE_OVERRIDE = {"top": [208, 40], "grid": [60, 300], "hw": [360, 300]}

# engine id -> design id (second occurrence of a repeated event gets its own node)
NODE = {"TOP": "top", "G_SUPPLY": "supply", "G_BACKUP": "backup", "G_UPS": "ups",
        "E_GRID": "grid", "E_HW": "hw", "E_GEN": "gen", "E_FUEL": "fuel", "E_BATT": "batt"}
REPEAT = {("G_UPS", "E_HW"): "hw2"}     # this edge draws the repeated event as its own node

T = {
    "begin": "Begin with one row: the failure itself.",
    "or": "OR gate: any input is enough, so each input starts a row of its own.",
    "orF": "B = x + y + z  →  one row becomes several",
    "and": "AND gate: every input is needed, so they all join one row.",
    "andF": "T = A · B  →  one row grows wider",
    "min": "Discard any row that contains another: a bigger combination that includes a "
           "smaller one is not minimal.",
    "minN": "What is left are the minimal cut sets.",
    "none": "No row contains another, so nothing is discarded here.",
}
UPS_NOTE = (" The UPS feeds the racks through the same hardware, so a hardware fault also "
            "stops it bridging.")
IMP_BEFORE = ("What it implies: both rows hold a single event, so each is a single point of "
              "failure - nothing else need go wrong. The grid one can be answered with a "
              "backup supply, which is what redundancy means here: turning a one-event row "
              "into a two-event row.")
IMP_AFTER = ("After the fix: losing the grid now needs a second failure alongside it, so "
             "three two-event rows replace one. The hardware fault is untouched and still "
             "stands alone - redundancy fixed one single point of failure, not the other.")


def label(ft, eid):
    node = ft.events.get(eid) or ft.gates.get(eid)
    return node.short or node.name or eid


def edges_of(ft):
    out = []
    for gid, gate in ft.gates.items():
        for child in gate.inputs:
            out.append([NODE[gid], REPEAT.get((gid, child), NODE[child])])
    return out


def row(items, state, tag=None):
    r = {"items": items, "state": state}
    if tag:
        r["tag"] = tag
    return r


def order_rows(sets, ft):
    """Shortest first, then alphabetical - so the single-event rows read as rows 01, 02."""
    return sorted(sets, key=lambda s: (len(s), sorted(label(ft, e) for e in s)))


def render(sets, ft, marked=None):
    rows = []
    for s in order_rows(sets, ft):
        items = sorted((label(ft, e) for e in s))
        has_gate = any(e in ft.gates for e in s)
        if marked is not None and s == marked:
            state = "mark"
        elif has_gate:
            state = "gate"
        else:
            state = "done"
        rows.append(row(items, state))
    return rows


def frames_for(ft, phase_after: bool, tree_name: str):
    """One frame per thing the reader has to follow, driven by the real expansion."""
    steps = list(expand_steps(ft))
    out = []

    if phase_after:
        out.append({"step": 1, "sys": True, "tree": "before", "rows": [], "fb": "changed",
                    "text": "The design changes: a standby generator, fuel and UPS now back "
                            "up the grid supply."})
        out.append({"step": 1, "sys": True, "tree": tree_name, "rows": [], "fb": "changed",
                    "text": "The tree is redrawn. Supply to the racks is now lost only if the "
                            "grid and the backup both fail."})
    else:
        out.append({"step": 1, "sys": False, "tree": "top", "rows": [],
                    "text": "Name the failure to prevent and put it at the top of the tree."})
        out.append({"step": 1, "sys": False, "tree": tree_name, "rows": [],
                    "text": "Ask what could cause it. Each cause hangs below, joined by a gate."})

    out.append({"step": 2, "sys": phase_after, "tree": tree_name, "text": T["begin"],
                "rows": [row([label(ft, ft.top)], "gate")]})

    prev = steps[0]["sets"]
    for st in steps[1:-1]:                       # each gate replacement
        gid = st["replaced"]
        is_and = ft.gates[gid].type == "AND"
        text = T["and"] if is_and else T["or"]
        if gid == "G_UPS":
            text += UPS_NOTE
        target = next(s for s in prev if gid in s)
        common = {"step": 3, "sys": phase_after, "tree": tree_name, "hl": NODE[gid],
                  "text": text, "formula": T["andF"] if is_and else T["orF"],
                  "replacing": label(ft, gid)}
        out.append({**common, "rows": render(prev, ft, marked=target)})
        out.append({**common, "rows": render(st["sets"], ft)})
        prev = st["sets"]

    final = [set(c) for c in minimal_cut_sets(ft)]
    discarded = [s for s in prev if not any(set(s) == f for f in final)]
    kept_rows = render(final, ft)
    if discarded:
        strike_rows = list(kept_rows)
        for d in discarded:
            contained = next(i for i, f in enumerate(order_rows(final, ft)) if f <= d)
            strike_rows.append(row(sorted(label(ft, e) for e in d), "strike",
                                   tag=f"Contains {contained + 1:02d}"))
        out.append({"step": 4, "sys": phase_after, "tree": tree_name, "text": T["min"],
                    "rows": strike_rows})
        struck = sorted(label(ft, e) for e in discarded[0])
        out.append({"step": 4, "sys": phase_after, "tree": tree_name, "rows": kept_rows,
                    "note": T["minN"], "fb": "next" if phase_after else "found",
                    "implication": IMP_AFTER if phase_after else IMP_BEFORE,
                    "text": f"Row {len(kept_rows) + 1:02d} is struck out: {struck[-1]} is "
                            f"already enough on its own."})
    else:
        out.append({"step": 4, "sys": phase_after, "tree": tree_name, "text": T["none"],
                    "note": T["minN"], "rows": kept_rows,
                    "fb": "next" if phase_after else "found",
                    "implication": IMP_AFTER if phase_after else IMP_BEFORE})
    return out


def main() -> None:
    before = load_model(os.path.join(EX, "processing_power", "model.json"))
    after = load_model(os.path.join(EX, "processing_power_backed", "model.json"))

    labels = {}
    for ft in (before, after):
        for eid in list(ft.gates) + list(ft.events):
            labels[NODE[eid]] = label(ft, eid)
    for (gid, child), node_id in REPEAT.items():
        labels[node_id] = label(after, child)

    data = {
        "steps": ["Write the failure as a tree", "Start at the top", "Replace each gate",
                  "Keep the minimal rows"],
        "labels": labels,
        "gates": {NODE[g]: after.gates[g].type for g in after.gates},
        "order": [NODE[e] for e in ["TOP", "G_SUPPLY", "E_HW", "E_GRID", "G_BACKUP", "E_GEN",
                                    "E_FUEL", "G_UPS", "E_BATT"]] + ["hw2"],
        "allEdges": sorted({tuple(e) for e in edges_of(before) + edges_of(after)},
                           key=lambda e: (e[0], e[1])),
        "trees": {
            "top": {"pos": {**AFTER_POS, **BEFORE_OVERRIDE}, "show": ["top"], "edges": [],
                    "noChips": True},
            "before": {"pos": {**AFTER_POS, **BEFORE_OVERRIDE},
                       "show": [NODE[e] for e in ["TOP", "E_GRID", "E_HW"]],
                       "edges": edges_of(before)},
            "after": {"pos": AFTER_POS,
                      "show": [NODE[e] for e in after.gates] + [NODE[e] for e in after.events]
                              + ["hw2"],
                      "edges": edges_of(after)},
        },
        "frames": frames_for(before, False, "before") + frames_for(after, True, "after"),
    }
    data["allEdges"] = [list(e) for e in data["allEdges"]]

    out = os.path.join(HERE, "cutsets-data.js")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("// GENERATED by docs/gen_cutsets_data.py - do not edit by hand.\n")
        fh.write("// Every row below is the output of pft.cutsets.expand_steps on the example\n")
        fh.write("// models in examples/processing_power{,_backed}. Regenerate after any model\n")
        fh.write("// change so the animation cannot drift from the code.\n")
        fh.write("window.CUTSETS = ")
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write(";\n")
    print(f"wrote {out} ({os.path.getsize(out)} bytes, {len(data['frames'])} frames)")


if __name__ == "__main__":
    main()
