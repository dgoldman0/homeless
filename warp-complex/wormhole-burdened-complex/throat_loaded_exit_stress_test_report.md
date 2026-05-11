# Throat-Loaded Exit Stability: Initial Stress Test and Control Implications

## Scope

This report evaluates the first reduced stress test of a throat-loaded transit branch derived from the compact warp-shell / wormhole ansatz. The tested branch moves the capacity and lapse structure into the wormhole throat while leaving the mobile bubble share as a passenger/coupling region with a transport shift. The main question is what the geometry does during traversal and exit: whether the passenger region settles back into ordinary exterior spacetime through a controlled release pulse, or whether the exit sequence amplifies the lapse-shift balance, null expansions, and curvature response.

Entrance sequencing is reserved for a separate pass. This report focuses on traversal and exit because exit is where the known warp-bubble control issue becomes most direct: the moving passenger region should have a prepared way to decouple from the transport geometry and return to standard exterior conditions.

The base ansatz already separates the three objects that matter for this stress test:

```math
\alpha=e^{\Phi(l)}T
```

```math
\gamma_{ij}=A^2q_{ij}
```

```math
\beta^i=-VS n^i
```

Here `A` carries spatial capacity, `T` carries lapse/time-rate support, and `beta` carries transport. That separation is the reason the burden-shift question can be evaluated cleanly: capacity, lapse, and transport can be anchored to different parts of the architecture.

## Literature motivation: control belongs to the infrastructure

The control problem for superluminal warp bubbles is a central reason to test a throat-loaded architecture. Everett and Roman describe the Alcubierre bubble center as causally separated from the outer wall, giving the central observer no on-demand control of bubble creation or wall behavior once the bubble exists.[^everett_roman] Lobo’s review makes the same point in the Krasnikov context: points on the outside front edge of a superluminal bubble are spacelike separated from the center, so the control system must be arranged by a larger geometry or pre-existing route.[^lobo_review]

That maps directly onto the current architecture:

> A throat-loaded transit architecture requires the wormhole complex to be the active control system. The mobile bubble share becomes a coupling/passenger region, while the throat infrastructure manages shift, capacity, lapse, and release timing.

The Krasnikov-tube literature is useful because it treats superluminal transit as an infrastructure problem rather than a self-contained vehicle problem. Krasnikov’s own framing asks what a traveller can achieve when the geometry of the route is part of the setup.[^krasnikov] Everett and Roman’s “superluminal subway” interpretation makes the infrastructure analogy explicit.[^everett_roman]

The throat-loaded ansatz follows that lesson. The passenger region does not need to command its own wall after entering a questionable causal regime. The wormhole complex supplies a prepared exit layer. The release sequence is built into the geometry.

## Relation to the base ansatz

The base family combines a Morris-Thorne wormhole throat with a generalized Bobrick-Martire warp shell and a Van den Broeck-style compact-exterior / large-interior capacity factor. Morris and Thorne provide the smooth throat geometry with areal radius `r(l)`, finite redshift, and flare-out structure.[^morris_thorne] Bobrick and Martire provide the ADM-style decomposition in which space capacity and time rate can be treated as independent design functions.[^bobrick_martire] Van den Broeck supplies the compact-exterior / large-interior idea that motivates `C0 >> 1` as an interior-capacity parameter.[^vdb]

The moving-shell tests used capacity and lapse functions that traveled with the mobile shell. The throat-loaded branch relocates those fields:

```math
A(\rho,t) \quad \longrightarrow \quad A_{\rm throat}(l,t)
```

```math
T(\rho,t) \quad \longrightarrow \quad T_{\rm throat}(l,t)
```

The mobile share keeps the transport/localization role:

```math
\beta^l_{\rm pass}=-V E(t,l)S_{\rm pass}(l-L(t))
```

The design goal is to put the high-gradient capacity/lapse structure in the wormhole complex, where the exotic-support and flare-out infrastructure already reside. The mobile bubble share then approaches a lower-burden coupling/passenger geometry.

## Stress-test model

The reduced model uses the same radial/spherical simplification as the earlier evaluations:

```math
r(l)=\sqrt{1+l^2},\qquad \Phi=0
```

The throat-supported capacity is:

```math
A(l,t)=\exp\left[q(t)W(l)\ln C_0\right]
```

The throat-supported lapse is:

```math
T(l,t)=\exp\left[q(t)W(l)\ln(\lambda C_0)\right]
```

Inside the active throat region, this gives:

```math
T\approx \lambda A
```

The passenger transport shift is:

```math
\beta^l=-V E(t)S_{\rm pass}(l-L(t))
```

or, in the infrastructure interpretation, `E` can be read as an exit-layer support function tied to position through `L(t)`. The stress test used two release profiles:

1. **Synchronized release**: transport and throat support relax together through `E=q^m`.
2. **Staged release**: the transport shift relaxes before the throat capacity/lapse support.

The staged profile used a shift-release lead time:

```math
E(t)=\left[\frac12\left(1-\tanh\frac{t-t_\beta}{\tau_\beta}\right)\right]^m
```

```math
t_\beta=t_{\rm exit}-b\tau
```

with `b` represented by `beta_lead`. The strongest staged cases used `beta_lead = 3`, meaning the transport shift was mostly faded before the throat support release.

The diagnostic set follows the base ansatz:

```math
R,\quad R_{\mu\nu}R^{\mu\nu},\quad R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
```

```math
G_{\mu\nu}k^\mu k^\nu
```

```math
g_{tt}=-T^2+A^2V^2E^2S_{\rm pass}^2
```

```math
\theta_+\theta_-
```

and a regional burden proxy:

```math
B_\Omega=\int_\Omega\left(|R|+\sqrt{|K_{\rm Kretsch}|}+\max(0,-G_{\mu\nu}k^\mu k^\nu)\right)dl
```

The burden-share diagnostic is:

```math
f_{\rm throat}=\frac{B_{\rm throat}}{B_{\rm throat}+B_{\rm passenger}}
```

This is a proxy, not a physical energy integral. Its role is to track whether the large diagnostic load is localized in the throat complex or follows the passenger region.

## Velocity choice

Two velocity branches were evaluated:

| Branch | Parameters | Role in this report |
|---|---:|---|
| Subluminal exit | `V = 0.9`, `lambda = 1.0` | baseline exit behavior for throat-loaded release |
| Superluminal stress exit | `V = 2.0`, `lambda = 2.25` | aggressive stress probe of the release ordering |

The superluminal value `V = 2.0` was chosen because the earlier `T = lambda A` family showed that the causal-margin condition follows:

```math
|V|S<\lambda
```

With `lambda = 2.25`, the active-throat phase has analytic lapse margin for the tested stress velocity. This makes `V = 2.0` useful as a release-sequencing probe: it amplifies timing effects while keeping the active-throat design inside the intended `lambda > V` margin.

## Results: burden localization

The throat-loaded branch achieved the central burden-shift objective in the reduced diagnostic. During exit, the throat region carried most of the measured burden proxy across the sampled cases.

| Release family | Representative range of mean throat burden share | Interpretation |
|---|---:|---|
| synchronized subluminal, `V = 0.9` | `0.72` to `0.89` | capacity/lapse burden centered in the throat, with finite passenger overlap during release |
| synchronized superluminal stress, `V = 2.0` | `0.71` to `0.93` | throat remains the dominant burden region during the stress pass |
| staged superluminal stress, `beta_lead = 3` | `0.81` to `0.96` | shift-first release concentrates the diagnostic burden most strongly in the throat complex |

The result supports the engineering interpretation: moving `A` and `T` into the throat changes the mobile bubble share into a lower-burden coupling region. The mobile share still carries transport and matching structure, while the fixed complex carries capacity, lapse, and most of the stress-energy proxy.

## Results: subluminal synchronized exit

For `V = 0.9`, synchronized release produced a pulse-and-settle exit signature across the sampled ramps. The causal balance stayed controlled throughout the sampled exit interval: `g_tt` remained below zero and the lapse-shift margin remained positive.

Representative case: `C0 = 100`, `Delta = 0.3`, synchronized release.

| Release time `tau` | max `g_tt` | min margin | max `theta_+ theta_-` | exit / traverse Kretschmann ratio |
|---:|---:|---:|---:|---:|
| `1.0` | `-0.2008` | `0.1060` | `1.3915` | `0.8946` |
| `0.5` | `-0.6121` | `0.3746` | `5.5662` | `0.8596` |
| `0.25` | `-0.3773` | `0.1948` | `22.2650` | `0.8598` |
| `0.1` | `-0.2248` | `0.1166` | `139.1563` | `0.8604` |

The release pulse is visible in the null-expansion product. Shorter release times produce larger expansion pulses. The curvature scale remains comparable to the traversal phase for this representative subluminal case.

The same pattern appears at `C0 = 10000`, `Delta = 0.3`: `g_tt` remains below zero, the margin remains positive, and `theta_+ theta_-` grows as `tau` decreases from `1.0` to `0.1`.

## Results: synchronized superluminal stress exit

The synchronized `V = 2.0`, `lambda = 2.25` stress case highlights the value of release ordering. During synchronized release, transport remains active while the throat capacity/lapse support is already relaxing. That timing produces a strong lapse-shift balance response.

Representative case: `V = 2.0`, `lambda = 2.25`, `C0 = 10000`, `Delta = 0.3`, synchronized release.

| Release time `tau` | max `g_tt` | min margin | max `theta_+ theta_-` | exit / traverse Kretschmann ratio |
|---:|---:|---:|---:|---:|
| `1.0` | `1.355e4` | `-15.3894` | `1071.6021` | `1.2002` |
| `0.5` | `2.311e5` | `-106.5666` | `1719.6062` | `3.1665` |
| `0.25` | `3.966e5` | `-147.7301` | `1842.1220` | `3.3260` |
| `0.1` | `3.088e5` | `-67.5922` | `1247.4140` | `2.8076` |

The synchronized stress result gives a clear sequencing rule. The transport shift should fade while throat-supported lapse remains available. A release profile that fades capacity/lapse while transport still overlaps the passenger region amplifies the balance term:

```math
g_{tt}=-T^2+A^2V^2E^2S_{\rm pass}^2
```

This is the same causal diagnostic that organized the earlier `T = A` and `T = lambda A` families.

## Results: staged superluminal stress exit

The staged exit scan used `V = 2.0`, `lambda = 2.25`, with `beta_lead` controlling how early the shift taper begins relative to throat support release.

Across the staged scan:

| Shift lead | Clean causal-margin cases | Mean throat burden share | max `theta_+ theta_-` across group |
|---:|---:|---:|---:|
| `beta_lead = 1` | `0 / 24` | `0.870` | `5343.913` |
| `beta_lead = 2` | `8 / 24` | `0.879` | `5090.972` |
| `beta_lead = 3` | `24 / 24` | `0.889` | `22.768` |

A “clean causal-margin case” means `max g_tt < 0` and positive minimum lapse-shift margin in the sampled grid. The `beta_lead = 3` family satisfied that condition across all 24 sampled combinations of `C0`, `Delta`, `tau`, and shift-taper width.

Representative comparison, `V = 2.0`, `lambda = 2.25`, `C0 = 10000`, `Delta = 0.3`, `tau = 1.0`:

| Exit profile | max `g_tt` | min margin | max `theta_+ theta_-` | max Kretschmann | mean throat burden share |
|---|---:|---:|---:|---:|---:|
| synchronized | `1.355e4` | `-15.3894` | `1071.6021` | `2.079e6` | `0.913` |
| staged, `beta_lead = 3` | `-1.0000` | `0.9979` | `1.4230` | `1.365e6` | `0.955` |

The staged profile gives the cleanest sampled exit behavior. Transport fades first; throat support remains active through the shift taper; the throat then relaxes its capacity/lapse structure after the passenger region has settled into the exterior branch.

For the narrower wall case `Delta = 0.1`, the curvature scale is higher, as expected from the capacity-gradient scaling. With `C0 = 10000`, `Delta = 0.1`, `tau = 1.0`, and `beta_lead = 3`, the staged scan gives:

| max `g_tt` | min margin | max `theta_+ theta_-` | max Kretschmann | mean throat burden share |
|---:|---:|---:|---:|---:|
| `-1.0000` | `0.9979` | `1.4230` | `6.659e7` | `0.955` |

The same causal sequencing works in the narrow-wall stress case. The curvature scale reflects the compact support and remains a throat-complex engineering quantity.

## Exit signature

The sampled smooth ramps produce a pulse-and-settle exit signature.

The passenger region returns toward exterior conditions after the release:

```math
A\rightarrow1,\qquad T\rightarrow1,\qquad g_{tt}\rightarrow-1
```

In the synchronized subluminal cases, the post-release `A` departure was about `1.1%` to `2.3%` in the sampled post window, consistent with the finite tail of the smooth `tanh` release profile. The post-release `g_tt` returned to `-1.0` in the sampled grid.

The pulse amplitude is controlled by release time, wall thickness, and shift/capacity timing. Shorter `tau` values raise the null-expansion pulse. Narrower `Delta` values raise the curvature scale. Earlier shift tapering improves the causal-margin diagnostic in the superluminal stress case.

## Physical interpretation

The throat-loaded branch shifts the engineering emphasis from mobile field generation to fixed infrastructure control.

In the moving-shell family, the mobile object carries capacity `A`, lapse `T`, and shift `beta`. In the throat-loaded family, the wormhole complex supplies the capacity and lapse fields while the passenger/coupling share rides the transport field through the active throat region. This changes the practical architecture:

| Component | Moving-shell family | Throat-loaded family |
|---|---|---|
| Capacity enlargement | mobile wall | throat complex |
| Lapse support | mobile wall | throat complex |
| Transport shift | mobile shell / shared field | externally profiled transit field |
| Release control | wall-dependent | exit-layer choreography |
| Passenger share | full compact-capacity geometry | coupling/passenger region |

The comparative ease of the mobile bubble share comes from removing the high-amplitude capacity/lapse gradients from the travelling object. The mobile share still requires matching, tidal shaping, and transport coupling. Its required geometry is smaller than the self-contained compact-capacity shell because the large `C0` structure is supplied by the throat.

The wormhole complex becomes the active megastructure. It carries the main exotic support, the throat flare-out, the capacity/lapse layer, and the exit timing. Repeated use becomes a property of the fixed complex: each transit passes through a prepared geometry rather than recreating the high-burden geometry inside the passenger object.

## Relation to known warp-drive constraints

The stress-test result aligns with the literature in three ways.

First, it accepts the control lesson from Alcubierre/Krasnikov analyses. Superluminal bubble control is a route/infrastructure problem. Everett and Roman’s causal separation result supports external control of the wall/route geometry.[^everett_roman] Krasnikov-style infrastructure supplies the closest conceptual precedent for prepared transit corridors.[^krasnikov]

Second, it preserves the capacity idea from Van den Broeck while relocating where the compact-capacity gradient lives. Van den Broeck’s construction uses a small external scale and a large interior volume to reduce total energy compared with the original Alcubierre proposal.[^vdb] In this throat-loaded branch, the compact-capacity gradient belongs mainly to the throat complex.

Third, it keeps the quantum and semiclassical questions active. Pfenning and Ford’s quantum-inequality analysis ties negative-energy magnitude and sampling duration to strong constraints on warp-wall thickness.[^pfenning_ford] Finazzi, Liberati, and Barceló find semiclassical growth of the renormalized stress-energy tensor near the front wall of dynamical superluminal warp-drive geometries.[^finazzi] McMonigal, Lewis, and O’Byrne find strong particle-energy effects associated with accelerating/decelerating Alcubierre bubbles.[^mcmonigal]

The throat-loaded design gives those questions a different target. The main semiclassical and accumulated-particle checks should be applied to the throat exit layer, the shift taper, and the release pulse, because those are the active locations in this architecture.

## Initial conclusions

The first reduced stress test supports five working conclusions.

1. **The burden-shift architecture behaves as designed in the diagnostic proxy.** The throat region carries the majority of the measured curvature/null-projection burden in both traversal and exit.

2. **Subluminal exit supports synchronized release.** For `V = 0.9`, the sampled synchronized ramps keep the causal-margin diagnostic controlled and return the exterior branch toward `A = T = 1`.

3. **Superluminal stress exit is release-order sensitive.** With `V = 2.0`, `lambda = 2.25`, synchronized release amplifies the lapse-shift balance. Shift-first staging preserves the sampled causal margin.

4. **The mobile bubble share becomes a coupling/passenger region.** The tested architecture places the demanding capacity/lapse structure in the wormhole complex and leaves the mobile share with transport coupling, local matching, and passenger-region shaping.

5. **The exit pulse is the main stability signature.** Smooth finite ramps produce finite diagnostic pulses. Pulse size grows with faster release, narrower wall support, and timing overlap between transport and fading lapse support.

## Evaluation priorities for the next stability pass

The present test is a radial/spherical reduced model. The next stability pass should extend the same exit logic through:

- a velocity ladder centered on `V = 1.01`, `1.1`, `1.25`, and `1.5`, with `V = 2.0` retained as the stress anchor;
- position-triggered release profiles `E(L)` and `q(L)`, so the exit is encoded as a prepared layer rather than a global time command;
- domain-of-dependence checks showing that the exit taper lies in the causal past of the release region from the infrastructure side;
- tidal-frame diagnostics along representative passenger geodesics;
- particle accumulation and release diagnostics inspired by McMonigal, Lewis, and O’Byrne;
- semiclassical stress-energy sensitivity around the front/exit layer, using the Finazzi-Liberati-Barceló result as the reference concern.

The key design principle remains fixed: the wormhole complex is the control system, and the mobile bubble share is the transit-coupled passenger region.

## Run artifacts

- Code: `ansatz_throat_exit_scan.py`
- Staged-exit code wrapper: `run_staged_exit.py`
- Synchronized results: `ansatz_throat_exit_results.json`
- Synchronized summary: `ansatz_throat_exit_summary.json`
- Staged results: `ansatz_throat_exit_staged_results.json`

## References

[^morris_thorne]: Michael S. Morris and Kip S. Thorne, “Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity,” *American Journal of Physics* 56, 395 (1988). https://www.pas.rochester.edu/~tim/introframe/AmJPhysBlackHoles.pdf

[^alcubierre]: Miguel Alcubierre, “The warp drive: hyper-fast travel within general relativity,” *Classical and Quantum Gravity* 11, L73 (1994). https://arxiv.org/abs/gr-qc/0009013

[^bobrick_martire]: Alexey Bobrick and Gianni Martire, “Introducing Physical Warp Drives,” *Classical and Quantum Gravity* 38, 105009 (2021). https://arxiv.org/abs/2102.06824

[^vdb]: Chris Van Den Broeck, “A ‘warp drive’ with more reasonable total energy requirements,” *Classical and Quantum Gravity* 16, 3973 (1999). https://arxiv.org/abs/gr-qc/9905084

[^pfenning_ford]: Michael J. Pfenning and L. H. Ford, “The unphysical nature of ‘Warp Drive’,” *Classical and Quantum Gravity* 14, 1743 (1997). https://arxiv.org/abs/gr-qc/9702026

[^everett_roman]: Allen E. Everett and Thomas A. Roman, “A Superluminal Subway: The Krasnikov Tube,” *Physical Review D* 56, 2100 (1997). https://arxiv.org/abs/gr-qc/9702049

[^krasnikov]: Serguei V. Krasnikov, “Hyperfast Interstellar Travel in General Relativity,” *Physical Review D* 57, 4760 (1998). https://arxiv.org/abs/gr-qc/9511068

[^lobo_review]: Francisco S. N. Lobo, “Exotic solutions in General Relativity: Traversable wormholes and ‘warp drive’ spacetimes,” arXiv:0710.4474 (2007). https://arxiv.org/pdf/0710.4474

[^finazzi]: Stefano Finazzi, Stefano Liberati, and Carlos Barceló, “Semiclassical instability of dynamical warp drives,” *Physical Review D* 79, 124017 (2009). https://arxiv.org/abs/0904.0141

[^mcmonigal]: Brendan McMonigal, Geraint F. Lewis, and Philip O’Byrne, “The Alcubierre Warp Drive: On the Matter of Matter,” *Physical Review D* 85, 064024 (2012). https://arxiv.org/abs/1202.5708
