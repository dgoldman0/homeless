# Composite gate detailed diagnostics

Reduced follow-up focused on failure location, catch timing thresholds, and gate classification. Still a screening harness, not a constraint-quality solve.

## Catch timing thresholds

Baseline has `x_beta=0.70`, `x_q=1.25`. The table varies `x_catch` while holding shift fade and throat relaxation fixed. Negative delta means catch starts before shift fade.

| V | lambda | first packet-norm fail x_catch | delta vs beta | first packet gtt fail x_catch | delta vs beta | first edge gtt fail x_catch | delta vs beta |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 3 | 0.65 | -0.05 | -0.2 | -0.9 | none | none |
| 5 | 5 | 0.7 | -1.11e-16 | none | none | none | none |
| 10 | 6 | 0.6 | -0.1 | -0.2 | -0.9 | 0.9 | 0.2 |
| 10 | 11.5 | 0.6 | -0.1 | none | none | none | none |

## Selected failure states

| V | lambda | case | packet norm fail pts | packet max norm | at s | at l | U | E | q | W | S | edge gtt fail pts | edge max gtt | edge s | edge l | edge U/E/q/W/S |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 5 | 5 | baseline | 0 | -0.75 | 1.65 | 1.99 | 0.5 | 2.6e-05 | 0.0116 | 1.92e-11 | 0.579 | 0 | -1.03 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 5 | 5 | no_hold | 0 | -0.75 | 0.887 | 1.23 | 0.5 | 0.000431 | 0.000672 | 0.0125 | 0.523 | 0 | -1 | 1.58 | 1.16 | 0.5/2e-07/3.2e-07/0.052/0.087 |
| 5 | 5 | edge_reinforced_p2 | 0 | -0.75 | 1.65 | 1.99 | 0.5 | 2.6e-05 | 0.0116 | 1.92e-11 | 0.579 | 0 | -1.03 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 5 | 5 | late_catch_after_shift | 668 | 1.1e+03 | 0.633 | 0.979 | 4.8 | 0.677 | 0.999 | 0.587 | 0.537 | 0 | -1.03 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 5 | 5 | late_catch_after_relax | 5177 | 1.62e+04 | 1.06 | 0.711 | 4.96 | 0.0181 | 0.892 | 0.984 | 0.509 | 0 | -1.03 | 1.58 | 1.16 | 1.1/5.9e-05/0.026/0.052/0.087 |
| 5 | 3 | baseline | 0 | -0.75 | 1.65 | 1.99 | 0.5 | 2.6e-05 | 0.0116 | 1.92e-11 | 0.579 | 0 | -1.02 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 5 | 3 | no_hold | 0 | -0.75 | 0.887 | 1.23 | 0.5 | 0.000431 | 0.000672 | 0.0125 | 0.523 | 0 | -1 | 1.58 | 1.16 | 0.5/2e-07/3.2e-07/0.052/0.087 |
| 5 | 3 | edge_reinforced_p2 | 0 | -0.75 | 1.65 | 1.99 | 0.5 | 2.6e-05 | 0.0116 | 1.92e-11 | 0.579 | 0 | -1.02 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 5 | 3 | late_catch_after_shift | 967 | 2.77e+04 | 0.707 | 0.357 | 4.54 | 0.481 | 0.998 | 0.999 | 0.502 | 0 | -1.02 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 5 | 3 | late_catch_after_relax | 6225 | 1.09e+05 | 0.887 | 0.54 | 4.99 | 0.111 | 0.983 | 0.997 | 0.522 | 0 | -1.02 | 1.58 | 1.16 | 1.1/5.9e-05/0.026/0.052/0.087 |
| 10 | 11.5 | baseline | 0 | -0.75 | 1.65 | 1.99 | 0.5 | 2.6e-05 | 0.0116 | 1.92e-11 | 0.579 | 0 | -1.03 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 10 | 11.5 | no_hold | 0 | -0.749 | 0.814 | 1.16 | 0.502 | 0.000978 | 0.00152 | 0.0517 | 0.517 | 0 | -1 | 1.58 | 1.16 | 0.5/2e-07/3.2e-07/0.052/0.087 |
| 10 | 11.5 | edge_reinforced_p2 | 0 | -0.75 | 1.65 | 1.99 | 0.5 | 2.6e-05 | 0.0116 | 1.92e-11 | 0.579 | 0 | -1.03 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 10 | 11.5 | late_catch_after_shift | 980 | 8.41e+03 | 0.617 | 0.967 | 9.66 | 0.716 | 0.999 | 0.634 | 0.502 | 0 | -1.03 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 10 | 11.5 | late_catch_after_relax | 5515 | 6.11e+04 | 1.09 | 0.747 | 9.86 | 0.0126 | 0.852 | 0.975 | 0.54 | 0 | -1.03 | 1.58 | 1.16 | 1.8/5.9e-05/0.026/0.052/0.087 |
| 10 | 6 | baseline | 0 | -0.75 | 1.65 | 1.99 | 0.5 | 2.6e-05 | 0.0116 | 1.92e-11 | 0.579 | 0 | -1.03 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 10 | 6 | no_hold | 9 | 277 | 0.158 | -0.191 | 5.02 | 0.589 | 0.691 | 1 | 0.51 | 0 | -1 | 1.58 | 1.16 | 0.5/2e-07/3.2e-07/0.052/0.087 |
| 10 | 6 | edge_reinforced_p2 | 0 | -0.75 | 1.65 | 1.99 | 0.5 | 2.6e-05 | 0.0116 | 1.92e-11 | 0.579 | 0 | -1.03 | 1.58 | 1.16 | 0.5/5.9e-05/0.026/0.052/0.087 |
| 10 | 6 | late_catch_after_shift | 1325 | 1.07e+05 | 0.707 | 0.357 | 9.02 | 0.481 | 0.998 | 0.999 | 0.502 | 3 | 543 | 0.609 | 0.893 | 9.7/0.73/1/0.84/0.88 |
| 10 | 6 | late_catch_after_relax | 6676 | 4.46e+05 | 0.887 | 0.54 | 9.99 | 0.111 | 0.983 | 0.997 | 0.522 | 9 | 4.74e+03 | 0.609 | 0.893 | 10/0.73/1/0.84/0.88 |

## Tidal/curvature gate notes from the first ablation

| V | case | packet-boundary tidal ratio | support-edge tidal ratio | packet-boundary Kretsch ratio | support-edge Kretsch ratio |
|---:|---|---:|---:|---:|---:|
| 2.5 | baseline_full_v1_like | 1 | 1 | 1 | 1 |
| 2.5 | no_B_prestretch | 2.51 | 0.413 | 6.08 | 0.278 |
| 2.5 | half_B_prestretch | 1.35 | 0.76 | 1.86 | 0.608 |
| 2.5 | no_N_edge_lapse_shape | 1.03 | 1.05 | 1.03 | 1.1 |
| 2.5 | no_quiet_hold | 1.33 | 0.978 | 1.23 | 1.02 |
| 2.5 | relaxed_B_R_no_hold | 0.656 | 0.407 | 0.498 | 0.306 |
| 5 | baseline_full_v1_like | 1 | 1 | 1 | 1 |
| 5 | no_B_prestretch | 2.56 | 0.397 | 6.31 | 0.422 |
| 5 | half_B_prestretch | 1.4 | 0.756 | 1.96 | 0.58 |
| 5 | no_N_edge_lapse_shape | 1.02 | 1.05 | 1.02 | 1.1 |
| 5 | no_quiet_hold | 1.06 | 0.996 | 0.813 | 0.963 |
| 5 | relaxed_B_R_no_hold | 0.542 | 0.404 | 0.334 | 0.465 |
| 10 | baseline_full_v1_like | 1 | 1 | 1 | 1 |
| 10 | no_B_prestretch | 2.61 | 0.374 | 6.56 | 0.642 |
| 10 | half_B_prestretch | 1.44 | 0.75 | 2.06 | 0.565 |
| 10 | no_N_edge_lapse_shape | 1.02 | 1.05 | 1.02 | 1.1 |
| 10 | no_quiet_hold | 0.865 | 1.02 | 0.596 | 0.967 |
| 10 | relaxed_B_R_no_hold | 0.459 | 0.397 | 0.25 | 0.705 |
