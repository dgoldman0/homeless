#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, sys, json, math, time
from pathlib import Path
import numpy as np
import pandas as pd

ADM_PATH=Path('/mnt/data/adm_3p1_viability_v3_baware.py')
spec=importlib.util.spec_from_file_location('adm', ADM_PATH)
adm=importlib.util.module_from_spec(spec); sys.modules['adm']=adm; spec.loader.exec_module(adm)

OUT=Path('/mnt/data/candidate_robustness_checks')
OUT.mkdir(exist_ok=True)

transition=dict(v_exit=0.5,x_catch=0.05,x_beta=0.70,x_q=1.25,w_catch=0.25,w_beta=0.28,w_q=0.30,p_beta=4.0,packet_radius=0.35)
base_v1=dict(B0=8.0,wB=10.0,T_B=150.0,T_R=5.0,T_H=60.0,T_C=20.0,T_Breset=150.0,n_sh_amp=-0.18,n_sh_center=2.3,n_sh_width=1.0)
fixed=dict(Rth=1.25,wth=0.12,Rpass=0.35,wpass=0.08)

candidates=[
 ('v01_baseline', {'C0':100.0,'C_perp':1.0,'Rth':0.75,'wth':0.05,'Rpass':0.35,'wpass':0.05}, {'B0':8.0,'wB':10.0}),
 ('noangular_C20_Cp1_B6_wB12', {**fixed,'C0':20.0,'C_perp':1.0}, {'B0':6.0,'wB':12.0}),
 ('candidate_C20_Cp5_B6_wB12', {**fixed,'C0':20.0,'C_perp':5.0}, {'B0':6.0,'wB':12.0}),
 ('reserve_C100_Cp5_B4_wB6', {**fixed,'C0':100.0,'C_perp':5.0}, {'B0':4.0,'wB':6.0}),
]
# stressed scenario for grid/proxy robustness
scenario=('V10_lam6',10.0,6.0)
# additional scenarios for score sanity summaries already handled by confirmation CSV
X_values=[0.05,0.35,0.70,1.00,1.25]


def eval_candidate(label,pkt_vars,v1_vars,nl,nth,nph=4):
    scen,V,lam=scenario
    gp=adm.GridParams(nl=nl,nth=nth,nph=nph,l_min=-2.4,l_max=2.4)
    coords=adm.make_grid(gp)
    l,th,ph=coords
    L,TH,PH=np.meshgrid(l,th,ph,indexing='ij')
    rows=[]
    pp=adm.PacketParams(**{**transition,**pkt_vars,'V':V,'lambda_factor':lam})
    v1p=adm.V1Params(**{**base_v1,**v1_vars})
    t_cycle=adm.cycle_time_from_phase('hold_mid', v1p)
    for X in X_values:
        summary,tensors=adm.evaluate_slice(t_cycle,float(X),coords,v1p,pp,'always_open',dt_time=1e-3)
        comp=adm.compact_status(summary)
        rho=tensors['rho_H']; j=tensors['j_norm']; R3=tensors['R3']; K=tensors['K_trace']; W=tensors['W']; S=tensors['S']; gtt=tensors['gtt']; pn=tensors['packet_norm']
        masks={
            'packet':np.abs(L-X)<=pp.packet_radius,
            'support_edge':(W>=0.05)&(W<=0.95),
            'release_edge':(W>=0.05)&(W<=0.95)&(S>=0.05),
        }
        row={'label':label,'X':float(X),'nl':nl,'nth':nth,'nph':nph,**comp}
        # pressure-sensitive null proxies: p_l = eta*rho_H and worst-sign bracket p_l=-abs(rho_H)
        proxies={
            'floor_eta0':rho - 2*np.abs(j),
            'pressure_eta_pos1':rho + rho - 2*np.abs(j),
            'pressure_eta_neg1':rho - rho - 2*np.abs(j),
            'pressure_worst_abs':rho - np.abs(rho) - 2*np.abs(j),
        }
        for region,m in masks.items():
            if not np.any(m):
                for pname in proxies.keys():
                    row[f'{region}_{pname}_min']=float('nan')
                    row[f'{region}_{pname}_negmean']=float('nan')
                    row[f'{region}_{pname}_negfrac']=float('nan')
                for arrname in ['rhoH','j','R3','K','gtt','packet_norm']:
                    row[f'{region}_{arrname}_p95_abs']=float('nan')
                    row[f'{region}_{arrname}_max']=float('nan')
                continue
            for pname,vals in proxies.items():
                v=vals[m]
                neg=np.maximum(-v,0.0)
                row[f'{region}_{pname}_min']=float(np.min(v))
                row[f'{region}_{pname}_negmean']=float(np.mean(neg))
                row[f'{region}_{pname}_negfrac']=float(np.mean(v<0))
            for arrname,arr in [('rhoH',rho),('j',j),('R3',R3),('K',K),('gtt',gtt),('packet_norm',pn)]:
                v=arr[m]
                row[f'{region}_{arrname}_p95_abs']=float(np.percentile(np.abs(v),95))
                row[f'{region}_{arrname}_max']=float(np.max(v))
        rows.append(row)
    return rows

# 1) Grid sensitivity and pressure proxy at 25/41/61 x 11/17/25
all_rows=[]
start=time.time()
for nl,nth in [(25,11),(41,17),(61,25)]:
    for label,pkt,v1 in candidates:
        all_rows.extend(eval_candidate(label,pkt,v1,nl,nth))
        print('done',label,nl,nth,flush=True)
raw=pd.DataFrame(all_rows)
raw.to_csv(OUT/'raw_proxy_grid_rows.csv',index=False)

# aggregate grid rows
agg=[]
for (label,nl,nth),g in raw.groupby(['label','nl','nth']):
    row={'label':label,'nl':int(nl),'nth':int(nth),'nph':int(g['nph'].iloc[0])}
    # constraints
    row['packet_fail_total']=int(g['packet_fail_points'].sum())
    row['edge_fail_total']=int(g['edge_fail_points'].sum())
    row['max_packet_norm']=float(g['packet_max_norm'].max())
    row['max_edge_gtt']=float(g['edge_max_gtt'].max())
    for region in ['packet','support_edge','release_edge']:
        for proxy in ['floor_eta0','pressure_eta_pos1','pressure_eta_neg1','pressure_worst_abs']:
            row[f'{region}_{proxy}_min']=float(g[f'{region}_{proxy}_min'].min())
            row[f'{region}_{proxy}_negmean_max']=float(g[f'{region}_{proxy}_negmean'].max())
            row[f'{region}_{proxy}_negfrac_max']=float(g[f'{region}_{proxy}_negfrac'].max())
        for metric in ['rhoH','j','R3','K']:
            row[f'{region}_{metric}_p95_max']=float(g[f'{region}_{metric}_p95_abs'].max())
    row['J_geom']=max(row['packet_rhoH_p95_max'], row['support_edge_rhoH_p95_max']) + 0.05*row['packet_R3_p95_max']
    row['J_dyn']=row['packet_j_p95_max'] + row['support_edge_j_p95_max'] + 0.02*row['packet_K_p95_max']
    row['J_total']=row['J_geom']+row['J_dyn']
    agg.append(row)
aggdf=pd.DataFrame(agg)
# relatives per grid to v01_baseline
for (nl,nth),sub in aggdf.groupby(['nl','nth']):
    base=sub[sub.label=='v01_baseline'].iloc[0]
    idx=(aggdf.nl==nl)&(aggdf.nth==nth)
    for col in ['J_geom','J_dyn','J_total','packet_floor_eta0_negmean_max','packet_pressure_eta_neg1_negmean_max','packet_pressure_worst_abs_negmean_max','packet_rhoH_p95_max','packet_j_p95_max','packet_R3_p95_max','packet_K_p95_max']:
        if abs(base[col])>1e-15:
            aggdf.loc[idx,'rel_'+col]=aggdf.loc[idx,col]/base[col]
aggdf.to_csv(OUT/'grid_pressure_robustness_summary.csv',index=False)

# 2) score-weight robustness on existing narrow fast sweep
fast_path=Path('/mnt/data/v02_confirmation_narrow/narrow_fast_sweep_25x11.csv')
df=pd.read_csv(fast_path)
df=df[df['clear']==True].copy()
# add noangular/ref if in file; all clear.
# normalize metrics to v01 baseline in same file
base=df[df.label=='v01_geometry_baseline'].iloc[0]
metrics=['J_geom','J_dyn','rhoH_packet_p95_max','rhoH_edge_p95_max','R3_packet_p95_max','K_packet_p95_max','j_packet_p95_max','j_edge_p95_max']
for m in metrics:
    df[f'n_{m}']=df[m]/base[m]
df['n_J_total']=df['J_total']/base['J_total']
# score definitions
score_defs={
    'J_geom_plus_J_dyn': df['n_J_geom']+df['n_J_dyn'],
    'J_geom_plus_0p1J_dyn': df['n_J_geom']+0.1*df['n_J_dyn'],
    '0p1J_geom_plus_J_dyn': 0.1*df['n_J_geom']+df['n_J_dyn'],
    'max_norm_metrics': df[[f'n_{m}' for m in ['J_geom','J_dyn','rhoH_packet_p95_max','R3_packet_p95_max','j_packet_p95_max','j_edge_p95_max']]].max(axis=1),
}
score_rows=[]
for name,score in score_defs.items():
    tmp=df.copy(); tmp['score']=score
    top=tmp.sort_values(['score','n_J_geom']).head(20).copy()
    top['score_name']=name
    top=top.assign(rank=range(1,len(top)+1))
    score_rows.append(top[['score_name','rank','label','score','pkt_C0','pkt_C_perp','pkt_Rth','pkt_wth','v1_B0','v1_wB','n_J_geom','n_J_dyn','n_J_total']])
scoredf=pd.concat(score_rows,ignore_index=True)
scoredf.to_csv(OUT/'score_weight_robustness_top20.csv',index=False)
# summarize top family
summary=[]
for name,group in scoredf.groupby('score_name'):
    top5=group[group['rank']<=5]
    summary.append({'score_name':name,
                    'top1_label':group.iloc[0]['label'],
                    'top1_C0':float(group.iloc[0]['pkt_C0']),'top1_Cperp':float(group.iloc[0]['pkt_C_perp']),'top1_B0':float(group.iloc[0]['v1_B0']),'top1_wB':float(group.iloc[0]['v1_wB']),
                    'top5_Cperp_values':sorted(set(map(float,top5['pkt_C_perp']))),
                    'top5_C0_values':sorted(set(map(float,top5['pkt_C0']))),
                    'top5_B0_values':sorted(set(map(float,top5['v1_B0']))),
                    'top5_wB_values':sorted(set(map(float,top5['v1_wB']))),
                   })
score_summary=pd.DataFrame(summary)
score_summary.to_csv(OUT/'score_weight_robustness_summary.csv',index=False)

# 3) human-readable tables
with open(OUT/'robustness_tables.md','w') as f:
    f.write('# Candidate robustness checks\n\n')
    f.write('## Grid and pressure-sensitive proxy summary at 61x25\n\n')
    cols=['label','packet_fail_total','edge_fail_total','max_packet_norm','max_edge_gtt','rel_J_total','rel_J_geom','rel_J_dyn','rel_packet_floor_eta0_negmean_max','rel_packet_pressure_eta_neg1_negmean_max','rel_packet_pressure_worst_abs_negmean_max','rel_packet_rhoH_p95_max','rel_packet_j_p95_max','rel_packet_R3_p95_max','rel_packet_K_p95_max']
    f.write(aggdf[(aggdf.nl==61)&(aggdf.nth==25)][cols].sort_values('rel_J_total').to_markdown(index=False,floatfmt='.6g'))
    f.write('\n\n## Score-weight top family summary\n\n')
    f.write(score_summary.to_markdown(index=False))
    f.write('\n\n## Top 5 under each scoring rule\n\n')
    f.write(scoredf[scoredf['rank']<=5][['score_name','rank','label','score','pkt_C0','pkt_C_perp','v1_B0','v1_wB','n_J_geom','n_J_dyn']].to_markdown(index=False,floatfmt='.6g'))

summary_json={'elapsed_seconds':time.time()-start,
              'grid_pressure_summary':aggdf.to_dict(orient='records'),
              'score_weight_summary':score_summary.to_dict(orient='records'),
              'notes':{
                  'pressure_sensitive_proxy':'Tkk_eta = rho_H + eta*rho_H - 2|j_M| for eta=-1,0,+1; worst_abs uses p_l=-|rho_H|. This is a pressure-sensitivity bracket, not a pressure-complete stress tensor.',
                  'grid_sensitivity':'V=10, lambda=6, X={0.05,0.35,0.70,1.00,1.25}; nph=4.',
                  'score_weighting':'uses narrow 25x11 candidate family from v02 confirmation sweep; ranks clear candidates under four normalized score definitions.'
              }}
(OUT/'robustness_summary.json').write_text(json.dumps(summary_json,indent=2))
print('wrote',OUT,'elapsed',time.time()-start)
print((OUT/'robustness_tables.md').read_text()[:4000])
