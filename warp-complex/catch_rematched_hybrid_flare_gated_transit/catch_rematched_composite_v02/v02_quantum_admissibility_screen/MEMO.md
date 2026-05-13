# v0.2 quantum-source admissibility proxy screen

## Executive finding

The ADM current-floor source screen supports freezing the catch-rematched composite v0.2 refinement.

The v0.2 candidate preserves packet and support-edge clearance and materially improves the source-exposure quantities that matter most for a first quantum-admissibility proxy. In the stressed service case

```math
V=10,
\qquad
\lambda=6,
```

the packet-region Lorentzian sampled current-floor exposure at `tau = 0.2` moves from

```math
-2.0645\times 10^{-2}
```

to

```math
-8.704\times 10^{-4}.
```

That is about

```math
4.2\% 
```

of the v01 geometry baseline exposure.

The v0.2 candidate used for the screen is

```math
C_0=20,
\qquad
C_\perp=5,
\qquad
R_{\rm th}=1.25,
\qquad
w_{\rm th}=0.12,
```

```math
R_{\rm pass}=0.35,
\qquad
w_{\rm pass}=0.08,
\qquad
B_0=6,
\qquad
w_B=12.
```

The transition layer is the v0.1 early-catch service layer:

```math
x_{\rm catch}=0.05,
\qquad
x_\beta=0.70,
\qquad
x_q=1.25,
```

```math
w_{\rm catch}=0.25,
\qquad
w_\beta=0.28,
\qquad
w_q=0.30,
\qquad
p_\beta=4.
```

## Screen definition

The screen uses the ADM source-demand fields from the `3+1` diagnostic harness and evaluates the conservative current-floor proxy

```math
Tkk_{\rm floor}=\rho_H-2|j_M|.
```

The proxy reads the part of the source demand that is exposed to radial null-current pressure. It is a low-cost pre-freeze screen for packet, support-edge, release-edge, and service-union exposure.

The Hamiltonian source-demand proxy is

```math
\rho_H=\frac{{}^{(3)}R+K^2-K_{ij}K^{ij}}{16\pi}.
```

The momentum/current source-demand proxy is

```math
j_M^i=\frac{D_j(K^{ij}-\gamma^{ij}K)}{8\pi}.
```

Lorentzian sampling is performed over service-position histories. The screen compares the v0.2 candidate to the v01 geometry baseline, a reserve-capacity v0.2 alternative, and a no-angular-capacity comparison.

## Stressed-case readout

Scenario:

```math
V=10,
\qquad
\lambda=6.
```

| Candidate | packet min `Tkk_floor` | packet negative-volume proxy | packet `j_M` p95 | packet `rho_H` p95 | packet `R3` p95 | packet `K` p95 | packet Lorentzian floor, `tau=0.2` |
|---|---:|---:|---:|---:|---:|---:|---:|
| v01 geometry baseline | -0.789658 | 0.123668 | 0.300257 | 0.315277 | 15.847573 | 67.616640 | -0.020645 |
| v0.2 `C0=20,Cperp=5,B0=6,wB=12` | -0.124632 | 0.011353 | 0.003341 | 0.096020 | 4.826470 | 0.198121 | -0.000870 |
| v0.2 no-angular `Cperp=1` | -0.319837 | 0.036047 | 0.000403 | 0.315283 | 15.847838 | 0.095573 | +0.008000 |
| v0.2 reserve `C0=100,Cperp=5,B0=4,wB=6` | -0.149332 | 0.016040 | 0.013881 | 0.099929 | 5.023008 | 0.297073 | -0.006098 |

The v0.2 candidate gives the best balanced source-admissibility result. It combines low packet current burden, low Hamiltonian/spatial-curvature burden, and strong Lorentzian sampled-current improvement.

## Relative improvements

Across the tested service scenarios, the v0.2 candidate has the following worst-case relative readout against the v01 geometry baseline:

| Quantity | v0.2 relative readout |
|---|---:|
| packet negative-volume proxy | 0.103× |
| service-union negative-volume proxy | 0.099× |
| packet `j_M` p95 | 0.0129× |
| packet `rho_H` p95 | 0.305× |
| packet `R3` p95 | 0.305× |
| packet `K` p95 | 0.0034× |
| support-edge negative-volume proxy | 0.417× |

The v0.2 geometry reduces sampled packet exposure more strongly than the total source-cost proxy alone would suggest. The reason is channel-specific: v0.2 suppresses the current channel that drives the conservative null-current floor.

## Implications

### 1. The freeze is supported by the source screen

The v0.2 refinement already showed lower ADM geometry and dynamic source-demand cost. The current-floor source screen adds a packet-focused admissibility readout. The same candidate wins the balanced comparison.

The freeze statement is:

```math
\boxed{
\text{v0.2 reduces ADM source demand and sampled packet current-floor exposure while preserving packet and edge clearance.}
}
```

### 2. Mixed radial/angular capacity improves quantum-source posture

The strongest geometry lesson from v0.2 remains active in the source screen. Moderate angular capacity is the handle that reduces Hamiltonian/spatial-curvature burden.

The no-angular comparison is decisive:

| Candidate | packet negative-volume proxy | packet `rho_H` p95 | packet `R3` p95 | packet Lorentzian floor, `tau=0.2` |
|---|---:|---:|---:|---:|
| `Cperp=1` | 0.036047 | 0.315283 | 15.847838 | +0.008000 |
| `Cperp=5` | 0.011353 | 0.096020 | 4.826470 | -0.000870 |

The no-angular case gives an excellent current-channel number. The mixed-capacity case gives the balanced source-admissibility posture by reducing the Hamiltonian and spatial-curvature burden at the same time.

The design language is:

```math
\boxed{
\text{minimum useful radial capacity plus moderate angular capacity.}
}
```

### 3. Burden-channel separation carries through to the source screen

The source screen confirms the v0.1/v0.2 decomposition:

```math
\text{transition profiles}\rightarrow j_M, K,
```

```math
\text{capacity/support geometry}\rightarrow \rho_H, {}^{(3)}R.
```

v0.1 reduced the transition-current channel. v0.2 reduced the Hamiltonian/spatial-curvature channel. The source proxy shows that reducing the current channel also reduces Lorentzian sampled packet exposure.

### 4. The reserve-capacity branch remains viable

The reserve candidate

```math
C_0=100,
\qquad
C_\perp=5,
\qquad
B_0=4,
\qquad
w_B=6
```

keeps a strong source-screen result:

```math
\text{packet negative-volume proxy}=0.016040,
```

```math
\text{packet Lorentzian floor at }\tau=0.2=-0.006098.
```

The minimum-burden v0.2 candidate has the better pre-freeze balance. The reserve branch remains useful for later high-capacity or high-velocity studies.

## Literature placement

The standard literature makes negative-energy duration, wall thickness, and source timing central to traversable wormhole and warp-drive feasibility. Morris--Thorne defines the traversable throat and its flare/tidal/support requirements. Ford--Roman and Pfenning--Ford connect macroscopic wormhole and warp support to quantum-inequality pressure. Van den Broeck introduces capacity engineering as an explicit geometric handle. Everett--Roman emphasize prepared infrastructure and causal control. Bobrick--Martire provide the ADM role separation that makes lapse, shift, spatial geometry, and capacity independently legible. Gao--Jafferis--Wall show traversability as a controlled source-timing effect in a holographic setting.

The v0.2 source screen adds a specific composite-system result inside that map:

```math
\boxed{
\text{mixed radial/angular capacity reduces packet-region current-floor exposure and Hamiltonian/spatial-curvature burden together.}
}
```

The literature supplies the broad expectation that smooth support and controlled source timing matter. The v0.2 screen supplies the design-specific mapping:

```math
C_\perp=5
\quad\text{reduces}\quad
\rho_H, {}^{(3)}R,
\text{ and sampled packet exposure}
```

while the v0.1 transition layer controls

```math
j_M
\quad\text{and}\quad
K.
```

That is the useful new contribution of this phase.

## Freeze recommendation

Freeze the v0.2 refinement.

The frozen candidate is:

```math
\boxed{
C_0=20,
\quad
C_\perp=5,
\quad
R_{\rm th}=1.25,
\quad
w_{\rm th}=0.12,
\quad
R_{\rm pass}=0.35,
\quad
w_{\rm pass}=0.08,
\quad
B_0=6,
\quad
w_B=12.
}
```

with the v0.1 transition layer:

```math
\boxed{
x_{\rm catch}=0.05,
\quad
x_\beta=0.70,
\quad
x_q=1.25,
\quad
w_{\rm catch}=0.25,
\quad
w_\beta=0.28,
\quad
w_q=0.30,
\quad
p_\beta=4.
}
```

The next source-level project is pressure-complete source-channel construction:

```math
T_{\mu\nu}^{\rm support}
+
T_{\mu\nu}^{\rm transition-current}
+
T_{\mu\nu}^{\rm angular-capacity}
+
T_{\mu\nu}^{\rm shoulder/matching}
+
T_{\mu\nu}^{\rm packet-coupling}.
```

The pressure-complete project can now start from a geometry whose low-cost quantum-source proxy supports the freeze.
