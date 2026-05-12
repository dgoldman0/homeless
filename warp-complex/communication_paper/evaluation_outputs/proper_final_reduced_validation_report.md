# Proper final reduced validation: simple catch-rematched baseline

This freezes the simple catch-rematched ansatz. No extra `W^p` shift gate is adopted. Core velocities are `V=1.5, 2.0, 2.5`; `V=3, 5` are stretch; `V=10` is an extreme stress case.

## Frozen baseline ansatz

```math
ds^2=-T^2dt^2+A^2(dl+\beta^l dt)^2+A^2r(l)^2d\Omega^2
```

```math
A=\exp(qW\ln C_0),\quad T=\exp(qW\ln(\lambda C_0)),\quad \beta^l=-U(t)E(X)W(l)S(l-X(t)).
```

Ordering: `catch -> shift fade -> throat relaxation`, i.e. `L_catch < L_beta < L_q`.

## 1. Nominal passenger-worldline results, 801 samples

| tier           |    V |   Delta |   timelike_fail_points |   gtt_positive_points |   max_worldline_norm |   max_abs_v_rel |   max_abs_tidal_pass |   I_neg_nec_sum_dtau |   I_abs_flux_dtau |   max_gtt |
|:---------------|-----:|--------:|-----------------------:|----------------------:|---------------------:|----------------:|---------------------:|---------------------:|------------------:|----------:|
| core           |  1.5 |     0.3 |                      0 |                     0 |            -0.749827 |        0.501644 |              286.084 |              82.8491 |           12.5631 |        -1 |
| core           |  1.5 |     0.1 |                      0 |                     0 |            -0.733669 |        0.526239 |             2385.18  |             223.938  |           37.0279 |        -1 |
| core           |  2   |     0.3 |                      0 |                     0 |            -0.749999 |        0.500022 |              309.785 |              83.3078 |           13.3225 |        -1 |
| core           |  2   |     0.1 |                      0 |                     0 |            -0.744805 |        0.510707 |             2581.55  |             228.581  |           39.2026 |        -1 |
| core           |  2.5 |     0.3 |                      0 |                     0 |            -0.75     |        0.5      |              328.976 |              82.9781 |           13.902  |        -1 |
| core           |  2.5 |     0.1 |                      0 |                     0 |            -0.748852 |        0.503072 |             2741.66  |             233.156  |           41.0216 |        -1 |
| stretch        |  3   |     0.3 |                      0 |                     0 |            -0.75     |        0.5      |              344.66  |              82.2781 |           14.3638 |        -1 |
| stretch        |  3   |     0.1 |                      0 |                     0 |            -0.749823 |        0.500618 |             2879.83  |             234.085  |           42.4191 |        -1 |
| stretch        |  5   |     0.3 |                      0 |                     0 |            -0.75     |        0.5      |              392.165 |              80.1472 |           15.666  |        -1 |
| stretch        |  5   |     0.1 |                      0 |                     0 |            -0.75     |        0.5      |             3255.03  |             228.681  |           46.2314 |        -1 |
| extreme_stress | 10   |     0.3 |                      0 |                     0 |            -0.75     |        0.5      |              460.473 |              77.0103 |           17.4249 |        -1 |
| extreme_stress | 10   |     0.1 |                      0 |                     0 |            -0.75     |        0.5      |             3861.11  |             219.583  |           51.5278 |        -1 |

## 2. Selected convergence checks

| tier           |    V |   Delta |    N |   timelike_fail_points |   gtt_positive_points |   max_abs_tidal_pass |   I_neg_nec_sum_dtau |   I_abs_flux_dtau |   rel_change_max_abs_tidal_pass_vs_prev |   rel_change_I_neg_nec_sum_dtau_vs_prev |   rel_change_I_abs_flux_dtau_vs_prev |
|:---------------|-----:|--------:|-----:|-----------------------:|----------------------:|---------------------:|---------------------:|------------------:|----------------------------------------:|----------------------------------------:|-------------------------------------:|
| core           |  2.5 |     0.1 |  801 |                      0 |                     0 |             2741.66  |             233.156  |           41.0216 |                           nan           |                           nan           |                        nan           |
| core           |  2.5 |     0.1 | 1601 |                      0 |                     0 |             2741.66  |             232.279  |           40.9624 |                             0           |                             0.00376213  |                          0.00144524  |
| core           |  2.5 |     0.3 |  201 |                      0 |                     0 |              324.595 |              82.5395 |           13.8678 |                           nan           |                           nan           |                        nan           |
| core           |  2.5 |     0.3 |  401 |                      0 |                     0 |              328.153 |              83.0913 |           13.9065 |                             0.0109618   |                             0.00668498  |                          0.00279159  |
| core           |  2.5 |     0.3 |  801 |                      0 |                     0 |              328.976 |              82.9781 |           13.902  |                             0.00250772  |                             0.00136281  |                          0.000319996 |
| core           |  2.5 |     0.3 | 1601 |                      0 |                     0 |              329.189 |              82.9505 |           13.8999 |                             0.000646543 |                             0.000332035 |                          0.000151513 |
| stretch        |  5   |     0.1 |  801 |                      0 |                     0 |             3255.03  |             228.681  |           46.2314 |                           nan           |                           nan           |                        nan           |
| stretch        |  5   |     0.1 | 1601 |                      0 |                     0 |             3275.77  |             229.354  |           46.2698 |                             0.00637288  |                             0.00294283  |                          0.000829788 |
| stretch        |  5   |     0.3 |  801 |                      0 |                     0 |              392.165 |              80.1472 |           15.666  |                           nan           |                           nan           |                        nan           |
| stretch        |  5   |     0.3 | 1601 |                      0 |                     0 |              392.165 |              80.1135 |           15.665  |                             0           |                             0.000419818 |                          6.37715e-05 |
| extreme_stress | 10   |     0.3 |  801 |                      0 |                     0 |              460.473 |              77.0103 |           17.4249 |                           nan           |                           nan           |                        nan           |
| extreme_stress | 10   |     0.3 | 1601 |                      0 |                     0 |              461.182 |              77.0681 |           17.4277 |                             0.00154051  |                             0.000750245 |                          0.000161818 |

## 3. Dense metric/source maps over catch/release layers

| tier           |    V |   gtt_positive_points |   max_gtt |   min_lapse_shift_margin |   maxabs_R |   maxabs_Kretsch |   max_neg_nec_sum |   min_rho_adm |   max_abs_flux_j_l |   max_theta_product |
|:---------------|-----:|----------------------:|----------:|-------------------------:|-----------:|-----------------:|------------------:|--------------:|-------------------:|--------------------:|
| core           |  1.5 |                     0 |  -1       |                 1        |    2358.25 |      1.01289e+06 |           638.035 |      -571.629 |            38.1323 |             3.23114 |
| core           |  2   |                     0 |  -1       |                 1        |    2491.17 |      1.15466e+06 |           622.172 |      -571.629 |            47.0351 |             2.95847 |
| core           |  2.5 |                     0 |  -1       |                 1        |    2617.54 |      1.30682e+06 |           610.371 |      -571.629 |            55.4347 |             2.76291 |
| stretch        |  3   |                     0 |  -1       |                 1        |    2743.59 |      1.47472e+06 |           601.07  |      -571.629 |            63.4534 |             2.61503 |
| stretch        |  5   |                     0 |  -1       |                 1        |    3280.71 |      2.38131e+06 |           576.482 |      -571.629 |            92.9216 |             2.28572 |
| extreme_stress | 10   |                     2 |   7.47349 |                -0.243733 |    5043.64 |      7.5445e+06  |           546.175 |      -571.629 |           156.392  |             7.77565 |

These dense maps use metric/source diagnostics only. Passenger-frame quantities are interpreted only on the actual passenger worldline.

## 4. Focused timing/catch perturbation basin

|    V | tier           |   Delta |   cases |   safe_cases |   safe_fraction |   timelike_fail_cases |   worldline_gtt_fail_cases |   near_null_cases |   best_safe_tidal |   median_safe_tidal |   worst_safe_tidal |   median_safe_nec_integral |   median_safe_flux_integral |
|-----:|:---------------|--------:|--------:|-------------:|----------------:|----------------------:|---------------------------:|------------------:|------------------:|--------------------:|-------------------:|---------------------------:|----------------------------:|
|  1.5 | core           |     0.1 |       9 |            9 |               1 |                     0 |                          0 |                 0 |          1975.43  |            2266.34  |           2835.54  |                   221.055  |                     41.9129 |
|  1.5 | core           |     0.3 |       9 |            9 |               1 |                     0 |                          0 |                 0 |           266     |             279.987 |            286.384 |                    82.7195 |                     12.5838 |
|  2   | core           |     0.1 |       9 |            9 |               1 |                     0 |                          0 |                 0 |          1733.38  |            2371.42  |           2542.82  |                   239.832  |                     40.5785 |
|  2   | core           |     0.3 |       9 |            9 |               1 |                     0 |                          0 |                 0 |           291.285 |             303.042 |            310.147 |                    82.6166 |                     13.3111 |
|  2.5 | core           |     0.1 |       9 |            9 |               1 |                     0 |                          0 |                 0 |          2008.46  |            2403.6   |           2745.88  |                   217.075  |                     41.9267 |
|  2.5 | core           |     0.3 |       9 |            9 |               1 |                     0 |                          0 |                 0 |           301.843 |             320.003 |            328.329 |                    83.723  |                     13.9799 |
|  3   | stretch        |     0.1 |       9 |            9 |               1 |                     0 |                          0 |                 0 |          2113.32  |            2807.54  |           2834.95  |                   234.597  |                     45.2328 |
|  3   | stretch        |     0.3 |       9 |            9 |               1 |                     0 |                          0 |                 0 |           330.634 |             336.618 |            345.295 |                    82.7958 |                     14.3756 |
|  5   | stretch        |     0.1 |       9 |            9 |               1 |                     0 |                          0 |                 0 |          2678.23  |            2905.03  |           3282.74  |                   235.455  |                     49.1417 |
|  5   | stretch        |     0.3 |       9 |            9 |               1 |                     0 |                          0 |                 0 |           374.997 |             385.496 |            392.012 |                    80.8321 |                     15.6865 |
| 10   | extreme_stress |     0.1 |       9 |            9 |               1 |                     0 |                          0 |                 0 |          3270.82  |            3687.92  |           3872.8   |                   240.54   |                     55.1533 |
| 10   | extreme_stress |     0.3 |       9 |            9 |               1 |                     0 |                          0 |                 0 |           454.922 |             457.79  |            461.006 |                    77.4209 |                     17.4913 |

## 5. Initial-data readiness proxy

| tier           |    V | slice_label    |   max_gtt |   gtt_positive_points |   max_abs_beta |   max_abs_R3_proxy |   max_abs_K_trace_proxy |   max_abs_H_lhs_proxy |   max_abs_Gnn |   max_abs_H_minus_2Gnn_proxy |
|:---------------|-----:|:---------------|----------:|----------------------:|---------------:|-------------------:|------------------------:|----------------------:|--------------:|-----------------------------:|
| core           |  2   | catch          |        -1 |                     0 |    0.870297    |           1151.91  |                 8.63086 |              1145.11  |       573.263 |                      84.1132 |
| core           |  2   | shift_release  |        -1 |                     0 |    0.0612932   |           1098.47  |                 1.95921 |              1097.84  |       558.679 |                      87.1655 |
| core           |  2   | throat_release |        -1 |                     0 |    3.91807e-09 |            787.408 |                 1.54472 |               786.856 |       419.244 |                     102.212  |
| core           |  2.5 | catch          |        -1 |                     0 |    0.94478     |           1151.91  |                 8.8327  |              1144.15  |       573.263 |                      84.1132 |
| core           |  2.5 | shift_release  |        -1 |                     0 |    0.0612931   |           1098.47  |                 1.85613 |              1097.86  |       558.68  |                      87.1655 |
| core           |  2.5 | throat_release |        -1 |                     0 |    3.91807e-09 |            787.408 |                 1.48507 |               786.869 |       419.257 |                     102.212  |
| stretch        |  5   | catch          |        -1 |                     0 |    1.19196     |           1151.91  |                 9.27757 |              1140.72  |       573.262 |                      84.4814 |
| stretch        |  5   | shift_release  |        -1 |                     0 |    0.0612931   |           1098.47  |                 1.58369 |              1097.91  |       558.682 |                      87.1655 |
| stretch        |  5   | throat_release |        -1 |                     0 |    3.91807e-09 |            787.408 |                 1.31408 |               786.907 |       419.295 |                     102.212  |
| extreme_stress | 10   | catch          |        -1 |                     0 |    1.46257     |           1151.91  |                 9.47752 |              1136.63  |       573.262 |                      86.681  |
| extreme_stress | 10   | shift_release  |        -1 |                     0 |    0.0612931   |           1098.47  |                 1.44606 |              1097.96  |       558.684 |                      87.1655 |
| extreme_stress | 10   | throat_release |        -1 |                     0 |    3.91807e-09 |            787.408 |                 1.19263 |               786.943 |       419.33  |                     102.212  |

These are proxy diagnostics from the prescribed metric, not a solved constraint system.

## Optional high-V aside, not adopted

This algebraic check is included only as a future high-velocity note for the `V=10` edge shoulder. It is not part of the baseline.

|   V |   beta_W_power | kind                            |   gtt_positive_points |   max_gtt |   min_lapse_shift_margin |
|----:|---------------:|:--------------------------------|----------------------:|----------:|-------------------------:|
|  10 |           1    | algebraic_gtt_only_not_baseline |                     2 |   7.47349 |                -0.243733 |
|  10 |           1.1  | algebraic_gtt_only_not_baseline |                     0 |  -1       |                 1        |
|  10 |           1.2  | algebraic_gtt_only_not_baseline |                     0 |  -1       |                 1        |
|  10 |           1.25 | algebraic_gtt_only_not_baseline |                     0 |  -1       |                 1        |
|  10 |           1.5  | algebraic_gtt_only_not_baseline |                     0 |  -1       |                 1        |
|  10 |           2    | algebraic_gtt_only_not_baseline |                     0 |  -1       |                 1        |

## Bottom line

- Core `V=1.5-2.5`, `Delta=0.3` passenger-worldline clean: **True**.
- Core dense metric maps clean for positive `gtt`: **True**.
- Stretch `V=3,5`, `Delta=0.3` passenger-worldline clean: **True**.
- `V=10` is a stress case; it shows a small dense-map edge issue in the baseline, but that is not a core-range failure and does not justify changing the baseline ansatz yet.
- The next appropriate step is constraint-quality 3+1 initial data for the simple catch-rematched baseline, starting in the core/stretch range, not another ansatz tweak.
