# Source-Realism Prescreen v0.1: Frozen Geometry Handoff

## Executive summary

Reference Geometry v0.3 remains the canonical access geometry. The source-realism prescreen confirms the open-interval compensation ledger and advances the next active task: promote the explicit positive compensation overlay into a conserved, physically interpretable stress tensor while accounting for support/shoulder source history during long radial prestretch and reset.

The geometry status is stable:

- \(B(l,t)\) supplies radial support dilution.
- \(R(l,t)\) supplies flare/access-state gating.
- \(N(l,t)\) supplies shoulder timing, redshift shaping, and matching control.
- The explicit positive overlay supplies the target repayment ledger.
- The shoulder region supplies buffer and transition containment.

The source-realism status is active:

- The effective geometric source \(T^{m geom}_{\mu
u}=G_{\mu
u}/8\pi\) is reconstructed on the frozen v0.3 lifecycle.
- The explicit compensation overlay supplies the desired null-contracted positive ledger during the compensation phase.
- The overlay now needs a full stress-tensor embedding: \(T_{tt},T_{ll},T_{tl},T_{	heta	heta}\), with conservation or a declared actuator-exchange term.
- The full-cycle ledger identifies support/shoulder source history during \(B\)-setup and \(B\)-reset as the next source-scheduling object.

This memo preserves the geometry freeze and opens the source-realism program. Geometry unfreezing becomes a design decision after the source program tests whether the setup/reset support-shoulder ledger can be modeled or scheduled cleanly.

## Frozen canonical geometry

The frozen reference is **Reference Geometry v0.3**:

\[
B_0=8.0,\quad w_B=10.0,\quad T_B=150.0,\quad T_R=5.0,\quad T_H=60.0,\quad T_C=20.0.
\]

The lifecycle is:

\[
	ext{flattened }R	ext{ standby}
ightarrow
B	ext{ prestretch}
ightarrow
R	ext{ flare opening}
ightarrow
	ext{quiet access hold}
ightarrow
R	ext{ closure}
ightarrow
	ext{balanced support/shoulder compensation with }N	ext{ shaping}
ightarrow
B	ext{ reset}.
\]

The compensation and shoulder-shaping settings are:

\[
A_{m support}=0.0082,\quad A_{m shoulder}=0.0019,\quad N_{m shoulder,amp}=-0.18.
\]

The phase times are:

| Phase boundary | Time |
|---|---:|
| \(B\)-setup end | 150.0 |
| \(R\)-open end | 155.0 |
| hold end | 215.0 |
| \(R\)-closure end | 220.0 |
| compensation end | 240.0 |
| \(B\)-reset end | 390.0 |

## Geometry status preserved

The invariant/proxy packet for v0.3 remains the geometry reference. Its source-history ledgers show balanced compensation in the open-interval accounting:

| Ledger | Open negative | Compensation positive | Ratio |
|---|---:|---:|---:|
| core line | 0.080748 | 0.087465 | 1.083 |
| support mean | 0.073111 | 0.076496 | 1.046 |
| shoulder mean | 0.007474 | 0.008291 | 1.109 |

Access isolation during compensation is strong:

| Diagnostic | Value |
|---|---:|
| access max flux during compensation | 9.480e-07 |
| access max \(|K^l{}_l|\) during compensation | 4.378e-09 |
| access max \(|K^	heta{}_	heta|\) during compensation | 1.161e-05 |
| access max \(|	heta_\pm|\) during compensation | 1.172e-04 |
| access min \(N\) during compensation | 1.000000 |
| access min \(R\) during compensation | 1.000000 |

The shoulder compensation bounds remain in the designed regime:

| Diagnostic | Value |
|---|---:|
| shoulder min \(N\) | 0.820036 |
| shoulder min \(R\) | 1.172512 |
| shoulder max flux during compensation | 1.374e-06 |
| shoulder max \(|\partial_l\ln N|\) | 0.300 |

This gives a frozen geometry reference with separated access, support, compensation, shoulder, and matching roles.

## Source-realism prescreen result

The prescreen reconstructs the required effective source and expands the ledger from the open interval to the full lifecycle. The open-interval compensation ledger remains balanced:

| Observer family | Open negative exposure | Compensation positive | Ratio | Repayment delay |
|---|---:|---:|---:|---:|
| core line | 0.080774 | 0.087466 | 1.083 | 45.00 |
| access mean | 0.082448 | 0.087313 | 1.059 | 45.00 |
| support mean | 0.073397 | 0.076940 | 1.048 | 45.00 |
| shoulder mean | 0.007596 | 0.008297 | 1.092 | 44.97 |

The compensation centroid occurs about 45 model-time units after the negative open-interval centroid. This delay is now a source-scheduling variable for quantum-interest-style analysis.

## Lorentzian sampled-stress screen

The prescreen applies a Lorentzian sampling proxy to observer-family \(T_{kk}\) histories. It uses the standard prototype scale

\[
C_{m QI}=rac{3}{32\pi^2},\qquad
\langle T_{kk}angle_	au \gtrsim -rac{C_{m QI}}{	au^4}.
\]

The current screen identifies the strongest sampled deficits as follows:

| Observer history | Worst \(	au\) | Worst center | Worst sampled average | Proxy bound | Margin |
|---|---:|---:|---:|---:|---:|
| core total | 5.0 | 176.963 | -1.082267e-03 | -1.519818e-05 | -1.067069e-03 |
| access total | 5.0 | 175.987 | -1.046657e-03 | -1.519818e-05 | -1.031459e-03 |
| support total | 2.0 | 8.287 | -9.179683e-03 | -5.936788e-04 | -8.586004e-03 |
| shoulder total | 2.0 | 8.287 | -8.786147e-03 | -5.936788e-04 | -8.192468e-03 |

The core/access histories concentrate their worst sampled deficit in the open/hold interval. The support/shoulder histories concentrate their strongest early deficits during radial prestretch. That pattern gives the next source-design target.

## Active source-design target

The active source target is the **setup/reset support-shoulder ledger**. The v0.3 geometry carries clean access isolation, and the source program now assigns the long \(B\)-setup/reset support-shoulder history to one of three source-side treatments:

1. **Standby infrastructure source model.** Treat the support/shoulder setup/reset contribution as part of the support plant's maintained source state.
2. **Setup/reset repayment schedule.** Add source-side compensation windows dedicated to support/shoulder observer families during or after radial prestretch/reset.
3. **Geometry v0.4 trigger.** Modify the standby shoulder geometry if the source model and source schedule produce poor sampled-stress behavior.

The first task is source embedding rather than geometry redesign.

## Source-embedding task

The explicit overlay currently specifies the target positive null-contracted component. The next step is a minimal conserved anisotropic stress ansatz:

\[
T^\mu{}_{
u}
=
\operatorname{diag}(-ho,p_r,p_t,p_t)+T^t{}_l
\]

with support and shoulder pulses fitted so that

\[
T_{kk}^{m ansatz}pprox T_{kk}^{m overlay}
\]

during compensation. The ansatz should report:

- conservation residuals \(
abla_\mu T^{\mu
u}\);
- energy density, radial pressure, angular pressure, and flux histories;
- support/shoulder localization;
- sampled \(T_{kk}\) along core, support, shoulder, and matching observer families;
- actuator-exchange terms if conservation closes through external control.

## Status statement for the report

Reference Geometry v0.3 is frozen as the canonical access geometry. Source-realism prescreen v0.1 validates the open-interval compensation ledger and identifies the setup/reset support-shoulder source history as the active full-cycle source ledger. The next stage builds a conserved stress-tensor embedding for the explicit compensation overlay and tests source scheduling for the setup/reset support-shoulder family.

## Included materials

This bundle includes:

- source-realism prescreen code;
- source-realism prescreen tables;
- v0.3 invariant/geometry reference outputs;
- v0.3 polish context outputs;
- report progress notes;
- this memo.
