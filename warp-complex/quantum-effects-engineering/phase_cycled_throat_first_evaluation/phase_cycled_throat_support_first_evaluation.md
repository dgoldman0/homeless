# Phase-Cycled Throat Support: First Evaluation

## Purpose

This evaluation begins a new line of work: treating the quantum-effects burden of a traversable throat as an engineering-control problem. The prior throat-loaded catch-rematched architecture organized the classical geometry and moved the hard support into a reusable throat complex. The present question is narrower and upstream:

Can the throat support itself be operated in a phase-cycled way, with short negative-energy support intervals, repayment phases, and controlled breathing, so that the quantum-inequality pressure becomes a bounded plant constraint rather than a static exotic-material wall?

The result is a first reduced proxy, not a semiclassical proof. It tests whether the simplest static and dynamic throat models show a credible macroscopic operating envelope.

## Model family

The baseline throat is the zero-redshift radial Morris--Thorne-style geometry

```math
ds^2=-dt^2+dl^2+r(l)^2d\Omega^2,
\qquad
r(l)=\sqrt{r_0^2+l^2}.
```

At the throat, the static effective source proxy is

```math
\rho_0=-\frac{1}{8\pi r_0^2},
\qquad
\rho_0+p_l=-\frac{1}{4\pi r_0^2}.
```

The quantum-inequality proxy uses Lorentzian sampling,

```math
\int \rho(\tau)
\frac{\tau_0/\pi}{(\tau-\tau_c)^2+\tau_0^2}
\,d\tau
\geq
-\frac{3}{32\pi^2\tau_0^4}.
```

The dynamic throat probe replaces the fixed throat radius with a breathing envelope,

```math
R(l,t)=\sqrt{a(t)^2+l^2},
```

and evaluates effective Einstein-source proxies at the throat. The tested dynamic profiles include a static throat, smooth sinusoidal breathing, and sharp open-gate pulses.

## Stage 1: static throat and pulse train around a static mean

The static throat fails the local QI proxy at macroscopic scale. With a sampling time

```math
\tau_0=\eta r_0,
```

the ratio of required negative energy density to the allowed Lorentzian-sampled magnitude is

```math
\mathcal R_{QI}
=\frac{|\rho_0|}{3/(32\pi^2\tau_0^4)}
=\frac{4\pi}{3}\eta^4r_0^2.
```

The pass condition is

```math
\mathcal R_{QI}\leq 1.
```

The corresponding allowed throat radii are Planck-scale to submicroscopic even for very short sampling fractions:

| Sampling fraction `eta` | Maximum `r0` in Planck lengths | Maximum `r0` in meters |
|---:|---:|---:|
| 0.1 | 48.8603 | 7.897e-34 |
| 0.03 | 542.892 | 8.775e-33 |
| 0.01 | 4886.03 | 7.897e-32 |
| 0.003 | 54289.2 | 8.775e-31 |
| 0.001 | 488603 | 7.897e-30 |

For a one-meter throat,

```math
r_0\approx 6.19\times 10^{34}L_P,
```

the violation ratio remains enormous across the tested sampling fractions:

| Sampling fraction `eta` | QI ratio for 1 m throat |
|---:|---:|
| 0.1 | `1.60e66` |
| 0.03 | `1.30e64` |
| 0.01 | `1.60e62` |
| 0.003 | `1.30e60` |
| 0.001 | `1.60e58` |

A compensated pulse train placed around the same static mean does not change the conclusion. When the pulse period is short enough for the throat to see a smooth average, Lorentzian sampling windows also recover the sustained negative mean. When the period is long enough to hide the mean from some short samples, the throat no longer has a continuous static support envelope.

The static-pulse result is therefore clear:

```math
\text{pulse modulation around a static support requirement does not rescue a macroscopic static throat.}
```

## Stage 2: dynamic phase-cycled throat envelope

The dynamic test lets the throat participate in the cycle. The intent is to separate three phases:

```math
\text{brief support/open phase}
\rightarrow
\text{positive-energy repayment or compression phase}
\rightarrow
\text{reset/standby phase}.
```

This is a different idea from pulsing a source while demanding a static throat. The geometry itself is allowed to breathe through `a(t)`. The diagnostic asks whether this creates a usable open window while keeping the source and tidal proxies bounded.

The selected Stage 2 cases are summarized below.

| Case | min `a` | max `a` | strict `log10(L0max/Lp)` | max angular tidal proxy | max theta-product proxy | quasi-static open fraction |
|---|---:|---:|---:|---:|---:|---:|
| `static_a1` | 1.00 | 1.00 | -0.311 | 0.000 | 0.000 | 1.000 |
| `sin_eps0.05_om1` | 0.95 | 1.05 | -0.321 | 0.0526 | 0.0100 | 1.000 |
| `sin_eps0.1_om20` | 0.90 | 1.10 | 3.840 | 44.44 | 16.16 | 0.0175 |
| `sin_eps0.6_om5` | 0.40 | 1.60 | 2.482 | 37.50 | 56.24 | 0.0175 |
| `pulse_ac0.5_w0.02` | 0.50 | 1.00 | 1.650 | 8286.59 | 11438.83 | 0.00150 |
| `pulse_ac0.1_w0.02` | 0.10 | 1.00 | 0.376 | 47754.72 | 137113.81 | 0.00150 |

The dynamic cases can improve the strict local QI scale compared with the static throat. The improvement comes with a sharp trade: the throat becomes strongly dynamic, the usable quasi-static open fraction collapses, and the source/tidal proxies grow rapidly.

The most favorable sampled sinusoidal high-frequency case reaches

```math
\log_{10}(L_{0,max}/L_P)\approx 3.84,
```

while the quasi-static open fraction drops to about `0.0175` and the angular tidal proxy rises to about `44`. The sharper pulse cases produce natural repayment-like phases, but the cost appears as source and tidal spikes. The `pulse_ac0.5_w0.02` case reaches

```math
\log_{10}(L_{0,max}/L_P)\approx 1.65,
```

with an angular tidal proxy above `8.2e3` and a quasi-static open fraction near `0.0015`.

## Open-window scaling

A simple open-window estimate gives the same qualitative message. For a throat radius `r0`, the QI-limited open duration scales as

```math
T_{max}\sim(8\pi C_{QI})^{1/4}\sqrt{r_0},
\qquad
C_{QI}=\frac{3}{32\pi^2}.
```

For a one-meter throat, this gives

```math
T_{max}\approx 9.37\times 10^{-27}\ \mathrm{s},
```

while the light-crossing time is

```math
r_0/c\approx 3.34\times10^{-9}\ \mathrm{s}.
```

The ratio is about

```math
2.81\times10^{-18}.
```

So a simple open-then-repay gate has a QI-friendly open interval far shorter than a macroscopic traversal time.

## Interpretation

The first evaluation supports a sharp division between source organization and source viability.

Phase-cycling does organize the quantum-effects engineering problem. It gives the throat plant knobs: cycle frequency, open fraction, repayment timing, breathing amplitude, and source-ripple tolerance. These are meaningful control variables for a fixed infrastructure plant.

The same evaluation does not find a macroscopic operating envelope. Static support fails immediately. Pulsing around a static mean preserves the sampled negative average. Letting the throat breathe creates repayment-like structure, but the cases that improve the QI proxy move into violent dynamic behavior with tiny usable windows.

The current result is therefore:

```math
\boxed{\text{phase-cycled throat support is a useful engineering formulation, but the first reduced model does not produce a viable macroscopic throat window.}}
```

## Current status

The throat support problem remains upstream of the transport/catch layer. The catch-rematched hybrid architecture can make passage classically organized once a throat plant exists, but this first quantum-effects evaluation says the plant itself has no easy static or simple dynamic operating mode under the QI proxy.

The next meaningful refinement would avoid global throat breathing and test spatial separation:

```math
\text{support band}
\quad + \quad
\text{repayment/buffer band}
\quad + \quad
\text{protected access window}.
```

That would ask whether positive repayment can be routed through an infrastructure buffer while the passenger-accessible region remains inside a smoother effective envelope. The present evaluation does not demonstrate that possibility. It defines the next target.

## Reproducibility note

The associated scripts regenerate the CSV and JSON outputs included with this report. The bundle includes a verification manifest with SHA-256 checksums for the scripts and generated data files.
