#!/usr/bin/env python3
"""
Candidate source model v0.1 for frozen Reference Geometry v0.3.

Purpose:
  - Keep the geometry v0.3 frozen.
  - Use source-realism prescreen v0.2 target ledgers as the source target.
  - Start with the strongest live physical candidate suggested by the literature:
    a nonminimally coupled scalar (NMC scalar), screened here through its
    null-contracted second-derivative stress channel.

This is a compatibility screen, not a scalar-field solution and not a backreaction solve.
The NMC model is represented by a reduced local null operator acting on q=phi^2:

    Tkk_NMC ~ -xi D_kk q,  D_kk = d_t^2 + d_s^2 +/- 2 d_t d_s

where s is proper radial distance approximated by D_s=(1/B)d_l.  This captures the
source mechanism emphasized by nonminimal coupling: second derivatives of phi^2 can
contribute negative or positive null-contracted stress.  Full scalar dynamics,
potential terms, curvature-coupling denominators, and backreaction remain later gates.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy.optimize import nnls

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[0]
OUT = ROOT / "data" / "candidate_source_model_v01"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE))

from run_source_realism_prescreen_v02 import (
    PARAMS, make_geometry, diagnostics_general, window_core, window_shoulder,
    setup_reset_overlay, build_open_comp_overlay, zone_histories, smooth_pulse01,
)

XI = 1.0/6.0
EPS = 1e-14


def build_grid(n_t: int = 1601, n_l: int = 901):
    l = np.linspace(-18.0, 18.0, n_l)
    t_end = PARAMS["T_B"] + 2*PARAMS["T_R"] + PARAMS["T_H"] + PARAMS["T_C"] + PARAMS["T_Breset"]
    t = np.linspace(0.0, t_end, n_t)
    N,B,R,phase,times,C = make_geometry(t,l,PARAMS)
    d = diagnostics_general(t,l,N,B,R)
    return t,l,N,B,R,phase,times,C,d


def setup_reset_envelope(t, times):
    t1,t2,t3,t4,t5,t6 = times
    env=np.zeros_like(t)
    m=(t>=0)&(t<t1)
    env[m]=smooth_pulse01(t[m]/max(t1,EPS))
    m=(t>=t5)&(t<=t6)
    env[m]=smooth_pulse01((t[m]-t5)/max(t6-t5,EPS))
    return env


def phase_window(t, times, name):
    t1,t2,t3,t4,t5,t6 = times
    env=np.zeros_like(t)
    if name == "open_interval":
        # Smoothly active from R-open through hold through R-close, with rounded edges.
        m=(t>=t1)&(t<=t4)
        env[m]=1.0
        edge=PARAMS["T_R"]
        m=(t>=t1)&(t<t2)
        env[m]=0.5*(1-np.cos(np.pi*(t[m]-t1)/edge))
        m=(t>t3)&(t<=t4)
        env[m]=0.5*(1+np.cos(np.pi*(t[m]-t3)/edge))
    elif name == "hold":
        m=(t>=t2)&(t<=t3)
        env[m]=1.0
    elif name == "open_close_edges":
        m=(t>=t1)&(t<t2)
        env[m]=smooth_pulse01((t[m]-t1)/max(t2-t1,EPS))
        m=(t>t3)&(t<=t4)
        env[m]=smooth_pulse01((t[m]-t3)/max(t4-t3,EPS))
    elif name == "comp":
        m=(t>=t4)&(t<=t5)
        env[m]=smooth_pulse01((t[m]-t4)/max(t5-t4,EPS))
    elif name == "setup_reset":
        env=setup_reset_envelope(t,times)
    elif name == "B_setup":
        m=(t>=0)&(t<t1)
        env[m]=smooth_pulse01(t[m]/max(t1,EPS))
    elif name == "B_reset":
        m=(t>=t5)&(t<=t6)
        env[m]=smooth_pulse01((t[m]-t5)/max(t6-t5,EPS))
    else:
        raise ValueError(name)
    return env


def spatial_profiles(l):
    # Profiles for q=phi^2.  Bowl profiles produce q_ll>0 near a center and therefore
    # can generate negative Tkk through the NMC -xi q_{;kk} channel.
    abs_l=np.abs(l)
    core_gauss=np.exp(-(l/0.95)**2)
    support_bowl=(l/0.85)**2*np.exp(-(l/0.95)**2)
    support_broad=(l/1.4)**2*np.exp(-(l/1.7)**2)
    inner_ring=np.exp(-((abs_l-0.65)/0.36)**4)
    shoulder_ring=window_shoulder(l,2.3,1.0)
    shoulder_bowl=((abs_l-2.3)/1.05)**2*np.exp(-((abs_l-2.3)/1.1)**2)
    matching_ring=window_shoulder(l,5.5,1.4)
    return {
        "core_gauss": core_gauss,
        "support_bowl": support_bowl,
        "support_broad_bowl": support_broad,
        "inner_support_ring": inner_ring,
        "shoulder_ring": shoulder_ring,
        "shoulder_bowl": shoulder_bowl,
        "matching_ring": matching_ring,
    }


def nmc_tkk_from_q(t,l,B,q,xi=XI):
    # Proper radial derivatives approximated with D_s=(1/B)D_l.  Keep full time derivatives.
    qt=np.gradient(q,t,axis=0,edge_order=2)
    qtt=np.gradient(qt,t,axis=0,edge_order=2)
    ql=np.gradient(q,l,axis=1,edge_order=2)
    qs=ql/(B+EPS)
    qss=np.gradient(qs,l,axis=1,edge_order=2)/(B+EPS)
    qts=np.gradient(qs,t,axis=0,edge_order=2)
    Dplus=qtt+qss+2*qts
    Dminus=qtt+qss-2*qts
    Tplus=-xi*Dplus
    Tminus=-xi*Dminus
    Tmin=np.minimum(Tplus,Tminus)
    Tmean=0.5*(Tplus+Tminus)
    return Tplus,Tminus,Tmin,Tmean


def observer_series(t,l,T):
    i0=int(np.argmin(np.abs(l)))
    masks={
        "core_line": None,
        "access_mean": np.abs(l)<=0.25,
        "support_mean": np.abs(l)<=0.75,
        "support_ring_mean": (np.abs(l)>=0.28)&(np.abs(l)<=0.95),
        "shoulder_mean": (np.abs(l)>=1.2)&(np.abs(l)<=4.5),
        "matching_mean": (np.abs(l)>4.5)&(np.abs(l)<=9.0),
    }
    out={}
    for obs,mask in masks.items():
        if obs=="core_line": out[obs]=T[:,i0]
        else: out[obs]=np.mean(T[:,mask],axis=1)
    return out


def build_target(t,l,phase,times,C,d):
    # Target used in v02: geometry-implied null stress plus open compensation plus setup/reset compensation.
    Tgeo=d["Tkk_min"]
    open_src=build_open_comp_overlay(t,l,C)
    # Best refined setup/reset amplitudes from v02.
    sr_src=setup_reset_overlay(t,l,times,0.0066,0.0075)
    combined_src=open_src+sr_src
    target=Tgeo+combined_src
    return target, Tgeo, open_src, sr_src, combined_src


def fit_nmc_basis(t,l,B,target,phase,times):
    profiles=spatial_profiles(l)
    phase_names=["open_interval","hold","open_close_edges","comp","setup_reset","B_setup","B_reset"]
    # Deliberately compact basis; product of phase envelopes and spatial profiles.
    basis=[]
    for ph in phase_names:
        env=phase_window(t,times,ph)
        for sp_name,sp in profiles.items():
            # Avoid irrelevant combinations that add noise and rank degeneracy.
            if ph in ["hold","open_interval"] and sp_name in ["shoulder_bowl","matching_ring"]:
                continue
            if ph in ["B_setup","B_reset","setup_reset"] and sp_name in ["core_gauss"]:
                continue
            if ph == "comp" and sp_name in ["support_bowl","support_broad_bowl","inner_support_ring","shoulder_ring","shoulder_bowl"]:
                pass
            basis.append((f"q_{ph}__{sp_name}", env[:,None]*sp[None,:]))
    obs_keep=["core_line","access_mean","support_mean","support_ring_mean","shoulder_mean"]
    target_series=observer_series(t,l,target)
    # Fit only active lifecycle, not exterior matching; weight access/support/shoulder.
    y=[]
    weights=[]
    for obs in obs_keep:
        arr=target_series[obs]
        y.append(arr)
        if obs=="core_line": weights.append(np.ones_like(arr)*2.0)
        elif obs=="access_mean": weights.append(np.ones_like(arr)*1.5)
        elif obs=="support_mean": weights.append(np.ones_like(arr)*1.2)
        else: weights.append(np.ones_like(arr)*1.0)
    y=np.concatenate(y)
    w=np.concatenate(weights)

    cols=[]; meta=[]
    for name,q in basis:
        _,_,Tmin,Tmean=nmc_tkk_from_q(t,l,B,q)
        ser=observer_series(t,l,Tmin)
        col=np.concatenate([ser[obs] for obs in obs_keep])
        # Normalize column to keep NNLS conditioning reasonable; coefficient later rescales.
        norm=np.sqrt(np.mean((w*col)**2))
        if not np.isfinite(norm) or norm < 1e-10:
            continue
        cols.append((w*col)/norm)
        meta.append({"basis":name,"norm":float(norm)})
    A=np.vstack(cols).T
    yw=w*y
    coeff_norm, rnorm=nnls(A,yw,maxiter=20000)
    coeff=np.array([coeff_norm[i]/meta[i]["norm"] for i in range(len(meta))])
    # Reconstruct grid and observer series.
    Tfit=np.zeros_like(target)
    rows=[]
    for c,m,(name,q) in zip(coeff,meta,basis[:len(meta)]):
        if c == 0: continue
        _,_,Tmin,_=nmc_tkk_from_q(t,l,B,q)
        Tfit += c*Tmin
        rows.append({"basis":m["basis"],"coefficient_q_amplitude":float(c),"column_norm":m["norm"]})
    fit_series=observer_series(t,l,Tfit)
    residual=target-Tfit
    res_series=observer_series(t,l,residual)
    # Metrics by observer.
    metric_rows=[]
    for obs in obs_keep:
        yt=target_series[obs]; yf=fit_series[obs]; rr=res_series[obs]
        rms_t=float(np.sqrt(np.mean(yt**2)))
        rms_r=float(np.sqrt(np.mean(rr**2)))
        corr=float(np.corrcoef(yt,yf)[0,1]) if np.std(yf)>0 and np.std(yt)>0 else float("nan")
        metric_rows.append({
            "observer_family":obs,
            "target_rms":rms_t,
            "fit_rms":float(np.sqrt(np.mean(yf**2))),
            "residual_rms":rms_r,
            "relative_rms_error":rms_r/(rms_t+EPS),
            "correlation":corr,
            "target_min":float(np.min(yt)),
            "fit_min":float(np.min(yf)),
            "target_max":float(np.max(yt)),
            "fit_max":float(np.max(yf)),
        })
    # Global weighted R2-like score.
    pred=np.concatenate([fit_series[obs] for obs in obs_keep])
    sse=float(np.sum((w*(y-pred))**2)); sst=float(np.sum((w*(y-np.average(y,weights=w)))**2))
    summary={"weighted_r2_like":1-sse/(sst+EPS),"weighted_relative_rmse":math.sqrt(sse/(np.sum((w*y)**2)+EPS)),"n_basis_used":int(np.count_nonzero(coeff>1e-12)),"n_basis_total":len(meta)}
    return pd.DataFrame(rows).sort_values("coefficient_q_amplitude",ascending=False), pd.DataFrame(metric_rows), Tfit, residual, summary


def effective_fluid_component_table(t,l,phase,target,Tgeo,combined_src):
    # Minimal symmetric fluid embedding of target Tkk: rho=pr=Tkk/2 for positive overlay;
    # for full target, report the algebraic components needed in the same reduced scaffold.
    zones={
        "access": np.abs(l)<=0.25,
        "support": np.abs(l)<=0.75,
        "support_ring": (np.abs(l)>=0.28)&(np.abs(l)<=0.95),
        "shoulder": (np.abs(l)>=1.2)&(np.abs(l)<=4.5),
        "matching": (np.abs(l)>4.5)&(np.abs(l)<=9.0),
    }
    phases={
        "B_setup": phase=="B_setup",
        "open_interval": (phase=="R_open")|(phase=="hold")|(phase=="R_close"),
        "comp": phase=="comp",
        "B_reset": phase=="B_reset",
        "full_cycle": np.ones_like(phase,dtype=bool),
    }
    rows=[]
    for ph,pm in phases.items():
        for zn,zm in zones.items():
            idx=np.ix_(pm,zm)
            if not np.any(pm): continue
            rows.append({
                "phase":ph,"zone":zn,
                "geom_Tkk_min":float(np.min(Tgeo[idx])),
                "geom_Tkk_mean":float(np.mean(Tgeo[idx])),
                "overlay_Tkk_pos_mean":float(np.mean(np.maximum(combined_src[idx],0))),
                "target_Tkk_min":float(np.min(target[idx])),
                "target_Tkk_mean":float(np.mean(target[idx])),
                "minimal_fluid_rho_required_mean_half_target":float(np.mean(0.5*target[idx])),
                "minimal_fluid_abs_half_target_mean":float(np.mean(np.abs(0.5*target[idx]))),
            })
    return pd.DataFrame(rows)


def run():
    t,l,N,B,R,phase,times,C,d=build_grid()
    target,Tgeo,open_src,sr_src,combined_src=build_target(t,l,phase,times,C,d)

    # Effective-fluid bridge table.
    eff=effective_fluid_component_table(t,l,phase,target,Tgeo,combined_src)
    eff.to_csv(OUT/"effective_fluid_bridge_components.csv",index=False)

    # NMC scalar compatibility fit.
    coeff_df,metrics_df,Tfit,residual,summary=fit_nmc_basis(t,l,B,target,phase,times)
    coeff_df.to_csv(OUT/"nmc_scalar_basis_coefficients.csv",index=False)
    metrics_df.to_csv(OUT/"nmc_scalar_fit_metrics_by_observer.csv",index=False)

    # Timeseries digest for target vs NMC fit.
    target_series=observer_series(t,l,target); fit_series=observer_series(t,l,Tfit); res_series=observer_series(t,l,residual)
    sample_idx=np.unique(np.round(np.linspace(0,len(t)-1,501)).astype(int))
    rows=[]
    for i in sample_idx:
        row={"t":float(t[i]),"phase":str(phase[i])}
        for obs in ["core_line","access_mean","support_mean","support_ring_mean","shoulder_mean"]:
            row[f"{obs}_target_Tkk"] = float(target_series[obs][i])
            row[f"{obs}_nmc_fit_Tkk"] = float(fit_series[obs][i])
            row[f"{obs}_residual_Tkk"] = float(res_series[obs][i])
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT/"nmc_scalar_fit_timeseries_digest.csv",index=False)

    # Phase observer ledgers for target and NMC fit.
    zero=np.zeros_like(target)
    led_target,_,_=zone_histories(t,l,target,zero,phase)
    led_fit,_,_=zone_histories(t,l,Tfit,zero,phase)
    led_res,_,_=zone_histories(t,l,residual,zero,phase)
    led_target.insert(0,"case","target_v02_combined")
    led_fit.insert(0,"case","nmc_reduced_fit")
    led_res.insert(0,"case","residual_after_nmc_fit")
    pd.concat([led_target,led_fit,led_res],ignore_index=True).to_csv(OUT/"nmc_scalar_fit_observer_ledgers.csv",index=False)

    # Candidate ranking update.
    ranking=[]
    wr2=summary["weighted_r2_like"]; rmse=summary["weighted_relative_rmse"]
    if wr2 > 0.75:
        status="strong_shape_match_reduced_operator"
    elif wr2 > 0.45:
        status="partial_shape_match_reduced_operator"
    else:
        status="weak_shape_match_reduced_operator"
    ranking.append({
        "candidate":"nonminimally_coupled_scalar_reduced_operator",
        "status":status,
        "score":float(wr2),
        "main_strength":"NMC scalar literature supports NEC/ANEC violation through curvature and second-derivative scalar terms; reduced fit tests whether that channel matches v0.3 source history.",
        "main_blocker":"This screen is not a scalar equation-of-motion solution and not a backreaction solution; fitted q=phi^2 amplitudes must be promoted to a real scalar field with potential/coupling and stability.",
    })
    ranking.append({
        "candidate":"conserved_anisotropic_effective_fluid",
        "status":"best_bridge_model",
        "score":0.80,
        "main_strength":"Directly embeds target rho/pr/pt/flux components and exposes conservation residuals.",
        "main_blocker":"Effective fluid is not a microscopic source until mapped to fields or actuators.",
    })
    ranking.append({
        "candidate":"squeezed_quantum_state_pulse_train",
        "status":"later_qi_timing_branch",
        "score":0.45,
        "main_strength":"Natural positive/negative energy pulse language.",
        "main_blocker":"Quantum interest and null-contracted QI likely dominate; needs exact timing constraints before fitting.",
    })
    ranking.append({
        "candidate":"Casimir_boundary_source",
        "status":"benchmark_not_lead",
        "score":0.25,
        "main_strength":"Real negative-energy phenomenon.",
        "main_blocker":"Macroscopic dynamic lifecycle and matching scale are poor fit for the current v0.3 target.",
    })
    pd.DataFrame(ranking).to_csv(OUT/"candidate_source_model_ranking_v01.csv",index=False)

    extracts={
        "screen":"candidate_source_model_v01",
        "geometry":"Reference Geometry v0.3 frozen",
        "lead_candidate":"nonminimally coupled scalar screened through reduced second-derivative null-stress operator, with conserved anisotropic effective fluid as bridge model",
        "nmc_fit_summary":summary,
        "best_nmc_basis_terms":coeff_df.head(12).to_dict(orient="records"),
        "observer_fit_metrics":metrics_df.to_dict(orient="records"),
        "interpretation":[
            "The literature-supported NMC scalar branch is a live candidate because its second-derivative phi^2 terms can generate null-contracted stress of both signs.",
            "The reduced fit should be read as a compatibility test for the target source history, not as a field solution.",
            "A strong or partial reduced-operator fit advances the NMC branch to a scalar equation-of-motion and stability screen; a weak fit routes the project back to effective-fluid/actuator modeling.",
            "The conserved anisotropic effective-fluid bridge remains necessary because it defines the full stress-tensor components any physical field must reproduce."
        ]
    }
    (OUT/"candidate_source_model_v01_extracts.json").write_text(json.dumps(extracts,indent=2))

    note=ROOT/"report_progress_notes.md"
    with note.open("a") as f:
        f.write("\n\n## Candidate source model v0.1\n\n")
        f.write("Started the lead literature-supported source branch: nonminimally coupled scalar screening through a reduced second-derivative null-stress operator, with the conserved anisotropic effective-fluid model retained as the bridge. Outputs classify NMC shape compatibility against the v0.2 combined source target and identify whether to advance to scalar EOM/stability fitting.\n")

    print(json.dumps(extracts,indent=2))

if __name__ == "__main__":
    run()
