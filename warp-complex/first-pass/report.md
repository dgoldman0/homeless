# First-Pass Diagnostic Report: Compact-Capacity Warp Shell Through a Wormhole Throat

Display equations are written in fenced `math` blocks for stable GitHub rendering.

## Purpose

This report records the first reduced diagnostic pass for the compact warp-shell / wormhole-throat ansatz. The goal is to identify invariant scaling behavior, throat response, causal-surface pressure, and null-expansion behavior before committing to a high-cost numerical evolution.

The test focuses on the shell-throat overlap because that is where the capacity gradient, radial shift, and throat flare-out occupy the same finite region.

## Reduced model tested

The reduced radial/spherical metric used in the scan was:

```math
ds^2 = -dt^2 + A^2(l,t)\left(dl - V S(l,t)dt\right)^2 + A^2(l,t)r^2(l)d\Omega^2
```

with:

```math
r(l)=\sqrt{1+l^2}
```

```math
A(l,t)=\exp\left(S(l,t)\log C_0\right)
```

The first pass set:

```math
\Phi(l)=0
```

```math
T(\rho)=1
```

```math
r_0=1
```

The shell profile was represented by a smooth tanh transition in squared radial distance. This gives a smooth computational proxy for the wall and avoids an artificial cusp at the shell center. The profile is not treated as the final compact-support profile; it is a diagnostic stand-in for scaling behavior.

## Quantities evaluated

The scan evaluated the following local diagnostics along a radial line through the throat:

```math
R
```

```math
R_{\mu\nu}R^{\mu\nu}
```

```math
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
```

```math
G_{\mu\nu}n^\mu n^\nu
```

```math
G_{\mu\nu}k_+^\mu k_+^\nu
```

```math
G_{\mu\nu}k_-^\mu k_-^\nu
```

```math
g_{tt}
```

```math
\det g
```

```math
\theta_+\theta_-
```

The effective areal radius used for throat tracking was:

```math
\mathcal R(l,t)=A(l,t)r(l)
```

The sampled throat location is the grid minimum of `R_eff = A r` over the radial scan interval.

## Parameter grid

The scan used:

```math
C_0 \in \{2,10,100,10^4\}
```

```math
\Delta \in \{1.0,0.3,0.1\}
```

```math
V \in \{0,0.1,0.5\}
```

```math
L_0 \in \{0,0.5\}
```

with `Rmid = 0.5` and `r0 = 1.0`.

## Primary finding

The reduced ansatz remains finite for the tested finite parameter values and keeps a Lorentzian determinant throughout the radial samples. The shell wall carries the dominant geometric cost. The cost increases strongly as the wall narrows and increases moderately to strongly with the capacity factor.

The moving high-capacity cases identify the key causal condition:

```math
g_{tt}=-1+A^2V^2S^2
```

The balance threshold is:

```math
A V S = 1
```

Inside the high-capacity region where `A` approaches `C0` and `S` approaches `1`, the practical threshold is:

```math
V \approx C_0^{-1}
```

This is the dominant design constraint found by the first pass.

## Static capacity wall results

These rows use `V = 0` and `L0 = 0.5`, placing the wall near the throat while removing shift-driven terms.

| C0 | Delta | max abs R | max Kretschmann | min radial null Gkk | effective throat l | max theta plus theta minus |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1.0 | 41.96 | 867.9 | -20.83 | -0.2595 | -0.0016 |
| 2 | 0.3 | 347.9 | 56,282.3 | -167.5 | -0.1245 | -4.143e-06 |
| 2 | 0.1 | 1,593.3 | 1.233e+06 | -785.0 | -0.0585 | -0.0084 |
| 10 | 1.0 | 104.0 | 4,358.7 | -46.38 | -0.3180 | -2.018e-05 |
| 10 | 0.3 | 892.7 | 3.156e+05 | -388.9 | -0.1470 | -4.547e-04 |
| 10 | 0.1 | 4,759.0 | 1.026e+07 | -2,258.5 | -0.0660 | -4.287e-04 |
| 100 | 1.0 | 153.0 | 8,789.1 | -65.06 | -0.3510 | -7.426e-07 |
| 100 | 0.3 | 1,221.5 | 5.210e+05 | -469.9 | -0.1590 | -6.076e-06 |
| 100 | 0.1 | 8,164.8 | 2.779e+07 | -3,684.6 | -0.0705 | -4.669e-06 |
| 1e4 | 1.0 | 200.7 | 14,880.5 | -84.00 | -0.3840 | -8.097e-10 |
| 1e4 | 0.3 | 1,491.9 | 8.437e+05 | -627.6 | -0.1710 | -6.112e-10 |
| 1e4 | 0.1 | 11,936.2 | 5.265e+07 | -4,906.1 | -0.0750 | -5.482e-10 |

### Interpretation

The static capacity deformation is finite in the tested range. The curvature concentration is wall-localized and grows rapidly as `Delta` is reduced.

The throat minimum of `A r` shifts smoothly away from the original `l = 0` throat. This confirms that the throat responds to the capacity gradient itself, rather than only to the compact exterior coordinate support.

The static `theta_plus theta_minus` values remain non-positive or very close to zero in this scan. This is a useful baseline: the capacity wall alone shows strong curvature demand while avoiding the clearest trapped-region signature in the reduced static test.

## Wall-thickness scaling

The following table shows the growth in `max abs R` for static `V = 0`, `L0 = 0.5` cases as `Delta` is reduced.

| C0 | Delta 1.0 | Delta 0.3 | Delta 0.1 | ratio 0.1 over 1.0 |
| --- | --- | --- | --- | --- |
| 2 | 41.96 | 347.9 | 1,593.3 | 37.97 |
| 10 | 104.0 | 892.7 | 4,759.0 | 45.74 |
| 100 | 153.0 | 1,221.5 | 8,164.8 | 53.35 |
| 1e4 | 200.7 | 1,491.9 | 11,936.2 | 59.47 |

### Interpretation

Reducing `Delta` from `1.0` to `0.1` increases `max abs R` by roughly `38x` to `59x` across the tested capacities. This is consistent with a dominant wall-gradient effect rather than a passenger-region effect.

The result supports the expected scaling structure:

```math
\nabla\log A \sim \frac{\log C_0}{\Delta}
```

```math
\Delta_q\log A \sim \frac{\log C_0}{\Delta^2}
```

The first-pass implication is constructive: the exterior can remain compact only with a wall that accepts concentrated curvature and stress-energy demand. The wall thickness is therefore a physical control parameter, not just a numerical convenience.

## Moving-shell results at narrow wall thickness

These rows use `Delta = 0.1` and `L0 = 0.5`.

| C0 | V | max g_tt | max theta plus theta minus | min radial null Gkk | max Kretschmann |
| --- | --- | --- | --- | --- | --- |
| 2 | 0.1 | -0.9600 | -0.0082 | -947.0 | 1.210e+06 |
| 2 | 0.5 | -3.166e-13 | 0.1855 | -1,747.2 | 7.278e+05 |
| 10 | 0.1 | -6.172e-13 | 0.0057 | -2,761.5 | 1.002e+07 |
| 10 | 0.5 | 24.00 | 0.2964 | -5,278.9 | 5.199e+06 |
| 100 | 0.1 | 99.00 | 0.0099 | -4,598.2 | 2.691e+07 |
| 100 | 0.5 | 2,499.0 | 4,048.4 | -9,263.7 | 1.146e+07 |
| 1e4 | 0.1 | 1.000e+06 | 735.8 | -6,415.8 | 4.978e+07 |
| 1e4 | 0.5 | 2.500e+07 | 19,125.5 | -14,476.5 | 3.281e+08 |

### Interpretation

The moving cases show the strongest causal pressure. The condition `A V S = 1` appears directly in `g_tt`.

For `C0 = 10`, `V = 0.1` is already near the balance surface. For `C0 = 100`, `V = 0.1` is beyond it. For `C0 = 10000`, even `V = 0.1` produces a very large positive `g_tt` region in the reduced metric.

The positive `theta_plus theta_minus` values in the high-capacity moving cases are the main traversability warning from this first pass. They indicate that the moving high-capacity geometry can generate trapped or marginal-region behavior in the reduced diagnostic model.

## Largest-curvature cases in the scan

| C0 | Delta | V | L0 | max abs R | max Kretschmann | max g_tt | max theta plus theta minus |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1e4 | 0.1 | 0.5 | 0.5 | 43,135.3 | 3.281e+08 | 2.500e+07 | 19,125.5 |
| 1e4 | 0.1 | 0.5 | 0.0 | 43,107.7 | 3.276e+08 | 2.500e+07 | 19,111.7 |
| 1e4 | 0.1 | 0.0 | 0.5 | 11,936.2 | 5.265e+07 | -1.0000 | -5.482e-10 |
| 1e4 | 0.1 | 0.0 | 0.0 | 11,868.7 | 5.218e+07 | -1.0000 | 0 |
| 1e4 | 0.1 | 0.1 | 0.5 | 11,415.7 | 4.978e+07 | 1.000e+06 | 735.8 |

### Interpretation

The largest curvature values occur for high C0, narrow Delta, and nonzero V. This follows the ansatz structure: capacity concentration enters through the compact wall, and motion adds the shift-driven contribution during throat overlap.

## Concerns identified

### 1. Capacity wall cost

The compact-exterior / large-interior mechanism deposits its invariant cost in the wall. The scan shows this through large values of `R`, the Kretschmann scalar, and radial null projections at the wall.

### 2. Causal balance

The initial lapse choice `T = 1` makes the moving high-capacity version tightly constrained by:

```math
V \lesssim C_0^{-1}
```

This condition is too restrictive for the intended large-capacity regime unless the lapse is redesigned.

### 3. Throat displacement

The effective throat moves smoothly under the capacity deformation. This is a useful result because it gives a geometric diagnostic rather than a coordinate claim. It also means the throat sees the capacity gradient.

### 4. Null-expansion pressure

Static capacity cases remain comparatively controlled in the reduced expansion diagnostic. Moving high-capacity cases produce positive `theta_plus theta_minus` values once the lapse-shift balance is stressed.

### 5. Profile dependence still needs a compact-support check

The tanh wall is a smooth proxy. The next pass should use the intended `C^infinity` compact-support shell profile and compare peak values, integrated negative parts, and throat displacement.

## Productive next modification

The next reduced run should test a capacity-coupled lapse:

```math
T=A^p
```

with:

```math
p\in\{0,1/2,1\}
```

The target inequality is:

```math
e^\Phi T > A |V| S
```

In the present reduced model with `Phi = 0`, this becomes:

```math
T > A |V| S
```

The most direct candidate is `T = A`, which changes the causal balance from `A V S = 1` to approximately `V S = 1` in the high-capacity interior. That modification should be tested against the same curvature, null-projection, throat-location, and expansion diagnostics.

## Current verdict

The reduced ansatz earns the next round of first-pass testing. The invariant quantities remain finite for finite sampled parameters, the wall localization is clear, and the throat displacement is smooth in the tested cases.

The first design constraint is also clear: with `T = 1`, large `C0` and finite `V` quickly drive the metric into a causal-balance regime. A capacity-coupled lapse is the highest-value refinement before any full simulation.

## Reproducibility

Companion files generated with this report:

- `ansatz_fast.py`: first-pass JAX diagnostic harness.
- `ansatz_first_pass_results.json`: raw scan output for the 72 parameter cases.

## Code appendix

```python
import math, json, time
import numpy as np
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp

def make_params(C0=10.0, Delta=0.3, Rmid=0.5, r0=1.0, V=0.0, L0=0.0, eps=1e-5):
    return jnp.array([float(C0), float(Delta), float(Rmid), float(r0), float(V), float(L0), float(eps), float(Delta/6.0)], dtype=jnp.float64)

def scalars(x,p):
    C0,Delta,Rmid,r0,V,L0,eps,w=p
    t,l,th,ph=x
    L=L0+V*t
    rho=jnp.sqrt((l-L)**2+eps**2)
    # Use squared radius in the transition to avoid an artificial cusp at the shell center.
    S=0.5*(1.0-jnp.tanh((((l-L)**2) - Rmid**2)/(2.0*Rmid*w)))
    A=jnp.exp(S*jnp.log(C0))
    r=jnp.sqrt(r0**2+l**2)
    return S,A,r,rho

def metric(x,p):
    S,A,r,rho=scalars(x,p)
    V=p[4]; th=x[2]
    return jnp.array([
        [-1.0 + A*A*V*V*S*S, -A*A*V*S, 0.0, 0.0],
        [-A*A*V*S, A*A, 0.0, 0.0],
        [0.0, 0.0, A*A*r*r, 0.0],
        [0.0, 0.0, 0.0, A*A*r*r*jnp.sin(th)**2],
    ], dtype=jnp.float64)

def gamma(x,p):
    g=metric(x,p)
    dg=jax.jacfwd(metric, argnums=0)(x,p)  # dg[b,c,dcoord]
    ginv=jnp.linalg.inv(g)
    Gamma=(jnp.einsum('ad,cdb->abc',ginv,dg)+
           jnp.einsum('ad,bdc->abc',ginv,dg)-
           jnp.einsum('ad,bcd->abc',ginv,dg))*0.5
    return Gamma

def R_eff(x,p):
    S,A,r,rho=scalars(x,p)
    return A*r

def curvature_raw(x,p):
    g=metric(x,p)
    ginv=jnp.linalg.inv(g)
    Gam=gamma(x,p)
    dGam=jax.jacfwd(gamma, argnums=0)(x,p) # [a,b,c,coord]
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
    S,A,r,rho=scalars(x,p)
    V=p[4]
    nvec=jnp.array([1.0,V*S,0.0,0.0])
    kp=jnp.array([1.0,V*S+1.0/A,0.0,0.0])
    km=jnp.array([1.0,V*S-1.0/A,0.0,0.0])
    Gnn=jnp.einsum('a,b,ab->',nvec,nvec,G)
    Gkp=jnp.einsum('a,b,ab->',kp,kp,G)
    Gkm=jnp.einsum('a,b,ab->',km,km,G)
    dR=jax.grad(R_eff, argnums=0)(x,p)
    beta=-V*S
    theta_p=2/(A*r)*((dR[0]-beta*dR[1])+(1/A)*dR[1])
    theta_m=2/(A*r)*((dR[0]-beta*dR[1])-(1/A)*dR[1])
    det=jnp.linalg.det(g)
    gtt=g[0,0]
    return jnp.array([Rsc,Ricci2,Kretsch,Gnn,Gkp,Gkm,gtt,det,theta_p,theta_m,S,A,r,rho], dtype=jnp.float64)

curvature_one=jax.jit(curvature_raw)
curvature_grid=jax.jit(jax.vmap(curvature_raw, in_axes=(0,None)))

names=['R','Ricci2','Kretsch','Gnn','Gkp','Gkm','gtt','det','theta_p','theta_m','S','A','r','rho']

def scan_case(p, lmin=-1.5,lmax=1.5,N=121):
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
    summary['max_A']=float(np.nanmax(arr[:,11]))
    summary['min_gtt']=float(np.nanmin(arr[:,6])); summary['max_gtt']=float(np.nanmax(arr[:,6]))
    # throat scan: use cheap vectorized R_eff
    lfine=np.linspace(lmin,lmax,2001)
    xs2=jnp.array([[0.0,float(l),math.pi/2,0.0] for l in lfine], dtype=jnp.float64)
    Reff=np.array(jax.vmap(R_eff, in_axes=(0,None))(xs2,p))
    summary['throat_l_min_Reff']=float(lfine[int(np.argmin(Reff))])
    summary['throat_min_Reff']=float(np.min(Reff))
    prod=arr[:,8]*arr[:,9]
    summary['theta_product_min']=float(np.nanmin(prod)); summary['theta_product_max']=float(np.nanmax(prod))
    return summary

def main():
    # warm compile
    p=make_params()
    print('warmup')
    print(curvature_one(jnp.array([0.0,0.0,math.pi/2,0.0], dtype=jnp.float64), p))
    cases=[]
    # Focused sweep
    for C0 in [2,10,100,1e4]:
      for Delta in [1.0,0.3,0.1]:
        for V in [0.0,0.1,0.5]:
          for L0 in [0.0,0.5]:
            p=make_params(C0=C0,Delta=Delta,Rmid=0.5,r0=1.0,V=V,L0=L0)
            s=scan_case(p,N=121)
            s.update(C0=float(C0),Delta=float(Delta),V=float(V),L0=float(L0),Rmid=0.5,r0=1.0)
            cases.append(s)
            print(json.dumps({k:s[k] for k in ['C0','Delta','V','L0','maxabs_R','maxabs_Kretsch','min_Gkp','min_Gkm','max_gtt','throat_l_min_Reff','theta_product_max']}))
    with open('/mnt/data/ansatz_first_pass_results.json','w') as f: json.dump(cases,f,indent=2)

if __name__=='__main__':
    main()
```
