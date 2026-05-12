# Flare-Gated Radial Stretch: Moving from B-Only Control to a Coupled B,R Protocol

## Executive summary

The earlier adiabatic radial-stretch protocol used the metric

```math
ds^2 = -dt^2 + B(l,t)^2 dl^2 + R_0(l)^2 d\Omega^2,
\qquad R_0(l)=\sqrt{1+l^2}.
```

That protocol correctly identified `B(l,t)` as a strong radial proper-length actuator. It softened local support during the hold and made setup/reset peak-rate and flux budgets scale down with ramp time. The serious source-history screen changed the interpretation: with `R_0(l)` held fixed, the `A_B=0` state is still an active areal throat. The system was not cycling between an ordinary standby state and an active throat. It was cycling between an unstretched exotic throat and a stretched exotic throat.

The new branch therefore lets `R(l,t)` participate. The role of `R` is not rapid access-core breathing during traversal. The role is **flare gating**: use `R` to flatten the standby flare curvature and restore the flared access geometry only after `B` has already been stretched.

The best reduced protocol tested here is:

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

This branch strongly improves the source-history ledger relative to the old `B`-only cycle. For the representative `B0=8, wB=8, TH=60` cases, the old `B`-only full-cycle core negative exposure grows from about `0.448` at `Tr=10` to `3.809` at `Tr=100`. The flare-gated branch with `TB=100` gives `0.081-0.112` across `TR=5-30`. This confirms that `R` participation is useful in the exact way the screening framework predicted: `B` remains the support-dilution actuator, while `R` supplies areal flare state and access-geometry control.

The branch still does not pass source realism. The quiet hold carries the same remaining support burden, approximately `Tkk(0)=-1/(4 pi B0^2)` for the restored access throat. The value of the branch is that it localizes the core negative history to the `R`-open/hold/`R`-close interval instead of letting the long `B` setup/reset phases carry throat support debt.

## 1. Why B-only was no longer enough

The B-only adiabatic protocol used

```math
B(l,t)=1+(B_0-1)F_B(l)A_B(t),
\qquad
R(l,t)=\sqrt{1+l^2}.
```

The prior result was positive at the peak-dynamics level:

```math
\max |B_t/B| \sim T_r^{-1},
\qquad
\max |T_{\hat t\hat l}| \sim T_r^{-1},
\qquad
\max |B_{tt}/B| \sim T_r^{-2}.
```

But the source-history screen asks a different question: what does a support observer sample over the full setup/hold/reset history? At the core of the B-only model, the areal throat exists at every phase because `R_0(l)` is fixed. The unstretched state is not a standby state. It is the baseline throat.

For the B-only model, the core null-contracted support approximately behaves as

```math
T_{kk}(0,t) \approx -\frac{1}{4\pi B(0,t)^2}.
```

Therefore, longer B ramps reduce peak rate/flux but increase the duration of negative source history. This is why pure adiabaticity becomes the wrong objective after the source-history gate is activated.

## 2. Why R participation is consistent with the screening framework

The previously developed framework assigns the metric controls as follows:

```math
B(l,t) \rightarrow \text{radial proper-length and support-dilution control},
```

```math
R(l,t) \rightarrow \text{areal access geometry and flare shaping},
```

```math
N(l,t) \rightarrow \text{redshift, timing, matching, and horizon control}.
```

It also emphasizes that these assignments are hypotheses to be screened, not assumptions of success. The B-only test passed a dynamic cleanliness gate and then failed a source-history gate. That failure naturally redirects the design back to the role-allocation layer.

The important point is that this is not a reversal of the earlier claim that access-core `R(t)` breathing is dangerous. The dynamic throat gate contains

```math
\theta_\pm = \frac{2}{R}\left(\frac{R_t}{N}\pm\frac{R_l}{B}\right),
```

so strong `R_t` in the access core activates expansion, access-quietness, tidal-history, and dynamic-throat gates. The updated branch avoids using `R` as continuous access-core breathing. Instead, it uses `R` outside the traversal hold to decide whether the flare/access geometry is active.

The branch therefore matches the framework's expected sequence:

```math
B\text{-only geometry screen}
\rightarrow
\text{source-history failure}
\rightarrow
R\text{ participates in access/flare state}
\rightarrow
\text{new source-history screen}.
```

## 3. Updated design: flare-gated radial stretch

The tested family uses

```math
ds^2=-dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The B actuator is

```math
B(l,t)=1+(B_0-1)F_B(l)A_B(t),
\qquad
F_B(l)=\exp[-(|l|/w_B)^4].
```

The active access geometry is

```math
R_{\rm access}(l)=\sqrt{1+l^2}.
```

The standby geometry is

```math
R_{\rm standby}(l)
=
R_{\rm access}(l)
+
W_R(l)\left(R_c-R_{\rm access}(l)\right),
\qquad
W_R(l)=\exp[-(|l|/w_R)^4].
```

The best first target used `Rc=1`, so the core radius stays essentially fixed but the flare curvature is flattened in standby:

```math
R_{\rm standby}(0)=R_{\rm access}(0)=1,
\qquad
R'_\text{standby}(0)\approx 0,
\qquad
R''_\text{standby}(0)\approx 0.
```

During access, the flare is restored:

```math
R(l,t)=R_{\rm access}(l),
\qquad
R_t\approx 0,
\qquad
B_t\approx 0.
```

This means `R` is being used to turn the flare condition on/off rather than to pulse the throat radius.

## 4. Reduced source-history test

The branch test reconstructs effective source proxies from `G_{mu nu}/8pi` for the warped-product metric. It computes radial null contractions

```math
T_{kk}^{\pm}=T_{tt}+T_{ll}/B^2\pm2T_{tl}/B,
```

and uses the more negative branch

```math
T_{kk}^{\rm min}=\min(T_{kk}^{+},T_{kk}^{-}).
```

The main history score is the core negative exposure

```math
I^-_{\rm core}=\int[-T_{kk}^{\rm min}(l=0,t)]_+\,dt.
```

This is not a full quantum-inequality calculation. It is a source-history screen designed to catch whether a candidate has converted a peak-dynamics win into a long negative-exposure loss.

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

The old B-only result shows the adiabatic trade clearly: longer `Tr` reduces peak dynamic rates but greatly increases the full-cycle negative source history. The flare-gated branch breaks that coupling because the B setup/reset phases occur while the flare is off.

### 5.2 Phase ledger for the representative branch

For `B0=8, wB=8, wR=5, Rc=1, TB=100, TR=10, TH=60`:

| Phase | core negative exposure | comment |
|---|---:|---|
| B setup | 4.37e-7 | effectively zero throat-support debt while flare is flat |
| R open | 0.006043 | flare debt appears only as access geometry opens |
| hold | 0.074225 | remaining quiet-hold support burden |
| R close | 0.006198 | symmetric closure cost |
| B reset | 4.37e-7 | effectively zero after flare is closed |
| full cycle | 0.086777 | much lower than B-only at comparable B ramp cleanliness |

The hold remains the dominant cost after the old B-ramp debt is removed.

### 5.3 Order matters

For `B0=8, wB=8, TB=100, TR=30, TH=60`:

| Order | full-cycle core negative exposure | interpretation |
|---|---:|---|
| B first, then R open | 0.111570 | best tested ordering |
| simultaneous B,R with `TB=100, TR=30` | 1.725187 | R opens too early relative to B stretch |
| R first, then B | 6.188991 | worst; active flare exists while B is unstretched |

The design rule is therefore:

```math
\text{Stretch first while flare is off; open the flare only after B is already large.}
```

### 5.4 Stretch strength matters

For `wB=8, TB=100, TR=10, TH=60`:

| B0 | full-cycle core negative exposure | hold `Tkk(0)` |
|---:|---:|---:|
| 3 | 0.617076 | -0.008815 |
| 5 | 0.222148 | -0.003174 |
| 8 | 0.086777 | -0.001240 |

A larger B stretch lowers the restored-hold support burden. This is consistent with the long-throat branch: increasing proper radial stretch weakens local null-contracted support, but it does not remove the source-realism gate.

## 6. Interpretation

The best branch is not simply `B+R` in any order. It is specifically:

```math
\text{flare-gated radial stretch}:
\quad
R\text{ controls flare state, }B\text{ controls support dilution.}
```

The most important design insight is that `R` should not be treated primarily as a throat-radius pulse. The useful standby/access distinction comes from changing the flare curvature, not from making the core radius breathe. With `Rc=1`, the core radius is approximately fixed across standby and access. This keeps `R_t/R` small in the access core while allowing the flare condition to be absent during B setup/reset.

The branch also explains why the previous B-only protocol was incomplete rather than wrong. B-only was a good way to test radial support dilution under a fixed areal throat. The serious source-history screen then exposed that the areal throat itself had to become a controlled subsystem. That is exactly the framework's role-and-gate logic.

## 7. Remaining failure modes

This branch is still a prescribed-geometry engineering screen.

It does not yet solve:

1. **Quiet-hold source realism.** The restored hold still has negative `Tkk` at the support core.
2. **Quantum-inequality compatibility.** The score here is integrated negative exposure, not a full Fewster-Roman-style sampled bound.
3. **Backreaction and stability.** No source model has been evolved; no ringing, instability, or semiclassical feedback is included.
4. **Topology or boundary interpretation.** The standby profile is a reduced local geometry. A true off/no-throat state may require matching, capping, boundary, or topology assumptions beyond this coordinate patch.
5. **Shoulder stress and compensation.** The next design should include explicit shoulder/buffer/source-management terms and scan sampled observers outside the core.

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

The next objective should combine dynamic cleanliness with source-history sampling:

```math
J =
w_1\max|B_t/B|
+w_2\max|R_t/R|
+w_3\max|T_{\hat t\hat l}|
+w_4\int[-T_{kk}]_+dt
+w_5\max_{\tau_s,\tau_0}\int T_{kk}(\tau)g_{\tau_s,\tau_0}(\tau)d\tau
+w_6S_{\rm shoulder}.
```

The immediate design question is whether shoulder `R`, lapse `N`, or explicit source terms can add positive compensation without re-contaminating the access observer family.

## 9. Bottom-line conclusion

The results support moving from the old B-only adiabatic protocol to a coupled B,R design.

The new design should be named **flare-gated radial stretch**:

- `B` prestretches and dilutes the support burden.
- `R` gates the flare/access state by flattening/restoring flare curvature.
- The access hold keeps `B_t≈0` and `R_t≈0`.
- The branch sharply reduces full-cycle core negative exposure compared with B-only ramps.
- The branch remains upstream of source realism and must next add shoulder compensation and null-contracted sampled-stress tests.
