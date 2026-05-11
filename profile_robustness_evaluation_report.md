# Profile Robustness Evaluation — Throat-Loaded Gated-Shift Reduced Ansatz
## Scope
- Reused the reduced ADM evaluator structure from the companion code: traversal, exit, and post-exit scans; causal-balance via `gtt` and lapse-shift margin; curvature, null expansion, tidal, burden-share, and post-exit recovery diagnostics.
- Full-resolution confirmation was run for the four coherent profile families and both mixed-release families that showed causal failures in the fast screen.
- Broad mixed-profile screening covered 23 profile suites over the original 336-configuration parameter grid: 7,728 profile-config rows and 23,184 phase scans.
- Full-resolution selected confirmation covered 2,016 additional phase scans for coherent and failure-bearing suites, plus full-resolution checks of all failure rows.

## Profile families
| Family | Used for | Interpretation |
|---|---|---|
| `tanh_r2` / `tanh` | W, S, E, q | Baseline tanh proxy from the original reduced evaluator |
| `smoothstep_compact` | W, S, E, q | Compact finite-width smoothstep transition |
| `cinf_compact` | W, S, E, q | Compact C-infinity bump/step stress test |
| `supergaussian` / `logistic_soft` | W/S and E/q | Noncompact/tail stress tests, useful for leakage sensitivity |

## Full-resolution selected results
| suite | clean/configs | exit gtt+ configs | worst exit max_gtt | worst exit min margin | worst exit theta product | worst exit Kretsch | mean throat share | min throat share | post gtt departure |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| coherent_tanh_r2 | 336/336 | 0 | -1 | 1 | 657.4 | 8.0137e+07 | 0.9948 | 0.9123 | 0.006759 |
| coherent_smoothstep_compact | 336/336 | 0 | -1 | 1 | 6622 | 2.1658e+08 | 0.9574 | 0.8068 | 0 |
| coherent_cinf_compact | 336/336 | 0 | -1 | 1 | 1.3574e+04 | 4.6422e+08 | 0.9557 | 0.8068 | 0 |
| coherent_supergaussian | 336/336 | 0 | -1 | 1 | 432.4 | 3.9047e+05 | 0.5057 | 0.01781 | 0.04352 |
| E_cinf_compact_q_tanh | 332/336 | 4 | 8.2184e+04 | -26.41 | 657.4 | 8.0129e+07 | 0.9948 | 0.9123 | 0.006759 |
| E_cinf_compact_q_logistic_soft | 330/336 | 6 | 2.2837e+05 | -55.75 | 432.4 | 8.0100e+07 | 0.9965 | 0.9608 | 0.04352 |

## Broad fast-screen aggregate
- Suites: 23; original configs per suite: 336; profile-config rows: 7728; phase scans: 23184.
- Clean rows: 7720/7728.
- Only two suite-level families produced positive `gtt` in the fast screen: `E_cinf_compact_q_tanh` and `E_cinf_compact_q_logistic_soft`.
- All fast-screen failures occurred in synchronized release at V=2.0. Shift-first and rapid-shift-first were clean across the whole mixed-profile screen.

## Full-resolution failure rows
| suite | mode | V | C0 | Delta | w_release | exit gtt+ pts | max_gtt | min margin |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| E_cinf_compact_q_tanh | synchronized | 2 | 100 | 0.1 | 0.35 | 3 | 97.91 | -0.9114 |
| E_cinf_compact_q_tanh | synchronized | 2 | 100 | 0.1 | 0.18 | 1 | 50.17 | -0.4885 |
| E_cinf_compact_q_tanh | synchronized | 2 | 1.0000e+04 | 0.1 | 0.35 | 3 | 8.2184e+04 | -26.41 |
| E_cinf_compact_q_tanh | synchronized | 2 | 1.0000e+04 | 0.1 | 0.18 | 1 | 3.9258e+04 | -13.67 |
| E_cinf_compact_q_logistic_soft | synchronized | 2 | 100 | 0.3 | 0.35 | 2 | 33.82 | -0.1944 |
| E_cinf_compact_q_logistic_soft | synchronized | 2 | 100 | 0.1 | 0.35 | 10 | 202.7 | -2.397 |
| E_cinf_compact_q_logistic_soft | synchronized | 2 | 100 | 0.1 | 0.18 | 4 | 160.3 | -1.978 |
| E_cinf_compact_q_logistic_soft | synchronized | 2 | 1.0000e+04 | 0.3 | 0.35 | 2 | 6.5021e+04 | -8.525 |
| E_cinf_compact_q_logistic_soft | synchronized | 2 | 1.0000e+04 | 0.1 | 0.35 | 10 | 2.2837e+05 | -55.75 |
| E_cinf_compact_q_logistic_soft | synchronized | 2 | 1.0000e+04 | 0.1 | 0.18 | 4 | 2.2587e+05 | -44.53 |

## Verdict
The throat-gated shift architecture is causally robust for coherent profile changes and for all one-at-a-time W/S swaps in the broad screen. The profile-sensitive failure mode is not W/S shape; it is release mismatch: synchronized release can fail when the transport support profile remains effectively larger than the capacity/lapse release profile near the exit. Shift-first ordering removes that failure in the tested grid.

Burden localization is robust for compact throat profiles. Noncompact super-Gaussian tails keep causal balance but leak burden outside the throat and leave larger post-exit departures, so they are unsuitable for the intended throat-loaded architecture unless truncated or compensated.

Sharper compact profiles increase null-expansion and curvature pulses. This does not overturn the architecture, but it makes profile smoothing/width optimization a required next step before 3+1 validation.
