import math, json, itertools, time
import numpy as np
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp

# Composite reduced screen:
# v1-like B,R,N throat infrastructure + catch-rematched throat-loaded packet.
# Coordinates x=(s,l,theta,phi), where s is a reduced transit progress/time parameter.
# This is a screening harness, not a constraint-quality source solve.

# parameter indices
# V, v_exit, C0, lam, B0, eta_B, eta_R, eta_N, hold_scale, p_beta, x_catch, x_beta, x_q, w_catch, w_rel, Rth, Rpass, r0, eps

def make_p(V=2.5, v_exit=0.5, C0=100.0, lam=None, B0=8.0,
           eta_B=1.0, eta_R=1.0, eta_N=1.0, hold_scale=1.0, p_beta=1.0):
    if lam is None:
        lam=max(1.05,1.15*V)
    # Baseline ordering: catch -> beta fade -> throat relax.
    # hold_scale shortens the separation between catch, shift release, and throat relaxation.
    x_catch=0.15
    x_beta=x_catch + 0.55*hold_scale
    x_q=x_beta + 0.55*hold_scale
    # avoid exact coincidence for zero hold but make it tight
    if hold_scale <= 0.0:
        x_beta=x_catch+0.04
        x_q=x_beta+0.04
    return jnp.array([V,v_exit,C0,lam,B0,eta_B,eta_R,eta_N,hold_scale,p_beta,
                      x_catch,x_beta,x_q,0.16,0.18,1.0,0.35,1.0,1e-5], dtype=jnp.float64)

def bump_sq(x2,R,w):
    z=(x2-R*R)/(2.0*R*w)
    return 0.5*(1.0-jnp.tanh(z))

def falloff(z,w):
    return 0.5*(1.0-jnp.tanh(z/w))

def scalars(x,p):
    s,l,th,ph=x
    V,v_exit,C0,lam,B0,eta_B,eta_R,eta_N,hold_scale,p_beta,x_catch,x_beta,x_q,w_catch,w_rel,Rth,Rpass,r0,eps=p
    C=falloff(s-x_catch,w_catch)
    U=v_exit+(V-v_exit)*C
    E=falloff(s-x_beta,w_rel)
    q=falloff(s-x_q,w_rel)
    W=bump_sq(l*l,Rth,0.12)
    S=bump_sq((l-s)*(l-s)+eps*eps,Rpass,0.06)
    A=jnp.exp(q*W*jnp.log(C0))
    T=jnp.exp(q*W*jnp.log(lam*C0))
    B=1.0 + eta_B*(B0-1.0)*W*q
    shoulder_center=1.05
    shoulder=jnp.exp(-((jnp.abs(l)-shoulder_center)/0.35)**2)
    # Edge lapse shaping, modeled as a positive support-edge lapse margin.
    N=jnp.exp(eta_N*0.18*q*shoulder)
    r_open=jnp.sqrt(r0*r0+l*l)
    r_flat=r0+0.055*l*l
    Rgeom=r_flat + eta_R*q*(r_open-r_flat)
    beta=-U*E*(W**p_beta)*S/B
    alpha=N*T
    return U,E,q,W,S,A,T,B,N,Rgeom,beta,alpha

def metric(x,p):
    U,E,q,W,S,A,T,B,N,Rgeom,beta,alpha=scalars(x,p)
    th=x[2]
    gll=(B*A)**2
    goo=(A*Rgeom)**2
    return jnp.array([
        [-alpha*alpha + gll*beta*beta, gll*beta, 0.0, 0.0],
        [ gll*beta,                  gll,       0.0, 0.0],
        [0.0,                        0.0,       goo, 0.0],
        [0.0,                        0.0,       0.0, goo*jnp.sin(th)**2],
    ], dtype=jnp.float64)

def gamma_conn(x,p):
    g=metric(x,p)
    dg=jax.jacfwd(metric,argnums=0)(x,p)
    ginv=jnp.linalg.inv(g)
    return 0.5*(jnp.einsum('ad,cdb->abc',ginv,dg)+jnp.einsum('ad,bdc->abc',ginv,dg)-jnp.einsum('ad,bcd->abc',ginv,dg))

def curvature_raw(x,p):
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
    U,E,q,W,S,A,T,B,N,Rgeom,beta,alpha=scalars(x,p)
    nvec=jnp.array([1.0/alpha, -beta/alpha, 0.0, 0.0])
    e_l=jnp.array([0.0, 1.0/(B*A), 0.0, 0.0])
    e_th=jnp.array([0.0,0.0,1.0/(A*Rgeom),0.0])
    tidal_radial=jnp.einsum('abcd,a,b,c,d->',Rdown,nvec,e_l,nvec,e_l)
    tidal_angular=jnp.einsum('abcd,a,b,c,d->',Rdown,nvec,e_th,nvec,e_th)
    kp=jnp.array([1.0/alpha, -beta/alpha + 1.0/(B*A), 0.0, 0.0])
    km=jnp.array([1.0/alpha, -beta/alpha - 1.0/(B*A), 0.0, 0.0])
    Gkp=jnp.einsum('a,b,ab->',kp,kp,G)
    Gkm=jnp.einsum('a,b,ab->',km,km,G)
    return jnp.array([Rsc,Kretsch,tidal_radial,tidal_angular,Gkp,Gkm,g[0,0],U,E,q,W,S,A,T,B,N,Rgeom,beta,alpha], dtype=jnp.float64)

curv_grid=jax.jit(jax.vmap(curvature_raw,in_axes=(0,None)))
curv_one=jax.jit(curvature_raw)

def numpy_scalars(S,L,p_np):
    # vectorized numpy version for dense causal scans, S and L mesh arrays.
    V,v_exit,C0,lam,B0,eta_B,eta_R,eta_N,hold_scale,p_beta,x_catch,x_beta,x_q,w_catch,w_rel,Rth,Rpass,r0,eps=p_np
    fall=lambda z,w: 0.5*(1-np.tanh(z/w))
    bump=lambda x2,R,w: 0.5*(1-np.tanh((x2-R*R)/(2*R*w)))
    C=fall(S-x_catch,w_catch); U=v_exit+(V-v_exit)*C
    E=fall(S-x_beta,w_rel); q=fall(S-x_q,w_rel)
    W=bump(L*L,Rth,0.12); S_pass=bump((L-S)*(L-S)+eps*eps,Rpass,0.06)
    A=np.exp(q*W*np.log(C0)); T=np.exp(q*W*np.log(lam*C0))
    B=1+eta_B*(B0-1)*W*q
    shoulder=np.exp(-((np.abs(L)-1.05)/0.35)**2)
    N=np.exp(eta_N*0.18*q*shoulder)
    beta=-U*E*(W**p_beta)*S_pass/B
    alpha=N*T
    gll=(B*A)**2
    gtt=-alpha**2+gll*beta**2
    gtl=gll*beta
    vcoord=U/B
    norm=gtt+2*gtl*vcoord+gll*vcoord*vcoord
    return dict(U=U,E=E,q=q,W=W,S_pass=S_pass,A=A,T=T,B=B,N=N,beta=beta,alpha=alpha,gll=gll,gtt=gtt,gtl=gtl,norm=norm)

def scan_case(name,p,do_curv=True):
    p_np=np.array(p)
    ss=np.linspace(-0.4,1.65,151)
    ls=np.linspace(-1.6,1.9,241)
    Smesh,Lmesh=np.meshgrid(ss,ls,indexing='ij')
    sc=numpy_scalars(Smesh,Lmesh,p_np)
    packet=np.abs(Lmesh-Smesh)<=0.35
    center=np.abs(Lmesh-Smesh)<=0.04
    edge=(sc['S_pass']>0.08)&(sc['W']>0.05)&(sc['W']<0.85)
    release=(Smesh>p_np[10]-0.25)&(Smesh<p_np[12]+0.35)
    def safe_max(a,mask): return float(np.nanmax(np.where(mask,a,np.nan)))
    def safe_min(a,mask): return float(np.nanmin(np.where(mask,a,np.nan)))
    out=dict(name=name,V=float(p_np[0]),eta_B=float(p_np[5]),eta_R=float(p_np[6]),eta_N=float(p_np[7]),hold_scale=float(p_np[8]),p_beta=float(p_np[9]))
    out.update({
        'packet_max_gtt':safe_max(sc['gtt'],packet),
        'edge_max_gtt':safe_max(sc['gtt'],edge),
        'release_edge_max_gtt':safe_max(sc['gtt'],edge&release),
        'packet_max_norm':safe_max(sc['norm'],packet),
        'center_max_norm':safe_max(sc['norm'],center),
        'packet_gtt_positive_points':int(np.sum((sc['gtt']>0)&packet)),
        'edge_gtt_positive_points':int(np.sum((sc['gtt']>0)&edge)),
        'packet_norm_positive_points':int(np.sum((sc['norm']>0)&packet)),
        'center_norm_positive_points':int(np.sum((sc['norm']>0)&center)),
        'min_packet_lapse_shift_margin':safe_min(sc['alpha'] - np.sqrt(sc['gll'])*np.abs(sc['beta']),packet),
        'min_edge_lapse_shift_margin':safe_min(sc['alpha'] - np.sqrt(sc['gll'])*np.abs(sc['beta']),edge),
        'max_post_A_departure':safe_max(np.abs(sc['A']-1),(Smesh>p_np[12]+0.35)),
        'max_post_T_departure':safe_max(np.abs(sc['T']-1),(Smesh>p_np[12]+0.35)),
    })
    # Curvature/tidal subset: sample packet boundary and support edge around release.
    if do_curv:
        pts=[]; labels=[]
        s_sub=np.linspace(-0.1,1.45,32)
        for s in s_sub:
            for off,label in [(0.0,'center'),(-0.35,'packet_boundary'),(0.35,'packet_boundary'),(-1.0,'support_edge'),(1.0,'support_edge')]:
                l=s+off if 'packet' in label or label=='center' else off
                if -1.6 <= l <= 1.9:
                    pts.append([s,l,math.pi/2,0.0]); labels.append(label)
        arr=np.array(curv_grid(jnp.array(pts,dtype=jnp.float64),p))
        labels=np.array(labels)
        for region in ['center','packet_boundary','support_edge']:
            m=labels==region
            out[f'{region}_maxabs_R']=float(np.nanmax(np.abs(arr[m,0])))
            out[f'{region}_maxabs_Kretsch']=float(np.nanmax(np.abs(arr[m,1])))
            out[f'{region}_maxabs_tidal_radial']=float(np.nanmax(np.abs(arr[m,2])))
            out[f'{region}_maxabs_tidal_angular']=float(np.nanmax(np.abs(arr[m,3])))
            out[f'{region}_min_Gkk']=float(np.nanmin(np.minimum(arr[m,4],arr[m,5])))
    # Classification
    hard_fail = (out['packet_gtt_positive_points']>0 or out['edge_gtt_positive_points']>0 or
                 out['packet_norm_positive_points']>0 or out['center_norm_positive_points']>0)
    out['hard_causal_fail']=bool(hard_fail)
    return out

def main():
    _=curv_one(jnp.array([0.0,0.0,math.pi/2,0.0],dtype=jnp.float64), make_p())
    cases=[]
    for V in [2.5,5.0,10.0]:
        base=make_p(V=V)
        configs=[
            ('baseline_full_v1_like', base),
            ('no_B_prestretch', make_p(V=V,eta_B=0.0)),
            ('half_B_prestretch', make_p(V=V,eta_B=0.5)),
            ('no_R_flare_gate', make_p(V=V,eta_R=0.0)),
            ('half_R_flare_gate', make_p(V=V,eta_R=0.5)),
            ('no_N_edge_lapse_shape', make_p(V=V,eta_N=0.0)),
            ('half_N_edge_lapse_shape', make_p(V=V,eta_N=0.5)),
            ('short_quiet_hold', make_p(V=V,hold_scale=0.35)),
            ('no_quiet_hold', make_p(V=V,hold_scale=0.0)),
            ('stronger_edge_shift_gating_p2', make_p(V=V,p_beta=2.0)),
            ('relaxed_B_R_no_hold', make_p(V=V,eta_B=0.0,eta_R=0.0,hold_scale=0.0)),
            ('no_N_no_hold', make_p(V=V,eta_N=0.0,hold_scale=0.0)),
        ]
        for name,p in configs:
            print('scan',V,name, flush=True)
            cases.append(scan_case(name,p,do_curv=True))
    # Compute ratios to baseline for each V
    byV={}
    for c in cases: byV.setdefault(c['V'],[]).append(c)
    for V,rows in byV.items():
        base=next(r for r in rows if r['name']=='baseline_full_v1_like')
        for r in rows:
            for k in ['center_maxabs_tidal_radial','packet_boundary_maxabs_tidal_radial','support_edge_maxabs_tidal_radial','center_maxabs_Kretsch','packet_boundary_maxabs_Kretsch','support_edge_maxabs_Kretsch']:
                r[k+'_ratio_to_base']=r[k]/base[k] if base[k] != 0 else float('nan')
    with open('/mnt/data/composite_gate_ablation_results.json','w') as f:
        json.dump(cases,f,indent=2)
    # compact markdown summary
    with open('/mnt/data/composite_gate_ablation_summary.md','w') as f:
        f.write('# Composite v1/catch-rematched gate ablation summary\n\n')
        f.write('Reduced screening harness: v1-like B/R/N throat infrastructure plus catch-rematched throat-gated packet. This is diagnostic, not a constraint-quality solve.\n\n')
        for V,rows in byV.items():
            f.write(f'## V={V}\n\n')
            f.write('| case | causal fail | packet max gtt | edge max gtt | packet max norm | edge margin | packet-boundary tidal ratio | support-edge tidal ratio |\n')
            f.write('|---|---:|---:|---:|---:|---:|---:|---:|\n')
            for r in rows:
                f.write(f"| {r['name']} | {int(r['hard_causal_fail'])} | {r['packet_max_gtt']:.3g} | {r['edge_max_gtt']:.3g} | {r['packet_max_norm']:.3g} | {r['min_edge_lapse_shift_margin']:.3g} | {r['packet_boundary_maxabs_tidal_radial_ratio_to_base']:.3g} | {r['support_edge_maxabs_tidal_radial_ratio_to_base']:.3g} |\n")
            f.write('\n')
    print('/mnt/data/composite_gate_ablation_results.json')
    print('/mnt/data/composite_gate_ablation_summary.md')

if __name__=='__main__':
    main()
