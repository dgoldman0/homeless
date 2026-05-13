# Catch-Rematched Throat-Rail Obstruction Screen

## Purpose

This bundle records a focused technical comparison motivated by Garattini and Zatrimaylov's wormhole–warp-drive correspondence [GZ2024]. Their result is the main prior-art foil for a naive hybrid: a localized Alcubierre-type warp drive trying to traverse a Morris–Thorne wormhole. The architecture studied here has a sharper object:

```math
\text{throat-supported shift rail}
+
\text{catch/rematched packet}
\rightarrow
\text{packet-centered active throat service} .
```

The working distinction is direct. A localized warp bubble crossing a throat carries an independent shell-like burden. A throat-supported shift rail makes the throat plant carry the shift inside the same support envelope that carries capacity and lapse. The packet is caught before the transport shift is faded, and throat relaxation follows after the packet-critical handoff.

## Closest prior-art comparison

Garattini and Zatrimaylov show that embedding a warp drive in a wormhole background requires a generalized Natário–Alcubierre setting with nonzero intrinsic spatial curvature. Their central no-go states that Alcubierre warp drives cannot traverse Morris–Thorne wormholes, while the no-go does not extend to spherically symmetric, nonlocalized warp drives [GZ2024].

The present screen frames the active-rail architecture as an engineered occupant of that distinction:

```math
\text{localized independent bubble crossing a throat}
\quad\leftrightarrow\quad
\text{GZ danger regime},
```

```math
\text{support-contained throat shift with packet catch/rematch}
\quad\leftrightarrow\quad
\text{active-rail candidate regime} .
```

The screen therefore compares the active rail against naive variants that model the obvious "put a warp bubble in a wormhole" idea.

## Reduced model

The reduced radial metric is written in ADM-like form:

```math
ds^2
=
-\alpha(s,l)^2 ds^2
+
\gamma_{ll}(s,l)
\left(dl+\beta^l(s,l)ds\right)^2
+
\gamma_{\Omega\Omega}(s,l)d\Omega^2 .
```

The stage-1 and stage-2 scripts use the radial sector. The radial null characteristic speeds are

```math
\frac{dl}{ds}
=
-\beta^l
\pm
\frac{\alpha}{\sqrt{\gamma_{ll}}}.
```

The active-rail support envelope is encoded by a throat support window `W(l)`, a packet support window `S(l-s)`, a catch profile, a shift-fade profile, and a throat-relaxation profile. The active rail uses

```math
\beta^l
=
-U(s)E(s)W(l)^{p_\beta}S(l-s)/B(s,l).
```

The naive independent-shift baseline removes the throat factor:

```math
\beta^l_{\rm naive}
=
-U(s)E(s)S(l-s)/B(s,l).
```

The no-catch baselines keep the packet fast through the handoff. The late-catch baseline delays catch to the shift-fade layer.

## Variants

| Variant | Meaning |
|---|---|
| `active_rail` | throat-gated shift with catch/rematch choreography |
| `catch_independent_shift` | catch/rematch with passenger-attached shift |
| `naive_independent_no_catch` | localized passenger shift with no catch/rematch |
| `naive_throat_gated_no_catch` | throat-gated shift with no catch/rematch |
| `late_catch_throat_gated` | throat-gated shift with catch delayed to the shift-fade layer |

The active-rail case encodes the service order:

```math
x_{\rm catch}<x_\beta<x_q .
```

For the included stress run,

```math
V=10,
\qquad
\lambda=6,
\qquad
x_{\rm catch}=0.05,
\qquad
x_\beta=0.70,
\qquad
x_q=1.25 .
```

## Stage 1: radial null-characteristic screen

Stage 1 launches radial null rays from a broad radial interval and integrates both null families through the service and cleanup window. The diagnostic checks ray ordering, near-zero null-speed samples, and final clearing.

| Variant | Min absolute null speed | Max near-zero fraction | Order preserved | Final radial range |
|---|---:|---:|---:|---:|
| `active_rail` | 0.0014876 | 0.000e+00 | true | [-5.15014, 5.15014] |
| `catch_independent_shift` | 0.0014876 | 0.000e+00 | true | [-5.15014, 5.15014] |
| `naive_independent_no_catch` | 1.297e-04 | 4.172e-04 | true | [-5.15014, 5.15014] |
| `naive_throat_gated_no_catch` | 4.567e-04 | 4.172e-04 | true | [-5.15014, 5.15014] |
| `late_catch_throat_gated` | 3.945e-04 | 2.086e-04 | true | [-5.15014, 5.15014] |


Stage 1 establishes that the tested variants clear the radial window without ray-order inversion. The active-rail branch preserves the bundle order and records no near-zero samples at the chosen threshold.

## Stage 2: packet/support-edge radial bundle screen

Stage 2 launches local radial null bundles from the packet/support-edge neighborhoods:

- leading packet edge at the positive support edge,
- trailing packet edge at the positive support edge,
- shift-fade layer at the support edge,
- throat-relax layer at the support edge,
- packet center at shift fade.

The diagnostic tracks bundle compression, near-zero null speeds, and ray-order preservation.

| Variant | Min absolute null speed in event bundles | Worst compression ratio | Order preserved | Most constraining event |
|---|---:|---:|---:|---|
| `active_rail` | 0.680795 | 0.81055 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |
| `catch_independent_shift` | 0.680795 | 0.81055 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |
| `naive_independent_no_catch` | 0.19296 | 0.48761 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |
| `naive_throat_gated_no_catch` | 0.195152 | 0.705065 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |
| `late_catch_throat_gated` | 0.59346 | 0.798626 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |


Stage 2 is the more relevant reduced obstruction screen. The active rail keeps a large null-speed margin in the local event bundles and preserves ray ordering. The naive independent no-catch branch records the strongest bundle compression and the lowest null-speed margin. The throat-gated no-catch branch improves the geometry over the independent no-catch baseline while retaining the service deficiency that the catch/rematch branch removes.

## Technical readout

The included data products are:

- `data/stage1_summary.json`
- `data/stage2_summary.json`
- `data/stage2_bundles.csv`

The most important reduced result is the event-bundle hierarchy:

```math
\text{active rail}
\quad\text{has larger event-bundle null-speed margins}
\quad\text{than the naive no-catch baselines} .
```

The active-rail branch also keeps event-bundle compression near unity in this reduced model. The naive independent no-catch branch concentrates the strongest compression at the packet/support-edge events.

## Interpretation

The session result is affirmative:

```math
\text{the throat-supported shift rail behaves as a different object}
\quad
\text{from a localized warp bubble crossing a throat} .
```

The reduced checks support the architectural distinction needed for a Garattini–Zatrimaylov comparison. The naive baseline models the localized shell-like idea. The active rail models support-contained transport with packet catch/rematch. In the included radial screens, the active rail clears the tested packet/support-edge bundle checks with better null-speed and compression behavior.

The result motivates a dedicated paper section or companion note:

1. State the Garattini–Zatrimaylov obstruction.
2. Show the naive independent-shift baseline as the relevant danger model.
3. Show the throat-gated no-catch variant as an intermediate.
4. Show the catch-rematched throat rail as the active-rail candidate.
5. Add curvature scaling and constraint-quality screens as the next validation tier.

## Scope and next validation tier

This bundle is a reduced radial causal screen. It supplies a tractable obstruction diagnostic and a reproducible code path. The next tier is:

```math
\text{radial null bundles}
\rightarrow
\text{curvature scaling at packet/support intersections}
\rightarrow
\text{global null maps}
\rightarrow
\text{constraint-quality initial data}
\rightarrow
\text{semiclassical stress screening} .
```

The immediate next code pass should add finite-difference curvature proxies around:

- packet leading/trailing edges,
- support edge,
- packet/support-edge intersections,
- catch layer,
- shift-fade layer,
- throat-relax layer.

## References

- [GZ2024] Remo Garattini and Kirill Zatrimaylov, “On the wormhole-warp drive correspondence,” *Journal of Cosmology and Astroparticle Physics* 2024(08):061, 2024. DOI: https://doi.org/10.1088/1475-7516/2024/08/061. arXiv: https://arxiv.org/abs/2401.15136.
- [EverettRoman1997] Allen E. Everett and Thomas A. Roman, “Superluminal subway: The Krasnikov tube,” *Physical Review D* 56, 2100–2108, 1997. DOI: https://doi.org/10.1103/PhysRevD.56.2100.
- [LoboVisser2004] Francisco S. N. Lobo and Matt Visser, “Fundamental limitations on ‘warp drive’ spacetimes,” *Classical and Quantum Gravity* 21, 5871–5892, 2004. DOI: https://doi.org/10.1088/0264-9381/21/24/011.
- [MorrisThorne1988] Michael S. Morris and Kip S. Thorne, “Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity,” *American Journal of Physics* 56, 395–412, 1988. DOI: https://doi.org/10.1119/1.15620.
- [FordRoman1996] L. H. Ford and Thomas A. Roman, “Quantum field theory constrains traversable wormhole geometries,” *Physical Review D* 53, 5496–5507, 1996. DOI: https://doi.org/10.1103/PhysRevD.53.5496.
- [BobrickMartire2021] Alexey Bobrick and Gianni Martire, “Introducing physical warp drives,” *Classical and Quantum Gravity* 38, 105009, 2021. DOI: https://doi.org/10.1088/1361-6382/abdf6e.
