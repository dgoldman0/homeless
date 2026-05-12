# Source-Anatomy Early-Break Pass
Scope: throat-gated ordinary shift-first family, using the same reduced metric/evaluation machinery as the gated-shift full evaluator, extended to project the Einstein tensor into an ADM-normal orthonormal frame. Values are dimensionless geometrized-source quantities; divide by 8π for T_ab in G=c=1 units.
## Main result
The local g_tt causal monitor still survives, but two stronger physical issues appear immediately:
1. All sampled exit configurations require negative energy density and NEC violation. This was expected, but now quantified.
2. For V>1, the moving profile-center curve l=L(t)=Vt becomes spacelike during release/outside support if interpreted as a passenger trajectory. This is an early-break candidate unless L(t) is a control label and the actual passenger worldline decelerates/re-matches separately.
## Aggregate source anatomy
- configs: 144
- exit_gtt_positive_configs: 0
- traverse_gtt_positive_configs: 0
- exit_nec_violation_configs: 144
- exit_neg_rho_configs: 144
- worst_exit_min_rho_src: -4842.804410686412
- worst_exit_maxabs_rho_src: 4842.804410686412
- worst_exit_maxabs_pressure: 5611.4082629926215
- worst_exit_maxabs_flux: 456.4854460775659
- worst_exit_min_nec: -2871.939514733865
- worst_exit_max_neg_nec_sum: 4325.757636526345
- median_exit_throat_share_neg_rho: 0.9878022033106573
- min_exit_throat_share_neg_rho: 0.9768729032864313
- median_exit_throat_share_neg_nec: 0.9849240383055362
- min_exit_throat_share_neg_nec: 0.9304983095949039
- max_exit_passenger_share_neg_rho: 0.9692851148479117
- max_exit_passenger_share_neg_nec: 0.9696961317574145
- worst_exit_pressure_over_absrho_p999: 12182.755192206248
- worst_exit_flux_over_absrho_p999: 87.89379553450968

## Exit severity by velocity
|    V |   configs |   max_tidal |   median_tidal |   max_rho |   min_nec |
|-----:|----------:|------------:|---------------:|----------:|----------:|
| 0.9  |        24 |     1879.02 |        950.022 |   4842.8  |  -2531.6  |
| 1.01 |        24 |     1944.57 |        963.958 |   4842.53 |  -2564.02 |
| 1.1  |        24 |     2000.83 |        975.815 |   4842.29 |  -2589.78 |
| 1.25 |        24 |     2086.76 |        993.731 |   4841.85 |  -2634.09 |
| 1.5  |        24 |     2213.9  |       1028.74  |   4841.02 |  -2710.88 |
| 2    |        24 |     2422.28 |       1095.43  |   4838.97 |  -2871.94 |

## Center-worldline timelikeness by velocity
|    V |   configs |   spacelike_configs |        max_ds2 |   med_max_ds2 |   med_spacelike_fraction |
|-----:|----------:|--------------------:|---------------:|--------------:|-------------------------:|
| 0.9  |        24 |                   0 |     -0.19      |      -0.19    |                 0        |
| 1.01 |        24 |                  24 |      0.0205754 |       0.0201  |                 0.489005 |
| 1.1  |        24 |                  24 |     19.3076    |       0.72955 |                 0.497501 |
| 1.25 |        24 |                  24 |   1800.52      |       9.17233 |                 0.506497 |
| 1.5  |        24 |                  24 |  41247.5       |      67.1811  |                 0.514993 |
| 2    |        24 |                  24 | 566751         |     618.356   |                 0.52099  |

## Selected center-worldline source/tidal exposure
| label                 |   gtt_positive_points |   min_rho_src |   maxabs_rho_src |   min_nec |   max_neg_nec_sum |   maxabs_tidal_radial |   maxabs_tidal_angular |   max_ds2_dt2 |   min_dtaudt |   max_dtaudt |
|:----------------------|----------------------:|--------------:|-----------------:|----------:|------------------:|----------------------:|-----------------------:|--------------:|-------------:|-------------:|
| best_lowV             |                     0 |      -542.556 |          542.556 |  -357.982 |           658.776 |               223.955 |                139.798 |        -0.19  |      0.43589 |      104.834 |
| highV_moderate_wall   |                     0 |      -543.175 |          543.175 |  -347.255 |           621.834 |               286.853 |                166.642 |       153.705 |      0       |      229.739 |
| worst_highV_thin_wall |                     0 |     -4892.15  |         4892.15  | -1926.93  |          3813.77  |              2567.65  |               1072.7   |       475.097 |      0       |      229.999 |

## Interpretation
The throat-gated architecture does not fail through g_tt in this pass. It fails, or at least becomes incomplete, at the stronger physical layer: what source is demanded and what actual timelike passenger worldline is being represented. The existing reduced ansatz uses L=Vt as the profile/control center. For V>1, when E and W fade, the same center curve reverts to an exterior superluminal coordinate path and becomes spacelike. A physically meaningful version needs a separate exit/re-matching law for the passenger worldline or a new L(t) satisfying |dot L - V E W S| < T/A through release.

## Files
- `source_anatomy_shift_first_phase_summary.csv`
- `source_anatomy_shift_first_aggregate.json`
- `source_anatomy_selected_worldlines.csv`
- `worldline_center_timelikeness_scan.csv`
- `worldline_center_timelikeness_byV.csv`
