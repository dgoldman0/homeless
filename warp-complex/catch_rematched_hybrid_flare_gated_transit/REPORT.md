# Catch-Rematched Hybrid Flare-Gated Transit: Engineering Complexity Shift Evaluation

## Executive statement

This bundle evaluates what changes when the **Catch-rematched throat-loaded transit design** is placed inside the control vocabulary of the **Hybrid Flare-Gated Reduced Reference Model v1.0**.

The combined design makes a concrete engineering shift:

```math
\text{passively comfortable traversable throat}
\quad\longrightarrow\quad
\text{active throat infrastructure carrying a protected service packet}.
```

Under the stated premise that the required null-violating or otherwise exotic support can be supplied, the combined system makes progress by narrowing the passenger-protection target. The v1 wormhole design makes the open throat itself behave like a usable passage. The combined design makes the throat behave like an active rail, launch, catch, and rematch apparatus. The passenger criterion belongs to a finite packet worldtube rather than to every infrastructure observer in the throat complex.

The reduced tests in this bundle establish the following engineering classification.

| Element | Engineering role in the combined system |
|---|---|
| Throat-gated shift | Hard packet-protection gate |
| Catch before shift fade | Hard packet-protection gate |
| Shift fade before throat relaxation | Hard packet-protection gate |
| Support-edge containment | Hard high-stress gate |
| `B` prestretch | Ride-quality and burden-smoothing actuator |
| `R` flare/access gating | Geometry, angular-tidal, flare-shape, and source-shaping actuator |
| `N` shoulder/lapse shaping | Margin and matching actuator |
| Quiet access hold | Shortenable service interval; not a passive-comfort requirement |
| `W^{p_\beta}` edge shift reinforcement | Edge-cleanup tool; not a substitute for catch timing |

The hard result is that **catch/rematch choreography protects the passenger packet more directly than passive throat quietness does**.

## Source premise and scope

This report assumes source availability. It does not claim that a physically admissible quantum or semiclassical source has been constructed. It evaluates engineering structure after the support problem has been made available as an input.

The evaluation remains a reduced screen. It is not a full `3+1` constraint solve, a quantum-source construction, or a stability evolution. Its value is in sorting the v1 gates into packet-essential gates and infrastructure-shaping gates.

## Input designs

### Hybrid Flare-Gated Reduced Reference Model v1.0

The v1 reference model uses the spherically symmetric metric family

```math
ds^2=-N(l,t)^2dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The v1 role allocation is:

```math
B: \text{ radial support dilution},
\qquad
R: \text{ flare/access-state gating},
\qquad
N: \text{ timing, shoulder matching, redshift shaping}.
```

The v1 model freezes a complete reduced lifecycle:

```math
\text{flattened }R\text{ standby}
\rightarrow B\text{ prestretch}
\rightarrow R\text{ flare opening}
\rightarrow \text{quiet access hold}
\rightarrow R\text{ closure}
\rightarrow \text{hybrid repayment / shoulder matching}
\rightarrow B\text{ reset}.
```

Its source architecture separates an NMC-like support component, infrastructure repayment, and shoulder/matching components. Its flux-completed full-cycle ledgers clear unity for the core, access, support, support-ring, and shoulder observer families. Its active physics gate remains quantum-source admissibility, with the Lorentzian sampled-stress proxy still carrying negative margins. [v1-reference-model]

### Catch-rematched throat-loaded transit design

The catch-rematched transit design uses the ADM separation

```math
 ds^2=-T^2dt^2 + A^2\left(dl+\beta^l dt\right)^2 + A^2r(l)^2d\Omega^2,
```

with throat-loaded capacity and lapse,

```math
 A=\exp\!\left(qW\ln C_0\right),
 \qquad
 T=\exp\!\left(qW\ln(\lambda C_0)\right),
```

and a catch-rematched, throat-gated transport shift,

```math
 \beta^l(l,t)=-U(t)E(X(t))W(l)S(l-X(t)).
```

The core choreography is:

```math
\text{catch }U(t)
\quad\rightarrow\quad
\text{fade transport }E(t)
\quad\rightarrow\quad
\text{relax throat support }q(t).
```

The design uses the throat complex as active infrastructure. The mobile share is the protected passenger/coupling packet. [catch-rematched-paper]

The prior gated-shift reduced evaluation established the architectural rule:

```math
\operatorname{supp}(\beta^l)
\subseteq
\operatorname{supp}(A,T).
```

In that evaluation, independent passenger shift produced many lapse-shift balance crossings, while throat-gated shift cleared the sampled configurations through the tested ladder. [throat-gated-evaluation]

## Composite ansatz used in the tests

The reduced composite screen treats the v1 geometry as infrastructure and the catch-rematched packet as the protected service region.

The working ADM form is

```math
 ds^2=-\alpha(l,t)^2dt^2
 +\gamma_{ll}(l,t)\left(dl+\beta^l(l,t)dt\right)^2
 +\gamma_{\Omega\Omega}(l,t)d\Omega^2.
```

The infrastructure-packet split is

```math
\alpha(l,t)=N_{\rm v1}(l,t)T_{\rm pkt}(l,t),
```

```math
\gamma_{ll}(l,t)=B_{\rm v1}(l,t)^2 A_\parallel(l,t)^2,
```

```math
\gamma_{\Omega\Omega}(l,t)=R_{\rm v1}(l,t)^2 A_\perp(l,t)^2,
```

```math
\beta^l(l,t)=-U(t)E(X(t))W_{\rm v1}(l,t)^{p_\beta}S(l-X(t)).
```

The protected packet is a finite worldtube,

```math
|l-X(t)|\le r_{\rm pkt}.
```

The hard passenger condition is the worldtube norm condition,

```math
g_{\mu\nu}\dot x^\mu_{\rm pkt}\dot x^\nu_{\rm pkt}<0,
```

not the stationary-observer condition alone,

```math
g_{tt}<0.
```

The stationary `gtt` diagnostic remains useful. It measures passive throat accessibility and support-edge safety. It is not identical to moving-packet safety.

## Evaluation files

The code used for this report is included in `code/`:

| File | Role |
|---|---|
| `code/composite_gate_ablation.py` | First composite gate-ablation harness |
| `code/composite_r_flare_gate_tests.py` | R-flare timing, smoothing, always-open, always-flat, and no-hold tests |
| `code/composite_extra_slim_and_edge_tests.py` | Slim architecture and `W^{p_\beta}` edge-gating tests |
| `code/build_report_tables.py` | Rebuilds compact derived tables from the JSON data |

The generated data is included in `data/`, and the compact derived tables are in `derived/`.

To rebuild the compact tables:

```bash
python code/build_report_tables.py
```

The raw JSON data files are the primary data artifacts:

| File | Content |
|---|---|
| `data/composite_gate_detailed_diagnostics.json` | Catch timing thresholds, failure states, and first ablations |
| `data/composite_r_flare_gate_tests.json` | R-flare gate variants across speed/lapse cases |
| `data/composite_extra_slim_and_edge_tests.json` | Slim architecture and edge-gating variants |

## Findings

### 1. Catch timing is the dominant packet-protection gate

The catch threshold screen held shift fade and throat relaxation fixed at

```math
x_\beta=0.70,
\qquad
x_q=1.25,
```

and varied the catch location `x_catch`.

| V | lambda | first packet fail `x_catch` | delta vs `x_beta` | first passive packet `gtt` fail | first edge `gtt` fail |
|---:|---:|---:|---:|---:|---:|
| 5 | 3 | 0.65 | -0.05 | -0.20 | none |
| 5 | 5 | 0.70 | 0.00 | none | none |
| 10 | 6 | 0.60 | -0.10 | -0.20 | 0.90 |
| 10 | 11.5 | 0.60 | -0.10 | none | none |

The engineering statement is:

```math
x_{\rm catch}<x_\beta<x_q
```

with real separation at high speed or low lapse margin.

Late catch produces packet-worldtube failure. At `V=10`, `lambda=6`, late catch after shift fade produced a packet max norm of `1.07e5`, and late catch after throat relaxation produced `4.46e5`. The baseline remained timelike with packet max norm `-0.75`.

### 2. Passive `gtt` and packet timelikeness are different tests

At reduced lapse margin, passive packet-region `gtt` can fail while the moving packet remains timelike. This is the central distinction introduced by the combined design.

```math
g_{tt}>0
```

marks a passive stationary-observer problem.

```math
g_{\mu\nu}\dot x^\mu_{\rm pkt}\dot x^\nu_{\rm pkt}>0
```

marks a packet failure.

The reduced data shows cases where passive `gtt` fails and the packet max norm remains `-0.75`. The active-rail architecture therefore uses packet timelikeness, packet-boundary tidal bounds, and support-edge containment as the primary passenger criteria.

### 3. R-flare gating is a geometry and ride-quality actuator in the combined design

The R-flare screen tested baseline `R` fade, early fade, delayed fade, always-open, always-flat, half-amplitude, sharp release, slow release, and no-hold variants.

Across the tested cases, R-flare variants did not create packet-worldtube failure when the catch/shift/relax ordering remained intact. Representative results:

| Case | R variant | packet fail | passive `gtt` fail | packet max norm | min flare `d2` | packet angular tidal ratio |
|---:|---|---:|---:|---:|---:|---:|
| `V=5`, `lambda=5.75` | baseline R fades with q | false | false | -0.75 | 5.63 | 1.00 |
| `V=5`, `lambda=5.75` | R always open | false | false | -0.75 | 2.74 | 0.996 |
| `V=5`, `lambda=5.75` | R always flat | false | false | -0.75 | 4.97 | 1.05 |
| `V=5`, `lambda=5.75` | R sharp release | false | false | -0.75 | 4.97 | 3.62 |
| `V=10`, `lambda=11.5` | R always open | false | false | -0.75 | 2.74 | 0.997 |
| `V=10`, `lambda=11.5` | R sharp release | false | false | -0.75 | 4.97 | 3.28 |

The engineering statement is:

```math
R\text{-flare gating is demoted from a hard packet-causal gate to a smooth infrastructure shape actuator.}
```

Smoothness remains important. Sharp R release inflated the packet-boundary angular tidal proxy by roughly `3.28x` to `4.04x` across the tested speed/lapse cases. Slow R release preserved packet timelikeness and improved the sampled flare-strength proxy.

R always open is a strong active-rail simplification. It preserved packet timelikeness in the tested baseline cases. R always flat also preserved packet timelikeness in the reduced screen, but it changes the throat geometry strongly and drove the no-hold flat-case flare proxy down to `0.22`. The preferred simplification is therefore **smooth R-open or gently relaxed R**, not aggressive flattening.

### 4. B-prestretch is a smoothing actuator

The first ablation shows that removing `B` prestretch does not produce packet timelike failure in the reduced screen. It does increase packet-boundary ride-quality proxies.

| V | no-B packet-boundary radial tidal ratio | no-B packet-boundary Kretschmann ratio |
|---:|---:|---:|
| 2.5 | 2.51 | 6.08 |
| 5 | 2.56 | 6.31 |
| 10 | 2.61 | 6.56 |

The engineering statement is:

```math
B\text{ is kept as support-dilution and ride smoothing, not as a binary packet-causal gate.}
```

### 5. N-shoulder shaping is a matching and margin actuator

Removing `N` shoulder/lapse shaping did not break packet timelikeness in the reduced tests. Its effects were comparatively modest, around `1.02x` to `1.03x` at the packet boundary and about `1.05x` support-edge tidal ratio in the first ablation.

The engineering statement is:

```math
N\text{ is retained for margin, timing, and support-edge matching.}
```

### 6. Quiet access hold is shortenable

The active-rail design does not require a long passive quiet throat interval. The reduced tests show that the quiet hold can be shortened when the catch/shift/relax order and lapse margin are maintained.

The high-stress case demonstrates the service-margin rule. At `V=10`, `lambda=6`, a completely collapsed no-hold variant can fail, while a short-hold slim architecture remains safe.

| Case | packet fail | passive `gtt` fail | packet max norm |
|---|---:|---:|---:|
| `V=10`, `lambda=6`, slim short-hold R-open half-B half-N | false | true | -0.75 |
| `V=10`, `lambda=6`, very slim no-hold R-open no-B no-N | true | true | 498 |
| `V=10`, `lambda=11.5`, very slim no-hold R-open no-B no-N | false | false | -0.749 |

The engineering statement is:

```math
\text{quiet hold becomes service separation, not passive passenger comfort.}
```

### 7. Edge shift reinforcement is not a substitute for catch timing

The tests swept

```math
\beta^l\propto W^{p_\beta},
\qquad
p_\beta\in\{1,1.25,1.5,2,3,4\}.
```

Under correct catch ordering, stronger edge gating preserves packet safety. Under late catch, stronger edge gating increases the packet norm failure because the still-fast packet loses shift support at the edge.

At `V=10`, `lambda=6`, late catch at beta gave:

| `p_beta` | packet fail | packet max norm |
|---:|---:|---:|
| 1 | true | `9.91e3` |
| 2 | true | `1.86e4` |
| 4 | true | `3.78e4` |

The engineering statement is:

```math
W^{p_\beta}\text{ cleans the edge after correct choreography; it does not replace choreography.}
```

## Complexity shift

The combined system shifts complexity in a productive direction.

### Before: passive traversable throat

The standalone v1 target asks the wormhole throat to function as a broadly safe passage. That pushes engineering effort into passive quietness, full observer-family ledgers, flare gating, support-ring repayment isolation, shoulder matching, and global lifecycle smoothing.

### After: active service packet through managed infrastructure

The combined target assigns the high-burden functions to the throat complex and assigns passenger safety to the protected packet.

```math
\text{whole throat comfortable}
\quad\longrightarrow\quad
\text{packet timelike + edge contained + catch/rematch ordered}.
```

The throat may be dynamically active. The passenger packet remains protected. Infrastructure observers and shoulder/support-ring regions continue to matter for source accounting, stability, and repeated operation, but they are not all passenger-comfort observers.

## Comparison with existing literature

### Wormhole literature

Morris and Thorne define the traversable-wormhole problem as a geometry with flare-out, redshift, and traversability conditions, together with exotic support requirements [MorrisThorne1988]. Ford and Roman show that quantum inequalities strongly constrain negative-energy magnitude and duration in macroscopic traversable wormhole geometries [FordRoman1996]. Hochberg and Visser show that energy-condition pressure remains local to the throat even for dynamic wormholes [HochbergVisser1998]. Barceló and Visser show how nonminimally coupled scalar fields can violate standard energy conditions, including ANEC, under specific classical-field conditions [BarceloVisser2000]. Gao, Jafferis, and Wall give a controlled holographic mechanism in which negative averaged null energy makes an Einstein-Rosen bridge traversable [GaoJafferisWall2017].

The present work does not remove those source constraints. It keeps source availability as the premise. It contributes an engineering distinction inside that premise: the passenger-protection criterion is localized to a packet worldtube instead of being assigned to the whole throat.

### Warp-drive and infrastructure literature

Alcubierre introduced the superluminal warp geometry [Alcubierre1994]. Pfenning and Ford applied quantum-inequality restrictions to the warp-drive setting and found severe wall-thickness and energy constraints [PfenningFord1997]. Van den Broeck introduced a compact-exterior, large-interior capacity concept [VanDenBroeck1999]. Bobrick and Martire describe warp drives using an ADM role separation in which lapse, shift, and spatial geometry carry distinct physical roles [BobrickMartire2021]. Everett and Roman identify a control problem for an observer at the center of an Alcubierre-type bubble and analyze a Krasnikov-tube infrastructure response [EverettRoman1997].

The present work takes those ideas into a combined gate architecture. It shows how the wormhole throat can carry capacity, lapse, shift support, release timing, and catch. This makes the warp-side share a coupling/passenger packet rather than a self-contained moving wall that must control itself.

## What this work makes clear beyond the literature alone

The available literature supplies the constraint map: wormholes need null-violating support, quantum inequalities constrain negative energy, dynamic throats keep local energy-condition pressure, warp bubbles have severe source and control issues, and infrastructure geometries can move control off the passenger craft.

This evaluation adds a concrete reduced engineering map:

1. **The hard passenger gate is packet timelikeness, not passive stationary-observer `gtt` everywhere.**
2. **Catch-before-release is a quantitative timing condition.** The threshold scans show real separation is required at high speed and low lapse margin.
3. **Throat-gated shift is the central architecture rule.** The shift belongs under the same support profile that carries lapse and capacity.
4. **R-flare gating is demoted for passenger safety and retained for smooth geometry.** It shapes angular tides, flare strength, and source/expansion proxies.
5. **B and N become infrastructure actuators.** They smooth burden and preserve margins rather than defining binary passenger feasibility.
6. **Quiet access hold becomes service separation.** The combined system requires enough time to catch, fade shift, and relax support; it does not require a passive open tunnel interval.
7. **Edge reinforcement is secondary.** `W^{p_beta}` is useful after correct ordering and harmful as a substitute for catch timing.

This gate classification is not explicit in Morris-Thorne, Ford-Roman, Alcubierre, Krasnikov-tube, Van den Broeck, or Bobrick-Martire literature. It emerges from combining v1's infrastructure controls with the catch-rematched packet and testing the gates against packet-centered diagnostics.

## Current best reduced architecture

The reduced tests support this slim active-rail target:

```math
R:\text{ mostly open or gently relaxed, smooth transitions},
```

```math
B:\text{ moderate prestretch for smoothing and support dilution},
```

```math
N:\text{ moderate shoulder/lapse shaping for margin},
```

```math
\beta^l=-U(t)E(X(t))W(l)^{p_\beta}S(l-X(t)),
```

with the operating order

```math
\boxed{
\text{catch with margin}
\rightarrow
\text{fade shift}
\rightarrow
\text{relax throat}
}
```

and the protected condition

```math
\boxed{
g_{\mu\nu}\dot x^\mu_{\rm pkt}\dot x^\nu_{\rm pkt}<0
\quad\text{throughout the packet worldtube.}
}
```

## Gate status after this evaluation

| Gate | Status |
|---|---|
| Throat-gated shift | Hard architecture gate |
| Catch before shift fade | Hard packet gate |
| Shift fade before throat relax | Hard packet gate |
| Minimum catch/shift/relax separation | Hard at high speed or low lapse margin |
| Support-edge containment | Hard high-stress infrastructure gate |
| R-flare gating | Smooth geometry/source actuator |
| R sharpness control | Ride-quality gate |
| R always open | Supported slim simplification in reduced tests |
| R always flat | Over-aggressive simplification; changes throat geometry strongly |
| B prestretch | Support smoothing and tidal/Kretschmann reduction |
| N shoulder/lapse shape | Margin and matching control |
| Quiet access hold | Shortenable service interval |
| `W^{p_beta}` edge gating | Edge cleanup after correct choreography |

## Next engineering pass

The next compact pass should turn this reduced classification into a cleaner candidate ansatz:

1. Use R-open or slow-R-relax as the default active-rail geometry.
2. Retain moderate B and N shaping.
3. Enforce catch margin before shift fade.
4. Treat passive `gtt` as a station/infrastructure diagnostic and packet norm as the passenger diagnostic.
5. Add a source ledger that follows packet, catch layer, shift-release layer, support edge, and repayment region separately.
6. Move from reduced screens to constraint-quality initial data after the slim candidate is frozen.

## Reproducibility notes

The report values are taken from `derived/report_metrics.json` and `derived/report_tables.md`, both generated from the raw JSON data by:

```bash
python code/build_report_tables.py
```

The code that generated the raw JSON is included in `code/`. The raw JSON and human-readable summaries are included in `data/`.

## References

Repository sources:

- [v1-reference-model] Daniel S. Goldman, **Hybrid Flare-Gated Reduced Reference Model v1.0**, GitHub repository report: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/quantum-effects-engineering/hybrid_flare_gated_reduced_reference_model_v1_0/report/hybrid_flare_gated_reduced_reference_model_v1_0_report.md>
- [catch-rematched-paper] Daniel S. Goldman, **A Catch-Rematched Throat-Loaded Transit Ansatz for Numerical Relativity Testing**, GitHub LaTeX source: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/communication_paper/latex/main.tex>
- [throat-gated-evaluation] Daniel S. Goldman, **Throat-Loaded Transit Architecture: Gated-Shift Reduced Evaluation**, GitHub repository report: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/wormhole-burdened-complex/throat_loaded_gated_shift_full_evaluation_report.md>

Literature:

- [MorrisThorne1988] M. S. Morris and K. S. Thorne, “Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity,” *American Journal of Physics* 56, 395–412 (1988). DOI: <https://doi.org/10.1119/1.15620>.
- [MorrisThorneYurtsever1988] M. S. Morris, K. S. Thorne, and U. Yurtsever, “Wormholes, Time Machines, and the Weak Energy Condition,” *Physical Review Letters* 61, 1446–1449 (1988). DOI: <https://doi.org/10.1103/PhysRevLett.61.1446>.
- [Alcubierre1994] M. Alcubierre, “The warp drive: hyper-fast travel within general relativity,” *Classical and Quantum Gravity* 11, L73–L77 (1994). DOI: <https://doi.org/10.1088/0264-9381/11/5/001>.
- [FordRoman1996] L. H. Ford and T. A. Roman, “Quantum field theory constrains traversable wormhole geometries,” *Physical Review D* 53, 5496–5507 (1996). DOI: <https://doi.org/10.1103/PhysRevD.53.5496>.
- [PfenningFord1997] M. J. Pfenning and L. H. Ford, “The unphysical nature of ‘warp drive’,” *Classical and Quantum Gravity* 14, 1743–1751 (1997). DOI: <https://doi.org/10.1088/0264-9381/14/7/011>.
- [EverettRoman1997] A. E. Everett and T. A. Roman, “Superluminal subway: The Krasnikov tube,” *Physical Review D* 56, 2100–2108 (1997). DOI: <https://doi.org/10.1103/PhysRevD.56.2100>.
- [HochbergVisser1998] D. Hochberg and M. Visser, “The Null Energy Condition in Dynamic Wormholes,” *Physical Review Letters* 81, 746–749 (1998). DOI: <https://doi.org/10.1103/PhysRevLett.81.746>.
- [VanDenBroeck1999] C. Van Den Broeck, “A ‘warp drive’ with more reasonable total energy requirements,” *Classical and Quantum Gravity* 16, 3973–3979 (1999). DOI: <https://doi.org/10.1088/0264-9381/16/12/314>.
- [BarceloVisser2000] C. Barceló and M. Visser, “Scalar fields, energy conditions, and traversable wormholes,” *Classical and Quantum Gravity* 17, 3843–3864 (2000). DOI: <https://doi.org/10.1088/0264-9381/17/18/318>.
- [BobrickMartire2021] A. Bobrick and G. Martire, “Introducing Physical Warp Drives,” *Classical and Quantum Gravity* 38, 105009 (2021). DOI: <https://doi.org/10.1088/1361-6382/abdf6e>; arXiv: <https://arxiv.org/abs/2102.06824>.
- [GaoJafferisWall2017] P. Gao, D. L. Jafferis, and A. C. Wall, “Traversable wormholes via a double trace deformation,” *Journal of High Energy Physics* 2017, 151 (2017). DOI: <https://doi.org/10.1007/JHEP12(2017)151>.
