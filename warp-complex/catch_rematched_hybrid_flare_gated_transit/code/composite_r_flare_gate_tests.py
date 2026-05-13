import math, json, time
from dataclasses import dataclass
import numpy as np
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp

# Reduced R-flare-gate diagnostic harness.
# Coordinates x=(s,l,theta,phi), s = reduced transit progress.
# Composite metric: v1-like B/N throat infrastructure + catch-rematched packet shift + R-flare schedule variants.
# Not a constraint-quality solve. It is a comparative diagnostic screen for R-gate demotion.

PARAM_NAMES = [
    'V','v_exit','C0','lam','B0','eta_B','eta_N','hold_scale','p_beta',
    'x_catch','x_beta','x_q','x_R','w_catch','w_rel','w_R','R_amp','Rth','Rpass','r0','eps','R_mode'
]
# R_mode: 0=scheduled falloff, 1=always_open, 2=always_flat

def make_p(V=5.0, lam=None, v_exit=0.5, C0=100.0, B0=8.0, eta_B=1.0, eta_N=1.0,
           hold_scale=1.0, p_beta=1.0, x_R=None, w_R=0.18, R_amp=1.0, R_mode=0):
    if lam is None:
        lam=max(1.05,1.15*V)
    x_catch=0.15
    x_beta=x_catch+0.55*hold_scale
    x_q=x_beta+0.55*hold_scale
    if hold_scale <= 0.0:
        x_beta=x_catch+0.04
        x_q=x_beta+0.04
    if x_R is None:
        x_R=x_q
    return jnp.array([V,v_exit,C0,lam,B0,eta_B,eta_N,hold_scale,p_beta,
                      x_catch,x_beta,x_q,x_R,0.16,0.18,w_R,R_amp,1.0,0.35,1.0,1e-5,R_mode], dtype=jnp.float64)

def unpack(p):
    return {k: float(p[i]) for i,k in enumerate(PARAM_NAMES)}

def bump_sq(x2,R,w):
    z=(x2-R*R)/(2.0*R*w)
    return 0.5*(1.0-jnp.tanh(z))

def falloff(z,w):
    return 0.5*(1.0-jnp.tanh(z/w))

def rise(z,w):
    return 0.5*(1.0+jnp.tanh(z/w))

def scalars(x,p):
    s,l,th,ph=x
    V,v_exit,C0,lam,B0,eta_B,eta_N,hold_scale,p_beta,x_catch,x_beta,x_q,x_R,w_catch,w_rel,w_R,R_amp,Rth,Rpass,r0,eps,R_mode=p
    C=falloff(s-x_catch,w_catch)
    U=v_exit+(V-v_exit)*C
    E=falloff(s-x_beta,w_rel)
    q=falloff(s-x_q,w_rel)
    qR_sched=falloff(s-x_R,w_R)
    qR=jnp.where(R_mode < 0.5, qR_sched, jnp.where(R_mode < 1.5, 1.0, 0.0))
    W=bump_sq(l*l,Rth,0.12)
    S=bump_sq((l-s)*(l-s)+eps*eps,Rpass,0.06)
    A=jnp.exp(q*W*jnp.log(C0))
    T=jnp.exp(q*W*jnp.log(lam*C0))
    B=1.0 + eta_B*(B0-1.0)*W*q
    shoulder=jnp.exp(-((jnp.abs(l)-1.05)/0.35)**2)
    N=jnp.exp(eta_N*0.18*q*shoulder)
    r_open=jnp.sqrt(r0*r0+l*l)
    # Flattened state retains a weak proper-radial areal variation, not an exact cylinder.
    r_flat=r0+0.055*l*l
    Rgeom=r_flat + R_amp*qR*(r_open-r_flat)
    beta=-U*E*(W**p_beta)*S/B
    alpha=N*T
    return U,E,q,qR,W,S,A,T,B,N,Rgeom,beta,alpha

def metric(x,p):
    U,E,q,qR,W,S,A,T,B,N,Rgeom,beta,alpha=scalars(x,p)
    th=x[2]
    gll=(B*A)**2
    goo=(A*Rgeom)**2
    return jnp.array([
        [-alpha*alpha+gll*beta*beta, gll*beta, 0.0, 0.0],
        [gll*beta,                   gll,      0.0, 0.0],
        [0.0,                        0.0,      goo, 0.0],
        [0.0,                        0.0,      0.0, goo*jnp.sin(th)**2],
    ], dtype=jnp.float64)

def R_eff(x,p):
    U,E,q,qR,W,S,A,T,B,N,Rgeom,beta,alpha=scalars(x,p)
    return A*Rgeom

def gamma_conn(x,p):
    g=metric(x,p)
    dg=jax.jacfwd(metric,argnums=0)(x,p)
    ginv=jnp.linalg.inv(g)
    return 0.5*(jnp.einsum('ad,cdb->abc',ginv,dg)+jnp.einsum('ad,bdc->abc',ginv,dg)-jnp.einsum('ad,bcd->abc',ginv,dg))

def raw_diagnostics(x,p):
    g=metric(x,p); ginv=jnp.linalg.inv(g)
    Gam=gamma_conn(x,p)
    dGam=jax.jacfwd(gamma_conn,argnums=0)(x,p)
    deriv=jnp.transpose(dGam,(0,2,3,1))-jnp.transpose(dGam,(0,2,1,3))
    prod1=jnp.einsum('ame,ens->asmn',Gam,Gam)
    prod2=jnp.einsum('ane,ems->asmn',Gam,Gam)
    Riem=deriv+prod1-prod2
    Ric=jnp.einsum('asan->sn',Riem)
    Rsc=jnp.einsum('ab,ab->',ginv,Ric)
    G=Ric-0.5*g*Rsc
    Rdown=jnp.einsum('pa,asmn->psmn',g,Riem)
    Kretsch=jnp.einsum('abcd,efgh,ae,bf,cg,dh->',Rdown,Rdown,ginv,ginv,ginv,ginv)
    U,E,q,qR,W,S,A,T,B,N,Rgeom,beta,alpha=scalars(x,p)
    sqrt_gll=B*A
    n=jnp.array([1.0/alpha, -beta/alpha, 0.0, 0.0])
    el=jnp.array([0.0, 1.0/sqrt_gll, 0.0, 0.0])
    eth=jnp.array([0.0, 0.0, 1.0/(A*Rgeom), 0.0])
    kp=n+el; km=n-el
    tidal_r=jnp.einsum('abcd,a,b,c,d->',Rdown,n,el,n,el)
    tidal_a=jnp.einsum('abcd,a,b,c,d->',Rdown,n,eth,n,eth)
    Gkp=jnp.einsum('a,b,ab->',kp,kp,G)
    Gkm=jnp.einsum('a,b,ab->',km,km,G)
    dRe=jax.grad(R_eff,argnums=0)(x,p)
    Re=R_eff(x,p)
    theta_p=2.0/Re*jnp.dot(kp,dRe)
    theta_m=2.0/Re*jnp.dot(km,dRe)
    theta_prod=theta_p*theta_m
    return jnp.array([Rsc,Kretsch,tidal_r,tidal_a,Gkp,Gkm,g[0,0],U,E,q,qR,W,S,A,T,B,N,Rgeom,beta,alpha,theta_p,theta_m,theta_prod,Re], dtype=jnp.float64)

raw_grid=jax.jit(jax.vmap(raw_diagnostics,in_axes=(0,None)))
raw_one=jax.jit(raw_diagnostics)

def np_scalars(Sgrid,Lgrid,p_np):
    V,v_exit,C0,lam,B0,eta_B,eta_N,hold_scale,p_beta,x_catch,x_beta,x_q,x_R,w_catch,w_rel,w_R,R_amp,Rth,Rpass,r0,eps,R_mode=p_np
    fall=lambda z,w: 0.5*(1-np.tanh(z/w))
    bump=lambda x2,R,w: 0.5*(1-np.tanh((x2-R*R)/(2*R*w)))
    C=fall(Sgrid-x_catch,w_catch); U=v_exit+(V-v_exit)*C
    E=fall(Sgrid-x_beta,w_rel); q=fall(Sgrid-x_q,w_rel)
    qR_sched=fall(Sgrid-x_R,w_R)
    if R_mode < 0.5: qR=qR_sched
    elif R_mode < 1.5: qR=np.ones_like(Sgrid)
    else: qR=np.zeros_like(Sgrid)
    W=bump(Lgrid*Lgrid,Rth,0.12); Sp=bump((Lgrid-Sgrid)*(Lgrid-Sgrid)+eps*eps,Rpass,0.06)
    A=np.exp(q*W*np.log(C0)); T=np.exp(q*W*np.log(lam*C0))
    B=1+eta_B*(B0-1)*W*q
    shoulder=np.exp(-((np.abs(Lgrid)-1.05)/0.35)**2)
    N=np.exp(eta_N*0.18*q*shoulder)
    r_open=np.sqrt(r0*r0+Lgrid*Lgrid); r_flat=r0+0.055*Lgrid*Lgrid
    Rgeom=r_flat+R_amp*qR*(r_open-r_flat)
    beta=-U*E*(W**p_beta)*Sp/B
    alpha=N*T
    gll=(B*A)**2; gtt=-alpha**2+gll*beta**2; gtl=gll*beta
    vcoord=U/B
    norm=gtt+2*gtl*vcoord+gll*vcoord*vcoord
    Reff=A*Rgeom
    return dict(U=U,E=E,q=q,qR=qR,W=W,S_pass=Sp,A=A,T=T,B=B,N=N,Rgeom=Rgeom,beta=beta,alpha=alpha,gll=gll,gtt=gtt,gtl=gtl,norm=norm,Reff=Reff)

def area_min_stats(p_np):
    ss=np.linspace(-0.25,1.55,73)
    ls=np.linspace(-1.4,1.4,401)
    out=[]
    for s in ss:
        S=np.full_like(ls,s)
        sc=np_scalars(S,ls,p_np)
        Re2=sc['Reff']**2
        j=int(np.argmin(Re2))
        dl=ls[1]-ls[0]
        d2=np.nan
        if 0<j<len(ls)-1:
            d2=(Re2[j+1]-2*Re2[j]+Re2[j-1])/(dl*dl)
        out.append((s,ls[j],math.sqrt(Re2[j]),d2,sc['qR'][j]))
    arr=np.array(out)
    return {
        'throat_min_l_maxabs':float(np.max(np.abs(arr[:,1]))),
        'throat_min_Reff_min':float(np.min(arr[:,2])),
        'throat_min_Reff_max':float(np.max(arr[:,2])),
        'throat_min_d2_Reff2_min':float(np.nanmin(arr[:,3])),
        'throat_min_d2_Reff2_median':float(np.nanmedian(arr[:,3])),
        'qR_at_min_min':float(np.min(arr[:,4])),
        'qR_at_min_median':float(np.median(arr[:,4])),
    }

def scan_variant(label,p,baseline_metrics=None):
    p_np=np.array(p)
    # Dense causal/passenger scan
    ss=np.linspace(-0.35,1.65,161)
    ls=np.linspace(-1.6,1.9,261)
    Sg,Lg=np.meshgrid(ss,ls,indexing='ij')
    sc=np_scalars(Sg,Lg,p_np)
    packet=np.abs(Lg-Sg)<=0.35
    center=np.abs(Lg-Sg)<=0.04
    support_edge=(sc['S_pass']>0.08)&(sc['W']>0.05)&(sc['W']<0.85)
    release=(Sg>p_np[9]-0.25)&(Sg<p_np[12]+0.35)
    rregion=np.abs(Lg)<=1.15
    def smax(a,m): return float(np.nanmax(np.where(m,a,np.nan)))
    def smin(a,m): return float(np.nanmin(np.where(m,a,np.nan)))
    out={
        'label':label,
        **unpack(p),
        'packet_max_gtt':smax(sc['gtt'],packet),
        'edge_max_gtt':smax(sc['gtt'],support_edge),
        'release_edge_max_gtt':smax(sc['gtt'],support_edge&release),
        'packet_max_norm':smax(sc['norm'],packet),
        'center_max_norm':smax(sc['norm'],center),
        'packet_gtt_positive_points':int(np.sum((sc['gtt']>0)&packet)),
        'edge_gtt_positive_points':int(np.sum((sc['gtt']>0)&support_edge)),
        'packet_norm_positive_points':int(np.sum((sc['norm']>0)&packet)),
        'center_norm_positive_points':int(np.sum((sc['norm']>0)&center)),
        'min_packet_margin':smin(sc['alpha']-np.sqrt(sc['gll'])*np.abs(sc['beta']),packet),
        'min_edge_margin':smin(sc['alpha']-np.sqrt(sc['gll'])*np.abs(sc['beta']),support_edge),
        'max_Reff':smax(sc['Reff'],rregion),
        'min_Reff':smin(sc['Reff'],rregion),
    }
    out.update(area_min_stats(p_np))
    # Sparse curvature/expansion samples: center/boundary/support edge across release interval
    pts=[]; regs=[]
    for s in np.linspace(-0.1,1.45,38):
        for l,reg in [(s,'center'),(s-0.35,'packet_boundary'),(s+0.35,'packet_boundary'),(-1.0,'support_edge'),(1.0,'support_edge'),(0.0,'throat_center')]:
            if -1.6 <= l <= 1.9:
                pts.append([float(s),float(l),math.pi/2,0.0]); regs.append(reg)
    arr=np.array(raw_grid(jnp.array(pts,dtype=jnp.float64),p))
    regs=np.array(regs)
    # cols: Rsc,Kretsch,tidal_r,tidal_a,Gkp,Gkm,gtt,U,E,q,qR,W,S,A,T,B,N,Rgeom,beta,alpha,theta_p,theta_m,theta_prod,Re
    for reg in ['center','packet_boundary','support_edge','throat_center']:
        m=regs==reg
        out[f'{reg}_maxabs_R']=float(np.max(np.abs(arr[m,0])))
        out[f'{reg}_maxabs_Kretsch']=float(np.max(np.abs(arr[m,1])))
        out[f'{reg}_maxabs_tidal_radial']=float(np.max(np.abs(arr[m,2])))
        out[f'{reg}_maxabs_tidal_angular']=float(np.max(np.abs(arr[m,3])))
        out[f'{reg}_min_Gkk']=float(np.min(np.minimum(arr[m,4],arr[m,5])))
        out[f'{reg}_max_theta_prod']=float(np.max(arr[m,22]))
        out[f'{reg}_min_theta_prod']=float(np.min(arr[m,22]))
    out['hard_packet_fail']=bool(out['packet_norm_positive_points']>0 or out['center_norm_positive_points']>0)
    out['passive_gtt_fail']=bool(out['packet_gtt_positive_points']>0 or out['edge_gtt_positive_points']>0)
    out['flare_out_fail']=bool(out['throat_min_d2_Reff2_min'] <= 0.0)
    return out

def run():
    _=raw_one(jnp.array([0.0,0.0,math.pi/2,0.0],dtype=jnp.float64),make_p())
    scenarios=[]
    # nominal and stressed cases
    for V,lam in [(2.5,None),(5.0,None),(10.0,None),(5.0,3.0),(10.0,6.0)]:
        base=make_p(V=V,lam=lam)
        x=unpack(base)
        variants=[]
        variants.append(('baseline_R_fades_with_q', base))
        variants.append(('R_fades_at_shift_fade', make_p(V=V,lam=lam,x_R=x['x_beta'])))
        variants.append(('R_fades_at_catch', make_p(V=V,lam=lam,x_R=x['x_catch'])))
        variants.append(('R_delayed_after_throat_relax', make_p(V=V,lam=lam,x_R=x['x_q']+0.45)))
        variants.append(('R_always_open', make_p(V=V,lam=lam,R_mode=1)))
        variants.append(('R_always_flat', make_p(V=V,lam=lam,R_mode=2)))
        variants.append(('R_half_amplitude', make_p(V=V,lam=lam,R_amp=0.5)))
        variants.append(('R_sharp_release', make_p(V=V,lam=lam,w_R=0.07)))
        variants.append(('R_slow_release', make_p(V=V,lam=lam,w_R=0.35)))
        variants.append(('R_always_open_no_quiet_hold', make_p(V=V,lam=lam,R_mode=1,hold_scale=0.0)))
        variants.append(('R_flat_no_quiet_hold', make_p(V=V,lam=lam,R_mode=2,hold_scale=0.0)))
        variants.append(('R_fades_q_no_B_no_N', make_p(V=V,lam=lam,eta_B=0.0,eta_N=0.0)))
        for label,p in variants:
            print('scan', V, lam, label, flush=True)
            scenarios.append(scan_variant(label,p))
    # Add ratios to baseline per V-lam pair
    bykey={}
    for r in scenarios:
        key=(r['V'],r['lam'])
        bykey.setdefault(key,[]).append(r)
    for key,rows in bykey.items():
        base=next(r for r in rows if r['label']=='baseline_R_fades_with_q')
        for r in rows:
            for metric in [
                'packet_boundary_maxabs_tidal_angular','packet_boundary_maxabs_tidal_radial','packet_boundary_maxabs_Kretsch',
                'support_edge_maxabs_tidal_angular','support_edge_maxabs_tidal_radial','support_edge_maxabs_Kretsch',
                'throat_center_max_theta_prod','support_edge_max_theta_prod','packet_boundary_max_theta_prod',
                'throat_min_d2_Reff2_min'
            ]:
                denom=base.get(metric,0.0)
                r[metric+'_ratio_to_base']=float(r[metric]/denom) if abs(denom)>1e-300 else float('nan')
    out_json='/mnt/data/composite_r_flare_gate_tests.json'
    with open(out_json,'w') as f: json.dump(scenarios,f,indent=2)
    # Markdown summary
    out_md='/mnt/data/composite_r_flare_gate_tests.md'
    with open(out_md,'w') as f:
        f.write('# Composite R-flare gate diagnostic tests\n\n')
        f.write('Reduced comparative screen for R-flare gating in the composite v1 + catch-rematched throat-loaded system. This is not a source solve or full 3+1 initial-data calculation.\n\n')
        f.write('Hard packet failure means the passenger worldtube norm became non-timelike. Passive gtt failure means either packet-region or support-edge stationary-observer gtt became positive. Flare-out failure means the sampled areal-radius minimum lost positive second derivative in this reduced slice screen.\n\n')
        for key,rows in sorted(bykey.items()):
            V,lam=key
            f.write(f'## V={V:g}, lambda={lam:g}\n\n')
            f.write('| variant | packet fail | passive gtt fail | flare-out fail | packet max norm | edge max gtt | min flare d2 | packet angular tidal ×base | edge angular tidal ×base | edge theta-prod ×base |\n')
            f.write('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n')
            for r in rows:
                f.write(f"| {r['label']} | {int(r['hard_packet_fail'])} | {int(r['passive_gtt_fail'])} | {int(r['flare_out_fail'])} | {r['packet_max_norm']:.3g} | {r['edge_max_gtt']:.3g} | {r['throat_min_d2_Reff2_min']:.3g} | {r['packet_boundary_maxabs_tidal_angular_ratio_to_base']:.3g} | {r['support_edge_maxabs_tidal_angular_ratio_to_base']:.3g} | {r['support_edge_max_theta_prod_ratio_to_base']:.3g} |\n")
            f.write('\n')
        f.write('## Notes\n\n')
        f.write('- R-always-open is a test of demoting flare closure entirely.\n')
        f.write('- R-always-flat is a test of replacing an opened flare with a nearly cylindrical access state.\n')
        f.write('- R fades at catch/shift/q/delayed are ordering tests relative to catch, shift fade, and throat relax.\n')
        f.write('- Ratios are normalized to the baseline R-fades-with-q case at the same V and lambda.\n')
    # Compute concise conclusions JSON
    summary=[]
    for key,rows in sorted(bykey.items()):
        for r in rows:
            if r['label']=='baseline_R_fades_with_q': continue
            summary.append({
                'V':key[0], 'lambda':key[1], 'variant':r['label'],
                'hard_packet_fail':r['hard_packet_fail'],
                'passive_gtt_fail':r['passive_gtt_fail'],
                'flare_out_fail':r['flare_out_fail'],
                'packet_angular_tidal_ratio':r['packet_boundary_maxabs_tidal_angular_ratio_to_base'],
                'edge_angular_tidal_ratio':r['support_edge_maxabs_tidal_angular_ratio_to_base'],
                'edge_theta_product_ratio':r['support_edge_max_theta_prod_ratio_to_base'],
                'min_flare_d2':r['throat_min_d2_Reff2_min'],
            })
    out_summary='/mnt/data/composite_r_flare_gate_conclusions.json'
    with open(out_summary,'w') as f: json.dump(summary,f,indent=2)
    print(out_md); print(out_json); print(out_summary)

if __name__=='__main__':
    run()
