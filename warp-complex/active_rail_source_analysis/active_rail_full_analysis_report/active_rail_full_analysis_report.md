# Active Rail Source, Construction, and Quarantine Analysis

**Status:** internal technical report  
**Scope:** prescribed-geometry source-ledger analysis, construction-resource toy estimates, quarantine diagnostics, and unfreeze sweep.  
**Main output:** a next active-rail candidate for a stronger model test: **quarantined active rail v2**.

## Executive result

The analysis changed the comparison frame.

A standard parked-open Morris--Thorne-style wormhole is extremely strong if its topology, throat, and separated mouths are simply granted. Once built and separated, its local maintenance burden is mostly tied to throat geometry, not to the exterior shortcut factor. The shortcut factor is paid in the construction/deployment history, especially mouth formation and separation.

A free-moving warp shell remains the harsh comparison case. For a ship-scale shell, the operating geometry is also the transport object, so setup and operation are closely coupled and the negative-energy burden grows badly with speed/shift scale.

The active rail's advantage is narrower but real: it can separate passenger safety from the worst support geometry. The cold rail does not need to be a fully passenger-safe static throat. It can be a non-passenger support substrate, later warmed into a service-ready plant and then used for packet service.

The best next design is not the compact freeze candidate. The best next design is a **two-scale quarantined rail plant**:

- inner packet corridor kept small,
- outer support/quarantine shell moved outward,
- broad weaker angular jacket,
- minimum-jerk decompression retained,
- passenger exposure counted only through live packet service, not through reset.

## Definitions used in the analysis

| Term | Meaning |
|---|---|
| cold active rail | non-passenger-safe support substrate, before rail-ready service state |
| warm/ready active rail | support-contained shift capacity, angular jacket, and packet service geometry prepared |
| active service | catch/carry/fade/rematch/decompression sequence |
| parked-open MT wormhole | already-built, already-separated, passenger-safe traversable throat |
| free warp shell | ship-scale shift shell that is created/operated as the transport object |
| quarantine | placing worst source channels in infrastructure, outside the passenger packet worldtube |

## Existing freeze result

The freeze report showed that the largest remaining angular-pressure ceiling is mostly warm standing plant support, not active-service excess.

| quantity                            |   active_total |   matched_holding |   active_excess | interpretation               |
|:------------------------------------|---------------:|------------------:|----------------:|:-----------------------------|
| global |pOmega| ceiling             |          1.286 |             1.283 |           0.003 | standing plant dominates     |
| support-edge |pOmega| ceiling       |          1.194 |             1.189 |           0.006 | standing plant dominates     |
| core decompression |pOmega|         |          0.262 |             0.049 |           0.213 | visible reset/service excess |
| support-edge decompression |pOmega| |          0.927 |             0.753 |           0.174 | below standing ceiling       |

This matters because the earlier active rail freeze does not say the whole system is cheap. It says the **incremental service burden over the ready plant** is small in held/early service and visible during decompression/reset.

## Corrected comparison frame

The earlier local throat-radius comparison was unfair because it did not normalize by delivered shortcut/service. The corrected frame is:

| System | What must be priced |
|---|---|
| Morris--Thorne | throat formation, passenger-safe aperture, stabilization, mouth separation/deployment, maintenance |
| Active rail | cold substrate, warm rail plant, packet service, reset/decompression, endpoint/service factor |
| Warp shell | shell creation, ship-scale operating shell, termination/rematch |

For MT, a larger exterior shortcut factor is not automatically present in the local throat ledger. It appears in the setup/deployment history. For active rail, the model parameter `V` is a stress/service parameter, not a direct delivered shortcut factor. For the warp shell, the speed/shift factor is much more directly tied to operating source burden.

## Initial construction-resource estimate

Toy model: Ellis/Morris--Thorne style throat inventory for MT and cold rail skeleton; Alcubierre-style shell inventory for warp shell.

| case                                          |   peak_rho |   int_negative_rho |   passenger_safe_aperture_factor | note                                                                       |
|:----------------------------------------------|-----------:|-------------------:|---------------------------------:|:---------------------------------------------------------------------------|
| MT minimum passenger-safe throat              |   -0.3248  |            -0.5498 |                           1      | Local support inventory only; mouth separation/topology not included.      |
| AR cold non-passenger skeleton r=0.15         |   -1.768   |            -0.2356 |                           0.4286 | Toy cold substrate; not passenger-safe by aperture.                        |
| AR support-scale throat-like substrate r=1.25 |   -0.02546 |            -1.963  |                           3.571  | Proxy for broad support-scale substrate, not full rail warm source ledger. |
| Warp shell R=0.35 wall=0.18 V=10              |   -8.302   |            -2.217  |                           1      | Shell inventory at operating factor; operation/setup merge.                |

Interpretation:

- The MT minimum passenger-safe throat at `Rpass = 0.35` is the minimal static throat that clears the passenger aperture in the toy model.
- The active rail cold skeleton at `r = 0.15` is not passenger-safe by aperture. That is the point: it can be a substrate rather than a usable passage.
- The cold skeleton has harsher local peak negative density but lower integrated inventory.
- The warp shell has much worse peak and integrated negative density at `V = 10`.

This makes the active rail construction advantage specific:

**The active rail can avoid constructing a fully passenger-safe static throat at the cold stage.**

It does not avoid hard local support; it trades broad passenger-safe construction for a smaller, sharper, non-passenger substrate.

## Sharper support tradeoff

Smaller cold support has the expected scaling:

- peak local burden worsens roughly like `1/r^2`,
- integrated inventory improves roughly like `r`.

This can help only if the limiting resource is total exotic inventory or passenger-safe volume. It hurts if the limiting resource is peak local field amplitude.

That is where source model choice matters. A localized shell/defect-like source could fit sharp cold substrate better than a volume field. A broad scalar/effective field may fit the larger warm quarantine shell better than the sharp core.

## Trans-Planckian issue and source placement

The nonminimally coupled scalar wormhole branch is useful but dangerous because known traversable-wormhole solutions can require trans-Planckian scalar values somewhere in the geometry.

The active rail does not erase that issue. It changes where the issue can be placed.

For a standard passenger-safe wormhole:

- the exotic support and passenger throat are tightly coupled.

For active rail:

- the worst scalar/support region can potentially be placed in non-passenger infrastructure,
- the passenger condition applies to a packet corridor during a timed service,
- the scalar sector should be broad and external, not the sharp passenger throat.

Updated source placement:

| Region | Preferred source role |
|---|---|
| cold substrate/core | shell, defect, or quarantined high-risk support |
| outer quarantine shell | broad scalar/effective jacket, lower local intensity |
| packet corridor | minimized exotic exposure, packet-safe local geometry |
| service correction | small transient/effective correction |
| reset/decompression | adiabatic control and positive-energy compensation where possible |

The key test is whether high-risk/trans-Planckian-support demand can be quarantined outside the passenger packet.

## Quarantine diagnostic result

The source-quarantine diagnostic found that the compact freeze candidate partly works: worst source points are generally outside the packet. But packet overlap remains too high in radial null stress and radial pressure.

Current freeze weak channels:

- negative radial `Tkk` leaks into the live packet corridor,
- radial pressure leaks into the live packet corridor,
- density/angular/current quarantine is better than null/radial-pressure quarantine.

So the next model should not merely refine `q(s)` again. It should spatially separate packet corridor from support edge.

## Unfreeze sweep result

The unfreeze sweep varied candidates across `V = 2, 5, 10`, so the conclusion is not based only on the old stressed `V = 10` case.

| candidate         |   max_score_lower_better |   max_live_Tkk_fraction |   max_live_radial_pressure_fraction |   max_Tkk_peak |   max_radial_pressure_peak |   mean_total_Tkk_burden |   Tkk_burden_change_vs_freeze |   mean_total_pOmega_burden |   pOmega_burden_change_vs_freeze |   worst_packet_norm |
|:------------------|-------------------------:|------------------------:|------------------------------------:|---------------:|---------------------------:|------------------------:|------------------------------:|---------------------------:|---------------------------------:|--------------------:|
| R2p0_quarantine   |                    1.114 |                  0.2292 |                              0.213  |         0.1229 |                    0.01986 |               1.627e+05 |                       0.7721  |                       2804 |                           0.65   |           -1129     |
| R1p75_quarantine  |                    1.314 |                  0.2726 |                              0.2493 |         0.1387 |                    0.0227  |               1.318e+05 |                       0.4352  |                       2095 |                           0.2326 |            -727     |
| broad_packet_edge |                    1.79  |                  0.3711 |                              0.3379 |         0.2256 |                    0.03619 |               9.285e+04 |                       0.01132 |                       1327 |                          -0.2192 |             -18     |
| freeze            |                    1.802 |                  0.4086 |                              0.3022 |         0.2011 |                    0.04431 |               9.181e+04 |                       0       |                       1699 |                           0      |              -8.555 |

Main result:

- Moving the support/quarantine shell outward improves packet quarantine.
- The best quarantine branch tested was `Rth = 2.0`.
- The better engineering compromise is likely `Rth = 1.75`.
- The improvement is not free: total infrastructure burden increases, especially in null/current/angular ledgers.

At `V = 10`, the R2.0 branch cut live packet negative radial `Tkk` fraction from about 41% to about 23%, and live radial-pressure fraction from about 30% to about 21%. It also reduced local peak `Tkk`, radial pressure, and angular pressure. The cost was a larger infrastructure plant.

## Updated design: quarantined active rail v2

| parameter                       | recommended_value                                                                          | role                                                                           |
|:--------------------------------|:-------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------|
| model name                      | quarantined active rail v2                                                                 | next model to test/freeze candidate                                            |
| packet radius Rpass             | 0.35                                                                                       | keeps passenger worldtube small                                                |
| support/quarantine radius Rth   | 1.75 default; 2.0 stress branch                                                            | moves worst support channels away from packet                                  |
| angular jacket radius ROmega    | co-located with Rth                                                                        | aligns angular support with quarantine shell                                   |
| support width w_th              | 0.35                                                                                       | broadens support edge and reduces local peaks                                  |
| angular jacket width wOmega     | 1.4 default; 1.6 stress branch                                                             | soft broad jacket rather than sharp shell                                      |
| angular jacket amplitude aOmega | 0.20                                                                                       | reduces peak angular pressure compared with freeze amplitude 0.35              |
| q(s)                            | minimum-jerk decompression                                                                 | retains adiabatic reset insight                                                |
| service order                   | catch/rematch before shift fade before decompression                                       | packet-safety choreography                                                     |
| packet lifecycle                | stop passenger-exposure accounting after release/rematch                                   | avoids falsely counting reset as packet exposure                               |
| source strategy                 | quarantined scalar/effective jacket + cold substrate/shell + transient service corrections | places trans-Planckian-risk channels in infrastructure, not passenger corridor |

## Recommended next model to test and possibly freeze

Default branch:

**quarantined active rail v2, R1.75 default**

Use this as the next serious candidate:

- `Rpass = 0.35`
- `Rth = 1.75`
- `ROmega = 1.75`
- `w_th = 0.35`
- `wOmega = 1.4`
- `aOmega = 0.20`
- minimum-jerk `q(s)`
- catch/rematch before shift fade
- decompression after packet release
- live packet mask ends at release/rematch, not through reset

Stress branch:

**R2.0 high-quarantine branch**

- `Rth = 2.0`
- `ROmega = 2.0`
- `w_th = 0.35`
- `wOmega = 1.6`
- `aOmega = 0.20`

Use this to test how much packet quarantine improves when the infrastructure shell grows further.

## Why R1.75 should be the next default

R2.0 gives stronger quarantine, but the infrastructure ledger increases sharply. R1.75 is the more plausible default because it moves the support edge outward enough to reduce packet exposure while avoiding the largest infrastructure expansion.

The design lesson is:

**Do not build a compact rail. Build a small packet corridor inside a wider source-management shell.**

## Next analysis gates

1. Implement a proper packet lifecycle map:
   - entry,
   - carry,
   - catch/rematch,
   - release,
   - no passenger exposure during reset.

2. Recompute quarantine with live packet exposure only.

3. Add volume-weighted source integrals with better convergence.

4. Add off-axis null congruence exposure; radial-only ray checks are insufficient.

5. Build a source-fit proxy:
   - broad scalar jacket fit,
   - shell/cold substrate fit,
   - transient service correction fit.

6. Estimate scalar amplitude/coupling burden by region:
   - packet corridor,
   - support edge,
   - outer quarantine shell,
   - cold core.

7. Test whether trans-Planckian-risk demand remains infrastructure-only.

8. If R1.75 passes, promote it to a source-shaped freeze candidate.

## Bottom line

The active rail is not an all-purpose lower-exotic wormhole. It is a source-placement architecture.

Its best current use is:

- avoid building a fully passenger-safe static throat at cold setup,
- keep the passenger packet small,
- move the worst support channels into infrastructure,
- broaden the scalar/effective support jacket to reduce local peaks,
- reserve the packet corridor for timed service safety.

The next freeze candidate should therefore be the **quarantined active rail v2** with a two-scale plant: inner packet corridor, outer source-management shell.
