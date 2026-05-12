# Stage 2 Dynamic Throat QI Poke

## Purpose

This pass tested the next distinct idea after the static-throat QI failure: let the throat itself be dynamic. The model does not try to make a static Morris--Thorne throat with a pulsed approximation to a static source. Instead it lets the areal-radius function breathe,

```math
ds^2=-dt^2+dl^2+R(l,t)^2d\Omega^2,
\qquad
R(l,t)=\sqrt{a(t)^2+l^2}.
```

The throat radius is `a(t)`. I evaluated the effective source from

```math
T_{\mu\nu}^{\rm eff}=G_{\mu\nu}/(8\pi)
```

at the throat, sampled the energy density with Lorentzian QI windows, and tracked throat kinematics through the radial NEC projections, expansion product, and angular tidal component.

## Tested dynamic envelopes

The run used three simple families.

```math
a(t)=a_0
```

for the static reference.

```math
a(t)=a_0\left(1+\epsilon\cos\Omega t\right)
```

for smooth breathing throats.

```math
a(t)=a_{\rm closed}+(a_{\rm open}-a_{\rm closed})
\frac{1}{2}\left[
\tanh\frac{t+w/2}{s}-\tanh\frac{t-w/2}{s}
\right]
```

for single open-gate pulses.

The QI proxy used

```math
\int \rho(\tau)\frac{\tau_0/\pi}{(\tau-\tau_c)^2+\tau_0^2}\,d\tau
\geq
-\frac{3}{32\pi^2\tau_0^4}.
```

The reported scale `L0max_planck_units` is the largest physical scale, in Planck units per dimensionless model unit, compatible with the most restrictive sampled negative-energy average in this proxy.

## Main result

The dynamic throat can make the local energy density oscillatory and can create positive-energy phases. That is the constructive part of the idea. The problem moves into the control burden: the cases that improve the QI scale do it by making the throat violently dynamic. They produce large radial NEC violation, large expansion-product pulses, large angular tidal terms, and very small quasi-static open fractions.

The best-looking QI-scale cases in this limited sweep are:

| case              |   min_a |    max_a |    min_rho |       max_rho |    mean_rho |      min_Gkp |   max_abs_tidal_angular |   max_abs_theta_product |   max_abs_adot_over_a |   fraction_quasistatic_open |   strict_log10_L0max |
|:------------------|--------:|---------:|-----------:|--------------:|------------:|-------------:|------------------------:|------------------------:|----------------------:|----------------------------:|---------------------:|
| sin_eps0.1_om20   |    0.9  | 1.1      | -0.0491219 |     0.120268  |  0.0397499  |     -91.358  |                 44.4444 |            16.1616      |               2.00996 |                  0.0174913  |             3.84019  |
| pulse_ac0.5_w0.02 |    0.5  | 0.999955 | -0.159155  |  1105.17      |  3.00145    | -143207      |              71601.2    |        111111           |             154.039   |                  0.00149925 |             2.52708  |
| sin_eps0.6_om5    |    0.4  | 1.6      | -0.24868   |     0.468096  |  0.170874   |     -87.5    |                 37.5    |            56.2494      |               3.74976 |                  0.0174913  |             2.48263  |
| pulse_ac0.5_w0.1  |    0.5  | 0.999955 | -0.159155  |    46.7049    |  0.479282   |   -6410.84   |               3202.63   |          4703.44        |              34.1902  |                  0.0154923  |             1.50964  |
| sin_eps0.3_om5    |    0.7  | 1.3      | -0.0812015 |     0.0523531 |  0.00218187 |     -25.5102 |                 10.7143 |             9.89001     |               1.57233 |                  0.0274863  |             1.35311  |
| pulse_ac0.1_w0.02 |    0.1  | 0.999918 | -3.97887   | 10648.3       | 28.4554     | -694425      |             347189      |             1.07051e+06 |             500.98    |                  0.00049975 |             1.12203  |
| pulse_ac0.1_w0.1  |    0.1  | 0.999918 | -3.97887   |   428.727     |  2.75594    |  -27821.7    |              13887.6    |         43142.4         |             103.806   |                  0.0124938  |             0.204111 |
| sin_eps0.05_om20  |    0.95 | 1.05     | -0.0440872 |     0         | -0.0200147  |     -44.3213 |                 21.0526 |             4.01002     |               1.00119 |                  0.0644678  |            -0.161743 |

The static reference has `log10(L0max) ~= -0.311`, which is Planck order. Some high-frequency or sharp-pulse cases reach `log10(L0max)` of order 2--4 in the dimensionless proxy, but they do so by creating extreme throat motion and source spikes rather than a stable operating envelope.

## Interpretation

The dynamic envelope does not rescue a macroscopic static throat. It shows a different failure trade:

```math
\text{better sampled energy bookkeeping}
\quad\Longleftrightarrow\quad
\text{violent breathing, NEC pulses, tidal pulses, and tiny usable windows}.
```

The most favorable sinusoidal case in this sweep, `sin_eps0.1_om20`, improves the QI scale to about

```math
L_0 \sim 10^{3.84} L_P
```

per dimensionless unit, while producing a minimum radial null projection around `Gkk = -91`, angular tidal proxy around `44`, and a maximum fractional throat-rate `|\dot a/a|` around `2`. That is a dynamic source plant, not a calm traversable throat.

The sharp open-pulse cases create positive-energy repayment phases naturally, but the repayment shows up as very large source and tidal spikes. Example: `pulse_ac0.5_w0.02` reaches a better QI scale but produces `max_rho ~ 1.1e3`, `min_Gkk ~ -1.4e5`, and angular tidal proxy near `7.2e4`.

## Physical open-window estimate

A useful analytic estimate comes directly from the static throat density at the open radius,

```math
\rho_0=-\frac{1}{8\pi r_0^2}.
```

If an open window lasts for a proper duration comparable to `T`, the local QI proxy gives roughly

```math
T_{\rm max}\sim (8\pi C_{QI})^{1/4}\sqrt{r_0},
\qquad
C_{QI}=\frac{3}{32\pi^2},
```

in Planck units. For macroscopic throats this is much shorter than the light-crossing time:

|   throat_radius_m |   r0_planck |   QI_open_duration_est_s |   light_crossing_time_s |   ratio_Tmax_to_light_crossing |
|------------------:|------------:|-------------------------:|------------------------:|-------------------------------:|
|             1e-15 | 6.18714e+19 |              2.96423e-34 |             3.33564e-24 |                    8.88654e-11 |
|             1e-12 | 6.18714e+22 |              9.37372e-33 |             3.33564e-21 |                    2.81017e-12 |
|             1e-09 | 6.18714e+25 |              2.96423e-31 |             3.33564e-18 |                    8.88654e-14 |
|             1e-06 | 6.18714e+28 |              9.37372e-30 |             3.33564e-15 |                    2.81017e-15 |
|             0.001 | 6.18714e+31 |              2.96423e-28 |             3.33564e-12 |                    8.88654e-17 |
|             1     | 6.18714e+34 |              9.37372e-27 |             3.33564e-09 |                    2.81017e-18 |
|          1000     | 6.18714e+37 |              2.96423e-25 |             3.33564e-06 |                    8.88654e-20 |
|             1e+09 | 6.18714e+43 |              2.96423e-22 |             3.33564     |                    8.88654e-23 |

That estimate explains why dynamic gating is so constrained. A one-meter throat can only remain in a simple negative-energy open state for about `1e-26 s` in this crude proxy, while the light-crossing time is about `3e-9 s`.

## Stage 2 verdict

The dynamic-throat idea is not empty. It produces the right qualitative ingredients: positive repayment phases, short negative-energy episodes, and time-dependent support. The present reduced test says those ingredients are purchased through violent throat dynamics. The available quiet, quasi-static traversable window remains far too small for macroscopic passage under this proxy.

The result does not justify adding the transport/catch layer yet. The throat plant still needs a plausible dynamic operating envelope before passenger access becomes the limiting problem.

## Files

- `dynamic_throat_case_summary.csv`: all tested cases and key diagnostics.
- `timeseries_*.csv`: selected throat time histories.
- `qi_samples_*.csv`: selected Lorentzian sampled-energy records.
- `analytic_open_window_estimates.csv`: physical open-window estimates.
