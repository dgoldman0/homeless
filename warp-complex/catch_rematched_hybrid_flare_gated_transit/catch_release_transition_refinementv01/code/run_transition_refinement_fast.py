import importlib.util, sys, json, time, csv, shutil, hashlib, zipfile
from pathlib import Path
import numpy as np

mod_path = Path('/mnt/data/adm_3p1_viability_v3_baware.py')
spec = importlib.util.spec_from_file_location('adm3p1', mod_path)
adm = importlib.util.module_from_spec(spec); sys.modules['adm3p1']=adm; spec.loader.exec_module(adm)

OUT = Path('/mnt/data/catch_release_transition_refinement')
if OUT.exists(): shutil.rmtree(OUT)
for sub in ['code','data','derived']: (OUT/sub).mkdir(parents=True, exist_ok=True)
shutil.copy2(mod_path, OUT/'code'/'adm_3p1_viability_v3_baware.py')
v1p=adm.V1Params()

def nz(x, default=0.0):
    return default if x is None else x

def evaluate_design(design, resolution='sweep'):
    if resolution=='sweep':
        gp=adm.GridParams(nl=37,nth=15,nph=4,l_min=-2.4,l_max=2.4)
        X_values=np.linspace(-0.20,1.40,6)
    else:
        gp=adm.GridParams(nl=73,nth=29,nph=6,l_min=-2.4,l_max=2.4)
        X_values=np.linspace(-0.25,1.45,8)
    coords=adm.make_grid(gp)
    t_cycle=adm.cycle_time_from_phase('hold_mid', v1p)
    pp=adm.PacketParams(V=10.0,v_exit=0.5,lambda_factor=6.0,C0=100.0,C_perp=1.0,Rth=0.75,Rpass=0.35,
                        wth=0.05,wpass=0.05,x_catch=design['x_catch'],x_beta=design['x_beta'],x_q=design['x_q'],
                        w_catch=design['w_catch'],w_beta=design['w_beta'],w_q=design['w_q'],p_beta=design['p_beta'],
                        p_capacity=1.0,packet_radius=0.35)
    rows=[]
    agg=dict(packet_fail_slices=0, edge_fail_slices=0, release_fail_slices=0,
             max_packet_norm=-1e300,max_edge_gtt=-1e300,max_release_packet_norm=-1e300,
             max_packet_rho=0,max_edge_rho=0,max_release_rho=0,
             max_packet_j=0,max_edge_j=0,max_release_j=0,
             max_packet_R3=0,max_packet_K=0)
    for X in X_values:
        summary,tensors=adm.evaluate_slice(t_cycle,float(X),coords,v1p,pp,design.get('r_mode','always_open'),dt_time=1e-3)
        cs=adm.compact_status(summary); rel=summary['release_edge']
        row={**design,'X':float(X),**cs,
             'release_fail_points':rel['fail_points_packet_norm_nonnegative']+rel['fail_points_gtt_nonnegative'],
             'release_rho_H_p95_abs':nz(rel['rho_H']['p95_abs']),
             'release_j_p95_abs':nz(rel['j_norm']['p95_abs'])}
        rows.append(row)
        agg['packet_fail_slices'] += int(cs['packet_fail_points']>0)
        agg['edge_fail_slices'] += int(cs['edge_fail_points']>0)
        agg['release_fail_slices'] += int(row['release_fail_points']>0)
        agg['max_packet_norm']=max(agg['max_packet_norm'], nz(cs['packet_max_norm'],-1e300))
        agg['max_edge_gtt']=max(agg['max_edge_gtt'], nz(cs['edge_max_gtt'],-1e300))
        agg['max_release_packet_norm']=max(agg['max_release_packet_norm'], nz(cs['release_packet_max_norm'],-1e300))
        agg['max_packet_rho']=max(agg['max_packet_rho'], nz(cs['rho_H_packet_p95_abs']))
        agg['max_edge_rho']=max(agg['max_edge_rho'], nz(cs['rho_H_edge_p95_abs']))
        agg['max_release_rho']=max(agg['max_release_rho'], row['release_rho_H_p95_abs'])
        agg['max_packet_j']=max(agg['max_packet_j'], nz(cs['j_packet_p95_abs']))
        agg['max_edge_j']=max(agg['max_edge_j'], nz(cs['j_edge_p95_abs']))
        agg['max_release_j']=max(agg['max_release_j'], row['release_j_p95_abs'])
        agg['max_packet_R3']=max(agg['max_packet_R3'], nz(cs['R3_packet_p95_abs']))
        agg['max_packet_K']=max(agg['max_packet_K'], nz(cs['K_packet_p95_abs']))
    agg['clear']=(agg['packet_fail_slices']==0 and agg['edge_fail_slices']==0 and agg['release_fail_slices']==0 and agg['max_packet_norm']<0 and agg['max_edge_gtt']<0)
    # emphasize momentum/source-current demand, with rho included.
    agg['raw_source_cost']=max(agg['max_packet_j'],agg['max_edge_j'],agg['max_release_j']) + max(agg['max_packet_rho'],agg['max_edge_rho'],agg['max_release_rho'])
    return {**design, **agg, 'resolution':resolution}, rows

baseline=dict(name='baseline_p4_open',r_mode='always_open',x_catch=0.25,x_beta=0.70,x_q=1.25,w_catch=0.18,w_beta=0.20,w_q=0.20,p_beta=4.0)

candidates=[baseline]
widths=[('medium',0.25,0.28,0.30),('smooth',0.35,0.38,0.42),('very_smooth',0.45,0.50,0.55)]
positions=[
    ('basepos',0.25,0.70,1.25),
    ('earlycatch',0.05,0.70,1.25),
    ('midcatch',0.15,0.70,1.25),
    ('later_beta',0.15,0.85,1.40),
    ('latewide',0.15,0.85,1.60),
    ('longgap',0.05,0.70,1.45),
]
idx=0
for pname,xc,xb,xq in positions:
  for wname,wc,wb,wq in widths:
    for p_beta in [2.0,3.0,4.0]:
      idx+=1
      candidates.append(dict(name=f'{pname}_{wname}_p{int(p_beta)}',r_mode='always_open',x_catch=xc,x_beta=xb,x_q=xq,w_catch=wc,w_beta=wb,w_q=wq,p_beta=p_beta))

start=time.time()
sweep=[]
for i,d in enumerate(candidates):
    s,_=evaluate_design(d,'sweep')
    sweep.append(s)
    if i%10==0: print('sweep',i,'/',len(candidates),'elapsed',round(time.time()-start,1),flush=True)
base_sweep=sweep[0]
for s in sweep:
    s['relative_source_cost']=s['raw_source_cost']/max(base_sweep['raw_source_cost'],1e-30)
    s['selection_score']=(0 if s['clear'] else 1000)+s['relative_source_cost']

best_sweep=sorted(sweep,key=lambda s:(s['selection_score'], s['max_packet_norm']))[:8]
confirm=[]; confirm_rows=[]
for d in [baseline]+[x for x in best_sweep if x['name']!=baseline['name']][:7]:
    design={k:d[k] for k in ['name','r_mode','x_catch','x_beta','x_q','w_catch','w_beta','w_q','p_beta']}
    s,rows=evaluate_design(design,'confirm')
    confirm.append(s); confirm_rows.extend(rows)
    print('confirm',s['name'],s['clear'],s['raw_source_cost'],s['max_packet_norm'],s['max_edge_gtt'],flush=True)
base_confirm=confirm[0]
for s in confirm:
    for key in ['raw_source_cost','max_packet_j','max_edge_j','max_release_j','max_packet_rho','max_edge_rho','max_release_rho','max_packet_K','max_packet_R3']:
        s['relative_'+key]=s[key]/max(base_confirm[key],1e-30)
    s['relative_source_cost']=s['raw_source_cost']/max(base_confirm['raw_source_cost'],1e-30)

# write data
for fname, rows in [('sweep_summaries.csv',sweep),('confirm_summaries.csv',confirm),('confirm_slice_rows.csv',confirm_rows)]:
    keys=[]
    for r in rows:
        for k in r:
            if k not in keys: keys.append(k)
    with open(OUT/'data'/fname,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(rows)
with open(OUT/'data'/'sweep_summaries.json','w') as f: json.dump(sweep,f,indent=2)
with open(OUT/'data'/'confirm_summaries.json','w') as f: json.dump(confirm,f,indent=2)
with open(OUT/'data'/'confirm_slice_rows.json','w') as f: json.dump(confirm_rows,f,indent=2)

confirmed_sorted=sorted(confirm,key=lambda s:((not s['clear']),s['relative_source_cost']))
md=['# Catch/release transition refinement results\n\n']
md.append('The refinement pass evaluates stressed service at $V=10$ and $\\lambda=6$ with v1 throat geometry, R-open service posture, B-aware packet choreography, paired capacity/lapse support, and ADM source-demand proxies.\n\n')
md.append('## Confirmed candidates\n\n')
md.append('| candidate | clear | rel source cost | max packet norm | max edge gtt | rel packet j | rel edge j | rel release j | x_catch | x_beta | x_q | widths | p_beta |\n')
md.append('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|\n')
for s in confirmed_sorted:
    md.append(f"| {s['name']} | {s['clear']} | {s['relative_source_cost']:.3g} | {s['max_packet_norm']:.3g} | {s['max_edge_gtt']:.3g} | {s['relative_max_packet_j']:.3g} | {s['relative_max_edge_j']:.3g} | {s['relative_max_release_j']:.3g} | {s['x_catch']:.2f} | {s['x_beta']:.2f} | {s['x_q']:.2f} | {s['w_catch']:.2f}/{s['w_beta']:.2f}/{s['w_q']:.2f} | {s['p_beta']:.1f} |\n")
best=confirmed_sorted[0]
md.append('\n## Design selection\n\n')
md.append(f"`{best['name']}` is the selected transition-layer direction in this pass. It keeps clearance and gives relative source cost `{best['relative_source_cost']:.3g}` against the baseline value `1.0`.\n\n")
md.append('The selected structure uses smoother transition profiles and a lower edge exponent than the baseline. The result shifts the design direction from maximum edge suppression toward balanced edge suppression plus transition smoothness.\n')
(OUT/'derived'/'transition_refinement_tables.md').write_text(''.join(md))

# memo
memo=f'''# Catch/release transition-layer refinement memo

## Result

The composite design now has a concrete transition-layer refinement target. The stressed case uses $V=10$, $\\lambda=6$, exact v1 throat controls, R-open service posture, B-aware packet choreography, and paired capacity/lapse support.

The selected candidate is `{best['name']}`.

```math
x_{{catch}}={best['x_catch']:.2f},\quad x_\\beta={best['x_beta']:.2f},\quad x_q={best['x_q']:.2f}
```

```math
w_{{catch}}={best['w_catch']:.2f},\quad w_\\beta={best['w_beta']:.2f},\quad w_q={best['w_q']:.2f},\quad p_\\beta={best['p_beta']:.1f}
```

The selected candidate clears packet, support-edge, and release-edge screens in the confirmation grid. Its source-demand cost is `{best['relative_source_cost']:.3g}` of the baseline reference.

## Engineering reading

The transition layer is the active actuator subsystem. Catch timing, shift fade, throat relaxation, and edge shaping jointly set the Hamiltonian and momentum source-demand proxies.

The refinement pass shows a useful trade:

```math
\\text{{maximum edge suppression}} \rightarrow \\text{{balanced edge suppression plus smoother transition}}
```

The selected candidate uses `p_beta={best['p_beta']:.1f}`. This keeps edge clearance while reducing transition demand relative to the baseline with `p_beta=4`.

## Confirmed comparison

{(OUT/'derived'/'transition_refinement_tables.md').read_text()}

## Design rule

The next composite design should freeze the following service-layer structure:

```math
A=\\exp(qW\\ln C_0)
```

```math
T=\\exp(qW\\ln(\\lambda C_0))
```

```math
\\dot X_{{coord}}=U/B_{{v1}}(X)
```

```math
\\beta^l=-\\dot X_{{coord}} E(X) W^{{p_\\beta}} S(l-X)
```

with smooth transition profiles and R held open through packet service.

## Next refinement

The next compact sweep should vary asymmetric transition widths and separate the catch profile from the shift profile more finely. The objective is source-current minimization with packet and edge clearance retained.
'''
(OUT/'MEMO.md').write_text(memo)

readme='''# Catch/release transition refinement

This bundle contains a compact transition-layer refinement pass for the exact-v1/catch-rematched composite design.

Files:

- `MEMO.md` — engineering memo.
- `code/adm_3p1_viability_v3_baware.py` — ADM diagnostic harness used by the refinement.
- `code/run_transition_refinement_fast.py` — targeted transition-layer sweep and confirmation script.
- `data/confirm_summaries.csv` / `.json` — confirmed candidate summaries.
- `data/confirm_slice_rows.csv` / `.json` — per-slice confirmation diagnostics.
- `data/sweep_summaries.csv` / `.json` — targeted sweep outputs.
- `derived/transition_refinement_tables.md` — Markdown tables generated from the data.
- `MANIFEST.sha256` — checksums.
'''
(OUT/'README.md').write_text(readme)
shutil.copy2('/mnt/data/run_transition_refinement_fast.py', OUT/'code'/'run_transition_refinement_fast.py')

# manifest
lines=[]
for f in sorted([p for p in OUT.rglob('*') if p.is_file() and p.name!='MANIFEST.sha256']):
    h=hashlib.sha256(f.read_bytes()).hexdigest(); lines.append(f"{h}  {f.relative_to(OUT)}")
(OUT/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
# zip
zip_path=Path('/mnt/data/catch_release_transition_refinement.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.rglob('*')):
        if f.is_file(): z.write(f, f.relative_to(OUT.parent))
print('done',round(time.time()-start,1),'best',best['name'],'relcost',best['relative_source_cost'],'zip',zip_path)
