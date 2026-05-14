#!/usr/bin/env python3
"""
Symbolic Einstein-tensor scaffold for the reduced active-rail metric.

Coordinates:
  tau   = service/evolution coordinate, formerly "s"
  ell   = radial rail/throat coordinate, formerly "l"
  th, ph = angular coordinates

Metric:
  dΣ² = -α(ell,tau)^2 dτ²
        + γ(ell,tau) (dell + β(ell,tau)dτ)^2
        + R2(ell,tau) dΩ²

where γ = γ_ell_ell and R2 = γ_ΩΩ.

This computes G_{μν} symbolically for generic α, β, γ, R2.
The full expressions are large; run individual components first.
"""

import sympy as sp
from pathlib import Path

tau, ell, th, ph = sp.symbols("tau ell th ph", real=True)
coords = (tau, ell, th, ph)
n = 4

alpha = sp.Function("alpha")(ell, tau)
beta = sp.Function("beta")(ell, tau)      # beta^ell
gamma = sp.Function("gamma")(ell, tau)    # gamma_ell_ell
R2 = sp.Function("R2")(ell, tau)          # gamma_OmegaOmega

# Metric matrix g_{μν}, order: (tau, ell, theta, phi)
g = sp.Matrix([
    [-alpha**2 + gamma*beta**2, gamma*beta, 0, 0],
    [gamma*beta,                gamma,      0, 0],
    [0,                         0,          R2, 0],
    [0,                         0,          0,  R2*sp.sin(th)**2],
])

g_inv = sp.simplify(g.inv())

def christoffel_symbols():
    Gamma = [[[
        sp.Rational(1, 2) * sum(
            g_inv[rho, sig] * (
                sp.diff(g[nu, sig], coords[mu])
                + sp.diff(g[mu, sig], coords[nu])
                - sp.diff(g[mu, nu], coords[sig])
            )
            for sig in range(n)
        )
        for nu in range(n)] for mu in range(n)] for rho in range(n)]
    return Gamma

def ricci_tensor(Gamma):
    Ric = sp.MutableDenseMatrix.zeros(n, n)
    for mu in range(n):
        for nu in range(n):
            expr = 0
            for rho in range(n):
                expr += sp.diff(Gamma[rho][mu][nu], coords[rho])
                expr -= sp.diff(Gamma[rho][mu][rho], coords[nu])
                for sig in range(n):
                    expr += Gamma[rho][mu][nu] * Gamma[sig][rho][sig]
                    expr -= Gamma[sig][mu][rho] * Gamma[rho][nu][sig]
            Ric[mu, nu] = sp.simplify(expr)
    return Ric

def einstein_tensor():
    Gamma = christoffel_symbols()
    Ric = ricci_tensor(Gamma)
    Rscalar = sp.simplify(sum(g_inv[mu, nu] * Ric[mu, nu] for mu in range(n) for nu in range(n)))
    G = sp.MutableDenseMatrix.zeros(n, n)
    for mu in range(n):
        for nu in range(n):
            G[mu, nu] = sp.simplify(Ric[mu, nu] - sp.Rational(1, 2) * g[mu, nu] * Rscalar)
    return sp.Matrix(G), Ric, Rscalar

if __name__ == "__main__":
    G, Ric, R = einstein_tensor()

    names = ["tau", "ell", "theta", "phi"]
    print("Metric g:")
    sp.printing.pprint(g)

    print("\nNonzero Einstein tensor components G_{μν}:")
    for i in range(n):
        for j in range(i, n):
            if G[i, j] != 0:
                print(f"\nG_{names[i]}{names[j]} =")
                sp.printing.pprint(G[i, j])

    # Optional: save all components to a text file.
    out = []
    for i in range(n):
        for j in range(i, n):
            out.append(f"G_{names[i]}{names[j]} = {sp.sstr(G[i,j])}\n")
    Path("active_rail_G_components.txt").write_text("\n".join(out), encoding="utf-8")
    print("\nWrote active_rail_G_components.txt")
