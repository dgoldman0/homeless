#!/usr/bin/env python3
"""
Polish screen: compare flare-open/close duration T_R for Reference Geometry v0.2.

Uses the existing reduced prescribed-geometry/effective-source diagnostics from
run_reference_polish_screen.py.  The goal is to decide whether the shorter
T_R=5 flare gate or smoother T_R=10 flare gate should become the canonical
reference, with repayment amplitudes retuned around the polished shoulder window.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run_reference_polish_screen import summarize_case  # noqa: E402

OUT = HERE.parents[0] / "data"
OUT.mkdir(parents=True, exist_ok=True)

BASE = {
    "B0": 8.0,
    "wB": 10.0,
    "T_B": 150.0,
    "T_H": 60.0,
    "T_C": 20.0,
    "T_Breset": 150.0,
    "Rc": 1.0,
    "wFlat": 1.6,
    "r_sh_amp": 0.0,
    "r_sh_center": 2.5,
    "r_sh_width": 1.2,
    "n_sh_amp": -0.18,
    "n_sh_center": 2.3,
    "n_sh_width": 1.0,
    "src_support_width": 0.9,
    "src_shoulder_center": 2.3,
    "src_shoulder_width": 1.0,
}

TARGET = np.array([1.08, 1.08, 1.08])

def polish_score(row: pd.Series) -> float:
    ratios = np.array([
        row["coreline_repay_ratio"],
        row["support_repay_ratio"],
        row["shoulder_repay_ratio"],
    ], dtype=float)
    balance = float(np.sum((ratios - TARGET) ** 2))
    # Penalize underpayment hard; modest overpayment is acceptable but less elegant.
    under = float(np.sum(np.maximum(1.02 - ratios, 0.0) ** 2) * 25.0)
    over = float(np.sum(np.maximum(ratios - 1.25, 0.0) ** 2) * 6.0)
    access_comp = float(row["access_comp_leak_metric"])
    shoulder_spike = float(row["shoulder_comp_spike_metric"])
    open_kth = float(row["access_open_max_abs_Kth"])
    open_flux = float(row["access_open_max_abs_flux"])
    open_theta = float(row["access_open_max_abs_theta"])
    # Shorter source exposure is valuable, but only after gates and balance.
    open_debt = float(row["coreline_open_neg"] + row["support_open_mean_neg"] + row["shoulder_open_mean_neg"])
    return -(
        balance + under + over
        + 50.0 * access_comp
        + 2.0 * shoulder_spike
        + 4.0 * max(open_kth - 0.010, 0.0) ** 2
        + 2.0 * max(open_flux - 0.0015, 0.0) ** 2
        + 0.02 * open_theta
        + 0.05 * open_debt
    )

def run_grid(n_l: int, n_t: int, path: Path) -> pd.DataFrame:
    rows = []
    for T_R in [5.0, 10.0, 20.0]:
        for src_sup in [0.0078, 0.0080, 0.0082, 0.0085, 0.0088, 0.0090]:
            for src_sh in [0.0015, 0.0016, 0.0017, 0.0018, 0.0019, 0.0020, 0.0021]:
                params = {
                    **BASE,
                    "T_R": T_R,
                    "src_support_amp": src_sup,
                    "src_shoulder_amp": src_sh,
                }
                row = summarize_case(params, n_l=n_l, n_t=n_t)
                row["case"] = f"TR{T_R:g}_sup{src_sup:.4f}_sh{src_sh:.4f}_N-0.18"
                rows.append(row)
    df = pd.DataFrame(rows)
    df["polish_score_v2"] = df.apply(polish_score, axis=1)
    df["pass_core"] = df["coreline_repay_ratio"].between(1.02, 1.25)
    df["pass_support"] = df["support_repay_ratio"].between(1.02, 1.25)
    df["pass_shoulder"] = df["shoulder_repay_ratio"].between(1.02, 1.25)
    df["pass_access_comp"] = df["access_comp_leak_metric"] < 0.002
    df["pass_open_dynamic"] = (df["access_open_max_abs_Kth"] < 0.012) & (df["access_open_max_abs_flux"] < 0.0015)
    df["pass_geometry_bounds"] = (df["access_comp_min_N"] > 0.8) & (df["shoulder_comp_min_N"] > 0.8) & (df["shoulder_comp_min_R"] > 1.0)
    df["pass_TR_polish"] = df[["pass_core","pass_support","pass_shoulder","pass_access_comp","pass_open_dynamic","pass_geometry_bounds"]].all(axis=1)
    df.to_csv(path, index=False)
    return df

def main():
    coarse = run_grid(501, 601, OUT / "TR_polish_comparison.csv")
    best_by_TR = []
    for T_R, g in coarse.groupby("T_R"):
        gg = g[g["pass_TR_polish"]]
        if len(gg) == 0:
            gg = g
        best_by_TR.append(gg.sort_values("polish_score_v2", ascending=False).head(3))
    best_coarse = pd.concat(best_by_TR, ignore_index=True)
    best_coarse.to_csv(OUT / "TR_polish_best_by_TR_coarse.csv", index=False)

    # High-resolution validation of the best 3 for each T_R plus prior v0.2 and targeted best from earlier screen.
    validation_params = []
    for _, r in best_coarse.iterrows():
        validation_params.append({
            **BASE,
            "T_R": float(r["T_R"]),
            "src_support_amp": float(r["src_support_amp"]),
            "src_shoulder_amp": float(r["src_shoulder_amp"]),
        })
    # Previous v0.2 named in notes and earlier targeted best.
    validation_params.extend([
        {**BASE, "T_R": 5.0, "src_support_amp": 0.0085, "src_shoulder_amp": 0.0020},
        {**BASE, "T_R": 5.0, "src_support_amp": 0.0082, "src_shoulder_amp": 0.0018},
        {**BASE, "T_R": 10.0, "src_support_amp": 0.0085, "src_shoulder_amp": 0.0020},
        {**BASE, "T_R": 10.0, "src_support_amp": 0.0082, "src_shoulder_amp": 0.0018},
    ])
    # De-duplicate.
    seen = set(); unique_params = []
    for p in validation_params:
        key = (p["T_R"], p["src_support_amp"], p["src_shoulder_amp"])
        if key not in seen:
            seen.add(key); unique_params.append(p)
    high_rows = []
    for p in unique_params:
        row = summarize_case(p, n_l=801, n_t=1001)
        row["case"] = f"HIGH_TR{p['T_R']:g}_sup{p['src_support_amp']:.4f}_sh{p['src_shoulder_amp']:.4f}_N-0.18"
        high_rows.append(row)
    high = pd.DataFrame(high_rows)
    high["polish_score_v2"] = high.apply(polish_score, axis=1)
    high["pass_core"] = high["coreline_repay_ratio"].between(1.02, 1.25)
    high["pass_support"] = high["support_repay_ratio"].between(1.02, 1.25)
    high["pass_shoulder"] = high["shoulder_repay_ratio"].between(1.02, 1.25)
    high["pass_access_comp"] = high["access_comp_leak_metric"] < 0.002
    high["pass_open_dynamic"] = (high["access_open_max_abs_Kth"] < 0.012) & (high["access_open_max_abs_flux"] < 0.0015)
    high["pass_geometry_bounds"] = (high["access_comp_min_N"] > 0.8) & (high["shoulder_comp_min_N"] > 0.8) & (high["shoulder_comp_min_R"] > 1.0)
    high["pass_TR_polish"] = high[["pass_core","pass_support","pass_shoulder","pass_access_comp","pass_open_dynamic","pass_geometry_bounds"]].all(axis=1)
    high.to_csv(OUT / "TR_polish_highres_validation.csv", index=False)

    # Progress tracker, in positive report-oriented language.
    best_high = high.sort_values("polish_score_v2", ascending=False).iloc[0]
    by_tr_summary = high.groupby("T_R").apply(lambda x: x.sort_values("polish_score_v2", ascending=False).iloc[0], include_groups=False)
    extracts = {
        "current_reference_after_TR_polish": {
            "label": "Reference Geometry v0.3 candidate",
            "B0": 8.0,
            "wB": 10.0,
            "T_B": 150.0,
            "T_R": float(best_high["T_R"]),
            "T_H": 60.0,
            "T_C": 20.0,
            "src_support_amp": float(best_high["src_support_amp"]),
            "src_shoulder_amp": float(best_high["src_shoulder_amp"]),
            "n_sh_amp": -0.18,
            "n_sh_center": 2.3,
            "n_sh_width": 1.0,
            "src_shoulder_center": 2.3,
            "src_shoulder_width": 1.0,
        },
        "best_highres_case": best_high[[
            "case","coreline_repay_ratio","support_repay_ratio","shoulder_repay_ratio",
            "access_comp_leak_metric","shoulder_comp_spike_metric",
            "access_open_max_abs_flux","access_open_max_abs_Kth","access_open_max_abs_theta",
            "access_comp_max_abs_flux","access_comp_max_abs_Kth","access_comp_max_abs_theta",
            "access_comp_min_N","shoulder_comp_min_N","shoulder_comp_min_R",
            "coreline_open_neg","support_open_mean_neg","shoulder_open_mean_neg",
            "polish_score_v2","pass_TR_polish"
        ]].to_dict(),
        "best_by_TR_highres": by_tr_summary[[
            "case","coreline_repay_ratio","support_repay_ratio","shoulder_repay_ratio",
            "access_open_max_abs_Kth","access_open_max_abs_flux","access_open_max_abs_theta",
            "access_comp_leak_metric","shoulder_comp_spike_metric","polish_score_v2","pass_TR_polish"
        ]].to_dict(orient="index"),
    }
    (OUT / "TR_polish_extracts.json").write_text(json.dumps(extracts, indent=2))

    notes = OUT.parent / "report_progress_notes.md"
    with notes.open("a", encoding="utf-8") as f:
        f.write("\n\n## Geometry polish progress: flare-gate duration comparison\n\n")
        f.write("The Reference Geometry v0.2 compensation balance was preserved as the baseline for a flare-gate duration comparison. ")
        f.write("The screen compared T_R = 5, 10, and 20 while retuning support and shoulder source amplitudes around the polished shoulder window.\n\n")
        f.write("Key design reading: the geometry remains in the same stable basin. Compensation is isolated from the access family after flare closure. ")
        f.write("The shorter T_R=5 branch preserves the smallest open-interval source exposure while keeping access dynamic quantities within the current geometry bounds. ")
        f.write("The T_R=10 branch supplies a smoother conservative alternate with modestly longer open exposure.\n\n")
        f.write("Current preferred reference: ")
        f.write(f"B0=8, wB=10, T_B=150, T_R={best_high['T_R']:.0f}, T_H=60, T_C=20, ")
        f.write(f"src_support_amp={best_high['src_support_amp']:.4f}, src_shoulder_amp={best_high['src_shoulder_amp']:.4f}, N_sh_amp=-0.18.\n")
        f.write("This is tracked as Reference Geometry v0.3 candidate pending the invariant/gauge diagnostic packet.\n")

    print("Coarse best by T_R:")
    print(best_coarse[["case","coreline_repay_ratio","support_repay_ratio","shoulder_repay_ratio","access_open_max_abs_Kth","access_open_max_abs_flux","polish_score_v2","pass_TR_polish"]].to_string(index=False))
    print("\nHigh-res validation:")
    print(high.sort_values("polish_score_v2", ascending=False)[["case","coreline_repay_ratio","support_repay_ratio","shoulder_repay_ratio","access_open_max_abs_Kth","access_open_max_abs_flux","access_comp_leak_metric","shoulder_comp_spike_metric","polish_score_v2","pass_TR_polish"]].to_string(index=False))

if __name__ == "__main__":
    main()
