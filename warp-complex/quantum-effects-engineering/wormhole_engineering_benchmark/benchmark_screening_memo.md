# Benchmarking the Wormhole-Support Engineering Screening Framework

## Purpose

This benchmark phase tests whether the engineering screening framework reproduces the known verdicts of canonical traversable-wormhole and quantum-inequality literature. The aim is methodological: the framework translates established physics constraints into subsystem roles and engineering gates for hypothetical wormhole-support infrastructure.

The benchmark uses reduced proxies and literature classifications. It is a first validation layer for the screening framework, rather than a full numerical reconstruction of every cited spacetime.

## Framework being benchmarked

The framework decomposes a proposed throat-support infrastructure into the following functions:

| Function | Engineering question | Diagnostic gate |
|---|---|---|
| Support core | What maintains flare-out? | radial NEC, null-contracted stress, sampled stress |
| Access region | What does a traversal path experience? | tidal history, quiet-open fraction, traversal/affine length |
| Repayment / compensation | Where does positive compensation occur? | observer-family sampled stress and locality |
| Buffer | What shields the access region from source cycling? | flux, tidal coupling, transition leakage |
| Matching / lapse | How are timing, redshift, and horizon margins managed? | lapse bounds, redshift gradients, horizon indicators |
| Transition shoulders | Where do gradients and support costs reappear? | curvature, derivative stress, shoulder maxima |
| Source realism | What source can realize the effective stress? | null-contracted QIs, quantum interest, backreaction |

## Literature anchors

Morris and Thorne establish the traversable throat as a flare-out geometry requiring exotic stress, including radial tension exceeding ordinary matter bounds. Ford and Roman impose quantum-inequality constraints on static traversable wormholes, concluding that macroscopic support requires either near-Planck scale or severe length-scale discrepancy. Ford and Roman's quantum-interest work constrains negative/positive pulse repayment schedules. Visser, Kar, and Dadhich show that volume-integral measures of energy-condition violation can be made small in selected geometries. Fewster and Roman apply null-contracted quantum inequalities to small-exotic-matter wormholes and show that macroscopic examples are ruled out or severely constrained. Hochberg and Visser supply local throat diagnostics for dynamic wormholes. Kuhfittig provides static/dynamic examples attempting to satisfy Ford-Roman constraints and shows how slow flare, traversability, and energy-condition issues interact.

## Benchmark catalog

The benchmark set includes seven cases:

1. Morris--Thorne ultrastatic baseline.
2. Ford--Roman length-scale-discrepancy gate.
3. VKD spatial-Schwarzschild-style proxy.
4. VKD small-integral exotic-matter family.
5. Kuhfittig slow-flare proxy.
6. Hochberg--Visser dynamic-throat gate.
7. B-stretched long-throat engineering proxy.

## Benchmark results

| model_id                            | framework_gate_sequence                                                                                                      | framework_expected_verdict              | known_literature_verdict                                                                                                                                                      |
|:------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------|:----------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MT_ultrastatic_baseline             | energy_density_sampling_gate; radial_nec_null_contracted_gate; source_realism_qi_gate                                        | support-core-QI-obstruction             | Traversable throat requires radial tension exceeding energy density; quantum inequalities make smooth macroscopic static support severely constrained.                        |
| Ford_Roman_length_scale_discrepancy | energy_density_gate_deferred; null_contracted_gate_required; length_scale_discrepancy_gate                                   | length-scale-discrepancy-gate           | Macroscopic wormhole support requires Planck-scale throat or large geometric length-scale discrepancy; negative energy typically lies in a thin band relative to throat size. |
| VKD_spatial_schwarzschild_proxy     | energy_density_relief_or_nonnegative; radial_nec_null_contracted_gate; source_realism_qi_gate                                | rho-relief-null-gate-remains            | Volume-integral exotic matter can be made small; quantum inequalities on null-contracted stress severely constrain macroscopic versions.                                      |
| VKD_small_integral_family           | energy_density_gate_deferred; null_contracted_gate_required; integrated_burden_separation_gate; source_realism_qi_gate       | integrated-burden-relief-source-QI-gate | Volume-integral measures can be made arbitrarily small; Fewster-Roman null-contracted QIs rule out or severely constrain macroscopic models.                                  |
| Kuhfittig_slow_flare_proxy          | energy_density_relief_or_nonnegative; radial_nec_null_contracted_gate; traversal_affine_length_gate                          | local-softening-traversal-gate          | Slow-flare/Ford-Roman-compatible attempts require fine tuning; Fewster-Roman reports a Kuhfittig model as nontraversable due to infinite affine parameter.                    |
| dynamic_throat_Hochberg_Visser_gate | dynamic_throat_gate; null_expansion_gate; flux_extrinsic_curvature_gate                                                      | dynamic-throat-gate-required            | Dynamic wormholes require local throat definitions; NEC violation remains generic and WEC avoidance is unlikely in Kuhfittig's dynamic analysis.                              |
| B_stretched_long_throat_proxy       | energy_density_relief_or_nonnegative; radial_nec_null_contracted_gate; length_scale_discrepancy_gate; source_realism_qi_gate | proper-length-stretch-null-source-gate  | Represents the established length-scale-discrepancy/slow-flare branch in engineering-control variables.                                                                       |

## Interpretation

The framework reproduces the expected literature verdicts in gate language.

The Morris--Thorne and Ford--Roman entries enter through the support-core and sampled-energy gates. The VKD entries show why local and integrated diagnostics must be separated: a model can reduce a volume-integral burden while retaining a null-contracted source-realism gate. The Kuhfittig proxy exercises the slow-flare/traversal gate: local support severity can be softened while affine length, fine tuning, and traversability become decisive. The Hochberg--Visser entry motivates the dynamic-throat gate: time-dependent throats require local null-expansion and flux/extrinsic-curvature diagnostics. The B-stretched engineering proxy maps the established length-scale-discrepancy branch into the proposed subsystem language.

## Result of the benchmark phase

The benchmark supports the framework as a reusable engineering screen. It does not introduce new wormhole physics. Its value is the organized mapping:

```math
known physics constraint
\rightarrow
engineering subsystem role
\rightarrow
diagnostic gate
\rightarrow
advance / revise / retire decision.
```

This is the field-facing methodological claim: candidate wormhole-support infrastructure can be compared by role and gate rather than by undifferentiated exotic-matter language.

## Next benchmark upgrades

The next implementation pass should add full metric-level reconstructions for selected published families:

1. Morris--Thorne baseline in proper-radial and curvature coordinates.
2. VKD spatial-Schwarzschild family with explicit volume-integral and boosted/null-stress diagnostics.
3. A Kuhfittig slow-flare model with traversal/affine-length scoring.
4. A dynamic wormhole example with Hochberg--Visser null-expansion throat location.

Those upgrades would turn this benchmark from a gate-classification pilot into a numerical validation suite.
