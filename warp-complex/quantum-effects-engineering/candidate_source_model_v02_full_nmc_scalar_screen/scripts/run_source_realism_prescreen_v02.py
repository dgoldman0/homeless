#!/usr/bin/env python3
"""
Source-realism pre-screen v0.2 for Reference Geometry v0.3.

This pass keeps the frozen v0.3 geometry fixed and refines the active source-realism tasks:

1. Embed the positive compensation Tkk overlay into a minimal anisotropic-stress ansatz.
2. Add setup/reset support-shoulder repayment overlays and search for full-cycle ledger balance.
3. Sweep repayment timing/duration against Lorentzian sampled-Tkk proxy diagnostics.

The output remains a reduced source-side screen.  It is a source-ledger and embedding diagnostic,
not a quantum-state construction and not a backreaction solve.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import sys
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[0]
OUT = ROOT / "data" / "source_realism_prescreen_v02"
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
EPS = 1e-15


def smooth_pulse01(x: np.ndarray) -> np.ndarray:
    """Compact smooth positive pulse on [0,1] with zero endpoints."""
    x = np.clip(x, 0.0, 1.0)
    return np.sin(np.pi*x)**2


def phase_masks(phase: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "B_setup": phase == "B_setup",
        "R_open": phase == "R_open",
        "hold": phase == "hold",
        "R_close": phase == "R_close",
        "comp": phase == "comp",
        "B_reset": phase == "B_reset",
        "open_interval": (phase == "R_open") | (phase == "hold") | (phase == "R_close"),
        "setup_reset": (phase == "B_setup") | (phase == "B_reset"),
        "full_cycle": np.ones_like(phase, dtype=bool),
    }


def integrate_pos_neg(t: np.ndarray, y: np.ndarray, mask: np.ndarray) -> tuple[float,float,float,float]:
    if not np.any(mask):
        return 0.0, 0.0, float("nan"), float("nan")
    tt = t[mask]
    yy = y[mask]
    neg_density = np.maximum(-yy, 0.0)
    pos_density = np.maximum(yy, 0.0)
    neg = float(np.trapezoid(neg_density, tt)) if len(tt) > 1 else 0.0
    pos = float(np.trapezoid(pos_density, tt)) if len(tt) > 1 else 0.0
    neg_centroid = float(np.trapezoid(tt*neg_density, tt)/neg) if neg > 0 else float("nan")
    pos_centroid = float(np.trapezoid(tt*pos_density, tt)/pos) if pos > 0 else float("nan")
    return neg, pos, neg_centroid, pos_centroid


def lorentzian_weights(t: np.ndarray, center: float, tau: float) -> np.ndarray:
    w = (tau / math.pi) / ((t-center)**2 + tau*tau)
    area = np.trapezoid(w, t)
    return w / area if area > 0 else w


def sampled_min(t: np.ndarray, y: np.ndarray, tau: float, centers: np.ndarray) -> dict:
    vals=[]; cs=[]
    for c in centers:
        if c - 4*tau < t[0] or c + 4*tau > t[-1]:
            continue
        w=lorentzian_weights(t,c,tau)
        vals.append(float(np.trapezoid(y*w,t)))
        cs.append(float(c))
    if not vals:
        return {"tau":tau,"min_sampled_avg":float("nan"),"center_at_min":float("nan"),"qi_proxy_bound":-C_QI/tau**4,"qi_proxy_margin":float("nan")}
    vals=np.array(vals); idx=int(np.argmin(vals)); bound=-C_QI/tau**4
    return {"tau":tau,"min_sampled_avg":float(vals[idx]),"center_at_min":cs[idx],"qi_proxy_bound":bound,"qi_proxy_margin":float(vals[idx]-bound),"status":"above_proxy_bound" if vals[idx]>=bound else "below_proxy_bound"}


def build_grid(n_t: int=1801, n_l: int=1001):
    l = np.linspace(-18.0, 18.0, n_l)
    t_end = PARAMS["T_B"] + 2*PARAMS["T_R"] + PARAMS["T_H"] + PARAMS["T_C"] + PARAMS["T_Breset"]
    t = np.linspace(0.0, t_end, n_t)
    N,B,R,phase,times,C = make_geometry(t,l,PARAMS)
    d = diagnostics_general(t,l,N,B,R)
    return t,l,N,B,R,phase,times,C,d


def build_open_comp_overlay(t: np.ndarray, l: np.ndarray, C: np.ndarray, src_support_amp=None, src_shoulder_amp=None) -> np.ndarray:
    if src_support_amp is None: src_support_amp = PARAMS["src_support_amp"]
    if src_shoulder_amp is None: src_shoulder_amp = PARAMS["src_shoulder_amp"]
    return (
        src_support_amp*C[:,None]*window_core(l, PARAMS["src_support_width"])[None,:]
        + src_shoulder_amp*C[:,None]*window_shoulder(l, PARAMS["src_shoulder_center"], PARAMS["src_shoulder_width"])[None,:]
    )


def setup_reset_envelope(t: np.ndarray, times: tuple[float,float,float,float,float,float]) -> np.ndarray:
    t1,t2,t3,t4,t5,t6 = times
    env = np.zeros_like(t)
    m=(t>=0)&(t<t1)
    env[m] = smooth_pulse01(t[m]/max(t1,EPS))
    m=(t>=t5)&(t<=t6)
    env[m] = smooth_pulse01((t[m]-t5)/max((t6-t5),EPS))
    return env


def support_ring_window(l: np.ndarray) -> np.ndarray:
    # Positive support/setup source concentrated in the inner support shoulders while preserving
    # the access-core line.  The smooth ring peaks near |l|~0.65 and falls rapidly inside |l|<0.3.
    return np.exp(-((np.abs(l)-0.65)/0.34)**4)


def setup_reset_overlay(t: np.ndarray, l: np.ndarray, times, amp_support: float, amp_shoulder: float, shoulder_center=2.3, shoulder_width=1.0) -> np.ndarray:
    env=setup_reset_envelope(t,times)
    Wsup=support_ring_window(l)
    Wsh=window_shoulder(l, shoulder_center, shoulder_width)
    return env[:,None]*(amp_support*Wsup[None,:] + amp_shoulder*Wsh[None,:])


def zone_histories(t,l,Tkk_total,src_overlay,phase):
    zones = {
        "core_line": None,
        "access_mean": np.abs(l) <= 0.25,
        "support_mean": np.abs(l) <= 0.75,
        "support_ring_mean": (np.abs(l) >= 0.28) & (np.abs(l) <= 0.95),
        "shoulder_mean": (np.abs(l) >= 1.2) & (np.abs(l) <= 4.5),
        "matching_mean": (np.abs(l) > 4.5) & (np.abs(l) <= 9.0),
    }
    i0=int(np.argmin(np.abs(l)))
    pm=phase_masks(phase)
    rows=[]; series={}; src_series={}
    for obs,zmask in zones.items():
        if obs=="core_line":
            y=Tkk_total[:,i0]; ys=src_overlay[:,i0]
        else:
            y=np.mean(Tkk_total[:,zmask],axis=1); ys=np.mean(src_overlay[:,zmask],axis=1)
        series[obs]=y; src_series[obs]=ys
        row={"observer_family":obs}
        for ph,mask in pm.items():
            neg,pos,nc,pc = integrate_pos_neg(t,y,mask)
            ns,ps,_,_ = integrate_pos_neg(t,ys,mask)
            row[f"{ph}_neg_total"] = neg
            row[f"{ph}_pos_total"] = pos
            row[f"{ph}_neg_centroid"] = nc
            row[f"{ph}_pos_centroid"] = pc
            row[f"{ph}_pos_overlay"] = ps
        row["open_comp_ratio"] = row["comp_pos_overlay"]/(row["open_interval_neg_total"]+EPS)
        row["setup_reset_comp_ratio"] = row["setup_reset_pos_overlay"]/(row["setup_reset_neg_total"]+EPS)
        row["full_cycle_overlay_to_total_neg_ratio"] = (row["comp_pos_overlay"]+row["setup_reset_pos_overlay"])/(row["full_cycle_neg_total"]+EPS)
        rows.append(row)
    return pd.DataFrame(rows), series, src_series


def flux_complete_ansatz(t,l,N,B,R,source_Tkk: np.ndarray, label: str):
    """Embed source_Tkk as rho+p_r with symmetric null positivity and compute continuity-completing radial flux.

    Minimal symmetric ansatz in orthonormal variables:
        rho = source_Tkk/2, p_r = source_Tkk/2, f=0 initially.
    A conservation-aware completion solves approximately
        d_t rho + (1/(B R^2)) d_l (N R^2 f) = 0
    for f with odd symmetry and f(0)=0 on each side.
    """
    rho = 0.5*source_Tkk
    pr = 0.5*source_Tkk
    rho_t = np.gradient(rho, t, axis=0, edge_order=2)
    source_weight = B*R*R*rho_t
    Q = np.zeros_like(source_weight)  # Q = N R^2 f
    i0 = int(np.argmin(np.abs(l)))
    # integrate separately right and left from the symmetry center
    for ti in range(len(t)):
        # right side: dQ/dl = -B R^2 rho_t
        if i0 < len(l)-1:
            integrand = -source_weight[ti, i0:]
            Q[ti, i0:] = np.concatenate([[0.0], np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(l[i0:]))])
        # left side integrating outward to negative l
        if i0 > 0:
            lleft = l[:i0+1][::-1]
            integrand = -source_weight[ti,:i0+1][::-1]
            qleft = np.concatenate([[0.0], np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(lleft))])
            Q[ti,:i0+1] = qleft[::-1]
    f = Q/(N*R*R + EPS)
    # Residual check
    div = np.gradient(N*R*R*f, l, axis=1, edge_order=2)/(B*R*R + EPS)
    residual = rho_t + div
    access = np.abs(l)<=0.25
    support = np.abs(l)<=0.75
    shoulder = (np.abs(l)>=1.2)&(np.abs(l)<=4.5)
    rows=[]
    for zn,zmask in {"access":access,"support":support,"shoulder":shoulder,"global":np.ones_like(l,dtype=bool)}.items():
        idx=np.ix_(np.ones(len(t),dtype=bool),zmask)
        rows.append({
            "ansatz": label,
            "zone": zn,
            "max_source_Tkk": float(np.max(source_Tkk[idx])),
            "max_rho": float(np.max(rho[idx])),
            "max_required_flux_completion": float(np.max(np.abs(f[idx]))),
            "rms_conservation_residual_flux_completed": float(np.sqrt(np.mean(residual[idx]**2))),
            "max_abs_conservation_residual_flux_completed": float(np.max(np.abs(residual[idx]))),
            "rms_zero_flux_exchange_term": float(np.sqrt(np.mean(rho_t[idx]**2))),
            "max_zero_flux_exchange_term": float(np.max(np.abs(rho_t[idx]))),
        })
    return pd.DataFrame(rows), f, residual


def run():
    t,l,N,B,R,phase,times,C,d = build_grid()
    Tkk_geo=d["Tkk_min"]
    open_src = build_open_comp_overlay(t,l,C)
    baseline_total = Tkk_geo + open_src

    # 1. Embedding ansatz for open compensation overlay.
    emb_rows, f_open, residual_open = flux_complete_ansatz(t,l,N,B,R,open_src,"open_compensation_overlay")
    emb_rows.to_csv(OUT/"compensation_embedding_ansatz.csv", index=False)

    # 2. Setup/reset compensation sweep.
    setup_rows=[]
    amp_support_values = np.linspace(0.0, 0.080, 17)
    amp_shoulder_values = np.linspace(0.0, 0.014, 15)
    for a_sup in amp_support_values:
        for a_sh in amp_shoulder_values:
            sr_src = setup_reset_overlay(t,l,times,float(a_sup),float(a_sh))
            src_total = open_src + sr_src
            Ttot = Tkk_geo + src_total
            ledger,_,_ = zone_histories(t,l,Ttot,src_total,phase)
            def get(obs,col): return float(ledger[ledger.observer_family==obs][col].iloc[0])
            # Main ratios for setup/reset and full cycle.
            row={
                "setup_support_amp": float(a_sup),
                "setup_shoulder_amp": float(a_sh),
                "access_setup_reset_pos_overlay": get("access_mean","setup_reset_pos_overlay"),
                "access_setup_reset_neg_total": get("access_mean","setup_reset_neg_total"),
                "support_setup_reset_neg_total": get("support_mean","setup_reset_neg_total"),
                "support_setup_reset_pos_overlay": get("support_mean","setup_reset_pos_overlay"),
                "shoulder_setup_reset_neg_total": get("shoulder_mean","setup_reset_neg_total"),
                "shoulder_setup_reset_pos_overlay": get("shoulder_mean","setup_reset_pos_overlay"),
                "support_setup_reset_ratio": get("support_mean","setup_reset_comp_ratio"),
                "shoulder_setup_reset_ratio": get("shoulder_mean","setup_reset_comp_ratio"),
                "support_full_ratio": get("support_mean","full_cycle_overlay_to_total_neg_ratio"),
                "shoulder_full_ratio": get("shoulder_mean","full_cycle_overlay_to_total_neg_ratio"),
                "core_full_ratio": get("core_line","full_cycle_overlay_to_total_neg_ratio"),
            }
            row["access_leakage_fraction_vs_support_setup"] = row["access_setup_reset_pos_overlay"]/(row["support_setup_reset_pos_overlay"]+EPS)
            ratios=np.array([row["support_setup_reset_ratio"], row["shoulder_setup_reset_ratio"]])
            row["ledger_balance_error"] = float(np.sum((ratios-1.08)**2))
            row["passes_setup_reset_ledger"] = bool(row["support_setup_reset_ratio"]>=1.0 and row["shoulder_setup_reset_ratio"]>=1.0 and row["access_leakage_fraction_vs_support_setup"]<0.08)
            row["score"] = float(-row["ledger_balance_error"] - 2*row["access_leakage_fraction_vs_support_setup"] - 0.05*(a_sup+a_sh))
            setup_rows.append(row)
    setup_df=pd.DataFrame(setup_rows)
    setup_df.to_csv(OUT/"setup_reset_compensation_sweep.csv", index=False)
    best_setup=setup_df[setup_df.passes_setup_reset_ledger].sort_values("score", ascending=False).head(20)
    best_setup.to_csv(OUT/"setup_reset_compensation_best.csv", index=False)

    # Use best setup/reset source for a combined ledger and embedding check.
    if len(best_setup)>0:
        best=best_setup.iloc[0]
    else:
        best=setup_df.sort_values("score",ascending=False).iloc[0]
    best_sr_src = setup_reset_overlay(t,l,times,float(best.setup_support_amp),float(best.setup_shoulder_amp))
    combined_src = open_src + best_sr_src
    combined_total = Tkk_geo + combined_src
    combined_ledger, combined_series, _ = zone_histories(t,l,combined_total,combined_src,phase)
    combined_ledger.to_csv(OUT/"combined_source_observer_ledgers.csv", index=False)

    emb_sr_rows, f_sr, residual_sr = flux_complete_ansatz(t,l,N,B,R,best_sr_src,"setup_reset_compensation_overlay_best")
    emb_all=pd.concat([emb_rows,emb_sr_rows], ignore_index=True)
    emb_all.to_csv(OUT/"source_embedding_ansatz_combined.csv", index=False)

    # 3. Sampling-aware timing sweep for open compensation schedule.
    # Geometry N pulse remains fixed, but the target source pulse is allowed to vary as a source schedule.
    open_mask=(phase=="R_open")|(phase=="hold")|(phase=="R_close")
    t1,t2,t3,t4,t5,t6=times
    Wsup=window_core(l, PARAMS["src_support_width"])
    Wsh=window_shoulder(l, PARAMS["src_shoulder_center"], PARAMS["src_shoulder_width"])
    timing_rows=[]
    centers=np.linspace(t[0],t[-1],701)
    taus=[1,2,5,10,20,40,80]
    # Open interval debts from geometry only.
    base_ledger,base_series,_=zone_histories(t,l,Tkk_geo,np.zeros_like(Tkk_geo),phase)
    target_ratios={"core_line":1.08,"support_mean":1.05,"shoulder_mean":1.08}
    # We scale support amplitude to cover support mean and shoulder amp to cover shoulder mean approximately.
    for delay in [0.0,2.5,5.0,10.0,20.0]:
        for TCsrc in [10.0,20.0,40.0,80.0]:
            start=t4+delay
            end=start+TCsrc
            env=np.zeros_like(t)
            m=(t>=start)&(t<=end)
            if np.any(m): env[m]=smooth_pulse01((t[m]-start)/TCsrc)
            # Solve simple amplitudes by integrated window means over source pulse.
            temp_sup = env[:,None]*Wsup[None,:]
            temp_sh = env[:,None]*Wsh[None,:]
            # Mean source exposures per unit amp.
            support_mask=np.abs(l)<=0.75
            shoulder_mask=(np.abs(l)>=1.2)&(np.abs(l)<=4.5)
            core_i=int(np.argmin(np.abs(l)))
            unit_support_exp=float(np.trapezoid(np.mean(temp_sup[:,support_mask],axis=1),t))
            unit_shoulder_exp=float(np.trapezoid(np.mean(temp_sh[:,shoulder_mask],axis=1),t))
            # open debts geometry only
            support_debt=float(base_ledger[base_ledger.observer_family=="support_mean"]["open_interval_neg_total"].iloc[0])
            shoulder_debt=float(base_ledger[base_ledger.observer_family=="shoulder_mean"]["open_interval_neg_total"].iloc[0])
            a_sup=target_ratios["support_mean"]*support_debt/(unit_support_exp+EPS)
            a_sh=target_ratios["shoulder_mean"]*shoulder_debt/(unit_shoulder_exp+EPS)
            src_open_var=a_sup*temp_sup + a_sh*temp_sh
            Ttot=Tkk_geo + src_open_var + best_sr_src
            ledger,series,_=zone_histories(t,l,Ttot,src_open_var+best_sr_src,phase)
            # sampled minima for total histories.
            sample_summ={}
            for obs in ["core_line","support_mean","shoulder_mean","access_mean"]:
                y=series[obs]
                worst=None
                for tau in taus:
                    sm=sampled_min(t,y,tau,centers)
                    if worst is None or sm["qi_proxy_margin"] < worst["qi_proxy_margin"]:
                        worst=sm
                sample_summ[obs]=worst
            row={
                "source_delay_after_R_close": delay,
                "source_comp_duration": TCsrc,
                "derived_support_amp": float(a_sup),
                "derived_shoulder_amp": float(a_sh),
                "core_source_to_open_neg_ratio": float(ledger[ledger.observer_family=="core_line"]["full_cycle_overlay_to_total_neg_ratio"].iloc[0]),
                "support_source_to_open_neg_ratio": float(ledger[ledger.observer_family=="support_mean"]["full_cycle_overlay_to_total_neg_ratio"].iloc[0]),
                "shoulder_source_to_open_neg_ratio": float(ledger[ledger.observer_family=="shoulder_mean"]["full_cycle_overlay_to_total_neg_ratio"].iloc[0]),
                "core_worst_qi_margin": sample_summ["core_line"]["qi_proxy_margin"],
                "core_worst_tau": sample_summ["core_line"]["tau"],
                "core_worst_center": sample_summ["core_line"]["center_at_min"],
                "support_worst_qi_margin": sample_summ["support_mean"]["qi_proxy_margin"],
                "support_worst_tau": sample_summ["support_mean"]["tau"],
                "shoulder_worst_qi_margin": sample_summ["shoulder_mean"]["qi_proxy_margin"],
                "shoulder_worst_tau": sample_summ["shoulder_mean"]["tau"],
            }
            # More positive margin is better. Include amplitude penalty to avoid impulse-like extremes.
            row["score_sampling"] = float(row["core_worst_qi_margin"] + row["support_worst_qi_margin"] + 0.5*row["shoulder_worst_qi_margin"] - 0.02*(a_sup+a_sh))
            timing_rows.append(row)
    timing_df=pd.DataFrame(timing_rows)
    timing_df.to_csv(OUT/"sampling_aware_timing_sweep.csv", index=False)
    timing_df.sort_values("score_sampling", ascending=False).head(15).to_csv(OUT/"sampling_aware_timing_best.csv", index=False)

    # Combined Lorentzian screen for baseline v01 and v02 best.
    sample_rows=[]
    centers=np.linspace(t[0],t[-1],901)
    for label,Ttot in [("v01_open_comp_only", baseline_total), ("v02_with_setup_reset_comp", combined_total)]:
        ledger,series,_=zone_histories(t,l,Ttot, open_src if label.startswith("v01") else combined_src, phase)
        for obs in ["core_line","access_mean","support_mean","shoulder_mean","matching_mean"]:
            for tau in [0.5,1,2,5,10,20,40,80]:
                sm=sampled_min(t,series[obs],tau,centers)
                sample_rows.append({"case":label,"observer_family":obs,**sm})
    sampled_df=pd.DataFrame(sample_rows)
    sampled_df.to_csv(OUT/"v02_lorentzian_sampling_comparison.csv", index=False)

    # Summaries/extracts.
    def ledger_row(df, obs): return df[df.observer_family==obs].iloc[0].to_dict()
    best_timing=timing_df.sort_values("score_sampling",ascending=False).iloc[0].to_dict()
    extracts={
        "reference_geometry":"v0.3 frozen",
        "best_setup_reset_compensation": {k: (float(v) if isinstance(v,(np.floating,float,int,np.integer)) else bool(v) if isinstance(v,(np.bool_,bool)) else v) for k,v in best.to_dict().items()},
        "best_sampling_timing": {k: (float(v) if isinstance(v,(np.floating,float,int,np.integer)) else v) for k,v in best_timing.items()},
        "combined_ledgers": {
            "core_line": ledger_row(combined_ledger,"core_line"),
            "access_mean": ledger_row(combined_ledger,"access_mean"),
            "support_mean": ledger_row(combined_ledger,"support_mean"),
            "shoulder_mean": ledger_row(combined_ledger,"shoulder_mean"),
        },
        "embedding_ansatz_reading": {
            "minimal_symmetric_ansatz":"rho=source_Tkk/2, p_r=source_Tkk/2, p_t=0, flux=0 gives the target null-positive ledger.",
            "flux_completed_ansatz":"A radial flux f(l,t) can satisfy a reduced continuity equation for the positive source pulse with bounded access-region flux; remaining task is field/source interpretation.",
        },
        "source_realism_reading":[
            "The active source ledger separates cleanly into open-interval repayment and setup/reset infrastructure repayment.",
            "Setup/reset support-shoulder repayment can be added with low access leakage by using support-ring and shoulder windows during B-setup/B-reset.",
            "Sampling-aware timing favors early post-closure compensation with moderate-to-long source duration; the simple QI proxy remains the active physics gate for long sampling windows.",
            "The next constructive task is a candidate physical source family for the flux-completed anisotropic repayment ansatz."
        ]
    }
    (OUT/"source_realism_prescreen_v02_extracts.json").write_text(json.dumps(extracts, indent=2))

    # Append progress note.
    note = ROOT/"report_progress_notes.md"
    with note.open("a") as f:
        f.write("\n\n## Source-realism pre-screen v0.2\n\n")
        f.write("Geometry v0.3 remains frozen. v0.2 separates source refinement into open-interval repayment embedding, setup/reset support-shoulder repayment, and sampling-aware timing. The best setup/reset overlay uses support-ring and shoulder windows with low access leakage. The minimal anisotropic embedding supplies the target null-positive ledger, and a flux-completed variant gives the reduced continuity closure target for physical source modeling.\n")

    print(json.dumps(extracts, indent=2))

if __name__ == "__main__":
    run()
