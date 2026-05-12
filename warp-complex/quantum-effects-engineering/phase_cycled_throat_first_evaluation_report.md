# Phase-Cycled Throat Support — First Reduced Evaluation

## Scope

This report starts a new line of work after the catch-rematched throat-loaded transit paper. The earlier geometry work treated the wormhole complex as a classical control system for capacity, lapse, shift, and passenger capture. The present report asks a different question:

> Can the quantum-energy support problem of a traversable throat be shaped into an engineering control problem, rather than treated as a static exotic-material requirement?

The test begins with the throat alone. The transport/catch layer is deliberately left out as the quantum-inequality pressure lands first on the throat support band. A transport profile may help passengers access a working throat, but it should not be asked to solve the throat's quantum support problem.

The working name for this direction is **phase-cycled throat support**, i.e. a throat-support architecture in which negative-energy support, positive-energy repayment, geometric ripple, and access timing are treated as coordinated phases of a controlled plant.

## Core idea

A static traversable wormhole needs sustained null-energy-condition violation at or near the throat. In a classical reduced model, that burden can be written as an effective source obtained from the Einstein tensor:

```math
T_{\mu\nu}^{\rm eff}=\frac{1}{8\pi}G_{\mu\nu}.
```

Quantum inequalities make the static picture severe. Negative energy can occur in quantum field theory, but an observer cannot sample a large negative energy density for an arbitrary duration. The engineering idea tested here is to replace a persistent support demand with a controlled cycle:

```math
\text{negative support phase}
\quad\rightarrow\quad
\text{positive repayment phase}
\quad\rightarrow\quad
\text{buffer / recovery phase}
\quad\rightarrow\quad
\text{access phase}.
```

The first evaluation separates two versions of that idea.

The first version keeps the throat static and pulses the source. This tests whether short negative pulses can impersonate a static exotic material while satisfying sampled-energy bounds.

The second version lets the throat itself become dynamic. This tests whether the geometry can participate in the source cycle by opening, breathing, repaying, and returning to an access condition.

## Stage A: static throat sampled-energy test

The baseline throat is the zero-redshift Morris--Thorne radial model:

```math
ds^2=-dt^2+dl^2+r(l)^2d\Omega^2,
\qquad
r(l)=\sqrt{r_0^2+l^2}.
```

At the throat, the effective static source is:

```math
\rho_0=-\frac{1}{8\pi r_0^2},
\qquad
\rho_0+p_l=-\frac{1}{4\pi r_0^2}.
```

The local Lorentzian-sampling proxy was:

```math
\int \rho(\tau)
\frac{\tau_0/\pi}{\tau^2+\tau_0^2}
\,d\tau
\geq
-\frac{3}{32\pi^2\tau_0^4}.
```

The sampling time was taken as a fraction of the throat radius:

```math
\tau_0=\eta r_0.
```

The resulting ratio between the required static negative density and the local sampling allowance is:

```math
\mathcal R_{\rm QI}
=
\frac{|\rho_0|}{3/(32\pi^2\tau_0^4)}
=
\frac{4\pi}{3}\eta^4 r_0^2.
```

The static proxy condition is:

```math
\mathcal R_{\rm QI}\leq 1.
```

The allowed radii remain near the Planck scale for the tested sampling fractions.

| Sampling fraction `eta` | Maximum `r0 / L_P` | Maximum radius in meters |
|---:|---:|---:|
| 0.1 | `4.886e1` | `7.897e-34` |
| 0.03 | `5.429e2` | `8.775e-33` |
| 0.01 | `4.886e3` | `7.897e-32` |
| 0.003 | `5.429e4` | `8.775e-31` |
| 0.001 | `4.886e5` | `7.897e-30` |

A one-meter throat has:

```math
r_0\approx6.19\times10^{34}L_P.
```

That places a smooth static macroscopic throat far outside the sampled-energy envelope. The gap is the expected Ford--Roman scale problem appearing in the cleanest reduced throat model.

## Stage A pulse-train result

The next static test added compensated negative and positive source phases while preserving the same average throat requirement. This is the simplest pulse version of phase-cycled support:

```math
\rho(t)=\rho_{\rm mean}
+\sum_n \rho^-_n(t)
+\sum_n \rho^+_n(t).
```

The pulse train exposes a direct fork.

| Pulse regime | Throat support seen by geometry | Sampled-energy behavior | Result |
|---|---|---|---|
| Fast carrier | Smooth averaged support | Broad sampling windows recover the negative mean | Same static QI problem |
| Slow carrier | Interrupted support | The negative average is less persistent | Static throat support is lost |

This is the first useful boundary. A pulse train that behaves like a static exotic material also inherits the static sampled-energy obstruction. A pulse train that improves the sampled-energy average stops behaving like static support.

That result motivates the dynamic test. The throat must participate in the control cycle if this direction is to remain viable.

## Stage B: dynamic breathing-throat test

The dynamic model lets the throat radius become a controlled envelope:

```math
R(l,t)=\sqrt{a(t)^2+l^2},
\qquad
ds^2=-dt^2+dl^2+R(l,t)^2d\Omega^2.
```

Here `a(t)` is the throat-control degree of freedom. The evaluation used smooth sinusoidal cycles and short open-gate pulses. The source was again read from the Einstein tensor:

```math
T_{\mu\nu}^{\rm eff}=\frac{1}{8\pi}G_{\mu\nu}.
```

The diagnostics tracked sampled energy, radial null projections, angular tidal proxies, expansion-product proxies, throat-rate severity through `|adot/a|`, and the fraction of time spent in a quasi-static open condition.

The dynamic model creates the desired source phases. Negative-support intervals and positive-repayment intervals appear naturally when the throat breathes. Some cases improve the strict sampled-energy proxy. The improvement arrives with strong classical cost: null-projection pulses, tidal pulses, expansion pulses, and small access windows.

| Case | Strict `log10(L0_max / L_P)` | Max radial null-projection proxy | Max angular tidal proxy | Max expansion-product proxy | Max `|adot/a|` | Quasi-static open fraction |
|---|---:|---:|---:|---:|---:|---:|
| static `a=1` | -0.31 | 2.0 | 0.0 | 0.0 | 0.0 | 1.000 |
| sinusoid `eps=0.1, Omega=20` | 3.84 | 91.36 | 44.44 | 16.16 | 2.01 | 0.017 |
| sinusoid `eps=0.6, Omega=5` | 2.48 | 87.50 | 37.50 | 56.25 | 3.75 | 0.017 |
| pulse `a_c=0.5, w=0.02` | 2.53 | `1.43e5` | `7.16e4` | `1.11e5` | 154.04 | 0.0015 |
| pulse `a_c=0.1, w=0.02` | 1.12 | `6.94e5` | `3.47e5` | `1.07e6` | 500.98 | 0.0005 |

The one-zone dynamic throat behaves like a strongly driven resonator. It can improve one sampled-energy metric by pushing the geometry into violent time dependence. The reportable result is the trade:

```math
\text{better sampled-energy bookkeeping}
\quad\Longleftrightarrow\quad
\text{stronger geometric ripple and smaller useful windows}.
```

## Passage-window estimate

A working gate needs an open window long enough for causal passage. The first evaluation used a crude open-window estimate:

```math
T_{\max}\sim (8\pi C_{\rm QI})^{1/4}\sqrt{r_0},
\qquad
C_{\rm QI}=\frac{3}{32\pi^2},
```

in Planck units. A light-crossing time scales as `r0`. The QI-friendlier open duration grows like `sqrt(r0)`, while the crossing time grows linearly with `r0`.

| Throat radius | Estimated QI open duration | Light-crossing time | Ratio |
|---:|---:|---:|---:|
| `1e-15 m` | `2.96e-34 s` | `3.34e-24 s` | `8.89e-11` |
| `1e-12 m` | `9.37e-33 s` | `3.34e-21 s` | `2.81e-12` |
| `1e-9 m` | `2.96e-31 s` | `3.34e-18 s` | `8.89e-14` |
| `1e-6 m` | `9.37e-30 s` | `3.34e-15 s` | `2.81e-15` |
| `1e-3 m` | `2.96e-28 s` | `3.34e-12 s` | `8.89e-17` |
| `1 m` | `9.37e-27 s` | `3.34e-9 s` | `2.81e-18` |
| `1e3 m` | `2.96e-25 s` | `3.34e-6 s` | `8.89e-20` |

This estimate is the sharpest practical boundary from the first evaluation. A simple whole-throat open-close cycle gives a QI-friendlier open phase that is far shorter than the throat light-crossing time at macroscopic scale.

## Engineering interpretation

Phase-cycled support gives useful engineering language even though the first one-zone models fail as operating designs.

The static throat test identifies the unsupported demand: a persistent negative-energy average across a macroscopic throat. The static pulse train shows that a high-frequency source carrier still returns that average to broad sampling windows. The dynamic breathing test supplies repayment phases, but the whole throat becomes the oscillator. The open-window estimate then shows that the simple access phase is too short for macroscopic passage.

The next design should stop treating the throat as one globally breathing object. The natural refinement is a multi-zone throat plant:

```math
\text{support band}
\quad + \quad
\text{repayment band}
\quad + \quad
\text{buffer region}
\quad + \quad
\text{protected passage island}.
```

The support band carries the flare-out burden. The repayment band handles positive-energy compensation. The buffer region absorbs flux and suppresses radiative coupling. The protected passage island is the region that remains smooth enough for access. A later transport/catch layer would synchronize passengers with low-ripple access phases rather than solving the source problem directly.

That architecture turns the quantum-effects question into a plant-control question: phase timing, spatial routing, buffer capacity, ripple amplitude, repayment delay, and access scheduling.

## Boundary established

The first evaluation establishes a firm boundary for this direction.

A smooth static macroscopic throat sits outside the sampled-energy envelope. A pulse train that averages into the same static support retains that obstruction. A single-zone breathing throat creates repayment structure, but its improvement comes with severe geometric ripple and extremely small access fractions. A simple globally pulsed or globally breathing throat does not provide a usable macroscopic operating mode in this reduced proxy.

The surviving next step is specific: test a **multi-zone phase-cycled throat plant**. The next model should spatially separate support, repayment, buffering, and access. It should track sampled energy for support observers, repayment/buffer observers, and candidate passage paths, while recording null expansions, tidal histories, horizon indicators, and source-flux proxies.

A meaningful improvement would look like a bounded phase schedule:

```math
\text{support phases maintain flare-out,}
```

```math
\text{repayment phases route away from the protected passage island,}
```

```math
\text{metric ripple along the accessible path remains inside causal and tidal margins.}
```

## Data products

This report summarizes the first reduced evaluation of phase-cycled throat support. The run products are:

- `stage1_static_wormhole_qi/`
  - static throat QI ratio sweep
  - allowed-radius table
  - compressed-band estimate
  - pulse-train Lorentzian sampling demonstration
  - summary metadata

- `stage2_dynamic_throat_qi/`
  - dynamic throat case summary
  - representative time series
  - Lorentzian sampling records
  - analytic open-window estimates
  - model notes

## References

M. S. Morris and K. S. Thorne, “Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity,” *American Journal of Physics* **56**, 395 (1988). This is the standard traversable-wormhole construction motivating the throat model and flare-out support requirement.

L. H. Ford and T. A. Roman, “Quantum field theory constrains traversable wormhole geometries,” *Physical Review D* **53**, 5496 (1996). This is the central quantum-inequality constraint source for macroscopic wormhole support.

M. J. Pfenning and L. H. Ford, “The unphysical nature of ‘warp drive’,” *Classical and Quantum Gravity* **14**, 1743 (1997). This applies quantum-inequality reasoning to warp-drive stress-energy and motivates the comparison between moving walls and fixed throat support.

L. H. Ford and T. A. Roman, “The quantum interest conjecture,” *Physical Review D* **60**, 104018 (1999). This motivates the repayment-phase language used in phase-cycled support.

C. J. Fewster and E. Teo, “Quantum inequalities and ‘quantum interest’ as eigenvalue problems,” *Physical Review D* **59**, 104016 (1999). This supports the interpretation of sampled-energy restrictions as constraints over sampling windows rather than instantaneous energy-density signs alone.
