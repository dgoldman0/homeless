# T = lambda A Lapse-Margin Evaluation

## Purpose

This report evaluates the moving-shell compact-capacity branch with a lapse multiplier:

```math
T = A\lambda^S
```

The construction keeps the same capacity wall, trajectory, and radial reduction used in the previous lapse scans. The new element is the independent lapse margin parameter `lambda`. Inside the passenger region, where `S` is close to 1, this gives:

```math
T \approx \lambda A
```

Outside the compact support, where `S` is 0, the lapse returns to the exterior value:

```math
T = 1
```

The evaluation measures how added lapse margin changes the superluminal branch of the same moving-shell family.

## Reduced geometry

The scan uses the radial/spherical ADM reduction:

```math
ds^2 =
\left(-T^2 + A^2V^2S^2\right)dt^2
-2A^2VS\,dt\,dl
+A^2dl^2
+A^2r^2(l)d\Omega^2
```

with:

```math
r(l)=\sqrt{1+l^2}
```

```math
A=\exp(S\ln C_0)
```

```math
T=\exp(S\ln(\lambda C_0))=A\lambda^S
```

The shell profile is the same smooth tanh wall used in the earlier reduced tests. The scan uses the equatorial radial line at `t = 0` and evaluates invariant and projected quantities along `l`.

## Parameter grid

The scan covers:

```math
C_0 \in \{2,10,100,10^4\}
```

```math
\Delta \in \{1.0,0.3,0.1\}
```

```math
L_0 \in \{0,0.5\}
```

```math
V \in \{1.01,1.1,1.5,2.0\}
```

```math
\lambda \in \{1.05,1.1,1.5,2.0,2.25\}
```

Each `(lambda, V)` pair contains 24 cases from the combinations of `C0`, `Delta`, and `L0`.

## Central causal-margin relation

The diagnostic quantity is:

```math
g_{tt}=-T^2+A^2V^2S^2
```

For the compact-supported lapse family:

```math
T=A\lambda^S
```

The margin used in the scan is:

```math
T-A|V|S
```

Inside the passenger region, `S` is close to 1, so the relation becomes:

```math
g_{tt}\approx A^2(-\lambda^2+V^2)
```

The branch boundary is:

```math
\lambda=|V|
```

Pairs with `lambda >= V` remain on the sampled causal-margin branch. Pairs with `lambda < V` enter the positive-`gtt` branch in the shell interior.

## Causal branch count

Entries show positive-`gtt` cases out of 24 for each pair.

| lambda | V=1.01 | V=1.1 | V=1.5 | V=2.0 |
|---:|---:|---:|---:|---:|
| 1.05 | 0 / 24 | 24 / 24 | 24 / 24 | 24 / 24 |
| 1.1 | 0 / 24 | 0 / 24 | 24 / 24 | 24 / 24 |
| 1.5 | 0 / 24 | 0 / 24 | 0 / 24 | 24 / 24 |
| 2 | 0 / 24 | 0 / 24 | 0 / 24 | 0 / 24 |
| 2.25 | 0 / 24 | 0 / 24 | 0 / 24 | 0 / 24 |


The branch structure follows the expected threshold. The sampled pairs with `lambda >= V` remain on the margin-preserving branch. The sampled pairs with `lambda < V` enter the positive-`gtt` branch.

## Full aggregate results

| lambda | V | positive-gtt cases | min margin | max gtt | max theta product | max abs R | max Kretschmann | min Gkp | min Gkm | max throat shift |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.05 | 1.01 | 0 / 24 | 0.08 | -0.3296 | 29.86 | 8,278 | 1.461e+07 | -70.58 | -12,357 | 0.864 |
| 1.05 | 1.1 | 24 / 24 | -500.0 | 1.075e+07 | 503.5 | 7,581 | 1.272e+07 | -54.69 | -13,476 | 0.864 |
| 1.05 | 1.5 | 24 / 24 | -4,500 | 1.147e+08 | 5,660 | 18,036 | 6.338e+07 | -688.2 | -19,036 | 0.864 |
| 1.05 | 2 | 24 / 24 | -9,500 | 2.897e+08 | 15,301 | 48,438 | 4.521e+08 | -2,870 | -27,334 | 0.864 |
| 1.1 | 1.01 | 0 / 24 | 0.18 | -0.7596 | 27.44 | 8,558 | 1.562e+07 | -71.28 | -12,330 | 0.864 |
| 1.1 | 1.1 | 0 / 24 | 1.861e-13 | -8.184e-13 | 484.3 | 7,784 | 1.372e+07 | -56.00 | -13,446 | 0.864 |
| 1.1 | 1.5 | 24 / 24 | -4,000 | 1.040e+08 | 5,555 | 17,755 | 6.148e+07 | -683.4 | -18,991 | 0.864 |
| 1.1 | 2 | 24 / 24 | -9,000 | 2.790e+08 | 15,114 | 47,984 | 4.435e+08 | -2,855 | -27,266 | 0.864 |
| 1.5 | 1.01 | 0 / 24 | 0.98 | -1 | 21.77 | 10,380 | 2.316e+07 | -78.72 | -12,152 | 0.864 |
| 1.5 | 1.1 | 0 / 24 | 0.8 | -1 | 358.2 | 9,666 | 2.130e+07 | -57.31 | -13,249 | 0.864 |
| 1.5 | 1.5 | 0 / 24 | 1.665e-13 | -1.001e-12 | 4,874 | 15,912 | 4.981e+07 | -651.8 | -18,694 | 0.864 |
| 1.5 | 2 | 24 / 24 | -5,000 | 1.750e+08 | 13,905 | 45,005 | 3.892e+08 | -2,760 | -26,816 | 0.864 |
| 2 | 1.01 | 0 / 24 | 1 | -1 | 16.57 | 12,017 | 3.149e+07 | -96.56 | -11,989 | 0.864 |
| 2 | 1.1 | 0 / 24 | 1 | -1 | 261.0 | 11,420 | 2.978e+07 | -67.57 | -13,068 | 0.864 |
| 2 | 1.5 | 0 / 24 | 0.9324 | -1 | 4,277 | 14,244 | 4.054e+07 | -623.4 | -18,422 | 0.864 |
| 2 | 2 | 0 / 24 | 1.146e-13 | -9.166e-13 | 12,843 | 42,319 | 3.435e+08 | -2,673 | -26,404 | 0.864 |
| 2.25 | 1.01 | 0 / 24 | 1 | -1 | 15.32 | 12,675 | 3.529e+07 | -103.3 | -11,923 | 0.864 |
| 2.25 | 1.1 | 0 / 24 | 1 | -1 | 252.8 | 12,121 | 3.367e+07 | -74.14 | -12,994 | 0.864 |
| 2.25 | 1.5 | 0 / 24 | 1 | -1 | 4,042 | 13,572 | 3.863e+07 | -612.1 | -18,311 | 0.864 |
| 2.25 | 2 | 0 / 24 | 0.5 | -1 | 12,424 | 41,239 | 3.260e+08 | -2,638 | -26,237 | 0.864 |


## Boundary and margin examples

This table tracks representative matched and overmatched lapse choices.

| lambda | V | min margin | max gtt | max theta product | max abs R | max Kretschmann | min Gkm |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.05 | 1.01 | 0.08 | -0.3296 | 29.86 | 8,278 | 1.461e+07 | -12,357 |
| 1.1 | 1.1 | 1.861e-13 | -8.184e-13 | 484.3 | 7,784 | 1.372e+07 | -13,446 |
| 1.5 | 1.5 | 1.665e-13 | -1.001e-12 | 4,874 | 15,912 | 4.981e+07 | -18,694 |
| 2 | 2 | 1.146e-13 | -9.166e-13 | 12,843 | 42,319 | 3.435e+08 | -26,404 |
| 2.25 | 2 | 0.5 | -1 | 12,424 | 41,239 | 3.260e+08 | -26,237 |


The matched cases sit on the branch boundary. The overmatched case `(lambda, V) = (2.25, 2.0)` gives a finite margin of `0.5` while keeping the same high-speed target.

## Interpretation

### Lapse margin extends the moving-shell family

The previous `T = A` family placed the transition at `V = 1`. The `T = lambda A` interior scaling moves the transition to:

```math
V=\lambda
```

Within this reduced evaluation, the moving compact-capacity shell reaches the sampled superluminal speeds when the lapse margin meets or exceeds the target speed.

### Causal margin and geometric concentration are separate design quantities

The `lambda` multiplier gives direct control over the `gtt` branch. The curvature, null-expansion, and Einstein-projection quantities continue to track the moving compact wall.

The largest geometric values occur where high `C0`, narrow `Delta`, and high `V` combine. This follows the ansatz structure: capacity concentration enters through the compact wall, and motion adds the shift-driven contribution during throat overlap.

### The equality surface is a useful calibration point

The cases with `lambda = V` sit at the boundary. They are useful for confirming the analytic relation and for calibrating numerical sensitivity near the transition.

A design scan with working margin uses:

```math
\lambda > V
```

The `(lambda, V) = (2.25, 2.0)` block gives the cleanest margin example in this run.

### Lapse margin also adds wall structure

The compact-supported form is:

```math
T=A\lambda^S
```

Therefore:

```math
\nabla\ln T
=
\nabla\ln A
+
(\ln\lambda)\nabla S
```

The same compact wall carries the capacity gradient and the lapse-margin gradient. Increasing `lambda` gives causal room and increases the lapse participation in the wall layer.

### Practical physical implication

This branch describes a moving shell that carries both spatial capacity and time-rate margin. It can be tuned through the sampled superluminal range by increasing `lambda` with `V`.

The engineering load remains concentrated in the moving wall. This makes the branch a useful benchmark before shifting capacity and lapse support toward the wormhole throat structure.

## Standing result from this pass

The `T = lambda A` scan establishes a clean relation between target speed and lapse margin:

```math
\lambda \ge |V|
```

For the sampled grid, all `lambda >= V` pairs remain on the causal-margin branch. The largest curvature and null-expansion values remain associated with high capacity, narrow walls, and high speed. The result supports the current interpretation: lapse margin handles the causal-balance condition, while wall shaping and eventual throat-load transfer address the geometric concentration.

## Files generated by this evaluation

- `ansatz_lambda_lapse_scan.py`
- `ansatz_lambda_A_results.json`
- `ansatz_lambda_A_summary.json`

## Reproducibility appendix

```python
import math, json
import numpy as np
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp

# Reduced radial/spherical ADM ansatz with compactly supported lapse multiplier.
# Coordinates: x=(t,l,theta,phi). Phi=0. r(l)=sqrt(r0^2+l^2).
# A = exp(S log C0)
# T = exp(S log(lambda*C0)) = A * lambda^S
# Thus outside support T=1; inside passenger region T=lambda*A.

def make_params(C0=10.0, Delta=0.3, Rmid=0.5, r0=1.0, V=0.0, L0=0.0, lapse_lambda=1.0, eps=1e-5):
    return jnp.array([float(C0), float(Delta), float(Rmid), float(r0), float(V), float(L0), float(lapse_lambda), float(eps), float(Delta/6.0)], dtype=jnp.float64)

def scalars(x,p):
    C0,Delta,Rmid,r0,V,L0,lapse_lambda,eps,w=p
    t,l,th,ph=x
    L=L0+V*t
    rho=jnp.sqrt((l-L)**2+eps**2)
    z=(((l-L)**2) - Rmid**2)/(2.0*Rmid*w)
    S=0.5*(1.0-jnp.tanh(z))
    A=jnp.exp(S*jnp.log(C0))
    T=jnp.exp(S*jnp.log(lapse_lambda*C0))
    r=jnp.sqrt(r0**2+l**2)
    return S,A,T,r,rho

def metric(x,p):
    S,A,T,r,rho=scalars(x,p)
    V=p[4]; th=x[2]
    return jnp.array([
        [-T*T + A*A*V*V*S*S, -A*A*V*S, 0.0, 0.0],
        [-A*A*V*S, A*A, 0.0, 0.0],
        [0.0, 0.0, A*A*r*r, 0.0],
        [0.0, 0.0, 0.0, A*A*r*r*jnp.sin(th)**2],
    ], dtype=jnp.float64)

def gamma_conn(x,p):
    g=metric(x,p)
    dg=jax.jacfwd(metric, argnums=0)(x,p)
    ginv=jnp.linalg.inv(g)
    Gamma=(jnp.einsum('ad,cdb->abc',ginv,dg)+
           jnp.einsum('ad,bdc->abc',ginv,dg)-
           jnp.einsum('ad,bcd->abc',ginv,dg))*0.5
    return Gamma

def R_eff(x,p):
    S,A,T,r,rho=scalars(x,p)
    return A*r

def curvature_raw(x,p):
    g=metric(x,p)
    ginv=jnp.linalg.inv(g)
    Gam=gamma_conn(x,p)
    dGam=jax.jacfwd(gamma_conn, argnums=0)(x,p)
    deriv=jnp.transpose(dGam,(0,2,3,1))-jnp.transpose(dGam,(0,2,1,3))
    prod1=jnp.einsum('ame,ens->asmn',Gam,Gam)
    prod2=jnp.einsum('ane,ems->asmn',Gam,Gam)
    Riem=deriv+prod1-prod2
    Ric=jnp.einsum('asan->sn', Riem)
    Rsc=jnp.einsum('ab,ab->', ginv, Ric)
    G=Ric-0.5*g*Rsc
    Rdown=jnp.einsum('pa,asmn->psmn',g,Riem)
    Ricci2=jnp.einsum('ab,cd,ac,bd->',Ric,Ric,ginv,ginv)
    Kretsch=jnp.einsum('abcd,efgh,ae,bf,cg,dh->',Rdown,Rdown,ginv,ginv,ginv,ginv)
    S,A,T,r,rho=scalars(x,p)
    V=p[4]
    nvec=jnp.array([1.0/T, V*S/T, 0.0, 0.0])
    kp=jnp.array([1.0/T, V*S/T + 1.0/A, 0.0, 0.0])
    km=jnp.array([1.0/T, V*S/T - 1.0/A, 0.0, 0.0])
    Gnn=jnp.einsum('a,b,ab->',nvec,nvec,G)
    Gkp=jnp.einsum('a,b,ab->',kp,kp,G)
    Gkm=jnp.einsum('a,b,ab->',km,km,G)
    dR=jax.grad(R_eff, argnums=0)(x,p)
    beta=-V*S
    theta_p=2/(A*r)*(((dR[0]-beta*dR[1])/T)+(1/A)*dR[1])
    theta_m=2/(A*r)*(((dR[0]-beta*dR[1])/T)-(1/A)*dR[1])
    det=jnp.linalg.det(g)
    gtt=g[0,0]
    return jnp.array([Rsc,Ricci2,Kretsch,Gnn,Gkp,Gkm,gtt,det,theta_p,theta_m,S,A,T,r,rho], dtype=jnp.float64)

curvature_one=jax.jit(curvature_raw)
curvature_grid=jax.jit(jax.vmap(curvature_raw, in_axes=(0,None)))
names=['R','Ricci2','Kretsch','Gnn','Gkp','Gkm','gtt','det','theta_p','theta_m','S','A','T','r','rho']

def scan_case(p, lmin=-1.5,lmax=1.5,N=161):
    ls=np.linspace(lmin,lmax,N)
    xs=jnp.array([[0.0,float(l),math.pi/2,0.0] for l in ls], dtype=jnp.float64)
    arr=np.array(curvature_grid(xs,p))
    summary={}
    for i,key in enumerate(names[:10]):
        a=arr[:,i]
        idx=int(np.nanargmax(np.abs(a)))
        summary['maxabs_'+key]=float(np.nanmax(np.abs(a)))
        summary['l_at_maxabs_'+key]=float(ls[idx])
        summary['min_'+key]=float(np.nanmin(a))
        summary['max_'+key]=float(np.nanmax(a))
    summary['min_det']=float(np.nanmin(arr[:,7]))
    summary['max_det']=float(np.nanmax(arr[:,7]))
    summary['max_A']=float(np.nanmax(arr[:,11]))
    summary['max_T']=float(np.nanmax(arr[:,12]))
    summary['min_gtt']=float(np.nanmin(arr[:,6]))
    summary['max_gtt']=float(np.nanmax(arr[:,6]))
    margin = arr[:,12] - arr[:,11]*abs(float(p[4]))*arr[:,10]
    summary['min_lapse_shift_margin']=float(np.nanmin(margin))
    summary['l_at_min_lapse_shift_margin']=float(ls[int(np.nanargmin(margin))])
    lfine=np.linspace(lmin,lmax,2001)
    xs2=jnp.array([[0.0,float(l),math.pi/2,0.0] for l in lfine], dtype=jnp.float64)
    Reff=np.array(jax.vmap(R_eff, in_axes=(0,None))(xs2,p))
    summary['throat_l_min_Reff']=float(lfine[int(np.argmin(Reff))])
    summary['throat_min_Reff']=float(np.min(Reff))
    prod=arr[:,8]*arr[:,9]
    summary['theta_product_min']=float(np.nanmin(prod))
    summary['theta_product_max']=float(np.nanmax(prod))
    return summary

def aggregate(cases):
    summary=[]
    keys=sorted(set((c['lapse_lambda'], c['V']) for c in cases))
    for lam,V in keys:
        group=[c for c in cases if c['lapse_lambda']==lam and c['V']==V]
        summary.append({
            'lapse_lambda': lam,
            'V': V,
            'cases': len(group),
            'cases_with_gtt_positive': sum(1 for c in group if c['max_gtt'] > 1e-9),
            'cases_with_margin_negative': sum(1 for c in group if c['min_lapse_shift_margin'] < -1e-9),
            'min_lapse_shift_margin': min(c['min_lapse_shift_margin'] for c in group),
            'max_gtt': max(c['max_gtt'] for c in group),
            'max_theta_product': max(c['theta_product_max'] for c in group),
            'max_abs_R': max(c['maxabs_R'] for c in group),
            'max_Kretsch': max(c['maxabs_Kretsch'] for c in group),
            'min_Gkp': min(c['min_Gkp'] for c in group),
            'min_Gkm': min(c['min_Gkm'] for c in group),
            'max_abs_throat_shift': max(abs(c['throat_l_min_Reff']) for c in group),
        })
    return summary

def run_sweep(out_results='/mnt/data/ansatz_lambda_A_results.json', out_summary='/mnt/data/ansatz_lambda_A_summary.json'):
    lambdas=[1.05,1.1,1.5,2.0,2.25]
    velocities=[1.01,1.1,1.5,2.0]
    # warm compile
    p=make_params(lapse_lambda=1.1,V=1.01)
    _=curvature_one(jnp.array([0.0,0.0,math.pi/2,0.0], dtype=jnp.float64), p)
    cases=[]
    for lam in lambdas:
      for C0 in [2,10,100,1e4]:
        for Delta in [1.0,0.3,0.1]:
          for V in velocities:
            for L0 in [0.0,0.5]:
              p=make_params(C0=C0,Delta=Delta,Rmid=0.5,r0=1.0,V=V,L0=L0,lapse_lambda=lam)
              s=scan_case(p,N=161)
              s.update(C0=float(C0),Delta=float(Delta),V=float(V),L0=float(L0),Rmid=0.5,r0=1.0,lapse_lambda=float(lam))
              cases.append(s)
              print(json.dumps({k:s[k] for k in ['lapse_lambda','C0','Delta','V','L0','maxabs_R','maxabs_Kretsch','min_Gkp','min_Gkm','max_gtt','min_lapse_shift_margin','theta_product_max','throat_l_min_Reff']}))
    summary=aggregate(cases)
    with open(out_results,'w') as f:
        json.dump(cases,f,indent=2)
    with open(out_summary,'w') as f:
        json.dump(summary,f,indent=2)
    return cases, summary

if __name__=='__main__':
    cases, summary = run_sweep()
    print('\nSUMMARY')
    for row in summary:
        print(json.dumps(row))

```
