"""The event tree, drawn from the model. Run: PYTHONPATH=src python3 docs/figure.py

Deliberately plain: initiating event on the left, one column per barrier, branches up when it
works and down when it fails, end states on the right. Everything - labels, probabilities,
frequencies, evidence classes - comes from the model and the ledger.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "csakernel", "src"))

from csakernel import Ledger                                    # noqa: E402
from pet.evidence import sequence_evidence                       # noqa: E402
from pet.fmt import decimal                                       # noqa: E402
from pet.model import load_model                                 # noqa: E402
from pet.quant import closure_error                              # noqa: E402
from pet.sequences import sequences                              # noqa: E402

EX = os.path.join(HERE, "..", "examples", "datacentre")

# heritage tokens
SURFACE, INK, MUTED, RULE = "#FAFAF8", "#232830", "#505050", "#DADBD7"
OXFORD, GREEN, ORANGE = "#002147", "#0B341C", "#FF9A2B"
CLASS = {"asserted": ORANGE, "modelled": "#A0A0A0", "demonstrated": OXFORD,
         "established": GREEN}


def draw():
    tree = load_model(os.path.join(EX, "model.json"))
    led = Ledger.load(os.path.join(EX, "ledger.json"))
    seqs = sequences(tree)
    n = len(tree.barriers)

    fig, ax = plt.subplots(figsize=(13.6, 5.6), dpi=140)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE); ax.axis("off")
    x0, dx = 0.14, 0.115                      # first branch point, column width
    top, bottom = 0.86, 0.10
    rows = len(seqs)
    ys = [top - i * (top - bottom) / (rows - 1) for i in range(rows)]

    # column headings
    for i, b in enumerate(tree.barriers):
        ax.text(x0 + i * dx + dx / 2, 0.96, tree.label(b), ha="center", va="top",
                fontsize=9, color=OXFORD)
        ax.text(x0 + i * dx + dx / 2, 0.925, f"fails {decimal(b.failure_probability)}",
                ha="center", va="top", fontsize=7.5, color=MUTED)
        ax.plot([x0 + i * dx, x0 + i * dx], [bottom - 0.04, 0.90], color=RULE,
                linewidth=0.8, zorder=0)

    # the branches: recurse, each level splitting the span it was given
    def branch(level, lo, hi, x):
        if level == n:
            return
        mid = (lo + hi) / 2
        y_works = (mid + hi) / 2          # success goes up - the top leaf is all-S
        y_fails = (lo + mid) / 2
        y = mid
        nxt = x + dx
        ax.plot([x, nxt], [y, y_works], color=OXFORD, linewidth=1.1)
        ax.plot([x, nxt], [y, y_fails], color=ORANGE, linewidth=1.1)
        if level == 0:
            ax.text(x + dx * 0.5, y_works + 0.02, "works", fontsize=7, color=OXFORD,
                    ha="center")
            ax.text(x + dx * 0.5, y_fails - 0.032, "fails", fontsize=7, color=ORANGE,
                    ha="center")
        branch(level + 1, mid, hi, nxt)   # upper half = this barrier worked
        branch(level + 1, lo, mid, nxt)

    span_lo, span_hi = bottom - 0.02, top + 0.02
    branch(0, span_lo, span_hi, x0)

    # initiating event
    ax.add_patch(FancyBboxPatch((0.01, (span_lo + span_hi) / 2 - 0.055), 0.13, 0.11,
                                boxstyle="round,pad=0.012,rounding_size=0.02",
                                facecolor="#FFFFFF", edgecolor=OXFORD, linewidth=1.4))
    ax.text(0.075, (span_lo + span_hi) / 2 + 0.018, tree.label(tree.initiator),
            ha="center", va="center", fontsize=9, color=INK)
    ax.text(0.075, (span_lo + span_hi) / 2 - 0.022,
            f"{decimal(tree.initiator.frequency)} / period", ha="center", va="center",
            fontsize=7.5, color=MUTED)

    # end states, in the order the branches land (all-works at the top)
    xr = x0 + n * dx + 0.015
    for y, s in zip(ys, seqs):
        cls = sequence_evidence(tree, led, s)
        ax.plot([x0 + n * dx, xr - 0.008], [y, y], color=RULE, linewidth=0.8)
        ax.text(xr, y, f"{s.id}  {s.pattern}", fontsize=7.5, color=MUTED, va="center",
                family="DejaVu Sans Mono")
        ax.text(xr + 0.065, y, s.end_state, fontsize=8.5, color=INK, va="center")
        ax.text(0.845, y, decimal(s.frequency, 2), fontsize=8.5, color=INK, va="center",
                ha="right", family="DejaVu Sans Mono")
        ax.add_patch(plt.Rectangle((0.852, y - 0.012), 0.010, 0.024, facecolor=CLASS[cls],
                                   edgecolor="none"))

    ax.text(xr, 0.955, "path", fontsize=8, color=MUTED, va="top")
    ax.text(xr + 0.065, 0.955, "end state", fontsize=8, color=MUTED, va="top")
    ax.text(0.845, 0.955, "per period", fontsize=8, color=MUTED, va="top", ha="right")

    # ---- outcome bar: what share of outages ends where
    from pet.quant import end_state_frequencies
    totals = end_state_frequencies(tree, seqs)
    f0 = tree.initiator.frequency
    maintained = totals.get("Load maintained", 0.0) / f0
    losses = [(st, fr / f0) for st, fr in totals.items() if st != "Load maintained"]
    loss_total = sum(v for _, v in losses)

    bx, bw = 0.872, 0.030            # main bar
    b_lo, b_hi = bottom - 0.02, top + 0.02
    h = b_hi - b_lo
    ax.add_patch(plt.Rectangle((bx, b_lo + h * loss_total), bw, h * maintained,
                               facecolor=OXFORD, edgecolor="none"))
    ax.add_patch(plt.Rectangle((bx, b_lo), bw, h * loss_total, facecolor=ORANGE,
                               edgecolor="none"))
    ax.text(bx + bw / 2, b_lo + h * loss_total + h * maintained / 2,
            f"load maintained  {maintained:.2%}", ha="center", va="center", fontsize=8.6,
            color="#FFFFFF", rotation=90)
    ax.text(bx + bw / 2, 0.955, "of outages", fontsize=8, color=MUTED, ha="center", va="top")

    # ---- the 1.89% expanded, because a linear slice of it is invisible
    ex, ew = 0.922, 0.026
    e_lo, e_hi = b_lo, b_lo + h * 0.62
    eh = e_hi - e_lo
    ax.plot([bx + bw, ex], [b_lo + h * loss_total, e_hi], color=RULE, linewidth=0.8)
    ax.plot([bx + bw, ex], [b_lo, e_lo], color=RULE, linewidth=0.8)
    run = e_lo
    for st, share in sorted(losses, key=lambda kv: kv[1]):
        seg = eh * (share / loss_total)
        ax.add_patch(plt.Rectangle((ex, run), ew, seg, facecolor=ORANGE, edgecolor=SURFACE,
                                   linewidth=1.2))
        short = (st.replace("Load lost when the ", "").replace("Load lost when ", "")
                   .replace("Immediate loss of processing power", "immediate loss")
                   .replace("Momentary interruption", "momentary interruption"))
        pct = f"{share * 100:.2f}%" if share >= 0.0001 else f"{decimal(share * 100, 2)}%"
        ax.text(ex + ew + 0.007, run + seg / 2, f"{pct}  {short}",
                fontsize=7.6, color=INK, va="center")
        run += seg
    ax.text(ex, e_hi + 0.025, f"the {loss_total:.2%} that does not \u2014 expanded",
            fontsize=7.8, color=MUTED, ha="left", va="bottom")

    ax.text(0.01, 1.005, "What follows a grid outage: the same data centre, forwards",
            fontsize=13, color=OXFORD, va="top")
    legend = "  ".join(f"■ {c}" for c in ("demonstrated", "modelled", "asserted"))
    ax.text(0.01, 0.052, "Bar at the right: the weakest evidence among the barriers that "
            "failed on that path.", fontsize=7.6, color=MUTED, va="center")
    for i, (c, col) in enumerate([("demonstrated", OXFORD), ("modelled", "#A0A0A0"),
                                  ("asserted", ORANGE)]):
        ax.add_patch(plt.Rectangle((0.62 + i * 0.13, 0.042), 0.012, 0.022, facecolor=col,
                                   edgecolor="none"))
        ax.text(0.638 + i * 0.13, 0.053, c, fontsize=7.6, color=MUTED, va="center")
    ax.text(0.18, 0.023, "Method: Rasmussen, WASH-1400 (1975); Fault Tree Handbook "
            "(NUREG-0492, 1981), ch. III", fontsize=7.4, color=MUTED, va="center")
    ax.text(0.01, 0.023, f"paths sum to {1 + closure_error(tree, seqs):.6f}", fontsize=7.6,
            color=MUTED, va="center")

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(HERE, f"event_tree.{ext}"), facecolor=SURFACE,
                    bbox_inches="tight")
    plt.close(fig)
    print("wrote", os.path.join(HERE, "event_tree.png"))


if __name__ == "__main__":
    draw()
