#!/usr/bin/env python3
"""
Source-ledger diagnostic for the throat-supported active rail.

This is a first-principles numerical Einstein-tensor diagnostic for the reduced
ADM metric used in active_rail_paper/code/obstruction_screen.py. It is intended
to live beside obstruction_screen.py and regenerate data/source_ledger_*.json/csv.

Scope and caveats
-----------------
* Computes a demanded classical source T_{mu nu} = G_{mu nu}/(8 pi) in G=c=1
  units for the specified metric closure.
* This is a diagnostic ledger, not a constraint solve, not a matter model, and
  not a renormalized/semi-classical stress tensor calculation.
* The reduced paper metric leaves gamma_{Omega Omega} as an architectural
  degree of freedom. This script makes that angular closure explicit via
  --angular-closure and writes it into metadata. Do not compare absolute source
  magnitudes across papers/runs without reporting that closure.
* Numerical curvature is finite-difference based. Use the convergence probe
  before trusting sharp-layer extrema.

Default geometry
----------------
The radial ADM sector follows the active-rail obstruction screen:

    ds^2 = -alpha^2 ds^2 + gamma_ll (dl + beta^l ds)^2
           + gamma_OmegaOmega dOmega^2.

The default angular closure is a static Morris-Thorne-style area radius,

    gamma_OmegaOmega = l^2 + Rth^2.

Additional closures are deliberately labeled exploratory.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import csv
import json
import math
from typing import Dict, Iterable, List, Tuple

import numpy as np

PI8 = 8.0 * math.pi
THETA0 = math.pi / 2.0


@dataclass(frozen=True)
class Params:
    V: float = 10.0
    v_exit: float = 0.5
    C0: float = 100.0
    lam: float = 6.0
    B0: float = 8.0
    eta_N: float = 1.0
    Rth: float = 1.25
    Rpass: float = 0.35
    p_beta: float = 1.0
    x_catch: float = 0.15
    x_beta: float = 0.70
    x_q: float = 1.25
    w_catch: float = 0.16
    w_beta: float = 0.18
    w_q: float = 0.18
    w_th: float = 0.12
    w_pass: float = 0.06
    eps: float = 1e-5


@dataclass(frozen=True)
class Variant:
    name: str
    throat_gated_shift: bool
    catch_enabled: bool
    late_catch: bool = False
    p_beta: float = 1.0


VARIANTS = [
    Variant("active_rail_catch_throat_gated", True, True, False, 4.0),
    Variant("naive_independent_no_catch", False, False, False, 1.0),
    Variant("naive_throat_gated_no_catch", True, False, False, 1.0),
    Variant("late_catch_throat_gated", True, True, True, 4.0),
    Variant("catch_independent_shift", False, True, False, 1.0),
]
VARIANT_BY_NAME = {v.name: v for v in VARIANTS}


def falloff(z: np.ndarray | float, w: float) -> np.ndarray | float:
    return 0.5 * (1.0 - np.tanh(np.asarray(z) / w))


def bump_sq(x2: np.ndarray | float, R: float, w: float) -> np.ndarray | float:
    z = (np.asarray(x2) - R * R) / (2.0 * R * w)
    return 0.5 * (1.0 - np.tanh(z))


def make_params(width_factor: float = 1.0, variant: Variant | None = None) -> Params:
    p = Params()
    x_catch = p.x_catch
    if variant and variant.late_catch:
        x_catch = p.x_q
    p_beta = variant.p_beta if variant else p.p_beta
    return Params(
        V=p.V,
        v_exit=p.v_exit,
        C0=p.C0,
        lam=p.lam,
        B0=p.B0,
        eta_N=p.eta_N,
        Rth=p.Rth,
        Rpass=p.Rpass,
        p_beta=p_beta,
        x_catch=x_catch,
        x_beta=p.x_beta,
        x_q=p.x_q,
        w_catch=max(1e-4, p.w_catch * width_factor),
        w_beta=max(1e-4, p.w_beta * width_factor),
        w_q=max(1e-4, p.w_q * width_factor),
        w_th=max(1e-4, p.w_th * width_factor),
        w_pass=max(1e-4, p.w_pass * width_factor),
        eps=p.eps,
    )


def scalars(s: float, l: float, p: Params, v: Variant) -> Dict[str, float]:
    s_arr = np.asarray(s, dtype=float)
    l_arr = np.asarray(l, dtype=float)
    if v.catch_enabled:
        C = falloff(s_arr - p.x_catch, p.w_catch)
        U = p.v_exit + (p.V - p.v_exit) * C
    else:
        U = np.full_like(s_arr + l_arr, p.V, dtype=float)
    E = falloff(s_arr - p.x_beta, p.w_beta)
    q = falloff(s_arr - p.x_q, p.w_q)
    W = bump_sq(l_arr * l_arr, p.Rth, p.w_th)
    S = bump_sq((l_arr - s_arr) * (l_arr - s_arr) + p.eps * p.eps, p.Rpass, p.w_pass)
    A = np.exp(q * W * math.log(p.C0))
    T = np.exp(q * W * math.log(p.lam * p.C0))
    B = 1.0 + (p.B0 - 1.0) * W * q
    shoulder = np.exp(-((np.abs(l_arr) - 1.05) / 0.35) ** 2)
    N = np.exp(p.eta_N * 0.18 * q * shoulder)
    Wpower = W ** p.p_beta if v.throat_gated_shift else 1.0
    beta = -U * E * Wpower * S / B
    alpha = N * T
    sqrt_gamma = B * A
    gamma_ll = sqrt_gamma * sqrt_gamma
    vcoord = U / B
    gtt = -alpha * alpha + gamma_ll * beta * beta
    packet_norm = -alpha * alpha + gamma_ll * (vcoord + beta) ** 2
    return {
        "U": float(U),
        "E": float(E),
        "q": float(q),
        "W": float(W),
        "S": float(S),
        "A": float(A),
        "T": float(T),
        "B": float(B),
        "N": float(N),
        "beta": float(beta),
        "alpha": float(alpha),
        "sqrt_gamma": float(sqrt_gamma),
        "gamma_ll": float(gamma_ll),
        "vcoord": float(vcoord),
        "gtt": float(gtt),
        "packet_norm": float(packet_norm),
    }


def gamma_omega(s: float, l: float, p: Params, v: Variant, closure: str) -> float:
    base = l * l + p.Rth * p.Rth
    if closure == "static_throat":
        return base
    sc = scalars(s, l, p, v)
    if closure == "area_capacity_A2":
        return base * sc["A"] ** 2
    if closure == "area_capacity_B2":
        return base * sc["B"] ** 2
    raise ValueError(f"unknown angular closure: {closure}")


def metric_at(x: np.ndarray, p: Params, v: Variant, closure: str) -> np.ndarray:
    s, l, theta, _phi = [float(z) for z in x]
    sc = scalars(s, l, p, v)
    alpha = sc["alpha"]
    beta = sc["beta"]
    gamma_ll = sc["gamma_ll"]
    goo = gamma_omega(s, l, p, v, closure)
    sin2 = math.sin(theta) ** 2
    g = np.zeros((4, 4), dtype=float)
    g[0, 0] = -alpha * alpha + gamma_ll * beta * beta
    g[0, 1] = g[1, 0] = gamma_ll * beta
    g[1, 1] = gamma_ll
    g[2, 2] = goo
    g[3, 3] = goo * sin2
    return g


def metric_derivative(x: np.ndarray, coord: int, h: np.ndarray, p: Params, v: Variant, closure: str) -> np.ndarray:
    if coord == 3:  # axisymmetric/no phi dependence
        return np.zeros((4, 4), dtype=float)
    xp = x.copy(); xm = x.copy()
    xp[coord] += h[coord]
    xm[coord] -= h[coord]
    return (metric_at(xp, p, v, closure) - metric_at(xm, p, v, closure)) / (2.0 * h[coord])


def christoffel_at(x: np.ndarray, h: np.ndarray, p: Params, v: Variant, closure: str) -> np.ndarray:
    g = metric_at(x, p, v, closure)
    invg = np.linalg.inv(g)
    dg = [metric_derivative(x, a, h, p, v, closure) for a in range(4)]
    Gamma = np.zeros((4, 4, 4), dtype=float)
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                total = 0.0
                for sig in range(4):
                    total += invg[rho, sig] * (dg[mu][nu, sig] + dg[nu][mu, sig] - dg[sig][mu, nu])
                Gamma[rho, mu, nu] = 0.5 * total
    return Gamma


def christoffel_derivative(x: np.ndarray, coord: int, h: np.ndarray, p: Params, v: Variant, closure: str) -> np.ndarray:
    if coord == 3:
        return np.zeros((4, 4, 4), dtype=float)
    xp = x.copy(); xm = x.copy()
    xp[coord] += h[coord]
    xm[coord] -= h[coord]
    return (christoffel_at(xp, h, p, v, closure) - christoffel_at(xm, h, p, v, closure)) / (2.0 * h[coord])


def einstein_tensor_at(s: float, l: float, p: Params, v: Variant, closure: str, h_s: float, h_l: float) -> Tuple[np.ndarray, Dict[str, float]]:
    x = np.array([s, l, THETA0, 0.0], dtype=float)
    h = np.array([h_s, h_l, 1e-4, 1.0], dtype=float)
    g = metric_at(x, p, v, closure)
    invg = np.linalg.inv(g)
    Gamma = christoffel_at(x, h, p, v, closure)
    dGamma = [christoffel_derivative(x, a, h, p, v, closure) for a in range(4)]

    Ric = np.zeros((4, 4), dtype=float)
    # R_{mu nu} = d_rho Gamma^rho_{mu nu} - d_nu Gamma^rho_{mu rho}
    #              + Gamma^rho_{mu nu} Gamma^sigma_{rho sigma}
    #              - Gamma^sigma_{mu rho} Gamma^rho_{nu sigma}
    for mu in range(4):
        for nu in range(4):
            term1 = sum(dGamma[rho][rho, mu, nu] for rho in range(4))
            term2 = sum(dGamma[nu][rho, mu, rho] for rho in range(4))
            term3 = 0.0
            term4 = 0.0
            for rho in range(4):
                trace = sum(Gamma[sig, rho, sig] for sig in range(4))
                term3 += Gamma[rho, mu, nu] * trace
                for sig in range(4):
                    term4 += Gamma[sig, mu, rho] * Gamma[rho, nu, sig]
            Ric[mu, nu] = term1 - term2 + term3 - term4
    R = float(np.einsum("ab,ab->", invg, Ric))
    G = Ric - 0.5 * g * R
    diagnostics = {"ricci_scalar": R, "cond_metric": float(np.linalg.cond(g))}
    return G, diagnostics


def projections(s: float, l: float, G: np.ndarray, p: Params, v: Variant) -> Dict[str, float]:
    sc = scalars(s, l, p, v)
    alpha = sc["alpha"]
    beta = sc["beta"]
    gamma_ll = sc["gamma_ll"]
    sqrt_gamma_ll = math.sqrt(gamma_ll)
    T = G / PI8

    # Eulerian normal n^mu = (1/alpha, -beta/alpha, 0, 0).
    n = np.array([1.0 / alpha, -beta / alpha, 0.0, 0.0], dtype=float)
    e_l_unit = np.array([0.0, 1.0 / sqrt_gamma_ll, 0.0, 0.0], dtype=float)
    rho = float(n @ T @ n)
    j_l_unit = float(-e_l_unit @ T @ n)
    p_l = float(e_l_unit @ T @ e_l_unit)

    # Angular unit vector at theta=pi/2. Closure-specific gamma_oo is not needed here;
    # the caller will provide T_theta_theta; approximate unit p_omega with metric value.
    # Use a direct spherical angular unit channel from local gamma_omega.
    # The caller could compare theta and phi channels; at theta=pi/2 they coincide.
    # p_omega is filled by caller region_sample with closure.

    # Packet-comoving vector from obstruction_screen convention: (1, vcoord, 0, 0)
    # normalized when timelike.
    u_raw = np.array([1.0, sc["vcoord"], 0.0, 0.0], dtype=float)
    # Norm is metric contraction; equals packet_norm from scalars.
    norm = sc["packet_norm"]
    if norm < 0.0:
        u_pkt = u_raw / math.sqrt(-norm)
        rho_pkt = float(u_pkt @ T @ u_pkt)
    else:
        rho_pkt = float("nan")

    # Radial null channels. dl/ds = -beta +/- alpha/sqrt(gamma_ll); k^mu=(1, dl/ds,0,0).
    k_plus = np.array([1.0, -beta + alpha / sqrt_gamma_ll, 0.0, 0.0], dtype=float)
    k_minus = np.array([1.0, -beta - alpha / sqrt_gamma_ll, 0.0, 0.0], dtype=float)
    Tkk_plus = float(k_plus @ T @ k_plus)
    Tkk_minus = float(k_minus @ T @ k_minus)

    return {
        "rho_euler": rho,
        "j_l_unit": j_l_unit,
        "p_l_unit": p_l,
        "rho_packet": rho_pkt,
        "Tkk_plus": Tkk_plus,
        "Tkk_minus": Tkk_minus,
        "packet_norm": norm,
        "gtt": sc["gtt"],
        "W": sc["W"],
        "S": sc["S"],
        "q": sc["q"],
        "E": sc["E"],
        "U": sc["U"],
    }


def region_name(s: float, l: float, p: Params) -> str:
    # Ordered to expose overlaps involving the packet first.
    if abs(l - s) <= p.Rpass:
        if abs(l) <= p.Rth:
            return "packet_in_support"
        return "packet_outer"
    if abs(l) <= 0.65 * p.Rth:
        return "core_throat"
    if 0.65 * p.Rth < abs(l) <= 1.20 * p.Rth:
        return "support_edge"
    if 1.20 * p.Rth < abs(l) <= 1.85 * p.Rth:
        return "outer_shoulder"
    return "exterior_tail"


def phase_name(s: float, p: Params) -> str:
    # Windows keyed to transition centers and widths.
    if s < p.x_catch - 2.0 * p.w_catch:
        return "pre_catch_support"
    if abs(s - p.x_catch) <= 2.0 * p.w_catch:
        return "catch_rematch"
    if p.x_catch + 2.0 * p.w_catch < s < p.x_beta - 2.0 * p.w_beta:
        return "held_transport"
    if abs(s - p.x_beta) <= 2.0 * p.w_beta:
        return "shift_fade"
    if p.x_beta + 2.0 * p.w_beta < s < p.x_q - 2.0 * p.w_q:
        return "post_shift_pre_relax"
    if abs(s - p.x_q) <= 2.0 * p.w_q:
        return "throat_relax"
    return "reset_tail"


def summarize_values(rows: List[Dict[str, float]]) -> Dict[str, float]:
    def finite_values(key: str) -> np.ndarray:
        vals = [float(r[key]) for r in rows if key in r and math.isfinite(float(r[key]))]
        return np.array(vals, dtype=float) if vals else np.array([], dtype=float)

    out: Dict[str, float] = {"points": float(len(rows))}
    keys = [
        "rho_euler", "j_l_unit", "p_l_unit", "p_omega_unit", "rho_packet",
        "Tkk_plus", "Tkk_minus", "ricci_scalar", "cond_metric",
    ]
    for key in keys:
        vals = finite_values(key)
        if vals.size == 0:
            out[f"{key}_min"] = float("nan")
            out[f"{key}_max"] = float("nan")
            out[f"{key}_mean"] = float("nan")
            out[f"{key}_max_abs"] = float("nan")
        else:
            out[f"{key}_min"] = float(np.min(vals))
            out[f"{key}_max"] = float(np.max(vals))
            out[f"{key}_mean"] = float(np.mean(vals))
            out[f"{key}_max_abs"] = float(np.max(np.abs(vals)))
    # Negative-volume-ish measures as point sums. Real volume weighting can be added once closure is fixed.
    for key in ["rho_euler", "rho_packet", "Tkk_plus", "Tkk_minus"]:
        vals = finite_values(key)
        out[f"{key}_negative_point_sum"] = float(np.sum(np.minimum(vals, 0.0))) if vals.size else float("nan")
    return out


def run_source_ledger(
    variant_name: str,
    width_factor: float,
    angular_closure: str,
    ns: int,
    nl: int,
    s_min: float,
    s_max: float,
    l_min: float,
    l_max: float,
    h_s: float,
    h_l: float,
) -> Dict[str, object]:
    if variant_name not in VARIANT_BY_NAME:
        raise ValueError(f"unknown variant {variant_name!r}; choose from {sorted(VARIANT_BY_NAME)}")
    variant = VARIANT_BY_NAME[variant_name]
    p = make_params(width_factor, variant)
    s_grid = np.linspace(s_min, s_max, ns)
    l_grid = np.linspace(l_min, l_max, nl)

    point_rows: List[Dict[str, float | str]] = []
    failures: List[Dict[str, float | str]] = []
    for s in s_grid:
        for l in l_grid:
            try:
                G, diag = einstein_tensor_at(float(s), float(l), p, variant, angular_closure, h_s, h_l)
                proj = projections(float(s), float(l), G, p, variant)
                goo = gamma_omega(float(s), float(l), p, variant, angular_closure)
                T = G / PI8
                p_omega = float(T[2, 2] / goo)
                row: Dict[str, float | str] = {
                    "s": float(s),
                    "l": float(l),
                    "phase": phase_name(float(s), p),
                    "region": region_name(float(s), float(l), p),
                    "p_omega_unit": p_omega,
                    **proj,
                    **diag,
                }
                point_rows.append(row)
            except Exception as exc:  # keep long runs inspectable
                failures.append({"s": float(s), "l": float(l), "error": repr(exc)})

    grouped: Dict[Tuple[str, str], List[Dict[str, float]]] = {}
    for r in point_rows:
        grouped.setdefault((str(r["phase"]), str(r["region"])), []).append(r)  # type: ignore[arg-type]
    summaries: List[Dict[str, float | str]] = []
    for (phase, region), rows in sorted(grouped.items()):
        summaries.append({"phase": phase, "region": region, **summarize_values(rows)})

    metadata = {
        "description": "Demanded classical source ledger for reduced active-rail metric.",
        "scope": "Numerical Einstein tensor diagnostic; not a constraint-quality solve, matter model, or RSET calculation.",
        "units": "G=c=1; T_munu = G_munu/(8*pi)",
        "variant": variant_name,
        "width_factor": width_factor,
        "angular_closure": angular_closure,
        "angular_closure_definitions": {
            "static_throat": "gamma_OmegaOmega = l^2 + Rth^2",
            "area_capacity_A2": "gamma_OmegaOmega = (l^2 + Rth^2) * A(s,l)^2 [exploratory]",
            "area_capacity_B2": "gamma_OmegaOmega = (l^2 + Rth^2) * B(s,l)^2 [exploratory]",
        },
        "grid": {"ns": ns, "nl": nl, "s_min": s_min, "s_max": s_max, "l_min": l_min, "l_max": l_max},
        "finite_difference_steps": {"h_s": h_s, "h_l": h_l, "h_theta": 1e-4},
        "params": asdict(p),
        "variant_definition": asdict(variant),
        "num_points": len(point_rows),
        "num_failures": len(failures),
    }
    return {"metadata": metadata, "summary": summaries, "points": point_rows, "failures": failures}


def write_outputs(result: Dict[str, object], outdir: Path, prefix: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    json_path = outdir / f"{prefix}.json"
    json_path.write_text(json.dumps(result, indent=2, allow_nan=True), encoding="utf-8")

    summary_path = outdir / f"{prefix}_summary.csv"
    summaries = result["summary"]  # type: ignore[index]
    if summaries:
        keys = list(summaries[0].keys())  # type: ignore[index]
        with summary_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for row in summaries:  # type: ignore[union-attr]
                w.writerow(row)

    points_path = outdir / f"{prefix}_points.csv"
    points = result["points"]  # type: ignore[index]
    if points:
        keys = list(points[0].keys())  # type: ignore[index]
        with points_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for row in points:  # type: ignore[union-attr]
                w.writerow(row)


def convergence_probe(args: argparse.Namespace, multipliers: Iterable[float]) -> List[Dict[str, object]]:
    rows = []
    for m in multipliers:
        result = run_source_ledger(
            args.variant, args.width_factor, args.angular_closure,
            max(9, args.ns // 2), max(11, args.nl // 2),
            args.s_min, args.s_max, args.l_min, args.l_max,
            args.h_s * m, args.h_l * m,
        )
        # Collapse global worst-channel summary.
        all_points = result["points"]  # type: ignore[index]
        vals = {k: [] for k in ["rho_euler", "j_l_unit", "p_l_unit", "p_omega_unit", "rho_packet", "Tkk_plus", "Tkk_minus"]}
        for r in all_points:  # type: ignore[union-attr]
            for k in vals:
                z = float(r.get(k, float("nan")))  # type: ignore[union-attr]
                if math.isfinite(z):
                    vals[k].append(z)
        row = {"step_multiplier": m, "num_points": len(all_points)}
        for k, vlist in vals.items():
            arr = np.array(vlist, dtype=float)
            row[f"{k}_max_abs"] = float(np.max(np.abs(arr))) if arr.size else float("nan")
            row[f"{k}_min"] = float(np.min(arr)) if arr.size else float("nan")
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", default="active_rail_catch_throat_gated", choices=sorted(VARIANT_BY_NAME))
    parser.add_argument("--width-factor", type=float, default=1.0)
    parser.add_argument("--angular-closure", default="static_throat", choices=["static_throat", "area_capacity_A2", "area_capacity_B2"])
    parser.add_argument("--ns", type=int, default=41)
    parser.add_argument("--nl", type=int, default=61)
    parser.add_argument("--s-min", type=float, default=-0.35)
    parser.add_argument("--s-max", type=float, default=1.65)
    parser.add_argument("--l-min", type=float, default=-1.85)
    parser.add_argument("--l-max", type=float, default=2.05)
    parser.add_argument("--h-s", type=float, default=2.5e-3)
    parser.add_argument("--h-l", type=float, default=2.5e-3)
    parser.add_argument("--outdir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    parser.add_argument("--prefix", default="source_ledger")
    parser.add_argument("--probe", action="store_true", help="Also run a small derivative-step convergence probe.")
    args = parser.parse_args()

    result = run_source_ledger(
        args.variant, args.width_factor, args.angular_closure,
        args.ns, args.nl, args.s_min, args.s_max, args.l_min, args.l_max,
        args.h_s, args.h_l,
    )
    prefix = f"{args.prefix}_{args.variant}_w{args.width_factor:g}_{args.angular_closure}"
    write_outputs(result, args.outdir, prefix)

    if args.probe:
        probe_rows = convergence_probe(args, multipliers=[2.0, 1.0, 0.5])
        probe_path = args.outdir / f"{prefix}_convergence_probe.csv"
        with probe_path.open("w", newline="", encoding="utf-8") as f:
            keys = list(probe_rows[0].keys())
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for row in probe_rows:
                w.writerow(row)

    print(json.dumps({
        "ok": True,
        "points": result["metadata"]["num_points"],  # type: ignore[index]
        "failures": result["metadata"]["num_failures"],  # type: ignore[index]
        "outdir": str(args.outdir),
        "prefix": prefix,
        "warning": "Report angular_closure and convergence probe with any numerical interpretation.",
    }, indent=2))


if __name__ == "__main__":
    main()
