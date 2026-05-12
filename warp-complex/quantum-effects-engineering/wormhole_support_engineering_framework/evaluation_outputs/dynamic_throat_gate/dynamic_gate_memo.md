# Dynamic-Throat Gate Prototype for Wormhole-Support Infrastructure

## Purpose

This bundle adds the dynamic-throat screening gate to the wormhole-support engineering framework.  The static benchmark phase showed that established wormhole and quantum-inequality literature can be mapped into support, access, integrated-burden, transition, and source-realism gates.  The present phase adds a time-dependent gate for candidates that use dynamic lapse, radial metric, or areal-radius control.

The engineering question is:

> When a candidate uses time dependence, does the throat remain a controlled access structure, or does the support burden move into null expansions, flux, extrinsic curvature, transition activity, or access-region tidal history?

The diagnostic target is the general spherically symmetric throat-control family

```math
ds^2=-N(l,t)^2dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The transport/catch/passenger layer remains outside this evaluation.

## Literature anchor

Hochberg and Visser developed a local definition of dynamic wormhole throats using marginally anti-trapped surfaces and null congruence expansions, emphasizing that time-dependent throats require local geometric diagnostics rather than static embedding intuition. They also showed that NEC violation remains generic at dynamic wormhole throats. Kuhfittig analyzed static and dynamic traversable wormhole geometries under Ford--Roman constraints and found that dynamic variants still keep weak-energy-condition violation as a central burden. Kar and Sahdev studied evolving Lorentzian wormholes with time-dependent scale factors and energy-condition behavior.

The dynamic gate used here follows that literature orientation: it promotes null expansions, flux, extrinsic curvature, and access-region history to first-class engineering diagnostics.

## Gate diagnostics

For the metric family above, the prototype computes:

```math
\theta_\pm = \frac{2}{R}\left(\frac{R_t}{N}\pm\frac{R_l}{B}\right),
```

radial null-contracted stress proxies,

```math
T_{kk}^{\pm}
=
\frac{1}{8\pi}
\left(
\frac{G_{tt}}{N^2}
+
\frac{G_{ll}}{B^2}
\pm
\frac{2G_{tl}}{NB}
\right),
```

orthonormal flux,

```math
T_{\hat t\hat l}=\frac{G_{tl}}{8\pi NB},
```

and zero-shift extrinsic-rate proxies,

```math
K^l{}_l=-\frac{B_t}{NB},
\qquad
K^\theta{}_{\theta}=-\frac{R_t}{NR}.
```

The screening categories are:

| Gate category | Meaning |
|---|---|
| `dynamic-gate-pass-prototype` | Dynamic diagnostics stay within the reduced quiet-access and shoulder thresholds. |
| `flux-or-extrinsic-curvature-limited` | Throat shape remains geometrically controlled, while dynamic radial stretching creates flux or radial extrinsic-curvature cost. |
| `access-quietness-failure` | Time dependence breaks the quiet access envelope through flux, rate, tidal, or expansion history. |
| `dynamic-throat-expansion-failure` | Null-expansion behavior at the throat itself becomes the dominant issue. |
| `transition-shoulder-limited` | Dynamic activity concentrates in the transition/shoulder region. |

## Tested cases

The prototype evaluates:

1. static baseline throat;
2. static `B=3` long-throat baseline;
3. adiabatic ramp-up of `B(l,t)`;
4. adiabatic ramp-down of `B(l,t)`;
5. slow periodic `B` breathing;
6. fast periodic `B` breathing;
7. sharp fast `B` wall;
8. core `R(l,t)` breathing comparison;
9. global scale-factor evolving comparison;
10. side `R` repayment with static `B=3`;
11. adiabatic `B` plus side `R`.

## Main findings

### 1. Static and quasi-static long-throat baselines pass the dynamic gate

The static baseline and static `B=3` long-throat cases produce near-zero throat expansion diagnostics and quiet access histories.  The long-throat case keeps the earlier local softening signal while adding no dynamic flux or extrinsic-curvature burden.

Representative rows:

| Case | Classification | Access quiet fraction | Throat expansion max | Access flux max | Access `K_l` max | Proper half-length max |
|---|---|---:|---:|---:|---:|---:|
| `static_baseline` | `dynamic-gate-pass-prototype` | 1.000 | ~0 | ~0 | ~0 | 1.73 |
| `static_B3_long_throat` | `dynamic-gate-pass-prototype` | 1.000 | ~0 | ~0 | ~0 | 4.51 |

### 2. Adiabatic dynamic `B(l,t)` preserves the throat-location structure while creating radial-rate and flux costs

The adiabatic ramp-up and ramp-down cases keep the throat expansion essentially zero, because `R(l,t)` remains quiet and the minimum areal radius stays fixed.  Their limiting terms are radial extrinsic curvature and small access flux.

This supports a useful gate distinction:

```math
\text{dynamic }B(l,t)\text{ can preserve the areal access throat}
```

while

```math
\text{dynamic }B(l,t)\text{ carries radial-rate and flux costs}.
```

The classification is `flux-or-extrinsic-curvature-limited`, not an expansion failure.

### 3. Periodic `B` control separates into slow and fast regimes

Slow `B` breathing produces a partial quiet-access history and moderate radial-rate cost. Fast `B` breathing produces large radial extrinsic curvature and larger access flux, with access quietness collapsing over most of the cycle.

| Case | Classification | Access quiet fraction | Access flux max | Access `K_l` max | Shoulder activity max |
|---|---|---:|---:|---:|---:|
| `slow_B_breathing` | `access-quietness-failure` | 0.456 | 0.00595 | 0.433 | 0.382 |
| `fast_B_breathing` | `access-quietness-failure` | 0.034 | 0.0714 | 5.19 | 4.59 |

The engineering implication is direct: dynamic radial stretching is best treated as adiabatic setup, shutdown, or low-frequency infrastructure adjustment. Fast periodic `B` actuation belongs in the stress-test category.

### 4. Core `R(l,t)` breathing triggers the cleanest dynamic-throat failure

The core areal-radius comparison case activates the throat expansion gate directly.  Its throat expansion reaches order unity, the access quiet fraction is zero, and the angular rate/tidal terms become the dominant access problem.

This strengthens the framework's control allocation:

```math
R(l,t)\text{ in the access core is a primary dynamic-throat gate variable,}
```

and therefore requires expansion, tidal, and access-window screening before any source-bookkeeping score is interpreted favorably.

### 5. Side `R` activity can remain compatible with a static long-throat access core

The `side_R_repayment_with_static_B3` case keeps the access core quiet while placing areal-radius activity in a shoulder/repayment band.  The shoulder activity approaches the chosen prototype threshold, which assigns the cost to transition management rather than to access-core failure.

This supports the subsystem allocation used in the broader framework:

```math
\text{access core: quasi-static support geometry}
```

```math
\text{side bands: repayment / buffer / transition-management activity}.
```

## Classification summary

| Classification | Count |
|---|---:|
| `dynamic-gate-pass-prototype` | 4 |
| `flux-or-extrinsic-curvature-limited` | 3 |
| `access-quietness-failure` | 3 |
| `dynamic-throat-expansion-failure` | 1 |

## Engineering interpretation

The dynamic gate adds the missing time-dependent screening layer to the framework.

The useful distinction is:

```math
\text{static }B(l):\text{ support dilution}
```

```math
\text{adiabatic }B(l,t):\text{ setup/shutdown candidate with flux/rate budget}
```

```math
\text{fast }B(l,t):\text{ access quietness and extrinsic-curvature limited}
```

```math
\text{core }R(l,t):\text{ null-expansion/tidal access gate}
```

```math
\text{side }R(l,t):\text{ repayment/shoulder management gate}
```

This makes the screening framework more general: a dynamic throat proposal can now be classified by the physical role of its time dependence rather than by a single energy-density score.

## How this fits the field-facing framework

The benchmark phase established that the static gates align with the known literature verdicts.  The dynamic gate adds the local-throat machinery needed for evolving proposals.  Together, they support a reusable screening sequence:

1. identify support, access, repayment, buffer, matching, and transition subsystems;
2. evaluate static support-core burden and integrated cost;
3. apply dynamic null-expansion, flux, and extrinsic-curvature gates to any time-dependent subsystem;
4. assign the remaining candidate to source-realism and null-contracted sampling tests.

The deliverable is an engineering screening method.  The physical constraints come from established wormhole and QI literature; the framework organizes those constraints into operational gates for hypothetical infrastructure design.

## Files

- `run_dynamic_throat_gate_eval.py` — generator script.
- `dynamic_gate_case_summary.csv` — full case diagnostics.
- `dynamic_gate_extract_table.csv` — compact readable result table.
- `dynamic_gate_time_digest.csv` — representative time histories.
- `dynamic_gate_summary.json` — metadata and high-level result.
- `manifest.json` — checksums.

## References

- D. Hochberg and M. Visser, "Dynamic wormholes, antitrapped surfaces, and energy conditions," *Physical Review D* **58**, 044021 (1998). DOI: 10.1103/PhysRevD.58.044021.
- D. Hochberg and M. Visser, "Null Energy Condition in Dynamic Wormholes," *Physical Review Letters* **81**, 746 (1998). DOI: 10.1103/PhysRevLett.81.746.
- P. K. F. Kuhfittig, "Static and dynamic traversable wormhole geometries satisfying the Ford-Roman constraints," *Physical Review D* **66**, 024015 (2002). DOI: 10.1103/PhysRevD.66.024015.
- S. Kar and D. Sahdev, "Evolving Lorentzian Wormholes," *Physical Review D* **53**, 722 (1996). DOI: 10.1103/PhysRevD.53.722.
