# Phase A reduced optical/radiation-adjacent screen

This is a classical reduced radial screen. It estimates local photon energy factor, radial characteristic reachability, focusing proxy, and a heuristic flux-risk proxy. It does not compute RSET, quantum emission, or material dose.

| variant                        |   width_factor |   packet_positive_points |   gtt_positive_points |   local_gain_worst_max |   local_gain_worst_p99 |   local_gain_worst_p95 |   local_gain_valid_fraction |   trace_valid_fraction_either_branch |   trace_valid_fraction_plus |   trace_valid_fraction_minus |   magnification_proxy_max |   magnification_proxy_p99 |   magnification_proxy_p95 |   risk_proxy_max |   risk_proxy_p99 |   risk_proxy_p95 |   min_null_speed_proxy |
|:-------------------------------|---------------:|-------------------------:|----------------------:|-----------------------:|-----------------------:|-----------------------:|----------------------------:|-------------------------------------:|----------------------------:|-----------------------------:|--------------------------:|--------------------------:|--------------------------:|-----------------:|-----------------:|-----------------:|-----------------------:|
| active_rail_catch_throat_gated |           0.25 |                        0 |                  3627 |                  1.732 |                  1.732 |                  1.732 |                      1      |                                0.495 |                           0 |                        0.495 |                 7.968e+04 |                      2061 |                     551.2 |              900 |              900 |            895.1 |              0.0001538 |
| naive_independent_no_catch     |           0.25 |                     8671 |                  9200 |                 36.17  |                  3.742 |                  1.446 |                      0.523  |                              nan     |                         nan |                      nan     |               nan         |                       nan |                     nan   |              nan |              nan |            nan   |            nan         |
| naive_throat_gated_no_catch    |           0.25 |                     8671 |                  9200 |                 36.17  |                  3.742 |                  1.446 |                      0.523  |                              nan     |                         nan |                      nan     |               nan         |                       nan |                     nan   |              nan |              nan |            nan   |            nan         |
| late_catch_throat_gated        |           0.25 |                     6102 |                  9200 |                 36.17  |                  4.477 |                  2.021 |                      0.6644 |                              nan     |                         nan |                      nan     |               nan         |                       nan |                     nan   |              nan |              nan |            nan   |            nan         |
| catch_independent_shift        |           0.25 |                        0 |                  3627 |                  1.732 |                  1.732 |                  1.732 |                      1      |                              nan     |                         nan |                      nan     |               nan         |                       nan |                     nan   |              nan |              nan |            nan   |            nan         |

## Active branch trace/focusing headline
- `trace_valid_fraction_either_branch`: 0.494994
- `trace_valid_fraction_plus`: 0
- `trace_valid_fraction_minus`: 0.494994
- `magnification_proxy_max`: 79682.2
- `magnification_proxy_p99`: 2060.94
- `magnification_proxy_p95`: 551.232
- `risk_proxy_max`: 899.988
- `risk_proxy_p99`: 899.965
- `risk_proxy_p95`: 895.097
- `min_null_speed_proxy`: 0.000153817