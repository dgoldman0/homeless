#!/usr/bin/env python3
"""Build paper figures from compact CSV data.

Run from the repository bundle root:
    python scripts/build_paper_figures.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

conf = pd.read_csv(ROOT / "data/geometry_v02/selected_confirmation_41x17.csv")
rows = conf.set_index("label")

# Burden-channel comparison.
fig, ax = plt.subplots(figsize=(7, 4.3))
labels = ["v01 geometry baseline", "no-angular", "v1 default"]
keys = ["v01_geometry_baseline", "C20_Cp1_B6_wB12_noangular", "C20_Cp5_B6_wB12_prior"]
geom = [rows.loc[k, "rel_J_geom"] for k in keys]
dyn = [rows.loc[k, "rel_J_dyn"] for k in keys]
total = [rows.loc[k, "rel_J_total"] for k in keys]
x = np.arange(len(labels)); w = 0.25
ax.bar(x-w, geom, w, label="geometry cost")
ax.bar(x, dyn, w, label="dynamic cost")
ax.bar(x+w, total, w, label="total cost")
ax.set_xticks(x); ax.set_xticklabels(labels, rotation=20, ha="right")
ax.set_ylabel("relative to v01 geometry baseline")
ax.set_title("Burden-channel comparison")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "burden_channel_comparison.png", dpi=180)
plt.close(fig)

# Mixed capacity comparison.
fig, ax = plt.subplots(figsize=(7, 4.3))
keys = ["C20_Cp1_B6_wB12_noangular", "C20_Cp3_B6_wB12", "C20_Cp4_B6_wB12", "C20_Cp5_B6_wB12_prior"]
labels = [r"$C_\perp=1$", r"$C_\perp=3$", r"$C_\perp=4$", r"$C_\perp=5$"]
geom = [rows.loc[k, "rel_J_geom"] for k in keys]
dyn = [rows.loc[k, "rel_J_dyn"] for k in keys]
total = [rows.loc[k, "rel_J_total"] for k in keys]
x = np.arange(len(labels)); w = 0.25
ax.bar(x-w, geom, w, label="geometry")
ax.bar(x, dyn, w, label="dynamic")
ax.bar(x+w, total, w, label="total")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("relative to v01 geometry baseline")
ax.set_title("Mixed radial/angular capacity comparison")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "mixed_capacity_comparison.png", dpi=180)
plt.close(fig)

# Quantum source-exposure proxy.
q = pd.read_csv(ROOT / "data/quantum_screen/quantum_source_proxy_summary.csv")
sub = q[q["scenario"] == "V10_lam6"].set_index("label")
baseline = abs(sub.loc["v01_geometry_baseline", "packet_lor_min_tau0.2"])
labels = ["v01 baseline", "v1 default", "no-angular", "reserve"]
keys = ["v01_geometry_baseline", "v02_C20_Cp5_B6_wB12", "v02_noangular_C20_Cp1_B6_wB12", "v02_reserve_C100_Cp5_B4_wB6"]
lor = [abs(sub.loc[k, "packet_lor_min_tau0.2"]) / baseline for k in keys]
negvol = [sub.loc[k, "rel_max_packet_neg_volume_proxy"] for k in keys]
fig, ax = plt.subplots(figsize=(7, 4.3))
x = np.arange(len(labels)); w = 0.35
ax.bar(x-w/2, lor, w, label="Lorentzian sampled floor")
ax.bar(x+w/2, negvol, w, label="negative-volume proxy")
ax.set_xticks(x); ax.set_xticklabels(labels, rotation=15, ha="right")
ax.set_ylabel("relative to v01 baseline")
ax.set_title(r"Packet source-exposure proxy at $V=10,\lambda=6$")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "packet_exposure_proxy.png", dpi=180)
plt.close(fig)

# Grid sensitivity.
rob = pd.read_csv(ROOT / "data/robustness/grid_pressure_robustness_summary.csv")
fig, ax = plt.subplots(figsize=(7, 4.3))
for label, name in [
    ("candidate_C20_Cp5_B6_wB12", "v1 default"),
    ("noangular_C20_Cp1_B6_wB12", "no-angular"),
    ("v01_baseline", "v01 baseline"),
]:
    ss = rob[rob["label"] == label].sort_values("nl")
    xx = [f"{int(n)}x{int(t)}" for n, t in zip(ss["nl"], ss["nth"])]
    ax.plot(xx, ss["rel_J_total"], marker="o", label=name)
ax.set_ylabel("relative total cost")
ax.set_xlabel("grid")
ax.set_title("Grid-sensitivity ordering")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "grid_sensitivity.png", dpi=180)
plt.close(fig)

print("figures written to", FIG)
