# Derived report tables
Generated from the JSON files in `data/` by `code/build_report_tables.py`.

## Catch timing thresholds
| V | lambda | first packet fail x_catch | delta vs beta | first packet gtt fail x_catch | first edge gtt fail x_catch |
|---:|---:|---:|---:|---:|---:|
| 5 | 3 | 0.65 | -0.05 | -0.2 | none |
| 5 | 5 | 0.7 | -1.11e-16 | none | none |
| 10 | 6 | 0.6 | -0.1 | -0.2 | 0.9 |
| 10 | 11.5 | 0.6 | -0.1 | none | none |

## R-flare highlights
| V | lambda | variant | packet fail | passive gtt fail | packet max norm | min flare d2 | packet angular tidal x base | edge theta x base |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 2.5 | 2.88 | baseline_R_fades_with_q | False | False | -0.75 | 5.63 | 1 | 1 |
| 2.5 | 2.88 | R_always_open | False | False | -0.75 | 2.74 | 0.995 | 0.739 |
| 2.5 | 2.88 | R_always_flat | False | False | -0.75 | 4.97 | 1.05 | 0.663 |
| 2.5 | 2.88 | R_sharp_release | False | False | -0.75 | 4.97 | 4.04 | 0.948 |
| 2.5 | 2.88 | R_slow_release | False | False | -0.75 | 8.05 | 1.01 | 0.898 |
| 2.5 | 2.88 | R_always_open_no_quiet_hold | False | False | -0.75 | 2 | 1.34 | 0.724 |
| 2.5 | 2.88 | R_flat_no_quiet_hold | False | False | -0.75 | 0.22 | 1.34 | 0.64 |
| 5 | 3 | baseline_R_fades_with_q | False | True | -0.75 | 5.63 | 1 | 1 |
| 5 | 3 | R_always_open | False | True | -0.75 | 2.74 | 0.995 | 0.739 |
| 5 | 3 | R_always_flat | False | True | -0.75 | 4.97 | 1.05 | 0.661 |
| 5 | 3 | R_sharp_release | False | True | -0.75 | 4.97 | 4.01 | 0.943 |
| 5 | 3 | R_slow_release | False | True | -0.75 | 8.05 | 1.01 | 0.897 |
| 5 | 3 | R_always_open_no_quiet_hold | False | True | -0.75 | 2 | 1.32 | 0.725 |
| 5 | 3 | R_flat_no_quiet_hold | False | True | -0.75 | 0.22 | 1.32 | 0.64 |
| 5 | 5.75 | baseline_R_fades_with_q | False | False | -0.75 | 5.63 | 1 | 1 |
| 5 | 5.75 | R_always_open | False | False | -0.75 | 2.74 | 0.996 | 0.731 |
| 5 | 5.75 | R_always_flat | False | False | -0.75 | 4.97 | 1.05 | 0.636 |
| 5 | 5.75 | R_sharp_release | False | False | -0.75 | 4.97 | 3.62 | 0.859 |
| 5 | 5.75 | R_slow_release | False | False | -0.75 | 8.05 | 1.01 | 0.893 |
| 5 | 5.75 | R_always_open_no_quiet_hold | False | False | -0.75 | 2 | 1.06 | 0.739 |
| 5 | 5.75 | R_flat_no_quiet_hold | False | False | -0.75 | 0.22 | 1.06 | 0.635 |
| 10 | 6 | baseline_R_fades_with_q | False | True | -0.75 | 5.63 | 1 | 1 |
| 10 | 6 | R_always_open | False | True | -0.75 | 2.74 | 0.996 | 0.731 |
| 10 | 6 | R_always_flat | False | True | -0.75 | 4.97 | 1.05 | 0.635 |
| 10 | 6 | R_sharp_release | False | True | -0.75 | 4.97 | 3.6 | 0.853 |
| 10 | 6 | R_slow_release | False | True | -0.75 | 8.05 | 1.01 | 0.892 |
| 10 | 6 | R_always_open_no_quiet_hold | True | True | 449 | 2 | 1.05 | 0.74 |
| 10 | 6 | R_flat_no_quiet_hold | True | True | 449 | 0.22 | 1.05 | 0.635 |
| 10 | 11.5 | baseline_R_fades_with_q | False | False | -0.75 | 5.63 | 1 | 1 |
| 10 | 11.5 | R_always_open | False | False | -0.75 | 2.74 | 0.997 | 0.744 |
| 10 | 11.5 | R_always_flat | False | False | -0.75 | 4.97 | 1.05 | 0.601 |
| 10 | 11.5 | R_sharp_release | False | False | -0.75 | 4.97 | 3.28 | 0.8 |
| 10 | 11.5 | R_slow_release | False | False | -0.75 | 8.05 | 1.01 | 0.924 |
| 10 | 11.5 | R_always_open_no_quiet_hold | False | False | -0.749 | 2 | 0.852 | 0.756 |
| 10 | 11.5 | R_flat_no_quiet_hold | False | False | -0.749 | 0.22 | 0.853 | 0.626 |

## Slim and edge-gating highlights
| V | lambda | variant | packet fail | passive gtt fail | packet max norm | packet angular tidal x base | edge angular tidal x base | edge theta x base |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 5 | 3 | slim_short_hold_Ropen_halfB_halfN | False | True | -0.75 | 1.33 | 0.857 | 0.58 |
| 5 | 3 | very_slim_nohold_Ropen_noB_noN | False | True | -0.75 | 1.32 | 1.06 | 0.384 |
| 5 | 3 | very_slim_plus_pbeta2 | False | True | -0.75 | 1.32 | 1.06 | 0.384 |
| 5 | 3 | baseline_plus_pbeta2 | False | True | -0.75 | 0.995 | 1 | 1 |
| 5 | 3 | latecatch_at_beta_pbeta_1 | True | True | 988 | 0.998 | 1 | 1 |
| 5 | 3 | latecatch_at_beta_pbeta_2 | True | True | 2.52e+03 | 0.995 | 1 | 1 |
| 5 | 3 | latecatch_at_beta_pbeta_4 | True | True | 6.36e+03 | 0.994 | 1 | 1 |
| 5 | 5.75 | slim_short_hold_Ropen_halfB_halfN | False | False | -0.75 | 1.05 | 0.892 | 0.575 |
| 5 | 5.75 | very_slim_nohold_Ropen_noB_noN | False | False | -0.75 | 1.06 | 1.35 | 0.388 |
| 5 | 5.75 | very_slim_plus_pbeta2 | False | False | -0.75 | 1.06 | 1.35 | 0.388 |
| 5 | 5.75 | baseline_plus_pbeta2 | False | False | -0.75 | 0.996 | 1 | 1 |
| 5 | 5.75 | latecatch_at_beta_pbeta_1 | True | False | 70.9 | 0.999 | 1 | 1 |
| 5 | 5.75 | latecatch_at_beta_pbeta_2 | True | False | 158 | 0.996 | 1 | 1 |
| 5 | 5.75 | latecatch_at_beta_pbeta_4 | True | False | 328 | 0.995 | 1 | 1 |
| 10 | 6 | slim_short_hold_Ropen_halfB_halfN | False | True | -0.75 | 1.04 | 0.895 | 0.577 |
| 10 | 6 | very_slim_nohold_Ropen_noB_noN | True | True | 498 | 1.05 | 1.38 | 0.388 |
| 10 | 6 | very_slim_plus_pbeta2 | True | True | 513 | 1.05 | 1.38 | 0.388 |
| 10 | 6 | baseline_plus_pbeta2 | False | True | -0.75 | 0.996 | 1 | 1 |
| 10 | 6 | latecatch_at_beta_pbeta_1 | True | True | 9.91e+03 | 0.996 | 1 | 1 |
| 10 | 6 | latecatch_at_beta_pbeta_2 | True | True | 1.86e+04 | 0.996 | 1 | 1 |
| 10 | 6 | latecatch_at_beta_pbeta_4 | True | True | 3.78e+04 | 0.995 | 1 | 1 |
| 10 | 11.5 | slim_short_hold_Ropen_halfB_halfN | False | False | -0.75 | 0.84 | 0.954 | 0.604 |
| 10 | 11.5 | very_slim_nohold_Ropen_noB_noN | False | False | -0.749 | 0.854 | 1.74 | 0.427 |
| 10 | 11.5 | very_slim_plus_pbeta2 | False | False | -0.749 | 0.854 | 1.74 | 0.427 |
| 10 | 11.5 | baseline_plus_pbeta2 | False | False | -0.75 | 0.997 | 1 | 1 |
| 10 | 11.5 | latecatch_at_beta_pbeta_1 | True | False | 1.72e+03 | 0.997 | 1 | 1 |
| 10 | 11.5 | latecatch_at_beta_pbeta_2 | True | False | 3.23e+03 | 0.996 | 1 | 1 |
| 10 | 11.5 | latecatch_at_beta_pbeta_4 | True | False | 6.11e+03 | 0.996 | 1 | 1 |
