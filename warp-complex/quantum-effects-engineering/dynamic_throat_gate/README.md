# Dynamic Throat Gate Prototype

This bundle contains the Phase 3 dynamic-throat gate prototype for the wormhole-support engineering screening framework.

It evaluates a reduced spherically symmetric metric family,

```math
ds^2=-N(l,t)^2dt^2+B(l,t)^2dl^2+R(l,t)^2d\Omega^2,
```

through dynamic gates for null expansions, null-contracted stress, flux, extrinsic curvature/rate, access quietness, and transition-shoulder behavior.

Run:

```bash
python run_dynamic_throat_gate_eval.py
```

Outputs:

- `dynamic_gate_case_summary.csv`
- `dynamic_gate_extract_table.csv`
- `dynamic_gate_time_digest.csv`
- `dynamic_gate_summary.json`
- `dynamic_gate_memo.md`
- `manifest.json`

The calculations are reduced prescribed-geometry engineering diagnostics. They are intended for screening and framework development, not as semiclassical source models.
