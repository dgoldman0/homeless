#!/usr/bin/env python3
"""
Lapse + radial-metric freedom throat plant: reduced QEE evaluation.

Wormhole-component-only continuation of the multi-zone phase-cycled throat eval.
It tests whether adding lapse N(l,t) and radial metric B(l,t) to

    ds^2 = -N(l,t)^2 dt^2 + B(l,t)^2 dl^2 + R(l,t)^2 dOmega^2

creates a useful middle regime that was absent in the R(l,t)-only model.

This is a reduced diagnostic, not a semiclassical proof or NR evolution.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

LP_M = 1.616255e-35
C_QI = 3.0 / (32.0 * math.pi**2)


def prof_core(l: np.ndarray, w: float = 0.55, power: int = 6) -> np.ndarray:
    return np.exp(-(np.abs(l) / w) ** power)


def prof_access(l: np.ndarray) -> np.ndarray:
    return np.exp(-(np.abs(l) / 0.25) ** 8)


def prof_ring(l: np.ndarray, center: float, width: float, power: int = 4) -> np.ndarray:
    return np.exp(-((np.abs(l) - center) / width) ** power)


def make_fields(case: str, t: np.ndarray, l: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    T, L = np.meshgrid(t, l, indexing="ij")
    Rbase = np.sqrt(1.0 + L**2)
    pc = prof_core(l)[None, :]
    pa = prof_access(l)[None, :]
    pr = prof_ring(l, 0.90, 0.25)[None, :]
    pb = prof_ring(l, 1.55, 0.35)[None, :]

    N = np.ones_like(Rbase)
    B = np.ones_like(Rbase)
    R = Rbase.copy()

    if case == "static_reference":
        pass

    elif case.startswith("static_Bcore_"):
        B0 = float(case.split("_")[-1].replace("p", "."))
        B = np.exp(np.log(B0) * pc)

    elif case == "static_lapse_core_N2":
        N = np.exp(np.log(2.0) * pc)

    elif case == "static_lapse_side_N2":
        N = np.exp(np.log(2.0) * pr)

    elif case == "side_lapse_cycle_static_core":
        N = np.exp(0.25 * np.sin(14.0 * T) * pr + 0.10 * np.sin(14.0 * T + math.pi / 2) * pb)

    elif case == "Bcore2_side_lapse_cycle":
        B = np.exp(np.log(2.0) * pc)
        N = np.exp(0.25 * np.sin(14.0 * T) * pr + 0.10 * np.sin(14.0 * T + math.pi / 2) * pb)

    elif case == "Bcore2_Rtiny_fast":
        B = np.exp(np.log(2.0) * pc)
        R = Rbase + 0.025 * np.sin(60.0 * T) * pa + 0.08 * np.sin(60.0 * T + math.pi) * pr

    elif case == "Bcore2_Rmild_split":
        B = np.exp(np.log(2.0) * pc)
        R = Rbase + 0.040 * np.sin(12.0 * T) * pa + 0.09 * np.sin(12.0 * T + math.pi) * pr + 0.03 * np.sin(12.0 * T + math.pi/2) * pb

    elif case == "Bcycle_core_static_R":
        # Dynamic radial metric while areal radius remains quiet; tests whether B motion carries the plant.
        B = np.exp((np.log(2.0) + 0.18 * np.sin(16.0 * T)) * pc + 0.08 * np.sin(16.0 * T + math.pi) * pr)

    elif case == "Bcycle_core_with_lapse_comp":
        B = np.exp((np.log(2.0) + 0.18 * np.sin(16.0 * T)) * pc + 0.08 * np.sin(16.0 * T + math.pi) * pr)
        N = np.exp(0.18 * np.sin(16.0 * T + math.pi / 2) * pc)

    elif case == "redshift_B_trade_N3_B2":
        B = np.exp(np.log(2.0) * pc)
        N = np.exp(np.log(3.0) * pc)

    elif case == "radial_tube_B5":
        B = np.exp(np.log(5.0) * pc)

    elif case == "radial_tube_B10":
        B = np.exp(np.log(10.0) * pc)

    else:
        raise ValueError(case)

    N = np.broadcast_to(N, Rbase.shape).copy()
    B = np.broadcast_to(B, Rbase.shape).copy()
    R = np.broadcast_to(R, Rbase.shape).copy()
    return np.maximum(N, 1e-6), np.maximum(B, 1e-6), np.maximum(R, 0.05)


def gradient_x(A: np.ndarray, x: np.ndarray, axis: int) -> np.ndarray:
    return np.gradient(A, x, axis=axis, edge_order=2)


def diagnostics(t: np.ndarray, l: np.ndarray, N: np.ndarray, B: np.ndarray, R: np.ndarray) -> Dict[str, np.ndarray]:
    # derivatives
    Nt = gradient_x(N, t, 0); Nl = gradient_x(N, l, 1)
    Bt = gradient_x(B, t, 0); Bl = gradient_x(B, l, 1)
    Rt = gradient_x(R, t, 0); Rl = gradient_x(R, l, 1)
    Rtt = gradient_x(Rt, t, 0); Rll = gradient_x(Rl, l, 1); Rtl = gradient_x(Rt, l, 1)

    # 2D base Christoffels for h_ab=diag(-N^2,B^2)
    Gt_tt = Nt / N
    Gt_tl = Nl / N
    Gt_ll = B * Bt / (N**2)
    Gl_tt = N * Nl / (B**2)
    Gl_tl = Bt / B
    Gl_ll = Bl / B

    nab_tt_R = Rtt - Gt_tt * Rt - Gl_tt * Rl
    nab_tl_R = Rtl - Gt_tl * Rt - Gl_tl * Rl
    nab_ll_R = Rll - Gt_ll * Rt - Gl_ll * Rl

    hTT = -1.0 / (N**2)
    hLL = 1.0 / (B**2)
    boxR = hTT * nab_tt_R + hLL * nab_ll_R
    gradR2 = hTT * Rt**2 + hLL * Rl**2

    htt = -N**2
    hll = B**2

    Gtt = -2.0 * nab_tt_R / R + 2.0 * htt * boxR / R - htt * (1.0 - gradR2) / (R**2)
    Gll = -2.0 * nab_ll_R / R + 2.0 * hll * boxR / R - hll * (1.0 - gradR2) / (R**2)
    Gtl = -2.0 * nab_tl_R / R

    rho = Gtt / (8.0 * math.pi * N**2)
    p_radial = Gll / (8.0 * math.pi * B**2)
    flux = Gtl / (8.0 * math.pi * N * B)
    Gkk_plus = Gtt / N**2 + Gll / B**2 + 2.0 * Gtl / (N * B)
    Gkk_minus = Gtt / N**2 + Gll / B**2 - 2.0 * Gtl / (N * B)
    Gkk_min = np.minimum(Gkk_plus, Gkk_minus)

    # Local geometry/risk proxies
    logN_t = Nt / N
    logN_l = Nl / N
    logB_t = Bt / B
    logB_l = Bl / B
    radial_accel_proxy = np.abs(logN_l) / B
    time_metric_rate_proxy = np.sqrt(logN_t**2 + logB_t**2)
    tidal_ang = -nab_tt_R / (N**2 * R)  # rough orthonormal angular component from time curvature of R
    theta_product = 4.0 * gradR2 / (R**2)

    return {
        "N": N, "B": B, "R": R,
        "rho": rho, "p_radial": p_radial, "rho_plus_p_radial": rho + p_radial,
        "flux": flux, "Gkk_min": Gkk_min, "Gkk_plus": Gkk_plus, "Gkk_minus": Gkk_minus,
        "tidal_ang": tidal_ang, "theta_product": theta_product,
        "logN_t": logN_t, "logN_l": logN_l, "logB_t": logB_t, "logB_l": logB_l,
        "radial_accel_proxy": radial_accel_proxy,
        "time_metric_rate_proxy": time_metric_rate_proxy,
    }


def qi_samples(t: np.ndarray, l: np.ndarray, quantity: np.ndarray, zones: Dict[str, Tuple[float, float]]) -> Dict[str, dict]:
    tau0s = np.array([0.02, 0.05, 0.10, 0.20, 0.50, 1.00])
    centers = np.linspace(float(t[0] * 0.85), float(t[-1] * 0.85), 41)
    results: Dict[str, dict] = {}
    for zone, (lo, hi) in zones.items():
        idxs = np.where((np.abs(l) >= lo) & (np.abs(l) <= hi))[0]
        if len(idxs) > 11:
            idxs = np.unique(np.round(np.linspace(idxs[0], idxs[-1], 11)).astype(int))
        q = quantity[:, idxs]
        best = {
            "qi_min_sampled_avg": float("inf"),
            "qi_strict_L0max_planck_units": float("inf"),
            "qi_strict_log10_L0max": float("inf"),
            "qi_strict_tau0": None,
            "qi_strict_t0": None,
            "qi_strict_l": None,
            "qi_strict_avg": None,
        }
        for tau0 in tau0s:
            W = (tau0 / math.pi) / ((t[None, :] - centers[:, None]) ** 2 + tau0**2)
            W = W / (np.trapezoid(W, t, axis=1)[:, None])
            avgs = np.trapezoid(W[:, :, None] * q[None, :, :], t, axis=1)
            local_min = float(np.min(avgs))
            best["qi_min_sampled_avg"] = min(float(best["qi_min_sampled_avg"]), local_min)
            neg = avgs < 0
            if np.any(neg):
                Lvals = np.full_like(avgs, float("inf"), dtype=float)
                Lvals[neg] = np.sqrt(C_QI / (np.abs(avgs[neg]) * tau0**4))
                flat = int(np.nanargmin(Lvals))
                Lmin = float(Lvals.flat[flat])
                if Lmin < float(best["qi_strict_L0max_planck_units"]):
                    ci, li = np.unravel_index(flat, Lvals.shape)
                    best.update({
                        "qi_strict_L0max_planck_units": Lmin,
                        "qi_strict_log10_L0max": math.log10(Lmin),
                        "qi_strict_tau0": float(tau0),
                        "qi_strict_t0": float(centers[ci]),
                        "qi_strict_l": float(l[idxs[li]]),
                        "qi_strict_avg": float(avgs[ci, li]),
                    })
        results[zone] = best
    return results


def summarize(case: str, t: np.ndarray, l: np.ndarray, d: Dict[str, np.ndarray]) -> dict:
    zones = {
        "access_core": (0.00, 0.25),
        "support_inner": (0.00, 0.55),
        "repayment_band": (0.65, 1.15),
        "buffer_band": (1.25, 1.90),
    }
    row = {"case": case}
    for zone, (lo, hi) in zones.items():
        mask = (np.abs(l) >= lo) & (np.abs(l) <= hi)
        for name in ["rho", "p_radial", "rho_plus_p_radial", "Gkk_min", "flux", "tidal_ang", "theta_product", "radial_accel_proxy", "time_metric_rate_proxy"]:
            arr = d[name][:, mask]
            row[f"{zone}_{name}_min"] = float(np.min(arr))
            row[f"{zone}_{name}_max"] = float(np.max(arr))
            row[f"{zone}_{name}_mean"] = float(np.mean(arr))
            row[f"{zone}_{name}_max_abs"] = float(np.max(np.abs(arr)))
    for name in ["N", "B", "R"]:
        row[f"min_{name}"] = float(np.min(d[name])); row[f"max_{name}"] = float(np.max(d[name]))

    access_mask = np.abs(l) <= 0.25
    baseR = np.sqrt(1.0 + l**2)
    quiet = (
        (np.max(np.abs(d["tidal_ang"][:, access_mask]), axis=1) < 1.0)
        & (np.max(np.abs(d["time_metric_rate_proxy"][:, access_mask]), axis=1) < 0.1)
        & (np.max(np.abs(d["radial_accel_proxy"][:, access_mask]), axis=1) < 1.0)
        & (np.max(np.abs(d["flux"][:, access_mask]), axis=1) < 0.1)
    )
    open_mask = np.min(d["R"][:, access_mask] / baseR[None, access_mask], axis=1) >= 0.90
    noncollapse_lapse = np.min(d["N"][:, access_mask], axis=1) > 0.2
    bounded_B = np.max(d["B"][:, access_mask], axis=1) < 10.0
    row["access_quiet_fraction"] = float(np.mean(quiet))
    row["access_open_fraction"] = float(np.mean(open_mask))
    row["access_quiet_open_fraction"] = float(np.mean(quiet & open_mask & noncollapse_lapse & bounded_B))

    qi_rho = qi_samples(t, l, d["rho"], zones)
    # Also sample rho+p as a crude null-support debt indicator; not a formal QI bound.
    qi_nec = qi_samples(t, l, d["rho_plus_p_radial"], zones)
    for zone in zones:
        for k, v in qi_rho[zone].items():
            row[f"{zone}_rho_{k}"] = v
        for k, v in qi_nec[zone].items():
            row[f"{zone}_nec_{k}"] = v

    rho_log = row["access_core_rho_qi_strict_log10_L0max"]
    nec_log = row["access_core_nec_qi_strict_log10_L0max"]
    quiet_open = row["access_quiet_open_fraction"]
    maxB = row["max_B"]
    maxN = row["max_N"]
    minN = row["min_N"]
    accel = row["access_core_radial_accel_proxy_max_abs"]

    if rho_log < -0.1 and quiet_open > 0.90:
        mode = "rho-QI-static-obstruction-preserved"
    elif rho_log > 0.0 and nec_log < 0.5 and quiet_open > 0.90:
        mode = "rho-helped-but-NEC-debt-remains"
    elif maxB > 4.0 and quiet_open > 0.90:
        mode = "burden-shifted-to-long-radial-throat"
    elif maxN > 2.5 or minN < 0.35 or accel > 2.0:
        mode = "lapse-radial-gradient-burden"
    elif quiet_open < 0.2:
        mode = "quiet-window-lost"
    else:
        mode = "mixed-transition"
    row["failure_mode"] = mode
    return row


def run_sweep(out: Path) -> None:
    t = np.linspace(-1.1, 1.1, 401)
    l = np.linspace(-3.2, 3.2, 321)
    T, L = np.meshgrid(t, l, indexing="ij")
    Rbase = np.sqrt(1.0 + L**2)
    pc = prof_core(l)[None, :]
    pr = prof_ring(l, 0.90, 0.25)[None, :]
    pa = prof_access(l)[None, :]
    rows = []
    for B0 in [1.0, 1.2, math.sqrt(2), 1.6, 2.0, 3.0, 5.0, 8.0, 12.0]:
        for N0 in [1.0, 2.0, 3.0]:
            for r_amp in [0.0, 0.025, 0.05]:
                for omega in [0.0, 16.0] if r_amp > 0 else [0.0]:
                    N = np.exp(np.log(N0) * pc)
                    B = np.exp(np.log(B0) * pc)
                    R = Rbase.copy()
                    if r_amp > 0:
                        R = R + r_amp * np.sin(omega*T) * pa + 0.06 * np.sin(omega*T + math.pi) * pr
                    N = np.broadcast_to(N, R.shape).copy()
                    B = np.broadcast_to(B, R.shape).copy()
                    R = np.broadcast_to(R, R.shape).copy()
                    d = diagnostics(t, l, N, B, R)
                    row = summarize("sweep", t, l, d)
                    rows.append({
                        "B0": B0, "N0": N0, "r_amp": r_amp, "omega": omega,
                        "access_rho_log10_L0max": row["access_core_rho_qi_strict_log10_L0max"],
                        "access_nec_log10_L0max": row["access_core_nec_qi_strict_log10_L0max"],
                        "access_quiet_open_fraction": row["access_quiet_open_fraction"],
                        "access_rho_min": row["access_core_rho_min"],
                        "access_nec_min": row["access_core_rho_plus_p_radial_min"],
                        "access_tidal_max_abs": row["access_core_tidal_ang_max_abs"],
                        "access_accel_max_abs": row["access_core_radial_accel_proxy_max_abs"],
                        "max_B": row["max_B"], "max_N": row["max_N"],
                        "failure_mode": row["failure_mode"],
                    })
    pd.DataFrame(rows).to_csv(out / "lapse_radial_parameter_sweep.csv", index=False)


def main(outdir: str = ".") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    t = np.linspace(-1.2, 1.2, 801)
    l = np.linspace(-3.5, 3.5, 401)
    cases = [
        "static_reference",
        "static_Bcore_1p2",
        "static_Bcore_1p41421356237",
        "static_Bcore_2p0",
        "static_Bcore_3p0",
        "radial_tube_B5",
        "radial_tube_B10",
        "static_lapse_core_N2",
        "static_lapse_side_N2",
        "side_lapse_cycle_static_core",
        "Bcore2_side_lapse_cycle",
        "Bcycle_core_static_R",
        "Bcycle_core_with_lapse_comp",
        "redshift_B_trade_N3_B2",
        "Bcore2_Rmild_split",
        "Bcore2_Rtiny_fast",
    ]
    rows = []
    digest = []
    for case in cases:
        N, B, R = make_fields(case, t, l)
        d = diagnostics(t, l, N, B, R)
        rows.append(summarize(case, t, l, d))
        # representative time digest at l=0 and l~0.9
        idx0 = int(np.argmin(np.abs(l)))
        idxr = int(np.argmin(np.abs(np.abs(l)-0.9)))
        for ti in np.linspace(0, len(t)-1, 101).round().astype(int):
            digest.append({
                "case": case,
                "t": float(t[ti]),
                "N0": float(N[ti, idx0]), "B0": float(B[ti, idx0]), "R0": float(R[ti, idx0]),
                "rho0": float(d["rho"][ti, idx0]), "nec0": float(d["rho_plus_p_radial"][ti, idx0]),
                "Gkk0": float(d["Gkk_min"][ti, idx0]), "tidal0": float(d["tidal_ang"][ti, idx0]),
                "rho_repay": float(d["rho"][ti, idxr]), "nec_repay": float(d["rho_plus_p_radial"][ti, idxr]),
            })
    pd.DataFrame(rows).to_csv(out / "lapse_radial_case_summary.csv", index=False)
    pd.DataFrame(digest).to_csv(out / "lapse_radial_time_digest.csv", index=False)
    run_sweep(out)

    model_summary = {
        "name": "lapse + radial metric freedom throat reduced evaluation",
        "scope": "wormhole/QEE component only; no transport/catch layer",
        "metric": "ds^2=-N(l,t)^2 dt^2 + B(l,t)^2 dl^2 + R(l,t)^2 dOmega^2",
        "high_level_question": "Does lapse/radial freedom create a useful middle regime beyond R(l,t)-only multi-zone cycling?",
        "provisional_result": "Radial B freedom can strongly reduce or remove the rho-energy-density QI obstruction in this proxy, but the radial NEC/flaring support debt remains and the burden shifts into long radial throat geometry / radial metric engineering. Lapse freedom alone does not help the throat-core energy density and mostly adds gradient/acceleration burdens. Dynamic core actuation still loses quiet access.",
    }
    (out / "lapse_radial_model_summary.json").write_text(json.dumps(model_summary, indent=2))

    files = [
        "run_lapse_radial_freedom_eval.py",
        "lapse_radial_case_summary.csv",
        "lapse_radial_parameter_sweep.csv",
        "lapse_radial_time_digest.csv",
        "lapse_radial_model_summary.json",
    ]
    checksums = {}
    for name in files:
        fp = out / name
        if fp.exists():
            checksums[name] = hashlib.sha256(fp.read_bytes()).hexdigest()
    (out / "manifest.json").write_text(json.dumps({"generated":"2026-05-12", "files":files, "sha256":checksums}, indent=2))


if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
