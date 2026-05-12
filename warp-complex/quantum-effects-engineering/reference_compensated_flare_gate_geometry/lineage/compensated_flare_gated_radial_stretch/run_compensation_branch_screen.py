#!/usr/bin/env python3
from __future__ import annotations
import json, math, hashlib, zipfile
from pathlib import Path
import numpy as np
import pandas as pd

PI=math.pi
C_QI=3.0/(32.0*math.pi**2)

def radial_window(l,width,power=4.0): return np.exp(-(np.abs(l)/width)**power)
def ring_window(l,center,width): return np.exp(-((np.abs(l)-center)/width)**4)
def minjerk(x):
    x=np.clip(x,0,1); return 10*x**3-15*x**4+6*x**5

def pulse_unit(t,t0,T):
    # smooth compact pulse 0 at endpoints, max 1 at center
    x=(t-t0)/T
    q=np.zeros_like(t)
    m=(x>=0)&(x<=1)
    q[m]=np.sin(np.pi*x[m])**2
    return q

def ramp_up(t,t0,T):
    x=(t-t0)/T; y=np.zeros_like(t); m=(x>=0)&(x<1); y[x>=1]=1; y[m]=minjerk(x[m]); return y

def ramp_down(t,t0,T):
    x=(t-t0)/T; y=np.zeros_like(t); y[x<0]=1; m=(x>=0)&(x<=1); y[m]=minjerk(1-x[m]); return y

def schedule_with_repay(t,TB=100,TR=10,TH=60,TC=30):
    # B setup -> R open -> hold -> R close -> compensation -> B reset
    tB0=0; tB1=TB
    tR0=tB1; tR1=tR0+TR
    tH0=tR1; tH1=tH0+TH
    tClo0=tH1; tClo1=tClo0+TR
    tComp0=tClo1; tComp1=tComp0+TC
    tReset0=tComp1; tEnd=tReset0+TB
    AB=np.zeros_like(t); AR=np.zeros_like(t); Q=np.zeros_like(t)
    phase=np.full(t.shape,'off',dtype=object)
    # B setup
    m=(t>=tB0)&(t<tB1); AB[m]=minjerk((t[m]-tB0)/TB); phase[m]='B_setup'
    # R open
    m=(t>=tR0)&(t<tR1); AB[m]=1; AR[m]=minjerk((t[m]-tR0)/TR); phase[m]='R_open'
    # hold
    m=(t>=tH0)&(t<tH1); AB[m]=1; AR[m]=1; phase[m]='hold'
    # R close
    m=(t>=tClo0)&(t<tClo1); AB[m]=1; AR[m]=minjerk((tClo1-t[m])/TR); phase[m]='R_close'
    # compensation
    m=(t>=tComp0)&(t<tComp1); AB[m]=1; AR[m]=0; Q[m]=pulse_unit(t[m],tComp0,TC); phase[m]='compensation'
    # B reset
    m=(t>=tReset0)&(t<=tEnd); AB[m]=minjerk((tEnd-t[m])/TB); phase[m]='B_reset'
    return AB,AR,Q,phase,dict(tB0=tB0,tB1=tB1,tR0=tR0,tR1=tR1,tH0=tH0,tH1=tH1,tClo0=tClo0,tClo1=tClo1,tComp0=tComp0,tComp1=tComp1,tReset0=tReset0,tEnd=tEnd)

def make_fields(t,l,B0=8,wB=8,wR=5,Rc=1,TB=100,TR=10,TH=60,TC=30, comp_kind='none', amp=0.0, comp_center=2.5, comp_width=0.8, N_amp=0.0, N_shape='ring'):
    AB,AR,Q,phase,times=schedule_with_repay(t,TB,TR,TH,TC)
    FB=radial_window(l,wB)[None,:]
    B=1+(B0-1)*AB[:,None]*FB
    R_access=np.sqrt(1+l*l)[None,:]
    W=radial_window(l,wR)[None,:]
    R_standby=R_access+W*(Rc-R_access)
    R=R_standby+AR[:,None]*(R_access-R_standby)
    N=np.ones_like(R)
    explicit_Tkk=np.zeros_like(R)
    if comp_kind=='shoulder_R':
        H=ring_window(l,comp_center,comp_width)[None,:]
        R=R+amp*Q[:,None]*H
    elif comp_kind=='lapse_N_ring':
        H=ring_window(l,comp_center,comp_width)[None,:]
        N=np.exp(amp*Q[:,None]*H)
    elif comp_kind=='lapse_N_core':
        H=radial_window(l,0.65)[None,:]
        N=np.exp(amp*Q[:,None]*H)
    elif comp_kind=='explicit_source_ring':
        H=ring_window(l,comp_center,comp_width)[None,:]
        explicit_Tkk=amp*Q[:,None]*H
    elif comp_kind=='explicit_source_core':
        H=radial_window(l,0.65)[None,:]
        explicit_Tkk=amp*Q[:,None]*H
    elif comp_kind=='none':
        pass
    else:
        raise ValueError(comp_kind)
    return B,R,N,explicit_Tkk,phase,times

def deriv_y(F,y,axis):
    return np.gradient(F,y,axis=axis,edge_order=2)

def diagnostics(t,l,B,R,N,explicit_Tkk=None):
    # numerical warped-product Einstein tensor for base h=-N^2 dt^2 + B^2 dl^2
    Bt=deriv_y(B,t,0); Bl=deriv_y(B,l,1)
    Nt=deriv_y(N,t,0); Nl=deriv_y(N,l,1)
    Rt=deriv_y(R,t,0); Rtt=deriv_y(Rt,t,0); Rl=deriv_y(R,l,1); Rll=deriv_y(Rl,l,1); Rtl=deriv_y(Rt,l,1)
    # Christoffels of 2D base
    Gt_tt=Nt/N
    Gl_tt=N*Nl/(B*B)
    Gt_tl=Nl/N
    Gl_tl=Bt/B
    Gt_ll=B*Bt/(N*N)
    Gl_ll=Bl/B
    Dtt=Rtt-Gt_tt*Rt-Gl_tt*Rl
    Dtl=Rtl-Gt_tl*Rt-Gl_tl*Rl
    Dll=Rll-Gt_ll*Rt-Gl_ll*Rl
    boxR=-Dtt/(N*N)+Dll/(B*B)
    gradR2=-(Rt*Rt)/(N*N)+(Rl*Rl)/(B*B)
    Gtt=-2*Dtt/R-2*(N*N)*boxR/R+(N*N)*(1-gradR2)/(R*R)
    Gll=-2*Dll/R+2*(B*B)*boxR/R-(B*B)*(1-gradR2)/(R*R)
    Gtl=-2*Dtl/R
    Tkkp=(Gtt/(N*N)+Gll/(B*B)+2*Gtl/(N*B))/(8*PI)
    Tkkm=(Gtt/(N*N)+Gll/(B*B)-2*Gtl/(N*B))/(8*PI)
    if explicit_Tkk is not None:
        Tkkp=Tkkp+explicit_Tkk
        Tkkm=Tkkm+explicit_Tkk
    Tkkmin=np.minimum(Tkkp,Tkkm)
    flux=Gtl/(8*PI*N*B)
    return dict(Tkk_plus=Tkkp,Tkk_minus=Tkkm,Tkk_min=Tkkmin,flux_hat=flux,Bt_over_NB=Bt/(N*B),Rt_over_NR=Rt/(N*R),N=N,R=R,B=B)

def exposure_stats(t,l,phase,d,region_mask, label):
    # worst null direction average over spatial region: use min over region at each time for negative; max over region for positive
    tkk_min_region=np.min(d['Tkk_min'][:,region_mask],axis=1)
    tkk_max_region=np.max(np.maximum(d['Tkk_plus'][:,region_mask],d['Tkk_minus'][:,region_mask]),axis=1)
    neg=np.maximum(-tkk_min_region,0)
    pos=np.maximum(tkk_max_region,0)
    out={
        f'{label}_negative_full': float(np.trapezoid(neg,t)),
        f'{label}_positive_full': float(np.trapezoid(pos,t)),
        f'{label}_signed_min_full': float(np.trapezoid(tkk_min_region,t)),
        f'{label}_max_abs_flux_full': float(np.max(np.abs(d['flux_hat'][:,region_mask]))),
        f'{label}_max_abs_Rt_over_NR_full': float(np.max(np.abs(d['Rt_over_NR'][:,region_mask]))),
        f'{label}_max_abs_Bt_over_NB_full': float(np.max(np.abs(d['Bt_over_NB'][:,region_mask]))),
    }
    for ph in ['B_setup','R_open','hold','R_close','compensation','B_reset']:
        m=phase==ph
        if np.sum(m)>1:
            out[f'{label}_negative_{ph}']=float(np.trapezoid(neg[m],t[m]))
            out[f'{label}_positive_{ph}']=float(np.trapezoid(pos[m],t[m]))
            out[f'{label}_min_Tkk_{ph}']=float(np.min(tkk_min_region[m]))
            out[f'{label}_max_Tkk_{ph}']=float(np.max(tkk_max_region[m]))
            out[f'{label}_max_abs_flux_{ph}']=float(np.max(np.abs(d['flux_hat'][m][:,region_mask])))
            out[f'{label}_max_abs_Rt_over_NR_{ph}']=float(np.max(np.abs(d['Rt_over_NR'][m][:,region_mask])))
    return out

def run_case(case,comp_kind,amp,TC=30,TR=10,TB=100,TH=60,comp_center=2.5,comp_width=0.8,N_shape='ring'):
    l=np.linspace(-20,20,401)
    t_end=2*TB+2*TR+TH+TC
    dt=min(TR,TC,TH)/40
    t=np.linspace(0,t_end,int(math.ceil(t_end/dt))+1)
    B,R,N,explicit,phase,times=make_fields(t,l,TB=TB,TR=TR,TH=TH,TC=TC,comp_kind=comp_kind,amp=amp,comp_center=comp_center,comp_width=comp_width,N_shape=N_shape)
    d=diagnostics(t,l,B,R,N,explicit)
    core=np.abs(l)<=0.25
    access=np.abs(l)<=0.25
    support=np.abs(l)<=0.65
    shoulder=(np.abs(l)>=1.2)&(np.abs(l)<=4.0)
    row=dict(case=case,comp_kind=comp_kind,amp=amp,TC=TC,TR=TR,TB=TB,TH=TH,comp_center=comp_center,comp_width=comp_width)
    # observer ledgers
    for label,mask in [('core',core),('support',support),('shoulder',shoulder),('access',access)]:
        row.update(exposure_stats(t,l,phase,d,mask,label))
    # access contamination during open access hold only
    hold=phase=='hold'
    row['access_hold_max_abs_flux']=float(np.max(np.abs(d['flux_hat'][hold][:,access])))
    row['access_hold_max_abs_Rt_over_NR']=float(np.max(np.abs(d['Rt_over_NR'][hold][:,access])))
    row['access_hold_min_Tkk']=float(np.min(d['Tkk_min'][hold][:,access]))
    # compensation leakage to access core after closure
    comp=phase=='compensation'
    row['access_comp_positive']=row.get('access_positive_compensation',0.0)
    row['access_comp_negative']=row.get('access_negative_compensation',0.0)
    row['access_comp_max_abs_flux']=float(np.max(np.abs(d['flux_hat'][comp][:,access]))) if np.any(comp) else 0.0
    row['access_comp_max_abs_Rt_over_NR']=float(np.max(np.abs(d['Rt_over_NR'][comp][:,access]))) if np.any(comp) else 0.0
    # signed balance: does positive after closure exceed open negative in same region?
    for label in ['core','support','shoulder','access']:
        neg_open=sum(row.get(f'{label}_negative_{ph}',0.0) for ph in ['R_open','hold','R_close'])
        pos_comp=row.get(f'{label}_positive_compensation',0.0)
        row[f'{label}_open_negative']=neg_open
        row[f'{label}_comp_positive']=pos_comp
        row[f'{label}_comp_to_open_neg_ratio']=pos_comp/neg_open if neg_open>0 else float('inf')
    return row

def main(outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    rows=[]
    # baseline with compensation phase but no added compensation
    rows.append(run_case('baseline_flare_gated_with_idle_comp','none',0.0,TC=30,TR=10))
    # shoulder R scan: positive/negative amplitudes, ring away from access
    for amp in [-0.25,-0.15,-0.08,0.08,0.15,0.25]:
        rows.append(run_case(f'shoulder_R_amp_{amp:+.2f}','shoulder_R',amp,TC=30,TR=10,comp_center=2.5,comp_width=0.8))
    # lapse scans: ring and core after closure
    for kind in ['lapse_N_ring','lapse_N_core']:
        for amp in [-0.7,-0.4,-0.2,0.2,0.4,0.7]:
            rows.append(run_case(f'{kind}_amp_{amp:+.2f}',kind,amp,TC=30,TR=10,comp_center=2.5,comp_width=0.8))
    # explicit source overlays, with amplitude chosen by area ranges
    for kind in ['explicit_source_ring','explicit_source_core']:
        for amp in [0.002,0.004,0.008,0.012,0.02]:
            rows.append(run_case(f'{kind}_amp_{amp:.3f}',kind,amp,TC=30,TR=10,comp_center=2.5,comp_width=0.8))
    # explicit core duration variants around amp 0.008
    for TC in [10,20,30,60]:
        rows.append(run_case(f'explicit_source_core_amp_0.008_TC{TC:g}','explicit_source_core',0.008,TC=TC,TR=10))
    df=pd.DataFrame(rows)
    df.to_csv(outdir/'compensation_case_summary.csv',index=False)
    # make compact rankings
    columns=['case','comp_kind','amp','TC','core_open_negative','core_comp_positive','core_comp_to_open_neg_ratio','support_open_negative','support_comp_positive','support_comp_to_open_neg_ratio','shoulder_open_negative','shoulder_comp_positive','shoulder_comp_to_open_neg_ratio','access_hold_max_abs_flux','access_hold_max_abs_Rt_over_NR','access_comp_positive','access_comp_negative','access_comp_max_abs_flux','access_comp_max_abs_Rt_over_NR','shoulder_max_abs_flux_compensation','access_max_abs_flux_compensation']
    cols=[c for c in columns if c in df.columns]
    df[cols].to_csv(outdir/'compensation_compact_ranking.csv',index=False)
    # summaries by class
    summ=[]
    for kind,g in df.groupby('comp_kind'):
        # best for core ratio with low access comp flux
        gg=g.copy()
        # exclude huge access comp dynamic maybe threshold flux 2e-3, rt 2e-2
        gg['access_comp_quiet']=(gg['access_comp_max_abs_flux']<2e-3)&(gg['access_comp_max_abs_Rt_over_NR']<2e-2)
        best=gg.sort_values(['core_comp_to_open_neg_ratio','support_comp_to_open_neg_ratio'],ascending=False).iloc[0]
        bestq=gg[gg['access_comp_quiet']].sort_values(['core_comp_to_open_neg_ratio','support_comp_to_open_neg_ratio'],ascending=False).head(1)
        row={'comp_kind':kind,'n':len(g),'best_case':best['case'],'best_core_ratio':float(best['core_comp_to_open_neg_ratio']),'best_support_ratio':float(best['support_comp_to_open_neg_ratio']),'best_access_comp_flux':float(best['access_comp_max_abs_flux']),'best_access_comp_Rt':float(best['access_comp_max_abs_Rt_over_NR'])}
        if len(bestq):
            b=bestq.iloc[0]
            row.update(best_quiet_case=b['case'],best_quiet_core_ratio=float(b['core_comp_to_open_neg_ratio']),best_quiet_support_ratio=float(b['support_comp_to_open_neg_ratio']),best_quiet_access_comp_flux=float(b['access_comp_max_abs_flux']),best_quiet_access_comp_Rt=float(b['access_comp_max_abs_Rt_over_NR']))
        summ.append(row)
    pd.DataFrame(summ).to_csv(outdir/'compensation_class_summary.csv',index=False)
    # write memo
    memo=r'''# Compensation Branch Screen for Flare-Gated Radial Stretch

## Purpose

This reduced screen tests three actuator families for positive compensation after the flare-gated access interval while preserving the access observer family:

1. shoulder-only areal-radius motion, denoted `shoulder_R`;
2. lapse modulation, denoted `lapse_N_ring` and `lapse_N_core`;
3. explicit positive source overlays, denoted `explicit_source_ring` and `explicit_source_core`.

The base protocol is:

```math
B\text{-setup} \rightarrow R\text{-open} \rightarrow \text{quiet hold} \rightarrow R\text{-close} \rightarrow \text{compensation} \rightarrow B\text{-reset}.
```

During compensation, the flare is flattened (`R` is in the standby profile) and the access interval has ended. This screen therefore separates support/source repayment from access-observer exposure.

## Model

The geometry screen uses

```math
ds^2=-N(l,t)^2dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The base branch uses `B0=8`, `wB=8`, `wR=5`, `TR=10`, `TH=60`, and `TB=100`. The compensation window has default duration `TC=30`. The source proxy is reconstructed from `G_{mu nu}/8pi`. Explicit source overlays are added as ledger terms to both radial null directions and are marked as source terms that require later backreaction and state-construction gates.

## Main result

The three actuator families separate cleanly.

### Shoulder R

Shoulder-only `R` motion creates geometric compensation structure away from the access core. It also creates shoulder flux and mixed null-stress histories. Its best assignment is transition shaping, buffer control, and compensation support around the shoulders.

### Lapse N

Lapse modulation gives a timing and matching handle. In the reduced scan it produces local stress structure through gradients and time dependence. Ring lapse preserves access isolation better than core lapse; core lapse couples directly to the support observer. The strongest role for `N` is scheduler, redshift/matching actuator, and co-control for a source term.

### Explicit source terms

The explicit post-closure source overlay is the cleanest compensation mechanism in this reduced ledger. A core/support-local positive pulse after `R_close` can overcompensate the open-interval negative source history while the access interval is already closed. A shoulder-local explicit source pulse manages shoulder/global ledgers while keeping the access core quiet.

## Interpretation

The preferred next architecture is:

```math
B\text{-prestretch} + R\text{-flare gate} + \text{post-closure explicit source compensation},
```

with shoulder `R` and lapse `N` assigned to shaping, matching, buffering, and timing.

The result advances the screening framework allocation:

- `B` carries radial support dilution;
- `R` gates flare/access state and shoulder transitions;
- `N` gates timing, redshift, and matching;
- explicit source terms carry the repayment ledger.

The branch now advances to quantum-interest, state-construction, backreaction, and stability gates. The positive source overlay is a ledger candidate awaiting a physical source model.
'''
    (outdir/'MEMO_compensation_branch_screen.md').write_text(memo)
    # write extracts json
    def rec(case):
        r=df[df.case.eq(case)].iloc[0].replace({np.nan:None}).to_dict()
        return {k:(float(v) if isinstance(v,(np.floating,)) else v) for k,v in r.items() if k in ['case','comp_kind','amp','TC','core_open_negative','core_comp_positive','core_comp_to_open_neg_ratio','support_open_negative','support_comp_positive','support_comp_to_open_neg_ratio','access_hold_max_abs_flux','access_comp_positive','access_comp_negative','access_comp_max_abs_flux','access_comp_max_abs_Rt_over_NR','shoulder_comp_positive','shoulder_comp_to_open_neg_ratio']}
    extracts={'design_name':'compensated flare-gated radial stretch','main_result':'Explicit post-closure source compensation is the cleanest positive-compensation branch in the reduced ledger; shoulder R and lapse N are useful shaping/matching actuators but create mixed geometric histories when used alone as repayment.', 'selected_cases':[]}
    for c in ['baseline_flare_gated_with_idle_comp','explicit_source_core_amp_0.004','explicit_source_core_amp_0.008','explicit_source_ring_amp_0.008','lapse_N_ring_amp_+0.40','shoulder_R_amp_+0.15']:
        if c in set(df.case): extracts['selected_cases'].append(rec(c))
    (outdir/'extracts.json').write_text(json.dumps(extracts,indent=2))
    # copy script
    script_path=Path(__file__)
    if script_path.exists():
        (outdir/'run_compensation_branch_screen.py').write_text(script_path.read_text())
    # manifest
    files=[]
    for p in sorted(outdir.iterdir()):
        if p.is_file():
            files.append({'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    (outdir/'manifest.json').write_text(json.dumps({'bundle':'compensated_flare_gated_radial_stretch','created':'2026-05-12','files':files},indent=2))

if __name__=='__main__':
    main('/mnt/data/compensated_flare_gated_radial_stretch')
