#!/usr/bin/env python3
"""
Hybrid source closure v0.1.

Keeps Reference Geometry v0.3 frozen and tests whether the leading hybrid
source architecture can be represented as a reduced anisotropic source with
bounded, localized conservation-completing radial fluxes.

Architecture:
    T_total = T_NMC_support + T_infrastructure_repayment/matching

This is a closure and consistency screen, not a field-equation solve.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[0]
OUT=ROOT/'data'/'hybrid_source_closure_v01'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0,str(HERE))

from run_source_realism_prescreen_v02 import (
    PARAMS, make_geometry, diagnostics_general, build_open_comp_overlay,
    setup_reset_overlay, phase_masks, integrate_pos_neg, C_QI
)
from run_candidate_source_model_v02 import observer_series
from run_candidate_source_model_v03_component_polish import fit_one, XI

EPS=1e-14
STRICT_A_SUPPORT=0.022
STRICT_A_SHOULDER=0.011


def build_grid(n_t=801,n_l=501):
    l=np.linspace(-18.0,18.0,n_l)
    t_end=PARAMS['T_B']+2*PARAMS['T_R']+PARAMS['T_H']+PARAMS['T_C']+PARAMS['T_Breset']
    t=np.linspace(0.0,t_end,n_t)
    N,B,R,phase,times,C=make_geometry(t,l,PARAMS)
    d=diagnostics_general(t,l,N,B,R)
    return t,l,N,B,R,phase,times,C,d


def flux_complete_signed(t,l,N,B,R,source_Tkk,label):
    """Minimal signed anisotropic embedding.

    Orthonormal reduced ansatz: rho = pr = source_Tkk/2.  A conservation-completing
    radial flux f solves approximately
        d_t rho + 1/(B R^2) d_l (N R^2 f) = 0
    with f=0 at the symmetry center.  The two radial null contractions are
        Tkk_+ = source_Tkk + 2 f,  Tkk_- = source_Tkk - 2 f.
    """
    rho=0.5*source_Tkk
    pr=0.5*source_Tkk
    rho_t=np.gradient(rho,t,axis=0,edge_order=2)
    weighted=B*R*R*rho_t
    Q=np.zeros_like(weighted)
    i0=int(np.argmin(np.abs(l)))
    for ti in range(len(t)):
        if i0 < len(l)-1:
            integrand=-weighted[ti,i0:]
            Q[ti,i0:]=np.concatenate([[0.0],np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(l[i0:]))])
        if i0 > 0:
            lleft=l[:i0+1][::-1]
            integrand=-weighted[ti,:i0+1][::-1]
            qleft=np.concatenate([[0.0],np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(lleft))])
            Q[ti,:i0+1]=qleft[::-1]
    f=Q/(N*R*R+EPS)
    div=np.gradient(N*R*R*f,l,axis=1,edge_order=2)/(B*R*R+EPS)
    residual_flux_completed=rho_t+div
    residual_zero_flux=rho_t
    Tkk_plus=source_Tkk+2*f
    Tkk_minus=source_Tkk-2*f
    Tkk_min=np.minimum(Tkk_plus,Tkk_minus)
    return {
        'label':label,'rho':rho,'pr':pr,'f':f,
        'residual_flux_completed':residual_flux_completed,
        'residual_zero_flux':residual_zero_flux,
        'Tkk_plus':Tkk_plus,'Tkk_minus':Tkk_minus,'Tkk_min':Tkk_min,
    }


def zones(l):
    return {
        'access':np.abs(l)<=0.25,
        'support':np.abs(l)<=0.75,
        'support_ring':(np.abs(l)>=0.28)&(np.abs(l)<=0.95),
        'shoulder':(np.abs(l)>=1.2)&(np.abs(l)<=4.5),
        'matching':(np.abs(l)>4.5)&(np.abs(l)<=9.0),
        'global':np.ones_like(l,dtype=bool),
    }


def phase_zone_summary(t,l,phase,embeds):
    z=zones(l); pm=phase_masks(phase)
    rows=[]
    for emb in embeds:
        lab=emb['label']
        source=emb.get('source_Tkk')
        for ph,tm in pm.items():
            for zn,lm in z.items():
                idx=np.ix_(tm,lm)
                if not np.any(tm) or not np.any(lm):
                    continue
                row={'component':lab,'phase':ph,'zone':zn}
                if source is not None:
                    row['max_abs_source_Tkk']=float(np.max(np.abs(source[idx])))
                    row['min_source_Tkk']=float(np.min(source[idx]))
                    row['max_source_Tkk']=float(np.max(source[idx]))
                for key in ['rho','pr','f','residual_flux_completed','residual_zero_flux','Tkk_min']:
                    arr=emb[key]
                    row[f'max_abs_{key}']=float(np.max(np.abs(arr[idx])))
                    row[f'rms_{key}']=float(np.sqrt(np.mean(arr[idx]**2)))
                    row[f'min_{key}']=float(np.min(arr[idx]))
                    row[f'max_{key}']=float(np.max(arr[idx]))
                # Normalized flux and residual diagnostics.
                scale=max(row.get('max_abs_source_Tkk',0.0),EPS)
                row['max_abs_flux_over_source_scale']=row['max_abs_f']/scale
                row['max_abs_flux_completed_residual_over_source_scale']=row['max_abs_residual_flux_completed']/scale
                row['max_abs_zero_flux_exchange_over_source_scale']=row['max_abs_residual_zero_flux']/scale
                rows.append(row)
    return pd.DataFrame(rows)


def observer_ledgers(t,l,phase,series_dict):
    pm=phase_masks(phase)
    rows=[]
    for label,T in series_dict.items():
        obs=observer_series(l,T)
        for o,y in obs.items():
            row={'series':label,'observer_family':o}
            for ph,m in pm.items():
                neg,pos,nc,pc=integrate_pos_neg(t,y,m)
                row[f'{ph}_neg']=neg; row[f'{ph}_pos']=pos
                row[f'{ph}_neg_centroid']=nc; row[f'{ph}_pos_centroid']=pc
            row['full_pos_to_neg_ratio']=row['full_cycle_pos']/(row['full_cycle_neg']+EPS)
            row['open_pos_to_neg_ratio']=row['open_interval_pos']/(row['open_interval_neg']+EPS)
            row['setup_reset_pos_to_neg_ratio']=row['setup_reset_pos']/(row['setup_reset_neg']+EPS)
            rows.append(row)
    return pd.DataFrame(rows)


def lorentzian_weights(t,center,tau):
    w=(tau/math.pi)/((t-center)**2+tau*tau)
    area=np.trapezoid(w,t)
    return w/area if area>0 else w


def sampled_min(t,y,tau,centers):
    vals=[]; cs=[]
    for c in centers:
        if c-4*tau<t[0] or c+4*tau>t[-1]:
            continue
        w=lorentzian_weights(t,c,tau)
        vals.append(float(np.trapezoid(y*w,t))); cs.append(float(c))
    if not vals:
        return {'tau':tau,'min_sampled_avg':float('nan'),'center_at_min':float('nan'),'qi_proxy_bound':-C_QI/tau**4,'qi_proxy_margin':float('nan')}
    vals=np.array(vals); i=int(np.argmin(vals)); bound=-C_QI/tau**4
    return {'tau':tau,'min_sampled_avg':float(vals[i]),'center_at_min':cs[i],'qi_proxy_bound':bound,'qi_proxy_margin':float(vals[i]-bound),'status':'above_proxy_bound' if vals[i]>=bound else 'below_proxy_bound'}


def sampling_table(t,l,series_dict):
    centers=np.linspace(t[0],t[-1],501)
    taus=[0.5,1,2,5,10,20,40,80]
    rows=[]
    for label,T in series_dict.items():
        obs=observer_series(l,T)
        for o,y in obs.items():
            if o not in ['core_line','access_mean','support_mean','support_ring_mean','shoulder_mean','matching_mean']:
                continue
            for tau in taus:
                sm=sampled_min(t,y,tau,centers)
                rows.append({'series':label,'observer_family':o,**sm})
    return pd.DataFrame(rows)


def run():
    t,l,N,B,R,phase,times,C,d=build_grid()
    Tgeo=d['Tkk_min']
    open_src=build_open_comp_overlay(t,l,C)
    sr_src=setup_reset_overlay(t,l,times,STRICT_A_SUPPORT,STRICT_A_SHOULDER)
    # Refit NMC support component using the v0.3 selected locality parameters.
    fit=fit_one(t,l,N,B,d,phase,times,Tgeo,lcut=0.8,shoulder_weight=10.0,ring_weight=0.8,lam=3e-4)
    Tnmc=fit['Tnmc']

    Ttarget=Tgeo+open_src+sr_src
    Tinfra=Ttarget-Tnmc

    # Reduced signed embeddings.
    comp_nmc=flux_complete_signed(t,l,N,B,R,Tnmc,'NMC_like_support_component')
    comp_nmc['source_Tkk']=Tnmc
    comp_infra=flux_complete_signed(t,l,N,B,R,Tinfra,'infrastructure_residual_component')
    comp_infra['source_Tkk']=Tinfra
    comp_total=flux_complete_signed(t,l,N,B,R,Ttarget,'combined_hybrid_source')
    comp_total['source_Tkk']=Ttarget
    comp_open=flux_complete_signed(t,l,N,B,R,open_src,'open_interval_repayment_overlay')
    comp_open['source_Tkk']=open_src
    comp_sr=flux_complete_signed(t,l,N,B,R,sr_src,'setup_reset_repayment_overlay')
    comp_sr['source_Tkk']=sr_src

    embeds=[comp_nmc,comp_infra,comp_total,comp_open,comp_sr]
    pz=phase_zone_summary(t,l,phase,embeds)
    pz.to_csv(OUT/'hybrid_closure_phase_zone_summary.csv',index=False)

    series={
        'target_zero_flux_Tkk':Ttarget,
        'combined_flux_completed_Tkk_min':comp_total['Tkk_min'],
        'nmc_component_Tkk_min':comp_nmc['Tkk_min'],
        'infrastructure_component_Tkk_min':comp_infra['Tkk_min'],
        'open_repayment_Tkk_min':comp_open['Tkk_min'],
        'setup_reset_repayment_Tkk_min':comp_sr['Tkk_min'],
    }
    led=observer_ledgers(t,l,phase,series)
    led.to_csv(OUT/'hybrid_closure_observer_ledgers.csv',index=False)

    samp=sampling_table(t,l,series)
    samp.to_csv(OUT/'hybrid_closure_lorentzian_sampling.csv',index=False)

    # Component closure scores and access containment.
    rows=[]
    for comp in embeds:
        lab=comp['label']
        source=comp['source_Tkk']
        for zn,lm in zones(l).items():
            idx=np.ix_(np.ones_like(t,dtype=bool),lm)
            source_scale=float(np.max(np.abs(source[idx])))+EPS
            rows.append({
                'component':lab,'zone':zn,
                'max_abs_source_Tkk':source_scale,
                'max_abs_required_flux':float(np.max(np.abs(comp['f'][idx]))),
                'flux_over_source_scale':float(np.max(np.abs(comp['f'][idx]))/source_scale),
                'rms_flux_completed_residual':float(np.sqrt(np.mean(comp['residual_flux_completed'][idx]**2))),
                'max_flux_completed_residual':float(np.max(np.abs(comp['residual_flux_completed'][idx]))),
                'rms_zero_flux_exchange':float(np.sqrt(np.mean(comp['residual_zero_flux'][idx]**2))),
                'max_zero_flux_exchange':float(np.max(np.abs(comp['residual_zero_flux'][idx]))),
                'flux_completed_residual_over_source_scale':float(np.max(np.abs(comp['residual_flux_completed'][idx]))/source_scale),
                'zero_flux_exchange_over_source_scale':float(np.max(np.abs(comp['residual_zero_flux'][idx]))/source_scale),
            })
    closure=pd.DataFrame(rows)
    closure.to_csv(OUT/'hybrid_closure_component_scores.csv',index=False)

    # Rank worst sampling rows for quick review.
    worst=samp.sort_values('qi_proxy_margin').groupby(['series','observer_family'],as_index=False).head(1).sort_values('qi_proxy_margin')
    worst.to_csv(OUT/'hybrid_closure_worst_sampling_by_series.csv',index=False)

    # Simple pass/fail summary.
    def row_metric(component,zone,col):
        r=closure[(closure.component==component)&(closure.zone==zone)].iloc[0]
        return float(r[col])
    access_flux=row_metric('combined_hybrid_source','access','max_abs_required_flux')
    access_src=row_metric('combined_hybrid_source','access','max_abs_source_Tkk')
    support_flux_ratio=row_metric('combined_hybrid_source','support','flux_over_source_scale')
    shoulder_flux_ratio=row_metric('combined_hybrid_source','shoulder','flux_over_source_scale')
    global_res_ratio=row_metric('combined_hybrid_source','global','flux_completed_residual_over_source_scale')
    # ledger comparison for target vs flux-completed min.
    def ledger_val(series_name,obs,col):
        r=led[(led.series==series_name)&(led.observer_family==obs)].iloc[0]
        return float(r[col])
    sampling_compare={}
    for obs in ['core_line','access_mean','support_mean','support_ring_mean','shoulder_mean']:
        rz=worst[(worst.series=='target_zero_flux_Tkk')&(worst.observer_family==obs)].iloc[0]
        rf=worst[(worst.series=='combined_flux_completed_Tkk_min')&(worst.observer_family==obs)].iloc[0]
        sampling_compare[obs]={
            'target_worst_margin':float(rz.qi_proxy_margin),
            'flux_completed_worst_margin':float(rf.qi_proxy_margin),
            'margin_delta_flux_minus_target':float(rf.qi_proxy_margin-rz.qi_proxy_margin),
            'flux_completed_tau':float(rf.tau),
            'flux_completed_center':float(rf.center_at_min),
        }

    summary={
        'screen':'hybrid_source_closure_v01',
        'geometry':'Reference Geometry v0.3 frozen',
        'source_architecture':'Candidate Source Architecture v0.3 strict-pass hybrid',
        'strict_pass_setup_reset_amps':{'A_support_setup_reset':STRICT_A_SUPPORT,'A_shoulder_setup_reset':STRICT_A_SHOULDER},
        'nmc_fit_parameters':{'xi':XI,'lcut':0.8,'shoulder_weight':10.0,'ring_weight':0.8},
        'closure_readout':{
            'access_flux':access_flux,
            'access_source_scale':access_src,
            'access_flux_over_source_scale':access_flux/(access_src+EPS),
            'support_flux_over_source_scale':support_flux_ratio,
            'shoulder_flux_over_source_scale':shoulder_flux_ratio,
            'global_flux_completed_residual_over_source_scale':global_res_ratio,
            'access_full_pos_to_neg_target':ledger_val('target_zero_flux_Tkk','access_mean','full_pos_to_neg_ratio'),
            'access_full_pos_to_neg_flux_completed_min':ledger_val('combined_flux_completed_Tkk_min','access_mean','full_pos_to_neg_ratio'),
            'support_full_pos_to_neg_target':ledger_val('target_zero_flux_Tkk','support_mean','full_pos_to_neg_ratio'),
            'support_full_pos_to_neg_flux_completed_min':ledger_val('combined_flux_completed_Tkk_min','support_mean','full_pos_to_neg_ratio'),
            'shoulder_full_pos_to_neg_target':ledger_val('target_zero_flux_Tkk','shoulder_mean','full_pos_to_neg_ratio'),
            'shoulder_full_pos_to_neg_flux_completed_min':ledger_val('combined_flux_completed_Tkk_min','shoulder_mean','full_pos_to_neg_ratio'),
        },
        'sampling_compare':sampling_compare,
        'decision':'freeze_reduced_reference_model_with_actuator_exchange_closure' if (access_flux/(access_src+EPS)<0.25 and global_res_ratio<0.05) else 'do_not_freeze_without_closure_polish',
        'interpretation':[
            'The hybrid source can be embedded in a reduced anisotropic tensor with conservation-completing radial flux.',
            'The flux-completed representation localizes the active exchange/transport burden outside the access core in this reduced screen.' if access_flux/(access_src+EPS)<0.25 else 'The flux-completed representation introduces nontrivial access-region flux that requires polish.',
            'The remaining physical source question is field-equation closure for the NMC support component and actuator interpretation for infrastructure repayment.'
        ]
    }
    (OUT/'hybrid_source_closure_v01_extracts.json').write_text(json.dumps(summary,indent=2,allow_nan=True))

    # Save a digest timeseries for visual review.
    obs_target=observer_series(l,Ttarget); obs_flux=observer_series(l,comp_total['Tkk_min'])
    obs_f=observer_series(l,comp_total['f'])
    sample_idx=np.unique(np.round(np.linspace(0,len(t)-1,401)).astype(int))
    rows=[]
    for k in sample_idx:
        row={'t':float(t[k]),'phase':str(phase[k])}
        for o in ['core_line','access_mean','support_mean','support_ring_mean','shoulder_mean']:
            row[f'{o}_target_Tkk']=float(obs_target[o][k])
            row[f'{o}_flux_completed_min_Tkk']=float(obs_flux[o][k])
            row[f'{o}_radial_flux_f']=float(obs_f[o][k])
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT/'hybrid_source_closure_timeseries_digest.csv',index=False)

if __name__=='__main__':
    run()
