# Multi-Zone Phase-Cycled Throat Design — Reduced Evaluation

## Executive summary

This evaluation tests the next wormhole-only step after the failure of static throat support, static source pulsing, and one-zone global throat breathing. The tested idea is a multi-zone phase-cycled throat plant: keep a protected access core as quiet as possible while support, repayment, and buffering dynamics occur in neighboring radial bands.

The reduced result is informative but negative for this specific model family. Spatially separated side-band cycling can create repayment-like positive-energy phases away from the access core, and it can do so while the access core remains quiet. However, the protected access core then retains the same local sampled-energy obstruction as the static throat. When the core itself is actuated strongly or quickly enough to improve the sampled-energy bookkeeping, the access region loses its quiet envelope through tidal/rate spikes or collapsed quiet-open fraction.

The main failure pattern is therefore:

```text
quiet protected core  -> static QI obstruction preserved
QI bookkeeping improves -> protected core becomes dynamically bad
```

This does not close the whole wormhole support problem. It does indicate that an areal-radius-only spherical multi-zone plant, by itself, is unlikely to be the destination. The next model should add lapse/redshift and radial-metric degrees of freedom, or treat this as evidence toward a reduced no-go for spherical `R(l,t)`-only throat plants under the chosen proxy.

## Scope

This is a wormhole-component-only evaluation. It deliberately excludes transport, catch/rematch, passenger packets, and hybrid network operation.

The model proxy is:

```math
ds^2=-dt^2+dl^2+R(l,t)^2d\Omega^2.
```

The effective source is read from the Einstein tensor of this metric family. The local energy-density proxy is:

```math
\rho(l,t)=\frac{G_{tt}}{8\pi}.
```

The sampled-energy proxy is Lorentzian sampling:

```math
\int \rho(\tau)\,\frac{\tau_0/\pi}{(\tau-\tau_c)^2+\tau_0^2}\,d\tau
\geq -\frac{3}{32\pi^2\tau_0^4}.
```

As in the earlier evaluations, `L0max` is the largest physical scale, in Planck units per dimensionless model unit, compatible with the strictest sampled negative-energy average in the proxy.

## Zone layout

The radial zones used in the code are:

| Zone | Radial range |
|---|---:|
| access core | `|l| <= 0.25` |
| support inner | `|l| <= 0.55` |
| repayment band | `0.65 <= |l| <= 1.15` |
| buffer band | `1.25 <= |l| <= 1.90` |
| outer field | `2.10 <= |l| <= 3.20` |

The cases use smooth even radial profiles for core/access, repayment, buffer, and outer-field actuation. The parameter sweep varies core amplitude, repayment amplitude, and actuation frequency.

## Diagnostics

The run records:

- local minimum, maximum, and mean `rho` by zone;
- radial null-projection proxy `Gkk` by zone;
- angular tidal proxy `-R_tt/R`;
- fractional throat-rate proxy `R_t/R`;
- source-flux proxy `G_tl/(8*pi)`;
- Lorentzian sampled-energy records by zone;
- access open fraction and quiet-open fraction.

A timestep is counted as quiet-open in the access core when the core is open and the local rate, tidal, and flux proxies remain below the simple thresholds used in the script.

## Named-case results

| case                                |   access_core_qi_strict_log10_L0max |   access_core_qi_positive_sample_fraction |   repayment_band_qi_positive_sample_fraction |   buffer_band_qi_positive_sample_fraction |   access_core_max_abs_tidal |   access_core_max_abs_rate |   access_quiet_open_fraction | failure_mode                           |
|:------------------------------------|------------------------------------:|------------------------------------------:|---------------------------------------------:|------------------------------------------:|----------------------------:|---------------------------:|-----------------------------:|:---------------------------------------|
| static_reference                    |                             -0.311  |                                    0      |                                       0      |                                    0      |                    5.21e-11 |                   5.68e-14 |                            1 | static-QI-obstruction-preserved        |
| sideband_repay_only                 |                             -0.311  |                                    0      |                                       0.31   |                                    0.176  |                    5.21e-11 |                   5.68e-14 |                            1 | static-QI-obstruction-preserved        |
| protected_core_sidecycle            |                             -0.311  |                                    0      |                                       0.776  |                                    0.801  |                    5.21e-11 |                   5.68e-14 |                            1 | static-QI-obstruction-preserved        |
| delayed_side_repay_with_static_core |                             -0.311  |                                    0      |                                       0.311  |                                    0.0322 |                    5.21e-11 |                   5.68e-14 |                            1 | static-QI-obstruction-preserved        |
| mild_split_phase                    |                             -0.322  |                                    0.0361 |                                       0.247  |                                    0.203  |                    2.32     |                   0.28     |                            0 | access-window-collapse                 |
| fast_split_phase                    |                              0.0687 |                                    0.827  |                                       0.93   |                                    0.756  |                   49.9      |                   1.68     |                            0 | access-window-collapse                 |
| ultrafast_tiny_core                 |                              3.91   |                                    0.998  |                                       1      |                                    0.993  |                  165        |                   1.98     |                            0 | QI-improvement-bought-by-access-ripple |
| aggressive_core_phase               |                            inf      |                                    1      |                                       1      |                                    0.98   |                  274        |                   5.42     |                            0 | QI-improvement-bought-by-access-ripple |
| short_access_pulse_repay_shoulders  |                             -0.962  |                                    0.157  |                                       0.393  |                                    0.0297 |                  734        |                  12        |                            0 | access-window-collapse                 |
| outward_repayment_wave              |                             -0.79   |                                    0.0399 |                                       0.0237 |                                    0.213  |                    2.71e+03 |                  16.3      |                            0 | access-window-collapse                 |

The side-band-only cases have the most important qualitative result. `sideband_repay_only`, `protected_core_sidecycle`, and `delayed_side_repay_with_static_core` all generate positive-sample fractions in repayment/buffer bands while keeping the access core quiet. Yet the access-core strict QI scale remains at the static value, approximately:

```math
\log_{10}(L_{0,max}/L_P)\approx -0.311.
```

The high-frequency core-actuated cases have the opposite behavior. `ultrafast_tiny_core` and `aggressive_core_phase` can improve or eliminate the strict sampled negative access-core average in the tested windows, but the access quiet-open fraction falls to zero and the access tidal/rate proxies become large.

## Parameter sweep results

The focused sweep covered 120 combinations of core amplitude, repayment amplitude, and frequency.

| failure_mode           |   count |
|:-----------------------|--------:|
| quiet-window-lost      |      60 |
| static-QI-preserved    |      40 |
| QI-improves-via-ripple |      12 |
| transition/marginal    |       8 |

Best cases that keep `access_quiet_open_fraction >= 0.9`:

|   core_amp |   repay_amp |   omega |   access_qi_log10_L0max |   access_max_abs_tidal |   access_max_abs_rate |   access_quiet_open_fraction |   repay_positive_sample_fraction | failure_mode        |
|-----------:|------------:|--------:|------------------------:|-----------------------:|----------------------:|-----------------------------:|---------------------------------:|:--------------------|
|      0.01  |        0.06 |       8 |                  -0.31  |                  0.646 |                  0.08 |                            1 |                            0.193 | static-QI-preserved |
|      0.01  |        0    |       8 |                  -0.31  |                  0.646 |                  0.08 |                            1 |                            0     | static-QI-preserved |
|      0.01  |        0.2  |       8 |                  -0.31  |                  0.646 |                  0.08 |                            1 |                            0.432 | static-QI-preserved |
|      0.01  |        0.12 |       8 |                  -0.31  |                  0.646 |                  0.08 |                            1 |                            0.281 | static-QI-preserved |
|      0.005 |        0.12 |       8 |                  -0.311 |                  0.321 |                  0.04 |                            1 |                            0.281 | static-QI-preserved |
|      0.005 |        0.2  |       8 |                  -0.311 |                  0.321 |                  0.04 |                            1 |                            0.432 | static-QI-preserved |
|      0.005 |        0.06 |       8 |                  -0.311 |                  0.321 |                  0.04 |                            1 |                            0.193 | static-QI-preserved |
|      0.005 |        0    |       8 |                  -0.311 |                  0.321 |                  0.04 |                            1 |                            0     | static-QI-preserved |

Best access-QI cases regardless of access violence:

|   core_amp |   repay_amp |   omega |   access_qi_log10_L0max |   access_positive_sample_fraction |   access_max_abs_tidal |   access_max_abs_rate |   access_quiet_open_fraction |   repay_positive_sample_fraction | failure_mode           |
|-----------:|------------:|--------:|------------------------:|----------------------------------:|-----------------------:|----------------------:|-----------------------------:|---------------------------------:|:-----------------------|
|       0.04 |        0.06 |      64 |                     inf |                                 1 |                    167 |                  2.53 |                            0 |                                1 | QI-improves-via-ripple |
|       0.04 |        0.12 |      64 |                     inf |                                 1 |                    167 |                  2.53 |                            0 |                                1 | QI-improves-via-ripple |
|       0.04 |        0.2  |      64 |                     inf |                                 1 |                    167 |                  2.53 |                            0 |                                1 | QI-improves-via-ripple |
|       0.08 |        0    |      64 |                     inf |                                 1 |                    348 |                  5.08 |                            0 |                                0 | QI-improves-via-ripple |
|       0.08 |        0.12 |      64 |                     inf |                                 1 |                    348 |                  5.08 |                            0 |                                1 | QI-improves-via-ripple |
|       0.08 |        0.2  |      64 |                     inf |                                 1 |                    348 |                  5.08 |                            0 |                                1 | QI-improves-via-ripple |
|       0.08 |        0.06 |      64 |                     inf |                                 1 |                    348 |                  5.08 |                            0 |                                1 | QI-improves-via-ripple |
|       0.04 |        0    |      64 |                     inf |                                 1 |                    167 |                  2.53 |                            0 |                                0 | QI-improves-via-ripple |

Transition/marginal cases:

|   core_amp |   repay_amp |   omega |   access_qi_log10_L0max |   access_positive_sample_fraction |   access_max_abs_tidal |   access_max_abs_rate |   access_quiet_open_fraction |   repay_positive_sample_fraction | failure_mode        |
|-----------:|------------:|--------:|------------------------:|----------------------------------:|-----------------------:|----------------------:|-----------------------------:|---------------------------------:|:--------------------|
|      0.005 |        0    |      16 |                  -0.31  |                            0      |                  1.28  |                0.0799 |                        0.581 |                            0     | transition/marginal |
|      0.005 |        0.06 |      16 |                  -0.31  |                            0      |                  1.28  |                0.0799 |                        0.581 |                            0.227 | transition/marginal |
|      0.005 |        0.12 |      16 |                  -0.31  |                            0      |                  1.28  |                0.0799 |                        0.581 |                            0.634 | transition/marginal |
|      0.005 |        0.2  |      16 |                  -0.31  |                            0      |                  1.28  |                0.0799 |                        0.581 |                            0.775 | transition/marginal |
|      0.04  |        0    |       4 |                  -0.347 |                            0.0674 |                  0.667 |                0.16   |                        0.335 |                            0     | transition/marginal |
|      0.04  |        0.06 |       4 |                  -0.347 |                            0.0674 |                  0.667 |                0.16   |                        0.335 |                            0.277 | transition/marginal |
|      0.04  |        0.12 |       4 |                  -0.347 |                            0.0674 |                  0.667 |                0.16   |                        0.335 |                            0.358 | transition/marginal |
|      0.04  |        0.2  |       4 |                  -0.347 |                            0.0674 |                  0.667 |                0.16   |                        0.335 |                            0.401 | transition/marginal |

The sweep reinforces the named-case result. Quiet cases preserve the static sampled-energy obstruction. Improved access-core QI bookkeeping appears only when the access core is dynamically active enough to fail the quiet-envelope criterion.

## Interpretation

### Result 1: spatial repayment routing is real but insufficient

The side-band cases show that repayment/buffer zones can be made dynamically active while the access core remains quiet. That is a useful engineering primitive. It means multi-zone routing can, in this reduced model, reduce direct access exposure to repayment pulses.

But this is not enough to support a traversable throat. The access/support core still carries the local flare-out burden. If the core remains quasi-static, its local observers continue to sample persistent negative energy.

### Result 2: the support debt is local in this proxy

The strongest conclusion is that the QI pressure is not merely a global accounting problem. Positive-energy activity in a nearby band does not automatically repair the sampled negative history of static observers in the throat core.

That is a useful physics-facing result. It pushes against the naive idea that one can simply arrange negative energy in one place, positive repayment somewhere else, and declare the total cycle acceptable. In this proxy, the observer family matters.

### Result 3: core actuation recovers the old breathing-throat trade

Once the core itself participates dynamically, the model finds the same basic trade as the one-zone breathing throat:

```text
better sampled-energy bookkeeping <-> stronger access-region ripple
```

The multi-zone plant makes the failure more localized and better diagnosed, but does not remove it.

### Result 4: the areal-radius-only model may be too constrained

The model uses only one geometric field, `R(l,t)`. That makes the flare-out geometry and access smoothness compete directly. It may be too restrictive to represent any real throat-support plant.

The next test should add lapse/redshift and radial-metric structure:

```math
ds^2=-N(l,t)^2dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The specific question is whether the support burden can be shifted among energy density, radial pressure/tension, lapse gradients, and radial metric dynamics without producing horizons or unacceptable tidal/rate histories in the access core.

## Potential implications

### If the negative result persists under richer models

If the same bifurcation survives when `N(l,t)` and `B(l,t)` are added, it would support a stronger reduced no-go statement: any quasi-static protected throat core in this class preserves the local sampled-energy obstruction, while any local cycling strong enough to improve the QI proxy damages traversability.

That would be a meaningful physics result even if it does not help the engineering program.

### If the richer model finds a middle regime

If adding `N(l,t)` and `B(l,t)` produces a regime where the core remains access-smooth while the sampled-energy burden moves into pressure, tension, or redshift structure, then the multi-zone design becomes more promising. The side-band repayment result would then serve as a useful shielding/routing primitive around a more sophisticated support core.

### What this evaluation does not show

This evaluation does not show a viable macroscopic throat. It also does not prove impossibility. It only shows that the simplest multi-zone extension of the previous breathing-throat model fails in a structured way.

## Recommended next step

Do not promote this to a final destination design. Use it as a failure-mode report and move to a richer spherical throat plant with independent lapse, radial metric, and areal-radius controls.

The next evaluation should test:

1. whether lapse/redshift modulation can alter sampled histories without creating horizon-like behavior;
2. whether radial metric support can carry some burden without forcing `R(l,t)` core ripple;
3. whether NEC violation can be redistributed into radial pressure/tension instead of persistent core energy density;
4. whether repayment/buffer bands remain useful once the support core has more degrees of freedom.

## Reproducibility

Run from this directory:

```bash
python run_multizone_phase_cycled_throat_eval.py
python run_multizone_parameter_sweep.py
```

Generated files:

- `multizone_case_summary.csv`
- `multizone_zone_qi_summary.csv`
- `multizone_time_digest.csv`
- `multizone_parameter_sweep.csv`
- `multizone_parameter_sweep_extracts.json`
- `multizone_model_summary.json`
