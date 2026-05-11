import math, time, json, itertools, os
from dataclasses import dataclass
import numpy as np
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp

names = [
    'R','Ricci2','Kretsch','Gnn','Gkp','Gkm','gtt','det','theta_p','theta_m',
    'tidal_radial','tidal_angular','S_pass','W','q','E','A','T','r','rho_pass','L'
]

PROFILE_NAMES = {0:'tanh_r2',1:'smoothstep_compact',2:'cinf_compact',3:'supergaussian'}
RELEASE_NAMES = {0:'tanh',1:'smoothstep_compact',2:'cinf_compact',3:'logistic_soft'}
MODE_NAMES = {0:'synchronized',1:'shift_first',2:'rapid_shift_first'}

def smootherstep(t):
    t = jnp.clip(t, 0.0, 1.0)
    return t*t*t*(t*(t*6.0 - 15.0) + 10.0)

def cinf_step01(t):
    # Smooth monotone 0->1 on [0,1], flat outside. safe branch evaluation.
    tt = jnp.clip(t, 1e-12, 1.0-1e-12)
    a = jnp.exp(-1.0/tt)
    b = jnp.exp(-1.0/(1.0-tt))
    s = a/(a+b)
    return jnp.where(t <= 0.0, 0.0, jnp.where(t >= 1.0, 1.0, s))

def bump_from_squared_radius_profile(x2, R, w, pid):
    # pid 0: original tanh proxy; pid 1: compact C2 smoothstep shell; pid 2: C-infinity compact bump; pid 3: super-Gaussian tail.
    z = (x2 - R*R)/(2.0*R*w)
    tanh_b = 0.5*(1.0 - jnp.tanh(z))
    rho = jnp.sqrt(x2 + 1e-18)
    # smoothstep: flat core R-w, compact by R+w.
    t = (rho - jnp.maximum(R-w, 0.0))/(2.0*w + 1e-15)
    smooth_b = 1.0 - smootherstep(t)
    # C-infinity compact bump: support R+w, normalized to 1 at center.
    Re = R + w
    u = x2/(Re*Re + 1e-300)
    uc = jnp.minimum(u, 1.0-1e-12)
    cinf_inside = jnp.exp(-uc/(1.0-uc))
    cinf_b = jnp.where(u < 1.0, cinf_inside, 0.0)
    # supergaussian: matched so value is small but nonzero around R+w.
    sg_scale = R + 0.5*w
    super_b = jnp.exp(- (x2/(sg_scale*sg_scale + 1e-300))**2 )
    return jnp.where(pid < 0.5, tanh_b, jnp.where(pid < 1.5, smooth_b, jnp.where(pid < 2.5, cinf_b, super_b)))

def falloff_profile(z, w, pid):
    tanh_f = 0.5*(1.0 - jnp.tanh(z/w))
    t = (z + w)/(2.0*w + 1e-15)
    smooth_f = 1.0 - smootherstep(t)
    cinf_f = 1.0 - cinf_step01(t)
    # logistic softer than tanh at same width; clipped for stability
    logistic_f = 1.0/(1.0 + jnp.exp(jnp.clip(z/(0.65*w + 1e-15), -60, 60)))
    return jnp.where(pid < 0.5, tanh_f, jnp.where(pid < 1.5, smooth_f, jnp.where(pid < 2.5, cinf_f, logistic_f)))

def make_params(C0=100.0, Delta=0.3, Rth=0.75, Rpass=0.35, r0=1.0,
                V=0.9, lapse_lambda=1.05, L_beta=0.75, L_q=1.10,
                w_release=0.25, mode_id=1, eps=1e-5,
                W_profile=0, S_profile=0, E_profile=0, q_profile=0):
    return jnp.array([
        float(C0), float(Delta), float(Rth), float(Rpass), float(r0),
        float(V), float(lapse_lambda), float(L_beta), float(L_q),
        float(w_release), float(mode_id), float(eps), float(Delta/6.0), float(Delta/6.0),
        float(W_profile), float(S_profile), float(E_profile), float(q_profile)
    ], dtype=jnp.float64)

def release_profiles(L, p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass,Wpid,Spid,Epid,qpid = p
    w = jnp.where(mode_id > 1.5, 0.5*w_release, w_release)
    E_shift = falloff_profile(L - L_beta, w, Epid)
    q_throat = falloff_profile(L - L_q, w, qpid)
    sync_E = falloff_profile(L - L_q, w, Epid)
    sync_q = falloff_profile(L - L_q, w, qpid)
    E = jnp.where(mode_id < 0.5, sync_E, E_shift)
    q = jnp.where(mode_id < 0.5, sync_q, q_throat)
    return q, E

def scalars(x, p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass,Wpid,Spid,Epid,qpid = p
    t,l,th,ph = x
    L = V*t
    q, E = release_profiles(L, p)
    W = bump_from_squared_radius_profile(l*l, Rth, wth, Wpid)
    rho2 = (l-L)*(l-L) + eps*eps
    S_pass = bump_from_squared_radius_profile(rho2, Rpass, wpass, Spid)
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

def curvature_raw(x, p):
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
    Ricci2 = jnp.einsum('ab,cd,ac,bd->', Ric, Ric, ginv, ginv)
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
    tidal_radial = jnp.einsum('abcd,a,b,c,d->', Rdown, nvec, e_l, nvec, e_l)
    tidal_angular = jnp.einsum('abcd,a,b,c,d->', Rdown, nvec, e_th, nvec, e_th)

    dR = jax.grad(R_eff, argnums=0)(x, p)
    theta_p = 2/(A*r)*(((dR[0]-beta*dR[1])/T)+(1/A)*dR[1])
    theta_m = 2/(A*r)*(((dR[0]-beta*dR[1])/T)-(1/A)*dR[1])
    det = jnp.linalg.det(g); gtt = g[0,0]
    return jnp.array([
        Rsc, Ricci2, Kretsch, Gnn, Gkp, Gkm, gtt, det, theta_p, theta_m,
        tidal_radial, tidal_angular, S, W, q, E, A, T, r, rho, L
    ], dtype=jnp.float64)

curvature_grid = jax.jit(jax.vmap(curvature_raw, in_axes=(0, None)))
curvature_one = jax.jit(curvature_raw)

def l_grid_for_phase(phase, resolution='full'):
    if resolution == 'fast':
        if phase == 'traverse': return np.linspace(-1.4, 1.4, 41)
        if phase == 'post': return np.linspace(-1.4, 2.4, 41)
        return np.linspace(-1.4, 2.4, 51)
    if phase == 'traverse': return np.linspace(-1.4, 1.4, 81)
    if phase == 'post': return np.linspace(-1.4, 2.4, 81)
    return np.linspace(-1.4, 2.4, 91)

def t_grid_for_phase(p, phase, Nt=13):
    V = float(p[5]); L_beta=float(p[7]); L_q=float(p[8]); w=float(p[9]); mode=float(p[10])
    if phase == 'traverse':
        Ls = np.linspace(-0.5, 0.5, Nt)
    elif phase == 'post':
        w_eff = 0.5*w if mode > 1.5 else w
        Ls = np.linspace(L_q + 4*w_eff, L_q + 7*w_eff, Nt)
    else:
        w_eff = 0.5*w if mode > 1.5 else w
        start = min(L_beta, L_q) - 3*w_eff
        stop = max(L_beta, L_q) + 3*w_eff
        Ls = np.linspace(start, stop, Nt)
    return Ls/max(V,1e-9)

def scan_case(p, phase='exit', Nt=None, resolution='full'):
    if Nt is None:
        Nt = 11 if phase != 'exit' else 13
        if resolution == 'fast': Nt = 7 if phase != 'exit' else 9
    ts = t_grid_for_phase(p, phase, Nt=Nt)
    ls = l_grid_for_phase(phase, resolution=resolution)
    xs = np.array([[float(t), float(l), math.pi/2, 0.0] for t in ts for l in ls], dtype=np.float64)
    arr = np.array(curvature_grid(jnp.array(xs), p))
    nT, nL = len(ts), len(ls)
    arr3 = arr.reshape((nT, nL, arr.shape[1]))
    summary = {'phase': phase, 'Nt': nT, 'Nl': nL, 't_min': float(ts[0]), 't_max': float(ts[-1]), 'l_min': float(ls[0]), 'l_max': float(ls[-1])}
    for i,key in enumerate(names[:12]):
        vals = arr[:, i]
        summary['maxabs_' + key] = float(np.nanmax(np.abs(vals)))
        summary['min_' + key] = float(np.nanmin(vals))
        summary['max_' + key] = float(np.nanmax(vals))
    prod = arr[:,8]*arr[:,9]
    summary['theta_product_min'] = float(np.nanmin(prod))
    summary['theta_product_max'] = float(np.nanmax(prod))
    summary['min_det'] = float(np.nanmin(arr[:,7]))
    summary['max_gtt'] = float(np.nanmax(arr[:,6]))
    summary['min_gtt'] = float(np.nanmin(arr[:,6]))
    summary['gtt_positive_points'] = int(np.sum(arr[:,6] > 1e-9))
    V = float(p[5]); S = arr[:,12]; E = arr[:,15]; A = arr[:,16]; T = arr[:,17]; Wm = arr[:,13]
    margin = T - A*abs(V)*E*S*Wm
    summary['min_lapse_shift_margin'] = float(np.nanmin(margin))
    Rth=float(p[2]); Rpass=float(p[3]); Delta=float(p[1])
    Bth_list=[]; Bpass_list=[]; Btot_list=[]; th_share=[]; pass_share=[]
    dl=(ls[-1]-ls[0])/(len(ls)-1)
    for ti,t in enumerate(ts):
        L = float(V*t)
        vals = arr3[ti,:,:]
        burden = (np.abs(vals[:,0]) + np.sqrt(np.maximum(np.abs(vals[:,2]),0.0)) +
                  np.maximum(0.0, -vals[:,4]) + np.maximum(0.0, -vals[:,5]) +
                  np.abs(vals[:,10]) + np.abs(vals[:,11]))
        throat_mask = np.abs(ls) <= (Rth + Delta)
        pass_mask = np.abs(ls - L) <= (Rpass + Delta)
        Btot = float(np.sum(burden)*dl)
        Bth = float(np.sum(burden[throat_mask])*dl)
        Bpass = float(np.sum(burden[pass_mask])*dl)
        Bth_list.append(Bth); Bpass_list.append(Bpass); Btot_list.append(Btot)
        th_share.append(Bth/Btot if Btot > 0 else np.nan)
        pass_share.append(Bpass/Btot if Btot > 0 else np.nan)
    summary['max_B_total'] = float(np.nanmax(Btot_list))
    summary['mean_throat_burden_share'] = float(np.nanmean(th_share))
    summary['min_throat_burden_share'] = float(np.nanmin(th_share))
    summary['mean_passenger_region_burden_share'] = float(np.nanmean(pass_share))
    summary['max_passenger_region_burden_share'] = float(np.nanmax(pass_share))
    summary['max_A'] = float(np.nanmax(arr[:,16])); summary['min_A'] = float(np.nanmin(arr[:,16]))
    summary['max_T'] = float(np.nanmax(arr[:,17])); summary['min_T'] = float(np.nanmin(arr[:,17]))
    summary['max_q'] = float(np.nanmax(arr[:,14])); summary['min_q'] = float(np.nanmin(arr[:,14]))
    summary['max_E'] = float(np.nanmax(arr[:,15])); summary['min_E'] = float(np.nanmin(arr[:,15]))
    summary['max_A_departure_from_1'] = float(max(abs(summary['max_A']-1.0), abs(summary['min_A']-1.0)))
    summary['max_T_departure_from_1'] = float(max(abs(summary['max_T']-1.0), abs(summary['min_T']-1.0)))
    summary['max_gtt_departure_from_minus1'] = float(max(abs(summary['max_gtt']+1.0), abs(summary['min_gtt']+1.0)))
    return summary

def lambda_for_V(V): return max(1.05, 1.15*float(V))

def config_grid():
    Vs = [0.9, 1.01, 1.1, 1.25, 1.5, 2.0]
    C0s = [100.0, 1e4]
    Deltas = [0.3, 0.1]
    widths = [0.35, 0.18]
    gaps = [0.35, 0.70, 1.00]
    configs=[]
    for V in Vs:
        lam=lambda_for_V(V)
        for C0 in C0s:
            for Delta in Deltas:
                for w_release in widths:
                    L_q=1.10
                    configs.append(('synchronized',0,V,lam,C0,Delta,w_release,L_q,L_q,0.0))
                    for gap in gaps:
                        L_beta=1.10-gap
                        configs.append(('shift_first',1,V,lam,C0,Delta,w_release,L_beta,1.10,gap))
                        configs.append(('rapid_shift_first',2,V,lam,C0,Delta,w_release,L_beta,1.10,gap))
    return configs

def profile_suites():
    # coherent families plus one-at-a-time swaps and release mismatches
    suites=[]
    for pid,name in PROFILE_NAMES.items():
        rid = 0 if pid==0 else pid
        suites.append((f'coherent_{name}', pid,pid,rid,rid))
    # one-at-a-time W/S replacements under baseline release
    for pid,name in PROFILE_NAMES.items():
        if pid!=0:
            suites.append((f'W_{name}_only', pid,0,0,0))
            suites.append((f'S_{name}_only', 0,pid,0,0))
    # release variants/mismatches under baseline shape
    for eid,ename in RELEASE_NAMES.items():
        for qid,qname in RELEASE_NAMES.items():
            if eid==0 and qid==0: continue
            if eid==qid or (eid,qid) in [(1,0),(0,1),(2,0),(0,2),(3,0),(0,3),(1,2),(2,1),(3,2),(2,3)]:
                suites.append((f'E_{ename}_q_{qname}',0,0,eid,qid))
    # remove duplicates while preserving order
    seen=set(); out=[]
    for s in suites:
        key=s[1:]
        if key not in seen:
            seen.add(key); out.append(s)
    return out

def run_suite(suites, configs, phases=('traverse','exit','post'), resolution='full', out='/mnt/data/profile_robustness_results.json'):
    start=time.time()
    _ = curvature_one(jnp.array([0.0,0.0,math.pi/2,0.0], dtype=jnp.float64), make_params())
    rows=[]; cases=0
    total=len(suites)*len(configs)*len(phases)
    for si,(suite,Wp,Sp,Ep,qp) in enumerate(suites,1):
        for ci,(mode_name,mode_id,V,lam,C0,Delta,w_release,L_beta,L_q,release_gap) in enumerate(configs,1):
            p = make_params(C0=C0, Delta=Delta, V=V, lapse_lambda=lam, L_beta=L_beta, L_q=L_q, w_release=w_release, mode_id=mode_id,
                            W_profile=Wp, S_profile=Sp, E_profile=Ep, q_profile=qp)
            phsum={}
            for phase in phases:
                s=scan_case(p, phase=phase, resolution=resolution)
                phsum[phase]=s; cases+=1
            tr=phsum.get('traverse',{}); ex=phsum.get('exit',{}); po=phsum.get('post',{})
            row={
                'suite':suite,'W_profile':PROFILE_NAMES[Wp],'S_profile':PROFILE_NAMES[Sp],
                'E_profile':RELEASE_NAMES[Ep],'q_profile':RELEASE_NAMES[qp],
                'mode':mode_name,'release_gap':release_gap,'V':V,'lapse_lambda':lam,'C0':C0,'Delta':Delta,'w_release':w_release,
                'traverse_max_gtt':tr.get('max_gtt'), 'traverse_gtt_positive_points':tr.get('gtt_positive_points'), 'traverse_min_margin':tr.get('min_lapse_shift_margin'),
                'exit_max_gtt':ex.get('max_gtt'), 'exit_gtt_positive_points':ex.get('gtt_positive_points'), 'exit_min_margin':ex.get('min_lapse_shift_margin'),
                'exit_max_theta_product':ex.get('theta_product_max'), 'exit_max_Kretsch':ex.get('maxabs_Kretsch'), 'exit_max_R':ex.get('maxabs_R'),
                'exit_min_Gkk':min(ex.get('min_Gkp',0), ex.get('min_Gkm',0)),
                'exit_max_tidal_radial':ex.get('maxabs_tidal_radial'), 'exit_max_tidal_angular':ex.get('maxabs_tidal_angular'),
                'exit_mean_throat_burden_share':ex.get('mean_throat_burden_share'), 'exit_min_throat_burden_share':ex.get('min_throat_burden_share'),
                'exit_max_passenger_region_burden_share':ex.get('max_passenger_region_burden_share'),
                'post_max_A_departure_from_1':po.get('max_A_departure_from_1'), 'post_max_T_departure_from_1':po.get('max_T_departure_from_1'),
                'post_max_gtt_departure_from_minus1':po.get('max_gtt_departure_from_minus1'),
                'clean_traverse_and_exit': (tr.get('gtt_positive_points',0)==0 and ex.get('gtt_positive_points',0)==0 and tr.get('min_lapse_shift_margin',0)>0 and ex.get('min_lapse_shift_margin',0)>0),
            }
            rows.append(row)
        print(f'suite {si}/{len(suites)} {suite}: {len(configs)} configs, elapsed {time.time()-start:.1f}s', flush=True)
    payload=summarize(rows, suites, configs, phases, resolution, cases, time.time()-start)
    with open(out,'w') as f: json.dump(payload,f,indent=2)
    return payload

def summarize(rows, suites, configs, phases, resolution, cases, elapsed):
    def finite(vals): return [v for v in vals if v is not None and np.isfinite(v)]
    suite_stats=[]
    for suite,*_ in suites:
        rr=[r for r in rows if r['suite']==suite]
        suite_stats.append({
            'suite':suite,'configs':len(rr),
            'clean_configs':int(sum(r['clean_traverse_and_exit'] for r in rr)),
            'exit_gtt_positive_configs':int(sum((r['exit_gtt_positive_points'] or 0)>0 for r in rr)),
            'traverse_gtt_positive_configs':int(sum((r['traverse_gtt_positive_points'] or 0)>0 for r in rr)),
            'worst_exit_max_gtt':float(max(finite([r['exit_max_gtt'] for r in rr]))),
            'worst_traverse_max_gtt':float(max(finite([r['traverse_max_gtt'] for r in rr]))),
            'worst_exit_min_margin':float(min(finite([r['exit_min_margin'] for r in rr]))),
            'worst_traverse_min_margin':float(min(finite([r['traverse_min_margin'] for r in rr]))),
            'worst_exit_theta_product':float(max(finite([r['exit_max_theta_product'] for r in rr]))),
            'median_exit_theta_product':float(np.median(finite([r['exit_max_theta_product'] for r in rr]))),
            'worst_exit_Kretsch':float(max(finite([r['exit_max_Kretsch'] for r in rr]))),
            'median_exit_Kretsch':float(np.median(finite([r['exit_max_Kretsch'] for r in rr]))),
            'worst_tidal_radial':float(max(finite([r['exit_max_tidal_radial'] for r in rr]))),
            'worst_tidal_angular':float(max(finite([r['exit_max_tidal_angular'] for r in rr]))),
            'mean_throat_burden_share':float(np.mean(finite([r['exit_mean_throat_burden_share'] for r in rr]))),
            'min_throat_burden_share':float(min(finite([r['exit_min_throat_burden_share'] for r in rr]))),
            'post_worst_A_departure':float(max(finite([r['post_max_A_departure_from_1'] for r in rr]))),
            'post_worst_T_departure':float(max(finite([r['post_max_T_departure_from_1'] for r in rr]))),
            'post_worst_gtt_departure':float(max(finite([r['post_max_gtt_departure_from_minus1'] for r in rr]))),
        })
    mode_stats=[]
    for mode in sorted(set(r['mode'] for r in rows)):
        rr=[r for r in rows if r['mode']==mode]
        mode_stats.append({
            'mode':mode,'configs':len(rr), 'clean_configs':int(sum(r['clean_traverse_and_exit'] for r in rr)),
            'exit_gtt_positive_configs':int(sum((r['exit_gtt_positive_points'] or 0)>0 for r in rr)),
            'worst_exit_max_gtt':float(max(finite([r['exit_max_gtt'] for r in rr]))),
            'worst_exit_theta_product':float(max(finite([r['exit_max_theta_product'] for r in rr]))),
            'mean_throat_burden_share':float(np.mean(finite([r['exit_mean_throat_burden_share'] for r in rr]))),
            'min_throat_burden_share':float(min(finite([r['exit_min_throat_burden_share'] for r in rr]))),
        })
    V_stats=[]
    for V in sorted(set(r['V'] for r in rows)):
        rr=[r for r in rows if r['V']==V]
        V_stats.append({
            'V':V,'configs':len(rr),'clean_configs':int(sum(r['clean_traverse_and_exit'] for r in rr)),
            'exit_gtt_positive_configs':int(sum((r['exit_gtt_positive_points'] or 0)>0 for r in rr)),
            'worst_exit_max_gtt':float(max(finite([r['exit_max_gtt'] for r in rr]))),
            'worst_exit_theta_product':float(max(finite([r['exit_max_theta_product'] for r in rr]))),
            'mean_throat_burden_share':float(np.mean(finite([r['exit_mean_throat_burden_share'] for r in rr]))),
            'min_throat_burden_share':float(min(finite([r['exit_min_throat_burden_share'] for r in rr]))),
        })
    top_theta=sorted(rows, key=lambda r: (r['exit_max_theta_product'] if r['exit_max_theta_product'] is not None else -np.inf), reverse=True)[:10]
    low_burden=sorted(rows, key=lambda r: (r['exit_min_throat_burden_share'] if r['exit_min_throat_burden_share'] is not None else np.inf))[:10]
    worst_gtt=sorted(rows, key=lambda r: (r['exit_max_gtt'] if r['exit_max_gtt'] is not None else -np.inf), reverse=True)[:10]
    return {'metadata':{'suite_count':len(suites),'config_count':len(configs),'row_count':len(rows),'case_count':cases,'phases':phases,'resolution':resolution,'elapsed_seconds':elapsed},
            'suite_stats':suite_stats,'mode_stats':mode_stats,'velocity_stats':V_stats,'top_exit_theta_product':top_theta,'lowest_throat_burden':low_burden,'worst_exit_gtt':worst_gtt,'rows':rows}

if __name__=='__main__':
    # default test run can be overridden by environment
    mode=os.environ.get('RUN_MODE','smoke')
    if mode=='smoke':
        suites=profile_suites()[:2]
        configs=config_grid()[:2]
        payload=run_suite(suites, configs, resolution='fast', out='/mnt/data/profile_robustness_smoke.json')
    elif mode=='full_suites':
        payload=run_suite(profile_suites(), config_grid(), resolution=os.environ.get('RESOLUTION','full'), out='/mnt/data/profile_robustness_results.json')
    elif mode=='coherent':
        suites=[s for s in profile_suites() if s[0].startswith('coherent_')]
        payload=run_suite(suites, config_grid(), resolution=os.environ.get('RESOLUTION','full'), out='/mnt/data/profile_robustness_coherent.json')
    print(json.dumps(payload['metadata'], indent=2))
    print(json.dumps(payload['suite_stats'][:5], indent=2))
