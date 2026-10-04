"""How the success probability evolves across the four nodes.

Conditional on the initiating event: 100% at the outage, then what is left after each barrier
has acted. The step down at each node is that barrier's contribution to loss.

    PYTHONPATH=src python3 docs/figure_survival.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "csakernel", "src"))

from csakernel import Ledger                    # noqa: E402
from pet.fmt import decimal                      # noqa: E402
from pet.model import load_model                 # noqa: E402

EX = os.path.join(HERE, "..", "examples", "datacentre")
SURFACE, INK, MUTED, RULE = "#FAFAF8", "#232830", "#505050", "#DADBD7"
OXFORD, ORANGE = "#002147", "#FF9A2B"
CLASS = {"asserted": ORANGE, "modelled": "#A0A0A0", "demonstrated": OXFORD,
         "established": "#0B341C"}


def draw():
    tree = load_model(os.path.join(EX, "model.json"))
    led = Ledger.load(os.path.join(EX, "ledger.json"))

    nodes = ["Outage\noccurs"]
    surv = [1.0]
    lost = [0.0]
    classes = [led.evidence_class(tree.initiator.ledger_ref)]
    for b in tree.barriers:
        nodes.append(f"{tree.label(b)}\nfails {decimal(b.failure_probability)}")
        lost.append(surv[-1] * b.failure_probability)
        surv.append(surv[-1] * (1 - b.failure_probability))
        classes.append(led.evidence_class(b.ledger_ref))

    fig, ax = plt.subplots(figsize=(9.2, 4.4), dpi=140)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    xs = range(len(nodes))

    ax.step(xs, [s * 100 for s in surv], where="post", color=OXFORD, linewidth=2)
    ax.plot(xs, [s * 100 for s in surv], "o", color=OXFORD, markersize=6)
    for i, (s, l, c) in enumerate(zip(surv, lost, classes)):
        ax.text(i - 0.06, s * 100, f"{s:.4%}", ha="right", va="center", fontsize=9,
                color=INK)
        if i:
            ax.annotate("", xy=(i, s * 100), xytext=(i, surv[i - 1] * 100),
                        arrowprops=dict(arrowstyle="-|>", color=CLASS[c], linewidth=1.6))
            ax.text(i + 0.07, (s + surv[i - 1]) * 50, f"-{l:.4%}", ha="left", va="center",
                    fontsize=8.5, color=CLASS[c])

    ax.set_xlim(-0.35, len(nodes) - 0.55)
    ax.set_xticks(list(xs)); ax.set_xticklabels(nodes, fontsize=8.5, color=INK)
    ax.set_ylim(97.85, 100.2)
    ax.set_ylabel("load still maintained", fontsize=9, color=MUTED)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:g}%")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(RULE)
    ax.tick_params(colors=MUTED, labelsize=8.5)
    ax.grid(axis="y", color="#EFEFEC", linewidth=0.8)
    ax.set_axisbelow(True)

    ax.set_title("Given a grid outage, what survives each barrier", fontsize=12.5,
                 color=OXFORD, loc="left", pad=26)
    ax.text(0, 1.075, "Each drop is that barrier's own contribution to loss; the colour is the "
            "evidence class of its number.", transform=ax.transAxes, fontsize=8.4, color=MUTED)
    ax.text(0, -0.30, "Conditional on an outage. Across all periods, an outage occurs "
            f"{tree.initiator.frequency:.0%} of the time, so {1 - tree.initiator.frequency * (1 - surv[-1]):.4%} "
            "of periods see no grid-driven loss.\nMethod: Rasmussen, WASH-1400 (1975); Fault "
            "Tree Handbook (NUREG-0492, 1981), ch. III",
            transform=ax.transAxes, fontsize=7.6, color=MUTED, va="top", linespacing=1.6)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(HERE, f"survival.{ext}"), facecolor=SURFACE,
                    bbox_inches="tight")
    plt.close(fig)
    print("wrote", os.path.join(HERE, "survival.png"))


if __name__ == "__main__":
    draw()
