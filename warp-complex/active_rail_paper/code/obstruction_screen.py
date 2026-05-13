#!/usr/bin/env python3
"""
Reduced obstruction and radial-null-bundle screen for a throat-supported shift rail.

This script intentionally stands alone. It does not import prior repository code or
prior generated JSON. It confirms the qualitative claims used in the paper by
recomputing the reduced ADM metric, packet norm, radial null speeds, and ray-bundle
compression for several variants:

  - active rail: catch-rematched, throat-gated shift
  - naive independent no-catch: passenger-attached shift without catch/rematch
  - naive throat-gated no-catch: support-contained shift without catch/rematch
  - late-catch throat-gated: support-contained shift with wrong catch timing

The model is a reduced diagnostic screen, not a constraint-quality initial-data
solve and not a semiclassical stress-tensor calculation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import math
from typing import Callable, Dict, List, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - plotting optional
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


def falloff(z: np.ndarray | float, w: float) -> np.ndarray | float:
    return 0.5 * (1.0 - np.tanh(np.asarray(z) / w))


def bump_sq(x2: np.ndarray | float, R: float, w: float) -> np.ndarray | float:
    z = (np.asarray(x2) - R * R) / (2.0 * R * w)
    return 0.5 * (1.0 - np.tanh(z))


def make_params(width_factor: float = 1.0, variant: Variant | None = None) -> Params:
    p = Params()
    x_catch = p.x_catch
    if variant and variant.late_catch:
        # Deliberately delay catch until throat relaxation begins.
        x_catch = p.x_q
    if variant:
        p_beta = variant.p_beta
    else:
        p_beta = p.p_beta
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


def scalars(s: np.ndarray | float, l: np.ndarray | float, p: Params, v: Variant) -> Dict[str, np.ndarray]:
    s_arr = np.asarray(s, dtype=float)
    l_arr = np.asarray(l, dtype=float)
    if v.catch_enabled:
        C = falloff(s_arr - p.x_catch, p.w_catch)
        U = p.v_exit + (p.V - p.v_exit) * C
    else:
        # Naive branch: the transport object reaches the throat without a catch/rematch stage.
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
    plus = -beta + alpha / sqrt_gamma
    minus = -beta - alpha / sqrt_gamma
    return {
        "U": U,
        "E": E,
        "q": q,
        "W": W,
        "S": S,
        "A": A,
        "T": T,
        "B": B,
        "N": N,
        "beta": beta,
        "alpha": alpha,
        "sqrt_gamma": sqrt_gamma,
        "gtt": gtt,
        "packet_norm": packet_norm,
        "plus_speed": plus,
        "minus_speed": minus,
    }



def speeds(branch: str, s: float, rays: np.ndarray, p: Params, v: Variant) -> np.ndarray:
    key = "plus_speed" if branch == "plus" else "minus_speed"
    return np.asarray(scalars(s, rays, p, v)[key], dtype=float)


def trace_bundle(branch: str, p: Params, v: Variant, s0: float, l0s: np.ndarray,
                 s1: float = 2.6, h: float = 0.01) -> Dict[str, object]:
    """Vectorized midpoint integration for a radial null bundle."""
    n = int(math.ceil((s1 - s0) / h))
    h = (s1 - s0) / n
    rays = np.array(l0s, dtype=float)
    min_abs_speed = float("inf")
    zero_samples = 0
    total_samples = 0
    min_width = float(np.max(rays) - np.min(rays))
    start_width = min_width
    folds = 0
    for i in range(n):
        s = s0 + i * h
        k1 = speeds(branch, s, rays, p, v)
        mid = rays + 0.5 * h * k1
        k2 = speeds(branch, s + 0.5 * h, mid, p, v)
        min_abs_speed = min(min_abs_speed, float(np.min(np.abs(k1))), float(np.min(np.abs(k2))))
        zero_samples += int(np.sum(np.abs(k1) < 1e-3)) + int(np.sum(np.abs(k2) < 1e-3))
        total_samples += int(k1.size + k2.size)
        rays = rays + h * k2
        width = float(np.max(rays) - np.min(rays))
        min_width = min(min_width, width)
        if np.any(np.diff(rays) <= 0):
            folds += 1
    compression = min_width / start_width if start_width > 0 else float("nan")
    return {
        "branch": branch,
        "s0": s0,
        "s1": s1,
        "start_l_min": float(np.min(l0s)),
        "start_l_max": float(np.max(l0s)),
        "final_l_min": float(np.min(rays)),
        "final_l_max": float(np.max(rays)),
        "min_abs_speed": min_abs_speed,
        "near_zero_fraction": zero_samples / total_samples if total_samples else 0.0,
        "min_bundle_width_ratio": compression,
        "fold_steps": folds,
        "cleared_exterior": bool(np.min(np.abs(rays)) > p.Rth),
    }

def dense_local_scan(p: Params, v: Variant) -> Dict[str, float]:
    ss = np.linspace(-0.35, 1.65, 161)
    ls = np.linspace(-1.85, 2.05, 221)
    Sg, Lg = np.meshgrid(ss, ls, indexing="ij")
    sc = scalars(Sg, Lg, p, v)
    packet = np.abs(Lg - Sg) <= p.Rpass
    edge = (sc["S"] > 0.08) & (sc["W"] > 0.05) & (sc["W"] < 0.85)
    packet_support_overlap = packet & (sc["W"] > 0.05)
    return {
        "packet_norm_positive_points": int(np.sum((sc["packet_norm"] > 0) & packet)),
        "edge_gtt_positive_points": int(np.sum((sc["gtt"] > 0) & edge)),
        "packet_max_norm": float(np.max(np.where(packet, sc["packet_norm"], -np.inf))),
        "edge_max_gtt": float(np.max(np.where(edge, sc["gtt"], -np.inf))),
        "min_abs_plus_overlap": float(np.min(np.abs(np.where(packet_support_overlap, sc["plus_speed"], np.inf)))),
        "min_abs_minus_overlap": float(np.min(np.abs(np.where(packet_support_overlap, sc["minus_speed"], np.inf)))),
    }


def bundle_initial_conditions(p: Params) -> List[Tuple[str, float, float]]:
    # (label, launch time, launch center). The l positions are local centers for bundles.
    return [
        ("leading_packet_edge_plus_support_edge", p.Rth - p.Rpass, p.Rth),
        ("trailing_packet_edge_plus_support_edge", p.Rth + p.Rpass, p.Rth),
        ("support_edge_shift_fade", p.x_beta, p.Rth),
        ("support_edge_throat_relax", p.x_q, p.Rth),
        ("negative_support_edge_shift_fade", p.x_beta, -p.Rth),
        ("negative_support_edge_throat_relax", p.x_q, -p.Rth),
    ]


def run(outdir: Path) -> Dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    all_rows: List[Dict[str, object]] = []
    width_factors = [1.0, 0.5, 0.25]
    for vf in width_factors:
        for variant in VARIANTS:
            p = make_params(vf, variant)
            local = dense_local_scan(p, variant)
            bundle_results = []
            for label, s0, lc in bundle_initial_conditions(p):
                span = 0.035
                l0s = np.linspace(lc - span, lc + span, 17)
                for branch in ("plus", "minus"):
                    br = trace_bundle(branch, p, variant, s0, l0s, s1=2.6, h=0.006)
                    br["bundle_label"] = label
                    bundle_results.append(br)
            row = {
                "variant": variant.name,
                "width_factor": vf,
                "params": asdict(p),
                "local_scan": local,
                "bundles": bundle_results,
                "worst_min_abs_speed": min(b["min_abs_speed"] for b in bundle_results),
                "worst_compression_ratio": min(b["min_bundle_width_ratio"] for b in bundle_results),
                "any_bundle_fold": any(b["fold_steps"] > 0 for b in bundle_results),
                "max_near_zero_fraction": max(b["near_zero_fraction"] for b in bundle_results),
            }
            all_rows.append(row)

    summary = {
        "description": "Reduced obstruction screen for throat-supported active-rail transit.",
        "scope": "Radial ADM null-characteristic and packet/support-edge bundle screen; not a constraint solve or RSET calculation.",
        "rows": all_rows,
    }
    (outdir / "obstruction_screen_results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Compact markdown table for the report.
    md_lines = [
        "# Obstruction screen compact results",
        "",
        "| variant | width | packet norm positive points | edge gtt positive points | packet max norm | edge max gtt | min abs speed | worst compression | fold? |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in all_rows:
        loc = row["local_scan"]
        md_lines.append(
            f"| {row['variant']} | {row['width_factor']:.3g} | "
            f"{loc['packet_norm_positive_points']} | {loc['edge_gtt_positive_points']} | "
            f"{loc['packet_max_norm']:.4g} | {loc['edge_max_gtt']:.4g} | "
            f"{row['worst_min_abs_speed']:.4g} | {row['worst_compression_ratio']:.4g} | "
            f"{int(row['any_bundle_fold'])} |"
        )
    (outdir / "obstruction_screen_summary.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if plt is not None:
        labels = []
        mins = []
        comp = []
        for row in all_rows:
            if abs(row["width_factor"] - 0.25) < 1e-12:
                labels.append(row["variant"].replace("_", "\n"))
                mins.append(row["worst_min_abs_speed"])
                comp.append(row["worst_compression_ratio"])
        packet_pos = []
        packet_max = []
        for row in all_rows:
            if abs(row["width_factor"] - 0.25) < 1e-12:
                loc = row["local_scan"]
                packet_pos.append(loc["packet_norm_positive_points"])
                packet_max.append(max(loc["packet_max_norm"], 1e-6))
        fig, ax = plt.subplots(figsize=(8, 4.5))
        x = np.arange(len(labels))
        ax.bar(x, packet_pos)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=7)
        ax.set_ylabel("Packet-norm positive grid points")
        ax.set_title("Packet clearance screen at width factor 0.25")
        fig.tight_layout()
        fig.savefig(outdir.parent / "figures" / "packet_positive_points_width025.png", dpi=180)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(x, packet_max)
        ax.set_yscale("log")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=7)
        ax.set_ylabel("Packet max norm, clipped at 1e-6 for clean cases")
        ax.set_title("Packet norm failure scale at width factor 0.25")
        fig.tight_layout()
        fig.savefig(outdir.parent / "figures" / "packet_max_norm_width025.png", dpi=180)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(x, mins)
        ax.set_yscale("log")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=7)
        ax.set_ylabel("Worst minimum absolute radial null speed")
        ax.set_title("Stage 2 bundle screen at width factor 0.25")
        fig.tight_layout()
        fig.savefig(outdir.parent / "figures" / "min_null_speed_width025.png", dpi=180)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(x, comp)
        ax.set_yscale("log")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=7)
        ax.set_ylabel("Worst bundle width ratio")
        ax.set_title("Bundle compression at width factor 0.25")
        fig.tight_layout()
        fig.savefig(outdir.parent / "figures" / "bundle_compression_width025.png", dpi=180)
        plt.close(fig)

    return summary


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    summary = run(base / "data")
    print(json.dumps({
        "rows": len(summary["rows"]),
        "output": str(base / "data" / "obstruction_screen_results.json"),
    }, indent=2))
