#!/usr/bin/env python3
"""
Invariant/gauge diagnostic packet for Reference Geometry v0.3 candidate.

Uses the reduced prescribed-geometry/effective-source model from the polish screens.
Outputs phase/zone extrema, lifecycle time-series diagnostics, timeslice profiles,
and an extracts JSON suitable for the eventual geometry report.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run_reference_polish_screen import (  # noqa: E402
    make_geometry,
    diagnostics_general,
    window_core,
    window_shoulder,
)

OUT = HERE.parents[0] / "data"
OUT.mkdir(parents=True, exist_ok=True)

PARAMS = {
    "label": "Reference Geometry v0.3 candidate",
    "B0": 8.0,
    "wB": 10.0,
    "T_B": 150.0,
    "T_R": 5.0,
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
    "src_support_amp": 0.0082,
    "src_support_width": 0.9,
    "src_shoulder_amp": 0.0019,
    "src_shoulder_center": 2.3,
    "src_shoulder_width": 1.0,
}


def proper_half_length_to_R(l: np.ndarray, B_row: np.ndarray, R_row: np.ndarray, target: float) -> float:
    pos = l >= 0
    ll = l[pos]
    BB = B_row[pos]
    RR = R_row[pos]
    mask = RR <= target
    if np.sum(mask) < 2:
        return float("nan")
    return float(np.trapezoid(BB[mask], ll[mask]))


def phase_masks(phase: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "B_setup": phase == "B_setup",
        "R_open": phase == "R_open",
        "hold": phase == "hold",
        "R_close": phase == "R_close",
        "comp": phase == "comp",
        "B_reset": phase == "B_reset",
        "open_interval": (phase == "R_open") | (phase == "hold") | (phase == "R_close"),
        "full_cycle": np.ones_like(phase, dtype=bool),
    }


def main() -> None:
    # Higher resolution than the polish screens but still lightweight enough for repeatable local runs.
    l = np.linspace(-18.0, 18.0, 1201)
    t_end = PARAMS["T_B"] + 2 * PARAMS["T_R"] + PARAMS["T_H"] + PARAMS["T_C"] + PARAMS["T_Breset"]
    t = np.linspace(0.0, t_end, 1601)

    N, B, R, phase, times, C = make_geometry(t, l, PARAMS)
    d = diagnostics_general(t, l, N, B, R)

    # Explicit source overlay for the null-contracted ledger, kept separate from geometry-only diagnostics.
    src = np.zeros_like(d["Tkk_min"])
    src += PARAMS["src_support_amp"] * C[:, None] * window_core(l, PARAMS["src_support_width"])[None, :]
    src += PARAMS["src_shoulder_amp"] * C[:, None] * window_shoulder(
        l, PARAMS["src_shoulder_center"], PARAMS["src_shoulder_width"]
    )[None, :]
    Tkk_total = d["Tkk_min"] + src

    # Additional derivative/proxy packet.
    Bt = np.gradient(B, t, axis=0, edge_order=2)
    Nt = np.gradient(N, t, axis=0, edge_order=2)
    Rt = np.gradient(R, t, axis=0, edge_order=2)
    B_l = np.gradient(B, l, axis=1, edge_order=2)
    N_l = np.gradient(N, l, axis=1, edge_order=2)
    R_l = np.gradient(R, l, axis=1, edge_order=2)
    R_ll = np.gradient(R_l, l, axis=1, edge_order=2)
    R_tt = np.gradient(Rt, t, axis=0, edge_order=2)
    dlogB_dl = B_l / B
    dlogN_dl = N_l / N
    B_rate = Bt / (N * B)
    N_rate = Nt / N
    R_rate = Rt / (N * R)

    arrays = {
        "N": N,
        "B": B,
        "R": R,
        "rho_geo": d["rho"],
        "pr_geo": d["pr"],
        "flux_geo": d["flux"],
        "Tkk_geo_min": d["Tkk_min"],
        "Tkk_total_min": Tkk_total,
        "src_Tkk_overlay": src,
        "Kll": d["Kll"],
        "Kth": d["Kth"],
        "theta_plus": d["theta_plus"],
        "theta_minus": d["theta_minus"],
        "abs_theta": np.maximum(np.abs(d["theta_plus"]), np.abs(d["theta_minus"])),
        "B_rate": B_rate,
        "N_rate": N_rate,
        "R_rate": R_rate,
        "dlogB_dl": dlogB_dl,
        "dlogN_dl": dlogN_dl,
        "R_l": R_l,
        "R_ll": R_ll,
        "R_t": Rt,
        "R_tt": R_tt,
    }

    zones = {
        "access": np.abs(l) <= 0.25,
        "support": np.abs(l) <= 0.75,
        "inner_shoulder": (np.abs(l) >= 1.2) & (np.abs(l) <= 2.7),
        "outer_shoulder": (np.abs(l) > 2.7) & (np.abs(l) <= 4.5),
        "shoulder": (np.abs(l) >= 1.2) & (np.abs(l) <= 4.5),
        "matching": (np.abs(l) > 4.5) & (np.abs(l) <= 9.0),
        "exterior": (np.abs(l) > 9.0) & (np.abs(l) <= 14.0),
    }
    pmasks = phase_masks(phase)

    # Phase-zone extrema table.
    rows = []
    for ph, tm in pmasks.items():
        if not np.any(tm):
            continue
        for zn, zm in zones.items():
            idx = np.ix_(tm, zm)
            row = {"phase": ph, "zone": zn}
            row["min_N"] = float(np.min(N[idx]))
            row["min_R"] = float(np.min(R[idx]))
            row["max_B"] = float(np.max(B[idx]))
            row["min_Tkk_geo"] = float(np.min(d["Tkk_min"][idx]))
            row["min_Tkk_total"] = float(np.min(Tkk_total[idx]))
            row["max_Tkk_total"] = float(np.max(Tkk_total[idx]))
            row["max_abs_flux_geo"] = float(np.max(np.abs(d["flux"][idx])))
            row["max_abs_Kll"] = float(np.max(np.abs(d["Kll"][idx])))
            row["max_abs_Kth"] = float(np.max(np.abs(d["Kth"][idx])))
            row["max_abs_theta"] = float(np.max(arrays["abs_theta"][idx]))
            row["max_abs_B_rate"] = float(np.max(np.abs(B_rate[idx])))
            row["max_abs_R_rate"] = float(np.max(np.abs(R_rate[idx])))
            row["max_abs_N_rate"] = float(np.max(np.abs(N_rate[idx])))
            row["max_abs_dlogB_dl"] = float(np.max(np.abs(dlogB_dl[idx])))
            row["max_abs_dlogN_dl"] = float(np.max(np.abs(dlogN_dl[idx])))
            row["max_abs_R_l"] = float(np.max(np.abs(R_l[idx])))
            row["max_abs_R_ll"] = float(np.max(np.abs(R_ll[idx])))
            row["max_abs_R_t"] = float(np.max(np.abs(Rt[idx])))
            row["max_abs_R_tt"] = float(np.max(np.abs(R_tt[idx])))
            rows.append(row)
    extrema = pd.DataFrame(rows)
    extrema.to_csv(OUT / "invariant_v03_phase_zone_extrema.csv", index=False)

    # Observer-family source-history ledgers.
    ledger_rows = []
    observers = {
        "core_line": np.abs(l) == np.min(np.abs(l)),
        "access_mean": zones["access"],
        "support_mean": zones["support"],
        "shoulder_mean": zones["shoulder"],
        "inner_shoulder_mean": zones["inner_shoulder"],
        "outer_shoulder_mean": zones["outer_shoulder"],
        "matching_mean": zones["matching"],
    }
    for obs, zm in observers.items():
        if obs == "core_line":
            y = Tkk_total[:, np.argmin(np.abs(l))]
            y_geo = d["Tkk_min"][:, np.argmin(np.abs(l))]
            y_src = src[:, np.argmin(np.abs(l))]
        else:
            y = np.mean(Tkk_total[:, zm], axis=1)
            y_geo = np.mean(d["Tkk_min"][:, zm], axis=1)
            y_src = np.mean(src[:, zm], axis=1)
        row = {"observer_family": obs}
        for ph, tm in pmasks.items():
            row[f"{ph}_neg_total"] = float(np.trapezoid(np.maximum(-y[tm], 0), t[tm])) if np.any(tm) else 0.0
            row[f"{ph}_pos_total"] = float(np.trapezoid(np.maximum(y[tm], 0), t[tm])) if np.any(tm) else 0.0
            row[f"{ph}_neg_geo"] = float(np.trapezoid(np.maximum(-y_geo[tm], 0), t[tm])) if np.any(tm) else 0.0
            row[f"{ph}_pos_src"] = float(np.trapezoid(np.maximum(y_src[tm], 0), t[tm])) if np.any(tm) else 0.0
        row["comp_to_open_ratio_total"] = row["comp_pos_total"] / (row["open_interval_neg_total"] + 1e-15)
        row["comp_src_to_open_ratio"] = row["comp_pos_src"] / (row["open_interval_neg_total"] + 1e-15)
        ledger_rows.append(row)
    ledgers = pd.DataFrame(ledger_rows)
    ledgers.to_csv(OUT / "invariant_v03_observer_ledgers.csv", index=False)

    # Lifecycle time series digest at each time.
    digest = pd.DataFrame({"t": t, "phase": phase})
    i0 = np.argmin(np.abs(l))
    for name, zm in {
        "access": zones["access"],
        "support": zones["support"],
        "shoulder": zones["shoulder"],
        "matching": zones["matching"],
    }.items():
        digest[f"{name}_mean_Tkk_total"] = np.mean(Tkk_total[:, zm], axis=1)
        digest[f"{name}_max_abs_flux"] = np.max(np.abs(d["flux"][:, zm]), axis=1)
        digest[f"{name}_max_abs_Kll"] = np.max(np.abs(d["Kll"][:, zm]), axis=1)
        digest[f"{name}_max_abs_Kth"] = np.max(np.abs(d["Kth"][:, zm]), axis=1)
        digest[f"{name}_max_abs_theta"] = np.max(arrays["abs_theta"][:, zm], axis=1)
        digest[f"{name}_min_N"] = np.min(N[:, zm], axis=1)
        digest[f"{name}_min_R"] = np.min(R[:, zm], axis=1)
    digest["coreline_Tkk_total"] = Tkk_total[:, i0]
    digest["coreline_Tkk_geo"] = d["Tkk_min"][:, i0]
    digest["coreline_src"] = src[:, i0]
    digest["proper_half_length_R2"] = [proper_half_length_to_R(l, B[i, :], R[i, :], 2.0) for i in range(len(t))]
    digest["proper_half_length_R3"] = [proper_half_length_to_R(l, B[i, :], R[i, :], 3.0) for i in range(len(t))]
    # Save full digest and a compact 401-row digest.
    digest.to_csv(OUT / "invariant_v03_lifecycle_timeseries.csv", index=False)
    sample_idx = np.unique(np.round(np.linspace(0, len(t)-1, 401)).astype(int))
    digest.iloc[sample_idx].to_csv(OUT / "invariant_v03_lifecycle_digest_401.csv", index=False)

    # Representative timeslice profiles.
    t1, t2, t3, t4, t5, t6 = times
    target_times = {
        "B_setup_mid": 0.5 * t1,
        "pre_R_open": t1,
        "R_open_mid": 0.5 * (t1 + t2),
        "hold_mid": 0.5 * (t2 + t3),
        "R_close_mid": 0.5 * (t3 + t4),
        "comp_peak": t4 + 0.5 * PARAMS["T_C"],
        "B_reset_mid": 0.5 * (t5 + t6),
    }
    prof_rows = []
    for label, tt in target_times.items():
        ii = int(np.argmin(np.abs(t - tt)))
        for j, lj in enumerate(l):
            prof_rows.append({
                "slice": label,
                "t": float(t[ii]),
                "l": float(lj),
                "N": float(N[ii, j]),
                "B": float(B[ii, j]),
                "R": float(R[ii, j]),
                "Tkk_geo_min": float(d["Tkk_min"][ii, j]),
                "Tkk_total_min": float(Tkk_total[ii, j]),
                "src_Tkk_overlay": float(src[ii, j]),
                "flux_geo": float(d["flux"][ii, j]),
                "Kll": float(d["Kll"][ii, j]),
                "Kth": float(d["Kth"][ii, j]),
                "theta_plus": float(d["theta_plus"][ii, j]),
                "theta_minus": float(d["theta_minus"][ii, j]),
                "R_l": float(R_l[ii, j]),
                "R_ll": float(R_ll[ii, j]),
                "dlogB_dl": float(dlogB_dl[ii, j]),
                "dlogN_dl": float(dlogN_dl[ii, j]),
            })
    profiles = pd.DataFrame(prof_rows)
    profiles.to_csv(OUT / "invariant_v03_timeslice_profiles.csv", index=False)

    # Extracts for report progress.
    def ez(phase_name: str, zone_name: str, col: str) -> float:
        return float(extrema[(extrema.phase == phase_name) & (extrema.zone == zone_name)][col].iloc[0])

    core_ledger = ledgers[ledgers.observer_family == "core_line"].iloc[0]
    support_ledger = ledgers[ledgers.observer_family == "support_mean"].iloc[0]
    shoulder_ledger = ledgers[ledgers.observer_family == "shoulder_mean"].iloc[0]
    access_comp = extrema[(extrema.phase == "comp") & (extrema.zone == "access")].iloc[0]
    open_access = extrema[(extrema.phase == "open_interval") & (extrema.zone == "access")].iloc[0]
    comp_shoulder = extrema[(extrema.phase == "comp") & (extrema.zone == "shoulder")].iloc[0]

    extracts = {
        "reference": PARAMS,
        "phase_times": {
            "B_setup_end": t1,
            "R_open_end": t2,
            "hold_end": t3,
            "R_close_end": t4,
            "comp_end": t5,
            "B_reset_end": t6,
        },
        "source_history_ledgers": {
            "coreline_open_neg": float(core_ledger["open_interval_neg_total"]),
            "coreline_comp_pos": float(core_ledger["comp_pos_total"]),
            "coreline_comp_to_open_ratio": float(core_ledger["comp_to_open_ratio_total"]),
            "support_open_neg": float(support_ledger["open_interval_neg_total"]),
            "support_comp_pos": float(support_ledger["comp_pos_total"]),
            "support_comp_to_open_ratio": float(support_ledger["comp_to_open_ratio_total"]),
            "shoulder_open_neg": float(shoulder_ledger["open_interval_neg_total"]),
            "shoulder_comp_pos": float(shoulder_ledger["comp_pos_total"]),
            "shoulder_comp_to_open_ratio": float(shoulder_ledger["comp_to_open_ratio_total"]),
        },
        "access_open_bounds": {
            "max_abs_flux": float(open_access["max_abs_flux_geo"]),
            "max_abs_Kll": float(open_access["max_abs_Kll"]),
            "max_abs_Kth": float(open_access["max_abs_Kth"]),
            "max_abs_theta": float(open_access["max_abs_theta"]),
            "min_N": float(open_access["min_N"]),
            "min_R": float(open_access["min_R"]),
        },
        "access_compensation_isolation": {
            "max_abs_flux": float(access_comp["max_abs_flux_geo"]),
            "max_abs_Kll": float(access_comp["max_abs_Kll"]),
            "max_abs_Kth": float(access_comp["max_abs_Kth"]),
            "max_abs_theta": float(access_comp["max_abs_theta"]),
            "min_N": float(access_comp["min_N"]),
            "min_R": float(access_comp["min_R"]),
        },
        "shoulder_compensation_bounds": {
            "max_abs_flux": float(comp_shoulder["max_abs_flux_geo"]),
            "max_abs_Kll": float(comp_shoulder["max_abs_Kll"]),
            "max_abs_Kth": float(comp_shoulder["max_abs_Kth"]),
            "max_abs_theta": float(comp_shoulder["max_abs_theta"]),
            "min_N": float(comp_shoulder["min_N"]),
            "min_R": float(comp_shoulder["min_R"]),
            "max_abs_dlogN_dl": float(comp_shoulder["max_abs_dlogN_dl"]),
            "max_abs_R_ll": float(comp_shoulder["max_abs_R_ll"]),
        },
        "proper_lengths": {
            "hold_mid_half_length_R2": float(digest.iloc[np.argmin(np.abs(t - target_times["hold_mid"]))]["proper_half_length_R2"]),
            "hold_mid_half_length_R3": float(digest.iloc[np.argmin(np.abs(t - target_times["hold_mid"]))]["proper_half_length_R3"]),
            "standby_preopen_half_length_R2": float(digest.iloc[np.argmin(np.abs(t - target_times["pre_R_open"]))]["proper_half_length_R2"]),
        },
        "geometry_global_bounds": {
            "N_min_full": float(np.min(N)),
            "R_min_full": float(np.min(R)),
            "B_max_full": float(np.max(B)),
            "max_abs_dlogB_dl_full": float(np.max(np.abs(dlogB_dl))),
            "max_abs_dlogN_dl_full": float(np.max(np.abs(dlogN_dl))),
            "max_abs_R_ll_full": float(np.max(np.abs(R_ll))),
            "max_abs_R_tt_full": float(np.max(np.abs(R_tt))),
        },
        "design_reading": [
            "Reference Geometry v0.3 has a bounded lapse, bounded areal radius, and stable support-dilution length scale in this reduced packet.",
            "Compensation remains isolated from the access observer family after flare closure.",
            "The largest dynamic access quantities occur during the deliberate R flare-open/close interval and remain within the current geometry bounds.",
            "Shoulder lapse shaping is the active matching/compensation geometry during the repayment phase; it stays outside the access core.",
        ],
    }
    (OUT / "invariant_v03_extracts.json").write_text(json.dumps(extracts, indent=2))

    # Progress notes.
    notes = OUT.parent / "report_progress_notes.md"
    with notes.open("a", encoding="utf-8") as f:
        f.write("\n\n## Geometry polish progress: invariant/gauge diagnostic packet for v0.3\n\n")
        f.write("Reference Geometry v0.3 was evaluated with a phase-zone invariant/proxy packet. ")
        f.write("The packet records N, B, R, proper radial length, null expansions, extrinsic-rate proxies, geometry-only Tkk, total Tkk with explicit compensation, flux, and transition derivatives.\n\n")
        f.write("The positive geometry reading is that the lifecycle remains well separated by observer family: ")
        f.write("open-interval dynamics occur during R flare gating, access compensation isolation is strong after R closure, and support/shoulder compensation ratios stay above unity. ")
        f.write("Lapse and radius bounds remain healthy in the reduced screen.\n\n")
        f.write(f"Core/support/shoulder compensation ratios: {extracts['source_history_ledgers']['coreline_comp_to_open_ratio']:.3f}, ")
        f.write(f"{extracts['source_history_ledgers']['support_comp_to_open_ratio']:.3f}, {extracts['source_history_ledgers']['shoulder_comp_to_open_ratio']:.3f}. ")
        f.write(f"Access compensation max flux/Kll/Kth/theta: {extracts['access_compensation_isolation']['max_abs_flux']:.3e}, ")
        f.write(f"{extracts['access_compensation_isolation']['max_abs_Kll']:.3e}, {extracts['access_compensation_isolation']['max_abs_Kth']:.3e}, ")
        f.write(f"{extracts['access_compensation_isolation']['max_abs_theta']:.3e}.\n")

    # Console report.
    print("Reference Geometry v0.3 invariant packet complete")
    print("Source-history ratios:")
    print(json.dumps(extracts["source_history_ledgers"], indent=2))
    print("\nAccess open bounds:")
    print(json.dumps(extracts["access_open_bounds"], indent=2))
    print("\nAccess compensation isolation:")
    print(json.dumps(extracts["access_compensation_isolation"], indent=2))
    print("\nShoulder compensation bounds:")
    print(json.dumps(extracts["shoulder_compensation_bounds"], indent=2))

if __name__ == "__main__":
    main()
