# Null-contracted long-throat B-stretch evaluation

This local scratch bundle tests whether the radial-metric stretch signal from the lapse/radial freedom sweep survives null-contracted diagnostics and transition-shoulder checks.

Metric family:

```math
ds^2=-dt^2+B(l)^2dl^2+R(l)^2d\Omega^2,\qquad R(l)=\sqrt{1+l^2}.
```

The sweep uses smooth B-stretch profiles:

```math
B(l)=1+(B_0-1)\exp[-(|l|/w_B)^p].
```

Files:

- `run_null_contracted_long_throat_eval.py`: generator script.
- `null_contracted_B_stretch_sweep.csv`: full parameter sweep.
- `null_contracted_profile_digest.csv`: representative profile samples.
- `null_contracted_result_extracts.json`: baseline, ranked candidates, and interpretation notes.
- `manifest.json`: checksums.

This is a reduced engineering diagnostic, not a rigorous semiclassical source construction.
