import math, time, json, os
import numpy as np
import pandas as pd
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp

# Baseline throat-gated shift evaluator, extended with source projections.
# p: C0, Delta, Rth, Rpass, r0, V, lambda, L_beta, L_q, w_release, mode_id, eps, wth, wpass

proj_names = [
    'R','Kretsch','Gnn','Gkp','Gkm','gtt','det','theta_p','theta_m',
    'tidal_radial','tidal_angular','S_pass','W','q','E','A','T','r','rho_pass','L',
    'rho_src','p_l','p_th','p_phi','j_l','trace_spatial','nec_min','nec_neg_sum'
]

def make_params(C0=100.0, Delta=0.3, Rth=0.75, Rpass=0.35, r0=1.0,
                V=0.9, lapse_lambda=1.05, L_beta=0.75, L_q=1.10,
                w_release=0.25, mode_id=1, eps=1e-5):
    return jnp.array([
        float(C0), float(Delta), float(Rth), float(Rpass), float(r0),
        float(V), float(lapse_lambda), float(L_beta), float(L_q),
        float(w_release), float(mode_id), float(eps), float(Delta/6.0), float(Delta/6.0)
    ], dtype=jnp.float64)

def bump_from_squared_radius(x2, R, w):
    z = (x2 - R*R)/(2.0*R*w)
    return 0.5*(1.0 - jnp.tanh(z))

def falloff(z, w):
    return 0.5*(1.0 - jnp.tanh(z/w))

def release_profiles(L, p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass = p
    w = jnp.where(mode_id > 1.5, 0.5*w_release, w_release)
    q_shift = falloff(L - L_beta, w)
    q_throat = falloff(L - L_q, w)
    sync = falloff(L - L_q, w)
    E = jnp.where(mode_id < 0.5, sync, q_shift)
    q = jnp.where(mode_id < 0.5, sync, q_throat)
    return q, E

def scalars(x, p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass = p
    t,l,th,ph = x
    L = V*t
    q, E = release_profiles(L, p)
    W = bump_from_squared_radius(l*l, Rth, wth)
    rho2 = (l-L)*(l-L) + eps*eps
    S_pass = bump_from_squared_radius(rho2, Rpass, wpass)
    A = jnp.exp(q*W*jnp.log(C0))
    T = jnp.exp(q*W*jnp.log(lapse_lambda*C0))
    r = jnp.sqrt(r0*r0 + l*l)
    rho = jnp.sqrt(rho2)
    return S_pass, W, q, E, A, T, r, rho, L

def metric(x, p):
    S,W,q,E,A,T,r,rho,L = scalars(x, p)
    V = p[5]; th = x[2]
    beta = -V*E*S*W
    return jnp.array([
        [-T*T + A*A*beta*beta, A*A*beta, 0.0, 0.0],
        [ A*A*beta,               A*A,       0.0, 0.0],
        [0.0,                     0.0,       A*A*r*r, 0.0],
        [0.0,                     0.0,       0.0, A*A*r*r*jnp.sin(th)**2],
    ], dtype=jnp.float64)

def gamma_conn(x, p):
    g = metric(x, p)
    dg = jax.jacfwd(metric, argnums=0)(x, p)
    ginv = jnp.linalg.inv(g)
    return 0.5*(
        jnp.einsum('ad,cdb->abc', ginv, dg) +
        jnp.einsum('ad,bdc->abc', ginv, dg) -
        jnp.einsum('ad,bcd->abc', ginv, dg)
    )

def R_eff(x, p):
    S,W,q,E,A,T,r,rho,L = scalars(x, p)
    return A*r

def extended_raw(x, p):
    g = metric(x, p); ginv = jnp.linalg.inv(g)
    Gam = gamma_conn(x, p)
    dGam = jax.jacfwd(gamma_conn, argnums=0)(x, p)
    deriv = jnp.transpose(dGam, (0,2,3,1)) - jnp.transpose(dGam, (0,2,1,3))
    prod1 = jnp.einsum('ame,ens->asmn', Gam, Gam)
    prod2 = jnp.einsum('ane,ems->asmn', Gam, Gam)
    Riem = deriv + prod1 - prod2
    Ric = jnp.einsum('asan->sn', Riem)
    Rsc = jnp.einsum('ab,ab->', ginv, Ric)
    G = Ric - 0.5*g*Rsc
    Rdown = jnp.einsum('pa,asmn->psmn', g, Riem)
    Kretsch = jnp.einsum('abcd,efgh,ae,bf,cg,dh->', Rdown, Rdown, ginv, ginv, ginv, ginv)

    S,W,q,E,A,T,r,rho,L = scalars(x, p)
    V = p[5]
    beta = -V*E*S*W
    nvec = jnp.array([1.0/T, -beta/T, 0.0, 0.0])
    kp = jnp.array([1.0/T, -beta/T + 1.0/A, 0.0, 0.0])
    km = jnp.array([1.0/T, -beta/T - 1.0/A, 0.0, 0.0])
    Gnn = jnp.einsum('a,b,ab->', nvec, nvec, G)
    Gkp = jnp.einsum('a,b,ab->', kp, kp, G)
    Gkm = jnp.einsum('a,b,ab->', km, km, G)

    e_l = jnp.array([0.0, 1.0/A, 0.0, 0.0])
    e_th = jnp.array([0.0, 0.0, 1.0/(A*r), 0.0])
    e_ph = jnp.array([0.0, 0.0, 0.0, 1.0/(A*r*jnp.sin(x[2]))])
    tidal_radial = jnp.einsum('abcd,a,b,c,d->', Rdown, nvec, e_l, nvec, e_l)
    tidal_angular = jnp.einsum('abcd,a,b,c,d->', Rdown, nvec, e_th, nvec, e_th)
    # Source projections in geometrized units WITHOUT 1/(8*pi). Divide later if desired.
    rho_src = Gnn
    p_l = jnp.einsum('a,b,ab->', e_l, e_l, G)
    p_th = jnp.einsum('a,b,ab->', e_th, e_th, G)
    p_phi = jnp.einsum('a,b,ab->', e_ph, e_ph, G)
    j_l = jnp.einsum('a,b,ab->', nvec, e_l, G)
    trace_spatial = p_l + p_th + p_phi

    dR = jax.grad(R_eff, argnums=0)(x, p)
    theta_p = 2/(A*r)*(((dR[0]-beta*dR[1])/T)+(1/A)*dR[1])
    theta_m = 2/(A*r)*(((dR[0]-beta*dR[1])/T)-(1/A)*dR[1])
    det = jnp.linalg.det(g); gtt = g[0,0]
    nec_min = jnp.minimum(Gkp, Gkm)
    nec_neg_sum = jnp.maximum(0.0, -Gkp) + jnp.maximum(0.0, -Gkm)
    return jnp.array([
        Rsc, Kretsch, Gnn, Gkp, Gkm, gtt, det, theta_p, theta_m,
        tidal_radial, tidal_angular, S, W, q, E, A, T, r, rho, L,
        rho_src, p_l, p_th, p_phi, j_l, trace_spatial, nec_min, nec_neg_sum
    ], dtype=jnp.float64)

extended_grid = jax.jit(jax.vmap(extended_raw, in_axes=(0, None)))
extended_one = jax.jit(extended_raw)

def lambda_for_V(V):
    return max(1.05, 1.15*float(V))

def l_grid_for_phase(phase, Nl=61):
    if phase == 'traverse': return np.linspace(-1.4, 1.4, Nl)
    if phase == 'post': return np.linspace(-1.4, 2.4, Nl)
    return np.linspace(-1.4, 2.4, Nl)

def t_grid_for_phase(p, phase, Nt=9):
    V = float(p[5]); L_beta=float(p[7]); L_q=float(p[8]); w=float(p[9]); mode=float(p[10])
    if phase == 'traverse': Ls = np.linspace(-0.5, 0.5, Nt)
    elif phase == 'post':
        w_eff = 0.5*w if mode > 1.5 else w
        Ls = np.linspace(L_q + 4*w_eff, L_q + 7*w_eff, Nt)
    else:
        w_eff = 0.5*w if mode > 1.5 else w
        start = min(L_beta, L_q) - 3*w_eff
        stop = max(L_beta, L_q) + 3*w_eff
        Ls = np.linspace(start, stop, Nt)
    return Ls/max(V,1e-9)

def summarize_phase(p, phase='exit', Nt=9, Nl=61):
    ts = t_grid_for_phase(p, phase, Nt=Nt)
    ls = l_grid_for_phase(phase, Nl=Nl)
    xs = np.array([[float(t), float(l), math.pi/2, 0.0] for t in ts for l in ls], dtype=np.float64)
    arr = np.array(extended_grid(jnp.array(xs), p))
    nT, nL = len(ts), len(ls)
    arr3 = arr.reshape((nT,nL,arr.shape[1]))
    dL = (ls[-1]-ls[0])/(len(ls)-1)
    V=float(p[5]); Rth=float(p[2]); Rpass=float(p[3]); Delta=float(p[1])
    res = dict(phase=phase, Nt=nT, Nl=nL)
    # global source extrema
    for name in ['rho_src','p_l','p_th','p_phi','j_l','trace_spatial','nec_min','nec_neg_sum','tidal_radial','tidal_angular','gtt','Gkp','Gkm','Kretsch']:
        i = proj_names.index(name)
        vals = arr[:,i]
        res[f'min_{name}'] = float(np.nanmin(vals))
        res[f'max_{name}'] = float(np.nanmax(vals))
        res[f'maxabs_{name}'] = float(np.nanmax(np.abs(vals)))
    res['gtt_positive_points'] = int(np.sum(arr[:,proj_names.index('gtt')] > 1e-9))
    res['neg_rho_points'] = int(np.sum(arr[:,proj_names.index('rho_src')] < -1e-9))
    res['nec_violation_points'] = int(np.sum(arr[:,proj_names.index('nec_min')] < -1e-9))
    # shares / integrals
    neg_rho_total=[]; neg_nec_total=[]; throat_neg_rho=[]; throat_nec=[]; passenger_nec=[]; passenger_neg_rho=[]
    for ti,t in enumerate(ts):
        L = V*t
        vals = arr3[ti,:,:]
        neg_rho = np.maximum(0, -vals[:,proj_names.index('rho_src')])
        neg_nec = vals[:,proj_names.index('nec_neg_sum')]
        throat_mask = np.abs(ls) <= (Rth+Delta)
        pass_mask = np.abs(ls-L) <= (Rpass+Delta)
        neg_rho_total.append(float(np.sum(neg_rho)*dL))
        neg_nec_total.append(float(np.sum(neg_nec)*dL))
        throat_neg_rho.append(float(np.sum(neg_rho[throat_mask])*dL))
        throat_nec.append(float(np.sum(neg_nec[throat_mask])*dL))
        passenger_neg_rho.append(float(np.sum(neg_rho[pass_mask])*dL))
        passenger_nec.append(float(np.sum(neg_nec[pass_mask])*dL))
    def share(a,b):
        a=np.array(a); b=np.array(b)
        return float(np.nanmean(np.where(np.array(b)>0, np.array(a)/np.array(b), np.nan)))
    res['max_int_neg_rho'] = float(np.nanmax(neg_rho_total))
    res['max_int_neg_nec'] = float(np.nanmax(neg_nec_total))
    res['mean_throat_share_neg_rho'] = share(throat_neg_rho, neg_rho_total)
    res['mean_throat_share_neg_nec'] = share(throat_nec, neg_nec_total)
    res['max_passenger_share_neg_rho'] = float(np.nanmax(np.where(np.array(neg_rho_total)>0, np.array(passenger_neg_rho)/np.array(neg_rho_total), np.nan)))
    res['max_passenger_share_neg_nec'] = float(np.nanmax(np.where(np.array(neg_nec_total)>0, np.array(passenger_nec)/np.array(neg_nec_total), np.nan)))
    # source dominance proxies
    rho_abs = np.abs(arr[:,proj_names.index('rho_src')])
    denom = np.maximum(rho_abs, 1e-12)
    pressure_abs_max = np.maximum.reduce([np.abs(arr[:,proj_names.index('p_l')]), np.abs(arr[:,proj_names.index('p_th')]), np.abs(arr[:,proj_names.index('p_phi')])])
    res['max_pressure_over_absrho_pointwise'] = float(np.nanmax(pressure_abs_max/denom))
    res['p999_pressure_over_absrho_pointwise'] = float(np.nanpercentile(pressure_abs_max/denom,99.9))
    res['max_flux_over_absrho_pointwise'] = float(np.nanmax(np.abs(arr[:,proj_names.index('j_l')])/denom))
    res['p999_flux_over_absrho_pointwise'] = float(np.nanpercentile(np.abs(arr[:,proj_names.index('j_l')])/denom,99.9))
    return res

def summarize_worldline(p, phase='exit', Nt=101, offsets=(0.0,0.1,0.25,0.35)):
    ts = t_grid_for_phase(p, phase, Nt=Nt)
    V=float(p[5])
    rows=[]
    for off in offsets:
        for sign in ([1] if off==0 else [1,-1]):
            o=off*sign
            xs=[]
            for t in ts:
                L=V*t
                xs.append([float(t), float(L+o), math.pi/2, 0.0])
            arr = np.array(extended_grid(jnp.array(xs,dtype=np.float64), p))
            gtt_pos=int(np.sum(arr[:,proj_names.index('gtt')]>1e-9))
            neg_nec = np.maximum(0,-arr[:,proj_names.index('Gkp')]) + np.maximum(0,-arr[:,proj_names.index('Gkm')])
            neg_rho = np.maximum(0,-arr[:,proj_names.index('rho_src')])
            # crude coordinate-time integral; also report max only.
            rows.append({
                'offset':o,
                'gtt_positive_points':gtt_pos,
                'min_rho_src':float(np.min(arr[:,proj_names.index('rho_src')])),
                'maxabs_rho_src':float(np.max(np.abs(arr[:,proj_names.index('rho_src')]))),
                'min_nec':float(np.min(arr[:,proj_names.index('nec_min')])),
                'max_neg_nec_sum':float(np.max(neg_nec)),
                'int_neg_nec_dt':float(np.trapz(neg_nec, ts)),
                'int_neg_rho_dt':float(np.trapz(neg_rho, ts)),
                'maxabs_tidal_radial':float(np.max(np.abs(arr[:,proj_names.index('tidal_radial')]))),
                'maxabs_tidal_angular':float(np.max(np.abs(arr[:,proj_names.index('tidal_angular')]))),
                'max_A':float(np.max(arr[:,proj_names.index('A')])),
                'min_A':float(np.min(arr[:,proj_names.index('A')])),
                'max_W':float(np.max(arr[:,proj_names.index('W')])),
                'min_W':float(np.min(arr[:,proj_names.index('W')])),
                'max_S':float(np.max(arr[:,proj_names.index('S_pass')])),
                'min_S':float(np.min(arr[:,proj_names.index('S_pass')]))
            })
    return rows

def config_rows(vs=(0.9,1.01,1.1,1.25,1.5,2.0), C0s=(100.0,1e4), Deltas=(0.3,0.1), widths=(0.35,0.18), gaps=(0.35,0.70,1.00), mode_id=1):
    configs=[]
    for V in vs:
        lam=lambda_for_V(V)
        for C0 in C0s:
            for Delta in Deltas:
                for w_release in widths:
                    for gap in gaps:
                        L_beta=1.10-gap
                        configs.append(dict(V=V,lapse_lambda=lam,C0=C0,Delta=Delta,w_release=w_release,L_beta=L_beta,L_q=1.10,release_gap=gap,mode='shift_first'))
    return configs

def run_subset(outdir='/mnt/data', Nt=9, Nl=61):
    os.makedirs(outdir, exist_ok=True)
    _=extended_one(jnp.array([0.0,0.0,math.pi/2,0.0], dtype=jnp.float64), make_params())
    rows=[]
    t0=time.time()
    cfgs=config_rows()
    for idx,cfg in enumerate(cfgs,1):
        p=make_params(C0=cfg['C0'], Delta=cfg['Delta'], V=cfg['V'], lapse_lambda=cfg['lapse_lambda'], L_beta=cfg['L_beta'], L_q=cfg['L_q'], w_release=cfg['w_release'], mode_id=1)
        for phase in ['traverse','exit','post']:
            r=summarize_phase(p, phase=phase, Nt=Nt, Nl=Nl)
            r.update(cfg)
            rows.append(r)
        if idx%12==0:
            print('done',idx,'/',len(cfgs),'elapsed',round(time.time()-t0,1), flush=True)
    df=pd.DataFrame(rows)
    path=os.path.join(outdir,'source_anatomy_shift_first_phase_summary.csv')
    df.to_csv(path,index=False)
    # Aggregate exit/traverse
    ex=df[df.phase=='exit']
    tr=df[df.phase=='traverse']
    agg={
        'configs':len(cfgs),
        'exit_gtt_positive_configs':int((ex.gtt_positive_points>0).sum()),
        'traverse_gtt_positive_configs':int((tr.gtt_positive_points>0).sum()),
        'exit_nec_violation_configs':int((ex.nec_violation_points>0).sum()),
        'exit_neg_rho_configs':int((ex.neg_rho_points>0).sum()),
        'worst_exit_min_rho_src':float(ex.min_rho_src.min()),
        'worst_exit_maxabs_rho_src':float(ex.maxabs_rho_src.max()),
        'worst_exit_maxabs_pressure':float(max(ex.maxabs_p_l.max(), ex.maxabs_p_th.max(), ex.maxabs_p_phi.max())),
        'worst_exit_maxabs_flux':float(ex.maxabs_j_l.max()),
        'worst_exit_min_nec':float(ex.min_nec_min.min()),
        'worst_exit_max_neg_nec_sum':float(ex.max_nec_neg_sum.max()),
        'median_exit_throat_share_neg_rho':float(ex.mean_throat_share_neg_rho.median()),
        'min_exit_throat_share_neg_rho':float(ex.mean_throat_share_neg_rho.min()),
        'median_exit_throat_share_neg_nec':float(ex.mean_throat_share_neg_nec.median()),
        'min_exit_throat_share_neg_nec':float(ex.mean_throat_share_neg_nec.min()),
        'max_exit_passenger_share_neg_rho':float(ex.max_passenger_share_neg_rho.max()),
        'max_exit_passenger_share_neg_nec':float(ex.max_passenger_share_neg_nec.max()),
        'worst_exit_pressure_over_absrho_p999':float(ex.p999_pressure_over_absrho_pointwise.max()),
        'worst_exit_flux_over_absrho_p999':float(ex.p999_flux_over_absrho_pointwise.max()),
    }
    with open(os.path.join(outdir,'source_anatomy_shift_first_aggregate.json'),'w') as f: json.dump(agg,f,indent=2)
    # Worst config worldline
    worst = ex.sort_values(['maxabs_tidal_radial','maxabs_rho_src'], ascending=False).iloc[0].to_dict()
    cfg={k:worst[k] for k in ['V','lapse_lambda','C0','Delta','w_release','L_beta','L_q','release_gap']}
    p=make_params(C0=cfg['C0'], Delta=cfg['Delta'], V=cfg['V'], lapse_lambda=cfg['lapse_lambda'], L_beta=cfg['L_beta'], L_q=cfg['L_q'], w_release=cfg['w_release'], mode_id=1)
    wl=pd.DataFrame(summarize_worldline(p, Nt=101))
    for k,v in cfg.items(): wl[k]=v
    wl.to_csv(os.path.join(outdir,'source_anatomy_worst_worldline_offsets.csv'),index=False)
    print(json.dumps(agg,indent=2), flush=True)
    return path

if __name__=='__main__':
    run_subset()
