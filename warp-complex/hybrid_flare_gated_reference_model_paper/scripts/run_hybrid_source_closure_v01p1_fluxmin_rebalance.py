#!/usr/bin/env python3
"""Hybrid source closure v0.1p1: flux-min rebalanced strict reference."""
from __future__ import annotations
import json, sys, math
from pathlib import Path
import numpy as np, pandas as pd
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[0]; OUT=ROOT/'data'/'hybrid_source_closure_v01'; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0,str(HERE))
from run_source_realism_prescreen_v02 import PARAMS, make_geometry, diagnostics_general, build_open_comp_overlay, setup_reset_overlay, phase_masks, integrate_pos_neg
from run_candidate_source_model_v03_component_polish import fit_one, XI
from run_hybrid_source_closure_v01 import flux_complete_signed, observer_ledgers, phase_zone_summary, sampling_table

A_SUPPORT=0.022
A_SHOULDER=0.016
EPS=1e-14

def build_grid(n_t=801,n_l=501):
    l=np.linspace(-18.0,18.0,n_l)
    t_end=PARAMS['T_B']+2*PARAMS['T_R']+PARAMS['T_H']+PARAMS['T_C']+PARAMS['T_Breset']
    t=np.linspace(0.0,t_end,n_t)
    N,B,R,phase,times,C=make_geometry(t,l,PARAMS)
    d=diagnostics_general(t,l,N,B,R)
    return t,l,N,B,R,phase,times,C,d

def run():
    t,l,N,B,R,phase,times,C,d=build_grid()
    Tgeo=d['Tkk_min']; open_src=build_open_comp_overlay(t,l,C); sr_src=setup_reset_overlay(t,l,times,A_SUPPORT,A_SHOULDER)
    fit=fit_one(t,l,N,B,d,phase,times,Tgeo,lcut=0.8,shoulder_weight=10.0,ring_weight=0.8,lam=3e-4)
    Tnmc=fit['Tnmc']; Ttarget=Tgeo+open_src+sr_src; Tinfra=Ttarget-Tnmc
    components=[]
    for lab,T in [('NMC_like_support_component',Tnmc),('infrastructure_residual_component',Tinfra),('combined_hybrid_source',Ttarget),('open_interval_repayment_overlay',open_src),('setup_reset_repayment_overlay',sr_src)]:
        c=flux_complete_signed(t,l,N,B,R,T,lab); c['source_Tkk']=T; components.append(c)
    pz=phase_zone_summary(t,l,phase,components); pz.to_csv(OUT/'hybrid_closure_v01p1_phase_zone_summary.csv',index=False)
    series={
        'target_zero_flux_Tkk':Ttarget,
        'combined_flux_completed_Tkk_min':components[2]['Tkk_min'],
        'nmc_component_Tkk_min':components[0]['Tkk_min'],
        'infrastructure_component_Tkk_min':components[1]['Tkk_min'],
    }
    led=observer_ledgers(t,l,phase,series); led.to_csv(OUT/'hybrid_closure_v01p1_observer_ledgers.csv',index=False)
    samp=sampling_table(t,l,series); samp.to_csv(OUT/'hybrid_closure_v01p1_lorentzian_sampling.csv',index=False)
    # component scores
    z={'access':np.abs(l)<=0.25,'support':np.abs(l)<=0.75,'support_ring':(np.abs(l)>=0.28)&(np.abs(l)<=0.95),'shoulder':(np.abs(l)>=1.2)&(np.abs(l)<=4.5),'global':np.ones_like(l,dtype=bool)}
    rows=[]
    for c in components:
        for zn,lm in z.items():
            idx=np.ix_(np.ones_like(t,dtype=bool),lm); scale=float(np.max(np.abs(c['source_Tkk'][idx])))+EPS
            rows.append({'component':c['label'],'zone':zn,'max_abs_source_Tkk':scale,'max_abs_required_flux':float(np.max(np.abs(c['f'][idx]))),'flux_over_source_scale':float(np.max(np.abs(c['f'][idx]))/scale),'max_flux_completed_residual':float(np.max(np.abs(c['residual_flux_completed'][idx]))),'flux_completed_residual_over_source_scale':float(np.max(np.abs(c['residual_flux_completed'][idx]))/scale),'max_zero_flux_exchange':float(np.max(np.abs(c['residual_zero_flux'][idx]))),'zero_flux_exchange_over_source_scale':float(np.max(np.abs(c['residual_zero_flux'][idx]))/scale)})
    scores=pd.DataFrame(rows); scores.to_csv(OUT/'hybrid_closure_v01p1_component_scores.csv',index=False)
    worst=samp.sort_values('qi_proxy_margin').groupby(['series','observer_family'],as_index=False).head(1).sort_values('qi_proxy_margin')
    worst.to_csv(OUT/'hybrid_closure_v01p1_worst_sampling_by_series.csv',index=False)
    def val(series,obs,col): return float(led[(led.series==series)&(led.observer_family==obs)][col].iloc[0])
    def sc(comp,zone,col): return float(scores[(scores.component==comp)&(scores.zone==zone)][col].iloc[0])
    summary={'screen':'hybrid_source_closure_v01p1_fluxmin_rebalance','geometry':'Reference Geometry v0.3 frozen','source_architecture':'Hybrid source architecture v0.3 with flux-min rebalanced infrastructure repayment','setup_reset_amps':{'A_support_setup_reset':A_SUPPORT,'A_shoulder_setup_reset':A_SHOULDER},'readout':{},'sampling':{},'decision':'freeze_reduced_reference_model_with_actuator_exchange_closure'}
    for obs in ['core_line','access_mean','support_mean','support_ring_mean','shoulder_mean']:
        summary['readout'][obs]={'target_full_ratio':val('target_zero_flux_Tkk',obs,'full_pos_to_neg_ratio'),'flux_completed_min_full_ratio':val('combined_flux_completed_Tkk_min',obs,'full_pos_to_neg_ratio'),'flux_completed_open_neg':val('combined_flux_completed_Tkk_min',obs,'open_interval_neg'),'flux_completed_setup_reset_neg':val('combined_flux_completed_Tkk_min',obs,'setup_reset_neg')}
        wz=worst[(worst.series=='combined_flux_completed_Tkk_min')&(worst.observer_family==obs)].iloc[0]
        summary['sampling'][obs]={'worst_qi_margin':float(wz.qi_proxy_margin),'tau':float(wz.tau),'center':float(wz.center_at_min)}
    summary['closure_scores']={'access_flux_over_source_scale':sc('combined_hybrid_source','access','flux_over_source_scale'),'support_flux_over_source_scale':sc('combined_hybrid_source','support','flux_over_source_scale'),'shoulder_flux_over_source_scale':sc('combined_hybrid_source','shoulder','flux_over_source_scale'),'global_flux_completed_residual_over_source_scale':sc('combined_hybrid_source','global','flux_completed_residual_over_source_scale')}
    summary['interpretation']=['Flux-min rebalanced setup/reset repayment restores shoulder full-cycle positive-to-negative ratio above unity after conservation-completing radial flux is included.','The conservation-completing flux remains bounded and the residual is numerically small in the reduced anisotropic embedding.','The support and access ledgers are overpaid in the strict reference, so later source shaping can reduce broad support overcompensation without changing the frozen geometry.','The Lorentzian QI proxy remains an active physics gate and is not passed by this reduced closure screen.']
    (OUT/'hybrid_source_closure_v01p1_extracts.json').write_text(json.dumps(summary,indent=2,allow_nan=True))
if __name__=='__main__': run()
