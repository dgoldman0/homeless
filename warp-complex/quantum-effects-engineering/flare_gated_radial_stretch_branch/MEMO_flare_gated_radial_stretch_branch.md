# Flare-Gated Radial Stretch: Coupled B,R Control for Source-History-Aware Wormhole Support Screening

## Executive summary

The adiabatic radial-stretch protocol established `B(l,t)` as a useful radial proper-length actuator for a prescribed wormhole-support geometry:

```math
ds^2=-dt^2+B(l,t)^2dl^2+R_0(l)^2d\Omega^2,
\qquad R_0(l)=\sqrt{1+l^2}.
```

That screen showed a real control advantage: increasing the ramp time lowers peak radial-rate, acceleration, and shoulder-flux budgets during setup/reset. The source-history screen then supplied the next design requirement. With `R_0(l)` fixed, the `A_B=0` state still contains the areal throat `R_0(l)=sqrt(1+l^2)`. The full cycle therefore keeps the flare-support geometry active through the long `B` setup and reset intervals.

The new branch adds `R(l,t)` as the flare-state actuator. Its job is **flare gating**: flatten the standby flare curvature, prestretch the radial infrastructure with `B`, restore the access flare for a quiet hold, close the flare, and then reset `B`.

The tested protocol is:

```math
B\text{-prestretch}
\rightarrow
R\text{-flare-open}
\rightarrow
\text{quiet hold}
\rightarrow
R\text{-flare-close}
\rightarrow
B\text{-reset}.
```

This branch sharply improves the source-history ledger. For the representative `B0=8, wB=8, TH=60` cases, the earlier `B`-only cycle gives full-cycle core negative exposure from about `0.448` at `Tr=10` to `3.809` at `Tr=100`. The flare-gated branch with `TB=100` gives `0.081-0.112` across `TR=5-30`. The result supports a clear design allocation: `B` prestretches and dilutes the local support burden; `R` controls the flare/access state; the access hold freezes both actuators.

The branch is a geometry/control improvement at the prescribed-source level. Source realism, null-contracted quantum-inequality sampling, backreaction, matching, and shoulder compensation remain the next development gates. The immediate advance is operational: the long `B` setup/reset phases can be carried while the core flare is flattened, and the remaining core negative exposure is concentrated into `R`-open, hold, and `R`-close.

## 1. What the B-only screen established

The previous adiabatic protocol used

```math
B(l,t)=1+(B_0-1)F_B(l)A_B(t),
\qquad
R(l,t)=\sqrt{1+l^2}.
```

It produced the desired peak-dynamics scaling:

```math
\max |B_t/B| \sim T_r^{-1},
\qquad
\max |T_{\hat t\hat l}| \sim T_r^{-1},
\qquad
\max |B_{tt}/B| \sim T_r^{-2}.
```

Those results identify `B(l,t)` as a strong actuator for radial proper-length control. The quiet hold inherits the static long-throat benefit, while the setup/reset disturbances decrease under slower `B` ramps.

The source-history screen added a second metric: the support observer's accumulated null-contracted exposure over the full cycle. At the core of the fixed-`R` model,

```math
T_{kk}(0,t) \approx -\frac{1}{4\pi B(0,t)^2}.
```

Longer `B` ramps lower peak rate/flux and extend the time spent carrying the fixed areal flare. The design lesson is direct: `B` supplies support dilution, and a separate areal-geometry control is needed to manage the active flare state during setup/reset.

## 2. Framework alignment

The screening framework assigns subsystem roles before making source-realism claims:

```math
B(l,t) \rightarrow \text{radial proper-length and support-dilution control},
```

```math
R(l,t) \rightarrow \text{areal access geometry and flare shaping},
```

```math
N(l,t) \rightarrow \text{redshift, timing, matching, and horizon control}.
```

The `B`-only screen advanced through the dynamic-cleanliness gate and activated the source-history gate. That result sends the design back to the framework's role-allocation layer, where `R` naturally enters as the areal flare/access-state control.

The dynamic gate also gives the access rule for `R`:

```math
\theta_\pm=\frac{2}{R}\left(\frac{R_t}{N}\pm\frac{R_l}{B}\right).
```

During traversal, the design keeps

```math
R_t\approx0,
\qquad B_t\approx0.
```

During setup/reset, `R` participates through flare opening and closure. This follows the framework sequence:

```math
B\text{-only geometry screen}
\rightarrow
\text{source-history gate}
\rightarrow
R\text{ flare/access-state control}
\rightarrow
\text{new source-history screen}.
```

## 3. Updated design: flare-gated radial stretch

The branch uses the prescribed metric

```math
ds^2=-dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The radial actuator is

```math
B(l,t)=1+(B_0-1)F_B(l)A_B(t),
\qquad
F_B(l)=\exp[-(|l|/w_B)^4].
```

The access areal profile is

```math
R_{\rm access}(l)=\sqrt{1+l^2}.
```

The standby profile is

```math
R_{\rm standby}(l)
=
R_{\rm access}(l)
+
W_R(l)\left(R_c-R_{\rm access}(l)\right),
\qquad
W_R(l)=\exp[-(|l|/w_R)^4].
```

The branch screen used `Rc=1` as the clean first target. This keeps the core radius essentially fixed while changing the local flare curvature:

```math
R_{\rm standby}(0)=R_{\rm access}(0)=1,
\qquad
R'_{\rm standby}(0)\approx0,
\qquad
R''_{\rm standby}(0)\approx0.
```

The time schedule is

```math
R(l,t)=R_{\rm standby}(l)+A_R(t)
\left(R_{\rm access}(l)-R_{\rm standby}(l)\right).
```

The operational phases are:

1. **B-prestretch:** increase `B` while the core flare is flattened.
2. **R-flare-open:** restore the access flare after the radial infrastructure is stretched.
3. **Quiet hold:** freeze `B` and `R` for access.
4. **R-flare-close:** flatten the flare after access.
5. **B-reset:** return the radial infrastructure after the flare is closed.

This gives the name **flare-gated radial stretch**.

## 4. Reduced source-history test

The script reconstructs effective source proxies from `G_{mu nu}/8pi` for the warped-product metric. It computes the radial null contractions

```math
T_{kk}^{\pm}=T_{tt}+T_{ll}/B^2\pm2T_{tl}/B,
```

and records

```math
T_{kk}^{\rm min}=\min(T_{kk}^{+},T_{kk}^{-}).
```

The main history score is the core negative exposure

```math
I^-_{\rm core}=\int[-T_{kk}^{\rm min}(l=0,t)]_+\,dt.
```

This diagnostic screens whether a control protocol concentrates support history into the intended access interval while keeping the setup/reset ledger small. It is the branch-level source-history ledger that comes before a full quantum-field source model.

## 5. Main results

### 5.1 B-only comparison

Representative cases with `B0=8, wB=8, TH=60`:

| Case | full-cycle core negative exposure | max access `|B_t/B|` | max access flux |
|---|---:|---:|---:|
| old B-only `Tr=10` | 0.447826 | 0.434358 | 0.004539 |
| old B-only `Tr=30` | 1.194719 | 0.144786 | 0.001513 |
| old B-only `Tr=100` | 3.808845 | 0.043456 | 0.000454 |
| flare-gated `TB=100, TR=5` | 0.080579 | 0.043467 | 0.000791 |
| flare-gated `TB=100, TR=10` | 0.086777 | 0.043467 | 0.000395 |
| flare-gated `TB=100, TR=30` | 0.111570 | 0.043466 | 0.000132 |

The comparison shows the design gain. The fixed-`R` `B` cycle trades peak cleanliness against a long active-flare history. The flare-gated branch carries the long `B` setup/reset phases with a flattened core flare, so the full-cycle core exposure stays far below the comparable `B`-only cases.

### 5.2 Phase ledger for the representative branch

For `B0=8, wB=8, wR=5, Rc=1, TB=100, TR=10, TH=60`:

| Phase | core negative exposure | design reading |
|---|---:|---|
| B setup | 4.37e-7 | radial infrastructure stretches while the core flare is flat |
| R open | 0.006043 | flare support appears during access-geometry opening |
| hold | 0.074225 | quiet-hold support burden dominates the ledger |
| R close | 0.006198 | closure carries a small flare-history cost |
| B reset | 4.37e-7 | radial reset occurs after flare closure |
| full cycle | 0.086777 | source history is concentrated into open/hold/close |

The phase ledger supplies the central result: the long `B` phases contribute essentially zero core exposure once `R` controls the flare state.

### 5.3 Order matters

For `B0=8, wB=8, TB=100, TR=30, TH=60`:

| Order | full-cycle core negative exposure | design reading |
|---|---:|---|
| B first, then R open | 0.111570 | radial support dilution is in place before flare activation |
| simultaneous B,R with `TB=100, TR=30` | 1.725187 | the flare is active during part of radial stretching |
| R first, then B | 6.188991 | the active flare is carried through the unstretched radial state |

The design rule is:

```math
\text{Stretch first while flare is flat; open the flare after B is already large.}
```

### 5.4 Stretch strength matters

For `wB=8, TB=100, TR=10, TH=60`:

| B0 | full-cycle core negative exposure | hold `Tkk(0)` |
|---:|---:|---:|
| 3 | 0.617076 | -0.008815 |
| 5 | 0.222148 | -0.003174 |
| 8 | 0.086777 | -0.001240 |

A larger `B` stretch lowers the restored-hold support burden. This is the long-throat support-dilution branch in operational form: radial proper-length stretch weakens the local null-contracted burden while source realism remains the next physics gate.

## 6. Design interpretation

The branch has a precise actuator allocation:

```math
\text{flare-gated radial stretch}:
\quad
R\text{ controls flare state, }B\text{ controls support dilution.}
```

The useful `R` action is flare-curvature control. With `Rc=1`, the core radius stays approximately fixed across standby and access, so the access-core `R_t/R` budget remains small. The flare condition is restored only after `B` has built the radial proper-length infrastructure.

The `B`-only screen remains the foundation of this branch. It established the support-dilution actuator and the adiabatic ramp scaling. The source-history screen then identified the areal flare as a controlled subsystem, exactly as the framework assigns `R(l,t)`.

## 7. Development gates

This branch sits at the geometry/control stage and advances the source-history ledger. The next gates are:

1. **Quiet-hold source realism:** identify a quantum/effective source that carries the restored-hold `Tkk` history.
2. **Null-contracted QI sampling:** replace the integrated exposure proxy with sampled-stress windows for throat, shoulder, and traversing observers.
3. **Backreaction and stability:** evolve a candidate source or initial-data construction and track ringing or feedback.
4. **Matching and boundary interpretation:** connect the flattened standby profile to a cap, boundary, matching layer, exterior, or topology model.
5. **Shoulder stress and compensation:** add explicit shoulder/buffer/source-management terms and scan off-core observer families.

These gates turn the present control improvement into the next source-realism test program.

## 8. Next branch

The next branch should keep the successful ordering and add compensation/source scheduling:

```math
B\text{-prestretch while flare is flat}
\rightarrow
R\text{-flare-open}
\rightarrow
\text{quiet hold}
\rightarrow
R\text{-flare-close}
\rightarrow
B\text{-reset}
\rightarrow
\text{shoulder compensation/source reset}.
```

The next objective should combine dynamic cleanliness with sampled source history:

```math
J =
w_1\max|B_t/B|
+w_2\max|R_t/R|
+w_3\max|T_{\hat t\hat l}|
+w_4\int[-T_{kk}]_+dt
+w_5\max_{\tau_s,\tau_0}\int T_{kk}(\tau)g_{\tau_s,\tau_0}(\tau)d\tau
+w_6S_{\rm shoulder}.
```

The immediate design question is which shoulder mechanism—`R`, lapse `N`, or explicit source terms—can provide positive compensation while preserving the quiet access observer family.

## 9. Bottom-line conclusion

The results support the move from the `B`-only adiabatic protocol to the coupled `B,R` design named **flare-gated radial stretch**.

- `B` prestretches and dilutes the support burden.
- `R` gates the flare/access state by flattening and restoring flare curvature.
- The access hold keeps `B_t≈0` and `R_t≈0`.
- The branch sharply reduces full-cycle core negative exposure compared with `B`-only ramps.
- The branch advances naturally to shoulder compensation and null-contracted sampled-stress tests.
