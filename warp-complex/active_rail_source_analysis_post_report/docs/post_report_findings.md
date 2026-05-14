# Post-report active-rail source analysis: soft angular jacket test

**Status:** diagnostic work only. **Do not refreeze the design yet.**

This folder contains the work done after the previous source-ledger report. The specific question was whether the emerging **soft angular jacket** candidate is strong enough to become the next frozen active-rail design. The answer from this test is:

> The candidate is a real source-routing improvement, but the remaining caveats are too large to refreeze.

## Candidate tested

The active-rail service geometry was kept fixed:

- support-contained shift,
- catch before release,
- same radial ADM sector,
- same packet/service timing,
- same active branch.

Only the angular closure was changed.

Baseline:

\[
\gamma_{\Omega\Omega} = l^2 + R_{\rm th}^2 .
\]

Soft angular jacket:

\[
\gamma_{\Omega\Omega} =
(l^2 + R_{\rm th}^2) C_\Omega(s,l)^2
\]

with

\[
C_\Omega(s,l) = \exp(a_\Omega Q_\Omega(s) W_\Omega(l)).
\]

Candidate parameters:

```text
a_Omega  = 0.35
R_Omega  = 1.25
w_Omega  = 0.70
x_Omega  = 2.00
w_tOmega = 0.60
```

Interpretation: mild angular expansion, broad radial edge, held through shift fade and throat relaxation, then reset.

## Computation

The diagnostic computes the demanded source,

\[
T_{\mu\nu}^{\rm demand} = \frac{1}{8\pi} G_{\mu\nu},
\]

in geometrized units, using a spherically symmetric warped-product reduction.

Observer/source channels reported:

- Eulerian density \(\rho\),
- radial source current \(|j_l|\),
- radial pressure/tension \(|p_l|\),
- angular pressure/tension \(|p_\Omega|\),
- packet-frame density \(\rho_{\rm pkt}\),
- radial null contractions \(T_{kk}^\pm\),
- packet norm and support-edge \(g_{tt}\) as clearance checks.

High-resolution check:

```text
s grid: 251
l grid: 375
s range: [-0.45, 3.25]
l range: [-2.8, 2.8]
```

## Main result

The soft angular jacket improves the null/source exposure substantially while preserving packet and stationary-monitor clearance.

| Diagnostic | Static angular closure | Soft angular jacket | Change |
|---|---:|---:|---:|
| packet-positive points | 0 | 0 | unchanged |
| max packet norm on packet | -0.75 | -0.75 | unchanged |
| support-edge gtt-positive points | 0 | 0 | unchanged |
| worst service-edge Tkk | -1.27856 | -0.418534 | improved |
| worst packet-support Tkk | -1.31663 | -0.614683 | improved |
| worst packet-support rho_pkt | -0.240293 | -0.061961 | improved |
| worst Eulerian rho overall | -0.0969108 | -0.0282269 | improved |
| max radial current | 0.288908 | 0.193168 | improved |
| max radial pressure/tension | 0.0779825 | 0.0512719 | improved |
| max angular pressure/tension | 1.29255 | 1.28139 | nearly unchanged |
| late-tail support-edge Tkk | -0.0149092 | -0.0389498 | worse tail debt |

## Interpretation

The soft jacket works as a **source-routing layer**. It reduces:

- support-edge null negativity,
- packet-support null exposure,
- packet-frame negative density,
- Eulerian negative density,
- radial current,
- radial pressure/tension.

It does **not** solve the angular-pressure ceiling. The maximum angular pressure/tension changes only slightly:

```text
static:      1.29255
soft jacket: 1.28139
```

That is the main reason not to refreeze.

## The useful design lesson

The soft angular jacket confirms the direction:

> Angular capacity should be mild, broad, and held through fade/relax.

But it also shows the missing piece:

> Angular pressure and late-tail reset debt need their own design controls.

So the design should not be refrozen as-is. The next stage should add a reset-tail cleaner and an angular-pressure reducer without disturbing the packet/source-routing gains.

## Reset sensitivity

The bundle includes a reset-taper sensitivity file:

```text
data/reset_taper_sensitivity.csv
```

A simple weighted diagnostic score favored earlier/sharper angular reset settings than the candidate in some cases, but those settings can raise radial pressure or alter the packet-centered balance. That means the reset problem is a real tradeoff, not a simple “delay more” knob.

Best-scoring sensitivity cases by the provisional score are in the CSV. They should be treated as leads, not final candidates.

## Decision

**Do not refreeze yet.**

The candidate remains the best architectural direction from the post-report tests:

```text
catch-rematched active rail
+ support-contained shift
+ soft angular jacket
```

but the unresolved gates are still large:

1. angular pressure/tension ceiling,
2. late-tail reset debt,
3. convergence/derivative robustness beyond finite-difference diagnostics,
4. later constraint-quality and off-axis tests.

## Files

```text
code/controlled_angular_source_test.py
data/high_resolution_baseline_vs_candidate_metrics.csv
data/grid_convergence_baseline_vs_candidate.csv
data/region_phase_ledger_high_resolution.csv
data/reset_taper_sensitivity.csv
data/summary.json
figures/baseline_vs_soft_jacket_metrics.png
figures/support_edge_null_by_phase.png
figures/packet_support_rho_pkt_by_phase.png
figures/reset_sensitivity_*.png
```
