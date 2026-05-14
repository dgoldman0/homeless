# Method note: controlled angular source test

This diagnostic freezes the active-rail service geometry and varies only the angular closure.

## Frozen sector

The following are not varied in this test:

- support-contained shift profile,
- catch timing,
- shift fade timing,
- throat relaxation timing,
- packet trajectory,
- radial ADM sector.

## Varied sector

The angular sector is promoted from a static throat closure to a soft jacket:

\[
\gamma_{\Omega\Omega} = (l^2 + R_{\rm th}^2) C_\Omega(s,l)^2.
\]

The tested jacket is:

\[
C_\Omega = \exp(a_\Omega Q_\Omega(s)W_\Omega(l)).
\]

## Einstein tensor reduction

For the spherically symmetric warped-product metric,

\[
ds^2 = h_{ab}dx^a dx^b + r(s,l)^2d\Omega^2,
\]

with \(a,b\in\{s,l\}\), the script computes the two-dimensional base Christoffels, base scalar curvature, Hessian of the angular radius, and the warped-product Einstein tensor.

The demanded source is then

\[
T_{\mu\nu}=G_{\mu\nu}/(8\pi).
\]

## Limitations

This is not a matter model, not a constraint solve, and not a semiclassical calculation. It is a demanded-source diagnostic for a prescribed metric family.

Finite differences are used. The CSV convergence probe should be inspected before treating numerical magnitudes as stable.
