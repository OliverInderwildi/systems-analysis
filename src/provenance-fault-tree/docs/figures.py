"""Figures for the article. Run: PYTHONPATH=src python3 docs/figures.py"""
import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.animation import FuncAnimation, PillowWriter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from pft.cutsets import expand_steps, minimal_cut_sets          # noqa: E402
from pft.evidence import Ledger, evidence_report                 # noqa: E402
from pft.model import load_model                                 # noqa: E402
from pft.quant import top_probability                            # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.path.join(HERE, "..", "examples", "backup_power_mixed")
OUT = HERE

# ordinal ramp, weakest -> strongest evidence (validated: one hue, monotone lightness)
CLASS_COLOR = {"asserted": "#86b6ef", "modelled": "#3987e5",
               "demonstrated": "#1c5cab", "established": "#0d366b"}
SURFACE, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
ORDER = ["asserted", "modelled", "demonstrated", "established"]


def _style(ax, fig):
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#d8d7d2")
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=INK2, labelsize=9, length=3, width=0.8)


def load():
    ft = load_model(os.path.join(EX, "model.json"))
    led = Ledger.load(os.path.join(EX, "ledger.json"))
    cuts = minimal_cut_sets(ft)
    return ft, led, cuts, evidence_report(ft, led, cuts), top_probability(cuts, ft)


def fig_mass(report, top_p):
    """One stacked bar: which evidence class carries the result."""
    fig, ax = plt.subplots(figsize=(8, 2.5), dpi=160)
    _style(ax, fig)
    left = 0.0
    for cls in ORDER:
        share = report["share_by_evidence_class"].get(cls, 0.0)
        if share <= 0:
            continue
        ax.barh(0, share, left=left, height=0.42, color=CLASS_COLOR[cls],
                edgecolor=SURFACE, linewidth=2)
        ax.text(left + share / 2, 0, f"{cls}\n{share:.0%}", ha="center", va="center",
                fontsize=9.5, color="#ffffff" if cls != "asserted" else INK, linespacing=1.4)
        left += share
    ax.set_xlim(0, 1); ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([]); ax.set_xticks([0, .25, .5, .75, 1])
    ax.set_xticklabels(["0", "25%", "50%", "75%", "100%"])
    ax.set_title(f"A top-event probability of {top_p:.2g} — and what it rests on",
                 fontsize=12, color=INK, pad=14, loc="left")
    ax.text(0, -0.72, "Share of cut-set probability by the weakest evidence class in each cut set.",
            fontsize=8.5, color=INK2, transform=ax.get_yaxis_transform(), clip_on=False)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"fig1_mass_by_evidence.{ext}"), facecolor=SURFACE)
    plt.close(fig)


def fig_importance(report):
    """Importance against evidence: what drives the answer, and how well sourced it is."""
    rows = report["importance"]
    names = [r["event"] for r in rows][::-1]
    vals = [r["fussell_vesely"] for r in rows][::-1]
    classes = [r["evidence_class"] for r in rows][::-1]
    fig, ax = plt.subplots(figsize=(8, 3.6), dpi=160)
    _style(ax, fig)
    ax.barh(names, vals, height=0.5, color=[CLASS_COLOR[c] for c in classes])
    for y, (v, c) in enumerate(zip(vals, classes)):
        ax.text(v + 0.015, y, f"{v:.0%}  {c}", va="center", fontsize=9, color=INK2)
    ax.set_xlim(0, 1.25); ax.set_xticks([0, .25, .5, .75, 1])
    ax.set_xticklabels(["0", "25%", "50%", "75%", "100%"])
    ax.grid(axis="x", color="#eceae5", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Importance against evidence", fontsize=12, color=INK, pad=30, loc="left")
    ax.text(0, 1.04, "Fussell–Vesely importance of each basic event, coloured by the evidence "
                     "class of its probability.", fontsize=8.5, color=INK2, transform=ax.transAxes)
    handles = [plt.Line2D([], [], marker="s", linestyle="", markersize=8,
                          color=CLASS_COLOR[c], label=c) for c in ORDER[:3]]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=8.5,
              labelcolor=INK2, handletextpad=0.5)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"fig2_importance_evidence.{ext}"), facecolor=SURFACE)
    plt.close(fig)


def _label(ft, nid):
    """Real wording for the picture; the ids stay the machine names in the code."""
    node = ft.events.get(nid) or ft.gates.get(nid)
    return (node.short or node.name or nid) if node else nid


def _layout(ft):
    """Depth from the top, leaves spread evenly, parents centred over their inputs."""
    depth, order = {}, []

    def walk(nid, d):
        depth[nid] = max(depth.get(nid, 0), d)
        for child in ft.gates.get(nid).inputs if nid in ft.gates else []:
            walk(child, d + 1)
        if nid not in ft.gates and nid not in order:
            order.append(nid)

    walk(ft.top, 0)
    x = {nid: i for i, nid in enumerate(order)}
    for nid in sorted(ft.gates, key=lambda g: -depth[g]):
        kids = [x[c] for c in ft.gates[nid].inputs if c in x]
        if kids:
            x[nid] = sum(kids) / len(kids)
    span = max(x.values()) or 1
    return {nid: (x[nid] / span, -depth[nid]) for nid in x}, max(depth.values())


def _node(ax, xy, text, kind, highlight=False, w=0.215, h=0.38):
    face = {"gate": "#e8f0fd", "event": "#ffffff"}[kind]
    edge = "#eb6834" if highlight else ("#1c5cab" if kind == "gate" else "#86b6ef")
    ax.add_patch(FancyBboxPatch((xy[0] - w / 2, xy[1] - h / 2), w, h,
                                boxstyle="round,pad=0.012,rounding_size=0.02",
                                facecolor=face, edgecolor=edge,
                                linewidth=2.2 if highlight else 1.2, zorder=3))
    ax.text(xy[0], xy[1], "\n".join(textwrap.wrap(text, 13)), ha="center", va="center",
            fontsize=7.0, color=INK, zorder=4, linespacing=1.35)


def _step_strip(fig, active):
    """The four steps as one sequence, with the current one marked."""
    labels = [(1, "write the failure\nas a tree"), (2, "start at the top"),
              (3, "replace each gate"), (4, "keep the minimal rows")]
    x0, w, gap = 0.245, 0.166, 0.018
    for i, (num, text) in enumerate(labels):
        x = x0 + i * (w + gap)
        on = (num == active)
        fig.patches.append(FancyBboxPatch((x, 0.760), w, 0.085,
                                          boxstyle="round,pad=0.004,rounding_size=0.012",
                                          transform=fig.transFigure, zorder=2,
                                          facecolor="#e8f0fd" if on else SURFACE,
                                          edgecolor="#1c5cab" if on else "#d8d7d2",
                                          linewidth=1.6 if on else 1.0))
        fig.text(x + 0.016, 0.802, str(num), fontsize=11,
                 color="#1c5cab" if on else "#a9a89f", va="center", ha="center")
        fig.text(x + 0.033, 0.802, text, fontsize=7.6, color=INK if on else INK2,
                 va="center", ha="left", linespacing=1.3)
        if i < 3:
            fig.text(x + w + gap / 2, 0.802, "\u203a", fontsize=11, color="#c9c8c2",
                     va="center", ha="center")


def _frame_band_unused(ax):
    """Kept for reference; the banner was dropped as unnecessary."""
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    steps = [
        (0.155, 0.30, False, "You want to prevent\na worst case",
         "judgement: which failure matters"),
        (0.50, 0.30, True, "Work backwards: how\ncould it occur?",
         "the algorithm - steps 1 to 4 below"),
        (0.845, 0.34, False, "Act: redundancy, decoupling,\npredictive maintenance",
         "judgement: what to change"),
    ]
    for x, w, is_algo, text, note in steps:
        ax.add_patch(FancyBboxPatch((x - w / 2, 0.34), w, 0.46,
                                    boxstyle="round,pad=0.012,rounding_size=0.04",
                                    facecolor="#e8f0fd" if is_algo else SURFACE,
                                    edgecolor="#1c5cab" if is_algo else "#c9c8c2",
                                    linewidth=1.8 if is_algo else 1.1,
                                    linestyle="solid" if is_algo else (0, (4, 3)), zorder=3))
        ax.text(x, 0.60, text, ha="center", va="center", fontsize=9.6,
                color=INK, zorder=4, linespacing=1.35)
        ax.text(x, 0.40, note, ha="center", va="center", fontsize=7.4,
                color="#1c5cab" if is_algo else INK2, zorder=4, style="italic")
    for x in (0.315, 0.665):
        ax.annotate("", xy=(x + 0.02, 0.57), xytext=(x - 0.02, 0.57),
                    arrowprops=dict(arrowstyle="-|>", color="#c9c8c2", linewidth=1.4))
    ax.text(0.5, 0.08, "Only the middle step is the algorithm. It tells you how the failure "
            "could happen; it does not tell you what to do about it.",
            ha="center", va="center", fontsize=8, color=INK2)


def _system_panel(ax, phase):
    """The system as it is used: supply in at one end, the service that matters at the other.

    Phase 0 shows it as built. Phase 1 adds what the analysis argues for - so the reader sees
    the fix arrive as a conclusion, not as part of the question.
    """
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    chain = [("Grid supply", 0.88), ("Data centre", 0.71), ("Racks", 0.54),
             ("CPUs", 0.37), ("Processing power", 0.20)]
    for i, (text, y) in enumerate(chain):
        service = (i == len(chain) - 1)
        ax.add_patch(FancyBboxPatch((0.30, y - 0.055), 0.56, 0.11,
                                    boxstyle="round,pad=0.010,rounding_size=0.03",
                                    facecolor="#f3f2ef" if service else "#ffffff",
                                    edgecolor="#1c5cab" if service else "#c9c8c2",
                                    linewidth=1.4 if service else 1.1, zorder=3))
        ax.text(0.58, y, text, ha="center", va="center", fontsize=7.8,
                color=INK, zorder=4)
        if i:
            ax.annotate("", xy=(0.58, y + 0.055), xytext=(0.58, chain[i - 1][1] - 0.055),
                        arrowprops=dict(arrowstyle="-|>", color="#c9c8c2", linewidth=1.1))
    if phase == 0:
        ax.text(0.02, 0.07, textwrap.fill("Processing power is the service the business runs "
                "on. It must not be unavailable - so the question is what could take it away.",
                40), fontsize=7.6, color=INK2, va="top", linespacing=1.5)
    else:
        ax.add_patch(FancyBboxPatch((0.02, 0.55), 0.24, 0.28,
                                    boxstyle="round,pad=0.012,rounding_size=0.03",
                                    facecolor="#fdf0e9", edgecolor="#eb6834",
                                    linewidth=1.4, zorder=3))
        ax.text(0.14, 0.69, "standby\ngenerator\n+ fuel\n+ UPS", ha="center", va="center",
                fontsize=7.2, color=INK, zorder=4, linespacing=1.35)
        ax.annotate("", xy=(0.30, 0.71), xytext=(0.26, 0.69),
                    arrowprops=dict(arrowstyle="-|>", color="#eb6834", linewidth=1.2))
        ax.text(0.02, 0.09, textwrap.fill("Added because the analysis found the grid to be a "
                "single point of failure. UPS = uninterruptible power supply: batteries that "
                "carry the load until the generator takes over.", 40),
                fontsize=7.4, color=INK2, va="top", linespacing=1.5)
    ax.text(0, 1.0, "the system" + ("" if phase == 0 else "  (after the fix)"),
            fontsize=9, color=INK2, va="top", transform=ax.transAxes)


def anim_cutsets(ft, ft_after=None):
    """Three panels: the system, its fault tree, and the expansion into cut sets.

    Two phases: the system as built, then the same analysis after the fix it argues for.
    """
    steps = [dict(st, phase=0) for st in expand_steps(ft)]
    steps += [dict(steps[-1])] * 2
    trees = {0: ft}
    if ft_after is not None:
        steps += [dict(st, phase=1) for st in expand_steps(ft_after)]
        steps += [dict(steps[-1])] * 3
        trees[1] = ft_after
    layouts = {k: _layout(v) for k, v in trees.items()}
    fig = plt.figure(figsize=(11.6, 5.3), dpi=130)
    fig.patch.set_facecolor(SURFACE)
    axs = fig.add_axes([0.025, 0.15, 0.185, 0.56])
    axl = fig.add_axes([0.245, 0.11, 0.395, 0.60])
    axr = fig.add_axes([0.665, 0.11, 0.310, 0.60])

    # which system component each basic event is about
    COMPONENT = {"E_GRID": "E_GRID", "E_GEN": "E_GEN", "E_FUEL": "E_FUEL", "E_UPS": "E_UPS"}

    def draw(i):
        st = steps[i]
        phase = st.get("phase", 0)
        ft_now = trees[phase]
        pos, maxdepth = layouts[phase]
        for ax in (axs, axl, axr):
            ax.clear(); ax.axis("off"); ax.set_facecolor(SURFACE)
        fig.texts.clear()
        fig.patches.clear()

        fig.text(0.025, 0.975, "Reverse-engineering failure: fault tree analysis in four steps",
                 fontsize=14, color=INK, va="top")
        fig.text(0.025, 0.925,
                 "Which combinations of basic failures are, on their own, enough to cause the "
                 "failure we want to prevent? Those combinations are called cut sets.",
                 fontsize=8.6, color=INK2, va="top")
        _step_strip(fig, {"start": 2, "AND": 3, "OR": 3, "min": 4}.get(
            "start" if st["rule"] == "start" else
            "AND" if st["rule"].startswith("AND") else
            "OR" if st["rule"].startswith("OR") else "min", 1))

        _system_panel(axs, phase)

        # ---- the tree
        axl.set_xlim(-0.24, 1.28); axl.set_ylim(-maxdepth - 0.40, 0.40)
        for gid, gate in ft_now.gates.items():
            for child in gate.inputs:
                axl.plot([pos[gid][0], pos[child][0]],
                         [pos[gid][1] - 0.19, pos[child][1] + 0.19],
                         color="#c9c8c2", linewidth=1.1, zorder=1)
            axl.text(pos[gid][0] + 0.245, pos[gid][1], gate.type, fontsize=7.5,
                     color="#1c5cab", ha="center", va="center", zorder=5,
                     bbox=dict(boxstyle="round,pad=0.22", facecolor=SURFACE,
                               edgecolor="#1c5cab", linewidth=0.9))
        for nid in pos:
            kind = "gate" if nid in ft_now.gates else "event"
            _node(axl, pos[nid], _label(ft_now, nid), kind, highlight=(nid == st["replaced"]))
        axl.text(0, 1.0, "the fault tree" if phase == 0 else "the fault tree, after the fix",
                 fontsize=9, color=INK2, va="top", transform=axl.transAxes)
        axl.text(0, -0.03, "AND = every input needed.  OR = any input enough.", fontsize=7.6,
                 color=INK2, va="top", transform=axl.transAxes)

        # ---- the expansion
        rules = {
            "start": ("step 2 — start at the top", "Begin with one row: the failure itself.", ""),
            "AND":   ("step 3 — replace each gate", "AND gate: every input is needed, so they "
                      "all join one row.", "T = A \u00b7 B  \u2192  one row grows wider"),
            "OR":    ("step 3 — replace each gate", "OR gate: any input is enough, so each "
                      "input starts a row of its own.", "B = x + y + z  \u2192  one row becomes three"),
            "min":   ("step 4 — keep only the minimal rows", "Discard any row that contains "
                      "another: a bigger combination that includes a smaller one is not minimal.",
                      "what is left are the minimal cut sets"),
        }
        key = ("start" if st["rule"] == "start" else
               "AND" if st["rule"].startswith("AND") else
               "OR" if st["rule"].startswith("OR") else "min")
        _, body, formal = rules[key]
        axr.text(0, 1.0, "the working set", fontsize=9, color=INK2, va="top",
                 transform=axr.transAxes)
        axr.text(0, 0.925, textwrap.fill(body, 40), fontsize=8.6, color=INK, va="top",
                 transform=axr.transAxes, linespacing=1.45)
        if formal:
            axr.text(0, 0.775, formal, fontsize=8, color="#1c5cab", va="top",
                     transform=axr.transAxes, family="DejaVu Sans")
        if st["replaced"]:
            axr.text(0, 0.715, f"replacing: {_label(ft_now, st['replaced'])}", fontsize=8,
                     color="#c14a18", va="top", transform=axr.transAxes)

        y = 0.635
        for row in sorted(st["sets"], key=lambda s: (len(s), sorted(s))):
            items = sorted(row)
            done = all(x in ft_now.events for x in items)
            txt = "  +  ".join(_label(ft_now, x) for x in items)
            wrapped = textwrap.fill(txt, 26)
            axr.text(0.015, y, wrapped, fontsize=8.4, va="top", color=INK,
                     transform=axr.transAxes,
                     bbox=dict(boxstyle="round,pad=0.42",
                               facecolor="#ffffff" if done else "#e8f0fd",
                               edgecolor="#1c5cab" if done else "#86b6ef", linewidth=1.2))
            y -= 0.135 if wrapped.count("\n") == 0 else 0.185
        axr.set_xlim(0, 1); axr.set_ylim(0, 1)

        if key == "min" and phase == 0:
            fig.text(0.665, 0.018, textwrap.fill(
                         "What it implies: both rows hold a single event, so each is a single "
                         "point of failure - nothing else need go wrong. The grid one can be "
                         "answered with a backup supply, which is what redundancy means here: "
                         "turning a one-event row into a two-event row.", 62),
                     fontsize=7.8, color=INK, va="bottom", linespacing=1.55)
        elif key == "min":
            fig.text(0.665, 0.018, textwrap.fill(
                         "After the fix: losing the grid now needs a second failure alongside "
                         "it, so three two-event rows replace one. The hardware fault is "
                         "untouched and still stands alone - redundancy fixed one single point "
                         "of failure, not the other.", 62),
                     fontsize=7.8, color=INK, va="bottom", linespacing=1.55)

        fig.text(0.42, 0.048, "still contains a gate", fontsize=7.6, color=INK2, va="center",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#e8f0fd", edgecolor="#86b6ef"))
        fig.text(0.55, 0.048, "a finished cut set", fontsize=7.6, color=INK2, va="center",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor="#1c5cab"))
        fig.text(0.025, 0.055, "Method: Vesely, Goldberg, Roberts & Haasl,\nFault Tree Handbook "
                 "(NUREG-0492, 1981), ch. VII", fontsize=7.4, color=INK2, va="center",
                 linespacing=1.5)

    anim = FuncAnimation(fig, draw, frames=len(steps), interval=1800)
    anim.save(os.path.join(OUT, "anim_cutsets.gif"), writer=PillowWriter(fps=0.55))
    draw(len(steps) - 1)
    fig.savefig(os.path.join(OUT, "fig3_cutsets_final.png"), facecolor=SURFACE)
    plt.close(fig)


if __name__ == "__main__":
    ft, led, cuts, report, top_p = load()
    ft_before = load_model(os.path.join(HERE, "..", "examples", "processing_power", "model.json"))
    ft_after = load_model(os.path.join(HERE, "..", "examples", "processing_power_backed",
                                       "model.json"))
    fig_mass(report, top_p)
    fig_importance(report)
    anim_cutsets(ft_before, ft_after)
    print("figures written to", OUT)
