# Catch-enabled passenger exposure evaluation

This pass evaluates the catch-enabled reduced throat-loaded gated-shift model with dense passenger-worldline sampling. 

Two variants were evaluated:

- `U_coupled_shift`: the shift amplitude follows the caught passenger velocity `U(t)`. This is the cleaner catch-rematched ansatz.
- `V_fixed_shift`: the shift amplitude remains tied to the nominal superluminal `V` until the shift gate fades. This is a harsher control-label variant.

The evaluated ordering is `catch -> shift release -> throat relaxation`, with nominal `L_catch=0.65`, `L_beta=1.10`, `L_q=1.45`.

## Nominal dense exposure summary

| variant         |    V |   timelike_fail_points |   max_worldline_norm |   max_abs_v_rel |   max_abs_tidal_pass |   I_neg_nec_sum_dtau |   I_abs_flux_dtau |   max_gtt |
|:----------------|-----:|-----------------------:|---------------------:|----------------:|---------------------:|---------------------:|------------------:|----------:|
| U_coupled_shift |  1.5 |                      0 |            -0.749827 |        0.501644 |        286.084       |              82.8491 |           12.5631 |     -1    |
| U_coupled_shift |  2   |                      0 |            -0.749999 |        0.500022 |        309.785       |              83.3078 |           13.3225 |     -1    |
| U_coupled_shift |  3   |                      0 |            -0.75     |        0.5      |        344.66        |              82.2781 |           14.3638 |     -1    |
| U_coupled_shift |  5   |                      0 |            -0.75     |        0.5      |        392.165       |              80.1472 |           15.666  |     -1    |
| U_coupled_shift | 10   |                      0 |            -0.75     |        0.5      |        460.473       |              77.0103 |           17.4249 |     -1    |
| V_fixed_shift   |  1.5 |                      0 |            -0.749838 |        0.500803 |        268.449       |              84.8785 |           32.9019 |     -1    |
| V_fixed_shift   |  2   |                      0 |            -0.749999 |        0.500007 |        277.63        |              86.2254 |           46.5646 |     -1    |
| V_fixed_shift   |  3   |                      0 |            -0.75     |        0.592718 |        276.963       |              86.7704 |           73.9418 |     -1    |
| V_fixed_shift   |  5   |                      0 |            -0.75     |        0.783114 |        238.897       |              87.6951 |          114.965  |     -1    |
| V_fixed_shift   | 10   |                     18 |          2323.06     |        1.18615  |          4.55358e+60 |              92.3378 |           45.2938 |   7317.51 |

## Aggregate sweep summary

| variant         |   V |   Delta |   cases |   timelike_fail_cases |   gtt_fail_cases |   worst_max_worldline_norm |   worst_max_abs_v_rel |   median_max_abs_tidal |   worst_max_abs_tidal |   median_I_neg_nec |   worst_I_neg_nec |   median_I_flux |   worst_I_flux |
|:----------------|----:|--------:|--------:|----------------------:|-----------------:|---------------------------:|----------------------:|-----------------------:|----------------------:|-------------------:|------------------:|----------------:|---------------:|
| U_coupled_shift |   2 |     0.1 |      36 |                    17 |                0 |                    7.41301 |               1.95077 |         6414.72        |           7.29526e+63 |            92.8697 |           498.335 |         41.0553 |       117.937  |
| U_coupled_shift |   2 |     0.3 |      36 |                    13 |                0 |                    6.9714  |               1.87463 |          309.827       |           1.0943e+63  |            38.5216 |           155.24  |         12.6044 |        15.3587 |
| U_coupled_shift |   5 |     0.1 |      36 |                    18 |                0 |                  149.32    |               4.72971 |            7.50205e+58 |           1.60338e+65 |            46.0284 |           478.019 |         40.9096 |        96.5849 |
| U_coupled_shift |   5 |     0.3 |      36 |                    17 |                0 |                  194.884   |               4.52612 |         5202.54        |           5.9782e+64  |            29.4853 |           145.357 |         15.2212 |        17.572  |
| U_coupled_shift |  10 |     0.1 |      36 |                    18 |                0 |                  206.405   |               9.58212 |            1.58506e+61 |           2.37644e+66 |            35.6736 |           473.146 |         48.3563 |       133.3    |
| U_coupled_shift |  10 |     0.3 |      36 |                    17 |                1 |                  609.286   |               8.98747 |          463.284       |           8.17302e+65 |            30.4075 |           141.3   |         17.0631 |        30.3833 |
| V_fixed_shift   |   2 |     0.1 |      36 |                    16 |                0 |                    7.32263 |               1.95069 |         4553.94        |           7.13249e+63 |           105.614  |           513.922 |         97.5022 |       279.254  |
| V_fixed_shift   |   2 |     0.3 |      36 |                    13 |                0 |                    6.84313 |               1.87422 |          276.973       |           1.09231e+63 |            41.1238 |           158.881 |         23.4371 |        83.271  |
| V_fixed_shift   |   5 |     0.1 |      36 |                    18 |                0 |                  133.087   |               4.72971 |            7.84557e+58 |           1.55014e+65 |            56.2964 |           517.444 |        180.277  |       581.918  |
| V_fixed_shift   |   5 |     0.3 |      36 |                    17 |                0 |                  189.72    |               4.52438 |          555.926       |           6.23137e+64 |            33.6825 |           154.459 |         56.3397 |       174.715  |
| V_fixed_shift   |  10 |     0.1 |      36 |                    35 |               21 |                 3482.71    |               9.58196 |            1.43331e+62 |           1.4429e+66  |            43.2378 |           554.09  |         64.9496 |       809.694  |
| V_fixed_shift   |  10 |     0.3 |      36 |                    35 |               25 |                 3909.59    |               8.98131 |            1.39043e+61 |           7.72963e+65 |            36.9982 |           160.478 |         42.3136 |       143.295  |

## Preliminary interpretation

The pass is designed to distinguish ansatz structure from evaluation structure. If the `U_coupled_shift` variant behaves cleanly while `V_fixed_shift` produces high flux/tide or timelike failures, the catch must be implemented as an actual transport-field rematching law, not merely as a separate passenger kinematic label.
