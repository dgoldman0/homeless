#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, sys, json, math, time
from pathlib import Path
import numpy as np
import pandas as pd

ADM_PATH=Path('/mnt/data/catch_rematched_composite_v02/code/adm_3p1_viability_v3_baware.py')
spec=importlib.util.spec_from_file_location('adm', ADM_PATH)
adm=importlib.util.module_from_spec(spec); sys.modules['adm']=adm; spec.loader.exec_module(adm)

OUT=Path('/mnt/data/v02_quantum_source_screen'); OUT.mkdir(exist_ok=True)
transition=dict(v_exit=0.5,x_catch=0.05,x_beta=0.70,x_q=1.25,w_catch=0.25,w_beta=0.28,w_q=0.30,p_beta=4.0,packet_radius=0.35)
base_v1=dict(B0=8.0,wB=10.0,T_B=150.0,T_R=5.0,T_H=60.0,T_C=20.0,T_Breset=150.0,n_sh_amp=-0.18,n_sh_center=2.3,n_sh_width=1.0)
fixed=dict(Rth=1.25,wth=0.12,Rpass=0.35,wpass=0.08)
# baseline and v02 winner, plus no-angular and reserve comparisons for interpretation
candidates=[
 ('v01_geometry_baseline', {'C0':100.0,'C_perp':1.0,'Rth':0.75,'wth':0.05,'Rpass':0.35,'wpass':0.05}, {'B0':8.0,'wB':10.0}),
 ('v02_C20_Cp5_B6_wB12', {**fixed,'C0':20.0,'C_perp':5.0}, {'B0':6.0,'wB':12.0}),
 ('v02_noangular_C20_Cp1_B6_wB12', {**fixed,'C0':20.0,'C_perp':1.0}, {'B0':6.0,'wB':12.0}),
 ('v02_reserve_C100_Cp5_B4_wB6', {**fixed,'C0':100.0,'C_perp':5.0}, {'B0':4.0,'wB':6.0}),
]
scenarios=[('V5_lam575',5.0,5.75),('V10_lam6',10.0,6.0),('V10_lam115',10.0,11.5)]
# Denser X grid for sampled exposure across service trajectory.
X_values=np.round(np.linspace(-0.15,1.45,17),4)
gp=adm.GridParams(nl=41,nth=17,nph=4,l_min=-2.4,l_max=2.4)
coords=adm.make_grid(gp)
l,th,ph=coords
L,TH,PH=np.meshgrid(l,th,ph,indexing='ij')

def region_stats(tensors, X, pp):
    rho=tensors['rho_H']; j=tensors['j_norm']; R3=tensors['R3']; K=tensors['K_trace']; W=tensors['W']; S=tensors['S']; gtt=tensors['gtt']; pn=tensors['packet_norm']
    # Conservative current-floor null proxy from ADM constraints only.
    # It is not a pressure-complete Tkk; it screens where current demand can overwhelm energy support.
    tkk_floor = rho - 2.0*j
    regs={
        'packet': np.abs(L-X)<=pp.packet_radius,
        'support_edge': (W>=0.05)&(W<=0.95),
        'release_edge': (W>=0.05)&(W<=0.95)&(S>=0.05),
        'service_union': ((np.abs(L-X)<=pp.packet_radius)|((W>=0.05)&(W<=0.95)&(S>=0.05))),
    }
    out={}
    for name,m in regs.items():
        if not np.any(m):
            continue
        vals=tkk_floor[m]
        out[f'{name}_tkk_floor_min']=float(np.min(vals))
        out[f'{name}_tkk_floor_mean']=float(np.mean(vals))
        out[f'{name}_tkk_floor_p05']=float(np.percentile(vals,5))
        out[f'{name}_neg_fraction']=float(np.mean(vals<0))
        out[f'{name}_neg_volume_proxy']=float(np.mean(np.maximum(-vals,0)))
        out[f'{name}_rho_p95_abs']=float(np.percentile(np.abs(rho[m]),95))
        out[f'{name}_j_p95_abs']=float(np.percentile(np.abs(j[m]),95))
        out[f'{name}_R3_p95_abs']=float(np.percentile(np.abs(R3[m]),95))
        out[f'{name}_K_p95_abs']=float(np.percentile(np.abs(K[m]),95))
        out[f'{name}_gtt_max']=float(np.max(gtt[m]))
        out[f'{name}_packet_norm_max']=float(np.max(pn[m]))
    return out

def lorentzian_sample(xs, ys, center, tau):
    # normalized discrete Lorentzian sampling over X parameter.
    w=(tau/math.pi)/((xs-center)**2+tau*tau)
    if np.sum(w)==0: return float('nan')
    return float(np.sum(w*ys)/np.sum(w))

rows=[]; start=time.time()
for label,pkt_vars,v1_vars in candidates:
    for scen,V,lam in scenarios:
        pp=adm.PacketParams(**{**transition,**pkt_vars,'V':V,'lambda_factor':lam})
        v1p=adm.V1Params(**{**base_v1,**v1_vars})
        t_cycle=adm.cycle_time_from_phase('hold_mid', v1p)
        for X in X_values:
            summary,tensors=adm.evaluate_slice(t_cycle,float(X),coords,v1p,pp,'always_open',dt_time=1e-3)
            comp=adm.compact_status(summary)
            r=region_stats(tensors,float(X),pp)
            rows.append({'label':label,'scenario':scen,'V':V,'lambda_factor':lam,'X':float(X),**comp,**r})
        print('done',label,scen,flush=True)

df=pd.DataFrame(rows)
df.to_csv(OUT/'quantum_source_proxy_timeseries.csv', index=False)
# per candidate scenario extrema
agg=[]
for (label,scen),g in df.groupby(['label','scenario']):
    row={'label':label,'scenario':scen,'V':float(g['V'].iloc[0]),'lambda_factor':float(g['lambda_factor'].iloc[0])}
    for region in ['packet','support_edge','release_edge','service_union']:
        for col in [f'{region}_tkk_floor_min', f'{region}_neg_volume_proxy', f'{region}_neg_fraction', f'{region}_rho_p95_abs', f'{region}_j_p95_abs', f'{region}_R3_p95_abs', f'{region}_K_p95_abs', f'{region}_gtt_max', f'{region}_packet_norm_max']:
            if col in g:
                if col.endswith('_min'):
                    row['min_'+col]=float(g[col].min())
                else:
                    row['max_'+col]=float(g[col].max())
    # Lorentzian sampled floor for packet/support/release over X with tau values.
    xs=g['X'].to_numpy(float)
    for region in ['packet','support_edge','release_edge','service_union']:
        y=g[f'{region}_tkk_floor_mean'].to_numpy(float)
        for tau in [0.10,0.20,0.35,0.50]:
            centers=xs
            samples=[lorentzian_sample(xs,y,c,tau) for c in centers]
            row[f'{region}_lor_min_tau{tau}']=float(np.nanmin(samples))
            # QI proxy margin with C=3/(32*pi^2), using X units; not physical time.
            C=3/(32*math.pi**2)
            margins=[s + C/(tau**4) for s in samples]
            row[f'{region}_lor_margin_min_tau{tau}']=float(np.nanmin(margins))
    agg.append(row)
aggdf=pd.DataFrame(agg)
# relative to v01 baseline per scenario
for scen in aggdf['scenario'].unique():
    base=aggdf[(aggdf.label=='v01_geometry_baseline')&(aggdf.scenario==scen)].iloc[0]
    idx=aggdf.scenario==scen
    for metric in ['max_packet_neg_volume_proxy','max_support_edge_neg_volume_proxy','max_release_edge_neg_volume_proxy','max_service_union_neg_volume_proxy','max_packet_j_p95_abs','max_support_edge_j_p95_abs','max_packet_rho_p95_abs','max_packet_R3_p95_abs','max_packet_K_p95_abs']:
        # names built with max_ + region... maybe verify exist below
        if metric in aggdf.columns and abs(base[metric])>1e-15:
            aggdf.loc[idx,'rel_'+metric]=aggdf.loc[idx,metric]/base[metric]
aggdf.to_csv(OUT/'quantum_source_proxy_summary.csv', index=False)
# summary JSON
summary={'elapsed_seconds':time.time()-start,'grid':'41x17x4','X_values':X_values.tolist(),'screen_note':'ADM-only current-floor null proxy Tkk_floor=rho_H-2|j_M|; pressure terms not included; Lorentzian sampling uses service-position X as ordering parameter.', 'rows':aggdf.to_dict(orient='records')}
(OUT/'quantum_source_proxy_summary.json').write_text(json.dumps(summary,indent=2))
# readable table
sel=aggdf[aggdf['scenario']=='V10_lam6'].copy()
cols=['label','min_packet_tkk_floor_min','max_packet_neg_volume_proxy','max_packet_j_p95_abs','max_packet_rho_p95_abs','max_packet_R3_p95_abs','max_packet_K_p95_abs','packet_lor_min_tau0.2','packet_lor_margin_min_tau0.2','min_support_edge_tkk_floor_min','max_support_edge_neg_volume_proxy','support_edge_lor_min_tau0.2']
with open(OUT/'screen_tables.md','w') as f:
    f.write('# v0.2 source-admissibility proxy screen\n\n')
    f.write('Stressed scenario `V=10, lambda=6`; ADM-only current-floor proxy `Tkk_floor = rho_H - 2 |j_M|`.\n\n')
    f.write(sel[cols].sort_values('max_packet_neg_volume_proxy').to_markdown(index=False,floatfmt='.6g'))
print(sel[cols].sort_values('max_packet_neg_volume_proxy').to_string(index=False))
print('wrote', OUT)
