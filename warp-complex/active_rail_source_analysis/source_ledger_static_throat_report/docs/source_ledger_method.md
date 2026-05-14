# Source ledger diagnostic method

This directory is a repo-ready candidate for the next compute pass in `warp-complex/active_rail_paper`.

## Purpose

Compute the demanded classical source for the reduced active-rail metric:

```math
T_{\mu\nu}^{\rm demand}=\frac{1}{8\pi}G_{\mu\nu}[g]
```

with `G=c=1`.

This is a numerical Einstein-tensor diagnostic. It is not a matter model, not a constraint-quality initial-data solve, and not an RSET/semi-classical calculation.

## Critical assumption

The paper writes the reduced metric with an angular sector

```math
\gamma_{\Omega\Omega}(s,l)d\Omega^2,
```

but the existing obstruction screen only fixes the radial ADM sector. Therefore this source ledger is not unique until the angular closure is specified.

The default closure is:

```math
\gamma_{\Omega\Omega}=l^2+R_{\rm th}^2.
```

The script also exposes exploratory closure sweeps:

```text
static_throat
area_capacity_A2
area_capacity_B2
```

Every reported result must include the closure name.

## Suggested smoke run

From `warp-complex/active_rail_paper`:

```bash
python code/source_ledger.py --variant active_rail_catch_throat_gated --width-factor 1.0 --angular-closure static_throat --ns 21 --nl 31 --probe
```

Larger diagnostic run:

```bash
python code/source_ledger.py --variant active_rail_catch_throat_gated --width-factor 1.0 --angular-closure static_throat --ns 41 --nl 61 --probe
```

Sharp-layer comparison:

```bash
python code/source_ledger.py --variant active_rail_catch_throat_gated --width-factor 0.25 --angular-closure static_throat --ns 41 --nl 61 --probe
```

## Output files

The script writes:

```text
data/source_ledger_<variant>_w<width>_<closure>.json
data/source_ledger_<variant>_w<width>_<closure>_summary.csv
data/source_ledger_<variant>_w<width>_<closure>_points.csv
data/source_ledger_<variant>_w<width>_<closure>_convergence_probe.csv  # if --probe
```

## Channels

The script reports region/phase aggregates of:

- Eulerian energy density `rho_euler`
- Eulerian radial current `j_l_unit`
- radial pressure/tension `p_l_unit`
- angular pressure/tension `p_omega_unit`
- packet-comoving density `rho_packet`, where the packet worldline is timelike
- radial null contractions `Tkk_plus`, `Tkk_minus`
- Ricci scalar and metric condition number diagnostics

## Region and phase bins

Regions are provisional bins tied to the active-rail architecture:

```text
packet_in_support
packet_outer
core_throat
support_edge
outer_shoulder
exterior_tail
```

Phases are keyed to the existing service order:

```text
pre_catch_support
catch_rematch
held_transport
shift_fade
post_shift_pre_relax
throat_relax
reset_tail
```

## Interpretation rule

No source-ledger number should be cited without:

1. the angular closure,
2. width factor,
3. grid size,
4. derivative step size,
5. convergence-probe behavior.

Until the angular sector is physically selected, the reliable deliverable is localization and channel structure, not an invariant source magnitude.
