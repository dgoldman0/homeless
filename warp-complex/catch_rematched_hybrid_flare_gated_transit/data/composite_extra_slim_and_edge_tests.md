# Extra composite slim-architecture and edge-gating tests

Small add-on screen focused on whether multiple relaxations combine safely, and whether stronger W^p_beta edge shift gating rescues late-catch failures.

## V=5, lambda=3

| variant | packet fail | passive gtt fail | packet max norm | edge max gtt | packet angular tidal ×base | edge angular tidal ×base | edge theta-prod ×base |
|---|---:|---:|---:|---:|---:|---:|---:|
| slim_short_hold_Ropen_halfB_halfN | 0 | 1 | -0.75 | -1 | 1.33 | 0.857 | 0.58 |
| very_slim_nohold_Ropen_noB_noN | 0 | 1 | -0.75 | -1 | 1.32 | 1.06 | 0.384 |
| very_slim_plus_pbeta2 | 0 | 1 | -0.75 | -1 | 1.32 | 1.06 | 0.384 |
| flat_very_slim_nohold_noB_noN | 0 | 1 | -0.75 | -1 | 1.32 | 1.1 | 0.183 |
| baseline_plus_pbeta2 | 0 | 1 | -0.75 | -1.02 | 0.995 | 1 | 1 |
| pbeta_sweep_1 | 0 | 1 | -0.75 | -1.02 | 1 | 1 | 1 |
| pbeta_sweep_1.25 | 0 | 1 | -0.75 | -1.02 | 0.997 | 1 | 1 |
| pbeta_sweep_1.5 | 0 | 1 | -0.75 | -1.02 | 0.996 | 1 | 1 |
| pbeta_sweep_2 | 0 | 1 | -0.75 | -1.02 | 0.995 | 1 | 1 |
| pbeta_sweep_3 | 0 | 1 | -0.75 | -1.02 | 0.994 | 1 | 1 |
| pbeta_sweep_4 | 0 | 1 | -0.75 | -1.02 | 0.994 | 1 | 1 |
| latecatch_at_beta_pbeta_1 | 1 | 1 | 988 | -1.02 | 0.998 | 1 | 1 |
| latecatch_at_beta_pbeta_1.5 | 1 | 1 | 1.7e+03 | -1.02 | 0.996 | 1 | 1 |
| latecatch_at_beta_pbeta_2 | 1 | 1 | 2.52e+03 | -1.02 | 0.995 | 1 | 1 |
| latecatch_at_beta_pbeta_3 | 1 | 1 | 4.38e+03 | -1.02 | 0.994 | 1 | 1 |
| latecatch_at_beta_pbeta_4 | 1 | 1 | 6.36e+03 | -1.02 | 0.994 | 1 | 1 |

## V=5, lambda=5.75

| variant | packet fail | passive gtt fail | packet max norm | edge max gtt | packet angular tidal ×base | edge angular tidal ×base | edge theta-prod ×base |
|---|---:|---:|---:|---:|---:|---:|---:|
| slim_short_hold_Ropen_halfB_halfN | 0 | 0 | -0.75 | -1 | 1.05 | 0.892 | 0.575 |
| very_slim_nohold_Ropen_noB_noN | 0 | 0 | -0.75 | -1 | 1.06 | 1.35 | 0.388 |
| very_slim_plus_pbeta2 | 0 | 0 | -0.75 | -1 | 1.06 | 1.35 | 0.388 |
| flat_very_slim_nohold_noB_noN | 0 | 0 | -0.75 | -1 | 1.06 | 1.41 | 0.189 |
| baseline_plus_pbeta2 | 0 | 0 | -0.75 | -1.03 | 0.996 | 1 | 1 |
| pbeta_sweep_1 | 0 | 0 | -0.75 | -1.03 | 1 | 1 | 1 |
| pbeta_sweep_1.25 | 0 | 0 | -0.75 | -1.03 | 0.998 | 1 | 1 |
| pbeta_sweep_1.5 | 0 | 0 | -0.75 | -1.03 | 0.997 | 1 | 1 |
| pbeta_sweep_2 | 0 | 0 | -0.75 | -1.03 | 0.996 | 1 | 1 |
| pbeta_sweep_3 | 0 | 0 | -0.75 | -1.03 | 0.995 | 1 | 1 |
| pbeta_sweep_4 | 0 | 0 | -0.75 | -1.03 | 0.995 | 1 | 1 |
| latecatch_at_beta_pbeta_1 | 1 | 0 | 70.9 | -1.03 | 0.999 | 1 | 1 |
| latecatch_at_beta_pbeta_1.5 | 1 | 0 | 119 | -1.03 | 0.996 | 1 | 1 |
| latecatch_at_beta_pbeta_2 | 1 | 0 | 158 | -1.03 | 0.996 | 1 | 1 |
| latecatch_at_beta_pbeta_3 | 1 | 0 | 256 | -1.03 | 0.995 | 1 | 1 |
| latecatch_at_beta_pbeta_4 | 1 | 0 | 328 | -1.03 | 0.995 | 1 | 1 |

## V=10, lambda=6

| variant | packet fail | passive gtt fail | packet max norm | edge max gtt | packet angular tidal ×base | edge angular tidal ×base | edge theta-prod ×base |
|---|---:|---:|---:|---:|---:|---:|---:|
| slim_short_hold_Ropen_halfB_halfN | 0 | 1 | -0.75 | -1 | 1.04 | 0.895 | 0.577 |
| very_slim_nohold_Ropen_noB_noN | 1 | 1 | 498 | -1 | 1.05 | 1.38 | 0.388 |
| very_slim_plus_pbeta2 | 1 | 1 | 513 | -1 | 1.05 | 1.38 | 0.388 |
| flat_very_slim_nohold_noB_noN | 1 | 1 | 498 | -1 | 1.05 | 1.43 | 0.19 |
| baseline_plus_pbeta2 | 0 | 1 | -0.75 | -1.03 | 0.996 | 1 | 1 |
| pbeta_sweep_1 | 0 | 1 | -0.75 | -1.03 | 1 | 1 | 1 |
| pbeta_sweep_1.25 | 0 | 1 | -0.75 | -1.03 | 0.998 | 1 | 1 |
| pbeta_sweep_1.5 | 0 | 1 | -0.75 | -1.03 | 0.997 | 1 | 1 |
| pbeta_sweep_2 | 0 | 1 | -0.75 | -1.03 | 0.996 | 1 | 1 |
| pbeta_sweep_3 | 0 | 1 | -0.75 | -1.03 | 0.995 | 1 | 1 |
| pbeta_sweep_4 | 0 | 1 | -0.75 | -1.03 | 0.995 | 1 | 1 |
| latecatch_at_beta_pbeta_1 | 1 | 1 | 9.91e+03 | -1.03 | 0.996 | 1 | 1 |
| latecatch_at_beta_pbeta_1.5 | 1 | 1 | 1.4e+04 | -1.03 | 0.996 | 1 | 1 |
| latecatch_at_beta_pbeta_2 | 1 | 1 | 1.86e+04 | -1.03 | 0.996 | 1 | 1 |
| latecatch_at_beta_pbeta_3 | 1 | 1 | 2.78e+04 | -1.03 | 0.995 | 1 | 1 |
| latecatch_at_beta_pbeta_4 | 1 | 1 | 3.78e+04 | -1.03 | 0.995 | 1 | 1 |

## V=10, lambda=11.5

| variant | packet fail | passive gtt fail | packet max norm | edge max gtt | packet angular tidal ×base | edge angular tidal ×base | edge theta-prod ×base |
|---|---:|---:|---:|---:|---:|---:|---:|
| slim_short_hold_Ropen_halfB_halfN | 0 | 0 | -0.75 | -1 | 0.84 | 0.954 | 0.604 |
| very_slim_nohold_Ropen_noB_noN | 0 | 0 | -0.749 | -1 | 0.854 | 1.74 | 0.427 |
| very_slim_plus_pbeta2 | 0 | 0 | -0.749 | -1 | 0.854 | 1.74 | 0.427 |
| flat_very_slim_nohold_noB_noN | 0 | 0 | -0.749 | -1 | 0.853 | 1.82 | 0.196 |
| baseline_plus_pbeta2 | 0 | 0 | -0.75 | -1.03 | 0.997 | 1 | 1 |
| pbeta_sweep_1 | 0 | 0 | -0.75 | -1.03 | 1 | 1 | 1 |
| pbeta_sweep_1.25 | 0 | 0 | -0.75 | -1.03 | 0.998 | 1 | 1 |
| pbeta_sweep_1.5 | 0 | 0 | -0.75 | -1.03 | 0.997 | 1 | 1 |
| pbeta_sweep_2 | 0 | 0 | -0.75 | -1.03 | 0.997 | 1 | 1 |
| pbeta_sweep_3 | 0 | 0 | -0.75 | -1.03 | 0.996 | 1 | 1 |
| pbeta_sweep_4 | 0 | 0 | -0.75 | -1.03 | 0.996 | 1 | 1 |
| latecatch_at_beta_pbeta_1 | 1 | 0 | 1.72e+03 | -1.03 | 0.997 | 1 | 1 |
| latecatch_at_beta_pbeta_1.5 | 1 | 0 | 2.43e+03 | -1.03 | 0.997 | 1 | 1 |
| latecatch_at_beta_pbeta_2 | 1 | 0 | 3.23e+03 | -1.03 | 0.996 | 1 | 1 |
| latecatch_at_beta_pbeta_3 | 1 | 0 | 4.73e+03 | -1.03 | 0.996 | 1 | 1 |
| latecatch_at_beta_pbeta_4 | 1 | 0 | 6.11e+03 | -1.03 | 0.996 | 1 | 1 |

