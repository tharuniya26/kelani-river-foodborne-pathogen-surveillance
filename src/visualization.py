"""Generate figures from the published aggregate table."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .data_processing import published_data
from .statistical_analysis import interval_table

ROOT = Path(__file__).resolve().parents[1]
SITES = ["Skin", "Mouth", "Gills", "Gut"]
GROUPS = ["Staphylococcus spp.", "Salmonella spp.", "Shigella spp."]
COLORS = ["#0072B2", "#D55E00", "#009E73"]


def save(fig, name, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(directory / f"{name}.png", dpi=220, bbox_inches="tight")
    fig.savefig(directory / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def generate_figures(directory=ROOT / "figures"):
    data = published_data()
    matrix = np.array([[float(data.loc[(data.pathogen == g) & (data.anatomical_site == s),
                                        "detection_percentage"].iloc[0]) for s in SITES] for g in GROUPS])
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(8, 3.6))
    im = ax.imshow(matrix, cmap="YlGnBu", vmin=0, vmax=100)
    ax.set_xticks(range(4), SITES); ax.set_yticks(range(3), GROUPS)
    for i in range(3):
        for j in range(4):
            ax.text(j, i, f"{matrix[i,j]:.1f}%", ha="center", va="center",
                    color="white" if matrix[i,j] > 55 else "black")
    fig.colorbar(im, ax=ax, label="Specimens with detected organism (%)")
    ax.set_title("Published detection proportions by anatomical site")
    save(fig, "01_heatmap", directory)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    x = np.arange(4); width = .25
    for i, group in enumerate(GROUPS):
        sub = data.set_index(["pathogen", "anatomical_site"])
        vals = [sub.loc[(group, site), "detection_percentage"] for site in SITES]
        counts = [sub.loc[(group, site), "positive_count"] for site in SITES]
        bars = ax.bar(x + (i-1)*width, vals, width, color=COLORS[i], label=group)
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1, f"{count}/27",
                    ha="center", va="bottom", fontsize=8, rotation=45)
    ax.set_xticks(x, SITES); ax.set_ylim(0, 117); ax.set_ylabel("Detection (%)")
    ax.legend(ncol=3, fontsize=8, loc="upper center")
    save(fig, "02_grouped_bars", directory)

    ci = interval_table()
    fig, axes = plt.subplots(1, 3, figsize=(11, 4), sharey=True)
    for i, (ax, group) in enumerate(zip(axes, GROUPS)):
        sub = ci.set_index(["pathogen", "anatomical_site"])
        p = np.array([sub.loc[(group, s), "detection_proportion"] for s in SITES])
        lo = np.array([sub.loc[(group, s), "wilson_low"] for s in SITES])
        hi = np.array([sub.loc[(group, s), "wilson_high"] for s in SITES])
        ax.errorbar(np.arange(4), p*100, yerr=np.vstack(((p-lo)*100, (hi-p)*100)),
                    fmt="o", capsize=4, color=COLORS[i])
        ax.set_xticks(range(4), SITES, rotation=45); ax.set_title(group, fontsize=10)
        ax.set_ylim(0, 110); ax.grid(axis="y", alpha=.2)
    axes[0].set_ylabel("Detection (%) with marginal 95% Wilson interval")
    save(fig, "03_wilson_intervals", directory)

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)
    for i, (ax, group) in enumerate(zip(axes, GROUPS)):
        ax.bar(SITES, matrix[i], color=COLORS[i], alpha=.85)
        ax.set_title(group, fontsize=10); ax.set_ylim(0, 105)
        for j, value in enumerate(matrix[i]): ax.text(j, value+2, f"{value:.1f}", ha="center", fontsize=8)
    axes[0].set_ylabel("Detection (%)")
    save(fig, "04_detection_profiles", directory)

    fig, ax = plt.subplots(figsize=(12, 2.6)); ax.axis("off")
    labels = ["Fish sampling", "Anatomical\nsampling", "Culture and\nenrichment", "Biochemical\nidentification", "Aggregate\nobservations", "Statistical\nanalysis", "Public health\ninterpretation"]
    for i, label in enumerate(labels):
        xpos = .02 + i*.14
        ax.text(xpos+.06, .52, label, ha="center", va="center", fontsize=8,
                bbox=dict(boxstyle="round,pad=.5", fc="#eaf4f6", ec="#0072B2"), transform=ax.transAxes)
        if i < len(labels)-1:
            ax.annotate("", xy=(xpos+.14, .52), xytext=(xpos+.12, .52),
                        arrowprops=dict(arrowstyle="->", color="#333"), xycoords="axes fraction")
    ax.set_title("Reconstruction from documented methods; analysis is a later extension", fontsize=11)
    save(fig, "05_workflow", directory)

    fig, ax = plt.subplots(figsize=(9, 2.3)); ax.axis("off")
    rows = [["Report results", "Staph. gut", "22/27 = 81.48%"],
            ["Report discussion", "Staph. gut", "22/25 = 88.00%; text says 81.48%"],
            ["Abstract", "Staph. gut", "22/27 = 81.48%"],
            ["Report discussion", "Shigella gut/gills", "Percentages mispaired with counts"]]
    table = ax.table(cellText=rows, colLabels=["Source", "Item", "Reading"], loc="center", cellLoc="left",
                     colWidths=[.25,.24,.51])
    table.auto_set_font_size(False); table.set_fontsize(8); table.scale(1, 1.7)
    ax.set_title("Source reconciliation overview")
    save(fig, "06_source_comparison", directory)


if __name__ == "__main__":
    generate_figures()
