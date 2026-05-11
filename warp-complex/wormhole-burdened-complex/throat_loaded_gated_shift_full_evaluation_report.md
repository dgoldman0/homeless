# Throat-Loaded Transit Architecture: Gated-Shift Reduced Evaluation

## Executive result

This evaluation selects the **throat-gated, shift-first throat-loaded family** as the strongest reduced candidate so far.

The base ansatz separated the geometry into three ADM control handles: spatial capacity, lapse/time-rate structure, and transport shift. That separation made the present refinement direct: move capacity and lapse into the wormhole throat complex, then place the transport shift under the same throat support profile. The evaluation result confirms that this is the coherent reduced architecture.

The guiding statement for the architecture is:

> A throat-loaded transit architecture requires the wormhole complex to be the active control system. The mobile bubble share becomes a coupling/passenger region, while the throat infrastructure manages shift, capacity, lapse, and release timing.

The main result is architectural confirmation. Capacity, lapse, and shift behave as one managed throat system. The mobile region becomes a passenger/coupling profile, with high-shift transport supplied by the throat infrastructure.

## Background

The starting ansatz used a Morris-Thorne-style wormhole background in proper radial coordinate, combined with a Bobrick-Martire-style ADM warp shell and a Van den Broeck-style compact-exterior / large-interior capacity factor. In ADM form, the ansatz separates lapse, shift, and spatial geometry:

```math
\alpha=e^{\Phi(l)}T,
\qquad
\gamma_{ij}=A^2q_{ij},
\qquad
\beta^i=-VSn^i.
```

The original compatibility diagnostics were determinant/signature, curvature invariants, Einstein tensor projections, ADM constraint quantities, throat-area behavior, and reduced null expansions. The base ansatz also identified the central causal diagnostic in the radial reduction:

```math
g_{tt}=-e^{2\Phi}T^2+A^2V^2S^2.
```

This report evaluates the throat-loaded refinement of that same structure. The refinement places capacity and lapse in the wormhole throat complex, then tests whether the shift must also be throat managed.

The external literature supports this direction. Morris and Thorne’s traversable wormhole framework makes the throat the natural locus of exotic geometric support. Bobrick and Martire’s ADM warp-drive framework separates the physical roles of lapse, shift, and spatial geometry. Van den Broeck’s compact-exterior / large-interior modification motivates the capacity factor. Everett and Roman’s Krasnikov-tube analysis highlights the control value of prepared infrastructure for superluminal transit, especially where onboard control of a bubble wall becomes causally constrained. Full citations are listed at the end of this report.

## Tested reduced family

The reduced evaluation used spherical symmetry on the radial axis with:

```math
r(l)=\sqrt{r_0^2+l^2},
\qquad
\Phi=0.
```

The throat-loaded capacity factor was:

```math
A(l,L)=\exp\!\left[q(L)W(l)\ln C_0\right].
```

The throat-loaded lapse factor was:

```math
T(l,L)=\exp\!\left[q(L)W(l)\ln(\lambda C_0)\right].
```

Here:

```math
W(l)
```

is the throat support profile, while

```math
q(L)
```

controls the release of throat capacity and lapse as the passenger center reaches the exit layer.

The passenger/coupling profile was:

```math
S_{\rm pass}(l-L).
```

Two transport structures were compared.

### Independent passenger shift comparison

```math
\beta^l=-V E(L)S_{\rm pass}(l-L).
```

This keeps transport attached to the passenger profile and allows the shift to extend beyond the strongest throat-supported region.

### Throat-gated shift family

```math
\beta^l=-V E(L)W(l)S_{\rm pass}(l-L).
```

This keeps transport inside the throat-managed support region. It makes capacity, lapse, and shift members of the same infrastructure-controlled geometry.

## Release profiles

Three release profiles were sampled.

| Release profile | Meaning |
|---|---|
| synchronized | shift support and throat capacity/lapse release together |
| shift-first | shift support tapers before throat capacity/lapse release |
| rapid shift-first | same ordering with a sharper shift taper |

The position functions were shaped by:

```math
E(L)
```

for transport support, and:

```math
q(L)
```

for throat capacity/lapse support.

The shift-first ordering is:

```math
L_{\beta}<L_q,
```

so the transport support decreases before the capacity/lapse support relaxes.

## Parameter sweep

The velocity ladder was:

```math
V\in\{0.9,\ 1.01,\ 1.1,\ 1.25,\ 1.5,\ 2.0\}.
```

The lapse margin was:

```math
\lambda=\max(1.05,\ 1.15V).
```

The capacity and wall settings were:

```math
C_0\in\{100,\ 10^4\},
\qquad
\Delta\in\{0.3,\ 0.1\}.
```

Release widths and gaps were sampled with:

```math
w_{\rm release}\in\{0.35,\ 0.18\},
\qquad
L_q-L_\beta\in\{0.35,\ 0.70,\ 1.00\}.
```

The full pass evaluated 336 configurations for the throat-gated family, with traversal, exit, and post-exit phases recorded for each configuration.

## Diagnostics

The evaluation recorded:

| Diagnostic | Role |
|---|---|
| `max_gtt` | lapse-shift causal-balance monitor |
| `min_lapse_shift_margin` | direct margin for the supported transport term |
| `R` | Ricci scalar response |
| `Kretsch` | full curvature concentration proxy |
| `Gkp`, `Gkm` | reduced null Einstein projections |
| `theta_p theta_m` | reduced null-expansion product |
| `tidal_radial`, `tidal_angular` | ADM-normal orthonormal tidal components |
| throat burden share | location of geometric burden |
| post-exit departures of `A`, `T`, and `gtt` | recovery toward exterior background |

The burden proxy was integrated over throat and passenger regions using:

```math
B
=
\int
\left(
|R|
+
\sqrt{|K_{\rm Kretsch}|}
+
\max(0,-G_{\mu\nu}k_+^\mu k_+^\nu)
+
\max(0,-G_{\mu\nu}k_-^\mu k_-^\nu)
+
|R_{\hat 0\hat l\hat 0\hat l}|
+
|R_{\hat 0\hat \theta\hat 0\hat \theta}|
\right)dV.
```

The throat share is:

```math
\frac{B_{\rm throat}}{B_{\rm total}}.
```

This proxy locates burden in the reduced model; full stress-energy accounting belongs to the later 3+1 validation pass.

## Core result: shift belongs to the throat complex

The independent passenger-shift comparison entered lapse-shift balance crossings in a substantial portion of the sweep. It produced:

| Independent passenger shift result | Value |
|---|---:|
| configurations | 336 |
| exit configurations with positive `gtt` points | 134 |
| traversal configurations with positive `gtt` points | 220 |
| clean traversal-and-exit configurations | 100 |
| worst exit `max_gtt` | `4.1995e5` |
| worst traversal `max_gtt` | `1.2970e5` |
| worst exit null-expansion product | `1.4260e4` |
| mean exit throat burden share | `0.9728` |
| minimum exit throat burden share | `0.6632` |

The throat-gated shift family produced the corresponding result:

| Throat-gated shift result | Value |
|---|---:|
| configurations | 336 |
| exit configurations with positive `gtt` points | 0 |
| traversal configurations with positive `gtt` points | 0 |
| clean traversal-and-exit configurations | 336 |
| worst exit `max_gtt` | `-1.0` |
| worst traversal `max_gtt` | `-1.0` |
| worst exit null-expansion product | `657.37` |
| mean exit throat burden share | `0.9948` |
| minimum exit throat burden share | `0.9123` |

The result is expected from the reduced metric. With throat-loaded capacity and lapse, the supported region is controlled by:

```math
A(l,L),
\qquad
T(l,L),
\qquad
W(l).
```

An independent passenger shift can extend transport support into regions where the throat support has tapered. A throat-gated shift keeps transport colocated with the same support profile that carries capacity and lapse.

The result selects the coherent reduced form:

```math
A=A_{\rm throat},
\qquad
T=T_{\rm throat},
\qquad
\beta^l=\beta^l_{\rm throat\ gated}.
```

## Velocity ladder result

Across the velocity ladder, the throat-gated family kept the causal-balance monitor clean in every sampled configuration.

| V | configurations | exit `gtt` positive | traversal `gtt` positive | worst exit `theta_+ theta_-` | mean throat burden share | minimum throat burden share |
|---:|---:|---:|---:|---:|---:|---:|
| 0.90 | 56 | 0 | 0 | 146.88 | 0.9935 | 0.9123 |
| 1.01 | 56 | 0 | 0 | 182.66 | 0.9940 | 0.9163 |
| 1.10 | 56 | 0 | 0 | 214.35 | 0.9944 | 0.9199 |
| 1.25 | 56 | 0 | 0 | 272.39 | 0.9949 | 0.9258 |
| 1.50 | 56 | 0 | 0 | 383.37 | 0.9956 | 0.9352 |
| 2.00 | 56 | 0 | 0 | 657.37 | 0.9966 | 0.9512 |

Two trends matter.

First, the throat-gated family keeps the lapse-shift monitor controlled through the full sampled ladder. Second, the null-expansion pulse grows with velocity. That gives a clean next target: shape the exit pulse while retaining throat-gated transport support.

## Release profile result

The release profiles all retained the clean causal margin once the shift was throat-gated.

| Release profile | configurations | exit `gtt` positive | traversal `gtt` positive | worst exit `theta_+ theta_-` | mean throat burden share | minimum throat burden share |
|---|---:|---:|---:|---:|---:|---:|
| synchronized | 48 | 0 | 0 | 170.44 | 0.9929 | 0.9123 |
| shift-first | 144 | 0 | 0 | 180.11 | 0.9937 | 0.9123 |
| rapid shift-first | 144 | 0 | 0 | 657.37 | 0.9966 | 0.9446 |

The rapid shift-first profile concentrates burden strongly in the throat and produces the largest expansion pulse. The ordinary shift-first profile keeps the intended operational ordering while maintaining a much smaller pulse. The synchronized profile also remains clean in this reduced gated pass, which shows that the gating is the dominant causal-balance organizer. The shift-first profile remains the preferred transit choreography because it matches the infrastructure control sequence: transport support fades first, then throat capacity/lapse relaxes.

## Post-exit recovery

The post-exit region returned close to the exterior background in the reduced scan.

| Quantity | worst post-exit departure |
|---|---:|
| `A` from 1 | `0.00309` |
| `T` from 1 | `0.00337` |
| `gtt` from -1 | `0.00676` |

This supports the intended exit interpretation: the passenger/coupling region passes through the throat-managed release layer, the transport support fades, and the geometry returns toward the exterior background state.

## Physical interpretation

The throat-gated result is an architectural confirmation.

The mobile bubble share becomes lighter because the high-shift field is assigned to the throat support profile. The throat complex supplies the three high-burden functions together:

```math
A_{\rm throat},
\qquad
T_{\rm throat},
\qquad
\beta^l_{\rm throat}.
```

That matches the burden-shift goal. The wormhole complex becomes the active transit machine. The mobile component becomes a coupling/passenger region whose job is local matching, passenger protection, and transit through the prepared support profile.

This also addresses the known warp-bubble control issue in the intended way. Everett and Roman emphasized causal separation between the observer at the center of an Alcubierre-type bubble and the outer bubble wall, placing wall control outside the passenger domain. Krasnikov-style infrastructure responds by preparing the relevant spacetime structure as an external route. The throat-loaded architecture follows the same infrastructure logic in a localized gate form: the wormhole complex manages shift, capacity, lapse, and release timing.

## Engineering interpretation

The clean architecture is a prepared wormhole transit complex.

The throat complex carries:

```math
A_{\rm throat},
\qquad
T_{\rm throat},
\qquad
\beta^l_{\rm throat},
\qquad
q(L),
\qquad
E(L).
```

The passenger component carries:

```math
S_{\rm pass},
\qquad
\text{local matching},
\qquad
\text{tidal smoothing},
\qquad
\text{occupant region definition}.
```

This is a reusable gate architecture. The throat infrastructure supplies the demanding geometry. The mobile share enters as the region that couples to the prepared throat support.

## Implications for the ansatz

The next ansatz candidate should be written directly with throat-gated transport:

```math
A(l,L)=\exp\!\left[q(L)W(l)\ln C_0\right],
```

```math
T(l,L)=\exp\!\left[q(L)W(l)\ln(\lambda C_0)\right],
```

```math
\beta^l(l,L)=-V E(L)W(l)S_{\rm pass}(l-L).
```

The support hierarchy is:

```math
\operatorname{supp}(\beta^l)
\subseteq
\operatorname{supp}(A,T),
```

or, operationally:

```math
\text{transport support remains inside throat-managed support}.
```

The release ordering for the preferred choreography is:

```math
E(L)\rightarrow0
\quad\text{before}\quad
q(L)\rightarrow0.
```

That ordering keeps the transport term under throat management during exit and lets the throat capacity/lapse relax after the passenger coupling has settled.

## What this result says about the previous moving-shell branch

The moving-shell branch was useful because it revealed the coordination rule among capacity, lapse, and shift. The throat-loaded branch now expresses that rule as infrastructure design.

The moving-shell form tested how much geometry a mobile compact wall can carry. The throat-loaded form transfers the main capacity/lapse/transport structure to the wormhole complex. The present result shows that the transfer should include shift as well as capacity and lapse.

## Remaining validation before major computation

The reduced family is strong enough to define the next ansatz. The following checks remain before expensive 3+1 evolution.

### 1. Profile robustness

Test multiple smooth compact profiles for:

```math
W(l),
\qquad
S_{\rm pass}(l-L),
\qquad
E(L),
\qquad
q(L).
```

The desired result is qualitative stability under profile changes.

### 2. Tidal worldline evaluation

Evaluate:

```math
R_{\hat 0\hat i\hat 0\hat j}
```

along representative passenger worldlines through traversal and exit. The current scan already records radial and angular tidal components on the grid; the next pass should convert that into passenger-frame histories.

### 3. Null congruence maps

The scalar product:

```math
\theta_+\theta_-
```

should be mapped across the throat and exit layer with finer resolution near the release surfaces. The current result identifies pulse growth with velocity and release sharpness.

### 4. Entrance branch

The same throat-gated architecture should be evaluated for entrance. The expected sequence is the reverse infrastructure choreography: establish capacity/lapse support, admit transport coupling, then guide the passenger region into the throat-supported domain.

### 5. Anisotropic capacity

The scalar capacity factor should be generalized to:

```math
A_{\parallel}(l,L),
\qquad
A_{\perp}(l,L).
```

This tests whether longitudinal throat traversal and angular passenger volume can be shaped independently.

### 6. Constraint-quality initial data

The reduced ansatz prescribes geometry and reads off stress-energy through the Einstein tensor. A later pass should formulate compatible initial data and evaluate Hamiltonian and momentum constraint behavior in a more explicit 3+1 setting.

### 7. Semiclassical and quantum-inequality checks

The architecture is still in the family of exotic spacetime geometries. The next theory pass should estimate quantum-inequality exposure, semiclassical stress-energy behavior, and possible radiation accumulation near the managed throat/exit surfaces.

## Conclusion

The full reduced evaluation supports a sharper ansatz:

```math
A=A_{\rm throat},
\qquad
T=T_{\rm throat},
\qquad
\beta^l=\beta^l_{\rm throat\ gated}.
```

The result is aligned with the design goal. The wormhole complex acts as the active transit system. The mobile share becomes the coupling/passenger region. The burden proxy concentrates in the throat region, the post-exit state returns close to exterior background values, and the causal-balance diagnostic stays controlled through the sampled velocity ladder up to:

```math
V=2.0.
```

The next ansatz should adopt throat-gated shift support from the start and treat exit timing as an infrastructure profile.

## Companion files

- `ansatz_throat_loaded_gated_full_eval.py` — main gated-shift evaluation code.
- `run_throat_loaded_gated_full_eval_batched.py` — batch runner.
- `ansatz_throat_loaded_gated_full_eval_results.json` — raw gated-shift results.
- `ansatz_throat_loaded_gated_full_eval_summary.json` — gated-shift aggregate summary.
- `ansatz_throat_loaded_full_eval.py` — independent passenger-shift comparison code.
- `ansatz_throat_loaded_full_eval_summary.json` — independent passenger-shift comparison summary.

## References

1. Morris, M. S., and Thorne, K. S. “Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity.” *American Journal of Physics* 56, 395 (1988). https://www.pas.rochester.edu/~tim/introframe/AmJPhysBlackHoles.pdf

2. Bobrick, A., and Martire, G. “Introducing physical warp drives.” *Classical and Quantum Gravity* 38, 105009 (2021). https://arxiv.org/abs/2102.06824

3. Van den Broeck, C. “A ‘warp drive’ with more reasonable total energy requirements.” *Classical and Quantum Gravity* 16, 3973 (1999). https://arxiv.org/abs/gr-qc/9905084

4. Everett, A. E., and Roman, T. A. “A Superluminal Subway: The Krasnikov Tube.” *Physical Review D* 56, 2100 (1997). https://arxiv.org/abs/gr-qc/9702049

5. Alcubierre, M. “The warp drive: hyper-fast travel within general relativity.” *Classical and Quantum Gravity* 11, L73 (1994). https://arxiv.org/abs/gr-qc/0009013
