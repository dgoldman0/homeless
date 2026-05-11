# Capacity-Coupled Lapse Evaluation: `T = A`

## Purpose

This report evaluates the capacity-coupled lapse choice

```math
T=A
```

inside the reduced radial/spherical ansatz. The evaluation folds the subluminal, near-luminal, and first superluminal velocity probes into one scan.

The reduced metric is

```math
ds^2=-T^2dt^2+A^2(dl-VSdt)^2+A^2r^2(l)d\Omega^2.
```

The tested lapse choice gives

```math
T=A,
```

so the reduced `tt` component becomes

```math
g_{tt}=A^2(-1+V^2S^2).
```

The causal-balance threshold is therefore organized by

```math
|V|S=1.
```

Since the passenger region has `S` close to one, the reduced family places the transition at `V = 1`.

## Model

The scan uses the same reduced model as the first-pass harness:

```math
r(l)=\sqrt{1+l^2}, \qquad r_0=1, \qquad \Phi=0.
```

The shell profile is a smooth tanh wall proxy centered around `Rmid = 0.5`. The capacity factor is

```math
A=\exp(S\ln C_0).
```

The lapse is

```math
T=A.
```

The scan evaluates the `t = 0` radial slice with shell-center placements

```math
L_0\in\{0,0.5\}.
```

The parameter grid is

```math
C_0\in\{2,10,100,10^4\},
```

```math
\Delta\in\{1.0,0.3,0.1\},
```

```math
V\in\{0,0.1,0.5,0.9,0.95,0.99,1.01,1.1\}.
```

Total cases:

```math
4\times3\times8\times2=192.
```

## Diagnostics

The evaluation records these quantities on the radial grid:

```math
R, \qquad R_{\mu\nu}R^{\mu\nu}, \qquad R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}.
```

Einstein-tensor projections are evaluated along the ADM normal and radial null directions:

```math
G_{\mu\nu}n^\mu n^\nu,
\qquad
G_{\mu\nu}k_+^\mu k_+^\nu,
\qquad
G_{\mu\nu}k_-^\mu k_-^\nu.
```

The causal-balance diagnostic is

```math
M=T-A|V|S.
```

For `T = A`, this reduces to

```math
M=A(1-|V|S).
```

The radial null-expansion product is recorded as

```math
\theta_+\theta_-.
```

The effective areal radius is

```math
\mathcal R=A r.
```

The throat tracker records the minimum of `A r` on the sampled radial slice.

## Aggregate velocity results

| `V` | cases | cases with `max gtt > 0` | cases with `M <= 0` | max `gtt` | min `M` | max `theta+theta-` | max `abs(R)` | max Kretschmann |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 24 | 0 | 0 | -1 | 1 | 0 | 20,993.3 | 85,144,910 |
| 0.1 | 24 | 0 | 0 | -1 | 1 | 0.009266 | 20,818.5 | 83,741,336 |
| 0.5 | 24 | 0 | 0 | -1 | 1 | 0.318809 | 16,966.8 | 53,580,377 |
| 0.9 | 24 | 0 | 0 | -0.76 | 0.2 | 3.947804 | 9,431.47 | 16,115,246 |
| 0.95 | 24 | 0 | 0 | -0.39 | 0.1 | 6.588129 | 8,766.30 | 14,947,587 |
| 0.99 | 24 | 0 | 0 | -0.0796 | 0.02 | 13.411088 | 8,208.27 | 14,036,739 |
| 1.01 | 24 | 16 | 16 | 2,010,000 | -100 | 32.837952 | 7,983.14 | 13,591,720 |
| 1.1 | 24 | 24 | 24 | 21,000,000 | -1000 | 523.708479 | 7,366.43 | 11,706,289 |

## Causal-balance result

The `T = A` family gives a clean subluminal branch in this reduced pass. Across all sampled cases with

```math
V<1,
```

there are `0` cases with positive `max gtt` and `0` cases with nonpositive margin `M`.

The near-luminal values show the expected narrowing of margin:

| `V` | minimum sampled margin `M` |
|---:|---:|
| 0.9 | 0.2 |
| 0.95 | 0.1 |
| 0.99 | 0.02 |

The first superluminal probes move into the above-threshold branch:

| `V` | cases with `max gtt > 0` | cases with `M <= 0` |
|---:|---:|---:|
| 1.01 | 16 / 24 | 16 / 24 |
| 1.1 | 24 / 24 | 24 / 24 |

This is the direct signature of the analytic condition

```math
|V|S=1.
```

The result identifies `T = A` as a capacity-coupled subluminal crossing family. The superluminal branch calls for an additional lapse amplitude or exponent.

## Null-expansion result

The null-expansion product remains small through ordinary subluminal speeds and grows toward the threshold:

| `V` | max `theta+theta-` |
|---:|---:|
| 0.1 | 0.009266 |
| 0.5 | 0.318809 |
| 0.9 | 3.947804 |
| 0.95 | 6.588129 |
| 0.99 | 13.411088 |
| 1.01 | 32.837952 |
| 1.1 | 523.708479 |

The expansion diagnostic tracks the same near-unity transition as `gtt` and the lapse-shift margin. The highest-resolution interval for the next analytic sampling is

```math
0.99\leq V\leq1.01.
```

## Curvature result

Curvature remains organized by wall thickness and capacity factor. The largest scalar-curvature and Kretschmann values occur in the narrow-wall, high-capacity cases.

By wall thickness:

| `Delta` | cases | max `abs(R)` | max Kretschmann | max `theta+theta-` |
|---:|---:|---:|---:|---:|
| 1.0 | 64 | 365.964 | 24,890.9 | 19.5944 |
| 0.3 | 64 | 2,817.10 | 1,419,143 | 91.0484 |
| 0.1 | 64 | 20,993.3 | 85,144,910 | 523.708 |

By capacity factor:

| `C0` | cases | max `abs(R)` | max Kretschmann | max `theta+theta-` |
|---:|---:|---:|---:|---:|
| 2 | 48 | 5,196.70 | 7,483,222 | 16.7548 |
| 10 | 48 | 12,876.4 | 30,941,538 | 85.6524 |
| 100 | 48 | 18,159.9 | 61,787,778 | 224.498 |
| 10,000 | 48 | 20,993.3 | 85,144,910 | 523.708 |

The leading curvature implication is unchanged by the lapse refinement: compact capacity concentration lives in the wall. The `T = A` choice improves the causal-balance structure while leaving wall scaling as the main invariant curvature driver.

## Einstein projection result

The radial null projections keep the expected wall concentration. The two radial null families separate as velocity increases, with the `k_-` family carrying the larger sampled magnitude near and above the threshold.

| `V` | min `G(k+,k+)` | min `G(k-,k-)` | max `abs(G(n,n))` |
|---:|---:|---:|---:|
| 0 | -3,129.43 | -3,129.43 | 5,934.36 |
| 0.1 | -2,546.47 | -3,772.46 | 5,907.41 |
| 0.5 | -815.427 | -6,945.40 | 5,260.45 |
| 0.9 | -98.2000 | -11,079.6 | 3,750.87 |
| 0.95 | -82.8891 | -11,664.0 | 3,501.52 |
| 0.99 | -73.7486 | -12,142.3 | 3,292.33 |
| 1.01 | -69.5016 | -12,385.0 | 3,203.27 |
| 1.1 | -53.0573 | -13,507.2 | 3,010.38 |

This projection split gives a useful direction-sensitive diagnostic for the next family. The `k_-` branch is the sharper null-projection monitor as `V` approaches and crosses unity.

## Throat tracking

The slice-local effective throat tracker records the minimum of

```math
\mathcal R=A r.
```

Across the full grid, the sampled minimum location ranges from

```math
-0.864\leq l_{\min(Ar)}\leq0.651.
```

The range is governed by the capacity-wall placement and shell-center offset on the sampled slice. Since the current scan evaluates `t = 0`, a crossing-time sweep over `L(t)` is the natural companion diagnostic.

## Dominant cases

Largest scalar curvature:

| `C0` | `Delta` | `V` | `L0` | max `abs(R)` | max Kretschmann | location of max `abs(R)` |
|---:|---:|---:|---:|---:|---:|---:|
| 10,000 | 0.1 | 0 | 0 | 20,993.3 | 85,144,910 | 0.525 |
| 10,000 | 0.1 | 0.1 | 0 | 20,818.5 | 83,741,336 | 0.525 |
| 10,000 | 0.1 | 0 | 0.5 | 20,651.2 | 71,111,271 | -0.01875 |
| 10,000 | 0.1 | 0.1 | 0.5 | 20,503.9 | 70,101,333 | -0.01875 |
| 100 | 0.1 | 0 | 0.5 | 18,159.9 | 61,787,778 | -0.01875 |

Largest null-expansion product:

| `C0` | `Delta` | `V` | `L0` | max `theta+theta-` | max `gtt` | min `M` |
|---:|---:|---:|---:|---:|---:|---:|
| 10,000 | 0.1 | 1.1 | 0 | 523.708 | 21,000,000 | -1000 |
| 10,000 | 0.1 | 1.1 | 0.5 | 310.614 | 21,000,000 | -1000 |
| 100 | 0.1 | 1.1 | 0 | 224.498 | 2100 | -10 |
| 100 | 0.1 | 1.1 | 0.5 | 113.140 | 2100 | -10 |
| 10,000 | 0.3 | 1.1 | 0.5 | 91.0484 | 20,971,424 | -999.081 |

The curvature and expansion extrema separate cleanly. Curvature peaks are driven by narrow, high-capacity walls. Expansion peaks are driven by the above-threshold velocity branch with narrow walls and high capacity.

## Design implications

1. `T = A` is the clean subluminal lapse refinement for the reduced ansatz.
2. The causal-balance threshold is transparent and parameter-independent in sign: `|V|S = 1`.
3. The first superluminal probes identify the next lapse family:

```math
T=\lambda A, \qquad \lambda>|V|,
```

or

```math
T=A^p, \qquad p>1.
```

4. Wall-localized curvature remains the main capacity diagnostic. The next comparison should measure how `lambda` or `p` changes the wall curvature and null-projection profiles.
5. The near-unity velocity interval deserves finer sampling because `gtt`, margin, and expansion diagnostics all organize around the same threshold.

## Reproducibility code

```python
import math, json
import numpy as np
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp


def make_params(C0=10.0, Delta=0.3, Rmid=0.5, r0=1.0,
                V=0.0, L0=0.0, lapse_power=1.0, eps=1e-5):
    return jnp.array([
        float(C0), float(Delta), float(Rmid), float(r0), float(V),
        float(L0), float(lapse_power), float(eps), float(Delta / 6.0)
    ], dtype=jnp.float64)


def scalars(x, p):
    C0, Delta, Rmid, r0, V, L0, lapse_power, eps, w = p
    t, l, th, ph = x
    L = L0 + V * t
    rho = jnp.sqrt((l - L) ** 2 + eps ** 2)
    z = (((l - L) ** 2) - Rmid ** 2) / (2.0 * Rmid * w)
    S = 0.5 * (1.0 - jnp.tanh(z))
    A = jnp.exp(S * jnp.log(C0))
    T = A ** lapse_power
    r = jnp.sqrt(r0 ** 2 + l ** 2)
    return S, A, T, r, rho


def metric(x, p):
    S, A, T, r, rho = scalars(x, p)
    V = p[4]
    th = x[2]
    return jnp.array([
        [-T * T + A * A * V * V * S * S, -A * A * V * S, 0.0, 0.0],
        [-A * A * V * S, A * A, 0.0, 0.0],
        [0.0, 0.0, A * A * r * r, 0.0],
        [0.0, 0.0, 0.0, A * A * r * r * jnp.sin(th) ** 2],
    ], dtype=jnp.float64)


def gamma_conn(x, p):
    g = metric(x, p)
    dg = jax.jacfwd(metric, argnums=0)(x, p)
    ginv = jnp.linalg.inv(g)
    Gamma = (
        jnp.einsum('ad,cdb->abc', ginv, dg)
        + jnp.einsum('ad,bdc->abc', ginv, dg)
        - jnp.einsum('ad,bcd->abc', ginv, dg)
    ) * 0.5
    return Gamma


def R_eff(x, p):
    S, A, T, r, rho = scalars(x, p)
    return A * r


def curvature_raw(x, p):
    g = metric(x, p)
    ginv = jnp.linalg.inv(g)
    Gam = gamma_conn(x, p)
    dGam = jax.jacfwd(gamma_conn, argnums=0)(x, p)
    deriv = jnp.transpose(dGam, (0, 2, 3, 1)) - jnp.transpose(dGam, (0, 2, 1, 3))
    prod1 = jnp.einsum('ame,ens->asmn', Gam, Gam)
    prod2 = jnp.einsum('ane,ems->asmn', Gam, Gam)
    Riem = deriv + prod1 - prod2
    Ric = jnp.einsum('asan->sn', Riem)
    Rsc = jnp.einsum('ab,ab->', ginv, Ric)
    G = Ric - 0.5 * g * Rsc
    Rdown = jnp.einsum('pa,asmn->psmn', g, Riem)
    Ricci2 = jnp.einsum('ab,cd,ac,bd->', Ric, Ric, ginv, ginv)
    Kretsch = jnp.einsum('abcd,efgh,ae,bf,cg,dh->', Rdown, Rdown, ginv, ginv, ginv, ginv)

    S, A, T, r, rho = scalars(x, p)
    V = p[4]
    nvec = jnp.array([1.0 / T, V * S / T, 0.0, 0.0])
    kp = jnp.array([1.0 / T, V * S / T + 1.0 / A, 0.0, 0.0])
    km = jnp.array([1.0 / T, V * S / T - 1.0 / A, 0.0, 0.0])
    Gnn = jnp.einsum('a,b,ab->', nvec, nvec, G)
    Gkp = jnp.einsum('a,b,ab->', kp, kp, G)
    Gkm = jnp.einsum('a,b,ab->', km, km, G)

    dR = jax.grad(R_eff, argnums=0)(x, p)
    beta = -V * S
    theta_p = 2 / (A * r) * (((dR[0] - beta * dR[1]) / T) + (1 / A) * dR[1])
    theta_m = 2 / (A * r) * (((dR[0] - beta * dR[1]) / T) - (1 / A) * dR[1])
    det = jnp.linalg.det(g)
    gtt = g[0, 0]
    return jnp.array([
        Rsc, Ricci2, Kretsch, Gnn, Gkp, Gkm, gtt, det,
        theta_p, theta_m, S, A, T, r, rho
    ], dtype=jnp.float64)


curvature_one = jax.jit(curvature_raw)
curvature_grid = jax.jit(jax.vmap(curvature_raw, in_axes=(0, None)))
names = ['R', 'Ricci2', 'Kretsch', 'Gnn', 'Gkp', 'Gkm', 'gtt', 'det', 'theta_p', 'theta_m', 'S', 'A', 'T', 'r', 'rho']


def scan_case(p, lmin=-1.5, lmax=1.5, N=161):
    ls = np.linspace(lmin, lmax, N)
    xs = jnp.array([[0.0, float(l), math.pi / 2, 0.0] for l in ls], dtype=jnp.float64)
    arr = np.array(curvature_grid(xs, p))
    summary = {}
    for i, key in enumerate(names[:10]):
        a = arr[:, i]
        idx = int(np.nanargmax(np.abs(a)))
        summary['maxabs_' + key] = float(np.nanmax(np.abs(a)))
        summary['l_at_maxabs_' + key] = float(ls[idx])
        summary['min_' + key] = float(np.nanmin(a))
        summary['max_' + key] = float(np.nanmax(a))
    margin = arr[:, 12] - arr[:, 11] * abs(float(p[4])) * arr[:, 10]
    summary['min_lapse_shift_margin'] = float(np.nanmin(margin))
    summary['l_at_min_lapse_shift_margin'] = float(ls[int(np.nanargmin(margin))])
    lfine = np.linspace(lmin, lmax, 2001)
    xs2 = jnp.array([[0.0, float(l), math.pi / 2, 0.0] for l in lfine], dtype=jnp.float64)
    Reff = np.array(jax.vmap(R_eff, in_axes=(0, None))(xs2, p))
    summary['throat_l_min_Reff'] = float(lfine[int(np.argmin(Reff))])
    summary['throat_min_Reff'] = float(np.min(Reff))
    prod = arr[:, 8] * arr[:, 9]
    summary['theta_product_min'] = float(np.nanmin(prod))
    summary['theta_product_max'] = float(np.nanmax(prod))
    summary['max_A'] = float(np.nanmax(arr[:, 11]))
    summary['max_T'] = float(np.nanmax(arr[:, 12]))
    return summary


def run_sweep(outpath='/mnt/data/ansatz_T_equals_A_results.json'):
    lapse_power = 1.0
    p = make_params(lapse_power=lapse_power)
    curvature_one(jnp.array([0.0, 0.0, math.pi / 2, 0.0], dtype=jnp.float64), p)
    cases = []
    for C0 in [2, 10, 100, 1e4]:
        for Delta in [1.0, 0.3, 0.1]:
            for V in [0.0, 0.1, 0.5, 0.9, 0.95, 0.99, 1.01, 1.1]:
                for L0 in [0.0, 0.5]:
                    p = make_params(C0=C0, Delta=Delta, Rmid=0.5, r0=1.0, V=V, L0=L0, lapse_power=lapse_power)
                    s = scan_case(p, N=161)
                    s.update(C0=float(C0), Delta=float(Delta), V=float(V), L0=float(L0), Rmid=0.5, r0=1.0, lapse_power=1.0)
                    cases.append(s)
    with open(outpath, 'w') as f:
        json.dump(cases, f, indent=2)
    return cases


if __name__ == '__main__':
    run_sweep()
```
