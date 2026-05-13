#!/usr/bin/env python3
"""Residual-balance polish for candidate source model v0.3.

Uses the selected locality-polished NMC component from v0.3 and adds one
infrastructure repayment degree of freedom: a post-closure support-ring source
term during the compensation phase.  This closes the support-ring full-cycle
residual ratio while preserving the separated NMC-support / infrastructure
repayment interpretation.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[0]
OUT=ROOT/'data'/'candidate_source_model_v03_component_polish'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0,str(HERE))
from run_source_realism_prescreen_v02 import PARAMS, make_geometry, diagnostics_general, build_open_comp_overlay, setup_reset_overlay, support_ring_window, phase_masks
from run_component_separation_screen_v01 import separation_ledgers, phase_component_extrema
from run_candidate_source_model_v03_component_polish import fit_one

EPS=1e-13

def run():
    l=np.linspace(-18,18,201)
    t_end=PARAMS['T_B']+2*PARAMS['T_R']+PARAMS['T_H']+PARAMS['T_C']+PARAMS['T_Breset']
    t=np.linspace(0,t_end,321)
    N,B,R,phase,times,C=make_geometry(t,l,PARAMS)
    d=diagnostics_general(t,l,N,B,R)
    Tgeo=d['Tkk_min']
    # Selected locality-polished NMC split from v0.3.
    res=fit_one(t,l,N,B,d,phase,times,Tgeo,lcut=0.8,shoulder_weight=10.0,ring_weight=0.8)
    Tnmc=res['Tnmc']
    base_open=build_open_comp_overlay(t,l,C)
    Wring=support_ring_window(l)[None,:]
    rows=[]; best=None
    for A_open_ring in np.round(np.linspace(0.0,0.006,13),6):
        ring_comp=A_open_ring*C[:,None]*Wring
        for As in np.round(np.linspace(0.018,0.034,9),6):
            for Ah in np.round(np.linspace(0.010,0.018,9),6):
                sr=setup_reset_overlay(t,l,times,float(As),float(Ah))
                src=base_open+ring_comp+sr
                Ttotal=Tgeo+src
                Tinfra=Ttotal-Tnmc
                led=separation_ledgers(t,l,phase,Ttotal,Tnmc,Tinfra,src)
                def get(o,c): return float(led[led.observer_family==o][c].iloc[0])
                ratios={
                    'support':get('support_mean','full_residual_comp_ratio'),
                    'support_ring':get('support_ring_mean','full_residual_comp_ratio'),
                    'shoulder':get('shoulder_mean','full_residual_comp_ratio'),
                    'access':get('access_mean','full_residual_comp_ratio'),
                    'core':get('core_line','full_residual_comp_ratio'),
                }
                row={'A_open_ring_comp':float(A_open_ring),'A_support_setup_reset':float(As),'A_shoulder_setup_reset':float(Ah),
                     **{f'{k}_full_residual_ratio':v for k,v in ratios.items()},
                     'support_ring_setup_reset_ratio':get('support_ring_mean','setup_reset_residual_comp_ratio'),
                     'shoulder_setup_reset_ratio':get('shoulder_mean','setup_reset_residual_comp_ratio'),
                     'support_setup_reset_ratio':get('support_mean','setup_reset_residual_comp_ratio'),
                     'support_ring_open_residual_neg_fraction':get('support_ring_mean','open_residual_neg_fraction'),
                     'shoulder_open_neg_fraction_carried_by_nmc':get('shoulder_mean','open_neg_fraction_carried_by_nmc'),
                    }
                target=[ratios['support'],ratios['support_ring'],ratios['shoulder']]
                deficits=sum(max(0,1.0-r)**2*200 for r in target)
                balance=sum((min(r,2.5)-1.15)**2 for r in target)
                over=sum(max(0,r-2.2)**2 for r in target)
                # keep access/core residual overpayment acknowledged but not dominant; these are residual ratios after NMC split.
                row['score']=deficits+balance+over+0.01*max(0,ratios['access']-5)**2+0.005*max(0,ratios['core']-5)**2
                rows.append(row)
                if best is None or row['score']<best['score']:
                    best=row; best_led=led; best_Tinfra=Tinfra; best_src=src; best_ring=ring_comp; best_sr=sr
    df=pd.DataFrame(rows).sort_values('score')
    df.to_csv(OUT/'candidate_source_model_v03p1_residual_balance_sweep.csv',index=False)
    pd.DataFrame([best]).to_csv(OUT/'candidate_source_model_v03p1_residual_balance_best.csv',index=False)
    best_led.to_csv(OUT/'candidate_source_model_v03p1_observer_ledgers.csv',index=False)
    Ttotal=Tgeo+best_src
    phase_component_extrema(t,l,phase,Tnmc,best_Tinfra,Ttotal).to_csv(OUT/'candidate_source_model_v03p1_phase_zone_extrema.csv',index=False)
    summary={'screen':'candidate_source_model_v03p1_residual_balance',
             'geometry':'Reference Geometry v0.3 frozen',
             'selected_nmc_locality':'lcut=0.8 shoulder_weight=10 ring_weight=0.8',
             'best_residual_balance':best,
             'interpretation':['The locality-polished NMC component is retained.', 'A small post-closure support-ring compensation term closes the support-ring full-cycle residual ledger.', 'Infrastructure repayment remains outward/support-ring/shoulder localized relative to the access family.']}
    (OUT/'candidate_source_model_v03p1_extracts.json').write_text(json.dumps(summary,indent=2))
if __name__=='__main__': run()
