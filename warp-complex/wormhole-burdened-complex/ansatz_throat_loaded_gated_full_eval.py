import math, json, os, time
from dataclasses import dataclass
import numpy as np
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp

# Full reduced throat-loaded evaluation.
# Coordinates x=(t,l,theta,phi), Phi=0, r(l)=sqrt(r0^2+l^2).
# Throat-loaded capacity/lapse:
#   A(l,t)=exp(q(L) W(l) ln C0)
#   T(l,t)=exp(q(L) W(l) ln(lambda*C0))
# Transport/coupling shift:
#   beta^l=-V E(L) W(l) S_pass(l-L(t))
# Release modes:
#   synchronized: E(L)=q(L)
#   shift_first: E(L) tapers before q(L)
#   rapid_shift_first: same ordering with a narrower release layer

names = [
    'R','Ricci2','Kretsch','Gnn','Gkp','Gkm','gtt','det','theta_p','theta_m',
    'tidal_radial','tidal_angular','S_pass','W','q','E','A','T','r','rho_pass','L'
]

# p vector indices:
# C0, Delta, Rth, Rpass, r0, V, lambda, L_beta, L_q, w_release, mode_id, eps, wth, wpass

def make_params(C0=100.0, Delta=0.3, Rth=0.75, Rpass=0.35, r0=1.0,
                V=0.9, lapse_lambda=1.05, L_beta=0.75, L_q=1.10,
                w_release=0.25, mode_id=1, eps=1e-5):
    return jnp.array([
        float(C0), float(Delta), float(Rth), float(Rpass), float(r0),
        float(V), float(lapse_lambda), float(L_beta), float(L_q),
        float(w_release), float(mode_id), float(eps), float(Delta/6.0), float(Delta/6.0)
    ], dtype=jnp.float64)


def bump_from_squared_radius(x2, R, w):
    # tanh proxy with squared-radius argument to keep smoothness at the center.
    z = (x2 - R*R)/(2.0*R*w)
    return 0.5*(1.0 - jnp.tanh(z))


def falloff(z, w):
    return 0.5*(1.0 - jnp.tanh(z/w))


def release_profiles(L, p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass = p
    # mode_id: 0=synchronized, 1=shift_first, 2=rapid_shift_first
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

    # Radial and angular tidal components in a local ADM-normal orthonormal frame.
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


def l_grid_for_phase(phase):
    if phase == 'traverse':
        return np.linspace(-1.4, 1.4, 81)
    if phase == 'post':
        return np.linspace(-1.4, 2.4, 81)
    return np.linspace(-1.4, 2.4, 91)


def t_grid_for_phase(p, phase, Nt=13):
    V = float(p[5]); L_beta=float(p[7]); L_q=float(p[8]); w=float(p[9]); mode=float(p[10])
    # Convert position windows into times through L=Vt.
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


def scan_case(p, phase='exit', Nt=13):
    ts = t_grid_for_phase(p, phase, Nt=Nt)
    ls = l_grid_for_phase(phase)
    xs = np.array([[float(t), float(l), math.pi/2, 0.0] for t in ts for l in ls], dtype=np.float64)
    arr = np.array(curvature_grid(jnp.array(xs), p))
    nT, nL = len(ts), len(ls)
    arr3 = arr.reshape((nT, nL, arr.shape[1]))
    summary = {'phase': phase, 'Nt': nT, 'Nl': nL, 't_min': float(ts[0]), 't_max': float(ts[-1]), 'l_min': float(ls[0]), 'l_max': float(ls[-1])}

    # Scalar maxima/minima with locations.
    for i,key in enumerate(names[:12]):
        vals = arr[:, i]
        idx = int(np.nanargmax(np.abs(vals)))
        ti, li = divmod(idx, nL)
        summary['maxabs_' + key] = float(np.nanmax(np.abs(vals)))
        summary['min_' + key] = float(np.nanmin(vals))
        summary['max_' + key] = float(np.nanmax(vals))
        summary['t_at_maxabs_' + key] = float(ts[ti])
        summary['l_at_maxabs_' + key] = float(ls[li])

    prod = arr[:,8]*arr[:,9]
    idx = int(np.nanargmax(prod)); ti,li = divmod(idx,nL)
    summary['theta_product_min'] = float(np.nanmin(prod))
    summary['theta_product_max'] = float(np.nanmax(prod))
    summary['t_at_theta_product_max'] = float(ts[ti])
    summary['l_at_theta_product_max'] = float(ls[li])
    summary['min_det'] = float(np.nanmin(arr[:,7]))
    summary['max_gtt'] = float(np.nanmax(arr[:,6]))
    summary['min_gtt'] = float(np.nanmin(arr[:,6]))
    summary['gtt_positive_points'] = int(np.sum(arr[:,6] > 1e-9))

    # Lapse-shift margin T - A |V| E S.
    V = float(p[5]); S = arr[:,12]; E = arr[:,15]; A = arr[:,16]; T = arr[:,17]
    Wm = arr[:,13]
    margin = T - A*abs(V)*E*S*Wm
    idx = int(np.nanargmin(margin)); ti, li = divmod(idx, nL)
    summary['min_lapse_shift_margin'] = float(np.nanmin(margin))
    summary['t_at_min_margin'] = float(ts[ti])
    summary['l_at_min_margin'] = float(ls[li])

    # Burden proxy split across throat and passenger regions.
    Rth=float(p[2]); Rpass=float(p[3]); Delta=float(p[1])
    Bth_list=[]; Bpass_list=[]; Btot_list=[]; th_share=[]; pass_share=[]
    throat_min_l=[]; throat_min_R=[]; throat_min_d2=[]
    dl=(ls[-1]-ls[0])/(len(ls)-1)
    for ti,t in enumerate(ts):
        L = float(V*t)
        vals = arr3[ti,:,:]
        burden = (
            np.abs(vals[:,0]) + np.sqrt(np.maximum(np.abs(vals[:,2]),0.0)) +
            np.maximum(0.0, -vals[:,4]) + np.maximum(0.0, -vals[:,5]) +
            np.abs(vals[:,10]) + np.abs(vals[:,11])
        )
        throat_mask = np.abs(ls) <= (Rth + Delta)
        pass_mask = np.abs(ls - L) <= (Rpass + Delta)
        Btot = float(np.sum(burden)*dl)
        Bth = float(np.sum(burden[throat_mask])*dl)
        Bpass = float(np.sum(burden[pass_mask])*dl)
        Bth_list.append(Bth); Bpass_list.append(Bpass); Btot_list.append(Btot)
        th_share.append(Bth/Btot if Btot > 0 else np.nan)
        pass_share.append(Bpass/Btot if Btot > 0 else np.nan)

        Reff = vals[:,16]*vals[:,18]
        j = int(np.argmin(Reff))
        throat_min_l.append(float(ls[j])); throat_min_R.append(float(Reff[j]))
        if 0 < j < len(ls)-1:
            d2 = (Reff[j+1]**2 - 2*Reff[j]**2 + Reff[j-1]**2)/(dl*dl)
            throat_min_d2.append(float(d2))
        else:
            throat_min_d2.append(float('nan'))

    summary['max_B_total'] = float(np.nanmax(Btot_list))
    summary['max_B_throat'] = float(np.nanmax(Bth_list))
    summary['max_B_passenger_region'] = float(np.nanmax(Bpass_list))
    summary['mean_throat_burden_share'] = float(np.nanmean(th_share))
    summary['min_throat_burden_share'] = float(np.nanmin(th_share))
    summary['mean_passenger_region_burden_share'] = float(np.nanmean(pass_share))
    summary['max_passenger_region_burden_share'] = float(np.nanmax(pass_share))

    summary['throat_min_l_maxabs'] = float(np.nanmax(np.abs(throat_min_l)))
    summary['throat_min_R_min'] = float(np.nanmin(throat_min_R))
    summary['throat_min_R_max'] = float(np.nanmax(throat_min_R))
    summary['throat_min_d2_Reff2_min'] = float(np.nanmin(throat_min_d2))

    # Post/field state ranges.
    summary['max_A'] = float(np.nanmax(arr[:,16])); summary['min_A'] = float(np.nanmin(arr[:,16]))
    summary['max_T'] = float(np.nanmax(arr[:,17])); summary['min_T'] = float(np.nanmin(arr[:,17]))
    summary['max_q'] = float(np.nanmax(arr[:,14])); summary['min_q'] = float(np.nanmin(arr[:,14]))
    summary['max_E'] = float(np.nanmax(arr[:,15])); summary['min_E'] = float(np.nanmin(arr[:,15]))
    summary['max_A_departure_from_1'] = float(max(abs(summary['max_A']-1.0), abs(summary['min_A']-1.0)))
    summary['max_T_departure_from_1'] = float(max(abs(summary['max_T']-1.0), abs(summary['min_T']-1.0)))
    summary['max_gtt_departure_from_minus1'] = float(max(abs(summary['max_gtt']+1.0), abs(summary['min_gtt']+1.0)))
    return summary


def lambda_for_V(V):
    # Margin chosen to test architecture rather than equality-boundary behavior.
    return max(1.05, 1.15*float(V))


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
                    # synchronized baseline: shift and throat release share one position.
                    L_q=1.10
                    configs.append(('synchronized',0,V,lam,C0,Delta,w_release,L_q,L_q,0.0))
                    # shift-first cases: shift release occurs upstream of throat release.
                    for gap in gaps:
                        L_beta=1.10-gap
                        configs.append(('shift_first',1,V,lam,C0,Delta,w_release,L_beta,1.10,gap))
                        configs.append(('rapid_shift_first',2,V,lam,C0,Delta,w_release,L_beta,1.10,gap))
    return configs


def run(out_results='/mnt/data/ansatz_throat_loaded_gated_full_eval_results.json',
        out_summary='/mnt/data/ansatz_throat_loaded_gated_full_eval_summary.json',
        out_markdown='/mnt/data/ansatz_throat_loaded_gated_full_eval_notes.md'):
    start=time.time()
    _ = curvature_one(jnp.array([0.0,0.0,math.pi/2,0.0], dtype=jnp.float64), make_params())
    cases=[]
    configs=config_grid()
    for idx,(mode_name,mode_id,V,lam,C0,Delta,w_release,L_beta,L_q,release_gap) in enumerate(configs, start=1):
        p = make_params(C0=C0, Delta=Delta, V=V, lapse_lambda=lam, L_beta=L_beta, L_q=L_q, w_release=w_release, mode_id=mode_id)
        for phase in ['traverse','exit','post']:
            Nt=11 if phase != 'exit' else 13
            s = scan_case(p, phase=phase, Nt=Nt)
            s.update({
                'mode': mode_name, 'mode_id': int(mode_id), 'V': float(V), 'lapse_lambda': float(lam),
                'C0': float(C0), 'Delta': float(Delta), 'w_release': float(w_release),
                'L_beta': float(L_beta), 'L_q': float(L_q), 'release_gap': float(release_gap), 'lambda_over_V': float(lam/V)
            })
            cases.append(s)
        if idx % 12 == 0 or idx == len(configs):
            print(f"completed {idx}/{len(configs)} configs in {time.time()-start:.1f}s", flush=True)

    # Aggregate per configuration.
    groups={}
    for c in cases:
        key=(c['mode'],c['release_gap'],c['V'],c['lapse_lambda'],c['C0'],c['Delta'],c['w_release'])
        groups.setdefault(key,{})[c['phase']]=c
    rows=[]
    for key,ph in groups.items():
        mode,release_gap,V,lam,C0,Delta,w_release=key
        tr=ph.get('traverse',{}); ex=ph.get('exit',{}); po=ph.get('post',{})
        rows.append({
            'mode':mode,'release_gap':release_gap,'V':V,'lapse_lambda':lam,'lambda_over_V':lam/V,'C0':C0,'Delta':Delta,'w_release':w_release,
            'traverse_max_gtt':tr.get('max_gtt'), 'exit_max_gtt':ex.get('max_gtt'), 'post_max_gtt':po.get('max_gtt'),
            'exit_gtt_positive_points':ex.get('gtt_positive_points'),
            'exit_min_margin':ex.get('min_lapse_shift_margin'),
            'exit_max_Kretsch':ex.get('maxabs_Kretsch'),
            'traverse_max_Kretsch':tr.get('maxabs_Kretsch'),
            'exit_to_traverse_Kretsch_ratio': (ex.get('maxabs_Kretsch',0)/max(tr.get('maxabs_Kretsch',1),1e-300)),
            'exit_max_R':ex.get('maxabs_R'),
            'exit_min_Gkk': min(ex.get('min_Gkp',0), ex.get('min_Gkm',0)),
            'exit_max_theta_product':ex.get('theta_product_max'),
            'exit_max_tidal_radial':ex.get('maxabs_tidal_radial'),
            'exit_max_tidal_angular':ex.get('maxabs_tidal_angular'),
            'exit_mean_throat_burden_share':ex.get('mean_throat_burden_share'),
            'exit_min_throat_burden_share':ex.get('min_throat_burden_share'),
            'exit_max_passenger_region_burden_share':ex.get('max_passenger_region_burden_share'),
            'exit_throat_min_l_maxabs':ex.get('throat_min_l_maxabs'),
            'exit_throat_min_d2_Reff2_min':ex.get('throat_min_d2_Reff2_min'),
            'post_max_A_departure_from_1':po.get('max_A_departure_from_1'),
            'post_max_T_departure_from_1':po.get('max_T_departure_from_1'),
            'post_max_gtt_departure_from_minus1':po.get('max_gtt_departure_from_minus1'),
        })

    # Mode/gap aggregates.
    mode_stats=[]
    stat_keys=[]
    for mode in ['synchronized','shift_first','rapid_shift_first']:
        gaps_sorted=sorted(set(r['release_gap'] for r in rows if r['mode']==mode))
        for gap in gaps_sorted:
            stat_keys.append((mode,gap))
    for mode,gap in stat_keys:
        mr=[r for r in rows if r['mode']==mode and r['release_gap']==gap]
        mode_stats.append({
            'mode':mode,
            'release_gap':gap,
            'configs':len(mr),
            'cases_with_exit_gtt_positive':int(sum((r['exit_gtt_positive_points'] or 0)>0 for r in mr)),
            'worst_exit_max_gtt':float(max(r['exit_max_gtt'] for r in mr)),
            'worst_exit_min_margin':float(min(r['exit_min_margin'] for r in mr)),
            'median_exit_min_margin':float(np.median([r['exit_min_margin'] for r in mr])),
            'worst_exit_theta_product':float(max(r['exit_max_theta_product'] for r in mr)),
            'median_exit_theta_product':float(np.median([r['exit_max_theta_product'] for r in mr])),
            'worst_exit_Kretsch':float(max(r['exit_max_Kretsch'] for r in mr)),
            'median_exit_Kretsch':float(np.median([r['exit_max_Kretsch'] for r in mr])),
            'mean_throat_burden_share':float(np.mean([r['exit_mean_throat_burden_share'] for r in mr])),
            'min_throat_burden_share':float(min(r['exit_min_throat_burden_share'] for r in mr)),
            'worst_tidal_radial':float(max(r['exit_max_tidal_radial'] for r in mr)),
            'worst_tidal_angular':float(max(r['exit_max_tidal_angular'] for r in mr)),
            'post_worst_A_departure':float(max(r['post_max_A_departure_from_1'] for r in mr)),
            'post_worst_T_departure':float(max(r['post_max_T_departure_from_1'] for r in mr)),
        })

    payload={'rows':rows,'mode_stats':mode_stats,'config_count':len(configs),'case_count':len(cases),'elapsed_seconds':time.time()-start}
    with open(out_results,'w') as f: json.dump(cases,f,indent=2)
    with open(out_summary,'w') as f: json.dump(payload,f,indent=2)

    # Compact notes markdown with no external citations; final response will cite the source file.
    with open(out_markdown,'w') as f:
        f.write('# Throat-Loaded Gated-Shift Full Reduced Evaluation Notes\n\n')
        f.write('This file summarizes the numerical outputs from `ansatz_throat_loaded_full_eval.py`.\n\n')
        f.write('## Mode aggregates\n\n')
        f.write('| mode | configs | gtt-positive exits | worst max gtt | worst min margin | worst theta product | worst Kretsch | mean throat burden share | min throat burden share |\n')
        f.write('|---|---:|---:|---:|---:|---:|---:|---:|---:|\n')
        for m in mode_stats:
            f.write(f"| {m['mode']} / gap {m.get('release_gap',0):.2f} | {m['configs']} | {m['cases_with_exit_gtt_positive']} | {m['worst_exit_max_gtt']:.6g} | {m['worst_exit_min_margin']:.6g} | {m['worst_exit_theta_product']:.6g} | {m['worst_exit_Kretsch']:.6g} | {m['mean_throat_burden_share']:.4f} | {m['min_throat_burden_share']:.4f} |\n")
        f.write('\n## Velocity ladder\n\n')
        f.write('`V = {0.9, 1.01, 1.1, 1.25, 1.5, 2.0}` with `lambda = max(1.05, 1.15 V)`. Shift-first cases sweep release gaps `{0.35, 0.70, 1.00}`.\n')
        f.write('\n## Files\n\n')
        f.write('- Raw cases: `ansatz_throat_loaded_full_eval_results.json`\n')
        f.write('- Summary: `ansatz_throat_loaded_full_eval_summary.json`\n')
    return payload

if __name__ == '__main__':
    payload=run()
    print(json.dumps(payload['mode_stats'], indent=2))
