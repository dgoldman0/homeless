# Composite v1/catch-rematched gate ablation summary

Reduced screening harness: v1-like B/R/N throat infrastructure plus catch-rematched throat-gated packet. This is diagnostic, not a constraint-quality solve.

## V=2.5

| case | causal fail | packet max gtt | edge max gtt | packet max norm | edge margin | packet-boundary tidal ratio | support-edge tidal ratio |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline_full_v1_like | 0 | -1 | -1.03 | -0.75 | 1.01 | 1 | 1 |
| no_B_prestretch | 0 | -1 | -1.03 | -0.75 | 1.01 | 2.51 | 0.413 |
| half_B_prestretch | 0 | -1 | -1.03 | -0.75 | 1.01 | 1.35 | 0.76 |
| no_R_flare_gate | 0 | -1 | -1.03 | -0.75 | 1.01 | 1 | 1 |
| half_R_flare_gate | 0 | -1 | -1.03 | -0.75 | 1.01 | 1 | 1 |
| no_N_edge_lapse_shape | 0 | -1 | -1.02 | -0.75 | 1.01 | 1.03 | 1.05 |
| half_N_edge_lapse_shape | 0 | -1 | -1.02 | -0.75 | 1.01 | 1.02 | 1.02 |
| short_quiet_hold | 0 | -1 | -1 | -0.75 | 1 | 1.28 | 0.997 |
| no_quiet_hold | 0 | -1 | -1 | -0.75 | 1 | 1.33 | 0.978 |
| stronger_edge_shift_gating_p2 | 0 | -1 | -1.03 | -0.75 | 1.01 | 1 | 1 |
| relaxed_B_R_no_hold | 0 | -1 | -1 | -0.75 | 1 | 0.656 | 0.407 |
| no_N_no_hold | 0 | -1 | -1 | -0.75 | 1 | 1.36 | 1.01 |

## V=5.0

| case | causal fail | packet max gtt | edge max gtt | packet max norm | edge margin | packet-boundary tidal ratio | support-edge tidal ratio |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline_full_v1_like | 0 | -1 | -1.03 | -0.75 | 1.02 | 1 | 1 |
| no_B_prestretch | 0 | -1 | -1.03 | -0.75 | 1.02 | 2.56 | 0.397 |
| half_B_prestretch | 0 | -1 | -1.03 | -0.75 | 1.02 | 1.4 | 0.756 |
| no_R_flare_gate | 0 | -1 | -1.03 | -0.75 | 1.02 | 1 | 1 |
| half_R_flare_gate | 0 | -1 | -1.03 | -0.75 | 1.02 | 1 | 1 |
| no_N_edge_lapse_shape | 0 | -1 | -1.02 | -0.75 | 1.01 | 1.02 | 1.05 |
| half_N_edge_lapse_shape | 0 | -1 | -1.03 | -0.75 | 1.01 | 1.01 | 1.02 |
| short_quiet_hold | 0 | -1 | -1 | -0.75 | 1 | 1 | 1.01 |
| no_quiet_hold | 0 | -1 | -1 | -0.75 | 1 | 1.06 | 0.996 |
| stronger_edge_shift_gating_p2 | 0 | -1 | -1.03 | -0.75 | 1.02 | 1 | 1 |
| relaxed_B_R_no_hold | 0 | -1 | -1 | -0.75 | 1 | 0.542 | 0.404 |
| no_N_no_hold | 0 | -1 | -1 | -0.75 | 1 | 1.08 | 1.03 |

## V=10.0

| case | causal fail | packet max gtt | edge max gtt | packet max norm | edge margin | packet-boundary tidal ratio | support-edge tidal ratio |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline_full_v1_like | 0 | -1 | -1.03 | -0.75 | 1.02 | 1 | 1 |
| no_B_prestretch | 0 | -1 | -1.03 | -0.75 | 1.02 | 2.61 | 0.374 |
| half_B_prestretch | 0 | -1 | -1.03 | -0.75 | 1.02 | 1.44 | 0.75 |
| no_R_flare_gate | 0 | -1 | -1.03 | -0.75 | 1.02 | 1 | 1 |
| half_R_flare_gate | 0 | -1 | -1.03 | -0.75 | 1.02 | 1 | 1 |
| no_N_edge_lapse_shape | 0 | -1 | -1.02 | -0.75 | 1.01 | 1.02 | 1.05 |
| half_N_edge_lapse_shape | 0 | -1 | -1.03 | -0.75 | 1.01 | 1.01 | 1.02 |
| short_quiet_hold | 0 | -1 | -1 | -0.75 | 1 | 0.792 | 1.03 |
| no_quiet_hold | 0 | -1 | -1 | -0.749 | 1 | 0.865 | 1.02 |
| stronger_edge_shift_gating_p2 | 0 | -1 | -1.03 | -0.75 | 1.02 | 1 | 1 |
| relaxed_B_R_no_hold | 0 | -1 | -1 | -0.749 | 1 | 0.459 | 0.397 |
| no_N_no_hold | 0 | -1 | -1 | -0.749 | 1 | 0.88 | 1.05 |

