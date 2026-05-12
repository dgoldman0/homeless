# Entrance Branch Reduced Evaluation

## Purpose

This pass evaluates the entrance-side mirror of the throat-loaded gated-shift architecture.

The exit branch already established the preferred release choreography: transport support should fade before throat capacity/lapse support relaxes. The entrance mirror tests the reverse operating sequence: throat capacity/lapse support is preloaded first, then transport/coupling support is admitted as the passenger region approaches the throat.

This file is a reduced numerical/diagnostic report. It is not a full 3+1 evolution, not a geodesic passenger-frame tidal pass, and not a semiclassical stress-energy validation.

## Branch definition

The entrance branch used the same base parameter ladder as the gated-shift reduced evaluation:

- velocities: 0.90, 1.01, 1.10, 1.25, 1.50, 2.00
- capacity settings: 100 and 10,000
- wall settings: 0.3 and 0.1
- release widths: 0.35 and 0.18
- release gaps: 0.35, 0.70, and 1.00 for the ordered families

The mirrored profiles were interpreted as:

| entrance mode | operating meaning |
|---|---|
| synchronized | throat support and transport/coupling support rise together |
| preload_first | throat capacity/lapse support rises before transport/coupling support |
| rapid_preload_first | same ordering with sharper release/activation layer |

The diagnostic grid used 13 entrance-time samples and 91 radial samples per configuration, for 1,183 sampled spacetime points per configuration.

## Executive result

The entrance branch was clean across the full base family.

| metric | result |
|---|---:|
| configurations | 336 |
| sampled spacetime points | 397,488 |
| configurations with positive gtt points | 0 |
| clean entrance configurations | 336 |
| worst max gtt | -1 |
| worst lapse-shift margin | 1 |
| worst null-expansion product | 657.369 |
| worst Kretschmann proxy | 8.0137e+07 |
| worst tidal proxy | 2783.68 |
| mean throat burden share | 0.994833 |
| minimum throat burden share | 0.912338 |

The result is essentially the expected mirror of the clean exit branch under the same reduced symmetry assumptions. The causal-balance monitor stayed clean. The ordinary preload-first family remained mild compared with the rapid family. The rapid preload-first family remained causally clean while producing the largest null-expansion pulse.

## Mode summary

| mode                |   configs |   gtt_positive_configs |   clean_configs |   worst_max_gtt |   worst_min_margin |   worst_theta_product_max |   median_theta_product_max |   worst_Kretsch |   worst_tidal_proxy |   mean_throat_burden_share |   min_throat_burden_share |
|:--------------------|----------:|-----------------------:|----------------:|----------------:|-------------------:|--------------------------:|---------------------------:|----------------:|--------------------:|---------------------------:|--------------------------:|
| preload_first       |       144 |                      0 |             144 |              -1 |                  1 |                   180.106 |                     33.524 |     8.0137e+07  |             2783.68 |                   0.993739 |                  0.912338 |
| rapid_preload_first |       144 |                      0 |             144 |              -1 |                  1 |                   657.369 |                    105.521 |     7.02484e+07 |             2429.99 |                   0.996566 |                  0.944577 |
| synchronized        |        48 |                      0 |              48 |              -1 |                  1 |                   170.442 |                     35.656 |     7.01708e+07 |             2422.28 |                   0.992919 |                  0.912338 |

## Velocity ladder

|    V |   configs |   gtt_positive_configs |   worst_theta_product_max |   median_theta_product_max |   worst_Kretsch |   worst_tidal_proxy |   mean_throat_burden_share |   min_throat_burden_share |
|-----:|----------:|-----------------------:|--------------------------:|---------------------------:|----------------:|--------------------:|---------------------------:|--------------------------:|
| 0.9  |        56 |                      0 |                   146.884 |                    31.7263 |     5.99234e+07 |             1959.48 |                   0.993462 |                  0.912338 |
| 1.01 |        56 |                      0 |                   182.655 |                    39.0268 |     6.07748e+07 |             2046.4  |                   0.993992 |                  0.916311 |
| 1.1  |        56 |                      0 |                   214.349 |                    45.3958 |     6.2317e+07  |             2121.37 |                   0.994377 |                  0.919871 |
| 1.25 |        56 |                      0 |                   272.388 |                    56.9293 |     6.52297e+07 |             2240.71 |                   0.994928 |                  0.925762 |
| 1.5  |        56 |                      0 |                   383.366 |                    78.626  |     7.00791e+07 |             2428.74 |                   0.995647 |                  0.935162 |
| 2    |        56 |                      0 |                   657.369 |                   130.869  |     8.0137e+07  |             2783.68 |                   0.996595 |                  0.951224 |

The entrance-side expansion pulse grows with velocity, matching the exit-side trend. This does not create a causal-balance failure in the sampled base family.

## Wall-thickness sensitivity

|   Delta |   configs |   gtt_positive_configs |   worst_theta_product_max |   median_theta_product_max |   worst_Kretsch |   worst_tidal_proxy |   median_tidal_proxy |   mean_throat_burden_share |   min_throat_burden_share |
|--------:|----------:|-----------------------:|--------------------------:|---------------------------:|----------------:|--------------------:|---------------------:|---------------------------:|--------------------------:|
|     0.1 |       168 |                      0 |                   657.369 |                    50.9517 |     8.0137e+07  |            2783.68  |             1958.84  |                   0.994891 |                  0.912338 |
|     0.3 |       168 |                      0 |                   657.369 |                    51.021  |     1.37478e+06 |             381.116 |              272.942 |                   0.994775 |                  0.917423 |

The thin wall remains the main harshness driver in curvature and tidal-proxy diagnostics. This is consistent with the tidal worldline pass: support-wall smoothing is still the most important passenger-comfort knob.

## Capacity sensitivity

|    C0 |   configs |   gtt_positive_configs |   worst_theta_product_max |   median_theta_product_max |   worst_Kretsch |   worst_tidal_proxy |   median_tidal_proxy |   mean_throat_burden_share |   min_throat_burden_share |
|------:|----------:|-----------------------:|--------------------------:|---------------------------:|----------------:|--------------------:|---------------------:|---------------------------:|--------------------------:|
|   100 |       168 |                      0 |                   494.088 |                    42.6884 |     8.0137e+07  |             2783.68 |              1128.81 |                   0.993855 |                  0.912338 |
| 10000 |       168 |                      0 |                   657.369 |                    60.6588 |     6.75273e+07 |             2123.5  |              1012.76 |                   0.995812 |                  0.946375 |

The larger capacity setting increases the expansion-product envelope but improves throat burden localization in this base entrance sweep. Capacity is active as a performance knob, not the dominant causal-stability knob.

## Release-width sensitivity

|   w_release |   configs |   gtt_positive_configs |   worst_theta_product_max |   median_theta_product_max |   worst_Kretsch |   worst_tidal_proxy |   median_tidal_proxy |   mean_throat_burden_share |   min_throat_burden_share |
|------------:|----------:|-----------------------:|--------------------------:|---------------------------:|----------------:|--------------------:|---------------------:|---------------------------:|--------------------------:|
|        0.18 |       168 |                      0 |                   657.369 |                    95.8413 |     7.02484e+07 |             2429.99 |              1035.72 |                   0.996283 |                  0.942971 |
|        0.35 |       168 |                      0 |                   187.451 |                    31.0206 |     8.0137e+07  |             2783.68 |              1060.23 |                   0.993384 |                  0.912338 |

The sharper activation layer increases the null-expansion product. The broader layer has lower expansion pulse but can still carry large curvature/tidal proxy in thin-wall cases. This keeps the same design lesson as exit: smooth timing helps, but throat-wall smoothing is a separate requirement.

## Worst-case notes

The worst null-expansion product occurred in the rapid preload-first family at the highest sampled velocity. The worst curvature proxy occurred in thin-wall cases. The causal monitor remained clean in both categories.

Top worst-case rows are stored in `entrance_branch_top_worst_cases.csv`.

## Interpretation

The entrance branch does not introduce a new failure mode in the symmetric reduced model.

This is a meaningful check because the entrance operation is not merely a replay of exit timing. The entrance sequence has to establish throat support before admitting transport/coupling. The reduced scan shows that this mirrored sequencing preserves the same causal-balance organization as the exit branch.

The main engineering implication is straightforward: entrance and exit can share one operating doctrine.

- Entrance: preload support first, then admit transport/coupling.
- Exit: remove transport/coupling first, then relax support.

That gives one coherent control law: transport should remain inside active throat support at both ends of the cycle.

## Remaining limitations

This pass uses reduced spherical/radial diagnostics. It does not resolve full 3+1 initial-data quality, cabin-frame tidal tensors, semiclassical constraints, or perturbative stability.

The next useful entrance-side refinement is not a wider brute-force scan. It is a targeted high-resolution check around the rapid preload-first expansion pulse and a passenger-frame tidal comparison through entrance, traversal, and exit.

## Output files

- `entrance_branch_base_family_cases.csv`
- `entrance_branch_mode_summary.csv`
- `entrance_branch_velocity_summary.csv`
- `entrance_branch_delta_summary.csv`
- `entrance_branch_capacity_summary.csv`
- `entrance_branch_release_width_summary.csv`
- `entrance_branch_top_worst_cases.csv`
- `entrance_branch_summary.json`
