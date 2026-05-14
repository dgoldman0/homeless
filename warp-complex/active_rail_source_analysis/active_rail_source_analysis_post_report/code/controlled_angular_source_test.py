#!/usr/bin/env python3
"""
Controlled angular source test for the active-rail geometry.

Status:
  Diagnostic source-ledger computation, not a refrozen design, not a matter
  model, not a constraint solve, and not a semiclassical RSET calculation.

It freezes the reduced active-rail ADM sector and compares:
  1. static angular closure
  2. soft angular jacket candidate

It computes the demanded source:
  T_mu_nu = G_mu_nu / (8*pi)
in geometrized units on a 2D spherical warped-product reduction.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import math
import numpy as np
import pandas as pd

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


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
    p_beta: float = 4.0
    x_catch: float = 0.15
    x_beta: float = 0.70
    x_q: float = 1.25
    w_catch: float = 0.16
    w_beta: float = 0.18
    w_q: float = 0.18
    w_th: float = 0.12
    w_pass: float = 0.06
    eps: float = 1e-5


def falloff(z, w):
    return 0.5 * (1.0 - np.tanh(np.asarray(z) / w))


def bump_sq(x2, R, w):
    z = (np.asarray(x2) - R * R) / (2.0 * R * w)
    return 0.5 * (1.0 - np.tanh(z))


def scalars(s, l, p: Params):
    s_arr = np.asarray(s, dtype=float)
    l_arr = np.asarray(l, dtype=float)
    C = falloff(s_arr - p.x_catch, p.w_catch)
    U = p.v_exit + (p.V - p.v_exit) * C
    E = falloff(s_arr - p.x_beta, p.w_beta)
    q = falloff(s_arr - p.x_q, p.w_q)
    W = bump_sq(l_arr * l_arr, p.Rth, p.w_th)
    S = bump_sq((l_arr - s_arr) * (l_arr - s_arr) + p.eps * p.eps, p.Rpass, p.w_pass)
    A = np.exp(q * W * math.log(p.C0))
    T = np.exp(q * W * math.log(p.lam * p.C0))
    B = 1.0 + (p.B0 - 1.0) * W * q
    shoulder = np.exp(-((np.abs(l_arr) - 1.05) / 0.35) ** 2)
    N = np.exp(p.eta_N * 0.18 * q * shoulder)
    beta = -U * E * (W ** p.p_beta) * S / B
    alpha = N * T
    sqrt_gamma = B * A
    gamma_ll = sqrt_gamma * sqrt_gamma
    vcoord = U / B
    gtt = -alpha * alpha + gamma_ll * beta * beta
    packet_norm = -alpha * alpha + gamma_ll * (vcoord + beta) ** 2
    plus = -beta + alpha / sqrt_gamma
    minus = -beta - alpha / sqrt_gamma
    return dict(U=U, E=E, q=q, W=W, S=S, A=A, T=T, B=B, N=N,
                beta=beta, alpha=alpha, sqrt_gamma=sqrt_gamma, gamma_ll=gamma_ll,
                vcoord=vcoord, gtt=gtt, packet_norm=packet_norm,
                plus_speed=plus, minus_speed=minus)


def angular_radius(s, l, p: Params, closure: str, pars: dict | None = None):
    r0 = np.sqrt(l * l + p.Rth * p.Rth)
    if closure == "static":
        return r0
    pars = pars or {}
    a = float(pars.get("a", 0.35))
    R = float(pars.get("R", p.Rth))
    w = float(pars.get("w", 0.70))
    x = float(pars.get("x", 2.00))
    wt = float(pars.get("wt", 0.60))
    Wom = bump_sq(l * l, R, w)
    Q = falloff(s - x, wt)
    return r0 * np.exp(a * Q * Wom)


def derivs(F, ds, dl):
    Fs, Fl = np.gradient(F, ds, dl, edge_order=2)
    Fss, Fsl = np.gradient(Fs, ds, dl, edge_order=2)
    Fls, Fll = np.gradient(Fl, ds, dl, edge_order=2)
    return Fs, Fl, Fss, 0.5 * (Fsl + Fls), Fll


def compute_ledger(ns=251, nl=375, closure="static", pars=None,
                   smin=-0.45, smax=3.25, lmin=-2.8, lmax=2.8):
    p = Params()
    s = np.linspace(smin, smax, ns)
    l = np.linspace(lmin, lmax, nl)
    ds = s[1] - s[0]
    dl = l[1] - l[0]
    Sg, Lg = np.meshgrid(s, l, indexing="ij")
    sc = scalars(Sg, Lg, p)

    alpha = sc["alpha"]
    beta = sc["beta"]
    gamma = sc["gamma_ll"]
    h00 = -alpha**2 + gamma * beta**2
    h01 = gamma * beta
    h11 = gamma
    det = h00 * h11 - h01 * h01
    inv00 = h11 / det
    inv01 = -h01 / det
    inv11 = h00 / det

    h00s, h00l, *_ = derivs(h00, ds, dl)
    h01s, h01l, *_ = derivs(h01, ds, dl)
    h11s, h11l, *_ = derivs(h11, ds, dl)
    dh = {
        (0, 0, 0): h00s, (1, 0, 0): h00l,
        (0, 0, 1): h01s, (1, 0, 1): h01l,
        (0, 1, 0): h01s, (1, 1, 0): h01l,
        (0, 1, 1): h11s, (1, 1, 1): h11l,
    }
    hinv = [[inv00, inv01], [inv01, inv11]]

    Gamma = [[[None for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for a in range(2):
        for b in range(2):
            for c in range(2):
                val = 0.0
                for d in range(2):
                    val += hinv[a][d] * (dh[(b, d, c)] + dh[(c, d, b)] - dh[(d, b, c)])
                Gamma[a][b][c] = 0.5 * val

    dGamma = {}
    for a in range(2):
        for b in range(2):
            for c in range(2):
                gs, gl = np.gradient(Gamma[a][b][c], ds, dl, edge_order=2)
                dGamma[(0, a, b, c)] = gs
                dGamma[(1, a, b, c)] = gl

    Ric = [[None] * 2 for _ in range(2)]
    for a in range(2):
        for b in range(2):
            val = 0.0
            for c in range(2):
                val += dGamma[(c, c, a, b)]
                val -= dGamma[(b, c, a, c)]
                trace = 0.0
                for d in range(2):
                    trace += Gamma[d][c][d]
                val += Gamma[c][a][b] * trace
                for d in range(2):
                    val -= Gamma[d][a][c] * Gamma[c][b][d]
            Ric[a][b] = val
    Rh = inv00 * Ric[0][0] + 2.0 * inv01 * Ric[0][1] + inv11 * Ric[1][1]

    r = angular_radius(Sg, Lg, p, closure, pars)
    rs, rl, rss, rsl, rll = derivs(r, ds, dl)
    grad = [rs, rl]
    d2r = {(0, 0): rss, (0, 1): rsl, (1, 0): rsl, (1, 1): rll}
    Hess = [[None] * 2 for _ in range(2)]
    for a in range(2):
        for b in range(2):
            val = d2r[(a, b)]
            for c in range(2):
                val -= Gamma[c][a][b] * grad[c]
            Hess[a][b] = val

    box = inv00 * Hess[0][0] + 2.0 * inv01 * Hess[0][1] + inv11 * Hess[1][1]
    grad2 = inv00 * rs * rs + 2.0 * inv01 * rs * rl + inv11 * rl * rl

    G00 = -2.0 / r * Hess[0][0] + 2.0 * h00 * box / r - h00 * (1.0 - grad2) / (r * r)
    G01 = -2.0 / r * Hess[0][1] + 2.0 * h01 * box / r - h01 * (1.0 - grad2) / (r * r)
    G11 = -2.0 / r * Hess[1][1] + 2.0 * h11 * box / r - h11 * (1.0 - grad2) / (r * r)
    Gthth = r * box - 0.5 * r * r * Rh

    fac = 1.0 / (8.0 * math.pi)
    T00, T01, T11, Tth = fac * G00, fac * G01, fac * G11, fac * Gthth

    n0 = 1.0 / alpha
    n1 = -beta / alpha
    rho = T00 * n0 * n0 + 2.0 * T01 * n0 * n1 + T11 * n1 * n1
    jl = -(T01 * n0 + T11 * n1)
    p_l = T11 / gamma
    p_om = Tth / (r * r)

    v = sc["vcoord"]
    norm = sc["packet_norm"]
    safe_norm = np.where(norm < 0.0, np.sqrt(-norm), np.nan)
    u0 = 1.0 / safe_norm
    u1 = v / safe_norm
    rho_pkt = T00 * u0 * u0 + 2.0 * T01 * u0 * u1 + T11 * u1 * u1

    gtt = sc["gtt"]
    rho_stat = np.where(gtt < 0.0, T00 / (-gtt), np.nan)
    vp = sc["plus_speed"]
    vm = sc["minus_speed"]
    Tkkp = T00 + 2.0 * vp * T01 + vp * vp * T11
    Tkkm = T00 + 2.0 * vm * T01 + vm * vm * T11
    Tkkmin = np.minimum(Tkkp, Tkkm)

    interior = np.zeros_like(Sg, dtype=bool)
    interior[3:-3, 3:-3] = True
    W = sc["W"]
    packet = np.abs(Lg - Sg) <= p.Rpass

    masks = {
        "core_throat": (W > 0.85),
        "support_edge": (W > 0.08) & (W < 0.85),
        "packet_in_support": packet & (W > 0.05),
        "packet_outer": packet & (W <= 0.05),
        "outer_shoulder": ((np.abs(np.abs(Lg) - 1.05) < 0.35) & (W < 0.5)),
        "whole_interior": np.ones_like(Sg, dtype=bool),
    }
    phases = {
        "pre_catch": (Sg >= -0.35) & (Sg < 0.00),
        "catch": (Sg >= 0.00) & (Sg < 0.35),
        "hold": (Sg >= 0.35) & (Sg < 0.60),
        "shift_fade": (Sg >= 0.60) & (Sg < 0.95),
        "throat_relax": (Sg >= 1.05) & (Sg < 1.50),
        "angular_reset": (Sg >= 1.60) & (Sg < 2.40),
        "late_tail": (Sg >= 2.40) & (Sg <= 3.15),
    }
    fields = {
        "rho": rho,
        "j_abs": np.abs(jl),
        "p_l_abs": np.abs(p_l),
        "p_om_abs": np.abs(p_om),
        "rho_pkt": rho_pkt,
        "rho_stat": rho_stat,
        "Tkk_plus": Tkkp,
        "Tkk_minus": Tkkm,
        "Tkk_min": Tkkmin,
        "packet_norm": sc["packet_norm"],
        "gtt": sc["gtt"],
    }

    rows = []
    for rn, rm in masks.items():
        for phn, pm in phases.items():
            m = rm & pm & interior
            if not np.any(m):
                continue
            row = dict(closure=closure, region=rn, phase=phn, count=int(np.sum(m)))
            for name, F in fields.items():
                vals = F[m]
                vals = vals[np.isfinite(vals)]
                if vals.size:
                    if name.endswith("_abs"):
                        row[f"max_{name}"] = float(np.nanmax(vals))
                    else:
                        row[f"min_{name}"] = float(np.nanmin(vals))
                        row[f"max_{name}"] = float(np.nanmax(vals))
            rows.append(row)

    service = ((Sg >= -0.35) & (Sg < 2.40) & interior)
    service_edge = masks["support_edge"] & service
    pkt_support = masks["packet_in_support"] & service
    packet_service = packet & service
    late_edge = masks["support_edge"] & phases["late_tail"] & interior
    reset_edge = masks["support_edge"] & phases["angular_reset"] & interior

    metrics = {
        "closure": closure,
        "pars": pars or {},
        "ns": ns,
        "nl": nl,
        "max_packet_norm_on_packet": float(np.nanmax(sc["packet_norm"][packet_service])),
        "positive_packet_points": int(np.sum((sc["packet_norm"] > 0.0) & packet_service)),
        "max_gtt_support_edge": float(np.nanmax(sc["gtt"][service_edge])),
        "positive_gtt_support_edge_points": int(np.sum((sc["gtt"] > 0.0) & service_edge)),
        "worst_service_edge_Tkk": float(np.nanmin(Tkkmin[service_edge])),
        "worst_packet_support_Tkk": float(np.nanmin(Tkkmin[pkt_support])),
        "worst_packet_support_rho_pkt": float(np.nanmin(rho_pkt[pkt_support])),
        "worst_rho_overall": float(np.nanmin(rho[service])),
        "max_j_abs_overall": float(np.nanmax(np.abs(jl)[service])),
        "max_p_l_abs_overall": float(np.nanmax(np.abs(p_l)[service])),
        "max_p_om_abs_overall": float(np.nanmax(np.abs(p_om)[service])),
        "late_tail_edge_Tkk": float(np.nanmin(Tkkmin[late_edge])),
        "late_tail_edge_max_p_om": float(np.nanmax(np.abs(p_om)[late_edge])),
        "angular_reset_edge_Tkk": float(np.nanmin(Tkkmin[reset_edge])),
    }
    return {"metrics": metrics, "rows": rows}


def flatten_metrics(rows):
    flat = []
    for r in rows:
        d = dict(r)
        pars = d.pop("pars", {}) or {}
        for k, v in pars.items():
            d[f"par_{k}"] = v
        flat.append(d)
    return pd.DataFrame(flat)


def add_score(df):
    df["score"] = (
        1.5 * (-df["worst_service_edge_Tkk"])
        + 2.0 * (-df["worst_packet_support_Tkk"])
        + 2.0 * np.maximum(0.0, -df["worst_packet_support_rho_pkt"])
        + 0.5 * df["max_j_abs_overall"]
        + 0.3 * df["max_p_l_abs_overall"]
        + 0.15 * df["max_p_om_abs_overall"]
        + 1.0 * (-df["late_tail_edge_Tkk"])
    )
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="source_ledger_test_output")
    ap.add_argument("--ns", type=int, default=251)
    ap.add_argument("--nl", type=int, default=375)
    args = ap.parse_args()

    out = Path(args.outdir)
    (out / "data").mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(parents=True, exist_ok=True)

    cand = {"a": 0.35, "R": 1.25, "w": 0.70, "x": 2.00, "wt": 0.60}
    static = compute_ledger(args.ns, args.nl, "static", {})
    soft = compute_ledger(args.ns, args.nl, "soft_jacket", cand)

    metrics = flatten_metrics([
        {"label": "static_angular_closure", **static["metrics"]},
        {"label": "soft_angular_jacket_candidate", **soft["metrics"]},
    ])
    metrics.to_csv(out / "data" / "high_resolution_baseline_vs_candidate_metrics.csv", index=False)

    rows = pd.DataFrame(static["rows"] + soft["rows"])
    rows["label"] = rows["closure"].map({
        "static": "static_angular_closure",
        "soft_jacket": "soft_angular_jacket_candidate",
    })
    rows.to_csv(out / "data" / "region_phase_ledger_high_resolution.csv", index=False)

    conv_rows = []
    for ns, nl in [(101, 151), (151, 225), (201, 301), (251, 375)]:
        for label, closure, pars in [
            ("static_angular_closure", "static", {}),
            ("soft_angular_jacket_candidate", "soft_jacket", cand),
        ]:
            r = compute_ledger(ns, nl, closure, pars)
            conv_rows.append({"label": label, **r["metrics"]})
    conv = flatten_metrics(conv_rows)
    conv.to_csv(out / "data" / "grid_convergence_baseline_vs_candidate.csv", index=False)

    sens_rows = []
    for x in [1.70, 1.85, 2.00, 2.20, 2.40, 2.60]:
        for wt in [0.40, 0.60, 0.80, 1.00]:
            pars = {"a": 0.35, "R": 1.25, "w": 0.70, "x": x, "wt": wt}
            r = compute_ledger(151, 225, "soft_jacket", pars)
            sens_rows.append({"xOmega": x, "wtOmega": wt, **r["metrics"]})
    sens = add_score(flatten_metrics(sens_rows))
    sens.to_csv(out / "data" / "reset_taper_sensitivity.csv", index=False)

    summary = {
        "status": "diagnostic; do not refreeze yet",
        "candidate": {
            "name": "soft angular jacket",
            "parameters": cand,
        },
        "high_resolution": {
            "static": static["metrics"],
            "soft_jacket": soft["metrics"],
        },
        "finding": (
            "The soft jacket substantially improves null-channel, packet-support, "
            "Eulerian density, radial current, and radial pressure diagnostics, but "
            "leaves the angular-pressure ceiling essentially unresolved and carries "
            "a smaller late-tail reset debt."
        ),
    }
    (out / "data" / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    if plt is not None:
        metric_names = [
            "worst_service_edge_Tkk", "worst_packet_support_Tkk",
            "worst_packet_support_rho_pkt", "worst_rho_overall",
            "max_j_abs_overall", "max_p_l_abs_overall", "max_p_om_abs_overall",
        ]
        display = ["edge -Tkk", "packet -Tkk", "packet -rho_pkt", "-rho overall",
                   "max |j|", "max |p_l|", "max |p_Omega|"]
        base_vals = [abs(static["metrics"][m]) for m in metric_names]
        cand_vals = [abs(soft["metrics"][m]) for m in metric_names]
        fig, ax = plt.subplots(figsize=(9, 5))
        x = np.arange(len(metric_names))
        width = 0.35
        ax.bar(x - width / 2, base_vals, width, label="static")
        ax.bar(x + width / 2, cand_vals, width, label="soft jacket")
        ax.set_xticks(x)
        ax.set_xticklabels(display, rotation=35, ha="right")
        ax.set_ylabel("Magnitude")
        ax.set_title("Baseline vs soft angular jacket")
        ax.legend()
        fig.tight_layout()
        fig.savefig(out / "figures" / "baseline_vs_soft_jacket_metrics.png", dpi=180)
        plt.close(fig)

    print(json.dumps({"outdir": str(out), "metrics_csv": str(out / "data" / "high_resolution_baseline_vs_candidate_metrics.csv")}, indent=2))


if __name__ == "__main__":
    main()
