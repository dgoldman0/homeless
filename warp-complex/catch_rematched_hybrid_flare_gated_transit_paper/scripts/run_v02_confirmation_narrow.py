import importlib.util, sys, json, time
from pathlib import Path
import numpy as np
import pandas as pd

ADM_PATH='/mnt/data/adm_3p1_viability_v3_baware.py'
spec=importlib.util.spec_from_file_location('adm', ADM_PATH)
adm=importlib.util.module_from_spec(spec); sys.modules['adm']=adm; spec.loader.exec_module(adm)

out=Path('/mnt/data/v02_confirmation_narrow'); out.mkdir(exist_ok=True)

transition=dict(v_exit=0.5, x_catch=0.05, x_beta=0.70, x_q=1.25, w_catch=0.25, w_beta=0.28, w_q=0.30, p_beta=4.0, packet_radius=0.35)
base_v1=dict(B0=8.0, wB=10.0, T_B=150.0, T_R=5.0, T_H=60.0, T_C=20.0, T_Breset=150.0, n_sh_amp=-0.18, n_sh_center=2.3, n_sh_width=1.0)
fixed_geom=dict(Rth=1.25, wth=0.12, Rpass=0.35, wpass=0.08)
# stress cases to confirm across
scenarios=[('V5_lam575',5.0,5.75),('V10_lam6',10.0,6.0),('V10_lam115',10.0,11.5)]
X_values=[0.05,0.35,0.70,1.00,1.25]

def get_coords(nl,nth,nph):
    gp=adm.GridParams(nl=nl,nth=nth,nph=nph,l_min=-2.4,l_max=2.4)
    return adm.make_grid(gp)

def eval_one_slice(coords, X, V, lam, pkt_vars, v1_vars, r_mode='always_open'):
    pp=adm.PacketParams(**{**transition, **pkt_vars, 'V':V, 'lambda_factor':lam})
    v1p=adm.V1Params(**{**base_v1, **v1_vars})
    t_cycle=adm.cycle_time_from_phase('hold_mid', v1p)
    s,t=adm.evaluate_slice(t_cycle, X, coords, v1p, pp, r_mode, dt_time=1e-3)
    return adm.compact_status(s)

def aggregate_candidate(label, pkt_vars, v1_vars, coords, include_per=False):
    per=[]
    clear=True
    for scen,V,lam in scenarios:
        for X in X_values:
            c=eval_one_slice(coords,X,V,lam,pkt_vars,v1_vars)
            c.update({'scenario':scen,'V':V,'lambda_factor':lam,'X':X,'label':label})
            per.append(c)
            if c['packet_fail_points']>0 or c['edge_fail_points']>0 or c['packet_max_norm']>=0 or c['edge_max_gtt']>=0:
                clear=False
    def maxraw(k):
        vals=[c[k] for c in per if c.get(k) is not None]
        return max(vals) if vals else np.nan
    def maxabs(k):
        vals=[abs(c[k]) for c in per if c.get(k) is not None]
        return max(vals) if vals else np.nan
    agg={'label':label,'clear':bool(clear), **{f'pkt_{k}':v for k,v in pkt_vars.items()}, **{f'v1_{k}':v for k,v in v1_vars.items()},
         'max_packet_norm':maxraw('packet_max_norm'), 'max_edge_gtt':maxraw('edge_max_gtt'), 'max_release_packet_norm':maxraw('release_packet_max_norm'),
         'rhoH_packet_p95_max':maxabs('rho_H_packet_p95_abs'), 'rhoH_edge_p95_max':maxabs('rho_H_edge_p95_abs'), 'R3_packet_p95_max':maxabs('R3_packet_p95_abs'),
         'K_packet_p95_max':maxabs('K_packet_p95_abs'), 'j_packet_p95_max':maxabs('j_packet_p95_abs'), 'j_edge_p95_max':maxabs('j_edge_p95_abs'),
         'packet_fail_total':sum(c['packet_fail_points'] for c in per), 'edge_fail_total':sum(c['edge_fail_points'] for c in per)}
    agg['J_geom']=max(agg['rhoH_packet_p95_max'], agg['rhoH_edge_p95_max']) + 0.05*agg['R3_packet_p95_max']
    agg['J_dyn']=agg['j_packet_p95_max'] + agg['j_edge_p95_max'] + 0.02*agg['K_packet_p95_max']
    agg['J_total']=agg['J_geom'] + agg['J_dyn']
    if include_per:
        return agg,per
    return agg,None

start=time.time()
coords_fast=get_coords(25,11,4)
# baseline for relative numbers across same three scenarios
baseline_pkt={'C0':100.0,'C_perp':1.0,'Rth':0.75,'wth':0.05,'Rpass':0.35,'wpass':0.05}
baseline_v1={'B0':8.0,'wB':10.0}
baseline,_=aggregate_candidate('v01_geometry_baseline', baseline_pkt, baseline_v1, coords_fast)
print('baseline', baseline, flush=True)
rows=[]
# Narrow family exactly requested
for Cperp in [3.0,4.0,5.0,6.0,8.0]:
  for C0 in [20.0,35.0,50.0,75.0,100.0]:
    for B0 in [4.0,5.0,6.0]:
      for wB in [6.0,8.0,10.0,12.0]:
        pkt={**fixed_geom,'C0':C0,'C_perp':Cperp}
        v1={'B0':B0,'wB':wB}
        label=f'C{C0:g}_Cp{Cperp:g}_B{B0:g}_wB{wB:g}'
        agg,_=aggregate_candidate(label,pkt,v1,coords_fast)
        rows.append(agg)
# Include two reference alternatives from previous pass in same grid
refs=[('v02_prior_minburden', {**fixed_geom,'C0':20.0,'C_perp':5.0}, {'B0':6.0,'wB':12.0}),
      ('v02_prior_reserve', {**fixed_geom,'C0':100.0,'C_perp':5.0}, {'B0':4.0,'wB':6.0}),
      ('no_angular_C20', {**fixed_geom,'C0':20.0,'C_perp':1.0}, {'B0':6.0,'wB':12.0}),
      ('v01_geometry_baseline', baseline_pkt, baseline_v1)]
for label,pkt,v1 in refs:
    agg,_=aggregate_candidate(label,pkt,v1,coords_fast)
    rows.append(agg)

df=pd.DataFrame(rows)
for col in ['J_geom','J_dyn','J_total','rhoH_packet_p95_max','rhoH_edge_p95_max','R3_packet_p95_max','K_packet_p95_max','j_packet_p95_max','j_edge_p95_max']:
    df['rel_'+col]=df[col]/baseline[col]
# sort and save fast sweep
df.to_csv(out/'narrow_fast_sweep_25x11.csv', index=False)
clear=df[df.clear].copy()
print('fast candidates',len(df),'clear',int(df.clear.sum()), 'elapsed', time.time()-start, flush=True)
print(clear.sort_values(['rel_J_total','rel_J_geom']).head(10)[['label','rel_J_total','rel_J_geom','rel_J_dyn','max_packet_norm','max_edge_gtt','max_release_packet_norm','pkt_C0','pkt_C_perp','v1_B0','v1_wB']].to_string(index=False), flush=True)

# confirm top candidates + a few capacity/reserve variants at higher grid
coords_conf=get_coords(61,25,4)
selected_labels=[]
for subset in [clear.sort_values(['rel_J_total','rel_J_geom']).head(10), clear.sort_values(['rel_J_geom','rel_J_total']).head(5), df[df.label.isin(['v01_geometry_baseline','no_angular_C20','v02_prior_minburden','v02_prior_reserve'])]]:
    selected_labels += list(subset.label)
selected_labels=list(dict.fromkeys(selected_labels))
confirm_rows=[]; per_rows=[]
for lab in selected_labels:
    r=df[df.label==lab].iloc[0]
    pkt={k[4:]:r[k] for k in r.index if k.startswith('pkt_') and not pd.isna(r[k])}
    v1={k[3:]:r[k] for k in r.index if k.startswith('v1_') and not pd.isna(r[k])}
    agg,per=aggregate_candidate(lab,pkt,v1,coords_conf, include_per=True)
    confirm_rows.append(agg)
    per_rows.extend(per)
    print('confirmed', lab, agg['J_total'], agg['clear'], flush=True)
conf=pd.DataFrame(confirm_rows)
for col in ['J_geom','J_dyn','J_total','rhoH_packet_p95_max','rhoH_edge_p95_max','R3_packet_p95_max','K_packet_p95_max','j_packet_p95_max','j_edge_p95_max']:
    conf['rel_'+col]=conf[col]/conf[conf.label=='v01_geometry_baseline'][col].iloc[0]
conf.to_csv(out/'narrow_confirmation_61x25.csv', index=False)
pd.DataFrame(per_rows).to_csv(out/'narrow_confirmation_61x25_per_slice.csv', index=False)
summary={'baseline_fast':baseline,'n_fast':int(len(df)),'n_fast_clear':int(df.clear.sum()),
         'top_fast_total':clear.sort_values(['rel_J_total','rel_J_geom']).head(20).to_dict(orient='records'),
         'confirmed':conf.sort_values(['rel_J_total','rel_J_geom']).to_dict(orient='records'),
         'elapsed_seconds':time.time()-start}
(out/'narrow_summary.json').write_text(json.dumps(summary,indent=2))
print('CONFIRM TOPS')
print(conf[conf.clear].sort_values(['rel_J_total','rel_J_geom']).head(12)[['label','rel_J_total','rel_J_geom','rel_J_dyn','max_packet_norm','max_edge_gtt','max_release_packet_norm','pkt_C0','pkt_C_perp','v1_B0','v1_wB']].to_string(index=False))
print('elapsed total',time.time()-start)
