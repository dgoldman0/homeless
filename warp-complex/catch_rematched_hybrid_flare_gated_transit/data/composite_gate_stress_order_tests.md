# Composite gate stress/order tests

## V=5, lambda=5

| case | packet worldtube fail | passive packet gtt fail | support edge gtt fail | packet max norm | packet max gtt | edge max gtt |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 0 | 0 | 0 | -0.75 | -1 | -1.02 |
| no_B | 0 | 0 | 0 | -0.75 | -1 | -1.02 |
| no_R | 0 | 0 | 0 | -0.75 | -1 | -1.02 |
| no_N | 0 | 0 | 0 | -0.75 | -1 | -1.01 |
| no_hold | 0 | 0 | 0 | -0.75 | -1 | -1 |
| late_catch_after_shift | 1 | 0 | 0 | 92.9 | -1 | -1.02 |
| late_catch_after_relax | 1 | 0 | 0 | 290 | -1 | -1.02 |
| edge_reinforced_p2 | 0 | 0 | 0 | -0.75 | -1 | -1.02 |

## V=10, lambda=11.5

| case | packet worldtube fail | passive packet gtt fail | support edge gtt fail | packet max norm | packet max gtt | edge max gtt |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 0 | 0 | 0 | -0.75 | -1 | -1.02 |
| no_B | 0 | 0 | 0 | -0.75 | -1 | -1.02 |
| no_R | 0 | 0 | 0 | -0.75 | -1 | -1.02 |
| no_N | 0 | 0 | 0 | -0.75 | -1 | -1.02 |
| no_hold | 0 | 0 | 0 | -0.749 | -1 | -1 |
| late_catch_after_shift | 1 | 0 | 0 | 508 | -1 | -1.02 |
| late_catch_after_relax | 1 | 0 | 0 | 1.33e+03 | -1 | -1.02 |
| edge_reinforced_p2 | 0 | 0 | 0 | -0.75 | -1 | -1.02 |

## V=5, lambda=3

| case | packet worldtube fail | passive packet gtt fail | support edge gtt fail | packet max norm | packet max gtt | edge max gtt |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 0 | 1 | 0 | -0.75 | 1.57e+03 | -1.02 |
| no_B | 0 | 1 | 0 | -0.75 | 1.57e+03 | -1.02 |
| no_R | 0 | 1 | 0 | -0.75 | 1.57e+03 | -1.02 |
| no_N | 0 | 1 | 0 | -0.75 | 1.57e+03 | -1.01 |
| no_hold | 0 | 1 | 0 | -0.75 | 1.55e+03 | -1 |
| late_catch_after_shift | 1 | 1 | 0 | 556 | 1.58e+03 | -1.02 |
| late_catch_after_relax | 1 | 1 | 0 | 1.19e+03 | 1.58e+03 | -1.02 |
| edge_reinforced_p2 | 0 | 1 | 0 | -0.75 | 1.56e+03 | -1.02 |

## V=10, lambda=6

| case | packet worldtube fail | passive packet gtt fail | support edge gtt fail | packet max norm | packet max gtt | edge max gtt |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 0 | 1 | 0 | -0.75 | 6.27e+03 | -1.02 |
| no_B | 0 | 1 | 0 | -0.75 | 6.27e+03 | -1.02 |
| no_R | 0 | 1 | 0 | -0.75 | 6.27e+03 | -1.02 |
| no_N | 0 | 1 | 0 | -0.75 | 6.29e+03 | -1.01 |
| no_hold | 0 | 1 | 0 | -0.451 | 6.23e+03 | -1 |
| late_catch_after_shift | 1 | 1 | 1 | 2.19e+03 | 6.33e+03 | 59 |
| late_catch_after_relax | 1 | 1 | 1 | 4.91e+03 | 6.33e+03 | 97.1 |
| edge_reinforced_p2 | 0 | 1 | 0 | -0.75 | 6.26e+03 | -1.02 |

