#!/usr/bin/env python3
"""Generate phase-1 paper figures from the stabilized synthesis."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.colors import ListedColormap
import numpy as np


OUT = Path(__file__).resolve().parent

COLORS = {
    "ashkenazi": "#2f5d7c",
    "rare": "#7c4d79",
    "jewish": "#2f7d62",
    "litvak": "#c7832e",
    "context": "#7a7a7a",
    "muted": "#e9ecef",
    "ink": "#1f252b",
    "grid": "#c9ced6",
    "pale": "#f7f8fa",
    "accent": "#b94343",
}


def save(fig, stem):
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def local_object_map():
    chrom_lengths = {"chr3": 198.3, "chr9": 141.2, "chr10": 135.5, "chr16": 90.3}
    rows = [
        {
            "chrom": "chr3",
            "start": 47.002931,
            "end": 49.291883,
            "label": "rare founder motif",
            "detail": "13-marker motif; complete 7-position bridge",
            "class": "High confidence compact founder object",
            "color": COLORS["rare"],
        },
        {
            "chrom": "chr3",
            "start": 106.986,
            "end": 107.926,
            "label": "Belorussian/local-Baltic micro-haplotype",
            "detail": "27/27 exact core",
            "class": "Moderate lower-tier micro-haplotype",
            "color": "#6b9d45",
        },
        {
            "chrom": "chr9",
            "start": 71.103406,
            "end": 74.208282,
            "label": "Jewish/Samaritan/Ashkenazi core",
            "detail": "95/95 exact core",
            "class": "High confidence shared Jewish-region object",
            "color": COLORS["jewish"],
        },
        {
            "chrom": "chr9",
            "start": 74.208282,
            "end": 76.891412,
            "label": "Samaritan extension",
            "detail": "right-tail context",
            "class": "Context shell around chr9 core",
            "color": "#8dbfae",
        },
        {
            "chrom": "chr10",
            "start": 63.809527,
            "end": 67.227685,
            "label": "Lithuanian-supported tract",
            "detail": "2.444 cM IBD/exact; 75/75 markers",
            "class": "High confidence regional tract",
            "color": COLORS["litvak"],
        },
        {
            "chrom": "chr16",
            "start": 85.0,
            "end": 90.0,
            "label": "regional context",
            "detail": "diffuse eastern-Mediterranean/Anatolian texture",
            "class": "Context, source object absent",
            "color": COLORS["context"],
            "hatch": "///",
        },
    ]

    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_facecolor("white")
    y_positions = np.arange(len(rows))[::-1]
    bar_h = 0.22

    for yi, row in zip(y_positions, rows):
        length = chrom_lengths[row["chrom"]]
        ax.add_patch(
            patches.FancyBboxPatch(
                (0, yi - bar_h / 2),
                length,
                bar_h,
                boxstyle="round,pad=0.02,rounding_size=0.05",
                facecolor=COLORS["muted"],
                edgecolor="none",
            )
        )
        ax.add_patch(
            patches.FancyBboxPatch(
                (row["start"], yi - 0.16),
                row["end"] - row["start"],
                0.32,
                boxstyle="round,pad=0.02,rounding_size=0.05",
                facecolor=row["color"],
                edgecolor=COLORS["ink"],
                linewidth=0.4,
                hatch=row.get("hatch", None),
            )
        )
        ax.text(-6.5, yi, row["chrom"], ha="right", va="center", fontsize=10.5, color=COLORS["ink"], weight="bold")
        ax.text(length + 4, yi + 0.10, row["label"], ha="left", va="center", fontsize=10.2, color=COLORS["ink"], weight="bold")
        ax.text(length + 4, yi - 0.20, row["detail"], ha="left", va="center", fontsize=8.8, color="#4b5563")
        ax.text((row["start"] + row["end"]) / 2, yi + 0.34, f"{row['start']:.2f}-{row['end']:.2f} Mb",
                ha="center", va="bottom", fontsize=7.7, color="#4b5563")

    ax.set_xlim(-18, 244)
    ax.set_ylim(-0.8, len(rows) - 0.2)
    ax.set_yticks([])
    ax.set_xticks([0, 50, 100, 150, 200])
    ax.set_xlabel("hg19 coordinate within chromosome (Mb)", fontsize=9.8, color=COLORS["ink"])
    ax.tick_params(axis="x", labelsize=8.5, colors="#4b5563")
    ax.grid(axis="x", color="#dfe3e8", linewidth=0.8)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.set_title("Local autosomal objects retained after Ashkenazi-control and phase-aware checks",
                 loc="left", fontsize=13.5, color=COLORS["ink"], weight="bold", pad=14)

    legend_items = [
        ("compact/founder", COLORS["rare"], None),
        ("regional or Jewish-region", COLORS["jewish"], None),
        ("context or lower tier", COLORS["context"], "///"),
    ]
    x0 = 0.04
    xs = [x0, x0 + 0.28, x0 + 0.62]
    for i, (lab, color, hatch) in enumerate(legend_items):
        ax.add_patch(
            patches.Rectangle((xs[i], -0.15), 0.023, 0.033,
                              transform=ax.transAxes, facecolor=color, edgecolor=COLORS["ink"],
                              linewidth=0.4, hatch=hatch, clip_on=False)
        )
        ax.text(xs[i] + 0.03, -0.132, lab, transform=ax.transAxes,
                ha="left", va="center", fontsize=8.0, color="#4b5563")

    save(fig, "fig1_local_object_map")


def chr3_bridge_schematic():
    rows = [
        ("Genome analyzed here", "1111111", "complete bridge"),
        ("Adana23108.HO", "0111111", "primary subclass"),
        ("HGDP00635.HO", "0111111", "primary subclass, high coverage"),
        ("Y064.HO", "0111111", "primary subclass"),
        ("moroccoC61", "0111111", "primary subclass"),
        ("HGDP00672.HO", "1011111", "alternate subclass, high coverage"),
        ("Jordan546", "0001111", "inner/right full-block subclass"),
    ]
    mat = np.array([[int(c) for c in state] for _, state, _ in rows])

    fig = plt.figure(figsize=(10.8, 6.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.6, 1.0], wspace=0.28)
    ax = fig.add_subplot(gs[0, 0])
    cmap = ListedColormap(["#f1f3f5", COLORS["rare"]])
    ax.imshow(mat, aspect="auto", cmap=cmap, vmin=0, vmax=1)

    ax.set_xticks(np.arange(7))
    ax.set_xticklabels([f"B{i}" for i in range(1, 8)], fontsize=9)
    ax.set_yticks(np.arange(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=9.2)
    ax.tick_params(axis="both", length=0)
    ax.set_xlabel("Seven bridge positions inside the 13-marker sparse-panel motif", fontsize=9.5, labelpad=10)

    for i in range(mat.shape[0] + 1):
        ax.axhline(i - 0.5, color="white", linewidth=1.2)
    for j in range(mat.shape[1] + 1):
        ax.axvline(j - 0.5, color="white", linewidth=1.2)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, str(mat[i, j]), ha="center", va="center",
                    fontsize=9.5, color="white" if mat[i, j] else "#6b7280", weight="bold")
    ax.set_title("chr3:47.0-49.3 Mb bridge subclasses", loc="left",
                 fontsize=13.5, color=COLORS["ink"], weight="bold", pad=12)

    for i, (_, _, desc) in enumerate(rows):
        ax.text(7.15, i, desc, va="center", ha="left", fontsize=8.4, color="#4b5563")
    ax.set_xlim(-0.5, 10.6)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis("off")
    ax2.set_title("Anchor behavior", loc="left", fontsize=12.5, color=COLORS["ink"], weight="bold", pad=12)

    scenarios = [
        ("Baseline", [("Jordan546", COLORS["jewish"], 0.45), ("moroccoC61", COLORS["rare"], 0.45)]),
        ("Remove moroccoC61", [("Jordan546 remains", COLORS["jewish"], 0.80)]),
        ("Remove Jordan546", [("moroccoC61 remains", COLORS["rare"], 0.80)]),
        ("Remove both", [("focus signal collapses", "#b8bdc5", 0.62)]),
    ]
    y = 0.84
    for label, parts in scenarios:
        ax2.text(0.0, y + 0.095, label, ha="left", va="center", fontsize=9.2,
                 color=COLORS["ink"], weight="bold")
        x = 0.0
        for txt, col, width in parts:
            ax2.add_patch(
                patches.FancyBboxPatch((x, y - 0.035), width, 0.08,
                                       boxstyle="round,pad=0.01,rounding_size=0.018",
                                       transform=ax2.transAxes, facecolor=col,
                                       edgecolor="none")
            )
            ax2.text(x + width / 2, y + 0.005, txt, ha="center", va="center",
                     fontsize=8.0, color="white" if col != "#b8bdc5" else COLORS["ink"],
                     transform=ax2.transAxes)
            x += width + 0.03
        y -= 0.22

    ax2.text(0.0, 0.03,
             "The bridge pattern is a local analytic construct.\n"
             "It summarizes seven positions inside a broader\n"
             "13-marker motif; route and age need denser exact carriers.",
             ha="left", va="bottom", fontsize=8.5, color="#4b5563", linespacing=1.35,
             transform=ax2.transAxes)

    save(fig, "fig2_chr3_bridge_schematic")


def comparator_matrix():
    rows = [
        ("chr3 rare motif", ["High", "Med", "Med", "", "", ""]),
        ("chr9 Jewish-region core", ["Med", "High", "High", "", "", ""]),
        ("chr10 Lithuanian tract", ["", "", "", "High", "", "Med"]),
        ("R-YP1366 Y line", ["High", "", "", "", "", "High"]),
        ("H1aj1a mtDNA", ["Med", "", "", "Med", "", "High"]),
        ("Roma/Romani story", ["", "", "", "", "High", "Med"]),
    ]
    cols = [
        "exact carriers\nor WGS",
        "Jewish subgroup\npanels",
        "late southern-\nLevant Jewish\ncontext",
        "Baltic/Litvak\nJewish panels",
        "Central/Eastern\nEuropean Roma\ncontrols",
        "public trees\nand projects",
    ]
    level_color = {"High": COLORS["accent"], "Med": COLORS["litvak"], "": "#edf0f2"}
    level_size = {"High": 520, "Med": 330, "": 120}

    fig, ax = plt.subplots(figsize=(10.8, 6.3))
    ax.set_xlim(-0.7, len(cols) - 0.3)
    ax.set_ylim(-0.8, len(rows) - 0.2)
    ax.invert_yaxis()
    ax.set_facecolor("white")

    for x in range(len(cols)):
        ax.axvline(x, color="#e1e5ea", linewidth=0.8, zorder=0)
    for y in range(len(rows)):
        ax.axhline(y, color="#e1e5ea", linewidth=0.8, zorder=0)

    for y, (row_label, vals) in enumerate(rows):
        ax.text(-0.85, y, row_label, ha="right", va="center", fontsize=10,
                color=COLORS["ink"], weight="bold")
        for x, val in enumerate(vals):
            ax.scatter([x], [y], s=level_size[val], c=level_color[val],
                       edgecolor="white", linewidth=1.2, zorder=3)
            if val:
                ax.text(x, y, val, ha="center", va="center", fontsize=8.0,
                        color="white", weight="bold", zorder=4)

    ax.set_xticks(np.arange(len(cols)))
    ax.set_xticklabels(cols, fontsize=9, rotation=0, ha="center")
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", length=0, pad=8)
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title("Data that would sharpen each retained target", loc="left",
                 fontsize=13.5, color=COLORS["ink"], weight="bold", pad=40)
    ax.text(-0.85, len(rows) - 0.02,
            "High = likely to change resolution; Med = useful comparison layer",
            ha="left", va="bottom", fontsize=8.8, color="#4b5563")
    save(fig, "fig3_comparator_matrix")


def main():
    local_object_map()
    chr3_bridge_schematic()
    comparator_matrix()


if __name__ == "__main__":
    main()
