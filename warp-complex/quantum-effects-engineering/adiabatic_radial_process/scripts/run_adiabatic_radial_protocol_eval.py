#!/usr/bin/env python3
"""
Adiabatic B(l,t) protocol evaluation.

Wormhole-component-only reduced diagnostic for the protocol

    setup ramp -> quasi-static B-stretched hold -> reset ramp

in the metric

    ds^2 = -dt^2 + B(l,t)^2 dl^2 + R0(l)^2 dOmega^2,
    R0(l) = sqrt(1+l^2).

The evaluation treats B(l,t) as a proper-radial infrastructure control.
It computes warped-product Einstein-source proxies, null-expansion proxies,
radial flux, extrinsic-rate proxies, transition/shoulder budgets, and access
hold isolation metrics.  It is a prescribed-geometry screening test rather
than a semiclassical source construction.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

C_QI = 3.0/(32.0*math.pi**2)

def radius(l: np.ndarray) -> np.ndarray:
    return np.sqrt(1.0 + l*l)

def radial_window(l: np.ndarray, width: float, power: float = 4.0) -> np.ndarray:
    return np.exp(-(np.abs(l)/width)**power)

def ramp_shape(x: np.ndarray, kind: str) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    if kind == "cosine":
        return 0.5*(1.0 - np.cos(np.pi*x))
    if kind == "minjerk":
        return 10*x**3 - 15*x**4 + 6*x**5
    if kind == "smootherstep":
        return x**3*(x*(x*6 - 15) + 10)
    raise ValueError(kind)

def amplitude_protocol(t: np.ndarray, Tr: float, Th: float, kind: str) -> tuple[np.ndarray, np.ndarray]:
    """Setup/hold/reset protocol and phase label."""
    A = np.zeros_like(t)
    phase = np.full(t.shape, "off", dtype=object)

    setup = (t >= 0.0) & (t < Tr)
    hold = (t >= Tr) & (t <= Tr + Th)
    reset = (t > Tr + Th) & (t <= 2*Tr + Th)

    A[setup] = ramp_shape(t[setup]/Tr, kind)
    A[hold] = 1.0
    A[reset] = ramp_shape((2*Tr + Th - t[reset])/Tr, kind)

    phase[setup] = "setup"
    phase[hold] = "hold"
    phase[reset] = "reset"
    return A, phase

def make_B(t: np.ndarray, l: np.ndarray, B0: float, width: float, Tr: float, Th: float, kind: str, static: bool=False) -> tuple[np.ndarray, np.ndarray]:
    F = radial_window(l, width)[None, :]
    if static:
        A = np.ones_like(t)
        phase = np.full(t.shape, "hold", dtype=object)
    else:
        A, phase = amplitude_protocol(t, Tr, Th, kind)
    B = 1.0 + (B0 - 1.0)*A[:, None]*F
    return B, phase

def diagnostics(t: np.ndarray, l: np.ndarray, B: np.ndarray) -> dict[str, np.ndarray]:
    R = radius(l)[None, :]
    Rl = (l/radius(l))[None, :]
    Rll = (1.0/(radius(l)**3))[None, :]

    Bt = np.gradient(B, t, axis=0, edge_order=2)
    Btt = np.gradient(Bt, t, axis=0, edge_order=2)
    Bl = np.gradient(B, l, axis=1, edge_order=2)

    # 2D warped-product quantities for h_ab dx^a dx^b = -dt^2 + B^2 dl^2.
    boxR = (Rll - (Bl/B)*Rl)/(B*B)
    gradR2 = (Rl*Rl)/(B*B)

    Gtt = -2.0*boxR/R + (1.0 - gradR2)/(R*R)
    Gll = -(B*B - Rl*Rl)/(R*R)
    Gtl = 2.0*(Bt/B)*Rl/R

    rho = Gtt/(8.0*math.pi)
    p_radial = Gll/(8.0*math.pi*B*B)
    Tkk_plus = (Gtt + Gll/(B*B) + 2.0*Gtl/B)/(8.0*math.pi)
    Tkk_minus = (Gtt + Gll/(B*B) - 2.0*Gtl/B)/(8.0*math.pi)
    Tkk_min = np.minimum(Tkk_plus, Tkk_minus)

    flux_hat = Gtl/(8.0*math.pi*B)

    # Angular pressure proxy: p_t = (Box R/R - 0.5 R_h)/(8pi), R_h=2 B_tt/B.
    p_tangential = (boxR/R - Btt/B)/(8.0*math.pi)

    # Null expansions for radial null congruences with R_t=0, N=1.
    theta_plus = 2.0*(Rl/B)/R
    theta_minus = -2.0*(Rl/B)/R
    expansion_product = theta_plus*theta_minus

    K_l_l = -Bt/B
    K_theta_theta_mixed = np.zeros_like(K_l_l)

    return {
        "B": B,
        "Bt": Bt,
        "Btt": Btt,
        "Bl": Bl,
        "rho": rho,
        "p_radial": p_radial,
        "Tkk_plus": Tkk_plus,
        "Tkk_minus": Tkk_minus,
        "Tkk_min": Tkk_min,
        "flux_hat": flux_hat,
        "p_tangential": p_tangential,
        "theta_plus": theta_plus,
        "theta_minus": theta_minus,
        "expansion_product": expansion_product,
        "K_l_l": K_l_l,
        "K_theta_theta": K_theta_theta_mixed,
        "rate": Bt/B,
        "accel": Btt/B,
    }

def summarize_case(case: str, params: dict, t: np.ndarray, l: np.ndarray, phase: np.ndarray, d: dict[str, np.ndarray]) -> dict:
    access = np.abs(l) <= 0.25
    support = np.abs(l) <= 0.55
    shoulder = (np.abs(l) >= 0.55) & (np.abs(l) <= max(3.0, 1.4*params["width"]))
    outer = np.abs(l) >= max(3.0, 1.4*params["width"])

    phase_masks = {
        "all": np.ones_like(t, dtype=bool),
        "setup": phase == "setup",
        "hold": phase == "hold",
        "reset": phase == "reset",
        "ramps": (phase == "setup") | (phase == "reset"),
    }

    row = {"case": case, **params}
    row["n_t"] = len(t)
    row["t_start"] = float(t[0])
    row["t_end"] = float(t[-1])

    # Static/source diagnostics during hold, excluding first/last few cells of hold.
    hold_mask = phase_masks["hold"]
    if np.any(hold_mask):
        hold_indices = np.where(hold_mask)[0]
        if len(hold_indices) > 10:
            hold_mask2 = np.zeros_like(hold_mask)
            hold_mask2[hold_indices[5:-5]] = True
            hold_mask = hold_mask2

    for zone_name, zmask in [("access", access), ("support", support), ("shoulder", shoulder)]:
        for phase_name, pmask in phase_masks.items():
            if not np.any(pmask):
                continue
            idx = np.ix_(pmask, zmask)
            row[f"{zone_name}_{phase_name}_min_rho"] = float(np.min(d["rho"][idx]))
            row[f"{zone_name}_{phase_name}_min_Tkk"] = float(np.min(d["Tkk_min"][idx]))
            row[f"{zone_name}_{phase_name}_max_abs_flux"] = float(np.max(np.abs(d["flux_hat"][idx])))
            row[f"{zone_name}_{phase_name}_max_abs_Kll"] = float(np.max(np.abs(d["K_l_l"][idx])))
            row[f"{zone_name}_{phase_name}_max_abs_accel"] = float(np.max(np.abs(d["accel"][idx])))
            row[f"{zone_name}_{phase_name}_max_abs_p_tangential"] = float(np.max(np.abs(d["p_tangential"][idx])))
            row[f"{zone_name}_{phase_name}_max_abs_expansion_product"] = float(np.max(np.abs(d["expansion_product"][idx])))

    # Access quietness at each time.
    access_rate = np.max(np.abs(d["rate"][:, access]), axis=1)
    access_flux = np.max(np.abs(d["flux_hat"][:, access]), axis=1)
    access_accel = np.max(np.abs(d["accel"][:, access]), axis=1)
    access_pt_dyn = np.max(np.abs(d["p_tangential"][:, access]), axis=1)

    quiet = (access_rate < 0.02) & (access_flux < 1e-3) & (access_accel < 0.02)
    for phase_name, pmask in phase_masks.items():
        if np.any(pmask):
            row[f"{phase_name}_access_quiet_fraction"] = float(np.mean(quiet[pmask]))

    # Integrated negative Tkk by proper radial length during hold midpoint.
    if np.any(phase == "hold"):
        hold_mid = np.where(phase == "hold")[0][len(np.where(phase == "hold")[0])//2]
    else:
        hold_mid = len(t)//2
    Bmid = d["B"][hold_mid, :]
    negTkk = np.maximum(-d["Tkk_min"][hold_mid, :], 0.0)
    row["hold_integrated_negative_Tkk_proper"] = float(np.trapezoid(negTkk*Bmid, l))
    row["hold_proper_half_length_R2"] = proper_half_length(l, Bmid, target_R=2.0)
    row["hold_proper_half_length_R3"] = proper_half_length(l, Bmid, target_R=3.0)

    # Gate classification.
    ramp_cost = max(row.get("access_ramps_max_abs_Kll", 0.0), row.get("access_ramps_max_abs_accel", 0.0))
    flux_cost = row.get("shoulder_ramps_max_abs_flux", 0.0)
    hold_quiet = row.get("hold_access_quiet_fraction", 0.0)
    hold_Tkk = row.get("access_hold_min_Tkk", row.get("access_all_min_Tkk", 0.0))

    if params.get("static", False):
        cls = "static-hold-reference"
    elif hold_quiet >= 0.98 and ramp_cost < 0.05 and flux_cost < 0.002:
        cls = "adiabatic-clean"
    elif hold_quiet >= 0.98 and ramp_cost < 0.15:
        cls = "adiabatic-rate-budget"
    elif hold_quiet >= 0.90:
        cls = "partial-adiabatic"
    else:
        cls = "dynamic-access-burden"
    row["classification"] = cls
    row["hold_Tkk_min_for_gate"] = hold_Tkk
    row["ramp_cost_max_access_K_or_accel"] = ramp_cost
    row["ramp_cost_max_shoulder_flux"] = flux_cost
    return row

def proper_half_length(l: np.ndarray, B: np.ndarray, target_R: float) -> float:
    R = radius(l)
    mask = (l >= 0) & (R <= target_R)
    if np.sum(mask) < 2:
        return float("nan")
    return float(np.trapezoid(B[mask], l[mask]))

def make_time_grid(Tr: float, Th: float, points_per_ramp: int = 241, points_hold: int = 241) -> np.ndarray:
    # Includes small off segments before and after.
    pre = np.linspace(-0.15*Tr, 0.0, max(20, points_per_ramp//6), endpoint=False)
    setup = np.linspace(0.0, Tr, points_per_ramp, endpoint=False)
    hold = np.linspace(Tr, Tr+Th, points_hold, endpoint=False)
    reset = np.linspace(Tr+Th, 2*Tr+Th, points_per_ramp, endpoint=False)
    post = np.linspace(2*Tr+Th, 2*Tr+Th+0.15*Tr, max(20, points_per_ramp//6))
    return np.unique(np.concatenate([pre, setup, hold, reset, post]))

def main(outdir: str = ".") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    l = np.linspace(-22.0, 22.0, 1601)
    B0_values = [2.0, 3.0, 5.0]
    width_values = [1.6, 5.0, 8.0]
    Tr_values = [10.0, 30.0, 100.0, 300.0]
    ramp_kinds = ["cosine", "minjerk"]
    Th = 60.0

    rows = []
    digest_rows = []

    # Static hold references, including the unstretched B=1 baseline.
    t_static = np.linspace(0.0, Th, 301)
    B, phase = make_B(t_static, l, 1.0, 1.0, 1.0, Th, "minjerk", static=True)
    d = diagnostics(t_static, l, B)
    params = {"B0": 1.0, "width": 1.0, "Tr": math.inf, "Th": Th, "ramp_kind": "static", "static": True}
    rows.append(summarize_case("static_B1_baseline", params, t_static, l, phase, d))
    for B0 in B0_values:
        for width in width_values:
            B, phase = make_B(t_static, l, B0, width, 1.0, Th, "minjerk", static=True)
            d = diagnostics(t_static, l, B)
            params = {"B0": B0, "width": width, "Tr": math.inf, "Th": Th, "ramp_kind": "static", "static": True}
            rows.append(summarize_case(f"static_B{B0:g}_w{width:g}", params, t_static, l, phase, d))

    # Dynamic protocols.
    for B0 in B0_values:
        for width in width_values:
            for kind in ramp_kinds:
                for Tr in Tr_values:
                    t = make_time_grid(Tr, Th)
                    B, phase = make_B(t, l, B0, width, Tr, Th, kind, static=False)
                    d = diagnostics(t, l, B)
                    params = {"B0": B0, "width": width, "Tr": Tr, "Th": Th, "ramp_kind": kind, "static": False}
                    case = f"adiabatic_B{B0:g}_w{width:g}_{kind}_Tr{Tr:g}"
                    row = summarize_case(case, params, t, l, phase, d)
                    rows.append(row)

                    # Compact time digest for representative cases only.
                    if (B0, width, kind, Tr) in [
                        (3.0, 5.0, "minjerk", 30.0),
                        (3.0, 5.0, "minjerk", 100.0),
                        (3.0, 5.0, "minjerk", 300.0),
                        (5.0, 8.0, "minjerk", 100.0),
                        (3.0, 1.6, "cosine", 10.0),
                    ]:
                        i0 = np.argmin(np.abs(l))
                        ish = np.argmin(np.abs(np.abs(l)-width))
                        sample_idx = np.unique(np.round(np.linspace(0, len(t)-1, 151)).astype(int))
                        for ti in sample_idx:
                            digest_rows.append({
                                "case": case,
                                "t": float(t[ti]),
                                "phase": str(phase[ti]),
                                "B_access_l0": float(d["B"][ti, i0]),
                                "Kll_access_l0": float(d["K_l_l"][ti, i0]),
                                "accel_access_l0": float(d["accel"][ti, i0]),
                                "rho_access_l0": float(d["rho"][ti, i0]),
                                "Tkk_access_l0": float(d["Tkk_min"][ti, i0]),
                                "flux_shoulder": float(d["flux_hat"][ti, ish]),
                                "p_tangential_access_l0": float(d["p_tangential"][ti, i0]),
                            })

    summary = pd.DataFrame(rows)
    summary.to_csv(out/"adiabatic_B_protocol_case_summary.csv", index=False)
    pd.DataFrame(digest_rows).to_csv(out/"adiabatic_B_protocol_time_digest.csv", index=False)

    # Scaling table: slopes for ramp costs vs Tr for each B0,width,kind.
    scale_rows = []
    dyn = summary[summary["static"] == False].copy()
    for (B0, width, kind), g in dyn.groupby(["B0","width","ramp_kind"]):
        gg = g.sort_values("Tr")
        for metric in ["access_ramps_max_abs_Kll", "access_ramps_max_abs_accel", "shoulder_ramps_max_abs_flux", "access_ramps_max_abs_p_tangential"]:
            x = np.log10(gg["Tr"].to_numpy(dtype=float))
            yv = gg[metric].to_numpy(dtype=float)
            if np.all(yv > 0):
                y = np.log10(yv)
                slope, intercept = np.polyfit(x, y, 1)
            else:
                slope, intercept = float("nan"), float("nan")
            scale_rows.append({
                "B0": B0,
                "width": width,
                "ramp_kind": kind,
                "metric": metric,
                "loglog_slope_vs_Tr": slope,
                "value_Tr10": float(gg[gg["Tr"]==10.0][metric].iloc[0]) if np.any(gg["Tr"]==10.0) else float("nan"),
                "value_Tr300": float(gg[gg["Tr"]==300.0][metric].iloc[0]) if np.any(gg["Tr"]==300.0) else float("nan"),
            })
    pd.DataFrame(scale_rows).to_csv(out/"adiabatic_B_protocol_scaling.csv", index=False)

    # Extracts.
    extracts = {
        "classification_counts": summary["classification"].value_counts().to_dict(),
        "best_adiabatic_clean": summary[summary["classification"].eq("adiabatic-clean")]
            .sort_values(["hold_Tkk_min_for_gate", "ramp_cost_max_access_K_or_accel"], ascending=[False, True])
            .head(12).to_dict(orient="records"),
        "representative_B3_w5": summary[(summary["B0"].eq(3.0)) & (summary["width"].eq(5.0))]
            .sort_values(["static","ramp_kind","Tr"]).to_dict(orient="records"),
        "scaling_summary": pd.DataFrame(scale_rows).groupby("metric")["loglog_slope_vs_Tr"].median().to_dict(),
        "main_interpretation": [
            "Adiabatic B(l,t) setup/hold/reset preserves the static hold benefits when evaluated during the hold interval.",
            "Ramp costs scale down with ramp time; rate/flux terms scale approximately as 1/Tr and acceleration/angular-pressure terms approximately as 1/Tr^2.",
            "Dynamic B does not move the areal throat or create R_t-driven null-expansion failure in this restricted metric family.",
            "The price of dynamic setup/reset is a radial extrinsic-curvature/flux/angular-pressure budget during the ramps.",
            "The prescribed-geometry model contains no evolution/ringing; stability and backreaction require a later source/evolution gate.",
        ],
    }
    (out/"adiabatic_B_protocol_extracts.json").write_text(json.dumps(extracts, indent=2))

    # README not memo, just provenance.
    (out/"README.md").write_text(
        "# Adiabatic B Protocol Evaluation\n\n"
        "Local scratch evaluation of setup/hold/reset protocols for a radially stretched wormhole throat metric.\n\n"
        "No report memo is included.  Files contain the generator script, case summary, scaling table, time digest, and extracts.\n"
    )

    files = [
        "run_adiabatic_B_protocol_eval.py",
        "adiabatic_B_protocol_case_summary.csv",
        "adiabatic_B_protocol_scaling.csv",
        "adiabatic_B_protocol_time_digest.csv",
        "adiabatic_B_protocol_extracts.json",
        "README.md",
    ]
    checksums = {}
    for name in files:
        fp = out/name
        if fp.exists():
            checksums[name] = hashlib.sha256(fp.read_bytes()).hexdigest()
    manifest = {
        "bundle": "adiabatic_B_protocol_eval",
        "scope": "dynamic B(l,t) setup/hold/reset prototype; no memo",
        "metric": "ds^2=-dt^2+B(l,t)^2 dl^2 + (1+l^2)dOmega^2",
        "files": files,
        "sha256": checksums,
    }
    (out/"manifest.json").write_text(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
