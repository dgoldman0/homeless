#!/usr/bin/env python3
"""
Dynamic throat gate prototype for wormhole-support infrastructure screening.

Scope:
  Wormhole component only.  No transport/catch/passenger layer.

Metric family:
  ds^2 = -N(l,t)^2 dt^2 + B(l,t)^2 dl^2 + R(l,t)^2 dOmega^2

This script evaluates a small set of static and dynamic throat-control cases
through a reusable dynamic screening gate:
  - null expansions theta_+, theta_-
  - throat location and expansion split
  - orthonormal energy density and radial/null stress proxies
  - flux G_tl / (8 pi N B)
  - extrinsic-curvature/rate proxies K^l_l, K^theta_theta
  - access quietness and shoulder activity

The diagnostics are reduced prescribed-geometry probes.  They are engineering
screening quantities, not semiclassical source models.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

PI = math.pi


def smooth_window(l: np.ndarray, width: float = 1.6, power: float = 4.0) -> np.ndarray:
    return np.exp(-((np.abs(l) / width) ** power))


def shoulder_window(l: np.ndarray, center: float = 1.6, width: float = 0.35, power: float = 4.0) -> np.ndarray:
    return np.exp(-(((np.abs(l) - center) / width) ** power))


def tanh_ramp(t: np.ndarray, t0: float = 0.0, tau: float = 1.0) -> np.ndarray:
    return 0.5 * (1.0 + np.tanh((t - t0) / tau))


def case_fields(case: str, t: np.ndarray, l: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """Return N(t,l), B(t,l), R(t,l), metadata for a named test case."""
    T, L = np.meshgrid(t, l, indexing="ij")
    R0 = np.sqrt(1.0 + L**2)
    F_core = smooth_window(l, width=1.6, power=4.0)[None, :]
    F_shoulder = shoulder_window(l, center=1.6, width=0.38, power=4.0)[None, :]
    F_access = smooth_window(l, width=0.35, power=6.0)[None, :]

    N = np.ones_like(T)
    B = np.ones_like(T)
    R = R0.copy()
    meta = {"case": case}

    if case == "static_baseline":
        pass

    elif case == "static_B3_long_throat":
        B = 1.0 + 2.0 * F_core

    elif case == "adiabatic_B_ramp_up":
        # B0 moves from 1 to 3 slowly over the interval.
        A = tanh_ramp(t, t0=0.0, tau=1.5)[:, None]
        B = 1.0 + 2.0 * A * F_core
        meta.update({"B0_initial": 1.0, "B0_final": 3.0, "ramp_tau": 1.5})

    elif case == "adiabatic_B_ramp_down":
        A = 1.0 - tanh_ramp(t, t0=0.0, tau=1.5)[:, None]
        B = 1.0 + 2.0 * A * F_core
        meta.update({"B0_initial": 3.0, "B0_final": 1.0, "ramp_tau": 1.5})

    elif case == "slow_B_breathing":
        # Slow B-only cycle, with R held quiet.
        omega = 0.75
        A = 0.5 * (1.0 + np.sin(omega * T))
        B = 1.0 + 2.0 * A * F_core
        meta.update({"omega": omega, "B0_range": [1.0, 3.0]})

    elif case == "fast_B_breathing":
        omega = 9.0
        A = 0.5 * (1.0 + np.sin(omega * T))
        B = 1.0 + 2.0 * A * F_core
        meta.update({"omega": omega, "B0_range": [1.0, 3.0]})

    elif case == "sharp_fast_B_wall":
        omega = 9.0
        F_sharp = smooth_window(l, width=0.75, power=8.0)[None, :]
        A = 0.5 * (1.0 + np.sin(omega * T))
        B = 1.0 + 5.0 * A * F_sharp
        meta.update({"omega": omega, "B0_range": [1.0, 6.0], "profile": "sharp"})

    elif case == "core_R_breathing_compare":
        omega = 9.0
        R = R0 + 0.08 * np.sin(omega * T) * F_access
        meta.update({"omega": omega, "R_access_amplitude": 0.08})

    elif case == "global_scale_factor_compare":
        omega = 1.2
        a = 1.0 + 0.12 * np.sin(omega * T)
        B = a
        R = a * R0
        meta.update({"omega": omega, "scale_factor_amplitude": 0.12})

    elif case == "side_R_repayment_with_static_B3":
        omega = 8.0
        B = 1.0 + 2.0 * F_core
        # R motion deliberately in shoulders/repayment bands, not access core.
        R = R0 + 0.08 * np.sin(omega * T) * F_shoulder
        meta.update({"omega": omega, "R_shoulder_amplitude": 0.08, "B0": 3.0})

    elif case == "adiabatic_B_plus_side_R":
        A = tanh_ramp(t, t0=0.0, tau=1.5)[:, None]
        B = 1.0 + 2.0 * A * F_core
        R = R0 + 0.04 * np.sin(1.0 * T) * F_shoulder
        meta.update({"B0_initial": 1.0, "B0_final": 3.0, "side_R_amplitude": 0.04})

    else:
        raise ValueError(case)

    # Broadcast static/separable fields to the full (t,l) grid.
    N = np.broadcast_to(N, T.shape).astype(float).copy()
    B = np.broadcast_to(B, T.shape).astype(float).copy()
    R = np.broadcast_to(R, T.shape).astype(float).copy()
    B = np.maximum(B, 0.05)
    N = np.maximum(N, 0.05)
    R = np.maximum(R, 0.05)
    return N, B, R, meta


def gradients_2d(f: np.ndarray, t: np.ndarray, l: np.ndarray) -> dict[str, np.ndarray]:
    ft = np.gradient(f, t, axis=0, edge_order=2)
    fl = np.gradient(f, l, axis=1, edge_order=2)
    ftt = np.gradient(ft, t, axis=0, edge_order=2)
    fll = np.gradient(fl, l, axis=1, edge_order=2)
    ftl = np.gradient(ft, l, axis=1, edge_order=2)
    return {"t": ft, "l": fl, "tt": ftt, "ll": fll, "tl": ftl}


def geometry_diagnostics(t: np.ndarray, l: np.ndarray, N: np.ndarray, B: np.ndarray, R: np.ndarray) -> dict[str, np.ndarray]:
    """Reduced exact diagnostics for the 2+2 warped product metric."""
    gN = gradients_2d(N, t, l)
    gB = gradients_2d(B, t, l)
    gR = gradients_2d(R, t, l)

    Nt, Nl = gN["t"], gN["l"]
    Bt, Bl = gB["t"], gB["l"]
    Rt, Rl, Rtt, Rll, Rtl = gR["t"], gR["l"], gR["tt"], gR["ll"], gR["tl"]

    # Base Christoffel terms for h_ab=diag(-N^2,+B^2).
    Dtt = Rtt - (Nt / N) * Rt - (N * Nl / (B**2)) * Rl
    Dtl = Rtl - (Nl / N) * Rt - (Bt / B) * Rl
    Dll = Rll - (B * Bt / (N**2)) * Rt - (Bl / B) * Rl

    boxR = -(Dtt / N**2) + (Dll / B**2)
    gradR2 = -(Rt**2 / N**2) + (Rl**2 / B**2)

    # Warped-product Einstein tensor base components.
    Gtt = -2.0 * Dtt / R + 2.0 * (-N**2) * boxR / R + (N**2) * (1.0 - gradR2) / (R**2)
    Gll = -2.0 * Dll / R + 2.0 * (B**2) * boxR / R - (B**2) * (1.0 - gradR2) / (R**2)
    Gtl = -2.0 * Dtl / R

    rho_hat = Gtt / (8.0 * PI * N**2)
    p_rad_hat = Gll / (8.0 * PI * B**2)
    flux_hat = Gtl / (8.0 * PI * N * B)

    # Future-directed radial null vectors in coordinate components: k_±=(1/N, ±1/B).
    Gkk_plus_hat = (Gtt / N**2 + Gll / B**2 + 2.0 * Gtl / (N * B)) / (8.0 * PI)
    Gkk_minus_hat = (Gtt / N**2 + Gll / B**2 - 2.0 * Gtl / (N * B)) / (8.0 * PI)

    theta_plus = 2.0 * (Rt / N + Rl / B) / R
    theta_minus = 2.0 * (Rt / N - Rl / B) / R
    theta_product = theta_plus * theta_minus

    # Zero-shift extrinsic curvature mixed components; sign convention irrelevant for magnitudes.
    K_l = -Bt / (N * B)
    K_ang = -Rt / (N * R)
    K_trace = K_l + 2.0 * K_ang

    # Angular tidal proxy from areal-radius acceleration.
    tidal_ang = -Dtt / (N**2 * R)

    return {
        "N": N, "B": B, "R": R,
        "rho": rho_hat, "p_radial": p_rad_hat, "Tkk_plus": Gkk_plus_hat, "Tkk_minus": Gkk_minus_hat,
        "Tkk_min": np.minimum(Gkk_plus_hat, Gkk_minus_hat),
        "flux": flux_hat,
        "theta_plus": theta_plus, "theta_minus": theta_minus, "theta_product": theta_product,
        "K_l": K_l, "K_ang": K_ang, "K_trace": K_trace,
        "tidal_ang": tidal_ang,
        "Rt_over_R": Rt / R, "Bt_over_B": Bt / B,
        "Rl": Rl, "Rt": Rt,
    }


def summarize_case(case: str, t: np.ndarray, l: np.ndarray, d: dict[str, np.ndarray]) -> dict:
    zones = {
        "throat": (0.0, 0.04),
        "access_core": (0.0, 0.25),
        "support_core": (0.0, 0.65),
        "shoulder": (1.1, 2.1),
        "outer": (2.4, 3.6),
    }
    row: dict[str, float | str] = {"case": case}
    abs_l = np.abs(l)

    for z, (lo, hi) in zones.items():
        mask = (abs_l >= lo) & (abs_l <= hi)
        for key in ["rho", "Tkk_min", "flux", "theta_plus", "theta_minus", "theta_product", "K_l", "K_ang", "tidal_ang", "Bt_over_B", "Rt_over_R"]:
            arr = d[key][:, mask]
            row[f"{z}_{key}_min"] = float(np.min(arr))
            row[f"{z}_{key}_max"] = float(np.max(arr))
            row[f"{z}_{key}_max_abs"] = float(np.max(np.abs(arr)))

    # Throat index by minimum R at each t; in symmetric cases this is near l=0.
    throat_idxs = np.argmin(d["R"], axis=1)
    throat_l = l[throat_idxs]
    idx_t = np.arange(len(t))
    theta_p_throat = d["theta_plus"][idx_t, throat_idxs]
    theta_m_throat = d["theta_minus"][idx_t, throat_idxs]
    Tkk_throat = d["Tkk_min"][idx_t, throat_idxs]
    flux_throat = d["flux"][idx_t, throat_idxs]
    K_l_throat = d["K_l"][idx_t, throat_idxs]
    K_ang_throat = d["K_ang"][idx_t, throat_idxs]
    R_throat = d["R"][idx_t, throat_idxs]

    row["throat_l_max_abs"] = float(np.max(np.abs(throat_l)))
    row["throat_theta_plus_max_abs"] = float(np.max(np.abs(theta_p_throat)))
    row["throat_theta_minus_max_abs"] = float(np.max(np.abs(theta_m_throat)))
    row["throat_expansion_split_max_abs"] = float(np.max(np.abs(theta_p_throat - theta_m_throat)))
    row["throat_Tkk_min"] = float(np.min(Tkk_throat))
    row["throat_flux_max_abs"] = float(np.max(np.abs(flux_throat)))
    row["throat_K_l_max_abs"] = float(np.max(np.abs(K_l_throat)))
    row["throat_K_ang_max_abs"] = float(np.max(np.abs(K_ang_throat)))
    row["throat_R_min"] = float(np.min(R_throat))
    row["throat_R_max"] = float(np.max(R_throat))

    access_mask = abs_l <= 0.25
    shoulder_mask = (abs_l >= 1.1) & (abs_l <= 2.1)

    # Engineering quietness thresholds for a reduced gate prototype.
    access_quiet = (
        (np.max(np.abs(d["theta_plus"][:, access_mask]), axis=1) < 0.75)
        & (np.max(np.abs(d["theta_minus"][:, access_mask]), axis=1) < 0.75)
        & (np.max(np.abs(d["flux"][:, access_mask]), axis=1) < 0.05)
        & (np.max(np.abs(d["K_l"][:, access_mask]), axis=1) < 0.25)
        & (np.max(np.abs(d["K_ang"][:, access_mask]), axis=1) < 0.15)
        & (np.max(np.abs(d["tidal_ang"][:, access_mask]), axis=1) < 1.0)
    )
    row["access_quiet_fraction"] = float(np.mean(access_quiet))

    shoulder_activity = (
        np.max(np.abs(d["flux"][:, shoulder_mask]), axis=1)
        + np.max(np.abs(d["K_l"][:, shoulder_mask]), axis=1)
        + np.max(np.abs(d["tidal_ang"][:, shoulder_mask]), axis=1)
    )
    row["shoulder_activity_max"] = float(np.max(shoulder_activity))
    row["shoulder_activity_mean"] = float(np.mean(shoulder_activity))

    # Proper half-length from l=0 to |l|=sqrt(3), roughly the coordinate radius where static R0 reaches 2.
    pos = l >= 0
    lpos = l[pos]
    idx_end = np.argmin(np.abs(lpos - math.sqrt(3.0)))
    Bpos = d["B"][:, pos]
    half_lengths = np.trapezoid(Bpos[:, :idx_end+1], lpos[:idx_end+1], axis=1)
    row["proper_half_length_R0_to_2_min"] = float(np.min(half_lengths))
    row["proper_half_length_R0_to_2_max"] = float(np.max(half_lengths))
    row["proper_half_length_R0_to_2_mean"] = float(np.mean(half_lengths))

    # Gate classification.
    if row["throat_theta_plus_max_abs"] > 0.5 or row["throat_theta_minus_max_abs"] > 0.5:
        classification = "dynamic-throat-expansion-failure"
    elif row["access_quiet_fraction"] < 0.5:
        classification = "access-quietness-failure"
    elif row["shoulder_activity_max"] > 3.0:
        classification = "transition-shoulder-limited"
    elif row["access_core_flux_max_abs"] > 0.05 or row["access_core_K_l_max_abs"] > 0.25:
        classification = "flux-or-extrinsic-curvature-limited"
    elif row["proper_half_length_R0_to_2_max"] > 8.0:
        classification = "adiabatic-long-throat-cost"
    else:
        classification = "dynamic-gate-pass-prototype"

    row["dynamic_gate_classification"] = classification
    return row


def main(outdir: str = ".") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    t = np.linspace(-4.0, 4.0, 1601)
    l = np.linspace(-4.0, 4.0, 801)

    cases = [
        "static_baseline",
        "static_B3_long_throat",
        "adiabatic_B_ramp_up",
        "adiabatic_B_ramp_down",
        "slow_B_breathing",
        "fast_B_breathing",
        "sharp_fast_B_wall",
        "core_R_breathing_compare",
        "global_scale_factor_compare",
        "side_R_repayment_with_static_B3",
        "adiabatic_B_plus_side_R",
    ]

    rows = []
    digest_rows = []
    metadata = {}
    for case in cases:
        N, B, R, meta = case_fields(case, t, l)
        d = geometry_diagnostics(t, l, N, B, R)
        rows.append(summarize_case(case, t, l, d))
        metadata[case] = meta

        # Compact digest at throat, access edge, shoulder representative.
        rep_locs = [0.0, 0.25, 1.6]
        rep_idxs = [int(np.argmin(np.abs(l - x))) for x in rep_locs]
        sample_ts = np.unique(np.round(np.linspace(0, len(t)-1, 161)).astype(int))
        for ti in sample_ts:
            for loc, li in zip(rep_locs, rep_idxs):
                digest_rows.append({
                    "case": case,
                    "t": float(t[ti]),
                    "l": float(l[li]),
                    "N": float(N[ti, li]),
                    "B": float(B[ti, li]),
                    "R": float(R[ti, li]),
                    "rho": float(d["rho"][ti, li]),
                    "Tkk_min": float(d["Tkk_min"][ti, li]),
                    "flux": float(d["flux"][ti, li]),
                    "theta_plus": float(d["theta_plus"][ti, li]),
                    "theta_minus": float(d["theta_minus"][ti, li]),
                    "K_l": float(d["K_l"][ti, li]),
                    "K_ang": float(d["K_ang"][ti, li]),
                    "tidal_ang": float(d["tidal_ang"][ti, li]),
                })

    case_df = pd.DataFrame(rows)
    case_df.to_csv(out / "dynamic_gate_case_summary.csv", index=False)
    pd.DataFrame(digest_rows).to_csv(out / "dynamic_gate_time_digest.csv", index=False)

    # Readable extract table.
    extract_cols = [
        "case",
        "dynamic_gate_classification",
        "access_quiet_fraction",
        "throat_theta_plus_max_abs",
        "throat_theta_minus_max_abs",
        "access_core_flux_max_abs",
        "access_core_K_l_max_abs",
        "access_core_K_ang_max_abs",
        "access_core_tidal_ang_max_abs",
        "shoulder_activity_max",
        "throat_Tkk_min",
        "proper_half_length_R0_to_2_min",
        "proper_half_length_R0_to_2_max",
    ]
    case_df[extract_cols].to_csv(out / "dynamic_gate_extract_table.csv", index=False)

    summary = {
        "scope": "dynamic throat gate prototype for wormhole-support infrastructure screening",
        "metric_family": "ds^2=-N(l,t)^2 dt^2 + B(l,t)^2 dl^2 + R(l,t)^2 dOmega^2",
        "cases": metadata,
        "diagnostic_notes": {
            "null_expansions": "theta_± = 2(R_t/N ± R_l/B)/R",
            "null_stress": "orthonormal radial null contraction from Einstein proxy, Tkk = (G_tt/N^2 + G_ll/B^2 ± 2G_tl/(NB))/(8pi)",
            "extrinsic_rates": "zero-shift mixed K proxies: K_l=-B_t/(NB), K_ang=-R_t/(NR)",
            "classification": "reduced engineering gate prototype, not a physical source proof"
        },
        "high_level_result": (
            "Adiabatic or slow B-only variation behaves closest to a sequence of static long-throat states, "
            "while fast or sharp B variation becomes flux/extrinsic-curvature/shoulder limited. "
            "Access-core R modulation directly activates expansion/tidal/access quietness failures. "
            "The dynamic gate therefore supports treating B(l) stretch as quasi-static infrastructure and "
            "using time dependence cautiously, mainly outside the access core."
        )
    }
    (out / "dynamic_gate_summary.json").write_text(json.dumps(summary, indent=2))

    # Manifest with checksums.
    files = [
        "run_dynamic_throat_gate_eval.py",
        "dynamic_gate_case_summary.csv",
        "dynamic_gate_extract_table.csv",
        "dynamic_gate_time_digest.csv",
        "dynamic_gate_summary.json",
        "dynamic_gate_memo.md",
        "README.md",
    ]
    checksums = {}
    for name in files:
        fp = out / name
        if fp.exists():
            checksums[name] = hashlib.sha256(fp.read_bytes()).hexdigest()
    manifest = {"bundle": "dynamic_throat_gate", "files": files, "sha256": checksums}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
