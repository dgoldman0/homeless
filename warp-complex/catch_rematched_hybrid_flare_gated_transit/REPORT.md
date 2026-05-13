# Catch-Rematched Hybrid Flare-Gated Transit

## Engineering complexity map with source support supplied

Source support is supplied as an input. The evaluation maps the engineering structure that follows: a catch-rematched throat-loaded packet uses the hybrid flare-gated v1 wormhole controls as active transit infrastructure.

```math
\text{hybrid flare-gated throat infrastructure}
+
\text{catch-rematched throat-loaded service packet}
\rightarrow
\text{active rail/catch transit geometry}.
```

The combined design places passenger safety in the packet worldtube. The throat complex carries support, capacity, lapse, shift containment, catch timing, release timing, and recovery. The passenger/coupling packet rides through that infrastructure.

```math
\boxed{
\text{passenger safety}
=
\text{timelike protected packet}
+
\text{bounded packet tides}
+
\text{contained support edge}
+
\text{ordered catch/release choreography}
}
```

The hard design rule is:

```math
\operatorname{supp}(\beta^l)\subseteq\operatorname{supp}(A,T),
\qquad
x_{\rm catch}<x_\beta<x_q.
```

The passenger diagnostic is:

```math
g_{\mu\nu}\dot x^\mu_{\rm pkt}\dot x^\nu_{\rm pkt}<0.
```

## Gate map

| Element | Combined-design role |
|---|---|
| throat-gated shift | hard architecture gate |
| catch before shift fade | hard packet gate |
| shift fade before throat relaxation | hard packet gate |
| minimum catch/shift/relax separation | hard high-speed and low-lapse-margin gate |
| support-edge containment | hard high-stress infrastructure gate |
| `B` prestretch | support dilution, tidal smoothing, curvature smoothing |
| `R` flare/access control | smooth throat shape, angular tidal control, flare proxy control |
| `N` shoulder/lapse control | timing margin, shoulder matching, edge margin |
| quiet access hold | service separation interval |
| `W^{p_\beta}` edge reinforcement | edge cleanup after correct choreography |

## Hybrid flare-gated v1 infrastructure

The v1 model uses:

```math
ds^2=-N(l,t)^2dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The frozen v1 control allocation is:

```math
B:\text{ radial support dilution},
\qquad
R:\text{ flare/access-state control},
\qquad
N:\text{ timing, shoulder matching, redshift shaping}.
```

The v1 lifecycle is:

```math
\text{flattened }R\text{ standby}
\rightarrow
B\text{ prestretch}
\rightarrow
R\text{ flare opening}
\rightarrow
\text{quiet access hold}
\rightarrow
R\text{ closure}
\rightarrow
\text{hybrid repayment / shoulder matching}
\rightarrow
B\text{ reset}.
```

The v1 source architecture separates NMC-like support, infrastructure repayment, and shoulder/matching components. Its flux-completed full-cycle ratios clear unity across the monitored observer families. Its conservation residual is small. Its Lorentzian sampled-stress proxy identifies the remaining source-admissibility gate. [v1-reference-model]

| v1 observer family | Flux-completed full-cycle positive/negative ratio |
|---|---:|
| core line | 1.083 |
| access mean | 1.471 |
| support mean | 2.801 |
| support ring mean | 1.135 |
| shoulder mean | 1.130 |

```math
\max |\mathrm{residual}|/\max|T_{kk}|\simeq 5.701\times10^{-4}.
```

The combined design uses this v1 result as an infrastructure library. `B`, `R`, and `N` become active-rail actuators around a packet-centered transit criterion.

## Catch-rematched throat-loaded packet

The catch-rematched transit design uses an ADM radial-axis form:

```math
 ds^2=-T^2dt^2+A^2\left(dl+\beta^l dt\right)^2+A^2r(l)^2d\Omega^2.
```

The throat-loaded capacity and lapse are:

```math
 A=\exp\!\left(qW\ln C_0\right),
\qquad
 T=\exp\!\left(qW\ln(\lambda C_0)\right).
```

The shift is throat-gated and packet-localized:

```math
\beta^l(l,t)=-U(t)E(X(t))W(l)S(l-X(t)).
```

The choreography is:

```math
\text{catch }U(t)
\rightarrow
\text{fade transport }E(t)
\rightarrow
\text{relax throat support }q(t).
```

The catch-rematched paper reports clean passenger worldlines and clean dense `gtt` maps through the core range `V = 1.5, 2.0, 2.5` and the stretch range `V = 3, 5`; the deliberately extreme `V = 10` map develops a small off-center support-edge shoulder. [catch-rematched-paper]

## Gated-shift result used as an architectural rule

The prior throat-loaded evaluation compared independent passenger shift with throat-gated shift. The result fixes the support-inclusion rule:

```math
\operatorname{supp}(\beta^l)\subseteq\operatorname{supp}(A,T).
```

| Transport structure | Configurations | Exit positive `gtt` points | Traversal positive `gtt` points | Clean traversal-and-exit configurations |
|---|---:|---:|---:|---:|
| independent passenger shift | 336 | 134 | 220 | 100 |
| throat-gated shift | 336 | 0 | 0 | 336 |

The throat complex carries capacity, lapse, and shift support as one managed infrastructure system. The mobile object is the protected passenger/coupling packet. [throat-gated-evaluation]

## Composite ansatz evaluated

The reduced composite screen inserts the packet into the v1 infrastructure controls:

```math
ds^2=-\alpha(l,t)^2dt^2
+\gamma_{ll}(l,t)\left(dl+\beta^l(l,t)dt\right)^2
+\gamma_{\Omega\Omega}(l,t)d\Omega^2.
```

The infrastructure-packet split is:

```math
\alpha(l,t)=N_{\rm v1}(l,t)T_{\rm pkt}(l,t),
```

```math
\gamma_{ll}(l,t)=B_{\rm v1}(l,t)^2A_\parallel(l,t)^2,
```

```math
\gamma_{\Omega\Omega}(l,t)=R_{\rm v1}(l,t)^2A_\perp(l,t)^2,
```

```math
\beta^l(l,t)=-U(t)E(X(t))W_{\rm v1}(l,t)^{p_\beta}S(l-X(t)).
```

The packet is sampled over:

```math
|l-X(t)|\le r_{\rm pkt}.
```

The evaluated diagnostics are:

| Diagnostic | Measurement role |
|---|---|
| packet norm | passenger/coupling worldtube timelikeness |
| packet-boundary norm | service-packet boundary timelikeness |
| packet `gtt` | stationary-observer accessibility in the packet region |
| support-edge `gtt` | infrastructure edge containment |
| radial tidal proxy | axial ride-quality and radial curvature exposure |
| angular tidal proxy | R-flare smoothness and angular ride-quality |
| Kretschmann proxy | curvature concentration |
| flare `d2` proxy | sampled throat-shape/flare strength |
| edge `theta` proxy | support-edge expansion pulse behavior |

The observer split is:

```math
g_{tt}<0
\quad\text{for stationary infrastructure observers,}
```

```math
g_{\mu\nu}\dot x^\mu_{\rm pkt}\dot x^\nu_{\rm pkt}<0
\quad\text{for the moving protected packet.}
```

## Code and data representation

The report values are generated from the JSON outputs in `data/` by `code/build_report_tables.py`.

```bash
python code/build_report_tables.py
```

The evaluation code is:

| Path | Role |
|---|---|
| `code/composite_gate_ablation.py` | first composite gate-ablation harness |
| `code/composite_r_flare_gate_tests.py` | R-flare timing, smoothing, always-open, always-flat, and no-hold tests |
| `code/composite_extra_slim_and_edge_tests.py` | slim architecture and `W^{p_\beta}` edge-gating tests |
| `code/build_report_tables.py` | table builder from raw JSON outputs |

The primary data files are:

| Path | Content |
|---|---|
| `data/composite_gate_detailed_diagnostics.json` | catch thresholds, packet failures, first ablations |
| `data/composite_r_flare_gate_tests.json` | R-flare variants across speed/lapse cases |
| `data/composite_extra_slim_and_edge_tests.json` | slim architecture and edge-reinforcement cases |
| `derived/report_tables.md` | compact tables generated from the JSON files |
| `derived/report_metrics.json` | compact metrics generated from the JSON files |

## Result 1: catch timing sets the packet gate

The catch-threshold sweep fixed:

```math
x_\beta=0.70,
\qquad
x_q=1.25,
```

and varied `x_catch`.

| V | lambda | first packet fail `x_catch` | delta vs `x_beta` | first passive packet `gtt` trigger | first edge `gtt` trigger |
|---:|---:|---:|---:|---:|---:|
| 5 | 3 | 0.65 | -0.05 | -0.20 | — |
| 5 | 5 | 0.70 | 0.00 | — | — |
| 10 | 6 | 0.60 | -0.10 | -0.20 | 0.90 |
| 10 | 11.5 | 0.60 | -0.10 | — | — |

The gate is:

```math
\boxed{x_{\rm catch}<x_\beta<x_q}
```

with larger catch margin at high speed and low lapse margin.

At `V = 10`, `lambda = 6`:

| Case | Packet max norm |
|---|---:|
| baseline ordering | -0.75 |
| late catch after shift fade | `1.07e5` |
| late catch after throat relaxation | `4.46e5` |

The active-rail timing rule is:

```math
\text{catch first, shift fade second, throat relax third.}
```

## Result 2: stationary-observer and packet diagnostics separate

The low-lapse cases show stationary-observer `gtt` triggers while the moving packet remains timelike.

| Case | Stationary packet-region `gtt` | Moving packet norm | Packet max norm |
|---|---|---|---:|
| `V=5`, `lambda=3`, baseline ordering | triggered | clear | -0.75 |
| `V=10`, `lambda=6`, baseline ordering | triggered | clear | -0.75 |
| `V=10`, `lambda=6`, late catch after shift fade | triggered | failed | `1.07e5` |

The combined design assigns diagnostics by observer class:

```math
\text{stationary }g_{tt}:\text{ station and infrastructure accessibility,}
```

```math
\text{packet norm}:\text{ passenger/coupling safety.}
```

## Result 3: R-flare control is a smooth geometry actuator

The R-flare screen tested baseline R fade, early fade, delayed fade, always-open, always-flat, half-amplitude, sharp release, slow release, and no-hold variants.

Representative outputs:

| Case | R variant | Packet status | Stationary `gtt` status | Packet max norm | Min flare `d2` | Packet angular tidal ratio |
|---:|---|---|---|---:|---:|---:|
| `V=5`, `lambda=5.75` | baseline R fades with q | clear | clear | -0.75 | 5.63 | 1.00 |
| `V=5`, `lambda=5.75` | R always open | clear | clear | -0.75 | 2.74 | 0.996 |
| `V=5`, `lambda=5.75` | R always flat | clear | clear | -0.75 | 4.97 | 1.05 |
| `V=5`, `lambda=5.75` | R sharp release | clear | clear | -0.75 | 4.97 | 3.62 |
| `V=10`, `lambda=11.5` | R always open | clear | clear | -0.75 | 2.74 | 0.997 |
| `V=10`, `lambda=11.5` | R sharp release | clear | clear | -0.75 | 4.97 | 3.28 |

The R result is:

```math
R:\text{ smooth, mostly open, gently relaxed infrastructure shape control.}
```

R timing variants preserve packet timelikeness under correct catch/shift/relax ordering. R sharpness raises the packet-boundary angular tidal proxy. R always-open preserves the service packet in the tested baseline cases and changes the flare proxy. R always-flat preserves packet timelikeness in the reduced screen and changes the throat-shape target strongly; in no-hold variants, the flare proxy reaches `0.22`.

The combined-design R rule is:

```math
\boxed{\text{keep R smooth; use R for angular geometry and source-shape management.}}
```

## Result 4: B prestretch smooths tidal and curvature burden

The no-`B` ablation gives:

| V | no-B packet-boundary radial tidal ratio | no-B packet-boundary Kretschmann ratio |
|---:|---:|---:|
| 2.5 | 2.51 | 6.08 |
| 5 | 2.56 | 6.31 |
| 10 | 2.61 | 6.56 |

The B result is:

```math
B:\text{ support dilution, packet-boundary radial tidal reduction, curvature smoothing.}
```

`B` remains valuable as an infrastructure actuator because it materially lowers packet-boundary radial tidal and Kretschmann proxies.

## Result 5: N shoulder/lapse shaping supplies margin

The first ablation gives modest N-removal penalties:

| Diagnostic | N-removal scale |
|---|---:|
| packet-boundary tidal ratio | `1.02x` to `1.03x` |
| support-edge tidal ratio | about `1.05x` |
| support-edge Kretschmann ratio | about `1.10x` |

The N result is:

```math
N:\text{ timing, shoulder matching, lapse margin, support-edge margin.}
```

`N` supplies matching and edge discipline around the release layers.

## Result 6: quiet hold becomes service separation

The high-stress service-margin cases show the value of retaining a compact service interval:

| Case | Packet status | Stationary `gtt` status | Packet max norm |
|---|---|---|---:|
| `V=10`, `lambda=6`, slim short-hold R-open half-B half-N | clear | triggered | -0.75 |
| `V=10`, `lambda=6`, very slim no-hold R-open no-B no-N | failed | triggered | 498 |
| `V=10`, `lambda=11.5`, very slim no-hold R-open no-B no-N | clear | clear | -0.749 |

The quiet-hold result is:

```math
\text{quiet hold}\rightarrow\text{service separation for catch, shift fade, and throat relaxation.}
```

A short service interval supports clean choreography at high speed and low lapse margin.

## Result 7: edge reinforcement follows the choreography

The edge-reinforcement sweep used:

```math
\beta^l\propto W^{p_\beta},
\qquad
p_\beta\in\{1,1.25,1.5,2,3,4\}.
```

Correct catch ordering remains clear with stronger edge reinforcement. Late catch remains a packet failure, and stronger edge suppression raises the packet norm failure because the still-fast packet loses shift support near the edge.

At `V=10`, `lambda=6`, late catch at beta gives:

| `p_beta` | Packet status | Packet max norm |
|---:|---|---:|
| 1 | failed | `9.91e3` |
| 2 | failed | `1.86e4` |
| 4 | failed | `3.78e4` |

The edge-reinforcement result is:

```math
W^{p_\beta}:\text{ edge cleanup after correct catch timing.}
```

## Engineering complexity shift

The v1 model supplies a full reduced wormhole lifecycle. The combined design reorganizes that lifecycle around a moving service packet.

```math
\text{whole-throat lifecycle control}
\rightarrow
\text{packet-centered active-rail control}.
```

The combined engineering target is:

```math
\boxed{
\text{packet timelike}
+
\text{bounded packet tides}
+
\text{support edge contained}
+
\text{catch/shift/relax ordered}
}
```

The design jobs are:

| Control element | Active-rail job |
|---|---|
| `B` | smooth support burden and reduce packet-boundary tidal/Kretschmann proxies |
| `R` | maintain smooth throat shape and angular geometry through service |
| `N` | provide timing, shoulder matching, and lapse margin |
| quiet hold | provide service separation among catch, shift fade, and relax |
| repayment/shoulder infrastructure | support source accounting and repeated operation |
| packet shift | remain throat-gated and catch-rematched |
| packet worldtube | define passenger safety |

## Literature comparison

### Wormhole literature

Morris and Thorne establish the traversable-wormhole throat, flare-out, redshift, and exotic-support setting [MorrisThorne1988]. Morris, Thorne, and Yurtsever add the chronology engineering issue for separated mouths [MorrisThorneYurtsever1988]. Ford and Roman establish strong quantum-inequality restrictions on negative energy in traversable wormhole geometries [FordRoman1996]. Hochberg and Visser show that the null energy condition pressure remains local to the throat for dynamic wormholes [HochbergVisser1998]. Barceló and Visser give nonminimally coupled scalar mechanisms that can violate standard energy conditions under classical-field conditions [BarceloVisser2000]. Gao, Jafferis, and Wall provide a controlled holographic construction in which negative averaged null energy produces traversability [GaoJafferisWall2017].

The combined evaluation takes the supplied-source case and maps the engineering controls that follow: packet norm, catch timing, shift containment, edge containment, R smoothness, B smoothing, and N margin.

### Warp-drive and infrastructure literature

Alcubierre introduces the superluminal warp metric [Alcubierre1994]. Pfenning and Ford apply quantum-inequality restrictions to warp-drive walls and obtain severe wall-thickness and energy constraints [PfenningFord1997]. Van den Broeck introduces a compact-exterior, large-interior capacity idea [VanDenBroeck1999]. Bobrick and Martire emphasize the ADM role split among lapse, shift, and spatial geometry [BobrickMartire2021]. Everett and Roman analyze the Krasnikov-tube infrastructure response to warp-bubble control limitations [EverettRoman1997].

The combined evaluation implements the infrastructure idea inside a throat gate. The wormhole complex carries capacity, lapse, shift support, release timing, and catch. The warp-side share becomes the protected coupling packet.

## Added engineering clarity from the combined tests

The combined tests make these design facts explicit:

1. Passenger safety is the packet worldtube norm.
2. Stationary `gtt` is a station and infrastructure diagnostic.
3. Catch timing has a quantitative threshold relative to shift fade.
4. Throat-gated shift is the central support-inclusion rule.
5. `R` flare control is smooth geometry and angular-tidal shaping in the active-rail version.
6. `B` and `N` are infrastructure actuators with measurable ride and edge-margin effects.
7. Quiet access hold becomes service separation among catch, shift fade, and throat relaxation.
8. Edge reinforcement works after correct catch timing.

This classification gives a practical design map between the general literature constraints and a full numerical-relativity construction.

## Current reduced candidate architecture

The reduced tests support this candidate:

```math
R:\text{ mostly open or slowly relaxed with smooth transitions},
```

```math
B:\text{ moderate prestretch for support dilution and ride smoothing},
```

```math
N:\text{ moderate shoulder/lapse shaping for margin},
```

```math
\beta^l=-U(t)E(X(t))W(l)^{p_\beta}S(l-X(t)),
```

with operating order

```math
\boxed{
\text{catch with margin}
\rightarrow
\text{fade shift}
\rightarrow
\text{relax throat}
}
```

and protected condition

```math
\boxed{
g_{\mu\nu}\dot x^\mu_{\rm pkt}\dot x^\nu_{\rm pkt}<0
\quad\text{throughout the packet worldtube.}
}
```

## Gate status after evaluation

| Gate | Status |
|---|---|
| throat-gated shift | hard architecture gate |
| catch before shift fade | hard packet gate |
| shift fade before throat relaxation | hard packet gate |
| minimum catch/shift/relax separation | hard high-speed or low-margin gate |
| support-edge containment | hard high-stress infrastructure gate |
| R-flare control | smooth geometry/source actuator |
| R sharpness control | ride-quality gate |
| R always-open simplification | supported slim reduced target |
| R always-flat simplification | strong throat-geometry change |
| B prestretch | support smoothing and tidal/Kretschmann reduction |
| N shoulder/lapse shape | margin and matching control |
| quiet access hold | shortenable service interval |
| `W^{p_beta}` edge gating | edge cleanup after correct choreography |

## Next engineering pass

The next compact pass is:

1. Freeze an R-open or slow-R-relax active-rail candidate.
2. Retain moderate `B` and `N` shaping.
3. Encode a catch-margin rule before shift fade.
4. Track stationary `gtt` as a station/infrastructure diagnostic.
5. Track packet norm as the passenger diagnostic.
6. Add source ledgers for packet, catch layer, shift-release layer, support edge, and repayment region.
7. Move the slim candidate into constraint-quality initial-data construction.

## References

Repository sources:

- [v1-reference-model] Daniel S. Goldman, **Hybrid Flare-Gated Reduced Reference Model v1.0**, GitHub repository report: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/quantum-effects-engineering/hybrid_flare_gated_reduced_reference_model_v1_0/report/hybrid_flare_gated_reduced_reference_model_v1_0_report.md>
- [catch-rematched-paper] Daniel S. Goldman, **A Catch-Rematched Throat-Loaded Transit Ansatz for Numerical Relativity Testing**, GitHub LaTeX source: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/communication_paper/latex/main.tex>
- [throat-gated-evaluation] Daniel S. Goldman, **Throat-Loaded Transit Architecture: Gated-Shift Reduced Evaluation**, GitHub repository report: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/wormhole-burdened-complex/throat_loaded_gated_shift_full_evaluation_report.md>
- [gated-shift-code] Daniel S. Goldman, **ansatz_throat_loaded_gated_full_eval.py**, GitHub code: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/wormhole-burdened-complex/ansatz_throat_loaded_gated_full_eval.py>

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
