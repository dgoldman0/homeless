# Shoulder-Optimized Compensated Flare-Gated Radial Stretch

## Summary

This screen optimizes the shoulder subsystem for the compensated flare-gated radial-stretch design. The design now has a complete geometry-control lifecycle:

```math
B\text{-prestretch}
\rightarrow
R\text{-flare opening}
\rightarrow
\text{quiet access hold}
\rightarrow
R\text{-closure}
\rightarrow
\text{compensation phase with shoulder }R/N\text{ shaping}
\rightarrow
B\text{-reset}.
```

The optimized division of labor is:

| Subsystem | Active role |
|---|---|
| `B(l,t)` | radial support dilution and prestretched infrastructure |
| `R(l,t)` | flare/access-state gating plus shoulder buffer shaping |
| `N(l,t)` | timing, lapse shaping, matching, and compensation isolation |
| explicit positive source overlay | repayment carrier |
| shoulders | transition, buffer, and compensation-distribution subsystem |

The main result is affirmative: the shoulder can be optimized into a clean buffer/matching subsystem while explicit source terms carry the main positive repayment ledger. A separated support-plus-shoulder compensation overlay gives balanced repayment without meaningful access-core dynamic leakage in this reduced screen.

## Baseline debt ledger

The reference geometry uses `B0=8`, `wB=8`, `T_B=100`, `T_R=10`, `T_H=60`, and `T_C=20`.

The open interval is:

```math
R\text{-open} + \text{hold} + R\text{-close}.
```

The baseline open-interval negative exposure is:

| Ledger | Open negative exposure |
|---|---:|
| access mean | 0.088046 |
| core line | 0.086591 |
| support mean | 0.078333 |
| shoulder mean | 0.007657 |

These values define the repayment target for the compensation phase.

## Geometry-only shoulder optimization

The screen tested shoulder-only `R`, shoulder-only `N`, and combined shoulder `R/N` pulses during the compensation phase.

The geometry-only shoulder controls keep the access contamination metric small. Their strongest role is buffer and transition shaping. The best geometry-only cases delivered modest shoulder repayment and preserved clean access isolation.

| Branch | Best support ratio | Best core-line ratio | Best shoulder ratio | Access leakage |
|---|---:|---:|---:|---:|
| baseline | 0.000 | 0.000 | 0.000 | 0.000038 |
| shoulder_N | 0.000 | 0.000 | 0.000 | 0.000038 |
| shoulder_R | 0.038 | 0.120 | 0.106 | 0.000038 |
| combined_RN | 0.000 | 0.000 | 0.050 | 0.000038 |


The geometry-only conclusion is:

```math
R_{\rm shoulder},N_{\rm shoulder}
\rightarrow
\text{buffer, transition, timing, and isolation shaping}.
```

## Balanced compensation optimization

The strongest compensation architecture uses separate positive overlays for the support and shoulder ledgers:

```math
T^+_{\rm comp}(l,t)
=
A_s C(t) W_{\rm support}(l)
+
A_h C(t) W_{\rm shoulder}(l).
```

The leading balanced case from the sweep is:

```text
sup0.0087_sh0.0020_Nshape
```

with the following repayment ratios:

| Ledger | Compensation ratio |
|---|---:|
| core line | 1.078 |
| support mean | 1.050 |
| shoulder mean | 1.063 |

The dynamic isolation metrics for the same case are:

| Diagnostic | Value |
|---|---:|
| access compensation leakage metric | 0.000038 |
| shoulder compensation spike metric | 0.000579 |
| access minimum lapse during compensation | 1.000 |
| shoulder minimum lapse during compensation | 1.000 |
| shoulder minimum areal radius during compensation | 1.168 |

This is the best reference point for the next geometry memo because it balances the three repayment ledgers near unity while keeping the access-family leakage metric far below the provisional threshold of `0.002`.

## Design interpretation

The optimized shoulder geometry supplies three positive functions.

First, it preserves access isolation. The shoulder activity is spatially separated from the access core and scheduled after `R` closure.

Second, it shapes the compensation region. Shoulder `R` adjusts transition geometry and shoulder support distribution. Shoulder `N` adjusts timing and lapse structure for compensation and matching.

Third, it gives the explicit source overlay a clean geometric container. The separated support-plus-shoulder overlay gives a better ledger balance than a broad single overlay because each repayment function has its own spatial carrier.

## Updated reference design

The next reference design should use:

| Parameter | Reference value |
|---|---:|
| `B0` | 8 |
| `wB` | 8 |
| `T_B` | 100 |
| `T_R` | 10 |
| `T_H` | 60 |
| `T_C` | 20 |
| support compensation amplitude | 0.0087 |
| shoulder compensation amplitude | 0.0020 |
| optional shoulder lapse amplitude | +0.3 |
| shoulder center | 2.5 |
| shoulder width | 1.2 |

The shoulder lapse is useful as a matching/timing control. The balanced source ratios remain clean with or without it; the lapse-shaped version is preferred for the next reference design because it exercises the matching subsystem while preserving access isolation.

## Geometry status

This screen moves the geometry-engineering program from branch selection to reference-design finalization.

The geometry part now has:

1. support dilution through `B`;
2. flare/access-state control through `R`;
3. quiet access hold;
4. post-closure compensation phase;
5. shoulder buffer and matching controls;
6. balanced repayment ledgers in the reduced screen;
7. access-family isolation during compensation.

The remaining geometry tasks are canonical reference documentation, invariant diagnostics, and a final observer-family gate table. Source realism, quantum-state construction, and backreaction remain later gates.
