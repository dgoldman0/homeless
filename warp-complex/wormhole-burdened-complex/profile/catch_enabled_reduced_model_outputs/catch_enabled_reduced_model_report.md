# Catch-Enabled Reduced Transit / Rematching Evaluation

## Purpose

This pass tests the missing superluminal-exit piece found in the previous source-anatomy check.

The previous reduced model used a profile center `L(t)=Vt`. For `V>1`, that curve becomes spacelike after support fades. This new reduced evaluator separates the passenger center from the old profile label and adds a smooth catch/rematching phase before shift release.

This is still a prescribed reduced metric test. It is not a full 3+1 constraint solve or evolution.

## Catch-enabled ansatz

The passenger/coupling center is now:

```math
X(t)=v_{exit}t+(V-v_{exit})\int_0^t C(s)\,ds
```

with

```math
C(t)=\frac12\left[1-\tanh\left(\frac{t-t_c}{w_c}\right)\right],
```

so the passenger coordinate velocity is

```math
U(t)=\dot X(t)=v_{exit}+(V-v_{exit})C(t).
```

The metric keeps the throat-loaded gated structure, but the shift is tied to the caught velocity:

```math
A=\exp(q(X)W(l)\ln C_0),
```

```math
T=\exp(q(X)W(l)\ln(\lambda C_0)),
```

```math
\beta^l=-U(t)E(X)W(l)S_{pass}(l-X(t)).
```

The operational ordering is:

```math
L_{catch} < L_\beta < L_q.
```

In words:

1. catch/rematch the passenger speed while throat support is still high,
2. fade shift support,
3. relax throat capacity/lapse.

## Parameter sweep

The coarse worldline/source sweep covered 540 configurations:

- `V in {1.5, 2, 3, 5, 10}`
- `C0 in {100, 1e4}`
- `Delta in {0.3, 0.1}`
- `v_exit in {0.3, 0.5, 0.8}`
- `L_catch in {0.45, 0.65, 0.85}`
- `w_catch_L in {0.15, 0.25, 0.40}`

Default release positions were:

```math
L_\beta=1.10,\qquad L_q=1.45.
```

The lapse margin used in this catch pass was:

```math
\lambda=\max(1.05,1.20V).
```

## Main result

The catch/rematching architecture fixes the specific superluminal center-worldline failure, provided catch happens before the shift-release layer and before the passenger reaches the throat-support edge.

For the nominal early/mid catch case:

```text
C0=100, Delta=0.3, v_exit=0.5, L_catch=0.65, w_catch_L=0.25
```

the model stayed timelike through `V=10`.

| V | timelike failures | max worldline norm | max |v_rel| | max radial passenger tidal proxy | max negative NEC sum |
|---:|---:|---:|---:|---:|---:|
| 1.5 | 0 | -0.749878 | 0.501439 | 234.146 | 373.851 |
| 2.0 | 0 | -0.749999 | 0.500022 | 303.165 | 602.33 |
| 3.0 | 0 | -0.75 | 0.5 | 214.711 | 554.335 |
| 5.0 | 0 | -0.75 | 0.5 | 355.959 | 434.536 |
| 10.0 | 0 | -0.75 | 0.5 | 414.995 | 464.288 |


The important point is not that `V=10` is now physically safe. It is that the specific earlier failure mode—`L=Vt` becoming spacelike after release—can be removed by an explicit catch law.

## Early/mid catch robustness

Restricting to `L_catch=0.45` or `0.65`, no timelike failures occurred in the coarse sweep. Failures appeared when catch was pushed late to `L_catch=0.85`, near or beyond the support-wall edge for `Rth=0.75`.

| V | early/mid catch configs | all reduced checks clean | timelike fail configs | gtt fail configs | median radial tidal | worst radial tidal |
|---:|---:|---:|---:|---:|---:|---:|
| 1.5 | 72 | 65 | 0 | 0 | 241.118 | 2122.26 |
| 2.0 | 72 | 56 | 0 | 0 | 303.096 | 2655.17 |
| 3.0 | 72 | 62 | 0 | 0 | 306.132 | 1751.48 |
| 5.0 | 72 | 54 | 0 | 0 | 354.067 | 3201.04 |
| 10.0 | 72 | 51 | 0 | 0 | 437.416 | 3748.56 |


The `all reduced checks clean` flag used a conservative coarse screen:

- passenger worldline timelike,
- no positive `gtt`,
- passenger tidal proxies below `1e3`,
- source proxies below `5e3`.

Rows can fail this coarse comfort screen without becoming spacelike.

## Failure mode in the catch model

Late catch is the new failure mode.

When catch is delayed to the edge of the throat support, the passenger still has high coordinate speed while `W(l)` is falling. The shift no longer cancels the passenger velocity strongly enough, and the local relative speed can exceed one:

```math
v_{rel}=\frac{A(U+\beta)}{T}.
```

The condition for safety is:

```math
|v_{rel}|<1.
```

The numerical failures occur when late catch violates that. Once `|v_rel|` exceeds one, passenger-frame contractions become meaningless or blow up. This is why the worst late-catch rows show enormous tidal proxies.

The refined rule is:

```math
\boxed{\text{catch inside high-}W\text{ throat support, before shift release, before throat relaxation.}}
```

## Nominal grid check

For the nominal catch sequence, a small two-dimensional throat grid was evaluated for `V=2,5,10`.

| V | grid gtt-positive points | min lapse-shift margin | max theta product | mean throat burden share | min throat burden share | mean negative-NEC throat share |
|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0 | 1 | 2.79503 | 0.963659 | 0.88622 | 0.95602 |
| 5.0 | 0 | 1 | 2.26664 | 0.962094 | 0.886235 | 0.953286 |
| 10.0 | 0 | 1 | 1.86943 | 0.96175 | 0.886246 | 0.952032 |


This grid check is encouraging but not decisive. It shows that the catch-enabled model keeps the same causal-balance organization and keeps the burden mostly throat-localized in the tested nominal cases.

## Interpretation

The catch-enabled model changes the superluminal status from:

```text
profile-center superluminal path becomes spacelike after support fades
```

to:

```text
supported high-speed carry -> timelike catch -> subluminal release
```

So the previous early-break issue is not fatal to the architecture. It becomes a design constraint.

The corrected exit choreography is:

```math
\boxed{\text{catch passenger first, then fade shift, then relax throat.}}
```

## Caveats

This result does not prove physical buildability.

Remaining hard issues:

1. The source remains exotic: negative energy / NEC violation persists.
2. This is a prescribed reduced metric, not a solved 3+1 initial-data set.
3. The stress-energy source needed to enact catch dynamically has not been constructed.
4. The passenger-frame tidal values are still dimensionless; physical comfort requires a length-scale assignment.
5. `V=5` and `V=10` survive this reduced catch test only under disciplined timing. They should not be treated as physically validated speeds.

## Recommendation

Do not move directly to big 3+1 evolution yet.

The next cheap pass should refine the catch model with:

- denser time resolution near catch,
- varied `Rth` so late catch can be tested inside a larger high-support plateau,
- proper-time integration along the passenger curve,
- stricter passenger-frame tidal and source exposure integrals,
- comparison against subluminal `V=0.9` and mild superluminal `V=1.5`.

If that holds, then proceed to constraint-quality 3+1 initial-data construction.
