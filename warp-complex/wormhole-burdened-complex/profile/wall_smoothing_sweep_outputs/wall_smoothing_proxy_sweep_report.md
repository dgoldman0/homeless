# Targeted Throat-Wall Smoothing Sweep

## Scope and status

This is a targeted throat-wall smoothing pass over the current worst and representative outgoing passenger-path cases. The full curvature-grid implementation timed out in this environment, so this run isolates the throat-wall mechanism with a calibrated reduced wall-gradient tidal proxy. It uses the actual baseline tidal worldline values from the prior run for calibration, then estimates the effect of widening only the throat support wall. Exact causal balance along the prescribed worldlines is still evaluated from the reduced metric scalars.

This result should be read as a fast design sweep, not as a replacement for the later full curvature/tetrad rerun. It is useful because the prior full tidal pass already localized the peak to the throat support flank, and this sweep directly varies that flank.

- Unique selected cases: 23
- Selection: ten worst previous tidal cases plus representative shift-first cases across velocity, capacity, and wall settings, with synchronized and rapid-shift-first mode checks.
- Wall width multipliers: 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0
- Total rows: 184
- Passenger offsets: -0.15, 0.00, +0.15

## Main result

The smoothing knob is important. The estimated passenger-path tidal proxy drops quickly as the throat wall is widened. The main improvement occurs by about the 3x to 4x range. Beyond that, the peak continues to fall, but compactness weakens because more of the wall-gradient support lives outside the original throat service region.

Exact worldline causal balance stayed clean in this proxy sweep: no selected row produced positive `gtt` points along the prescribed passenger paths, and the lapse-shift margin remained positive.

## Multiplier summary

| throat wall multiplier | worst tidal estimate | median tidal estimate | median reduction | worst exact max gtt | worst exact margin | min compactness share | worst outside W tail |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 3304.10 | 2928.97 | 0.0% | -1 | 1 | 1.0000 | 0.0000 |
| 1.5 | 1474.90 | 1309.78 | 55.4% | -1 | 1 | 0.9997 | 0.0002 |
| 2.0 | 829.44 | 734.91 | 74.9% | -1 | 1 | 0.9972 | 0.0016 |
| 2.5 | 531.75 | 471.97 | 83.9% | -1 | 1 | 0.9901 | 0.0057 |
| 3.0 | 369.18 | 327.80 | 88.8% | -1 | 1 | 0.9769 | 0.0133 |
| 4.0 | 208.25 | 184.78 | 93.7% | -1 | 1 | 0.9353 | 0.0381 |
| 5.0 | 133.59 | 118.53 | 95.9% | -1 | 1 | 0.8833 | 0.0702 |
| 6.0 | 93.04 | 82.59 | 97.2% | -1 | 1 | 0.8311 | 0.1041 |

## Interpretation

The sweep supports the earlier diagnosis: the worst passenger-path peaks are throat-wall crossings. Widening the throat support wall lowers the relevant gradient scale, so the passenger path crosses a gentler transition.

The result also exposes the engineering trade. Smoothing improves passenger tidal behavior, while very aggressive smoothing spreads the active support flank outside the compact throat service region. The design target should not be the widest possible wall. The useful band is the smallest smoothing that brings passenger tidal exposure down while keeping the support burden compact and serviceable.

In this reduced proxy pass, the 3x to 4x range is the strongest next candidate band. It gives a large estimated tidal reduction while preserving a compact enough support-wall density share for targeted full-curvature retesting.

## Design consequence

The next architecture rule is now clearer. Release ordering protects causal balance. Throat-wall smoothing protects passenger comfort. These are separate controls and should remain independently tunable.

## Next full run

The next full diagnostic should not rescan the whole original family. It should retest the selected cases near the 3x to 4x throat-wall band with the full curvature evaluator, higher sampling near the wall flank, and a passenger-frame tidal tensor.

## Generated files

- `wall_smoothing_proxy_sweep_all_rows.csv`
- `wall_smoothing_proxy_sweep_multiplier_summary.csv`
- `wall_smoothing_proxy_sweep_best_by_case.csv`
- `wall_smoothing_proxy_sweep_top_worst_by_multiplier.csv`
- `wall_smoothing_proxy_highres_worst_history.csv`
- `proxy_tidal_vs_wall_smoothing.png`
- `proxy_compactness_vs_wall_smoothing.png`
- `proxy_highres_worst_case_histories.png`
