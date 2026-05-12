#!/usr/bin/env python3
"""
Reduced source-history screen for a flare-gated radial-stretch wormhole-support protocol.

Metric family:
    ds^2 = -dt^2 + B(l,t)^2 dl^2 + R(l,t)^2 dOmega^2

Design branch:
    B-prestretch -> R-flare-open -> quiet hold -> R-flare-close -> B-reset

The point of the branch is to fix a defect in the earlier B-only adiabatic
protocol: with R(l)=sqrt(1+l^2) held fixed, the A=0 state is still an active
areal throat and still carries negative null-contracted source history.  Here
R participates by flattening/restoring the flare curvature while keeping the
core radius nearly fixed; B remains the radial proper-length support-dilution
actuator.

This is a prescribed-geometry screen.  It reconstructs effective source
proxies from G_{mu nu}/(8 pi) using warped-product Einstein tensor formulas.
It is not a quantum-state construction and not a backreaction calculation.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

C_QI = 3.0 / (32.0 * math.pi**2)


def radius_access(l: np.ndarray, a: float = 1.0) -> np.ndarray:
    return np.sqrt(a * a + l * l)


def radial_window(l: np.ndarray, width: float, power: float = 4.0) -> np.ndarray:
    return np.exp(-(np.abs(l) / width) ** power)


def minjerk(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return 10 * x**3 - 15 * x**4 + 6 * x**5


def protocol_schedule(
    t: np.ndarray,
    order: str,
    TB: float,
    TR: float,
    TH: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return B amplitude, R-open amplitude, and phase labels."""
    AB = np.zeros_like(t, dtype=float)
    AR = np.zeros_like(t, dtype=float)
    phase = np.full(t.shape, "off", dtype=object)

    if order == "b_first":
        # B setup -> R open -> hold -> R close -> B reset.
        t0, t1 = 0.0, TB
        t2, t3 = t1 + TR, t1 + TR + TH
        t4, t5 = t3 + TR, t3 + TR + TB

        m = (t >= t0) & (t < t1)
        AB[m] = minjerk((t[m] - t0) / TB)
        phase[m] = "B_setup"

        m = (t >= t1) & (t < t2)
        AB[m] = 1.0
        AR[m] = minjerk((t[m] - t1) / TR)
        phase[m] = "R_open"

        m = (t >= t2) & (t < t3)
        AB[m] = 1.0
        AR[m] = 1.0
        phase[m] = "hold"

        m = (t >= t3) & (t < t4)
        AB[m] = 1.0
        AR[m] = minjerk((t4 - t[m]) / TR)
        phase[m] = "R_close"

        m = (t >= t4) & (t <= t5)
        AB[m] = minjerk((t5 - t[m]) / TB)
        phase[m] = "B_reset"

    elif order == "r_first":
        # R open while B is unstretched -> B setup -> hold -> B reset -> R close.
        t0, t1 = 0.0, TR
        t2, t3 = t1 + TB, t1 + TB + TH
        t4, t5 = t3 + TB, t3 + TB + TR

        m = (t >= t0) & (t < t1)
        AR[m] = minjerk((t[m] - t0) / TR)
        phase[m] = "R_open"

        m = (t >= t1) & (t < t2)
        AR[m] = 1.0
        AB[m] = minjerk((t[m] - t1) / TB)
        phase[m] = "B_setup"

        m = (t >= t2) & (t < t3)
        AB[m] = 1.0
        AR[m] = 1.0
        phase[m] = "hold"

        m = (t >= t3) & (t < t4)
        AR[m] = 1.0
        AB[m] = minjerk((t4 - t[m]) / TB)
        phase[m] = "B_reset"

        m = (t >= t4) & (t <= t5)
        AR[m] = minjerk((t5 - t[m]) / TR)
        phase[m] = "R_close"

    elif order == "simultaneous":
        # B and R start together; if one ramp finishes early it stays at 1.
        T = max(TB, TR)
        t0, t1 = 0.0, T
        t2, t3 = t1 + TH, t1 + TH + T

        m = (t >= t0) & (t < t1)
        AB[m] = minjerk((t[m] - t0) / TB)
        AR[m] = minjerk((t[m] - t0) / TR)
        phase[m] = "setup"

        m = (t >= t1) & (t < t2)
        AB[m] = 1.0
        AR[m] = 1.0
        phase[m] = "hold"

        m = (t >= t2) & (t <= t3)
        AB[m] = minjerk((t3 - t[m]) / TB)
        AR[m] = minjerk((t3 - t[m]) / TR)
        phase[m] = "reset"

    else:
        raise ValueError(f"unknown order {order!r}")

    return AB, AR, phase


def time_grid(order: str, TB: float, TR: float, TH: float, points_per_shortest_phase: int = 80) -> np.ndarray:
    if order in {"b_first", "r_first"}:
        t_end = 2 * TB + 2 * TR + TH
    elif order == "simultaneous":
        t_end = 2 * max(TB, TR) + TH
    else:
        raise ValueError(order)

    dt = min(TB, TR, TH) / points_per_shortest_phase
    n = int(math.ceil(t_end / dt)) + 1
    return np.linspace(0.0, t_end, n)


def make_BR_fields(
    t: np.ndarray,
    l: np.ndarray,
    *,
    B0: float,
    wB: float,
    wR: float,
    Rc: float,
    order: str,
    TB: float,
    TR: float,
    TH: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    AB, AR, phase = protocol_schedule(t, order, TB, TR, TH)
    FB = radial_window(l, wB)[None, :]
    B = 1.0 + (B0 - 1.0) * AB[:, None] * FB

    R_access = radius_access(l)[None, :]
    W = radial_window(l, wR)[None, :]
    R_standby = R_access + W * (Rc - R_access)
    R = R_standby + AR[:, None] * (R_access - R_standby)
    return B, R, phase


def make_B_only_fields(
    t: np.ndarray,
    l: np.ndarray,
    *,
    B0: float,
    wB: float,
    Tr: float,
    TH: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    A = np.zeros_like(t, dtype=float)
    phase = np.full(t.shape, "off", dtype=object)

    m = (t >= 0.0) & (t < Tr)
    A[m] = minjerk(t[m] / Tr)
    phase[m] = "B_setup"

    m = (t >= Tr) & (t < Tr + TH)
    A[m] = 1.0
    phase[m] = "hold"

    m = (t >= Tr + TH) & (t <= 2 * Tr + TH)
    A[m] = minjerk((2 * Tr + TH - t[m]) / Tr)
    phase[m] = "B_reset"

    B = 1.0 + (B0 - 1.0) * A[:, None] * radial_window(l, wB)[None, :]
    R = radius_access(l)[None, :] + np.zeros_like(B)
    return B, R, phase


def diagnostics(t: np.ndarray, l: np.ndarray, B: np.ndarray, R: np.ndarray) -> Dict[str, np.ndarray]:
    """Warped-product Einstein-source proxies for ds^2=-dt^2+B^2 dl^2+R^2 dOmega^2."""
    Bt = np.gradient(B, t, axis=0, edge_order=2)
    Bl = np.gradient(B, l, axis=1, edge_order=2)

    Rt = np.gradient(R, t, axis=0, edge_order=2)
    Rtt = np.gradient(Rt, t, axis=0, edge_order=2)
    Rl = np.gradient(R, l, axis=1, edge_order=2)
    Rll = np.gradient(Rl, l, axis=1, edge_order=2)
    Rtl = np.gradient(Rt, l, axis=1, edge_order=2)

    # Covariant Hessian of R in h_ab dx^a dx^b = -dt^2 + B^2 dl^2.
    Dtt = Rtt
    Dtl = Rtl - (Bt / B) * Rl
    Dll = Rll - B * Bt * Rt - (Bl / B) * Rl

    boxR = -Dtt + Dll / (B * B)
    gradR2 = -(Rt * Rt) + (Rl * Rl) / (B * B)

    Gtt = -2.0 * Dtt / R - 2.0 * boxR / R + (1.0 - gradR2) / (R * R)
    Gll = -2.0 * Dll / R + 2.0 * (B * B) * boxR / R - (B * B) * (1.0 - gradR2) / (R * R)
    Gtl = -2.0 * Dtl / R

    Tkk_plus = (Gtt + Gll / (B * B) + 2.0 * Gtl / B) / (8.0 * math.pi)
    Tkk_minus = (Gtt + Gll / (B * B) - 2.0 * Gtl / B) / (8.0 * math.pi)
    Tkk_min = np.minimum(Tkk_plus, Tkk_minus)
    flux_hat = Gtl / (8.0 * math.pi * B)

    return {
        "Bt_over_B": Bt / B,
        "Rt_over_R": Rt / R,
        "Tkk_plus": Tkk_plus,
        "Tkk_minus": Tkk_minus,
        "Tkk_min": Tkk_min,
        "flux_hat": flux_hat,
    }


def summarize_case(
    *,
    case: str,
    order: str,
    B0: float,
    wB: float,
    wR: float | None,
    Rc: float | None,
    TB: float,
    TR: float | None,
    TH: float,
    l_extent: float = 22.0,
    n_l: int = 801,
) -> Tuple[dict, pd.DataFrame]:
    l = np.linspace(-l_extent, l_extent, n_l)

    if order == "B_only":
        Tr = TB
        dt = min(Tr, TH) / 80.0
        t = np.linspace(0.0, 2 * Tr + TH, int(math.ceil((2 * Tr + TH) / dt)) + 1)
        B, R, phase = make_B_only_fields(t, l, B0=B0, wB=wB, Tr=Tr, TH=TH)
    else:
        assert TR is not None and wR is not None and Rc is not None
        t = time_grid(order, TB, TR, TH)
        B, R, phase = make_BR_fields(t, l, B0=B0, wB=wB, wR=wR, Rc=Rc, order=order, TB=TB, TR=TR, TH=TH)

    d = diagnostics(t, l, B, R)
    i0 = int(np.argmin(np.abs(l)))
    access = np.abs(l) <= 0.25
    shoulder = (np.abs(l) >= 0.55) & (np.abs(l) <= max(3.0, 1.4 * max(wB, wR or wB)))

    neg_core = np.maximum(-d["Tkk_min"][:, i0], 0.0)
    row = {
        "case": case,
        "order": order,
        "B0": B0,
        "wB": wB,
        "wR": wR,
        "Rc": Rc,
        "TB_or_Tr": TB,
        "TR": TR,
        "TH": TH,
        "full_core_negative_exposure": float(np.trapezoid(neg_core, t)),
        "min_core_Tkk": float(np.min(d["Tkk_min"][:, i0])),
        "hold_core_Tkk_min": float(np.min(d["Tkk_min"][phase == "hold", i0])) if np.any(phase == "hold") else float("nan"),
        "max_access_abs_Bt_over_B": float(np.max(np.abs(d["Bt_over_B"][:, access]))),
        "max_access_abs_Rt_over_R": float(np.max(np.abs(d["Rt_over_R"][:, access]))),
        "max_access_abs_flux": float(np.max(np.abs(d["flux_hat"][:, access]))),
        "max_shoulder_abs_flux": float(np.max(np.abs(d["flux_hat"][:, shoulder]))),
    }

    phase_rows = []
    for ph in [p for p in ["B_setup", "R_open", "setup", "hold", "R_close", "reset", "B_reset"] if np.any(phase == p)]:
        m = phase == ph
        exp = float(np.trapezoid(neg_core[m], t[m])) if np.sum(m) > 1 else 0.0
        row[f"{ph}_core_negative_exposure"] = exp
        phase_rows.append({
            "case": case,
            "phase": ph,
            "core_negative_exposure": exp,
            "phase_duration": float(t[m][-1] - t[m][0]) if np.sum(m) > 1 else 0.0,
            "phase_min_core_Tkk": float(np.min(d["Tkk_min"][m, i0])) if np.sum(m) else float("nan"),
            "phase_max_access_abs_Bt_over_B": float(np.max(np.abs(d["Bt_over_B"][m][:, access]))) if np.sum(m) else float("nan"),
            "phase_max_access_abs_Rt_over_R": float(np.max(np.abs(d["Rt_over_R"][m][:, access]))) if np.sum(m) else float("nan"),
            "phase_max_access_abs_flux": float(np.max(np.abs(d["flux_hat"][m][:, access]))) if np.sum(m) else float("nan"),
        })

    return row, pd.DataFrame(phase_rows)


def run(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    cases = []
    phase_tables = []

    # Main comparison: old B-only versus flare-gated B,R branch.
    for Tr in [10.0, 30.0, 100.0]:
        row, ph = summarize_case(case=f"old_B_only_B8_w8_Tr{Tr:g}", order="B_only", B0=8.0, wB=8.0, wR=None, Rc=None, TB=Tr, TR=None, TH=60.0)
        cases.append(row); phase_tables.append(ph)

    for TR in [5.0, 10.0, 30.0]:
        row, ph = summarize_case(case=f"flare_gated_B8_w8_TB100_TR{TR:g}", order="b_first", B0=8.0, wB=8.0, wR=5.0, Rc=1.0, TB=100.0, TR=TR, TH=60.0)
        cases.append(row); phase_tables.append(ph)

    # Ordering comparison.
    for order in ["b_first", "simultaneous", "r_first"]:
        row, ph = summarize_case(case=f"order_{order}_B8_w8_TB100_TR30", order=order, B0=8.0, wB=8.0, wR=5.0, Rc=1.0, TB=100.0, TR=30.0, TH=60.0)
        cases.append(row); phase_tables.append(ph)

    # Simultaneous ramp sanity variants.
    for TB, TR in [(30.0, 30.0), (10.0, 10.0), (30.0, 10.0), (10.0, 30.0)]:
        row, ph = summarize_case(case=f"simultaneous_B8_w8_TB{TB:g}_TR{TR:g}", order="simultaneous", B0=8.0, wB=8.0, wR=5.0, Rc=1.0, TB=TB, TR=TR, TH=60.0)
        cases.append(row); phase_tables.append(ph)

    # Sensitivity to stretch strength.
    for B0 in [3.0, 5.0, 8.0]:
        row, ph = summarize_case(case=f"stretch_sensitivity_B{B0:g}_w8_TB100_TR10", order="b_first", B0=B0, wB=8.0, wR=5.0, Rc=1.0, TB=100.0, TR=10.0, TH=60.0)
        cases.append(row); phase_tables.append(ph)

    summary = pd.DataFrame(cases)
    phases = pd.concat(phase_tables, ignore_index=True)
    summary.to_csv(outdir / "branch_case_summary.csv", index=False)
    phases.to_csv(outdir / "branch_phase_exposures.csv", index=False)

    main_cols = [
        "case", "order", "B0", "TB_or_Tr", "TR", "TH", "full_core_negative_exposure",
        "hold_core_Tkk_min", "max_access_abs_Bt_over_B", "max_access_abs_Rt_over_R", "max_access_abs_flux",
    ]
    summary[main_cols].to_csv(outdir / "comparison_table.csv", index=False)

    extracts = {
        "design_name": "flare-gated radial stretch",
        "core_claims": [
            "B-only stretching was dynamically clean but source-history failing because the R=sqrt(1+l^2) throat remains active when A_B=0.",
            "R participation is most useful as flare-curvature gating, not core radius breathing during access.",
            "The best tested ordering is B-prestretch -> R-flare-open -> quiet hold -> R-flare-close -> B-reset.",
            "B_setup and B_reset carry essentially zero core negative exposure when R is in the flattened standby profile.",
            "The hold still carries negative null-contracted exposure, so this remains a geometry/control improvement, not a source-realism solution.",
        ],
        "selected_cases": summary[main_cols].to_dict(orient="records"),
    }
    (outdir / "extracts.json").write_text(json.dumps(extracts, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    args = parser.parse_args()
    run(args.outdir)
