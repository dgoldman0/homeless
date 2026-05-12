#!/usr/bin/env python3
"""
Reduced screen for shoulder-optimized compensated flare-gated radial stretch.

Metric family:
    ds^2 = -N(l,t)^2 dt^2 + B(l,t)^2 dl^2 + R(l,t)^2 dOmega^2

Lifecycle:
    B prestretch -> R flare open -> quiet hold -> R closure ->
    compensation phase with shoulder R/N shaping and explicit source overlay ->
    B reset

This is a prescribed-geometry/effective-source screen. It evaluates observer-family
ledgers and geometry proxies; it is not a quantum-state construction.
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
import pandas as pd

def minjerk(x):
    x=np.clip(x,0,1)
    return 10*x**3-15*x**4+6*x**5

def pulse_smooth(x):
    x=np.clip(x,0,1)
    return 16*x**2*(1-x)**2

def radius_access(l,a=1.0):
    return np.sqrt(a*a+l*l)

def window_core(l,width,power=4):
    return np.exp(-(np.abs(l)/width)**power)

def window_shoulder(l,center=2.5,width=0.9,power=4):
    return np.exp(-((np.abs(l)-center)/width)**power)

def A_sequence(t, T_B=100, T_R=10, T_H=60, T_C=20, T_Breset=100):
    t=np.asarray(t)
    t1=T_B; t2=t1+T_R; t3=t2+T_H; t4=t3+T_R; t5=t4+T_C; t6=t5+T_Breset
    A_B=np.zeros_like(t,dtype=float)
    A_R=np.zeros_like(t,dtype=float)
    C=np.zeros_like(t,dtype=float)
    phase=np.full(t.shape,'off',dtype=object)
    m=(t>=0)&(t<t1); A_B[m]=minjerk(t[m]/T_B); phase[m]='B_setup'
    m=(t>=t1)&(t<t5); A_B[m]=1
    m=(t>=t5)&(t<=t6); A_B[m]=minjerk((t6-t[m])/T_Breset); phase[m]='B_reset'
    m=(t>=t1)&(t<t2); A_R[m]=minjerk((t[m]-t1)/T_R); phase[m]='R_open'
    m=(t>=t2)&(t<t3); A_R[m]=1; phase[m]='hold'
    m=(t>=t3)&(t<t4); A_R[m]=minjerk((t4-t[m])/T_R); phase[m]='R_close'
    m=(t>=t4)&(t<t5); A_R[m]=0; C[m]=pulse_smooth((t[m]-t4)/T_C); phase[m]='comp'
    return A_B,A_R,C,phase,(t1,t2,t3,t4,t5,t6)

def make_geometry(t,l,params):
    B0=params.get('B0',8.0); wB=params.get('wB',8.0)
    Rc=params.get('Rc',1.0); wFlat=params.get('wFlat',1.6)
    T_B=params.get('T_B',100.0); T_R=params.get('T_R',10.0)
    T_H=params.get('T_H',60.0); T_C=params.get('T_C',20.0); T_Breset=params.get('T_Breset',T_B)
    r_sh_amp=params.get('r_sh_amp',0.0); r_sh_center=params.get('r_sh_center',2.5); r_sh_width=params.get('r_sh_width',0.9)
    n_sh_amp=params.get('n_sh_amp',0.0); n_sh_center=params.get('n_sh_center',2.5); n_sh_width=params.get('n_sh_width',0.9)
    A_B,A_R,C,phase,times=A_sequence(t,T_B,T_R,T_H,T_C,T_Breset)
    F_B=window_core(l,wB)[None,:]
    B=1+(B0-1)*A_B[:,None]*F_B
    R_acc=radius_access(l)[None,:]
    W_flat=window_core(l,wFlat)[None,:]
    R_stand=R_acc + W_flat*(Rc - R_acc)
    H_R=window_shoulder(l,r_sh_center,r_sh_width)[None,:]
    R=R_stand + A_R[:,None]*(R_acc-R_stand) + r_sh_amp*C[:,None]*H_R
    H_N=window_shoulder(l,n_sh_center,n_sh_width)[None,:]
    N=1 + n_sh_amp*C[:,None]*H_N
    return N,B,R,phase,times,C

def diagnostics_general(t,l,N,B,R):
    Nt=np.gradient(N,t,axis=0,edge_order=2); Nl=np.gradient(N,l,axis=1,edge_order=2)
    Bt=np.gradient(B,t,axis=0,edge_order=2); Bl=np.gradient(B,l,axis=1,edge_order=2)
    Rt=np.gradient(R,t,axis=0,edge_order=2); Rl=np.gradient(R,l,axis=1,edge_order=2)
    Rtt=np.gradient(Rt,t,axis=0,edge_order=2); Rtl=np.gradient(Rt,l,axis=1,edge_order=2); Rll=np.gradient(Rl,l,axis=1,edge_order=2)
    cov_tt = Rtt - (Nt/N)*Rt - (N*Nl/(B*B))*Rl
    cov_tl = Rtl - (Nl/N)*Rt - (Bt/B)*Rl
    cov_ll = Rll - (B*Bt/(N*N))*Rt - (Bl/B)*Rl
    gradR2 = -(Rt*Rt)/(N*N) + (Rl*Rl)/(B*B)
    boxR = -cov_tt/(N*N) + cov_ll/(B*B)
    Gtt = -2*cov_tt/R - 2*(N*N)*boxR/R + (N*N)*(1-gradR2)/(R*R)
    Gll = -2*cov_ll/R + 2*(B*B)*boxR/R - (B*B)*(1-gradR2)/(R*R)
    Gtl = -2*cov_tl/R
    rho = Gtt/(8*math.pi*N*N)
    pr = Gll/(8*math.pi*B*B)
    flux = Gtl/(8*math.pi*N*B)
    Tkk_plus=rho+pr+2*flux
    Tkk_minus=rho+pr-2*flux
    Tkk_min=np.minimum(Tkk_plus,Tkk_minus)
    Kll = -Bt/(N*B)
    Kth = -Rt/(N*R)
    theta_plus=2/R*(Rt/N + Rl/B)
    theta_minus=2/R*(Rt/N - Rl/B)
    return dict(N=N,B=B,R=R,rho=rho,pr=pr,flux=flux,Tkk_min=Tkk_min,Kll=Kll,Kth=Kth,theta_plus=theta_plus,theta_minus=theta_minus)

def summarize_case(params, n_l=501, n_t=501):
    l=np.linspace(-18,18,n_l)
    T_B=params.get('T_B',100.0); T_R=params.get('T_R',10.0)
    T_H=params.get('T_H',60.0); T_C=params.get('T_C',20.0); T_Breset=params.get('T_Breset',T_B)
    t_end=T_B+2*T_R+T_H+T_C+T_Breset
    t=np.linspace(0,t_end,n_t)
    N,B,R,phase,times,C=make_geometry(t,l,params)
    d=diagnostics_general(t,l,N,B,R)
    src=np.zeros_like(d['Tkk_min'])
    if params.get('src_support_amp',0.0) != 0:
        src += params['src_support_amp']*C[:,None]*window_core(l,params.get('src_support_width',0.9))[None,:]
    if params.get('src_shoulder_amp',0.0) != 0:
        src += params['src_shoulder_amp']*C[:,None]*window_shoulder(l,params.get('src_shoulder_center',2.5),params.get('src_shoulder_width',0.9))[None,:]
    Tkk_total=d['Tkk_min'] + src
    access=np.abs(l)<=0.25
    support=np.abs(l)<=0.75
    shoulder=(np.abs(l)>=1.2)&(np.abs(l)<=4.5)
    masks={'access':access,'support':support,'shoulder':shoulder}
    open_mask=(phase=='R_open')|(phase=='hold')|(phase=='R_close')
    comp_mask=(phase=='comp')
    row={k:params.get(k) for k in ['r_sh_amp','r_sh_center','r_sh_width','n_sh_amp','n_sh_center','n_sh_width','src_support_amp','src_shoulder_amp','T_C','T_R','B0','wB']}
    i0=np.argmin(abs(l))
    for label,tmask in [('open',open_mask),('comp',comp_mask),('all',np.ones_like(t,dtype=bool))]:
        y=Tkk_total[:,i0]
        row[f'coreline_{label}_neg']=float(np.trapezoid(np.maximum(-y[tmask],0),t[tmask])) if np.any(tmask) else 0.0
        row[f'coreline_{label}_pos']=float(np.trapezoid(np.maximum(y[tmask],0),t[tmask])) if np.any(tmask) else 0.0
    for zn,zmask in masks.items():
        y=np.mean(Tkk_total[:,zmask],axis=1)
        for label,tmask in [('open',open_mask),('comp',comp_mask),('all',np.ones_like(t,dtype=bool))]:
            row[f'{zn}_{label}_mean_neg']=float(np.trapezoid(np.maximum(-y[tmask],0),t[tmask])) if np.any(tmask) else 0.0
            row[f'{zn}_{label}_mean_pos']=float(np.trapezoid(np.maximum(y[tmask],0),t[tmask])) if np.any(tmask) else 0.0
    for zn,zmask in masks.items():
        for label,tmask in [('open',open_mask),('comp',comp_mask)]:
            idx=np.ix_(tmask,zmask)
            row[f'{zn}_{label}_max_abs_flux']=float(np.max(np.abs(d['flux'][idx])))
            row[f'{zn}_{label}_max_abs_Kll']=float(np.max(np.abs(d['Kll'][idx])))
            row[f'{zn}_{label}_max_abs_Kth']=float(np.max(np.abs(d['Kth'][idx])))
            row[f'{zn}_{label}_max_abs_theta']=float(max(np.max(np.abs(d['theta_plus'][idx])),np.max(np.abs(d['theta_minus'][idx]))))
            row[f'{zn}_{label}_min_N']=float(np.min(d['N'][idx]))
            row[f'{zn}_{label}_min_R']=float(np.min(d['R'][idx]))
    eps=1e-12
    row['support_repay_ratio']=row['support_comp_mean_pos']/(row['support_open_mean_neg']+eps)
    row['coreline_repay_ratio']=row['coreline_comp_pos']/(row['coreline_open_neg']+eps)
    row['shoulder_repay_ratio']=row['shoulder_comp_mean_pos']/(row['shoulder_open_mean_neg']+eps)
    row['access_comp_leak_metric']=float(max(row.get('access_comp_max_abs_flux',0), row.get('access_comp_max_abs_Kll',0), row.get('access_comp_max_abs_Kth',0)))
    row['shoulder_comp_spike_metric']=float(max(row.get('shoulder_comp_max_abs_flux',0), row.get('shoulder_comp_max_abs_Kll',0), row.get('shoulder_comp_max_abs_Kth',0)))
    ratios=np.array([row['support_repay_ratio'],row['coreline_repay_ratio'],row['shoulder_repay_ratio']])
    row['balance_error']=float(np.sum((ratios-1.05)**2))
    row['valid_access']=row['access_comp_leak_metric']<0.002 and row['access_comp_min_N']>0.6
    row['valid_shoulder']=row['shoulder_comp_min_N']>0.55 and row['shoulder_comp_min_R']>0.5 and row['shoulder_comp_spike_metric']<0.08
    row['valid']=row['valid_access'] and row['valid_shoulder']
    row['score_balanced']=float(-row['balance_error'] - 50*row['access_comp_leak_metric'] - 2*row['shoulder_comp_spike_metric'])
    return row

def run():
    common={'B0':8,'wB':8,'T_B':100,'T_R':10,'T_H':60,'T_C':20}
    rows=[]
    for src_sup in np.linspace(0.0075,0.0095,9):
        for src_sh in np.linspace(0.0010,0.0025,7):
            for r_amp,n_amp,name in [(0,0,'none'),(0.25,0,'Rshape'),(0,0.3,'Nshape'),(0.15,0.2,'RNshape')]:
                params={**common,'src_support_amp':float(src_sup),'src_support_width':0.9,
                        'src_shoulder_amp':float(src_sh),'src_shoulder_center':2.5,'src_shoulder_width':0.9,
                        'r_sh_amp':r_amp,'r_sh_center':2.5,'r_sh_width':1.2,
                        'n_sh_amp':n_amp,'n_sh_center':2.5,'n_sh_width':1.2}
                row=summarize_case(params)
                row['case']=f'sup{src_sup:.4f}_sh{src_sh:.4f}_{name}'
                rows.append(row)
    df=pd.DataFrame(rows)
    out=Path(__file__).resolve().parents[1]/'data'
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out/'balanced_source_shoulder_sweep_reproduced.csv',index=False)
    best=df[df.valid].sort_values('score_balanced',ascending=False).head(15)
    print(best[['case','coreline_repay_ratio','support_repay_ratio','shoulder_repay_ratio','access_comp_leak_metric','shoulder_comp_spike_metric','balance_error']].to_string(index=False))

if __name__ == '__main__':
    run()
