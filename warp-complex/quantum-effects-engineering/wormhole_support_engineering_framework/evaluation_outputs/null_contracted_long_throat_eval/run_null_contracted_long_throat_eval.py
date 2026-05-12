#!/usr/bin/env python3
"""
Null-contracted long-throat evaluation for B(l)-stretched wormhole geometries.

Scope: wormhole/QEE component only. No transport, catch, passenger packet, or network layer.

Metric family:
    ds^2 = -dt^2 + B(l)^2 dl^2 + R(l)^2 dOmega^2,
    R(l) = sqrt(1 + l^2),
    B(l) = 1 + (B0 - 1) exp[-(|l|/wB)^p].

Purpose:
    Test whether the local softening found in the B-stretched throat survives
    null-contracted diagnostics, traversal sampling, and transition-shoulder checks.

Notes:
    - Tkk is the orthonormal radial null contraction rho + p_r = G_hat(k,k)/(8 pi).
    - Static-observer local sampling of Tkk is represented by a simple Lorentzian QI proxy.
    - Null-path/traversal sampling is an engineering diagnostic over the proper radial coordinate.
      It should not be read as a rigorous four-dimensional null-geodesic quantum inequality.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

C_QI = 3.0 / (32.0 * math.pi**2)


def B_profile(l: np.ndarray, B0: float, wB: float, p: float) -> np.ndarray:
    return 1.0 + (B0 - 1.0) * np.exp(-((np.abs(l) / wB) ** p))


def geometry(l: np.ndarray, B0: float, wB: float, p: float) -> dict[str, np.ndarray]:
    R = np.sqrt(1.0 + l**2)
    B = B_profile(l, B0, wB, p)

    Rp = np.gradient(R, l, edge_order=2)
    Rpp = np.gradient(Rp, l, edge_order=2)
    Bp = np.gradient(B, l, edge_order=2)

    # Static N=1 warped-product Einstein components in orthonormal frame.
    # rho = G_tt/(8pi), p_r = G_ll/(8pi B^2), Tkk = rho+p_r.
    rho = (-(2.0 / (R * B**2)) * (Rpp - (Bp / B) * Rp) + (1.0 - (Rp**2 / B**2)) / R**2) / (8.0 * math.pi)
    pr = (-(1.0 - (Rp**2 / B**2)) / R**2) / (8.0 * math.pi)
    tkk = rho + pr

    # Proper radial coordinate s(l), centered at l=0. For symmetric grids.
    dsdl = B
    s = np.zeros_like(l)
    mid = len(l) // 2
    for i in range(mid + 1, len(l)):
        s[i] = s[i - 1] + 0.5 * (dsdl[i] + dsdl[i - 1]) * (l[i] - l[i - 1])
    for i in range(mid - 1, -1, -1):
        s[i] = s[i + 1] - 0.5 * (dsdl[i] + dsdl[i + 1]) * (l[i + 1] - l[i])

    dlnB_dl = Bp / B
    dlnB_ds = dlnB_dl / B
    d2lnB_ds2 = np.gradient(dlnB_ds, s, edge_order=2)

    return {
        "l": l,
        "s": s,
        "R": R,
        "B": B,
        "rho": rho,
        "pr": pr,
        "tkk": tkk,
        "dlnB_ds": dlnB_ds,
        "d2lnB_ds2": d2lnB_ds2,
    }


def lorentzian_avg(x: np.ndarray, y: np.ndarray, x0: float, tau: float) -> float:
    w = (tau / math.pi) / ((x - x0) ** 2 + tau**2)
    return float(np.trapezoid(y * w, x) / np.trapezoid(w, x))


def sample_profile(x: np.ndarray, y: np.ndarray, tau0s: list[float], centers: np.ndarray) -> dict[str, float]:
    strict_L = float("inf")
    strict_tau = float("nan")
    strict_center = float("nan")
    strict_avg = float("nan")
    min_avg = float("inf")
    for tau in tau0s:
        # Vectorized enough for moderate grids.
        for c in centers:
            avg = lorentzian_avg(x, y, float(c), tau)
            min_avg = min(min_avg, avg)
            if avg < 0:
                Lmax = math.sqrt(C_QI / (abs(avg) * tau**4))
                if Lmax < strict_L:
                    strict_L = Lmax
                    strict_tau = float(tau)
                    strict_center = float(c)
                    strict_avg = float(avg)
    return {
        "min_sampled_avg": min_avg,
        "strict_L0max": strict_L,
        "strict_log10_L0max": math.log10(strict_L) if np.isfinite(strict_L) and strict_L > 0 else float("inf"),
        "strict_tau0": strict_tau,
        "strict_center": strict_center,
        "strict_avg": strict_avg,
    }


def half_length_to_R(l: np.ndarray, s: np.ndarray, R: np.ndarray, target: float) -> float:
    pos = l >= 0
    lp, sp, Rp = l[pos], s[pos], R[pos]
    idx = np.where(Rp >= target)[0]
    if len(idx) == 0:
        return float("nan")
    i = int(idx[0])
    if i == 0:
        return float(sp[i])
    # linear interpolation in R
    f = (target - Rp[i - 1]) / (Rp[i] - Rp[i - 1])
    return float(sp[i - 1] + f * (sp[i] - sp[i - 1]))


def summarize_case(g: dict[str, np.ndarray], B0: float, wB: float, p: float) -> dict[str, float | str]:
    l = g["l"]
    s = g["s"]
    R = g["R"]
    B = g["B"]
    rho = g["rho"]
    pr = g["pr"]
    tkk = g["tkk"]
    dlnB_ds = g["dlnB_ds"]
    d2lnB_ds2 = g["d2lnB_ds2"]

    core = np.abs(l) <= 0.25
    inner = np.abs(l) <= 0.55
    shoulder = (np.abs(l) >= 0.55) & (np.abs(l) <= max(3.0 * wB, 0.8))
    allmask = np.ones_like(l, dtype=bool)

    neg_tkk = np.maximum(-tkk, 0.0)
    neg_tkk_integral = float(np.trapezoid(neg_tkk * B, l))
    neg_tkk_core = float(np.trapezoid(neg_tkk[core] * B[core], l[core])) if np.any(core) else 0.0
    neg_tkk_inner = float(np.trapezoid(neg_tkk[inner] * B[inner], l[inner])) if np.any(inner) else 0.0
    neg_tkk_shoulder = float(np.trapezoid(neg_tkk[shoulder] * B[shoulder], l[shoulder])) if np.any(shoulder) else 0.0

    # Static observer local proxy for Tkk with tau0=1 in dimensionless units.
    local_tkk_min = float(np.min(tkk[core]))
    local_L = math.sqrt(C_QI / abs(local_tkk_min)) if local_tkk_min < 0 else float("inf")
    local_log = math.log10(local_L) if np.isfinite(local_L) else float("inf")

    # Traversal/null-path engineering sampling over proper radial coordinate s.
    # Use a wide tau range so broad weak distributions are tested at their support scale.
    s_abs_max = float(np.max(np.abs(s)))
    tau0s = [0.10, 0.20, 0.50, 1.0, 2.0, 5.0, 10.0]
    tau0s = [tau for tau in tau0s if tau < 0.8 * s_abs_max]
    centers = np.linspace(-min(8.0, 0.65 * s_abs_max), min(8.0, 0.65 * s_abs_max), 41)
    trav = sample_profile(s, tkk, tau0s, centers)

    # Timelike static worldline proxy sampled in time is just local for static source; record rho too.
    local_rho_min = float(np.min(rho[core]))
    rho_L = math.sqrt(C_QI / abs(local_rho_min)) if local_rho_min < 0 else float("inf")
    rho_log = math.log10(rho_L) if np.isfinite(rho_L) else float("inf")

    shoulder_min_tkk = float(np.min(tkk[shoulder])) if np.any(shoulder) else float("nan")
    shoulder_min_rho = float(np.min(rho[shoulder])) if np.any(shoulder) else float("nan")
    shoulder_max_abs_deriv = float(np.max(np.abs(dlnB_ds[shoulder]))) if np.any(shoulder) else 0.0
    shoulder_max_abs_second = float(np.max(np.abs(d2lnB_ds2[shoulder]))) if np.any(shoulder) else 0.0

    proper_half_R2 = half_length_to_R(l, s, R, 2.0)
    coordinate_half_R2 = half_length_to_R(l, l, R, 2.0)

    # Result classification.
    if shoulder_min_tkk < local_tkk_min * 1.10 and (shoulder_max_abs_deriv > 0.75 or shoulder_max_abs_second > 2.0):
        mode = "transition-shoulder-pathology"
    elif trav["strict_log10_L0max"] <= -0.35:
        mode = "null-sampled-burden-preserved"
    elif local_log > 0.0 and trav["strict_log10_L0max"] < local_log - 0.25:
        mode = "local-relief-traversal-penalty"
    elif proper_half_R2 > 8.0:
        mode = "long-throat-infrastructure-cost"
    else:
        mode = "useful-weak-distribution-candidate"

    return {
        "B0": B0,
        "wB": wB,
        "p": p,
        "mode": mode,
        "core_min_rho": local_rho_min,
        "core_min_tkk": local_tkk_min,
        "core_min_pr": float(np.min(pr[core])),
        "core_rho_log10_L0max_tau1": rho_log,
        "core_tkk_log10_L0max_tau1": local_log,
        "traversal_tkk_min_sampled_avg": trav["min_sampled_avg"],
        "traversal_tkk_strict_log10_L0max": trav["strict_log10_L0max"],
        "traversal_tkk_strict_tau0": trav["strict_tau0"],
        "traversal_tkk_strict_center_s": trav["strict_center"],
        "traversal_tkk_strict_avg": trav["strict_avg"],
        "neg_tkk_integral_proper": neg_tkk_integral,
        "neg_tkk_integral_core": neg_tkk_core,
        "neg_tkk_integral_inner": neg_tkk_inner,
        "neg_tkk_integral_shoulder": neg_tkk_shoulder,
        "core_fraction_neg_tkk_integral": neg_tkk_core / neg_tkk_integral if neg_tkk_integral > 0 else 0.0,
        "inner_fraction_neg_tkk_integral": neg_tkk_inner / neg_tkk_integral if neg_tkk_integral > 0 else 0.0,
        "shoulder_fraction_neg_tkk_integral": neg_tkk_shoulder / neg_tkk_integral if neg_tkk_integral > 0 else 0.0,
        "shoulder_min_tkk": shoulder_min_tkk,
        "shoulder_min_rho": shoulder_min_rho,
        "shoulder_max_abs_dlnB_ds": shoulder_max_abs_deriv,
        "shoulder_max_abs_d2lnB_ds2": shoulder_max_abs_second,
        "proper_half_length_to_R2": proper_half_R2,
        "coordinate_half_length_to_R2": coordinate_half_R2,
        "proper_to_coordinate_half_length_R2": proper_half_R2 / coordinate_half_R2 if coordinate_half_R2 > 0 else float("nan"),
        "max_B": float(np.max(B)),
    }


def main(outdir: str = ".") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    # Large enough domain for broad B shoulders; baseline R=2 occurs at l=sqrt(3) ~= 1.732.
    l = np.linspace(-28.0, 28.0, 7001)

    B0s = [1.0, 1.2, math.sqrt(2.0), 1.6, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0]
    wBs = [0.35, 0.55, 0.90, 1.60, 2.80, 5.00, 8.00]
    ps = [2.0, 4.0, 8.0]

    rows: list[dict[str, float | str]] = []
    digest_rows: list[dict[str, float | str]] = []

    for B0 in B0s:
        for wB in wBs:
            for p in ps:
                g = geometry(l, B0, wB, p)
                row = summarize_case(g, B0, wB, p)
                rows.append(row)

                # Store representative profiles for a small subset.
                if (B0, wB, p) in [
                    (1.0, 0.9, 4.0),
                    (2.0, 1.6, 4.0),
                    (3.0, 1.6, 4.0),
                    (5.0, 1.6, 4.0),
                    (3.0, 0.45, 8.0),
                    (3.0, 5.0, 2.0),
                    (10.0, 10.0, 2.0),
                ]:
                    idxs = np.unique(np.round(np.linspace(0, len(l) - 1, 801)).astype(int))
                    for i in idxs:
                        digest_rows.append({
                            "B0": B0,
                            "wB": wB,
                            "p": p,
                            "l": float(g["l"][i]),
                            "s": float(g["s"][i]),
                            "B": float(g["B"][i]),
                            "R": float(g["R"][i]),
                            "rho": float(g["rho"][i]),
                            "pr": float(g["pr"][i]),
                            "tkk": float(g["tkk"][i]),
                            "dlnB_ds": float(g["dlnB_ds"][i]),
                        })

    df = pd.DataFrame(rows)
    df.to_csv(out / "null_contracted_B_stretch_sweep.csv", index=False)
    pd.DataFrame(digest_rows).to_csv(out / "null_contracted_profile_digest.csv", index=False)

    # Extract baseline and useful rankings.
    baseline = df[(df.B0 == 1.0) & (df.wB == 0.9) & (df.p == 4.0)].iloc[0].to_dict()
    # local candidates with positive rho and locally softened Tkk, sorted by traversal QI and moderate length.
    candidates = df[
        (df["core_min_rho"] >= -1e-6)
        & (df["core_min_tkk"] > -0.015)
        & (df["proper_half_length_to_R2"] <= 7.5)
        & (df["shoulder_max_abs_dlnB_ds"] <= 0.8)
    ].copy()
    candidates = candidates.sort_values([
        "traversal_tkk_strict_log10_L0max",
        "core_tkk_log10_L0max_tau1",
        "proper_half_length_to_R2",
    ], ascending=[False, False, True]).head(20)

    best_local = df.sort_values("core_tkk_log10_L0max_tau1", ascending=False).head(20)
    best_traversal = df.sort_values("traversal_tkk_strict_log10_L0max", ascending=False).head(20)
    worst_shoulders = df.sort_values(["shoulder_max_abs_dlnB_ds", "shoulder_max_abs_d2lnB_ds2"], ascending=False).head(20)
    mode_counts = df["mode"].value_counts().to_dict()

    extracts = {
        "baseline": baseline,
        "mode_counts": mode_counts,
        "top_moderate_candidates": candidates.to_dict(orient="records"),
        "top_local_core_tkk_relief": best_local.to_dict(orient="records"),
        "top_traversal_sampled_tkk_relief": best_traversal.to_dict(orient="records"),
        "worst_transition_derivative_cases": worst_shoulders.to_dict(orient="records"),
        "interpretation": {
            "main_result": "B-stretch gives clean local rho and local Tkk relief, but traversal/null-path sampling and proper integrated negative Tkk show that the support debt is mainly spread over a longer affine/proper interval rather than removed.",
            "transition_result": "Broad smooth B shoulders avoid large derivative pathologies; narrow or high-p profiles move stress into transition shoulders and produce derivative spikes.",
            "next_gate": "A credible quantum/source model must support a long, weak radial null-contracted stress distribution. Timelike-sampled Tkk and integrated null-burden diagnostics are the next source-level tests."
        }
    }
    (out / "null_contracted_result_extracts.json").write_text(json.dumps(extracts, indent=2))

    readme = """# Null-contracted long-throat B-stretch evaluation

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
"""
    (out / "README.md").write_text(readme)

    manifest_files = [
        "run_null_contracted_long_throat_eval.py",
        "null_contracted_B_stretch_sweep.csv",
        "null_contracted_profile_digest.csv",
        "null_contracted_result_extracts.json",
        "README.md",
    ]
    checksums = {}
    for fn in manifest_files:
        fp = out / fn
        if fp.exists():
            checksums[fn] = hashlib.sha256(fp.read_bytes()).hexdigest()
    (out / "manifest.json").write_text(json.dumps({
        "bundle": "null-contracted long-throat B-stretch scratch evaluation",
        "scope": "wormhole/QEE component only",
        "files": manifest_files + ["manifest.json"],
        "sha256": checksums,
    }, indent=2))


if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
