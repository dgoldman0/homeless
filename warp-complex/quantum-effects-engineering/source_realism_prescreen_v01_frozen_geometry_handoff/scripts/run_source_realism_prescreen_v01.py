#!/usr/bin/env python3
"""
Source-realism pre-screen v0.1 for Reference Geometry v0.3.

This is a reduced source-side diagnostic.  It does three things:
1. Reconstructs the geometry-implied effective source proxies for the frozen N,B,R history.
2. Samples null-contracted stress histories along observer families with Lorentzian windows.
3. Separates the conserved geometry-implied effective source from the explicit positive compensation
   ledger overlay, which is currently a target null-contraction component rather than a full
   conserved stress tensor ansatz.

The output is a source pre-screen, not a quantum-state construction and not a backreaction solve.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import sys
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[0] / "data" / "source_realism_prescreen_v01"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE))

from run_reference_polish_screen import make_geometry, diagnostics_general, window_core, window_shoulder

PARAMS = {
    "label": "Reference Geometry v0.3",
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
C_QI = 3.0/(32.0*math.pi**2)


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


def lorentzian_weights(t: np.ndarray, center: float, tau: float) -> np.ndarray:
    # Normalized over the available grid so edge windows do not change scale.
    w = (tau / math.pi) / ((t-center)**2 + tau*tau)
    area = np.trapezoid(w, t)
    if area <= 0:
        return w
    return w / area


def sampled_minima(t: np.ndarray, y: np.ndarray, taus: list[float], centers: np.ndarray) -> list[dict]:
    rows = []
    for tau in taus:
        vals = []
        c_used = []
        for c in centers:
            # Skip heavily edge-truncated windows: require a reasonable span around center.
            if c - 4*tau < t[0] or c + 4*tau > t[-1]:
                continue
            w = lorentzian_weights(t, c, tau)
            vals.append(float(np.trapezoid(y*w, t)))
            c_used.append(float(c))
        if len(vals) == 0:
            continue
        vals_np = np.array(vals)
        idx = int(np.argmin(vals_np))
        min_avg = float(vals_np[idx])
        bound = -C_QI/(tau**4)
        rows.append({
            "tau": tau,
            "min_sampled_avg": min_avg,
            "center_at_min": c_used[idx],
            "qi_proxy_bound": bound,
            "qi_proxy_margin": min_avg - bound,  # negative means below proxy bound
            "qi_proxy_status": "above_proxy_bound" if min_avg >= bound else "below_proxy_bound",
        })
    return rows


def integrate_pos_neg(t: np.ndarray, y: np.ndarray, mask: np.ndarray) -> tuple[float,float,float,float]:
    if not np.any(mask):
        return 0.0,0.0,float("nan"),float("nan")
    tt = t[mask]
    yy = y[mask]
    neg_density = np.maximum(-yy, 0.0)
    pos_density = np.maximum(yy, 0.0)
    neg = float(np.trapezoid(neg_density, tt))
    pos = float(np.trapezoid(pos_density, tt))
    neg_centroid = float(np.trapezoid(tt*neg_density, tt)/neg) if neg > 0 else float("nan")
    pos_centroid = float(np.trapezoid(tt*pos_density, tt)/pos) if pos > 0 else float("nan")
    return neg,pos,neg_centroid,pos_centroid


def main() -> None:
    # Moderately high resolution for source-side sampling.
    l = np.linspace(-18.0, 18.0, 1501)
    t_end = PARAMS["T_B"] + 2*PARAMS["T_R"] + PARAMS["T_H"] + PARAMS["T_C"] + PARAMS["T_Breset"]
    t = np.linspace(0.0, t_end, 2401)
    N,B,R,phase,times,C = make_geometry(t,l,PARAMS)
    d = diagnostics_general(t,l,N,B,R)

    src = np.zeros_like(d["Tkk_min"])
    src_support = PARAMS["src_support_amp"] * C[:,None] * window_core(l, PARAMS["src_support_width"])[None,:]
    src_shoulder = PARAMS["src_shoulder_amp"] * C[:,None] * window_shoulder(l, PARAMS["src_shoulder_center"], PARAMS["src_shoulder_width"])[None,:]
    src += src_support + src_shoulder
    Tkk_geo = d["Tkk_min"]
    Tkk_total = Tkk_geo + src

    zones = {
        "access_mean": np.abs(l) <= 0.25,
        "support_mean": np.abs(l) <= 0.75,
        "inner_shoulder_mean": (np.abs(l) >= 1.2) & (np.abs(l) <= 2.7),
        "shoulder_mean": (np.abs(l) >= 1.2) & (np.abs(l) <= 4.5),
        "matching_mean": (np.abs(l) > 4.5) & (np.abs(l) <= 9.0),
    }
    i0 = int(np.argmin(np.abs(l)))
    observers = {"core_line": None, **zones}
    pm = phase_masks(phase)

    # Required source ledger by observer and phase.
    ledger_rows = []
    y_by_obs = {}
    ygeo_by_obs = {}
    ysrc_by_obs = {}
    for obs, zmask in observers.items():
        if obs == "core_line":
            y = Tkk_total[:, i0]
            yg = Tkk_geo[:, i0]
            ys = src[:, i0]
        else:
            y = np.mean(Tkk_total[:, zmask], axis=1)
            yg = np.mean(Tkk_geo[:, zmask], axis=1)
            ys = np.mean(src[:, zmask], axis=1)
        y_by_obs[obs] = y
        ygeo_by_obs[obs] = yg
        ysrc_by_obs[obs] = ys
        row = {"observer_family": obs}
        for ph, mask in pm.items():
            neg,pos,neg_c,pos_c = integrate_pos_neg(t,y,mask)
            neg_g,pos_g,_,_ = integrate_pos_neg(t,yg,mask)
            neg_s,pos_s,_,_ = integrate_pos_neg(t,ys,mask)
            row[f"{ph}_neg_total"] = neg
            row[f"{ph}_pos_total"] = pos
            row[f"{ph}_neg_geo"] = neg_g
            row[f"{ph}_pos_geo"] = pos_g
            row[f"{ph}_neg_overlay"] = neg_s
            row[f"{ph}_pos_overlay"] = pos_s
            row[f"{ph}_neg_centroid"] = neg_c
            row[f"{ph}_pos_centroid"] = pos_c
        row["comp_overlay_to_open_total_neg"] = row["comp_pos_overlay"]/(row["open_interval_neg_total"]+1e-15)
        row["comp_total_to_open_total_neg"] = row["comp_pos_total"]/(row["open_interval_neg_total"]+1e-15)
        row["open_neg_centroid_to_comp_pos_centroid_delay"] = row["comp_pos_centroid"] - row["open_interval_neg_centroid"]
        ledger_rows.append(row)
    ledger = pd.DataFrame(ledger_rows)
    ledger.to_csv(OUT/"required_source_observer_ledgers.csv", index=False)

    # Phase-region extrema of geometry-only and total null contractions plus flux/pressures proxies.
    extrema_rows = []
    for ph, mask in pm.items():
        if not np.any(mask):
            continue
        for zn, zmask in {"access": zones["access_mean"], "support": zones["support_mean"], "shoulder": zones["shoulder_mean"], "matching": zones["matching_mean"]}.items():
            idx = np.ix_(mask,zmask)
            extrema_rows.append({
                "phase": ph,
                "zone": zn,
                "min_Tkk_geo": float(np.min(Tkk_geo[idx])),
                "min_Tkk_total": float(np.min(Tkk_total[idx])),
                "max_Tkk_total": float(np.max(Tkk_total[idx])),
                "mean_Tkk_total": float(np.mean(Tkk_total[idx])),
                "max_overlay": float(np.max(src[idx])),
                "max_abs_flux_geo": float(np.max(np.abs(d["flux"][idx]))),
                "max_abs_Kll": float(np.max(np.abs(d["Kll"][idx]))),
                "max_abs_Kth": float(np.max(np.abs(d["Kth"][idx]))),
                "min_N": float(np.min(N[idx])),
                "min_R": float(np.min(R[idx])),
            })
    extrema = pd.DataFrame(extrema_rows)
    extrema.to_csv(OUT/"required_source_phase_zone_extrema.csv", index=False)

    # Lorentzian sampled stress screen.  We sample total and geometry-only histories separately.
    taus = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0, 80.0]
    centers = np.linspace(t[0], t[-1], 801)
    sample_rows = []
    for obs in ["core_line","access_mean","support_mean","shoulder_mean","matching_mean"]:
        for component, y in [("geometry_only", ygeo_by_obs[obs]), ("total_with_overlay", y_by_obs[obs]), ("overlay_only", ysrc_by_obs[obs])]:
            for row in sampled_minima(t,y,taus,centers):
                row2 = {"observer_family": obs, "component": component, **row}
                sample_rows.append(row2)
    samples = pd.DataFrame(sample_rows)
    samples.to_csv(OUT/"lorentzian_sampled_Tkk_screen.csv", index=False)

    # A simple quantum-interest ledger table.
    qi_rows = []
    for obs in ["core_line","access_mean","support_mean","shoulder_mean"]:
        r = ledger[ledger.observer_family == obs].iloc[0]
        open_duration = times[3] - times[0]  # B_setup ends at t1, R_close ends at t4; but open interval is t1-t4.
        open_duration = times[3] - times[0]
        actual_open_duration = times[3] - times[0]
        # More useful: R-open+hold+R-close duration
        open_interval_duration = times[3] - times[0]
        # times tuple = t1,t2,t3,t4,t5,t6, open starts at t1 ends t4.
        open_interval_duration = times[3] - times[0]
        qi_rows.append({
            "observer_family": obs,
            "open_interval_negative_exposure": float(r["open_interval_neg_total"]),
            "compensation_positive_exposure": float(r["comp_pos_total"]),
            "overlay_positive_exposure": float(r["comp_pos_overlay"]),
            "positive_to_negative_ratio": float(r["comp_total_to_open_total_neg"]),
            "overlay_to_negative_ratio": float(r["comp_overlay_to_open_total_neg"]),
            "negative_centroid_time": float(r["open_interval_neg_centroid"]),
            "positive_centroid_time": float(r["comp_pos_centroid"]),
            "centroid_delay": float(r["open_neg_centroid_to_comp_pos_centroid_delay"]),
            "open_interval_duration": float(PARAMS["T_R"] + PARAMS["T_H"] + PARAMS["T_R"]),
            "compensation_duration": float(PARAMS["T_C"]),
            "source_interest_reading": "structured_post_closure_repayment_target; quantum-interest model still required",
        })
    qi = pd.DataFrame(qi_rows)
    qi.to_csv(OUT/"quantum_interest_ledger.csv", index=False)

    # Source embedding status table: what we know from this pre-screen.
    embedding = pd.DataFrame([
        {
            "component": "geometry_implied_effective_source",
            "definition": "G_mu_nu[N,B,R]/8pi in the prescribed v0.3 geometry",
            "conservation_status": "conserved analytically by Bianchi identity for exact metric; finite-difference proxy not yet the limiting issue",
            "source_realism_status": "requires physical source model; supplies negative support and dynamic flare-gate stress history",
            "next_check": "compare full tensor components to candidate quantum or effective matter models",
        },
        {
            "component": "explicit_positive_compensation_overlay",
            "definition": "positive target contribution added to the null-contracted Tkk ledger during compensation phase",
            "conservation_status": "not yet a conserved stress tensor; currently a target null-contraction schedule",
            "source_realism_status": "primary embedding task; must be promoted to T_tt,T_ll,T_tl,T_thth components with nabla_mu T^munu closure or actuator exchange",
            "next_check": "construct minimal conserved stress-tensor ansatz for the support and shoulder repayment pulses",
        },
        {
            "component": "shoulder_lapse_shape",
            "definition": "bounded N shoulder pulse during compensation phase",
            "conservation_status": "part of geometry-implied effective source",
            "source_realism_status": "acts as matching/timing/co-control geometry; source model must explain associated stresses",
            "next_check": "test whether lapse-shaped stresses can be bundled with repayment source ansatz",
        },
    ])
    embedding.to_csv(OUT/"source_embedding_status.csv", index=False)

    # Candidate source priority table.
    candidates = pd.DataFrame([
        {"candidate_source_class":"conserved effective fluid / anisotropic stress ansatz", "fit_to_geometry":"high as a diagnostic model", "fit_to_compensation":"high", "physics_risk":"formal source rather than fundamental field", "priority":"first engineering embedding"},
        {"candidate_source_class":"nonminimally coupled scalar effective stress", "fit_to_geometry":"moderate", "fit_to_compensation":"moderate", "physics_risk":"stability and parameter tuning", "priority":"early physical ansatz"},
        {"candidate_source_class":"squeezed quantum field pulse train", "fit_to_geometry":"uncertain", "fit_to_compensation":"conceptually aligned", "physics_risk":"QI and quantum-interest bounds", "priority":"QI-facing model"},
        {"candidate_source_class":"Casimir/boundary vacuum stress", "fit_to_geometry":"possible for stationary support", "fit_to_compensation":"weak for dynamic repayment", "physics_risk":"boundary scale/matching", "priority":"support component only"},
        {"candidate_source_class":"holographic/double-trace traversability analogue", "fit_to_geometry":"conceptual", "fit_to_compensation":"conceptual", "physics_risk":"setting-specific rather than local construction", "priority":"theory comparison"},
        {"candidate_source_class":"modified-gravity effective stress", "fit_to_geometry":"potentially high", "fit_to_compensation":"potentially high", "physics_risk":"theory consistency/observational constraints", "priority":"separate branch"},
    ])
    candidates.to_csv(OUT/"candidate_source_priority_table.csv", index=False)

    # Extract the most important findings.
    def sample_summary(obs: str, component: str):
        sub = samples[(samples.observer_family == obs) & (samples.component == component)].copy()
        below = sub[sub.qi_proxy_status == "below_proxy_bound"]
        worst = sub.sort_values("qi_proxy_margin").iloc[0]
        return {
            "num_tau_tested": int(len(sub)),
            "num_below_proxy_bound": int(len(below)),
            "worst_tau": float(worst["tau"]),
            "worst_center": float(worst["center_at_min"]),
            "worst_sampled_avg": float(worst["min_sampled_avg"]),
            "worst_qi_proxy_bound": float(worst["qi_proxy_bound"]),
            "worst_qi_proxy_margin": float(worst["qi_proxy_margin"]),
        }

    source_ledgers = {}
    for obs in ["core_line","support_mean","shoulder_mean","access_mean"]:
        row = ledger[ledger.observer_family == obs].iloc[0]
        source_ledgers[obs] = {
            "open_negative_total": float(row["open_interval_neg_total"]),
            "comp_positive_total": float(row["comp_pos_total"]),
            "overlay_positive_total": float(row["comp_pos_overlay"]),
            "comp_total_to_open_neg": float(row["comp_total_to_open_total_neg"]),
            "delay": float(row["open_neg_centroid_to_comp_pos_centroid_delay"]),
        }
    extracts = {
        "reference": PARAMS,
        "phase_times": {"B_setup_end": times[0], "R_open_end": times[1], "hold_end": times[2], "R_close_end": times[3], "comp_end": times[4], "B_reset_end": times[5]},
        "source_ledgers": source_ledgers,
        "lorentzian_sampling_summary": {
            "core_total": sample_summary("core_line","total_with_overlay"),
            "support_total": sample_summary("support_mean","total_with_overlay"),
            "shoulder_total": sample_summary("shoulder_mean","total_with_overlay"),
            "access_total": sample_summary("access_mean","total_with_overlay"),
            "core_geometry_only": sample_summary("core_line","geometry_only"),
        },
        "embedding_reading": [
            "The geometry-implied effective source has a clean observer-family ledger for the frozen v0.3 metric.",
            "The explicit positive repayment overlay gives the desired compensation ratios but is currently a target null-contraction schedule, not a full conserved stress tensor.",
            "Lorentzian sampled histories remain the active physics gate: open/hold windows produce negative sampled averages below the simple QI proxy for long sampling times in the core/support observer families.",
            "The next constructive step is a minimal conserved stress-tensor ansatz for the compensation overlay, followed by QI/quantum-interest comparison for that ansatz.",
        ]
    }
    (OUT/"source_realism_prescreen_extracts.json").write_text(json.dumps(extracts, indent=2))

    print("Source-realism pre-screen v0.1 complete")
    print(json.dumps(extracts, indent=2))

if __name__ == "__main__":
    main()
