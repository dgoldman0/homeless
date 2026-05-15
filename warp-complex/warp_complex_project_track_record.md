# Warp Complex Project Track Record

## What this document is

This document gives a standalone orientation to the `warp-complex` project: what question it began with, how the internal architecture changed, which folders contain the major artifacts, and what findings currently organize the work.

The chronology below is a best reconstruction from the present repository structure, generated reports, and project memory. The repository was assembled through manual uploads and iterative bundles, so the order is reconstructed from artifact roles, folder placement, and project progression.

## Project in one sentence

The project began as a question about whether compact warp-shell geometry could interface with a traversable wormhole throat, then developed into a packet-centered active-rail architecture in which the wormhole throat acts as the transport plant and the passenger or vehicle becomes a serviced packet.

The current public-facing FAQ states this pivot directly: the project moved from asking whether a wormhole-throat / warp-shell interface could work into asking what happens when the throat itself becomes the shift plant and the passenger becomes a packet.[^faq]

## Current repository map

The top-level `warp-complex` folder currently contains the following main nodes:[^repo_root]

| Folder or file | Role |
|---|---|
| [`compact_warp_shell_ansatz.md`](https://github.com/dgoldman0/homeless/blob/main/warp-complex/compact_warp_shell_ansatz.md) | base ADM ansatz joining a Morris-Thorne throat, Bobrick-Martire-style ADM warp structure, and Van den Broeck-style capacity factor |
| [`first-pass/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/first-pass) | earliest reduced diagnostic tests for determinant, curvature, causal balance, throat behavior, and null expansions |
| [`capacity-coupled-lapse/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/capacity-coupled-lapse) | `T = A` lapse-coupling tests and extended velocity scan |
| [`lambda-A-lapse-margin/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/lambda-A-lapse-margin) | `T = lambda A` lapse-margin tests and superluminal threshold scans |
| [`wormhole-burdened-complex/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/wormhole-burdened-complex) | throat-loaded/gated-shift branch and exit/traversal reduced evaluations |
| [`communication_paper/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/communication_paper) | catch-rematched throat-loaded transit paper bundle and evaluation outputs |
| [`catch_rematched_hybrid_flare_gated_transit/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/catch_rematched_hybrid_flare_gated_transit) | engineering-complexity bundle for catch-rematched transit on the hybrid flare-gated reference model |
| [`catch_rematched_hybrid_flare_gated_transit_paper/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/catch_rematched_hybrid_flare_gated_transit_paper) | standalone LaTeX/PDF paper package for the packet-centered active-rail architecture |
| [`active_rail_paper/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/active_rail_paper) | public paper bundle connecting the 2022 warp/wormhole question, Garattini-Zatrimaylov, and the throat-supported shift-rail architecture |
| [`active_rail_passenger_optics_radiation_analysis/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/active_rail_passenger_optics_radiation_analysis) | passenger optics, radiation, and propagation-oriented follow-up work |
| [`active_rail_source_analysis/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/active_rail_source_analysis) | Einstein-tensor/source-ledger analysis and post-paper source accounting |
| [`quantum-effects-engineering/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/quantum-effects-engineering) | wormhole-support engineering, phase-cycled throat tests, source-realism screens, and hybrid reference models |
| [`throat_loaded_transit_complex_engineering_concept.md`](https://github.com/dgoldman0/homeless/blob/main/warp-complex/throat_loaded_transit_complex_engineering_concept.md) | conceptual engineering summary for the throat-loaded transit complex |
| [`FAQ.md`](https://github.com/dgoldman0/homeless/blob/main/warp-complex/FAQ.md) | public orientation FAQ and source-family discussion |

## Reconstructed development track

### Phase 0 — The interface question

The starting question was whether a compact warp-drive spacetime could be embedded in or propagated through a traversable wormhole throat while preserving regularity, traversability, and controlled stress-energy behavior.

The public FAQ links this starting point to a 2022 inquiry and to Garattini and Zatrimaylov’s later wormhole/warp-drive correspondence result.[^faq] The repository’s current framing treats that literature result as the reason to move from a simple “warp bubble through a wormhole” image toward an engineered interface architecture.

### Phase 1 — Base compact warp shell / wormhole ansatz

The first concrete model is the file [`compact_warp_shell_ansatz.md`](https://github.com/dgoldman0/homeless/blob/main/warp-complex/compact_warp_shell_ansatz.md). It combines three ingredients:

1. a smooth Morris-Thorne wormhole in proper radial coordinate,
2. a Bobrick-Martire-style ADM warp-side decomposition,
3. a Van den Broeck-style compact-exterior / large-interior capacity factor.

The key move was the ADM separation:

```math
\alpha=e^{\Phi(l)}T,
\qquad
\gamma_{ij}=A^2q_{ij},
\qquad
\beta^i=-VS n^i.
```

This made the geometry diagnosable by role:

| ADM handle | Role |
|---|---|
| `A` | spatial capacity / compact-large interior mechanism |
| `T` | lapse / local time-rate and causal margin |
| `beta` | transport shift / carrying field |
| `r(l), Phi(l)` | wormhole throat flare, radius, redshift, and base support |

The base ansatz also fixed the diagnostic vocabulary used throughout the project: determinant/signature, curvature invariants, Einstein tensor projections, ADM constraints, throat-area behavior, lapse-shift balance, and null expansions.[^compact_ansatz]

### Phase 2 — First-pass reduced tests

The [`first-pass/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/first-pass) folder contains the earliest reduced computational triage: `ansatz_fast.py`, raw JSON results, and a report.[^first_pass]

The central result was that the naive moving compact-capacity shell with unit lapse has a severe lapse-shift balance constraint:

```math
g_{tt}=-1+A^2V^2S^2.
```

Large capacity `C0` and finite shift speed `V` quickly push the geometry toward the balance surface. The first-pass result therefore identified lapse support as a necessary partner to capacity support.

This phase also confirmed that compact capacity concentrates curvature in the shell wall through the same scaling visible in the ansatz:

```math
\nabla\ln A\sim\frac{\ln C_0}{\Delta},
\qquad
\Delta\ln A\sim\frac{\ln C_0}{\Delta^2}.
```

### Phase 3 — Capacity-coupled lapse, `T = A`

The [`capacity-coupled-lapse/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/capacity-coupled-lapse) folder contains the `T = A` scan code, raw extended-velocity JSON, summary JSON, and report.[^capacity_folder]

With `T = A`, the reduced causal diagnostic becomes:

```math
g_{tt}=A^2(-1+V^2S^2).
```

The speed threshold shifts from roughly `V ~ 1/C0` to the local condition `|V|S < 1`. The result established a clean subluminal branch and gave a physical interpretation: spatial capacity and local time-rate structure should scale together.

### Phase 4 — Lapse-margin branch, `T = lambda A`

The [`lambda-A-lapse-margin/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/lambda-A-lapse-margin) folder contains the `T = lambda A` branch: code, raw results, summary, and report.[^lambda_folder]

The compact-supported version used:

```math
T=A\lambda^S.
```

Inside the passenger region this behaves as:

```math
T\approx \lambda A.
```

The tested causal-margin rule was:

```math
|V|S<\lambda.
```

This phase showed that lapse margin can extend the moving-shell family into sampled superluminal regimes in the reduced model. It also kept the geometric burden visible in the moving wall, especially for high `C0`, narrow `Delta`, and high `V`.

### Phase 5 — Burden shift to the wormhole throat

The burden-shift idea became the first real architectural pivot. The working question changed from “can the moving shell carry the compact-large geometry through the wormhole?” to “can the fixed wormhole complex carry most of the geometry while the passenger becomes a coupling region?”

The throat-loaded branch placed capacity and lapse into the throat support profile:

```math
A(l,L)=\exp\left[q(L)W(l)\ln C_0\right],
```

```math
T(l,L)=\exp\left[q(L)W(l)\ln(\lambda C_0)\right].
```

The early exit/stability tests in [`wormhole-burdened-complex/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/wormhole-burdened-complex) showed that the throat could carry most of the burden proxy during traversal and exit, and that release ordering matters: shift support should fade while throat capacity/lapse support remains active.[^wormhole_burdened]

This phase made the “throat plant” idea concrete: the wormhole complex becomes the active controller, and the mobile object becomes a serviced passenger/coupling region.

### Phase 6 — Gated-shift turning point

The decisive refinement was the gated-shift evaluation in [`wormhole-burdened-complex/throat_loaded_gated_shift_full_evaluation_report.md`](https://github.com/dgoldman0/homeless/blob/main/warp-complex/wormhole-burdened-complex/throat_loaded_gated_shift_full_evaluation_report.md). The report states the architectural conclusion directly: the wormhole complex is the active control system; the mobile bubble share is a coupling/passenger region; the throat infrastructure manages shift, capacity, lapse, and release timing.[^gated_report]

The comparison was:

```math
\beta^l=-V E(L)S_{\rm pass}(l-L)
```

versus:

```math
\beta^l=-V E(L)W(l)S_{\rm pass}(l-L).
```

The second form keeps transport inside the throat-managed support region. This produced the hard support-inclusion rule:

```math
\operatorname{supp}(\beta^l)\subseteq\operatorname{supp}(A,T).
```

This is the project’s major engineering turn. Capacity and lapse support in the throat were a strong start; the shift also had to be throat-carried/gated. That changed the architecture from a moving warp shell with throat assistance into a throat-supported shift rail.

### Phase 7 — Catch/rematch and packet-centered transit

The next development was the catch/rematched packet framework. The `communication_paper/` bundle describes a standalone paper package with source snapshots and reduced-evaluation outputs for the catch-rematched throat-loaded transit ansatz.[^communication]

The catch/rematch phase reframed the passenger as a protected packet with its own timelike worldtube. The engineering question became service-order dependent: support the rail, carry the packet, catch/rematch the packet, fade the shift, relax the throat, reset.

The key service sentence is:

```text
prepare throat support -> carry packet -> catch packet -> fade shift -> relax throat
```

The expanded public mnemonic in the FAQ is:

```text
Support -> Carry -> Catch -> Fade -> Decompress -> Reset
```

The active-rail FAQ explains the packet-centered architecture in prose: the rail supplies the support envelope, carrying flow, synchronization environment, release conditions, and reset cycle, while the packet is the delivered payload moving through coordinated stages.[^faq]

### Phase 8 — Hybrid flare-gated active rail

The [`catch_rematched_hybrid_flare_gated_transit/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/catch_rematched_hybrid_flare_gated_transit) bundle evaluates how the catch-rematched throat-loaded packet changes the engineering complexity of the hybrid flare-gated reduced reference model.[^catch_bundle]

Its README describes a report-driven bundle with code, data, derived tables, and source notes. The report states the combined structure:

```math
\text{hybrid flare-gated throat infrastructure}
+
\text{catch-rematched throat-loaded service packet}
\rightarrow
\text{active rail/catch transit geometry}.
```

The paper version in [`catch_rematched_hybrid_flare_gated_transit_paper/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/catch_rematched_hybrid_flare_gated_transit_paper) packages the same architecture as a standalone LaTeX/PDF artifact.[^catch_paper_bundle]

The paper abstract reports that the frozen reduced candidate preserves packet and support-edge clearance, reduces ADM source-demand proxies relative to the reference geometry, and lowers Lorentzian-sampled packet current-floor exposure to about four percent of the reference value in the stressed source screen.[^catch_tex]

### Phase 9 — Active-rail synthesis

The [`active_rail_paper/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/active_rail_paper) bundle is the current synthesis node. Its README states the paper connects the 2022 exploratory question, Garattini and Zatrimaylov’s wormhole/warp-drive correspondence, and the throat-supported shift-rail / catch-rematched active-rail architecture.[^active_rail_readme]

The same README gives the concise architectural pivot:

> From bubble-through-throat imagery to throat-carried transport shift.

The reduced diagnostic in this bundle tests packet norm, stationary infrastructure diagnostics, radial null speeds, and packet/support-edge bundle compression in stressed service branches. Its next technical gates are constraint-quality initial data, off-axis global causal analysis, and semiclassical stress-tensor analysis.[^active_rail_readme]

## Major findings by theme

### 1. The ADM split was the enabling move

The base ansatz separated capacity, lapse, shift, and throat support. That allowed each burden to be tested separately:

| Question | Geometry handle |
|---|---|
| where does compact-large capacity live? | `A` |
| where does causal margin live? | `T` / lapse |
| where does transport live? | `beta` / shift |
| where does infrastructure support live? | `r(l), Phi(l), W(l)` |
| where does passenger safety live? | packet worldtube |

### 2. Unit lapse made the capacity-shell burden visible

The `T = 1` branch showed that spatial capacity alone produces a tight causal-balance condition. This result turned lapse support from an optional metric factor into a primary engineering channel.

### 3. `T = A` gave the first clean coupled branch

The `T = A` scan showed that space and time-rate scaling can be paired, producing a clean subluminal family in the reduced model.

### 4. `T = lambda A` gave a tunable margin rule

The `T = lambda A` branch produced the reduced rule:

```math
\lambda\ge |V|.
```

This made lapse margin an explicit engineering knob.

### 5. Throat-loading moved the main burden into the infrastructure

The throat-loaded branch moved `A` and `T` into a fixed throat profile. This changed the project’s physical picture: the wormhole becomes the high-burden megastructure, and the moving bubble becomes a lighter coupling/passenger region.

### 6. Gated shift created the throat plant

The support-inclusion rule:

```math
\operatorname{supp}(\beta^l)\subseteq\operatorname{supp}(A,T)
```

is the architectural turning point. The shift is a transport action performed by supported infrastructure.

### 7. Catch/rematch made passenger safety packet-centered

The architecture now treats the passenger as a packet whose worldtube is evaluated directly. This lets the support edge, release layer, shoulder, and reset region act as plant/infrastructure regions while packet safety is followed where the packet actually is.

### 8. Active rail became the public synthesis

The active-rail architecture is the current high-level form:

```text
Support -> Carry -> Catch -> Fade -> Decompress -> Reset
```

The rail prepares, carries, synchronizes, releases, relaxes, and resets as one coordinated geometric plant.[^faq]

## Reading guide for new visitors

### Quick conceptual route

1. Start with [`FAQ.md`](https://github.com/dgoldman0/homeless/blob/main/warp-complex/FAQ.md).
2. Read [`compact_warp_shell_ansatz.md`](https://github.com/dgoldman0/homeless/blob/main/warp-complex/compact_warp_shell_ansatz.md) for the initial ADM formulation.
3. Read [`wormhole-burdened-complex/throat_loaded_gated_shift_full_evaluation_report.md`](https://github.com/dgoldman0/homeless/blob/main/warp-complex/wormhole-burdened-complex/throat_loaded_gated_shift_full_evaluation_report.md) for the throat-plant turn.
4. Read [`communication_paper/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/communication_paper) for the catch-rematched throat-loaded ansatz paper bundle.
5. Read [`active_rail_paper/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/active_rail_paper) for the current public synthesis.

### Technical route

1. Review [`first-pass/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/first-pass) for the initial finite-parameter diagnostics.
2. Review [`capacity-coupled-lapse/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/capacity-coupled-lapse) and [`lambda-A-lapse-margin/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/lambda-A-lapse-margin) for causal-margin evolution.
3. Review [`wormhole-burdened-complex/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/wormhole-burdened-complex) for throat loading and gated-shift testing.
4. Review [`catch_rematched_hybrid_flare_gated_transit/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/catch_rematched_hybrid_flare_gated_transit) for packet/catch service testing against a hybrid flare-gated reference geometry.
5. Review [`active_rail_source_analysis/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/active_rail_source_analysis) for source-ledger and demanded-Einstein-tensor accounting.
6. Review [`quantum-effects-engineering/`](https://github.com/dgoldman0/homeless/tree/main/warp-complex/quantum-effects-engineering) for the source-realism and wormhole-support engineering background.

## Current status

The project has a coherent reduced architecture:

```text
throat-supported plant + support-contained shift + protected packet + ordered catch/release service
```

The best current rule set is:

```math
\operatorname{supp}(\beta^l)\subseteq\operatorname{supp}(A,T),
```

```text
Support -> Carry -> Catch -> Fade -> Decompress -> Reset.
```

The strongest reduced candidate uses the wormhole throat as active rail infrastructure. It carries support, capacity, lapse, shift containment, release timing, and reset. The passenger becomes a packet serviced by that infrastructure.

## Open technical gates

The repository already marks several next gates in its paper bundles and source-analysis folders:

| Gate | Purpose |
|---|---|
| Constraint-quality initial data | move from reduced ADM diagnostics to `3+1` initial-data consistency |
| Off-axis global causal analysis | test the geometry beyond radial-axis reductions |
| Semiclassical stress-tensor analysis | examine RSET/particle/radiation behavior in the active support and release layers |
| Full stress-energy ledger | compute and decompose demanded `T_{mu nu}` by observer channel, region, and service phase |
| Source-family integration | connect support/lapse/edge/reset burdens to plausible source sectors |
| Passenger optical/radiation histories | trace propagation, blueshift/redshift, particle accumulation, and release through service phases |

The current architecture is therefore best read as a source-supplied reduced engineering framework. It organizes the geometric burden and service order clearly enough to define the next numerical-relativity and source-realism work.

## Compact timeline

| Reconstructed stage | Main artifact | Main result |
|---|---|---|
| Interface question | FAQ / 2022 inquiry | asks whether warp-shell and wormhole geometries can combine productively |
| Base ansatz | `compact_warp_shell_ansatz.md` | ADM split identifies capacity, lapse, shift, throat response, null expansions |
| First-pass tests | `first-pass/` | unit lapse exposes lapse-shift balance and capacity wall concentration |
| Capacity-coupled lapse | `capacity-coupled-lapse/` | `T = A` creates clean subluminal coupled branch |
| Lapse margin | `lambda-A-lapse-margin/` | `T = lambda A` gives reduced rule `lambda >= |V|` |
| Throat loading | `wormhole-burdened-complex/` | capacity/lapse move into the throat plant |
| Gated shift | `throat_loaded_gated_shift_full_evaluation_report.md` | shift also belongs inside throat support, giving `supp(beta) subset supp(A,T)` |
| Catch/rematch | `communication_paper/` | packet service order becomes central to passenger protection |
| Hybrid active rail | `catch_rematched_hybrid_flare_gated_transit/` | catch-rematched packet uses hybrid flare-gated infrastructure |
| Public synthesis | `active_rail_paper/` | active rail replaces bubble-through-throat image with throat-supported shift rail |
| Source ledger | `active_rail_source_analysis/` | demanded source accounting becomes the main next engineering layer |

## Short conclusion

The project’s track record is a sequence of increasingly specific burden-allocation results. The early compact warp shell tried to carry capacity, lapse, and shift through a wormhole throat. The later throat-loaded branch moved capacity and lapse into the wormhole complex. The gated-shift evaluation moved the shift there too. The catch/rematched active-rail architecture then made the passenger a packet serviced by a throat-supported plant.

The current idea is simple in engineering language: build the difficult geometry into the fixed wormhole infrastructure, then carry a protected packet through it in a precise service order.

## References and source links

[^repo_root]: Top-level repository listing for `warp-complex`, showing the current folder map including `active_rail_paper`, `active_rail_source_analysis`, `capacity-coupled-lapse`, `catch_rematched_hybrid_flare_gated_transit`, `communication_paper`, `first-pass`, `lambda-A-lapse-margin`, `quantum-effects-engineering`, and `wormhole-burdened-complex`: <https://github.com/dgoldman0/homeless/tree/main/warp-complex>.

[^faq]: Project FAQ: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/FAQ.md>. The FAQ describes the starting 2022 question, the Garattini-Zatrimaylov context, the shift toward the throat as shift plant, and the packet-centered active-rail formulation.

[^compact_ansatz]: Base compact warp-shell / wormhole ansatz: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/compact_warp_shell_ansatz.md>. This file formulates the Morris-Thorne + Bobrick-Martire + Van den Broeck ADM family and defines the compatibility diagnostics.

[^first_pass]: First-pass reduced diagnostic folder: <https://github.com/dgoldman0/homeless/tree/main/warp-complex/first-pass>.

[^capacity_folder]: Capacity-coupled lapse folder: <https://github.com/dgoldman0/homeless/tree/main/warp-complex/capacity-coupled-lapse>.

[^lambda_folder]: Lapse-margin folder: <https://github.com/dgoldman0/homeless/tree/main/warp-complex/lambda-A-lapse-margin>.

[^wormhole_burdened]: Wormhole-burdened / throat-loaded complex folder: <https://github.com/dgoldman0/homeless/tree/main/warp-complex/wormhole-burdened-complex>.

[^gated_report]: Throat-loaded gated-shift evaluation report: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/wormhole-burdened-complex/throat_loaded_gated_shift_full_evaluation_report.md>.

[^communication]: Catch-rematched throat-loaded transit paper bundle: <https://github.com/dgoldman0/homeless/tree/main/warp-complex/communication_paper>.

[^catch_bundle]: Catch-rematched hybrid flare-gated transit bundle: <https://github.com/dgoldman0/homeless/tree/main/warp-complex/catch_rematched_hybrid_flare_gated_transit>.

[^catch_paper_bundle]: Catch-rematched hybrid flare-gated transit v1 paper bundle: <https://github.com/dgoldman0/homeless/tree/main/warp-complex/catch_rematched_hybrid_flare_gated_transit_paper>.

[^catch_tex]: Paper source for `Catch-Rematched Hybrid Flare-Gated Transit`: <https://github.com/dgoldman0/homeless/blob/main/warp-complex/catch_rematched_hybrid_flare_gated_transit_paper/latex/main.tex>.

[^active_rail_readme]: Active-rail paper README: <https://github.com/dgoldman0/homeless/tree/main/warp-complex/active_rail_paper>.
