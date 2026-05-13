# Candidate Source Model v0.2: Full Nonminimally Coupled Scalar Compatibility Screen

## Executive summary

This report records the second candidate-source screen for the frozen Reference Geometry v0.3. The screen advances from the reduced scalar operator used in v0.1 to the full null-contracted channel of a nonminimally coupled scalar field. The leading result is a clean source allocation:

\[
T_{\mu\nu}^{\rm total}
=
T_{\mu\nu}^{\rm NMC\ support}
+
T_{\mu\nu}^{\rm infrastructure\ repayment}
+
T_{\mu\nu}^{\rm shoulder/matching}.
\]

The full scalar channel improves the core/access fit substantially. The core-line relative RMS error moves from 0.553 to 0.382, and the access-mean relative RMS error moves from 0.662 to 0.392. The corresponding correlations rise to 0.949 and 0.941. The scalar branch therefore remains a strong support-component candidate.

The support-ring and shoulder infrastructure ledgers continue to classify as infrastructure-source tasks. The support-mean and support-ring fits stay weak under the full scalar screen, with relative errors around unity and correlations near zero. The rank-one consistency check assigns the single-field global interpretation to a low-priority branch. The selected architecture is a hybrid source model: nonminimally coupled scalar stress channels for the core/access support component, plus an infrastructure/repayment component for setup/reset and shoulder matching.

The result is a source-architecture decision, not a physical-source closure. The next phase is Candidate Source Model v0.3: fit the scalar support component and the infrastructure repayment component separately, then enforce conservation or explicit actuator exchange for the infrastructure sector.

## 1. Context and purpose

The frozen geometry is Reference Geometry v0.3, a compensated flare-gated radial-stretch lifecycle:

\[
\text{flattened }R\text{ standby}
\rightarrow
B\text{ prestretch}
\rightarrow
R\text{ flare opening}
\rightarrow
\text{quiet hold}
\rightarrow
R\text{ closure}
\rightarrow
\text{balanced compensation}
\rightarrow
B\text{ reset}.
\]

Geometry screening established the control allocation:

\[
B(l,t) \rightarrow \text{radial support dilution},
\]

\[
R(l,t) \rightarrow \text{flare/access-state gating},
\]

\[
N(l,t) \rightarrow \text{timing, matching, and shoulder shaping},
\]

\[
T^+_{kk,\rm overlay} \rightarrow \text{repayment target}.
\]

Source-realism prescreen v0.2 then organized the source target into a phase-structured ledger: open support, open repayment, setup/reset infrastructure repayment, and shoulder/matching control. Candidate Source Model v0.1 tested a reduced nonminimal-scalar second-derivative channel, which matched the core/access timing better than the full infrastructure ledger. Candidate Source Model v0.2 tests the fuller scalar stress channel to determine the role of the NMC scalar branch in the source architecture.

## 2. Literature placement

Traversable wormhole throat support begins with the Morris--Thorne flare-out condition, which requires radial null-energy-condition violation near the throat [MorrisThorne1988]. Ford--Roman quantum inequalities add the key sampled-energy constraint: macroscopic support faces severe restrictions unless the geometry uses extreme length-scale discrepancy or source histories that satisfy quantum-field-theoretic bounds [FordRoman1996]. Quantum interest further makes compensation a structured timing and overcompensation problem rather than global bookkeeping [FordRoman1999]. Fewster--Roman null-contracted quantum-inequality tests are directly relevant to the present observer-family screens because they constrain null-contracted stress-energy averaged along timelike worldlines [FewsterRoman2005].

Nonminimally coupled scalar fields remain a serious GR-adjacent source candidate because the coupling introduces curvature and second-derivative stress channels that can violate standard energy conditions. Barceló and Visser showed that nonminimal scalar coupling can violate even averaged energy conditions and can support wormhole branches under appropriate conditions, while also highlighting strong amplitude and consistency requirements [BarceloVisser2000]. This makes the NMC scalar branch a natural first candidate after the effective-fluid bridge.

Modern holographic traversability results, including Gao--Jafferis--Wall, demonstrate that controlled interactions can generate negative averaged null energy in special quantum-gravity settings [GaoJafferisWall2017]. That literature supports the source-scheduling lesson while placing a high bar on physical realization. The present screen remains in the semiclassical/effective-source lane: it maps the v0.3 target ledger onto candidate stress-tensor structures.

## 3. Candidate source model

The NMC scalar stress tensor is

\[
T_{\mu\nu}^{\rm NMC}
=
\nabla_\mu\phi\nabla_\nu\phi
-
\frac12 g_{\mu\nu}(\nabla\phi)^2
-g_{\mu\nu}V(\phi)
+
\xi\left[
G_{\mu\nu}\phi^2
-\nabla_\mu\nabla_\nu(\phi^2)
+g_{\mu\nu}\Box(\phi^2)
\right].
\]

For null-contracted screening, the metric-proportional terms drop out because \(g_{\mu\nu}k^\mu k^\nu=0\). The tested null channel is therefore

\[
T_{kk}^{\rm NMC}
=
(k^\mu\nabla_\mu\phi)^2
+
\xi\left[
G_{kk}\phi^2
-k^\mu k^\nu\nabla_\mu\nabla_\nu(\phi^2)
\right].
\]

The screen uses smooth scalar-mode basis functions \(\phi_i(l,t)\) over the lifecycle phases. It fits the quadratic feature space generated by \(\phi_i\phi_j\), derivative terms, and the geometric \(G_{kk}\phi^2\) channel. It then performs a rank-one consistency check. A positive rank-one matrix corresponds to one smooth scalar field \(\phi(l,t)\). A broad quadratic fit with poor rank-one compression corresponds to an effective multi-component scalar-feature model or a source architecture with additional infrastructure components.

The scan tested the conformal value \(\xi=1/6\) and a stronger positive coupling \(\xi=0.5\). The best fit selected \(\xi=0.5\).

## 4. Results

### 4.1 Coupling scan

| \(\xi\) | quadratic-feature weighted relative RMSE | quadratic-feature weighted score | rank-one weighted relative RMSE |
|---:|---:|---:|---:|
| 0.5 | 0.962 | 0.0569 | \(2.33\times10^9\) |
| 1/6 | 0.976 | 0.0291 | \(2.45\times10^9\) |

The stronger positive coupling supplies the better scalar-feature fit in this basis. The global weighted score remains modest because the support-ring, matching, and setup/reset infrastructure features dominate the unresolved part of the target ledger.

### 4.2 Observer-family fit metrics

| Observer family | Relative RMS error | Correlation | Interpretation |
|---|---:|---:|---|
| core line | 0.382 | 0.949 | strong scalar support-component match |
| access mean | 0.392 | 0.941 | strong scalar support-component match |
| support mean | 1.003 | 0.081 | infrastructure ledger dominates residual |
| support ring mean | 0.989 | 0.055 | infrastructure ledger dominates residual |
| shoulder mean | 0.881 | 0.553 | partial shoulder structure match |
| matching mean | 49.9 | -0.692 | matching sector assigned to infrastructure/matching source |

The scalar branch supplies a coherent core/access component. The support ring and matching sectors select a separate source role.

### 4.3 v0.1 to v0.2 comparison

| Observer family | v0.1 relative error | v0.2 relative error | v0.1 correlation | v0.2 correlation |
|---|---:|---:|---:|---:|
| core line | 0.553 | 0.382 | 0.852 | 0.949 |
| access mean | 0.662 | 0.392 | 0.779 | 0.941 |
| support mean | 0.961 | 1.003 | 0.281 | 0.081 |
| support ring mean | 0.894 | 0.989 | 0.338 | 0.055 |
| shoulder mean | 0.921 | 0.881 | 0.465 | 0.553 |

The fuller scalar screen sharpens the architecture. It advances the core/access source candidate and assigns the support-ring/setup-reset ledger to the infrastructure-source branch.

### 4.4 Feature and rank-one diagnostics

The top quadratic terms couple the compensation core mode with setup/reset matching-ring and shoulder-ring modes. This is an informative signature: the unrestricted quadratic feature fit can span phase-cross terms that a single scalar field cannot freely realize as independent infrastructure behavior.

The rank-one check produces very large coefficients and catastrophic residual values. That result classifies a one-field global scalar model as a low-priority branch for the full lifecycle. It also strengthens the hybrid interpretation: scalar support channels remain valuable, and infrastructure repayment channels carry the support-ring and shoulder ledgers.

## 5. Source-architecture interpretation

The selected source architecture is

\[
T_{\mu\nu}^{\rm total}
=
T_{\mu\nu}^{\rm NMC\ scalar\ support}
+
T_{\mu\nu}^{\rm infrastructure\ repayment}
+
T_{\mu\nu}^{\rm shoulder/matching}.
\]

The NMC scalar branch contributes the core/access support stress because the full scalar null channel matches those observer-family histories with high correlation. The infrastructure branch carries setup/reset support-ring repayment and shoulder/matching control because those ledgers require phase-localized, zone-localized structure beyond the one-field scalar screen.

This allocation is consistent with the geometry framework. The geometry already separated support, access, repayment, buffer, matching, and transition functions. The source screen now gives the parallel source allocation: scalar support, infrastructure repayment, and shoulder/matching source control.

## 6. Current status

Reference Geometry v0.3 remains frozen as the canonical geometry. Candidate Source Model v0.2 advances source realism from a ledger overlay to a component architecture. The active source branch is now hybrid.

The scalar candidate has a clear role:

\[
\text{NMC scalar} \rightarrow \text{core/access exotic support component}.
\]

The infrastructure source has a clear role:

\[
\text{effective conserved infrastructure sector} \rightarrow \text{setup/reset repayment and shoulder/matching}.
\]

The next screen should fit these components separately and enforce conservation or explicit actuator exchange in the infrastructure sector.

## 7. Recommended next phase: Candidate Source Model v0.3

Candidate Source Model v0.3 should use a hybrid fit from the start.

1. Fit the NMC scalar support component only to core/access and broad open-support windows.
2. Fit an anisotropic infrastructure source to setup/reset support-ring and shoulder/matching windows.
3. Compute the conservation residual

\[
\nabla_\mu T^{\mu\nu}_{\rm infrastructure}
\]

and identify any required exchange current

\[
J^\nu_{\rm actuator}.
\]

4. Re-run observer-family sampled \(T_{kk}\) using the fitted scalar-plus-infrastructure tensor rather than overlay targets.
5. Rank source families for the infrastructure sector: effective anisotropic fluid, boundary/actuator source, squeezed-state scheduling with quantum-interest constraints, and modified-effective source as a separate theory branch.

## 8. Bundle contents

This bundle includes:

- the v0.2 candidate-source script;
- the v0.2 scalar fit metrics, feature coefficients, rank-one diagnostics, observer ledgers, and timeseries digest;
- v0.1 context for comparison;
- source-realism v0.2 context;
- frozen Reference Geometry v0.3 context;
- figures for observer errors, v0.1/v0.2 comparison, and coupling scan;
- a bibliography and manifest.

## References

See `references.bib` in this report directory.
