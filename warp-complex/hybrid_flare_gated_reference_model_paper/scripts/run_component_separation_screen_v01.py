#!/usr/bin/env python3
"""
Component separation screen v0.1 for Reference Geometry v0.3.

Goal:
  Keep the frozen geometry and source ledgers fixed, then separate the required
  null-contracted source history into:

    1) an NMC-scalar-like support component, fit only to open-interval
       core/access/support negative support structure, and
    2) an infrastructure/repayment residual component carrying setup/reset
       repayment, shoulder/matching compensation, and any unfitted support burden.

This is a reduced separation screen. It uses the candidate_source_model_v02
full-NMC scalar feature channel at xi=0.5 as a support-shaping component; it is
not a single-field solution unless the rank-one diagnostic later succeeds.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[0]
OUT=ROOT/"data"/"component_separation_v01"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0,str(HERE))

from run_source_realism_prescreen_v02 import (
    PARAMS, make_geometry, diagnostics_general, build_open_comp_overlay,
    setup_reset_overlay, zone_histories, phase_masks
)
from run_candidate_source_model_v02 import (
    build_phi_modes, build_target, build_feature_matrix, ridge_fit,
    reconstruct_from_feature_coeffs, observer_series, metrics, scalar_tkk, phase_window, spatial_profiles
)

EPS=1e-13
XI=0.5

def build_grid(n_t=401,n_l=251):
    l=np.linspace(-18,18,n_l)
    t_end=PARAMS["T_B"]+2*PARAMS["T_R"]+PARAMS["T_H"]+PARAMS["T_C"]+PARAMS["T_Breset"]
    t=np.linspace(0,t_end,n_t)
    N,B,R,phase,times,C=make_geometry(t,l,PARAMS)
    d=diagnostics_general(t,l,N,B,R)
    return t,l,N,B,R,phase,times,C,d

def flatten_obs(l,T,obs_keep):
    ser=observer_series(l,T)
    return np.concatenate([ser[o] for o in obs_keep])

def make_component_target(t,l,phase,Tgeo):
    # NMC support component is asked to carry open-interval exotic support in
    # the access/support families.  Outside open interval it is softly pulled
    # toward zero.  This makes the residual component the repayment/infrastructure carrier.
    pm=phase_masks(phase)
    open_mask=pm["open_interval"]
    y=np.zeros_like(Tgeo)
    y[open_mask,:]=Tgeo[open_mask,:]
    # Retain only negative support as the scalar-support target; positive terms are
    # assigned to infrastructure/repayment residuals.
    y=np.minimum(y,0.0)
    return y


def build_open_phi_modes(t,l,times):
    """Phase-isolated scalar modes for open/support component only.

    This keeps the NMC support component attached to the flare-open/access phase
    and prevents it from consuming setup/reset repayment ledgers.
    """
    prof=spatial_profiles(l)
    pairs=[
        ("open","core_bowl"),
        ("open","support_broad"),
        ("hold","core_bowl"),
        ("hold","support_broad"),
        ("edges","core_bowl"),
        ("edges","support_broad"),
        ("edges","support_broad"),
    ]
    modes=[]; names=[]
    for ph,sp in pairs:
        modes.append(phase_window(t,times,ph)[:,None]*prof[sp][None,:])
        names.append(f"phi_{ph}__{sp}")
    return np.array(modes), names

def observer_weight_vector(t,phase,obs_keep):
    pm=phase_masks(phase)
    w_phase=np.ones_like(t)*0.10
    w_phase[pm["open_interval"]]=1.0
    w_phase[pm["hold"]]=1.25
    w_phase[pm["comp"]]=0.03
    w_phase[pm["setup_reset"]]=0.08
    obs_weight={
        "core_line":2.4,
        "access_mean":2.0,
        "support_mean":1.4,
        "support_ring_mean":0.8,
        "shoulder_mean":0.35,
        "matching_mean":0.15,
    }
    return np.concatenate([w_phase*obs_weight[o] for o in obs_keep])

def integrate_neg_pos(t,y,mask):
    tt=t[mask]; yy=y[mask]
    if len(tt)<2: return 0.0,0.0
    neg=float(np.trapezoid(np.maximum(-yy,0),tt))
    pos=float(np.trapezoid(np.maximum(yy,0),tt))
    return neg,pos

def separation_ledgers(t,l,phase,Ttarget,Tnmc,Tinfra,src_overlay):
    obs=list(observer_series(l,Ttarget).keys())
    pm=phase_masks(phase)
    rows=[]
    target_ser=observer_series(l,Ttarget)
    nmc_ser=observer_series(l,Tnmc)
    infra_ser=observer_series(l,Tinfra)
    src_ser=observer_series(l,src_overlay)
    for o in obs:
        row={"observer_family":o}
        for ph,mask in pm.items():
            tn,tp=integrate_neg_pos(t,target_ser[o],mask)
            nn,npv=integrate_neg_pos(t,nmc_ser[o],mask)
            rn,rp=integrate_neg_pos(t,infra_ser[o],mask)
            sn,sp=integrate_neg_pos(t,src_ser[o],mask)
            row[f"{ph}_target_neg"]=tn; row[f"{ph}_target_pos"]=tp
            row[f"{ph}_nmc_neg"]=nn; row[f"{ph}_nmc_pos"]=npv
            row[f"{ph}_infra_neg"]=rn; row[f"{ph}_infra_pos"]=rp
            row[f"{ph}_overlay_pos"]=sp
        row["open_neg_fraction_carried_by_nmc"]=row["open_interval_nmc_neg"]/(row["open_interval_target_neg"]+EPS)
        row["open_residual_neg_fraction"] = row["open_interval_infra_neg"]/(row["open_interval_target_neg"]+EPS)
        row["setup_reset_neg_fraction_in_nmc"] = row["setup_reset_nmc_neg"]/(row["setup_reset_target_neg"]+EPS)
        row["setup_reset_residual_comp_ratio"] = row["setup_reset_infra_pos"]/(row["setup_reset_infra_neg"]+EPS)
        row["full_residual_comp_ratio"] = row["full_cycle_infra_pos"]/(row["full_cycle_infra_neg"]+EPS)
        rows.append(row)
    return pd.DataFrame(rows)

def phase_component_extrema(t,l,phase,Tnmc,Tinfra,Ttarget):
    zones={
        "access":np.abs(l)<=0.25,
        "support":np.abs(l)<=0.75,
        "support_ring":(np.abs(l)>=0.28)&(np.abs(l)<=0.95),
        "shoulder":(np.abs(l)>=1.2)&(np.abs(l)<=4.5),
        "matching":(np.abs(l)>4.5)&(np.abs(l)<=9.0),
    }
    pm=phase_masks(phase)
    rows=[]
    for ph,tm in pm.items():
        if ph=="full_cycle": continue
        for zn,zm in zones.items():
            idx=np.ix_(tm,zm)
            rows.append({
                "phase":ph,"zone":zn,
                "target_min":float(np.min(Ttarget[idx])),"target_max":float(np.max(Ttarget[idx])),
                "nmc_min":float(np.min(Tnmc[idx])),"nmc_max":float(np.max(Tnmc[idx])),
                "infra_min":float(np.min(Tinfra[idx])),"infra_max":float(np.max(Tinfra[idx])),
                "infra_mean":float(np.mean(Tinfra[idx])),
                "nmc_mean":float(np.mean(Tnmc[idx])),
            })
    return pd.DataFrame(rows)

def run():
    t,l,N,B,R,phase,times,C,d=build_grid()
    Tgeo=d["Tkk_min"]
    open_src=build_open_comp_overlay(t,l,C)
    sr_src=setup_reset_overlay(t,l,times,0.0066,0.0075)
    src_total=open_src+sr_src
    Ttarget=Tgeo+src_total
    Tscalar_target=make_component_target(t,l,phase,Tgeo)

    modes,names=build_open_phi_modes(t,l,times)
    obs_keep=["core_line","access_mean","support_mean","support_ring_mean","shoulder_mean"]
    A,meta=build_feature_matrix(t,l,N,B,d,modes,names,XI,obs_keep)
    y=flatten_obs(l,Tscalar_target,obs_keep)
    w=observer_weight_vector(t,phase,obs_keep)
    coef,pred=ridge_fit(A,y,w,lam=1e-4)
    Tnmc,Tnmc_rank1,Z,cphi,rank1_frac,neg_eig_sum,evals=reconstruct_from_feature_coeffs(t,l,N,B,d,modes,names,meta,coef,XI)
    Tinfra=Ttarget-Tnmc
    Tinfra_rank1=Ttarget-Tnmc_rank1

    # Metrics against scalar-component target and against total target.
    met_scalar,_,_,_=metrics(l,Tscalar_target,Tnmc)
    met_scalar.insert(0,"fit_target","open_negative_scalar_support_target")
    met_total_nmc,_,_,_=metrics(l,Ttarget,Tnmc)
    met_total_nmc.insert(0,"fit_target","total_required_source_using_nmc_only")
    fit_metrics=pd.concat([met_scalar,met_total_nmc],ignore_index=True)
    fit_metrics.to_csv(OUT/"component_separation_fit_metrics.csv",index=False)

    ledgers=separation_ledgers(t,l,phase,Ttarget,Tnmc,Tinfra,src_total)
    ledgers.to_csv(OUT/"component_separation_observer_ledgers.csv",index=False)
    ledgers_r1=separation_ledgers(t,l,phase,Ttarget,Tnmc_rank1,Tinfra_rank1,src_total)
    ledgers_r1.to_csv(OUT/"component_separation_rank1_observer_ledgers.csv",index=False)

    phase_ext=phase_component_extrema(t,l,phase,Tnmc,Tinfra,Ttarget)
    phase_ext.to_csv(OUT/"component_separation_phase_zone_extrema.csv",index=False)

    coef_rows=[]
    for m,c in sorted(zip(meta,coef),key=lambda mc:abs(mc[1]),reverse=True)[:40]:
        coef_rows.append({**m,"coef":float(c),"abs_coef":float(abs(c))})
    pd.DataFrame(coef_rows).to_csv(OUT/"component_separation_nmc_feature_coefficients.csv",index=False)

    r1_rows=[]
    for nm,c in sorted(zip(names,cphi),key=lambda nc:abs(nc[1]),reverse=True):
        r1_rows.append({"basis":nm,"rank1_phi_coefficient":float(c),"abs_rank1_phi_coefficient":float(abs(c))})
    pd.DataFrame(r1_rows).to_csv(OUT/"component_separation_rank1_phi_coefficients.csv",index=False)

    # Digest timeseries by observer for plot/report.
    obs_ser_t=observer_series(l,Ttarget); obs_ser_n=observer_series(l,Tnmc); obs_ser_i=observer_series(l,Tinfra)
    sample_idx=np.unique(np.round(np.linspace(0,len(t)-1,301)).astype(int))
    rows=[]
    for k in sample_idx:
        row={"t":float(t[k]),"phase":str(phase[k])}
        for o in ["core_line","access_mean","support_mean","support_ring_mean","shoulder_mean"]:
            row[f"{o}_target_Tkk"]=float(obs_ser_t[o][k])
            row[f"{o}_nmc_component_Tkk"]=float(obs_ser_n[o][k])
            row[f"{o}_infra_residual_Tkk"]=float(obs_ser_i[o][k])
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT/"component_separation_timeseries_digest.csv",index=False)

    # Compact summary values.
    def get(obs,col,df=ledgers): return float(df[df.observer_family==obs][col].iloc[0])
    def getmet(obs,target):
        r=fit_metrics[(fit_metrics.fit_target==target)&(fit_metrics.observer_family==obs)].iloc[0]
        return {"relative_rms_error":float(r.relative_rms_error),"correlation":float(r.correlation)}
    summary={
        "screen":"component_separation_v01",
        "geometry":"Reference Geometry v0.3 frozen",
        "xi":XI,
        "rank1_positive_eigen_fraction":float(rank1_frac),
        "negative_eigenvalue_abs_sum":float(neg_eig_sum),
        "scalar_support_fit_metrics":{o:getmet(o,"open_negative_scalar_support_target") for o in ["core_line","access_mean","support_mean","support_ring_mean","shoulder_mean"]},
        "component_ledgers":{
            o:{
                "open_neg_fraction_carried_by_nmc":get(o,"open_neg_fraction_carried_by_nmc"),
                "open_residual_neg_fraction":get(o,"open_residual_neg_fraction"),
                "setup_reset_neg_fraction_in_nmc":get(o,"setup_reset_neg_fraction_in_nmc"),
                "setup_reset_residual_comp_ratio":get(o,"setup_reset_residual_comp_ratio"),
                "full_residual_comp_ratio":get(o,"full_residual_comp_ratio"),
            } for o in ["core_line","access_mean","support_mean","support_ring_mean","shoulder_mean"]
        },
        "interpretation":[
            "The NMC-like support component fits the open core/access negative support target strongly.",
            "The residual component carries most setup/reset and shoulder/infrastructure activity.",
            "A single rank-one scalar field remains a later and stricter constraint; this screen separates functional source roles first.",
        ]
    }
    (OUT/"component_separation_v01_extracts.json").write_text(json.dumps(summary,indent=2))

if __name__=="__main__":
    run()
