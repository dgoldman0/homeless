# Exact-v1 Composite Viability Atlas
Reduced tests for the Reference Geometry v0.3 throat controls combined with the catch-rematched throat-loaded packet.
The metric used in the screen is
```math
ds^2=-\alpha^2 d\sigma^2+\gamma_{ll}(dl+\beta^l d\sigma)^2+\gamma_{\Omega\Omega}d\Omega^2
```
with exact v1 controls $N_{v1}$, $B_{v1}$, and $R_{v1}$, packet lapse/capacity factors, and catch-rematched throat-gated shift.
```math
\alpha=N_{v1}T_{pkt},\qquad \gamma_{ll}=(B_{v1}A_{pkt})^2,\qquad \gamma_{\Omega\Omega}=(R_{v1}A_{pkt})^2
```
```math
\beta^l=-U(s)E(s)W(l)^{p_\beta}S(l-X(s))/B_{v1}
```
## Baseline and R-state checks
| V | lambda | R mode | packet clear | edge clear | flare clear | packet max norm | release edge max gtt | min edge margin | min flare d2 |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2.5 | 2.88 | v1 | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 0.001794 |
| 2.5 | 2.88 | always_open | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 2.225 |
| 2.5 | 2.88 | always_flat | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 0.001794 |
| 2.5 | 2.88 | half_amplitude | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 0.001794 |
| 2.5 | 2.88 | delayed_close | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 2.225 |
| 5 | 5.75 | v1 | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 0.001794 |
| 5 | 5.75 | always_open | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 2.225 |
| 5 | 5.75 | always_flat | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 0.001794 |
| 5 | 5.75 | half_amplitude | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 0.001794 |
| 5 | 5.75 | delayed_close | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 2.225 |
| 10 | 11.5 | v1 | 1 | 1 | 1 | -0.75 | -1.025 | 1.013 | 0.001794 |
| 10 | 11.5 | always_open | 1 | 1 | 1 | -0.75 | -1.025 | 1.013 | 2.225 |
| 10 | 11.5 | always_flat | 1 | 1 | 1 | -0.75 | -1.025 | 1.013 | 0.001794 |
| 10 | 11.5 | half_amplitude | 1 | 1 | 1 | -0.75 | -1.025 | 1.013 | 0.001794 |
| 10 | 11.5 | delayed_close | 1 | 1 | 1 | -0.75 | -1.025 | 1.013 | 2.225 |
| 5 | 3 | v1 | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 0.001794 |
| 5 | 3 | always_open | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 2.225 |
| 5 | 3 | always_flat | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 0.001794 |
| 5 | 3 | half_amplitude | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 0.001794 |
| 5 | 3 | delayed_close | 1 | 1 | 1 | -0.75 | -1.02 | 1.01 | 2.225 |
| 10 | 6 | v1 | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 0.001794 |
| 10 | 6 | always_open | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 2.225 |
| 10 | 6 | always_flat | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 0.001794 |
| 10 | 6 | half_amplitude | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 0.001794 |
| 10 | 6 | delayed_close | 1 | 1 | 1 | -0.75 | -1.023 | 1.011 | 2.225 |

## Choreography basin summary
| scenario | evaluated | clear | clear fraction | packet clear fraction | min clear catch margin | min clear release margin | max clear x_catch |
|---|---:|---:|---:|---:|---:|---:|---:|
| V10_low_lapse | 594 | 359 | 0.604 | 0.604 | -0.10000000000000003 | 0.09999999999999987 | 0.55 |
| V10_nominal | 594 | 375 | 0.631 | 0.631 | -0.20000000000000007 | 0.09999999999999987 | 0.55 |
| V5_low_lapse | 594 | 369 | 0.621 | 0.621 | -0.10000000000000003 | 0.09999999999999987 | 0.55 |
| V5_nominal | 594 | 386 | 0.650 | 0.650 | -0.20000000000000007 | 0.09999999999999987 | 0.65 |

## Support-edge sweep summary

### V10_low_lapse

Evaluated 162 support-edge configurations; 162 clear.

| p_beta | eta_B | eta_N | R mode | min edge margin | release edge max gtt | packet max norm | edge shape proxy | min flare d2 |
|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 4 | 0 | 0 | always_open | 1.018 | -1.037 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 0 | delayed_close | 1.018 | -1.037 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 0.5 | always_open | 1.018 | -1.037 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 0.5 | delayed_close | 1.018 | -1.037 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 1 | always_open | 1.018 | -1.037 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 1 | delayed_close | 1.018 | -1.037 | -0.75 | 0.4047 | 2.225 |
| 4 | 0.5 | 0 | always_open | 1.018 | -1.037 | -0.75 | 0.4049 | 2.225 |
| 4 | 0.5 | 0 | delayed_close | 1.018 | -1.037 | -0.75 | 0.4049 | 2.225 |
| 4 | 0.5 | 0.5 | always_open | 1.018 | -1.037 | -0.75 | 0.4049 | 2.225 |
| 4 | 0.5 | 0.5 | delayed_close | 1.018 | -1.037 | -0.75 | 0.4049 | 2.225 |

### V10_nominal

Evaluated 162 support-edge configurations; 162 clear.

| p_beta | eta_B | eta_N | R mode | min edge margin | release edge max gtt | packet max norm | edge shape proxy | min flare d2 |
|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 4 | 0 | 0 | always_open | 1.02 | -1.041 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 0 | delayed_close | 1.02 | -1.041 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 0.5 | always_open | 1.02 | -1.041 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 0.5 | delayed_close | 1.02 | -1.041 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 1 | always_open | 1.02 | -1.041 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 1 | delayed_close | 1.02 | -1.041 | -0.75 | 0.4047 | 2.225 |
| 4 | 0.5 | 0 | always_open | 1.02 | -1.041 | -0.75 | 0.4049 | 2.225 |
| 4 | 0.5 | 0 | delayed_close | 1.02 | -1.041 | -0.75 | 0.4049 | 2.225 |
| 4 | 0.5 | 0.5 | always_open | 1.02 | -1.041 | -0.75 | 0.4049 | 2.225 |
| 4 | 0.5 | 0.5 | delayed_close | 1.02 | -1.041 | -0.75 | 0.4049 | 2.225 |

### V5_low_lapse

Evaluated 162 support-edge configurations; 162 clear.

| p_beta | eta_B | eta_N | R mode | min edge margin | release edge max gtt | packet max norm | edge shape proxy | min flare d2 |
|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 4 | 0 | 0 | always_open | 1.016 | -1.033 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 0 | delayed_close | 1.016 | -1.033 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 0.5 | always_open | 1.016 | -1.033 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 0.5 | delayed_close | 1.016 | -1.033 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 1 | always_open | 1.016 | -1.033 | -0.75 | 0.4047 | 2.225 |
| 4 | 0 | 1 | delayed_close | 1.016 | -1.033 | -0.75 | 0.4047 | 2.225 |
| 4 | 0.5 | 0 | always_open | 1.016 | -1.033 | -0.75 | 0.4049 | 2.225 |
| 4 | 0.5 | 0 | delayed_close | 1.016 | -1.033 | -0.75 | 0.4049 | 2.225 |
| 4 | 0.5 | 0.5 | always_open | 1.016 | -1.033 | -0.75 | 0.4049 | 2.225 |
| 4 | 0.5 | 0.5 | delayed_close | 1.016 | -1.033 | -0.75 | 0.4049 | 2.225 |

## Design readout
The combined design operates through packet timelikeness, support-edge margin, and timed catch/shift/throat release. The v1 throat controls supply bounded infrastructure profiles. The catch-rematched packet supplies the moving protected service worldtube.

Files: `exact_v1_composite_atlas.py`, `baselines.json`, `choreography_basin.json`, `choreography_basin_summary.json`, `support_edge_sweep.json`, `support_edge_sweep_summary.json`.
