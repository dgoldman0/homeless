# Method and Limitations

## Method

The diagnostic script in `code/source_freeze_diagnostic.py` computes an effective Einstein-source ledger for a spherically symmetric warped-product metric of the reduced active-rail form:

```math
ds^2 =
h_{ab}(s,l)dx^a dx^b + R(s,l)^2 d\Omega^2,
```

where the 2D base metric is the ADM radial sector:

```math
h_{ss}=-\alpha^2+\gamma_{ll}\beta^2,
\quad
h_{sl}=\gamma_{ll}\beta,
\quad
h_{ll}=\gamma_{ll}.
```

The script uses warped-product formulas to compute the 4D Einstein tensor:

```math
T_{\mu\nu}^{demand}=G_{\mu\nu}/8\pi.
```

It then projects onto diagnostic channels:

- Eulerian energy density,
- radial momentum/current,
- radial pressure proxy,
- angular pressure,
- radial null contractions,
- packet-frame density,
- packet norm,
- support-edge g_tt.

## Important limitations

This is a prescribed-geometry diagnostic. It does not construct physical matter fields.

Finite differences are used, so extrema should be treated as diagnostic and compared structurally rather than as exact continuum values.

The calculation is radial/spherical. Off-axis global causal behavior remains untested.

The angular sector is a closure/design family, not a derived physical matter solution.

The report's freeze is a reduced-design freeze, not a final physical feasibility claim.
