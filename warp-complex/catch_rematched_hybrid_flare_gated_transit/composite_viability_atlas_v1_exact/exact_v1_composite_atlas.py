#!/usr/bin/env python3
"""
Reduced exact-v1 composite viability atlas.

Scope: items 1--4 only.
1. Exact v1 B,R,N throat controls from Reference Geometry v0.3 functions.
2. Catch-rematched throat-loaded packet worldtube checks.
3. Choreography basin map over catch/shift/throat-release timing.
4. Support-edge sweep over edge gating, B/N strength, and R treatment.

This is a reduced prescribed-metric diagnostic harness. It does not compute ADM constraints,
solve matter field equations, or evolve Einstein equations.
"""
from __future__ import annotations
import json, math, hashlib
from pathlib import Path
from dataclasses import dataclass, asdict
import numpy as np

OUT = Path('/mnt/data/composite_viability_atlas_v1_exact')
OUT.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Exact v1 geometry functions
# -----------------------------
PARAMS = {
    "label": "Reference Geometry v0.3 candidate",
    "B0": 8.0,
    "wB": 10.0,
    "T_B": 150.0,
    "T_R": 5.0,
    "T_H": 60.0,
    "T_C": 20.0,
    "T_Breset": 150.0,
    "Rc": 1.0,
    "wFlat": 1.6,
    "r_sh_amp": 0.0,
    "r_sh_center": 2.5,
    "r_sh_width": 1.2,
    "n_sh_amp": -0.18,
    "n_sh_center": 2.3,
    "n_sh_width": 1.0,
}

def minjerk(x):
    x = np.clip(x, 0.0, 1.0)
    return 10*x**3 - 15*x**4 + 6*x**5

def pulse_smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return 16*x**2*(1-x)**2

def radius_access(l, a=1.0):
    return np.sqrt(a*a + l*l)

def window_core(l, width, power=4):
    return np.exp(-(np.abs(l)/width)**power)

def window_shoulder(l, center=2.5, width=0.9, power=4):
    return np.exp(-((np.abs(l)-center)/width)**power)

def A_sequence(t, T_B=150.0, T_R=5.0, T_H=60.0, T_C=20.0, T_Breset=150.0):
    t = np.asarray(t)
    t1=T_B; t2=t1+T_R; t3=t2+T_H; t4=t3+T_R; t5=t4+T_C; t6=t5+T_Breset
    A_B=np.zeros_like(t,dtype=float)
    A_R=np.zeros_like(t,dtype=float)
    C=np.zeros_like(t,dtype=float)
    phase=np.full(t.shape,'off',dtype=object)
    m=(t>=0)&(t<t1); A_B[m]=minjerk(t[m]/T_B); phase[m]='B_setup'
    m=(t>=t1)&(t<t5); A_B[m]=1; phase[m]='open_or_comp_window'
    m=(t>=t5)&(t<=t6); A_B[m]=minjerk((t6-t[m])/T_Breset); phase[m]='B_reset'
    m=(t>=t1)&(t<t2); A_R[m]=minjerk((t[m]-t1)/T_R); phase[m]='R_open'
    m=(t>=t2)&(t<t3); A_R[m]=1; phase[m]='hold'
    m=(t>=t3)&(t<t4); A_R[m]=minjerk((t4-t[m])/T_R); phase[m]='R_close'
    m=(t>=t4)&(t<t5); A_R[m]=0; C[m]=pulse_smooth((t[m]-t4)/T_C); phase[m]='comp'
    return A_B, A_R, C, phase, (t1,t2,t3,t4,t5,t6)

def make_geometry_exact(t, l, params=PARAMS, eta_B=1.0, eta_N=1.0, R_mode='v1', R_amp=1.0):
    B0=params.get('B0',8.0); wB=params.get('wB',10.0)
    Rc=params.get('Rc',1.0); wFlat=params.get('wFlat',1.6)
    T_B=params.get('T_B',150.0); T_R=params.get('T_R',5.0)
    T_H=params.get('T_H',60.0); T_C=params.get('T_C',20.0); T_Breset=params.get('T_Breset',T_B)
    r_sh_amp=params.get('r_sh_amp',0.0); r_sh_center=params.get('r_sh_center',2.5); r_sh_width=params.get('r_sh_width',1.2)
    n_sh_amp=params.get('n_sh_amp',-0.18); n_sh_center=params.get('n_sh_center',2.3); n_sh_width=params.get('n_sh_width',1.0)
    A_B,A_R,C,phase,times=A_sequence(t,T_B,T_R,T_H,T_C,T_Breset)
    if R_mode == 'always_open':
        A_R = np.ones_like(A_R)
    elif R_mode == 'always_flat':
        A_R = np.zeros_like(A_R)
    elif R_mode == 'half_amplitude':
        A_R = 0.5*A_R
    elif R_mode == 'delayed_close':
        # Hold the open state deeper into the release interval, then close smoothly.
        t1,t2,t3,t4,t5,t6=times
        A_R2=np.zeros_like(t,dtype=float)
        m=t<t3; A_R2[m]=A_R[m]
        delay=0.5*(t5-t4)
        close_start=t4+delay
        close_end=t5
        m=(t>=t3)&(t<close_start); A_R2[m]=1.0
        m=(t>=close_start)&(t<close_end); A_R2[m]=minjerk((close_end-t[m])/(close_end-close_start))
        A_R=A_R2
    F_B=window_core(l,wB)[None,:]
    B=1+eta_B*(B0-1)*A_B[:,None]*F_B
    R_acc=radius_access(l)[None,:]
    W_flat=window_core(l,wFlat)[None,:]
    R_stand=R_acc+W_flat*(Rc-R_acc)
    H_R=window_shoulder(l,r_sh_center,r_sh_width)[None,:]
    R=R_stand + R_amp*A_R[:,None]*(R_acc-R_stand) + r_sh_amp*C[:,None]*H_R
    H_N=window_shoulder(l,n_sh_center,n_sh_width)[None,:]
    N=1 + eta_N*n_sh_amp*C[:,None]*H_N
    return N,B,R,phase,times,C,A_R

# -----------------------------
# Composite packet functions
# -----------------------------
def falloff(z,w):
    return 0.5*(1.0-np.tanh(z/w))

def bump_sq(x2,R,w):
    return 0.5*(1.0-np.tanh((x2-R*R)/(2.0*R*w)))

@dataclass
class CompositeParams:
    V: float = 5.0
    lam: float | None = None
    v_exit: float = 0.5
    C0: float = 100.0
    x_catch: float = 0.15
    x_beta: float = 0.70
    x_q: float = 1.25
    w_catch: float = 0.16
    w_beta: float = 0.18
    w_q: float = 0.18
    p_beta: float = 1.0
    Rth: float = 1.0
    Rpass: float = 0.35
    eta_B: float = 1.0
    eta_N: float = 1.0
    R_mode: str = 'v1'
    R_amp: float = 1.0
    s_min: float = -0.35
    s_max: float = 1.65

    def resolved_lam(self):
        return max(1.05, 1.15*self.V) if self.lam is None else self.lam


def v1_time_from_progress(s, params=PARAMS, s_min=-0.35, s_max=1.65):
    # Align packet traversal with the exact v1 open interval: hold start through R-close end.
    # s_min -> hold start, s_max -> R_close end.
    t1 = params['T_B']; t2=t1+params['T_R']; t3=t2+params['T_H']; t4=t3+params['T_R']
    frac=(s-s_min)/(s_max-s_min)
    return t2 + frac*(t4-t2)

def scan_composite(cp: CompositeParams, Ns=161, Nl=261, curvature_proxy=False):
    ss=np.linspace(cp.s_min,cp.s_max,Ns)
    ls=np.linspace(-1.75,2.05,Nl)
    Sg,Lg=np.meshgrid(ss,ls,indexing='ij')
    trow=v1_time_from_progress(ss, s_min=cp.s_min, s_max=cp.s_max)
    # exact v1 controls for all s,l
    N,B,R,phase,times,C,A_R=make_geometry_exact(trow,ls,eta_B=cp.eta_B,eta_N=cp.eta_N,R_mode=cp.R_mode,R_amp=cp.R_amp)
    Ccatch=falloff(Sg-cp.x_catch,cp.w_catch)
    U=cp.v_exit+(cp.V-cp.v_exit)*Ccatch
    E=falloff(Sg-cp.x_beta,cp.w_beta)
    q=falloff(Sg-cp.x_q,cp.w_q)
    W=bump_sq(Lg*Lg,cp.Rth,0.12)
    Sp=bump_sq((Lg-Sg)*(Lg-Sg)+1e-10,cp.Rpass,0.06)
    A=np.exp(q*W*np.log(cp.C0))
    T=np.exp(q*W*np.log(cp.resolved_lam()*cp.C0))
    beta=-U*E*(W**cp.p_beta)*Sp/B
    alpha=N*T
    gll=(B*A)**2
    gtt=-alpha**2+gll*beta**2
    gtl=gll*beta
    # Coordinate velocity consistent with previous reduced packet harness.
    vcoord=U/B
    norm=gtt+2*gtl*vcoord+gll*vcoord*vcoord
    packet=np.abs(Lg-Sg)<=cp.Rpass
    center=np.abs(Lg-Sg)<=0.04
    support_edge=(Sp>0.08)&(W>0.05)&(W<0.85)
    release=(Sg>min(cp.x_catch,cp.x_beta)-0.20)&(Sg<cp.x_q+0.35)
    edge_rel=support_edge&release
    def smax(a,m):
        vals=np.where(m,a,np.nan)
        return float(np.nanmax(vals))
    def smin(a,m):
        vals=np.where(m,a,np.nan)
        return float(np.nanmin(vals))
    def locmax(a,m):
        vals=np.where(m,a,-np.inf)
        idx=np.unravel_index(np.nanargmax(vals), vals.shape)
        return float(ss[idx[0]]), float(ls[idx[1]]), float(vals[idx])
    # flare/area stats from exact R_eff=A*R
    Reff=A*R
    d2_vals=[]; lmins=[]; rmins=[]
    dl=ls[1]-ls[0]
    for i in range(len(ss)):
        j=int(np.argmin(Reff[i]**2)); lmins.append(ls[j]); rmins.append(Reff[i,j])
        if 0<j<len(ls)-1:
            d2_vals.append(((Reff[i,j+1]**2)-2*(Reff[i,j]**2)+(Reff[i,j-1]**2))/(dl*dl))
    # light curvature/shape proxies through finite differences
    # The radial derivatives are cheap and provide edge-shaping information for item 4.
    Rl=np.gradient(R,ls,axis=1,edge_order=2)
    Rll=np.gradient(Rl,ls,axis=1,edge_order=2)
    dlogB=np.gradient(np.log(B),ls,axis=1,edge_order=2)
    dlogN=np.gradient(np.log(np.maximum(N,1e-12)),ls,axis=1,edge_order=2)
    shape_proxy=np.abs(Rll)+np.abs(dlogB)+np.abs(dlogN)
    norm_loc=locmax(norm,packet)
    edge_loc=locmax(gtt,edge_rel)
    out={
        **asdict(cp),
        'lam': cp.resolved_lam(),
        'packet_max_norm': smax(norm,packet),
        'center_max_norm': smax(norm,center),
        'packet_norm_positive_points': int(np.sum((norm>0)&packet)),
        'center_norm_positive_points': int(np.sum((norm>0)&center)),
        'packet_max_gtt': smax(gtt,packet),
        'packet_gtt_positive_points': int(np.sum((gtt>0)&packet)),
        'edge_max_gtt': smax(gtt,support_edge),
        'release_edge_max_gtt': smax(gtt,edge_rel),
        'edge_gtt_positive_points': int(np.sum((gtt>0)&support_edge)),
        'release_edge_gtt_positive_points': int(np.sum((gtt>0)&edge_rel)),
        'min_packet_margin': smin(alpha-np.sqrt(gll)*np.abs(beta),packet),
        'min_edge_margin': smin(alpha-np.sqrt(gll)*np.abs(beta),support_edge),
        'packet_norm_s_at_max': norm_loc[0],
        'packet_norm_l_at_max': norm_loc[1],
        'edge_gtt_s_at_max': edge_loc[0],
        'edge_gtt_l_at_max': edge_loc[1],
        'min_flare_d2_Reff2': float(np.nanmin(d2_vals)),
        'median_flare_d2_Reff2': float(np.nanmedian(d2_vals)),
        'throat_min_l_maxabs': float(np.max(np.abs(lmins))),
        'throat_min_Reff_min': float(np.min(rmins)),
        'edge_shape_proxy_max': smax(shape_proxy,support_edge),
        'packet_shape_proxy_max': smax(shape_proxy,packet),
        'R_l_edge_maxabs': smax(np.abs(Rl),support_edge),
        'R_ll_edge_maxabs': smax(np.abs(Rll),support_edge),
        'dlogB_edge_maxabs': smax(np.abs(dlogB),support_edge),
        'dlogN_edge_maxabs': smax(np.abs(dlogN),support_edge),
    }
    out['packet_clear']=bool(out['packet_norm_positive_points']==0 and out['center_norm_positive_points']==0)
    out['edge_clear']=bool(out['release_edge_gtt_positive_points']==0)
    out['flare_clear']=bool(out['min_flare_d2_Reff2']>0)
    out['clear']=bool(out['packet_clear'] and out['edge_clear'] and out['flare_clear'])
    return out

def run_baselines():
    cases=[]
    for V,lam in [(2.5,None),(5.0,None),(10.0,None),(5.0,3.0),(10.0,6.0)]:
        for R_mode in ['v1','always_open','always_flat','half_amplitude','delayed_close']:
            cp=CompositeParams(V=V,lam=lam,R_mode=R_mode)
            cases.append(scan_composite(cp,Ns=121,Nl=221))
    return cases

def run_choreography_basin():
    rows=[]
    scenarios=[('V5_nominal',5.0,None),('V5_low_lapse',5.0,3.0),('V10_nominal',10.0,None),('V10_low_lapse',10.0,6.0)]
    for name,V,lam in scenarios:
        for x_catch in np.round(np.linspace(-0.05,0.95,11),3):
            for x_beta in np.round(np.linspace(0.35,1.05,8),3):
                for x_q in np.round(np.linspace(0.75,1.45,8),3):
                    if x_q <= x_beta+0.05: continue
                    cp=CompositeParams(V=V,lam=lam,x_catch=float(x_catch),x_beta=float(x_beta),x_q=float(x_q),R_mode='v1')
                    r=scan_composite(cp,Ns=81,Nl=151)
                    r['scenario']=name
                    r['catch_before_beta']=bool(x_catch < x_beta)
                    r['beta_before_q']=bool(x_beta < x_q)
                    r['catch_margin']=float(x_beta-x_catch)
                    r['release_margin']=float(x_q-x_beta)
                    rows.append(r)
    return rows

def summarize_basin(rows):
    out=[]
    for sc in sorted(set(r['scenario'] for r in rows)):
        rr=[r for r in rows if r['scenario']==sc]
        clear=[r for r in rr if r['clear']]
        packet_clear=[r for r in rr if r['packet_clear']]
        # thresholds among clear rows
        def safe_min(key, arr=clear):
            return float(np.min([r[key] for r in arr])) if arr else None
        def safe_max(key, arr=clear):
            return float(np.max([r[key] for r in arr])) if arr else None
        out.append({
            'scenario': sc,
            'evaluated': len(rr),
            'clear': len(clear),
            'packet_clear': len(packet_clear),
            'clear_fraction': len(clear)/len(rr) if rr else 0.0,
            'packet_clear_fraction': len(packet_clear)/len(rr) if rr else 0.0,
            'min_clear_catch_margin': safe_min('catch_margin'),
            'min_clear_release_margin': safe_min('release_margin'),
            'max_clear_x_catch': safe_max('x_catch'),
            'max_clear_packet_norm': float(np.max([r['packet_max_norm'] for r in clear])) if clear else None,
            'max_clear_edge_gtt': float(np.max([r['release_edge_max_gtt'] for r in clear])) if clear else None,
        })
    return out

def run_support_edge_sweep():
    rows=[]
    for V,lam,tag in [(10.0,6.0,'V10_low_lapse'),(10.0,None,'V10_nominal'),(5.0,3.0,'V5_low_lapse')]:
        for p_beta in [1.0,1.25,1.5,2.0,3.0,4.0]:
            for eta_B in [0.0,0.5,1.0]:
                for eta_N in [0.0,0.5,1.0]:
                    for R_mode in ['v1','always_open','delayed_close']:
                        cp=CompositeParams(V=V,lam=lam,p_beta=p_beta,eta_B=eta_B,eta_N=eta_N,R_mode=R_mode)
                        r=scan_composite(cp,Ns=91,Nl=181)
                        r['scenario']=tag
                        rows.append(r)
    return rows

def summarize_edge(rows):
    out=[]
    for sc in sorted(set(r['scenario'] for r in rows)):
        rr=[r for r in rows if r['scenario']==sc]
        clear=[r for r in rr if r['clear']]
        # top 10 by edge margin among clear cases, then shape proxy.
        top=sorted(clear, key=lambda r: (r['min_edge_margin'], -r['edge_shape_proxy_max']), reverse=True)[:10]
        out.append({
            'scenario': sc,
            'evaluated': len(rr),
            'clear': len(clear),
            'clear_fraction': len(clear)/len(rr) if rr else 0.0,
            'best_clear': [
                {
                    'p_beta': r['p_beta'], 'eta_B': r['eta_B'], 'eta_N': r['eta_N'], 'R_mode': r['R_mode'],
                    'min_edge_margin': r['min_edge_margin'],
                    'release_edge_max_gtt': r['release_edge_max_gtt'],
                    'packet_max_norm': r['packet_max_norm'],
                    'edge_shape_proxy_max': r['edge_shape_proxy_max'],
                    'min_flare_d2_Reff2': r['min_flare_d2_Reff2'],
                } for r in top
            ],
        })
    return out

def write_md(baselines, basin_summary, edge_summary):
    md=[]
    md.append('# Exact-v1 Composite Viability Atlas\n')
    md.append('Reduced tests for the Reference Geometry v0.3 throat controls combined with the catch-rematched throat-loaded packet.\n')
    md.append('The metric used in the screen is\n')
    md.append('```math\n')
    md.append('ds^2=-\\alpha^2 ds^2+\\gamma_{ll}(dl+\\beta^l ds)^2+\\gamma_{\\Omega\\Omega}d\\Omega^2\n')
    md.append('```\n')
    md.append('with exact v1 controls $N_{v1}$, $B_{v1}$, and $R_{v1}$, packet lapse/capacity factors, and catch-rematched throat-gated shift.\n')
    md.append('```math\n')
    md.append('\\alpha=N_{v1}T_{pkt},\\qquad \\gamma_{ll}=(B_{v1}A_{pkt})^2,\\qquad \\gamma_{\\Omega\\Omega}=(R_{v1}A_{pkt})^2\n')
    md.append('```\n')
    md.append('```math\n')
    md.append('\\beta^l=-U(s)E(s)W(l)^{p_\\beta}S(l-X(s))/B_{v1}\n')
    md.append('```\n')
    md.append('## Baseline and R-state checks\n')
    md.append('| V | lambda | R mode | packet clear | edge clear | flare clear | packet max norm | release edge max gtt | min edge margin | min flare d2 |\n')
    md.append('|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|\n')
    for r in baselines:
        md.append(f"| {r['V']:.3g} | {r['lam']:.3g} | {r['R_mode']} | {int(r['packet_clear'])} | {int(r['edge_clear'])} | {int(r['flare_clear'])} | {r['packet_max_norm']:.4g} | {r['release_edge_max_gtt']:.4g} | {r['min_edge_margin']:.4g} | {r['min_flare_d2_Reff2']:.4g} |\n")
    md.append('\n## Choreography basin summary\n')
    md.append('| scenario | evaluated | clear | clear fraction | packet clear fraction | min clear catch margin | min clear release margin | max clear x_catch |\n')
    md.append('|---|---:|---:|---:|---:|---:|---:|---:|\n')
    for s in basin_summary:
        md.append(f"| {s['scenario']} | {s['evaluated']} | {s['clear']} | {s['clear_fraction']:.3f} | {s['packet_clear_fraction']:.3f} | {s['min_clear_catch_margin']} | {s['min_clear_release_margin']} | {s['max_clear_x_catch']} |\n")
    md.append('\n## Support-edge sweep summary\n')
    for s in edge_summary:
        md.append(f"\n### {s['scenario']}\n\n")
        md.append(f"Evaluated {s['evaluated']} support-edge configurations; {s['clear']} clear.\n\n")
        md.append('| p_beta | eta_B | eta_N | R mode | min edge margin | release edge max gtt | packet max norm | edge shape proxy | min flare d2 |\n')
        md.append('|---:|---:|---:|---|---:|---:|---:|---:|---:|\n')
        for r in s['best_clear']:
            md.append(f"| {r['p_beta']:.3g} | {r['eta_B']:.3g} | {r['eta_N']:.3g} | {r['R_mode']} | {r['min_edge_margin']:.4g} | {r['release_edge_max_gtt']:.4g} | {r['packet_max_norm']:.4g} | {r['edge_shape_proxy_max']:.4g} | {r['min_flare_d2_Reff2']:.4g} |\n")
    md.append('\n## Design readout\n')
    md.append('The combined design operates through packet timelikeness, support-edge margin, and timed catch/shift/throat release. The v1 throat controls supply bounded infrastructure profiles. The catch-rematched packet supplies the moving protected service worldtube.\n')
    md.append('\nFiles: `exact_v1_composite_atlas.py`, `baselines.json`, `choreography_basin.json`, `choreography_basin_summary.json`, `support_edge_sweep.json`, `support_edge_sweep_summary.json`.\n')
    (OUT/'SUMMARY.md').write_text(''.join(md), encoding='utf-8')

def manifest():
    lines=[]
    for p in sorted(OUT.glob('*')):
        if p.is_file():
            h=hashlib.sha256(p.read_bytes()).hexdigest()
            lines.append(f'{h}  {p.name}\n')
    (OUT/'MANIFEST.sha256').write_text(''.join(lines), encoding='utf-8')

def main():
    baselines=run_baselines()
    (OUT/'baselines.json').write_text(json.dumps(baselines,indent=2), encoding='utf-8')
    basin=run_choreography_basin()
    basin_summary=summarize_basin(basin)
    (OUT/'choreography_basin.json').write_text(json.dumps(basin,indent=2), encoding='utf-8')
    (OUT/'choreography_basin_summary.json').write_text(json.dumps(basin_summary,indent=2), encoding='utf-8')
    edge=run_support_edge_sweep()
    edge_summary=summarize_edge(edge)
    (OUT/'support_edge_sweep.json').write_text(json.dumps(edge,indent=2), encoding='utf-8')
    (OUT/'support_edge_sweep_summary.json').write_text(json.dumps(edge_summary,indent=2), encoding='utf-8')
    # save source code into bundle
    src=Path(__file__).read_text(encoding='utf-8') if '__file__' in globals() else ''
    (OUT/'exact_v1_composite_atlas.py').write_text(src, encoding='utf-8')
    write_md(baselines,basin_summary,edge_summary)
    manifest()
    print(OUT/'SUMMARY.md')
    print(json.dumps(basin_summary,indent=2))
    print(json.dumps(edge_summary,indent=2)[:5000])

if __name__ == '__main__':
    main()
