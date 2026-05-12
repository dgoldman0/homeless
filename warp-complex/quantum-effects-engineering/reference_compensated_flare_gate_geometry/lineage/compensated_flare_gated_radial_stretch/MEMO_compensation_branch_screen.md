# Compensation Branch Screen for Flare-Gated Radial Stretch

## Design question

The flare-gated radial-stretch branch now has a clear operating sequence:

```math
B	ext{-setup} ightarrow R	ext{-open} ightarrow 	ext{quiet hold} ightarrow R	ext{-close} ightarrow 	ext{compensation} ightarrow B	ext{-reset}.
```

This screen asks which mechanism can carry positive compensation after the access interval while preserving the access observer family during the quiet hold.

The tested compensation mechanisms are:

1. shoulder-only areal-radius motion, `shoulder_R`;
2. lapse modulation, `lapse_N_ring` and `lapse_N_core`;
3. explicit positive source overlays, `explicit_source_ring` and `explicit_source_core`.

## Base geometry

The geometry screen uses

```math
ds^2=-N(l,t)^2dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2.
```

The base branch uses `B0=8`, `wB=8`, `wR=5`, `TR=10`, `TH=60`, and `TB=100`. The compensation window has default duration `TC=30`. During compensation, `R` is in its flattened standby profile and the access interval has ended.

The source proxy is reconstructed from `G_{mu nu}/8pi`. Explicit source overlays are added as separate ledger terms to both radial null directions, so they advance to a later physical source and backreaction gate.

## Ledger result

The base open interval carries the following negative null exposure:

| Observer region | Open-interval negative exposure |
|---|---:|
| core/access | 0.092664 |
| support | 0.103717 |
| shoulder | 0.068615 |

The compensation mechanisms produce distinct ledger roles.

### Shoulder R: buffer and transition compensation

Shoulder-only `R` motion creates positive geometric source history in the shoulder band while preserving the access core. The strongest tested shoulder case, `shoulder_R_amp_-0.25`, supplies shoulder positive exposure of `0.033902`, about `49.4%` of the shoulder open-interval negative exposure. Its access-core compensation-window flux remains at `5.84e-7`, with access-core `|R_t/R|` around `5.96e-6`.

This assigns shoulder `R` to transition shaping, shoulder buffering, and partial shoulder-ledger compensation.

### Lapse N: timing and matching co-control

Lapse modulation supplies timing and matching structure. Ring lapse preserves access isolation. In this geometry-only scan, lapse pulses supply small positive shoulder ledger contributions compared with explicit source terms. The useful role is scheduling, redshift/matching control, and co-control of a physical source term.

### Explicit source terms: repayment ledger carrier

The explicit post-closure source overlay supplies the clearest positive compensation ledger.

For `explicit_source_core_amp_0.008` with `TC=30`:

| Observer region | Open negative | Compensation positive | Ratio |
|---|---:|---:|---:|
| core/access location | 0.092664 | 0.119999 | 1.295 |
| support | 0.103717 | 0.119999 | 1.157 |

The access interval remains quiet because the positive pulse is scheduled after `R_close`. The spatial access core receives repayment during the closed-access compensation phase, which makes this a support/source ledger mechanism rather than an access-use exposure.

For `explicit_source_ring_amp_0.008`, the shoulder ledger receives positive exposure of `0.110675`, about `161%` of the shoulder open-interval negative exposure, while the core/support repayment ledger remains assigned to a core/support source term.

## Architecture update

The preferred compensated branch is:

```math
B	ext{-prestretch}
+R	ext{-flare gate}
+	ext{post-closure explicit source compensation}
+	ext{shoulder }R/N	ext{ shaping}.
```

The actuator allocation becomes:

| Actuator | Positive role |
|---|---|
| `B(l,t)` | radial support dilution and setup/reset smoothing |
| `R(l,t)` | flare access-state gate plus shoulder transition/buffer shaping |
| `N(l,t)` | timing, redshift, matching, and source co-control |
| explicit source term | repayment ledger carrier after access closure |

## Design implication

The branch now has a concrete next-stage target: use explicit post-closure source compensation for the core/support repayment ledger, use shoulder `R` for shoulder-buffer shaping, and use lapse `N` to schedule and match the compensation phase.

The next gates are quantum-interest timing, candidate state construction, semiclassical backreaction, stability, and repeated-cycle accumulation.
