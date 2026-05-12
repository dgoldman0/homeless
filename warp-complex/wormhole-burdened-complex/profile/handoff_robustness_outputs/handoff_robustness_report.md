# Handoff Robustness Evaluation

## Setup
Tested superluminal cases only: V = 1.01, 1.1, 1.25, 1.5, 2.0 across C0 ∈ {100, 1e4}, Delta ∈ {0.3, 0.1}, release width ∈ {0.35, 0.18}, and shift-first release gaps ∈ {0.35, 0.70, 1.00}; 120 configurations total.

Candidate passenger handoff laws were layered on top of the same shift-first metric. The key support factor was F = E W S.

- fixed_V_baseline: dx/dt = V.
- blend_EWS_stop: dx/dt = V F.
- blend_EWS_v05: dx/dt = 0.5 + (V - 0.5) F.
- blend_EWS_v09: dx/dt = 0.9 + (V - 0.9) F.
- blend_EW_v05: dx/dt = 0.5 + (V - 0.5) E W.
- clip_eta09: dx/dt = min(V, V E W S + 0.9 T/A).

Timelike condition evaluated: ds^2/dt^2 = -T^2 + A^2(dx/dt - V E W S)^2 < 0.

## Timelikeness summary

| variant          |   cases |   timelike_cases |   spacelike_cases |   worst_margin |   worst_max_ds2 |   median_final_x |   median_lag |   max_accel |
|:-----------------|--------:|-----------------:|------------------:|---------------:|----------------:|-----------------:|-------------:|------------:|
| fixed_V_baseline |     120 |                0 |               120 |        -1      |       5.538e+05 |           2.16   |       0      |   5.684e-14 |
| blend_EWS_stop   |     120 |              120 |                 0 |         1      |      -1         |           0.3858 |       1.749  |  15.37      |
| blend_EWS_v05    |     120 |              120 |                 0 |         0.5    |      -0.75      |           1.06   |       1.064  |  17.84      |
| blend_EWS_v09    |     120 |              120 |                 0 |         0.1    |      -0.19      |           1.588  |       0.481  |  43.33      |
| blend_EW_v05     |     120 |              120 |                 0 |         0.3165 |      -0.75      |           1.064  |       1.064  |  41.47      |
| clip_eta09       |     120 |              120 |                 0 |         0.1    |      -0.19      |           1.669  |       0.3812 |  96.57      |

## Source/tidal exposure summary

| variant          |   cases |   timelike_cases |   worst_rho |   worst_nec |   max_neg_nec |   max_tidal_r |   max_tidal_a |   med_int_neg_nec |   max_int_neg_nec |   median_final_x |   median_lag |
|:-----------------|--------:|-----------------:|------------:|------------:|--------------:|--------------:|--------------:|------------------:|------------------:|-----------------:|-------------:|
| fixed_V_baseline |     120 |                0 |   -5571     |       -3374 |          6177 |          2661 |        1722   |            45.11  |            424.6  |           2.16   |        0     |
| blend_EWS_stop   |     120 |              120 |      -5.961 |        -146 |           192 |           382 |         229.4 |             9.318 |             25.44 |           0.3858 |        1.749 |
| blend_EWS_v05    |     120 |              120 |   -5749     |       -3335 |          6320 |          2602 |        1784   |            70.11  |            307.4  |           1.06   |        1.064 |
| blend_EWS_v09    |     120 |              120 |   -5772     |       -3411 |          6210 |          2553 |        1628   |            79.45  |            402.2  |           1.588  |        0.481 |
| blend_EW_v05     |     120 |              120 |   -5749     |       -3335 |          6320 |          2639 |        1704   |            70.12  |            311.1  |           1.064  |        1.064 |
| clip_eta09       |     120 |              120 |   -5864     |       -3413 |          6224 |          2697 |        1725   |            84.95  |            310.5  |           1.669  |        0.381 |

## Conclusions

The handoff save works kinematically. Every rematched law tested was timelike in all 120 superluminal configurations. The baseline fixed-V path failed in all 120.

The cleanest mathematical law is the EWS blend: dx/dt = v_out + (V-v_out) E W S. For v_out < 1 it inherits a built-in margin because the difference from the local shift is v_out(1-EWS), while T/A >= 1 in this ansatz. This explains the exact observed margins: stop gives ~1, v05 gives ~0.5, v09 gives ~0.1.

The physically relevant tradeoff is not timelikeness anymore. It is progress versus exposure. The stop handoff is very gentle but barely exits: median final x ≈ 0.386 while the control center reaches ≈ 2.16. The 0.5 and 0.9 rematches make more progress, but they pass through the high-curvature/source wall and recover source/tidal exposures comparable to the baseline.

Operationally, the handoff must be designed as a capture/rematch system, not just as a velocity clip. A robust version should combine EWS-slaved timelikeness with a geometry that moves the high-curvature wall away from the actual passenger path or performs the handoff in a low-source corridor.
