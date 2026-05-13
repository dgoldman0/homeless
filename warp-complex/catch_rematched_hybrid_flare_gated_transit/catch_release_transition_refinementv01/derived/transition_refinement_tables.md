# Catch/release transition refinement results

The refinement pass evaluates stressed service at $V=10$ and $\lambda=6$ with v1 throat geometry, R-open service posture, B-aware packet choreography, paired capacity/lapse support, and ADM source-demand proxies.

## Confirmed candidates

| candidate | clear | rel source cost | max packet norm | max edge gtt | rel packet j | rel edge j | rel release j | x_catch | x_beta | x_q | widths | p_beta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| earlycatch_medium_p4 | True | 0.939 | -0.704 | -1.35 | 0.603 | 0.603 | 0.603 | 0.05 | 0.70 | 1.25 | 0.25/0.28/0.30 | 4.0 |
| longgap_medium_p4 | True | 0.941 | -0.704 | -2.05 | 0.612 | 0.612 | 0.612 | 0.05 | 0.70 | 1.45 | 0.25/0.28/0.30 | 4.0 |
| earlycatch_medium_p3 | True | 0.986 | -0.704 | -1.35 | 0.91 | 0.91 | 0.91 | 0.05 | 0.70 | 1.25 | 0.25/0.28/0.30 | 3.0 |
| longgap_medium_p3 | True | 0.989 | -0.704 | -2.05 | 0.925 | 0.925 | 0.925 | 0.05 | 0.70 | 1.45 | 0.25/0.28/0.30 | 3.0 |
| baseline_p4_open | True | 1 | -0.194 | -1.19 | 1 | 1 | 1 | 0.25 | 0.70 | 1.25 | 0.18/0.20/0.20 | 4.0 |
| earlycatch_medium_p2 | True | 1.05 | -0.704 | -1.35 | 1.34 | 1.34 | 1.34 | 0.05 | 0.70 | 1.25 | 0.25/0.28/0.30 | 2.0 |
| longgap_medium_p2 | True | 1.06 | -0.704 | -2.05 | 1.36 | 1.36 | 1.36 | 0.05 | 0.70 | 1.45 | 0.25/0.28/0.30 | 2.0 |
| earlycatch_smooth_p4 | False | 0.971 | 0.259 | -1.49 | 0.81 | 0.81 | 0.81 | 0.05 | 0.70 | 1.25 | 0.35/0.38/0.42 | 4.0 |

## Design selection

`earlycatch_medium_p4` is the selected transition-layer direction in this pass. It keeps packet, support-edge, and release-edge clearance and gives relative source cost `0.939` against the baseline value `1.0`.

The selected structure moves catch earlier and uses medium-width transition profiles while retaining the strong support-edge exponent. This reduces source-current demand and improves packet-timelike margin.
