# Active-Rail Source Ledger: First Diagnostic Report

## Status

This is a **first diagnostic source-ledger pass**, not a final active-rail source model.

It computes the demanded classical source

```math
T_{\mu\nu}^{\rm demand} = \frac{1}{8\pi}G_{\mu\nu}[g]
```

for the reduced active-rail metric in geometrized units, `G=c=1`, using the active branch:

```text
variant = active_rail_catch_throat_gated
width_factor = 1.0
angular_closure = static_throat
gamma_OmegaOmega = l^2 + Rth^2
```

The calculation is a numerical Einstein-tensor diagnostic. It is not a constraint-quality initial-data solve, not a matter model, and not a semiclassical/RSET calculation.

The angular closure is provisional. Absolute source magnitudes should not be treated as a design claim until an angular-closure family is run.

## Main finding

The frozen active-rail geometry was not shown to be wrong. It was shown to be **undercommitted for source accounting**.

The packet-clearance geometry did what it was designed to do: it organized the service sequence around support-contained shift and catch-before-release. The source ledger asks a harder question: where does the geometry demand stress-energy once treated as a physical metric?

The first answer is:

> The main source burden is routed into the infrastructure, especially the support edge and packet/support interface. Catch/rematch is a packet-control operation, while shift fade, throat relaxation, and reset carry the larger source ledger.

This supports the rail-not-bubble interpretation. The dominant burden does not appear primarily as a passenger-centered bubble wall in this closure. It appears as an infrastructure-edge bill.

## Channel ranking

| channel | global_max_abs | phase_at_max | region_at_max |
| --- | --- | --- | --- |
| Outgoing null Tkk+ | 0.6192 | throat_relax | packet_in_support |
| Ingoing null Tkk- | 0.5686 | throat_relax | support_edge |
| Angular pressure/tension p_Omega | 0.521 | reset_tail | support_edge |
| Euler energy density rho | 0.08133 | throat_relax | support_edge |
| Radial pressure/tension p_l | 0.06529 | throat_relax | support_edge |
| Packet-frame density rho_pkt | 0.06523 | throat_relax | support_edge |
| Euler radial current j_l | 0.04803 | throat_relax | support_edge |

Interpretation:

1. The largest individual contractions are radial null-channel contractions, so NEC-type accounting is the sharpest warning channel.
2. The largest material stress channel is angular pressure/tension, so `gamma_OmegaOmega` is a real design variable rather than a harmless closure.
3. Eulerian negative density is present but smaller than the null and angular-stress ledgers.
4. Radial current is concentrated later, mainly during relax/reset, not during catch.

## Where the angular bill lands

| phase | region | points | p_omega_unit_max_abs |
| --- | --- | --- | --- |
| reset_tail | support_edge | 3 | 0.521 |
| reset_tail | core_throat | 3 | 0.5172 |
| shift_fade | support_edge | 5 | 0.5085 |
| throat_relax | support_edge | 2 | 0.4806 |
| catch_rematch | support_edge | 6 | 0.4434 |
| pre_catch_support | support_edge | 3 | 0.4433 |
| pre_catch_support | outer_shoulder | 3 | 0.3281 |
| catch_rematch | outer_shoulder | 6 | 0.3281 |

Implication: `gamma_OmegaOmega` is not cosmetic. It controls a primary pressure/tension bill. The angular sector must be designed, not guessed.

## Where NEC-like pressure appears

The table below uses the more negative of the outgoing/ingoing radial null contractions as the last column.

| phase | region | points | Tkk_plus_min | Tkk_minus_min | Tkk_worst_min |
| --- | --- | --- | --- | --- | --- |
| throat_relax | packet_in_support | 1 | -0.6192 | 0.5302 | -0.6192 |
| throat_relax | support_edge | 2 | -0.09117 | -0.5686 | -0.5686 |
| shift_fade | support_edge | 5 | -0.4905 | -0.5038 | -0.5038 |
| catch_rematch | support_edge | 6 | -0.4915 | -0.4915 | -0.4915 |
| pre_catch_support | support_edge | 3 | -0.4915 | -0.4915 | -0.4915 |
| throat_relax | core_throat | 3 | -0.4556 | -0.338 | -0.4556 |
| shift_fade | packet_in_support | 2 | -0.3473 | -0.06881 | -0.3473 |
| catch_rematch | core_throat | 3 | -0.2316 | -0.1573 | -0.2316 |

Implication: the support edge has a standing null-channel burden before and during service. The most serious packet-adjacent null exposure occurs around throat relaxation.

## Eulerian negative density

| phase | region | points | rho_euler_min |
| --- | --- | --- | --- |
| throat_relax | support_edge | 2 | -0.08133 |
| shift_fade | support_edge | 5 | -0.04066 |
| catch_rematch | support_edge | 6 | -0.03741 |
| pre_catch_support | support_edge | 3 | -0.03741 |
| pre_catch_support | outer_shoulder | 3 | -0.02272 |
| catch_rematch | outer_shoulder | 6 | -0.02272 |
| shift_fade | outer_shoulder | 6 | -0.0227 |
| reset_tail | core_throat | 3 | -0.01345 |

Implication: the exotic-density signal is strongest at the support edge during throat relaxation. The core throat is comparatively mild in this closure.

## Packet-frame density

| phase | region | points | rho_packet_min |
| --- | --- | --- | --- |
| throat_relax | support_edge | 2 | -0.06523 |
| reset_tail | support_edge | 3 | -0.05571 |
| shift_fade | support_edge | 5 | -0.0535 |
| reset_tail | core_throat | 3 | -0.05281 |
| shift_fade | outer_shoulder | 6 | -0.03746 |
| throat_relax | packet_outer | 1 | -0.01992 |
| reset_tail | packet_outer | 1 | -0.007019 |
| throat_relax | outer_shoulder | 2 | -0.004221 |

Implication: the packet interior is not the main sink, but the packet-adjacent support region is not automatically clean. Passenger-facing source exposure needs its own ledger beyond packet timelikeness.

## Radial current / momentum channel

| phase | region | points | j_l_unit_max_abs |
| --- | --- | --- | --- |
| throat_relax | support_edge | 2 | 0.04803 |
| reset_tail | support_edge | 3 | 0.03438 |
| reset_tail | core_throat | 3 | 0.02816 |
| throat_relax | packet_in_support | 1 | 0.005302 |
| throat_relax | core_throat | 3 | 0.003508 |
| shift_fade | support_edge | 5 | 0.002586 |
| throat_relax | packet_outer | 1 | 0.002427 |
| shift_fade | outer_shoulder | 6 | 0.0004935 |

Implication: catch/rematch did not show up as the large current event in this run. The larger current demand appears during relaxation/reset and at the support edge.

## Comparison to the existing active-rail work

### What the frozen model established

The frozen model was a kinematic/service scaffold. It tested whether the active branch could preserve packet timelikeness under a stressed reduced radial screen. It separated roles: support, shift, catch, fade, relaxation, reset, packet, and support edge.

### What the source ledger adds

The source ledger turns the same geometry into a source request. Generic windows and edges now have derivatives and curvature cost. That does not invalidate the frozen model. It promotes formerly generic choices into physical design variables.

The updated division of labor is:

```text
catch/rematch          -> packet timelikeness control
support edge           -> main exotic/null burden
angular sector         -> dominant pressure/tension stress channel
shift fade / relax     -> expensive actuation phases
reset shoulder         -> possible residual/reusability ledger
```

### Design implication

The next active-rail design problem is source routing:

> Keep the packet clean by moving the hard geometric work into infrastructure, then engineer the infrastructure edge and angular sector so the burden is bounded, localized, and resettable.

## What to unfreeze first

The first design variables to unfreeze should be:

1. **Angular closure**: vary `gamma_OmegaOmega` and test whether angular pressure/tension and null contractions can be reduced or spread.
2. **Support-edge shape**: vary `W(l)`, edge width, edge smoothness, and shoulder matching.
3. **Fade/relax timing**: vary `x_beta`, `x_q`, `w_beta`, `w_q`, and the overlap/separation between shift fade and throat relaxation.
4. **Packet-boundary exposure**: add integrated packet-frame density, null exposure, and eventually tidal channels.
5. **Repeated-cycle reset**: ask whether reset really returns the plant to baseline or leaves residual edge stress.

## Figures

- `figures/global_channel_ranking.png`
- `figures/angular_pressure_region_phase.png`
- `figures/worst_null_locations.png`

## Reproduce

From this folder:

```bash
python code/source_ledger.py \
  --variant active_rail_catch_throat_gated \
  --width-factor 1.0 \
  --angular-closure static_throat \
  --ns 41 \
  --nl 61 \
  --probe
```

The script writes regenerated outputs under `data/`.

## Caveats

- The angular closure is provisional.
- The numerical curvature uses finite differences.
- The convergence probe is a stability check, not a proof.
- The reported point sums are unweighted point sums, not invariant integrated energy measures.
- No matter model is supplied; this is demanded-source accounting only.
- No semiclassical stress tensor is computed.
