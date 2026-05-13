#!/usr/bin/env python3
"""Narrow confirmation sweep for the catch-rematched composite v0.2 candidate.

The script holds the v01 transition layer fixed, sweeps / confirms the v0.2
capacity-support family, and writes compact CSV/JSON outputs. It is intentionally
GitHub-sized: it records aggregate and per-slice summaries, not tensor archives.

Run from the bundle root:

    python code/run_v02_confirmation.py --outdir data_recomputed

The default grid reproduces the bundled confirmation table at 41 x 17 x 4.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd


def load_adm_module(path: Path):
    spec = importlib.util.spec_from_file_location("adm", path)
    adm = importlib.util.module_from_spec(spec)
    sys.modules["adm"] = adm
    assert spec.loader is not None
    spec.loader.exec_module(adm)
    return adm


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="data_recomputed")
    parser.add_argument("--grid-nl", type=int, default=41)
    parser.add_argument("--grid-nth", type=int, default=17)
    parser.add_argument("--grid-nph", type=int, default=4)
    parser.add_argument("--adm", default="code/adm_3p1_viability_v3_baware.py")
    args = parser.parse_args()

    root = Path.cwd()
    out = root / args.outdir
    out.mkdir(parents=True, exist_ok=True)
    adm = load_adm_module(root / args.adm)

    transition = dict(
        v_exit=0.5,
        x_catch=0.05,
        x_beta=0.70,
        x_q=1.25,
        w_catch=0.25,
        w_beta=0.28,
        w_q=0.30,
        p_beta=4.0,
        packet_radius=0.35,
    )
    base_v1 = dict(
        B0=8.0,
        wB=10.0,
        T_B=150.0,
        T_R=5.0,
        T_H=60.0,
        T_C=20.0,
        T_Breset=150.0,
        n_sh_amp=-0.18,
        n_sh_center=2.3,
        n_sh_width=1.0,
    )
    fixed = dict(Rth=1.25, wth=0.12, Rpass=0.35, wpass=0.08)
    scenarios = [("V5_lam575", 5.0, 5.75), ("V10_lam6", 10.0, 6.0), ("V10_lam115", 10.0, 11.5)]
    x_values = [0.05, 0.35, 0.70, 1.00, 1.25]

    gp = adm.GridParams(nl=args.grid_nl, nth=args.grid_nth, nph=args.grid_nph, l_min=-2.4, l_max=2.4)
    coords = adm.make_grid(gp)

    def eval_candidate(label: str, pkt_vars: dict, v1_vars: dict, r_mode: str = "always_open"):
        clear = True
        per = []
        for scen, V, lam in scenarios:
            pp = adm.PacketParams(**{**transition, **pkt_vars, "V": V, "lambda_factor": lam})
            v1p = adm.V1Params(**{**base_v1, **v1_vars})
            t_cycle = adm.cycle_time_from_phase("hold_mid", v1p)
            for X in x_values:
                summary, _tensors = adm.evaluate_slice(t_cycle, X, coords, v1p, pp, r_mode, dt_time=1e-3)
                compact = adm.compact_status(summary)
                compact.update({"label": label, "scenario": scen, "V": V, "lambda_factor": lam, "X": X})
                per.append(compact)
                if compact["packet_fail_points"] > 0 or compact["edge_fail_points"] > 0:
                    clear = False
                if compact["packet_max_norm"] >= 0 or compact["edge_max_gtt"] >= 0:
                    clear = False

        def maxraw(key: str) -> float:
            return max(c[key] for c in per if c.get(key) is not None)

        def maxabs(key: str) -> float:
            return max(abs(c[key]) for c in per if c.get(key) is not None)

        agg = {
            "label": label,
            "clear": bool(clear),
            **{f"pkt_{k}": v for k, v in pkt_vars.items()},
            **{f"v1_{k}": v for k, v in v1_vars.items()},
            "max_packet_norm": maxraw("packet_max_norm"),
            "max_edge_gtt": maxraw("edge_max_gtt"),
            "max_release_packet_norm": maxraw("release_packet_max_norm"),
            "rhoH_packet_p95_max": maxabs("rho_H_packet_p95_abs"),
            "rhoH_edge_p95_max": maxabs("rho_H_edge_p95_abs"),
            "R3_packet_p95_max": maxabs("R3_packet_p95_abs"),
            "K_packet_p95_max": maxabs("K_packet_p95_abs"),
            "j_packet_p95_max": maxabs("j_packet_p95_abs"),
            "j_edge_p95_max": maxabs("j_edge_p95_abs"),
            "packet_fail_total": sum(c["packet_fail_points"] for c in per),
            "edge_fail_total": sum(c["edge_fail_points"] for c in per),
        }
        agg["J_geom"] = max(agg["rhoH_packet_p95_max"], agg["rhoH_edge_p95_max"]) + 0.05 * agg["R3_packet_p95_max"]
        agg["J_dyn"] = agg["j_packet_p95_max"] + agg["j_edge_p95_max"] + 0.02 * agg["K_packet_p95_max"]
        agg["J_total"] = agg["J_geom"] + agg["J_dyn"]
        return agg, per

    candidates = [
        ("v01_geometry_baseline", {"C0": 100.0, "C_perp": 1.0, "Rth": 0.75, "wth": 0.05, "Rpass": 0.35, "wpass": 0.05}, {"B0": 8.0, "wB": 10.0}),
        ("C20_Cp3_B6_wB12", {**fixed, "C0": 20.0, "C_perp": 3.0}, {"B0": 6.0, "wB": 12.0}),
        ("C20_Cp3_B6_wB6", {**fixed, "C0": 20.0, "C_perp": 3.0}, {"B0": 6.0, "wB": 6.0}),
        ("C35_Cp3_B6_wB6", {**fixed, "C0": 35.0, "C_perp": 3.0}, {"B0": 6.0, "wB": 6.0}),
        ("C35_Cp3_B6_wB12", {**fixed, "C0": 35.0, "C_perp": 3.0}, {"B0": 6.0, "wB": 12.0}),
        ("C50_Cp3_B6_wB12", {**fixed, "C0": 50.0, "C_perp": 3.0}, {"B0": 6.0, "wB": 12.0}),
        ("C20_Cp4_B6_wB12", {**fixed, "C0": 20.0, "C_perp": 4.0}, {"B0": 6.0, "wB": 12.0}),
        ("C20_Cp5_B6_wB12", {**fixed, "C0": 20.0, "C_perp": 5.0}, {"B0": 6.0, "wB": 12.0}),
        ("C100_Cp5_B4_wB6", {**fixed, "C0": 100.0, "C_perp": 5.0}, {"B0": 4.0, "wB": 6.0}),
        ("C20_Cp1_B6_wB12_noangular", {**fixed, "C0": 20.0, "C_perp": 1.0}, {"B0": 6.0, "wB": 12.0}),
    ]

    rows = []
    perrows = []
    start = time.time()
    for label, pkt, v1 in candidates:
        agg, per = eval_candidate(label, pkt, v1)
        rows.append(agg)
        perrows.extend(per)
        print(f"done {label}: clear={agg['clear']} J_total={agg['J_total']:.6g}", flush=True)

    df = pd.DataFrame(rows)
    base = df[df.label == "v01_geometry_baseline"].iloc[0]
    for col in ["J_geom", "J_dyn", "J_total", "rhoH_packet_p95_max", "rhoH_edge_p95_max", "R3_packet_p95_max", "K_packet_p95_max", "j_packet_p95_max", "j_edge_p95_max"]:
        df["rel_" + col] = df[col] / base[col]

    df.to_csv(out / "selected_confirmation_41x17.csv", index=False)
    pd.DataFrame(perrows).to_csv(out / "selected_confirmation_41x17_per_slice.csv", index=False)
    summary = {
        "grid": f"{args.grid_nl}x{args.grid_nth}x{args.grid_nph}",
        "scenarios": scenarios,
        "X_values": x_values,
        "rows": df.sort_values(["rel_J_total", "rel_J_geom"]).to_dict(orient="records"),
        "elapsed_seconds": time.time() - start,
    }
    (out / "selected_confirmation_summary.json").write_text(json.dumps(summary, indent=2))
    print(df.sort_values(["rel_J_total", "rel_J_geom"])[["label", "clear", "rel_J_total", "rel_J_geom", "rel_J_dyn", "max_packet_norm", "max_edge_gtt", "max_release_packet_norm", "pkt_C0", "pkt_C_perp", "v1_B0", "v1_wB"]].to_string(index=False))


if __name__ == "__main__":
    main()
