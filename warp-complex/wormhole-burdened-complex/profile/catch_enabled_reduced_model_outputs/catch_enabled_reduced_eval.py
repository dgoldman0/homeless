#!/usr/bin/env python3
"""
Catch-enabled throat-loaded gated-shift reduced evaluator.

This is a reduced prescribed-metric test, not a 3+1 solve.
It separates the passenger center X(t) from the old X=Vt profile center
and adds a smooth catch/rematching phase before shift release.

Core sequence:
  catch/rematch passenger speed -> shift release E(X) -> throat support release q(X)

Metric:
  A = exp(q(X) W(l) ln C0)
  T = exp(q(X) W(l) ln(lambda C0))
  beta^l = -U(t) E(X) W(l) S(l-X)
where U=dX/dt is the captured passenger coordinate speed.

Requires: numpy, pandas, jax.
"""

import math, json, time
import numpy as np
import pandas as pd
import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp

NAMES = [
    'R','Ricci2','Kretsch','Gnn','Gkp','Gkm','gtt','det','theta_p','theta_m',
    'tidal_radial_adm','tidal_angular_adm','S_pass','W','q','E','A','T','r','rho_pass_coord','X','U',
    'worldline_norm','v_rel','gamma_rel','tidal_radial_pass','tidal_angular_pass',
    'rho_adm','rho_world','j_l_adm','p_l_adm','p_th_adm','p_ph_adm'
]

def make_params_catch(C0=100.0, Delta=0.3, Rth=0.75, Rpass=0.35, r0=1.0,
                      V=2.0, lapse_lambda=None, L_beta=1.10, L_q=1.45,
                      w_release=0.30, mode_id=1, eps=1e-5,
                      v_exit=0.5, L_catch=0.65, w_catch_L=0.25):
    if lapse_lambda is None:
        lapse_lambda = max(1.05, 1.20*float(V))
    t_catch = float(L_catch)/max(float(V), 1e-9)
    w_catch = float(w_catch_L)/max(float(V), 1e-9)
    return jnp.array([
        float(C0), float(Delta), float(Rth), float(Rpass), float(r0),
        float(V), float(lapse_lambda), float(L_beta), float(L_q),
        float(w_release), float(mode_id), float(eps), float(Delta/6.0), float(Delta/6.0),
        float(v_exit), float(t_catch), float(w_catch)
    ], dtype=jnp.float64)

def falloff(z, w):
    return 0.5*(1.0 - jnp.tanh(z/w))

def smooth_integral_falloff(t, tc, wc):
    def F(s):
        return 0.5*s - 0.5*wc*jnp.log(jnp.cosh((s-tc)/wc))
    return F(t) - F(0.0)

def passenger_X_U(t, p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass,v_exit,t_catch,w_catch = p
    C = falloff(t - t_catch, w_catch)
    X = v_exit*t + (V-v_exit)*smooth_integral_falloff(t, t_catch, w_catch)
    U = v_exit + (V-v_exit)*C
    return X, U, C

def bump_from_squared_radius(x2, R, w):
    z = (x2 - R*R)/(2.0*R*w)
    return 0.5*(1.0 - jnp.tanh(z))

def release_profiles_from_X(X, p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass,v_exit,t_catch,w_catch = p
    w = jnp.where(mode_id > 1.5, 0.5*w_release, w_release)
    q_shift = falloff(X - L_beta, w)
    q_throat = falloff(X - L_q, w)
    sync = falloff(X - L_q, w)
    E = jnp.where(mode_id < 0.5, sync, q_shift)
    q = jnp.where(mode_id < 0.5, sync, q_throat)
    return q, E

def scalars_catch(x, p):
    C0,Delta,Rth,Rpass,r0,V,lapse_lambda,L_beta,L_q,w_release,mode_id,eps,wth,wpass,v_exit,t_catch,w_catch = p
    t,l,th,ph = x
    X, U, Ccatch = passenger_X_U(t, p)
    q, E = release_profiles_from_X(X, p)
    W = bump_from_squared_radius(l*l, Rth, wth)
    rho2 = (l-X)*(l-X) + eps*eps
    S_pass = bump_from_squared_radius(rho2, Rpass, wpass)
    A = jnp.exp(q*W*jnp.log(C0))
    T = jnp.exp(q*W*jnp.log(lapse_lambda*C0))
    r = jnp.sqrt(r0*r0 + l*l)
    rho = jnp.sqrt(rho2)
    return S_pass, W, q, E, A, T, r, rho, X, U

def metric_catch(x, p):
    S,W,q,E,A,T,r,rho,X,U = scalars_catch(x,p)
    th = x[2]
    beta = -U*E*S*W
    return jnp.array([
        [-T*T + A*A*beta*beta, A*A*beta, 0.0, 0.0],
        [ A*A*beta,             A*A,       0.0, 0.0],
        [0.0,                   0.0,       A*A*r*r, 0.0],
        [0.0,                   0.0,       0.0, A*A*r*r*jnp.sin(th)**2],
    ], dtype=jnp.float64)

def gamma_conn_catch(x, p):
    g = metric_catch(x,p)
    dg = jax.jacfwd(metric_catch, argnums=0)(x,p)
    ginv = jnp.linalg.inv(g)
    return 0.5*(jnp.einsum('ad,cdb->abc', ginv, dg) +
                jnp.einsum('ad,bdc->abc', ginv, dg) -
                jnp.einsum('ad,bcd->abc', ginv, dg))

def R_eff_catch(x,p):
    S,W,q,E,A,T,r,rho,X,U = scalars_catch(x,p)
    return A*r

def curvature_catch_raw(x,p):
    g = metric_catch(x,p); ginv = jnp.linalg.inv(g)
    Gam = gamma_conn_catch(x,p)
    dGam = jax.jacfwd(gamma_conn_catch, argnums=0)(x,p)
    deriv = jnp.transpose(dGam,(0,2,3,1)) - jnp.transpose(dGam,(0,2,1,3))
    prod1 = jnp.einsum('ame,ens->asmn', Gam, Gam)
    prod2 = jnp.einsum('ane,ems->asmn', Gam, Gam)
    Riem = deriv + prod1 - prod2
    Ric = jnp.einsum('asan->sn', Riem)
    Rsc = jnp.einsum('ab,ab->', ginv, Ric)
    G = Ric - 0.5*g*Rsc
    Rdown = jnp.einsum('pa,asmn->psmn', g, Riem)
    Ricci2 = jnp.einsum('ab,cd,ac,bd->', Ric, Ric, ginv, ginv)
    Kretsch = jnp.einsum('abcd,efgh,ae,bf,cg,dh->', Rdown, Rdown, ginv, ginv, ginv, ginv)
    S,W,q,E,A,T,r,rho,X,U = scalars_catch(x,p)
    beta = -U*E*S*W
    nvec = jnp.array([1.0/T, -beta/T, 0.0, 0.0])
    el = jnp.array([0.0, 1.0/A, 0.0, 0.0])
    eth = jnp.array([0.0, 0.0, 1.0/(A*r), 0.0])
    eph = jnp.array([0.0, 0.0, 0.0, 1.0/(A*r*jnp.sin(x[2]))])
    kp = jnp.array([1.0/T, -beta/T + 1.0/A, 0.0, 0.0])
    km = jnp.array([1.0/T, -beta/T - 1.0/A, 0.0, 0.0])
    Gnn = jnp.einsum('a,b,ab->', nvec,nvec,G)
    Gkp = jnp.einsum('a,b,ab->', kp,kp,G)
    Gkm = jnp.einsum('a,b,ab->', km,km,G)
    rho_adm = Gnn
    j_l_adm = -jnp.einsum('a,b,ab->', nvec, el, G)
    p_l_adm = jnp.einsum('a,b,ab->', el, el, G)
    p_th_adm = jnp.einsum('a,b,ab->', eth, eth, G)
    p_ph_adm = jnp.einsum('a,b,ab->', eph, eph, G)
    tidal_radial_adm = jnp.einsum('abcd,a,b,c,d->', Rdown, nvec, el, nvec, el)
    tidal_angular_adm = jnp.einsum('abcd,a,b,c,d->', Rdown, nvec, eth, nvec, eth)
    ucoord_raw = jnp.array([1.0, U, 0.0, 0.0])
    worldline_norm = jnp.einsum('a,b,ab->', ucoord_raw, ucoord_raw, g)
    v_rel = A*(U + beta)/T
    gamma_rel = 1.0/jnp.sqrt(jnp.maximum(1.0 - v_rel*v_rel, 1e-30))
    u_pass = gamma_rel*(nvec + v_rel*el)
    e_rad_pass = gamma_rel*(v_rel*nvec + el)
    tidal_radial_pass = jnp.einsum('abcd,a,b,c,d->', Rdown, u_pass, e_rad_pass, u_pass, e_rad_pass)
    tidal_angular_pass = jnp.einsum('abcd,a,b,c,d->', Rdown, u_pass, eth, u_pass, eth)
    rho_world = jnp.einsum('a,b,ab->', u_pass, u_pass, G)
    dR = jax.grad(R_eff_catch,argnums=0)(x,p)
    theta_p = 2/(A*r)*(((dR[0]-beta*dR[1])/T)+(1/A)*dR[1])
    theta_m = 2/(A*r)*(((dR[0]-beta*dR[1])/T)-(1/A)*dR[1])
    det = jnp.linalg.det(g); gtt = g[0,0]
    return jnp.array([
        Rsc, Ricci2, Kretsch, Gnn, Gkp, Gkm, gtt, det, theta_p, theta_m,
        tidal_radial_adm, tidal_angular_adm, S, W, q, E, A, T, r, rho, X, U,
        worldline_norm, v_rel, gamma_rel, tidal_radial_pass, tidal_angular_pass,
        rho_adm, rho_world, j_l_adm, p_l_adm, p_th_adm, p_ph_adm
    ], dtype=jnp.float64)

curvature_catch_grid = jax.jit(jax.vmap(curvature_catch_raw, in_axes=(0,None)))

def falloff_np(z,w):
    return 0.5*(1.0-np.tanh(z/w))

def XU_np(t, V, v_exit, t_catch, w_catch):
    def F(s):
        return 0.5*s - 0.5*w_catch*np.log(np.cosh((s-t_catch)/w_catch))
    C=falloff_np(t-t_catch,w_catch)
    X=v_exit*t + (V-v_exit)*(F(t)-F(0.0))
    U=v_exit + (V-v_exit)*C
    return X,U,C

def p_to_dict(p):
    arr=np.array(p)
    keys=['C0','Delta','Rth','Rpass','r0','V','lambda','L_beta','L_q','w_release','mode_id','eps','wth','wpass','v_exit','t_catch','w_catch']
    return dict(zip(keys, arr.tolist()))

def invert_X(target, p):
    d=p_to_dict(p); V=d['V']; v=d['v_exit']; tc=d['t_catch']; wc=d['w_catch']
    lo=-5.0/max(V,1e-6); hi=target/max(v,1e-6)+10.0
    for _ in range(80):
        mid=(lo+hi)/2
        xm,_,_=XU_np(mid,V,v,tc,wc)
        if xm<target: lo=mid
        else: hi=mid
    return (lo+hi)/2

def worldline_scan(p, Nx=49, X_min=-0.4, X_max=None):
    d=p_to_dict(p)
    if X_max is None:
        X_max=d['L_q']+5*d['w_release']
    t_min=invert_X(X_min,p); t_max=invert_X(X_max,p)
    ts=np.linspace(t_min,t_max,Nx)
    Xs=[]; Us=[]
    for t in ts:
        X,U,_=XU_np(t,d['V'],d['v_exit'],d['t_catch'],d['w_catch'])
        Xs.append(X); Us.append(U)
    xs=np.array([[t,x,math.pi/2,0.0] for t,x in zip(ts,Xs)], dtype=np.float64)
    arr=np.array(curvature_catch_grid(jnp.array(xs),p))
    idx={k:i for i,k in enumerate(NAMES)}
    prod=arr[:,idx['theta_p']]*arr[:,idx['theta_m']]
    neg_nec=np.maximum(0,-arr[:,idx['Gkp']])+np.maximum(0,-arr[:,idx['Gkm']])
    return {
        'V': d['V'], 'lambda': d['lambda'], 'lambda_over_V': d['lambda']/d['V'],
        'C0': d['C0'], 'Delta': d['Delta'], 'Rth': d['Rth'], 'Rpass': d['Rpass'],
        'v_exit': d['v_exit'], 'L_beta': d['L_beta'], 'L_q': d['L_q'], 'w_release': d['w_release'],
        'L_catch_design': d['V']*d['t_catch'], 'w_catch_L_design': d['V']*d['w_catch'],
        'timelike_fail_points': int(np.sum(arr[:,idx['worldline_norm']] >= -1e-9)),
        'max_worldline_norm': float(np.nanmax(arr[:,idx['worldline_norm']])),
        'max_abs_v_rel': float(np.nanmax(np.abs(arr[:,idx['v_rel']]))),
        'gtt_positive_points': int(np.sum(arr[:,idx['gtt']] > 1e-9)),
        'max_gtt': float(np.nanmax(arr[:,idx['gtt']])),
        'max_theta_product': float(np.nanmax(prod)),
        'max_neg_nec_sum': float(np.nanmax(neg_nec)),
        'min_rho_world': float(np.nanmin(arr[:,idx['rho_world']])),
        'max_abs_j_l_adm': float(np.nanmax(np.abs(arr[:,idx['j_l_adm']]))),
        'max_abs_p_th_adm': float(np.nanmax(np.abs(arr[:,idx['p_th_adm']]))),
        'max_abs_tidal_radial_pass': float(np.nanmax(np.abs(arr[:,idx['tidal_radial_pass']]))),
        'max_abs_tidal_angular_pass': float(np.nanmax(np.abs(arr[:,idx['tidal_angular_pass']]))),
    }

if __name__ == "__main__":
    rows=[]
    for V in [1.5,2.0,3.0,5.0,10.0]:
        p=make_params_catch(V=V, C0=100.0, Delta=0.3, v_exit=0.5, L_catch=0.65, w_catch_L=0.25)
        rows.append(worldline_scan(p,Nx=49))
    print(pd.DataFrame(rows).to_string(index=False))
