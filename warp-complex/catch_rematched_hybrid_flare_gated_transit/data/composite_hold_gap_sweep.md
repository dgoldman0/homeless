# Composite hold/gap sweep

Order-preserving compression test: `hold_scale` shrinks catch→shift and shift→relax gaps while preserving order. Safety here means no packet-norm failure and no support-edge gtt failure. Passive packet gtt is tracked separately and ignored for low-lapse active-packet safety.

| V | lambda | p_beta | min hold scale safe | hold=0 packet norm pts | hold=0 max norm | hold=0 edge gtt pts |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 3 | 1 | 0 | 0 | -0.75 | 0 |
| 5 | 3 | 1.5 | 0 | 0 | -0.75 | 0 |
| 5 | 3 | 2 | 0 | 0 | -0.75 | 0 |
| 5 | 3 | 3 | 0 | 0 | -0.75 | 0 |
| 5 | 5 | 1 | 0 | 0 | -0.75 | 0 |
| 5 | 5 | 1.5 | 0 | 0 | -0.75 | 0 |
| 5 | 5 | 2 | 0 | 0 | -0.75 | 0 |
| 5 | 5 | 3 | 0 | 0 | -0.75 | 0 |
| 10 | 6 | 1 | 0.1 | 9 | 240 | 0 |
| 10 | 6 | 1.5 | 0.1 | 9 | 241 | 0 |
| 10 | 6 | 2 | 0.1 | 9 | 241 | 0 |
| 10 | 6 | 3 | 0.1 | 9 | 243 | 0 |
| 10 | 11.5 | 1 | 0 | 0 | -0.749 | 0 |
| 10 | 11.5 | 1.5 | 0 | 0 | -0.749 | 0 |
| 10 | 11.5 | 2 | 0 | 0 | -0.749 | 0 |
| 10 | 11.5 | 3 | 0 | 0 | -0.749 | 0 |
