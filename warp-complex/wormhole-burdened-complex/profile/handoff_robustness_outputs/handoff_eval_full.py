import math, json, os, time, zipfile
import numpy as np
import pandas as pd
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp

proj_names = [
    'R','Kretsch','Gnn','Gkp','Gkm','gtt','det','theta_p','theta_m',
    'tidal_radial','tidal_angular','S_pass','W','q','E','A','T','r','rho_pass','L',
    'rho_src','p_l','p_th','p_phi','j_l','trace_spatial','nec_min','nec_neg_sum'
]

def make_params(C0=100.0, Delta=0.3, Rth=0.75, Rpass=0.35, r0=1.0,
                V=0.9, lapse_lambda=1.05, L_beta=0.75, L_q=1.10,
                w_release=0.25, mode_id=1, eps=1e-5):
    return jnp.array([float(C0),float(Delta),float(Rth),float(Rpass),float(r0),float(V),float(lapse_lambda),float(L_beta),float(L_q),float(w_release),float(mode_id),float(eps),float(Delta/6.0),float(Delta/6.0)], dtype=jnp.float64)

def lambda_for_V(V): return max(1.05, 1.15*float(V))

def bump_j(x2,R,w):
    z=(x2-R*R)/(2.0*R*w)
    return 0.5*(1.0-jnp.tanh(z))
def falloff_j(z,w): return 0.5*(1.0-jnp.tanh(z/w))

def release_profiles(L,p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass=p
    w=jnp.where(mode_id>1.5,0.5*w_release,w_release)
    q_shift=falloff_j(L-L_beta,w)
    q_throat=falloff_j(L-L_q,w)
    sync=falloff_j(L-L_q,w)
    E=jnp.where(mode_id<0.5,sync,q_shift)
    q=jnp.where(mode_id<0.5,sync,q_throat)
    return q,E

def scalars_j(x,p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass=p
    t,l,th,ph=x; L=V*t
    q,E=release_profiles(L,p)
    W=bump_j(l*l,Rth,wth)
    rho2=(l-L)*(l-L)+eps*eps
    S=bump_j(rho2,Rpass,wpass)
    A=jnp.exp(q*W*jnp.log(C0))
    T=jnp.exp(q*W*jnp.log(lapse_lambda*C0))
    r=jnp.sqrt(r0*r0+l*l)
    rho=jnp.sqrt(rho2)
    return S,W,q,E,A,T,r,rho,L

def metric(x,p):
    S,W,q,E,A,T,r,rho,L=scalars_j(x,p)
    V=p[5]; th=x[2]
    beta=-V*E*S*W
    return jnp.array([[-T*T+A*A*beta*beta, A*A*beta, 0.0,0.0],
                      [ A*A*beta, A*A, 0.0,0.0],
                      [0.0,0.0,A*A*r*r,0.0],
                      [0.0,0.0,0.0,A*A*r*r*jnp.sin(th)**2]], dtype=jnp.float64)

def gamma_conn(x,p):
    g=metric(x,p); dg=jax.jacfwd(metric,argnums=0)(x,p); ginv=jnp.linalg.inv(g)
    return 0.5*(jnp.einsum('ad,cdb->abc',ginv,dg)+jnp.einsum('ad,bdc->abc',ginv,dg)-jnp.einsum('ad,bcd->abc',ginv,dg))

def R_eff(x,p):
    S,W,q,E,A,T,r,rho,L=scalars_j(x,p); return A*r

def extended_raw(x,p):
    g=metric(x,p); ginv=jnp.linalg.inv(g)
    Gam=gamma_conn(x,p); dGam=jax.jacfwd(gamma_conn,argnums=0)(x,p)
    deriv=jnp.transpose(dGam,(0,2,3,1))-jnp.transpose(dGam,(0,2,1,3))
    prod1=jnp.einsum('ame,ens->asmn',Gam,Gam)
    prod2=jnp.einsum('ane,ems->asmn',Gam,Gam)
    Riem=deriv+prod1-prod2
    Ric=jnp.einsum('asan->sn',Riem)
    Rsc=jnp.einsum('ab,ab->',ginv,Ric)
    G=Ric-0.5*g*Rsc
    Rdown=jnp.einsum('pa,asmn->psmn',g,Riem)
    Kretsch=jnp.einsum('abcd,efgh,ae,bf,cg,dh->',Rdown,Rdown,ginv,ginv,ginv,ginv)
    S,W,q,E,A,T,r,rho,L=scalars_j(x,p); V=p[5]; beta=-V*E*S*W
    nvec=jnp.array([1.0/T,-beta/T,0.0,0.0])
    kp=jnp.array([1.0/T,-beta/T+1.0/A,0.0,0.0])
    km=jnp.array([1.0/T,-beta/T-1.0/A,0.0,0.0])
    e_l=jnp.array([0.0,1.0/A,0.0,0.0])
    e_th=jnp.array([0.0,0.0,1.0/(A*r),0.0])
    e_ph=jnp.array([0.0,0.0,0.0,1.0/(A*r*jnp.sin(x[2]))])
    Gnn=jnp.einsum('a,b,ab->',nvec,nvec,G)
    Gkp=jnp.einsum('a,b,ab->',kp,kp,G)
    Gkm=jnp.einsum('a,b,ab->',km,km,G)
    tidal_radial=jnp.einsum('abcd,a,b,c,d->',Rdown,nvec,e_l,nvec,e_l)
    tidal_angular=jnp.einsum('abcd,a,b,c,d->',Rdown,nvec,e_th,nvec,e_th)
    rho_src=Gnn
    p_l=jnp.einsum('a,b,ab->',e_l,e_l,G)
    p_th=jnp.einsum('a,b,ab->',e_th,e_th,G)
    p_phi=jnp.einsum('a,b,ab->',e_ph,e_ph,G)
    j_l=jnp.einsum('a,b,ab->',nvec,e_l,G)
    trace_spatial=p_l+p_th+p_phi
    dR=jax.grad(R_eff,argnums=0)(x,p)
    theta_p=2/(A*r)*(((dR[0]-beta*dR[1])/T)+(1/A)*dR[1])
    theta_m=2/(A*r)*(((dR[0]-beta*dR[1])/T)-(1/A)*dR[1])
    det=jnp.linalg.det(g); gtt=g[0,0]
    nec_min=jnp.minimum(Gkp,Gkm)
    nec_neg_sum=jnp.maximum(0.0,-Gkp)+jnp.maximum(0.0,-Gkm)
    return jnp.array([Rsc,Kretsch,Gnn,Gkp,Gkm,gtt,det,theta_p,theta_m,tidal_radial,tidal_angular,S,W,q,E,A,T,r,rho,L,rho_src,p_l,p_th,p_phi,j_l,trace_spatial,nec_min,nec_neg_sum], dtype=jnp.float64)

extended_grid=jax.jit(jax.vmap(extended_raw,in_axes=(0,None)))
extended_one=jax.jit(extended_raw)

# numpy scalar model for integration
def bump(x2,R,w):
    z=(x2-R*R)/(2.0*R*w)
    return 0.5*(1.0-np.tanh(z))
def falloff(z,w): return 0.5*(1.0-np.tanh(z/w))
def scalars_np(t,x,cfg):
    V=cfg['V']; L=V*t; Delta=cfg['Delta']; Rth=0.75; Rpass=0.35; eps=1e-5
    wth=Delta/6.0; wpass=Delta/6.0
    W=bump(x*x,Rth,wth); S=bump((x-L)*(x-L)+eps*eps,Rpass,wpass)
    E=falloff(L-cfg['L_beta'],cfg['w_release']); q=falloff(L-cfg['L_q'],cfg['w_release'])
    A=np.exp(q*W*np.log(cfg['C0'])); T=np.exp(q*W*np.log(cfg['lapse_lambda']*cfg['C0']))
    return S,W,E,q,A,T,L

def velocity_law(t,x,cfg,variant):
    V=cfg['V']; S,W,E,q,A,T,L=scalars_np(t,x,cfg)
    F={'EWS':E*W*S,'EW':E*W,'ES':E*S,'E':E}[variant.get('support','EWS')]
    typ=variant['type']
    if typ=='fixed': return V
    if typ=='blend':
        vout=variant.get('vout',0.0); return vout+(V-vout)*F
    if typ=='clip':
        eta=variant.get('eta',0.9); shift=V*E*W*S
        return min(V, shift+eta*T/A)
    raise ValueError(typ)

def integrate_path(cfg,variant,Nt=301,L_start=None,L_stop=None):
    V=cfg['V']
    if L_start is None: L_start=min(-0.5,cfg['L_beta']-3*cfg['w_release'])
    if L_stop is None: L_stop=max(cfg['L_q']+4*cfg['w_release'],1.4)
    ts=np.linspace(L_start/V,L_stop/V,Nt); xs=np.zeros(Nt); vs=np.zeros(Nt); norms=np.zeros(Nt); margins=np.zeros(Nt)
    xs[0]=L_start
    for i in range(Nt-1):
        t=ts[i]; x=xs[i]; dt=ts[i+1]-ts[i]
        k1=velocity_law(t,x,cfg,variant)
        k2=velocity_law(t+0.5*dt,x+0.5*dt*k1,cfg,variant)
        k3=velocity_law(t+0.5*dt,x+0.5*dt*k2,cfg,variant)
        k4=velocity_law(t+dt,x+dt*k3,cfg,variant)
        xs[i+1]=x+(dt/6.0)*(k1+2*k2+2*k3+k4); vs[i]=k1
    vs[-1]=velocity_law(ts[-1],xs[-1],cfg,variant)
    for i,(t,x,v) in enumerate(zip(ts,xs,vs)):
        S,W,E,q,A,T,L=scalars_np(t,x,cfg); shift=cfg['V']*E*W*S
        norms[i]=-T*T+A*A*(v-shift)**2
        margins[i]=T/A-abs(v-shift)
    return ts,xs,vs,norms,margins

def super_configs():
    rows=[]
    for V in [1.01,1.1,1.25,1.5,2.0]:
        lam=lambda_for_V(V)
        for C0 in [100.0,1e4]:
            for Delta in [0.3,0.1]:
                for w_release in [0.35,0.18]:
                    for gap in [0.35,0.70,1.00]:
                        rows.append(dict(V=V,lapse_lambda=lam,C0=C0,Delta=Delta,w_release=w_release,L_beta=1.10-gap,L_q=1.10,release_gap=gap,mode='shift_first'))
    return rows

VARIANTS=[
    dict(name='fixed_V_baseline', type='fixed', support='EWS', vout=np.nan),
    dict(name='blend_EWS_stop', type='blend', support='EWS', vout=0.0),
    dict(name='blend_EWS_v05', type='blend', support='EWS', vout=0.5),
    dict(name='blend_EWS_v09', type='blend', support='EWS', vout=0.9),
    dict(name='blend_EW_v05', type='blend', support='EW', vout=0.5),
    dict(name='clip_eta09', type='clip', support='EWS', eta=0.9, vout=np.nan),
]

def norm_scan(Nt=401):
    rows=[]
    for cfg in super_configs():
        for var in VARIANTS:
            ts,xs,vs,norms,margins=integrate_path(cfg,var,Nt=Nt)
            rows.append({**cfg,'variant':var['name'],'type':var['type'],'support':var.get('support'),'vout':var.get('vout'),'eta':var.get('eta',np.nan),'timelike':bool(np.all(norms<-1e-10)),'spacelike_points':int(np.sum(norms>=0)),'max_ds2_dt2':float(np.max(norms)),'min_ds2_dt2':float(np.min(norms)),'min_margin':float(np.min(margins)),'final_x':float(xs[-1]),'control_final_L':float(cfg['V']*ts[-1]),'lag_final':float(cfg['V']*ts[-1]-xs[-1]),'max_speed':float(np.max(vs)),'min_speed':float(np.min(vs)),'max_accel_coord':float(np.max(np.abs(np.gradient(vs,ts)))),'path_length_coord':float(np.trapz(np.abs(vs),ts))})
    df=pd.DataFrame(rows); df.to_csv('/mnt/data/handoff_norm_scan.csv',index=False)
    summary=df.groupby('variant').agg(cases=('variant','size'),timelike_cases=('timelike','sum'),spacelike_cases=('spacelike_points',lambda s:int((s>0).sum())),worst_margin=('min_margin','min'),worst_max_ds2=('max_ds2_dt2','max'),median_final_x=('final_x','median'),median_lag=('lag_final','median'),max_accel=('max_accel_coord','max')).reset_index()
    summary.to_csv('/mnt/data/handoff_norm_summary.csv',index=False)
    return df,summary

def source_sample_for_variant(variant_name,Nt=101):
    var=[v for v in VARIANTS if v['name']==variant_name][0]; rows=[]
    _=extended_one(jnp.array([0.0,0.0,math.pi/2,0.0], dtype=jnp.float64), make_params())
    t0=time.time()
    for idx,cfg in enumerate(super_configs(),1):
        ts,xs,vs,norms,margins=integrate_path(cfg,var,Nt=Nt)
        p=make_params(C0=cfg['C0'],Delta=cfg['Delta'],V=cfg['V'],lapse_lambda=cfg['lapse_lambda'],L_beta=cfg['L_beta'],L_q=cfg['L_q'],w_release=cfg['w_release'],mode_id=1)
        xarr=np.array([[float(t),float(x),math.pi/2,0.0] for t,x in zip(ts,xs)], dtype=np.float64)
        arr=np.array(extended_grid(jnp.array(xarr),p)); names=proj_names
        neg_nec=np.maximum(0,-arr[:,names.index('Gkp')])+np.maximum(0,-arr[:,names.index('Gkm')])
        neg_rho=np.maximum(0,-arr[:,names.index('rho_src')])
        rows.append({**cfg,'variant':variant_name,'timelike':bool(np.all(norms<-1e-10)),'spacelike_points':int(np.sum(norms>=0)),'max_ds2_dt2':float(np.max(norms)),'min_margin':float(np.min(margins)),'final_x':float(xs[-1]),'lag_final':float(cfg['V']*ts[-1]-xs[-1]),'maxabs_rho_src':float(np.max(np.abs(arr[:,names.index('rho_src')]))),'min_rho_src':float(np.min(arr[:,names.index('rho_src')])),'maxabs_j_l':float(np.max(np.abs(arr[:,names.index('j_l')]))),'min_nec':float(np.min(arr[:,names.index('nec_min')])),'max_neg_nec_sum':float(np.max(neg_nec)),'int_neg_nec_dt':float(np.trapz(neg_nec,ts)),'int_neg_rho_dt':float(np.trapz(neg_rho,ts)),'maxabs_tidal_radial':float(np.max(np.abs(arr[:,names.index('tidal_radial')]))),'maxabs_tidal_angular':float(np.max(np.abs(arr[:,names.index('tidal_angular')]))),'max_A':float(np.max(arr[:,names.index('A')])),'min_A':float(np.min(arr[:,names.index('A')])),'max_W':float(np.max(arr[:,names.index('W')])),'min_W':float(np.min(arr[:,names.index('W')])),'max_S':float(np.max(arr[:,names.index('S_pass')])),'min_S':float(np.min(arr[:,names.index('S_pass')])),'max_E':float(np.max(arr[:,names.index('E')])),'min_E':float(np.min(arr[:,names.index('E')])),'max_q':float(np.max(arr[:,names.index('q')])),'min_q':float(np.min(arr[:,names.index('q')]))})
        if idx%24==0: print(variant_name,'done',idx,'/',len(super_configs()),'elapsed',round(time.time()-t0,1),flush=True)
    df=pd.DataFrame(rows); df.to_csv(f'/mnt/data/handoff_source_{variant_name}.csv',index=False); return df

def summarize_source():
    files=[f'/mnt/data/handoff_source_{v}.csv' for v in ['fixed_V_baseline','blend_EWS_stop','blend_EWS_v05','blend_EWS_v09','blend_EW_v05','clip_eta09'] if os.path.exists(f'/mnt/data/handoff_source_{v}.csv')]
    df=pd.concat([pd.read_csv(f) for f in files],ignore_index=True); df.to_csv('/mnt/data/handoff_source_all_sampled.csv',index=False)
    summ=df.groupby('variant').agg(cases=('variant','size'),timelike_cases=('timelike','sum'),spacelike_cases=('spacelike_points',lambda s:int((s>0).sum())),worst_margin=('min_margin','min'),worst_max_ds2=('max_ds2_dt2','max'),worst_rho=('min_rho_src','min'),max_abs_rho=('maxabs_rho_src','max'),worst_nec=('min_nec','min'),max_neg_nec=('max_neg_nec_sum','max'),max_tidal_r=('maxabs_tidal_radial','max'),max_tidal_a=('maxabs_tidal_angular','max'),med_int_neg_nec=('int_neg_nec_dt','median'),max_int_neg_nec=('int_neg_nec_dt','max'),median_final_x=('final_x','median'),median_lag=('lag_final','median')).reset_index()
    summ.to_csv('/mnt/data/handoff_source_summary.csv',index=False); return df,summ

if __name__=='__main__':
    mode=os.environ.get('HANDOFF_MODE','norm')
    if mode=='norm':
        df,s=norm_scan(); print(s.to_string(index=False))
    elif mode.startswith('source:'):
        variant=mode.split(':',1)[1]; df=source_sample_for_variant(variant); print(df.head().to_string())
    elif mode=='summarize':
        df,s=summarize_source(); print(s.to_string(index=False))
