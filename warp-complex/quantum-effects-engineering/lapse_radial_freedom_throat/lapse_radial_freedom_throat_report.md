# Lapse and Radial-Metric Freedom in a Phase-Cycled Wormhole Throat Plant — Reduced Evaluation

## Executive summary

This evaluation extends the multi-zone phase-cycled throat work from an areal-radius-only model into a broader wormhole-only metric family,

```math
ds^2=-N(l,t)^2dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The transport/catch/passenger layer remains outside the evaluation. The active question is whether lapse freedom `N(l,t)` and radial metric freedom `B(l,t)` provide a more useful quantum-effects engineering envelope for the wormhole component than global throat breathing or areal-radius-only phase cycling.

The results produce a useful design pivot. Fast actuation of the access throat continues to trade sampled-energy improvement for access-core ripple. Lapse freedom acts mainly as a timing, redshift, and matching degree of freedom in this reduced proxy. Radial proper-length freedom gives the first quiet local softening signal: a stretched radial core can move the access-core energy-density diagnostic from negative to nonnegative while reducing the local radial NEC debt. The integrated radial NEC burden remains present and is spread through proper length and transition structure.

The current design direction is therefore:

```math
\text{long, gently flared, quasi-static throat plant}
\quad + \quad
\text{multi-zone repayment / buffer management}.
```

The combined results have produced a sharper design target. A finished functional throat design remains ahead.

## Literature frame

The baseline throat problem follows the Morris--Thorne traversable wormhole construction, where a throat without a horizon requires exotic stress-energy and radial tension conditions at the flare-out region [MorrisThorne1988]. Ford and Roman's quantum-inequality analysis is the central constraint on macroscopic static wormholes: the allowed arrangements tend toward Planck-scale throats or large discrepancies between throat size and the length scale over which negative energy is concentrated [FordRoman1996]. The quantum-interest literature motivates the repayment language: negative-energy episodes require compensating positive-energy structure with timing and overcompensation constraints [FordRoman1999]. Static-spacetime quantum inequalities motivate the use of observer families and sampling functions beyond instantaneous energy-density signs alone [FewsterTeo1999]. Visser's wormhole treatment provides the broader energy-condition language used here [Visser1996].

The project also keeps ADM role separation in view, especially the distinction between lapse, spatial metric, and shift emphasized in modern warp-drive metric organization [BobrickMartire2021]. The present run uses that role separation only inside the wormhole component. The shift/transport layer is absent.

## Prior boundary from the multi-zone areal-radius model

The previous multi-zone phase-cycled throat test used

```math
ds^2=-dt^2+dl^2+R(l,t)^2d\Omega^2.
```

It spatially separated access, support, repayment, and buffer regions. That produced a clean boundary:

- side-band repayment and buffer cycling can keep repayment activity away from the access core;
- protected side-band cycling leaves the access-core QI score at the static-throat value;
- core actuation can improve sampled-energy bookkeeping, and the same cases lose the quiet access window through tidal/rate growth.

The useful conclusion was that repayment routing is meaningful, while the local flare-out support debt remains attached to the throat core in an `R(l,t)`-only plant.

## Evaluation A: lapse and radial metric freedom

The first extension evaluated named cases and a parameter sweep in the metric family

```math
ds^2=-N(l,t)^2dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The model computed effective Einstein-source proxies from the prescribed metric, then recorded zone diagnostics for:

- energy density `rho`;
- radial pressure/tension proxy `p_radial`;
- radial NEC proxy `rho + p_radial`;
- sampled-energy scale estimates for `rho` and the radial NEC proxy;
- tidal, flux, lapse-gradient, radial-metric-rate, and quiet-open diagnostics.

The principal named-case results were:

| Case | access rho log10 L0max | access NEC log10 L0max | quiet-open fraction | min rho | min rho+p_r | max N | max B | classification |
|---|---|---|---|---|---|---|---|---|
| static_reference | -0.310911 | -0.461493 | 1 | -0.0397644 | -0.0795531 | 1 | 1 | rho-QI-static-obstruction-preserved |
| static_Bcore_1p2 | -0.10572 | -0.382312 | 1 | -0.0154565 | -0.0552452 | 1 | 1.2 | rho-QI-static-obstruction-preserved |
| static_Bcore_1p41421356237 | ∞ | -0.310978 | 1 | 1.218e-05 | -0.0397766 | 1 | 1.41421 | rho-helped-but-NEC-debt-remains |
| static_Bcore_2p0 | ∞ | -0.160463 | 1 | 0.0184839 | -0.0198883 | 1 | 2 | rho-helped-but-NEC-debt-remains |
| static_Bcore_3p0 | ∞ | 0.0156284 | 1 | 0.0288521 | -0.00883924 | 1 | 3 | rho-helped-but-NEC-debt-remains |
| radial_tube_B5 | ∞ | 0.237477 | 1 | 0.0343104 | -0.00318212 | 1 | 5 | rho-helped-but-NEC-debt-remains |
| static_lapse_core_N2 | -0.310911 | -0.461493 | 1 | -0.0397644 | -0.0795531 | 2 | 1 | rho-QI-static-obstruction-preserved |
| Bcore2_Rmild_split | 1.87862 | -0.281799 | 0 | -0.106574 | -0.542182 | 1 | 2 | quiet-window-lost |
| Bcore2_Rtiny_fast | ∞ | -0.637538 | 0 | -0.0583075 | -7.28701 | 1 | 2 | quiet-window-lost |


The named cases establish four useful points.

First, lapse structure by itself preserves the access-core energy-density obstruction in this proxy. The lapse cases remain useful as timing and matching candidates, while the core `rho` diagnostic stays aligned with the static reference.

Second, a static stretched radial core changes the local source anatomy. Near `B0 = sqrt(2)`, the access-core `rho` diagnostic crosses toward nonnegative values. Larger `B0` values keep `rho` nonnegative and continue reducing the magnitude of the radial NEC proxy.

Third, dynamic `R` actuation on top of a stretched core recovers the earlier access-ripple trade. The `Bcore2_Rmild_split` and `Bcore2_Rtiny_fast` rows show improved or altered `rho` bookkeeping together with zero quiet-open fraction and large tidal/NEC excursions.

Fourth, extremely large radial stretch has its own engineering cost. The `radial_tube_B10` case improves the local NEC scale and crosses the bounded-core criteria used in the quiet-open classification. This supports a finite-stretch design target with explicit radial-length cost accounting.

The parameter sweep around `N`, `B`, and mild `R` actuation produced the following classification counts:

| Classification | Count |
|---|---:|
| rho-helped-but-NEC-debt-remains | 60 |
| quiet-window-lost | 38 |
| rho-QI-static-obstruction-preserved | 19 |
| lapse-radial-gradient-burden | 14 |
| mixed-transition | 4 |


The sweep sharpened the qualitative picture: `B` freedom supplies a quiet local softening knob; `N` freedom supplies role separation and matching structure; dynamic access-core actuation continues to be the expensive path.

## Evaluation B: proper-length optimized static sweep

The next sweep focused on static, quasi-engineering geometry:

```math
ds^2=-dt^2+B(l)^2dl^2+R(l)^2d\Omega^2.
```

The sweep varied:

- `B0`: radial proper-length stretch in the throat core;
- `wB`: width of the radial stretch;
- `aR`: slow-flare / areal-radius shaping parameter;
- `wR`: transition width for the areal-radius profile.

The grid contained **3,087** static profiles. It evaluated local access-core stress, transition shoulders, integrated negative energy-density burden, integrated negative radial-NEC burden, and the proper half-length required to reach selected areal radii.

Classification counts:

| Classification | Count |
|---|---:|
| candidate-static-envelope | 1855 |
| rho-helped-nec-debt-remains | 616 |
| long-throat-engineering-burden | 511 |
| rho-obstruction-persists | 105 |


Representative profiles:

| B0 | wB | aR | wR | min rho | min rho+p_r | rho log10 L0max | NEC log10 L0max | proper half-length to R=2 | integrated neg NEC | integrated neg rho | transition |NEC| max | classification |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.45 | 1 | 0.45 | -0.0397808 | -0.0795695 | -0.311001 | -0.461538 | 1.74 | 0.158605 | 0.0961196 | 0.0407458 | rho-obstruction-persists |
| 2 | 5 | 1 | 0.45 | 0.0187337 | -0.0198924 | ∞ | -0.160508 | 3.47939 | 0.158605 | 0.0687907 | 0.0154774 | rho-helped-nec-debt-remains |
| 3 | 0.45 | 1 | 0.45 | 0.0268569 | -0.0103305 | ∞ | -0.0182245 | 2.52517 | 0.158658 | 0.0918678 | 0.0407458 | rho-helped-nec-debt-remains |
| 3 | 1.6 | 1 | 0.45 | 0.0291296 | -0.00884106 | ∞ | 0.0155837 | 4.50315 | 0.158612 | 0.0849456 | 0.0608041 | candidate-static-envelope |
| 5 | 0.45 | 12 | 1.6 | 0.0397403 | -3.119e-05 | ∞ | 1.24182 | 3.39604 | 0.350044 | 0.339295 | 0.420449 | candidate-static-envelope |
| 5 | 1.1 | 12 | 1.6 | 0.0397491 | -2.233e-05 | ∞ | 1.31438 | 5.60033 | 0.350068 | 0.338217 | 0.431186 | candidate-static-envelope |
| 8 | 5 | 1 | 0.45 | 0.0362786 | -0.00124327 | ∞ | 0.441552 | 13.9127 | 0.158609 | 0.112681 | 0.0266049 | long-throat-engineering-burden |


The baseline static throat has access-core `rho_min = -0.0397808`, access-core `rho+p_r` minimum `-0.0795695`, access `rho` sampled scale `-0.0397808_LOG`, access NEC sampled scale `-0.0795695_LOG`, proper half-length to `R=2` of `1.74`, and total integrated negative radial NEC burden `0.158605`.

The stretched radial profiles improve the local access diagnostics. For example, the `B0=3, aR=1` family makes access-core `rho` positive and reduces the local `rho+p_r` magnitude to roughly `1e-2`, while the total integrated negative radial NEC remains near the baseline value. Larger slow-flare profiles can make the local NEC diagnostic extremely small, and the integrated burden then grows or moves into transition shoulders and added proper length.

The integrated-burden summary by classification is:

| Classification | Profiles | NEC integral min | NEC integral median | NEC integral max | length min | length median | length max |
|---|---:|---:|---:|---:|---:|---:|---:|
| candidate-static-envelope | 1855 | 0.158606 | 0.268444 | 0.417693 | 1.74 | 3.98604 | 9.99303 |
| long-throat-engineering-burden | 511 | 0.158607 | 0.170943 | 0.417693 | 10.0118 | 15.9058 | 46.4171 |
| rho-helped-nec-debt-remains | 616 | 0.158605 | 0.195905 | 0.300813 | 1.74 | 2.36 | 4.83387 |
| rho-obstruction-persists | 105 | 0.158605 | 0.158605 | 0.173248 | 1.74 | 1.74 | 2.0879 |


The proper-length sweep therefore gives a coherent interpretation: local stress severity can be diluted by stretching the radial geometry and slowing the areal flare; the radial NEC support burden is redistributed through proper length and transition structure.

## Main findings

### 1. Radial metric freedom is the strongest new design knob

The `R(l,t)`-only phase-cycled plant had a sharp bifurcation between quiet access and improved sampled-energy bookkeeping. Adding `B(l,t)` creates a useful middle region: a quiet static access core with positive or near-positive `rho` and weaker local radial NEC proxy.

This is the first reduced signal that a wormhole throat component can move from fast temporal cycling toward geometric burden dilution.

### 2. Lapse freedom is a supporting degree of freedom in this proxy

The lapse cases preserve the access-core `rho` and radial NEC values of the underlying spatial geometry. Lapse gradients add their own acceleration and tidal-like diagnostics. This keeps `N(l,t)` in the design as a matching, scheduling, and redshift-control variable, while `B(l)` and `R(l)` carry the main static support-shaping task.

### 3. The local `rho` diagnostic and the radial NEC diagnostic separate

The stretched-core cases can make access-core `rho` nonnegative. The radial NEC proxy remains the central throat-support diagnostic. This separation is important because an energy-density-only score makes the geometry look more successful than a null-support or radial-tension score.

The next QEE scoring system should therefore track both:

```math
\rho
```

and

```math
\rho+p_r,
```

with future work replacing the latter proxy by a more careful null-contracted sampling diagnostic.

### 4. The integrated NEC burden behaves like a conserved engineering debt in this family

Across the static proper-length sweep, many profiles improve the access-core values while the integrated negative radial NEC remains near the baseline or grows with added proper length and transition shaping. This suggests a reduced conservation-like pattern: this metric family can spread the burden, soften it locally, and move it into shoulders, while the total radial support requirement remains present.

That pattern resonates with Ford and Roman's length-scale-discrepancy result: macroscopic wormhole support can trade local severity against extreme or carefully shaped length scales [FordRoman1996]. The present sweep finds a gentler version of that trade in a prescribed-geometry engineering proxy.

### 5. Phase cycling remains useful as repayment and buffer management

The multi-zone phase-cycling idea retains value. The role changes. The access core wants quasi-static shaping; repayment and buffer zones remain useful places for time dependence, compensation, and source-routing tests. This gives a two-level throat design:

```math
\text{quasi-static long throat/access plant}
\quad + \quad
\text{time-managed support, repayment, and buffer bands}.
```

## Physics implications

### Local QI pressure can be diluted through geometry

The most constructive implication is that the access-core energy-density QI pressure is sensitive to radial metric freedom. The areal-radius-only throat made the local `rho` obstruction look fixed. The broader `B(l),R(l)` family shows that local core stress can be softened while avoiding violent time dependence.

### The wormhole NEC condition remains the central burden

The same profiles show that radial NEC support remains the central throat requirement. This aligns with the Morris--Thorne flare-out condition and the broader energy-condition literature. The proper-length sweep frames that burden as an engineering distribution problem: where it sits, how sharply it peaks, how long the support region becomes, and how large the transition shoulders grow.

### Repayment locality matters

The earlier phase-cycling results showed that positive-energy repayment away from the core can protect the access region from repayment pulses, while local observers still sample the local throat-support debt. That matches the spirit of quantum-interest constraints: compensation has timing and placement structure, and global bookkeeping alone is a weak guide [FordRoman1999].

### Energy-density sampling is an incomplete viability score

A profile can pass the access-core `rho` proxy while retaining radial NEC debt. The next tier should use null-contracted sampled quantities, state-dependent source assumptions, and curvature-radius consistency checks. Fewster--Teo style static-spacetime sampling results support this shift toward observer/sampling-function discipline [FewsterTeo1999].

## Design implications

The best current design target is a **long-throat quasi-static support plant**:

```math
N(l,t) \approx \text{matching/timing control},
```

```math
B(l) \approx \text{proper-length support dilution},
```

```math
R(l) \approx \text{slow areal flare / transition shaping},
```

```math
\text{repayment and buffer bands} \approx \text{managed time-dependent source routing}.
```

Useful near-term design rules from the reduced evaluations:

1. Keep the access core quasi-static during access windows.
2. Use radial proper-length shaping to reduce local energy-density and radial NEC severity.
3. Track integrated negative NEC as a primary cost, alongside local peak values.
4. Treat transition shoulders as active engineering components with their own stress and gradient budgets.
5. Reserve time dependence for repayment/buffer regions until a source model justifies access-core actuation.
6. Score `rho`, radial NEC, null projections, curvature/tidal proxies, lapse gradients, radial metric gradients, and proper length together.

## Recommended next evaluation

The next reduced evaluation should optimize a static or slowly varying long-throat plant against three costs:

```math
J = w_1\,\max_{\rm access}|(\rho+p_r)_-| 
+ w_2\,\int (-(\rho+p_r))_+\,ds
+ w_3\,L_{\rm proper}
+ w_4\,S_{\rm shoulder},
```

with separate constraints for access-core tidal history, lapse boundedness, horizon indicators, and transition stress. The strongest next upgrade is a null-projected sampling calculation for selected candidate profiles, using observer families adapted to the static throat, transition shoulders, and repayment bands.

A later source-model study should ask whether any known semiclassical state class can approximate the required radial-tension support distribution. That study becomes the true QEE viability gate.

## Reproducibility

This bundle contains the scripts and data used for the reduced evaluations:

- `run_lapse_radial_freedom_eval.py` — named cases and `N,B,R` parameter sweep.
- `lapse_radial_case_summary.csv` — named-case diagnostics.
- `lapse_radial_parameter_sweep.csv` — dynamic/static parameter sweep.
- `lapse_radial_time_digest.csv` — compact time histories.
- `lapse_radial_result_extracts.json` — selected results.
- `run_proper_length_optimized_sweep.py` — static proper-length sweep.
- `proper_length_optimized_sweep.csv` — 3,087-profile sweep table.
- `proper_length_profile_digest.csv` — selected profile digest.
- `proper_length_sweep_extracts.json` — selected proper-length results.
- `proper_length_sweep_summary.json` — sweep metadata.

The calculations are prescribed-geometry reduced diagnostics. They identify engineering signals and operating boundaries for the wormhole component. Semiclassical source construction, quantum-state modeling, and numerical-relativity initial-data checks remain future gates.

## References

[MorrisThorne1988] M. S. Morris and K. S. Thorne, “Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity,” *American Journal of Physics* 56, 395–412 (1988). DOI: <https://doi.org/10.1119/1.15620>.

[FordRoman1996] L. H. Ford and T. A. Roman, “Quantum field theory constrains traversable wormhole geometries,” *Physical Review D* 53, 5496–5507 (1996). DOI: <https://doi.org/10.1103/PhysRevD.53.5496>.

[FordRoman1999] L. H. Ford and T. A. Roman, “The quantum interest conjecture,” *Physical Review D* 60, 104018 (1999). DOI: <https://doi.org/10.1103/PhysRevD.60.104018>.

[FewsterTeo1999] C. J. Fewster and E. Teo, “Bounds on negative energy densities in static space-times,” *Physical Review D* 59, 104016 (1999). DOI: <https://doi.org/10.1103/PhysRevD.59.104016>.

[PfenningFord1997] M. J. Pfenning and L. H. Ford, “The unphysical nature of ‘warp drive’,” *Classical and Quantum Gravity* 14, 1743–1751 (1997). DOI: <https://doi.org/10.1088/0264-9381/14/7/011>.

[Visser1996] M. Visser, *Lorentzian Wormholes: From Einstein to Hawking*, American Institute of Physics / Springer (1996). ISBN 978-1-56396-653-8. Publisher page: <https://link.springer.com/book/9781563966538>.

[BobrickMartire2021] A. Bobrick and G. Martire, “Introducing physical warp drives,” *Classical and Quantum Gravity* 38, 105009 (2021). DOI: <https://doi.org/10.1088/1361-6382/abdf6e>.
