# Catch-Rematched Hybrid-Flare-Gated Composite v0.2 Geometry-Burden Refinement

## Executive result

This v0.2 refinement selects a broadened mixed-capacity throat-support geometry for the catch-rematched hybrid-flare-gated composite transit architecture.

The selected geometry is:

```math
\boxed{
C_0=20,
\quad C_\perp=5,
\quad R_{\rm th}=1.25,
\quad w_{\rm th}=0.12,
\quad R_{\rm pass}=0.35,
\quad w_{\rm pass}=0.08,
\quad B_0=6,
\quad w_B=12.
}
```

The selected transition layer is the v01 early-catch service layer:

```math
\boxed{
x_{\rm catch}=0.05,
\quad x_\beta=0.70,
\quad x_q=1.25,
\quad w_{\rm catch}=0.25,
\quad w_\beta=0.28,
\quad w_q=0.30,
\quad p_\beta=4.
}
```

The confirmed v0.2 candidate clears packet and support-edge tests across the evaluated service cases:

```math
(V,\lambda)\in\{(5,5.75),(10,6),(10,11.5)\},
\qquad
X\in\{0.05,0.35,0.70,1.00,1.25\}.
```

Relative to the v01 geometry baseline, the v0.2 candidate gives:

| Quantity | v0.2 relative value |
|---|---:|
| total source-demand proxy $J_{\rm total}$ | 0.162 |
| geometry burden $J_{\rm geom}$ | 0.274 |
| dynamic burden $J_{\rm dyn}$ | 0.0108 |
| packet $\rho_H$ p95 maximum | 0.274 |
| packet ${}^{(3)}R$ p95 maximum | 0.274 |
| packet $K$ p95 maximum | 0.00352 |
| packet $j_M$ p95 maximum | 0.0216 |

The result gives a concrete engineering doctrine:

```math
\boxed{
\text{use minimum useful radial capacity, moderate angular capacity, broadened throat support, and broad moderate }B\text{-stretch.}
}
```

## Design setting

The composite system combines:

1. the hybrid flare-gated v1 wormhole geometry as active throat infrastructure,
2. the catch-rematched throat-loaded packet as the protected service worldtube,
3. the v01 transition layer as the service choreography,
4. the v0.2 mixed-capacity geometry as the spatial burden-reduction layer.

The ADM slice family is written as:

```math
 ds^2=-\alpha^2dt^2
 +\gamma_{ll}\left(dl+\beta^l dt\right)^2
 +\gamma_{\theta\theta}d\theta^2
 +\gamma_{\phi\phi}d\phi^2.
```

The composite fields are:

```math
\alpha=N_{\rm v1}(l,t)\,T_{\rm pkt}(l,X),
```

```math
\gamma_{ll}=B_{\rm v1}(l,t)^2 A_\parallel(l,X)^2,
```

```math
\gamma_{\theta\theta}=R_{\rm v1}(l,t)^2 A_\perp(l,X)^2,
\qquad
\gamma_{\phi\phi}=\gamma_{\theta\theta}\sin^2\theta,
```

```math
\beta^l=-\dot X_{\rm coord}\,E(X)\,W(l)^{p_\beta}S(l-X).
```

The capacity and lapse pair are:

```math
A_\parallel=\exp\!\left(qW\ln C_0\right),
```

```math
A_\perp=\exp\!\left(qW\ln C_\perp\right),
```

```math
T_{\rm pkt}=\exp\!\left(qW\ln(\lambda C_0)\right).
```

The B-aware service velocity is:

```math
\dot X_{\rm coord}=\frac{U}{B_{\rm v1}(X,t)}.
```

This convention treats $U$ as a proper-radial service speed through the stretched throat infrastructure.

## Evaluation method

The confirmation screen computes reduced ADM source-demand proxies on a finite angular grid. The Hamiltonian source-demand proxy is:

```math
\rho_H=rac{{}^{(3)}R+K^2-K_{ij}K^{ij}}{16\pi}.
```

The momentum source-current proxy is:

```math
j_M^i=\frac{D_j\left(K^{ij}-\gamma^{ij}K\right)}{8\pi}.
```

The safety checks are packet timelikeness and support-edge containment:

```math
\max_{\rm packet}\left[-\alpha^2+\gamma_{ll}\left(\dot X_{\rm coord}+\beta^l\right)^2\right]<0,
```

```math
\max_{\rm edge}\left[-\alpha^2+\gamma_{ll}\left(\beta^l\right)^2\right]<0.
```

The scoring functions are:

```math
J_{\rm geom}
=
\max\left(|\rho_H|_{\rm packet,p95},|\rho_H|_{\rm edge,p95}\right)
+0.05\,|{}^{(3)}R|_{\rm packet,p95},
```

```math
J_{\rm dyn}
=|j_M|_{\rm packet,p95}+|j_M|_{\rm edge,p95}+0.02|K|_{\rm packet,p95},
```

```math
J_{\rm total}=J_{\rm geom}+J_{\rm dyn}.
```

The bundle contains the code that computes the fields and reproduces the confirmation tables:

- `code/adm_3p1_viability_v3_baware.py`
- `code/run_v02_confirmation.py`

The compact confirmation data are in:

- `data/narrow_fast_sweep_25x11.csv`
- `data/selected_confirmation_41x17.csv`
- `data/selected_confirmation_41x17_per_slice.csv`
- `data/selected_confirmation_summary.json`

## Confirmation results

### Selected confirmation ranking

| label | clear | $C_0$ | $C_\perp$ | $B_0$ | $w_B$ | max packet norm | max edge $g_{tt}$ | max release packet norm | $J_{\rm total}$ rel. | $J_{\rm geom}$ rel. | $J_{\rm dyn}$ rel. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C20_Cp5_B6_wB12 | true | 20 | 5 | 6 | 12 | -0.7616 | -3.001 | -2.500 | 0.1617 | 0.2742 | 0.0108 |
| C20_Cp4_B6_wB12 | true | 20 | 4 | 6 | 12 | -0.7616 | -3.001 | -2.500 | 0.1665 | 0.2835 | 0.00944 |
| C50_Cp3_B6_wB12 | true | 50 | 3 | 6 | 12 | -0.7637 | -3.710 | -3.091 | 0.1731 | 0.2950 | 0.00956 |
| C35_Cp3_B6_wB12 | true | 35 | 3 | 6 | 12 | -0.7629 | -3.416 | -2.846 | 0.1734 | 0.2961 | 0.00879 |
| C100_Cp5_B4_wB6 | true | 100 | 5 | 4 | 6 | -0.7662 | -4.356 | -3.630 | 0.1740 | 0.2783 | 0.0341 |
| C20_Cp3_B6_wB12 | true | 20 | 3 | 6 | 12 | -0.7616 | -3.001 | -2.500 | 0.1741 | 0.2981 | 0.00776 |
| C20_Cp1_B6_wB12_noangular | true | 20 | 1 | 6 | 12 | -0.7616 | -3.001 | -2.500 | 0.5738 | 1.000 | 0.00208 |
| v01_geometry_baseline | true | 100 | 1 | 8 | 10 | -0.6959 | -128.5 | -3443 | 1.000 | 1.000 | 1.000 |

### Main before/after comparison

| case | packet max norm | edge max $g_{tt}$ | release packet max norm | $J_{\rm total}$ rel. | $J_{\rm geom}$ rel. | $J_{\rm dyn}$ rel. | packet $\rho_H$ rel. | packet ${}^{(3)}R$ rel. | packet $K$ rel. | packet $j_M$ rel. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v01 geometry baseline | -0.6959 | -128.5 | -3443 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| v0.2 candidate | -0.7616 | -3.001 | -2.500 | 0.1617 | 0.2742 | 0.0108 | 0.2739 | 0.2744 | 0.00352 | 0.0216 |

### Angular capacity comparison

| case | $C_\perp$ | $J_{\rm total}$ rel. | $J_{\rm geom}$ rel. | $J_{\rm dyn}$ rel. | packet $\rho_H$ rel. | packet ${}^{(3)}R$ rel. |
|---|---:|---:|---:|---:|---:|---:|
| C20_Cp1_B6_wB12_noangular | 1 | 0.5738 | 1.000 | 0.00208 | 1.000 | 1.000 |
| C20_Cp3_B6_wB12 | 3 | 0.1741 | 0.2981 | 0.00776 | 0.2979 | 0.2982 |
| C20_Cp4_B6_wB12 | 4 | 0.1665 | 0.2835 | 0.00944 | 0.2832 | 0.2836 |
| C20_Cp5_B6_wB12 | 5 | 0.1617 | 0.2742 | 0.0108 | 0.2739 | 0.2744 |

The angular-capacity comparison gives the central v0.2 result:

```math
\boxed{
C_\perp=5\text{ reduces Hamiltonian and spatial-curvature burden while preserving packet and edge clearance.}
}
```

## Engineering implications

### 1. Transition profiles and capacity geometry control different burdens

The refinement sequence gives a two-part design rule:

```math
\boxed{
\text{transition profiles control }j_M\text{ and }K\text{ burden.}
}
```

```math
\boxed{
\text{capacity/support geometry controls }\rho_H\text{ and }{}^{(3)}R\text{ burden.}
}
```

This decomposition turns the combined FTL-service geometry into a subsystem engineering problem. The transition actuator layer sets source-current demand. The spatial support layer sets Hamiltonian and curvature demand.

### 2. Mixed radial/angular capacity is the key v0.2 contribution

The v01-style radial-capacity-only geometry carries higher Hamiltonian/spatial-curvature burden. The v0.2 geometry adds moderate angular capacity and gives a large burden reduction.

The engineering doctrine is:

```math
\boxed{
\text{use mixed radial/angular service capacity rather than a purely radial service geometry.}
}
```

The result identifies $C_\perp\approx5$ as the best confirmed value in the evaluated family. This is the strongest new result because it connects a concrete ADM burden reduction to an anisotropic capacity choice.

### 3. Capacity is an optimized support field

The best confirmed candidate uses $C_0=20$ rather than a larger radial capacity. The design uses enough radial capacity to preserve the packet service layer and uses angular capacity to reduce spatial curvature concentration.

The engineering doctrine is:

```math
\boxed{
\text{select the minimum useful radial capacity and pair it with moderate angular capacity.}
}
```

### 4. Broadened support carries the wall-thickness lesson into the composite system

The v0.2 support envelope uses:

```math
R_{\rm th}=1.25,
\qquad
w_{\rm th}=0.12.
```

This broadens the active support relative to the earlier narrow support. The result agrees with the field expectation that thin walls and sharp gradients are expensive, and it provides the composite-system value range that works with packet and edge clearance.

### 5. Moderate broad radial stretch is the confirmed v0.2 posture

The v0.2 candidate uses:

```math
B_0=6,
\qquad
w_B=12.
```

The radial stretch remains an active infrastructure control. The confirmed posture is moderate in amplitude and broad in support. This gives a clean service-coordinate interpretation: $B$ supports proper-radial service choreography while keeping transition burden low.

## Literature embedding

Morris and Thorne establish the traversable-wormhole throat as a geometric object with flare-out, low tidal-force, and exotic-support requirements [MorrisThorne1988]. Ford and Roman show that quantum inequalities create severe magnitude-duration and length-scale pressure for macroscopic traversable wormhole support, especially when negative energy is concentrated in thin regions [FordRoman1996]. Alcubierre introduces the warp-drive geometry and makes exotic matter part of the superluminal warp problem [Alcubierre1994]. Pfenning and Ford sharpen the warp-drive burden by connecting the Alcubierre wall to quantum-inequality severity and extreme wall thinness [PfenningFord1997]. Van den Broeck shows that capacity engineering can change energy accounting through compact exterior / large interior structure [VanDenBroeck1999]. Everett and Roman emphasize prepared-route infrastructure and the causal-control issue of bubble-wall engineering [EverettRoman1997]. Bobrick and Martire provide the ADM framework that separates lapse, shift, spatial geometry, capacity, and time-rate structure [BobrickMartire2021]. Gao, Jafferis, and Wall show that traversability can arise from a controlled source-timing mechanism in a holographic setting [GaoJafferisWall2017].

The v0.2 result sits inside that map and adds a composite-engineering answer. The literature supplies the broad principles: shell thickness matters, capacity matters, ADM role separation matters, and source timing matters. The v0.2 sweep supplies the design-specific mapping:

```math
\boxed{
C_0, C_\perp, R_{\rm th}, w_{\rm th}, B_0, w_B
\quad\longrightarrow\quad
\rho_H, {}^{(3)}R, j_M, K, \text{packet clearance, edge clearance}.
}
```

The new contribution is the burden allocation rule:

```math
\boxed{
\text{radial capacity alone preserves a service packet while carrying avoidable spatial-curvature burden; moderate angular capacity removes much of that burden.}
}
```

That statement follows from the composite v1/catch-rematched ADM screen and is more specific than the existing literature’s general wall-thickness and capacity guidance.

## v0.2 freeze statement

The v0.2 composite reference candidate is:

```math
\boxed{
\text{Catch-Rematched Hybrid-Flare-Gated Composite v0.2}
}
```

with:

```math
\boxed{
\text{early-catch v01 transition choreography plus broadened mixed radial/angular capacity support.}
}
```

The reference parameter set is:

```math
\boxed{
C_0=20,
\quad C_\perp=5,
\quad R_{\rm th}=1.25,
\quad w_{\rm th}=0.12,
\quad R_{\rm pass}=0.35,
\quad w_{\rm pass}=0.08,
\quad B_0=6,
\quad w_B=12.
}
```

The operational service layer is:

```math
\boxed{
x_{\rm catch}=0.05,
\quad x_\beta=0.70,
\quad x_q=1.25,
\quad w_{\rm catch}=0.25,
\quad w_\beta=0.28,
\quad w_q=0.30,
\quad p_\beta=4.
}
```

## Next gates

The next useful checks are:

1. higher-grid confirmation for the v0.2 candidate,
2. a dedicated $C_\perp\in\{4,5,6,7\}$ local scan,
3. repeated-cycle accumulation of $\rho_H$, $j_M$, and edge burden,
4. source-component matching for the transition-current layer and spatial-support layer,
5. perturbative timing tolerance around $x_{\rm catch}$, $x_\beta$, and $x_q$.

The v0.2 architecture gives those gates a specific target.

## Bundle contents

- `REPORT.md` — this report.
- `README.md` — reproduction notes.
- `code/adm_3p1_viability_v3_baware.py` — ADM diagnostic engine.
- `code/run_v02_confirmation.py` — compact v0.2 confirmation runner.
- `data/narrow_fast_sweep_25x11.csv` — broad narrow-family sweep.
- `data/selected_confirmation_41x17.csv` — selected candidate confirmation summary.
- `data/selected_confirmation_41x17_per_slice.csv` — per-slice confirmation data.
- `data/selected_confirmation_summary.json` — confirmation metadata and ranked rows.
- `derived/v02_tables.md` — derived report tables.
- `derived/v02_candidate_summary.json` — compact candidate summary.
- `sources/references.md` — literature references.
- `MANIFEST.sha256` — checksum manifest.

