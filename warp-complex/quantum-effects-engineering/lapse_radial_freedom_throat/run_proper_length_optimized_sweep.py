#!/usr/bin/env python3
"""
Proper-length optimized throat sweep.

Continuation of the lapse/radial-metric freedom toy model. This script stays
wormhole-component-only and asks whether the positive B(l) signal is a real
static/quasi-static engineering direction or just local bookkeeping.

Metric proxy:
    ds^2 = -dt^2 + B(l)^2 dl^2 + R(l)^2 dOmega^2

N=1 throughout.  The sweep varies:
    - B0: radial proper-length stretch in the throat core
    - wB: radial width over which B(l)>1
    - aR: slow-flare factor for R(l) in the core
    - wR: transition width returning R(l) toward ordinary asymptotic slope

Diagnostics include local rho and rho+p_r at the access core, QI-style scale
estimates, transition/shoulder stresses, and integrated negative burdens over
proper radial length B dl.

This is not a semiclassical calculation.  It is a reduced failure-mode probe.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

C_QI = 3.0 / (32.0 * math.pi**2)


def even_profile(l: np.ndarray, width: float, power: int = 6) -> np.ndarray:
    return np.exp(-(np.abs(l) / width) ** power)


def make_static_fields(l: np.ndarray, B0: float, wB: float, aR: float, wR: float) -> tuple[np.ndarray, np.ndarray]:
    """Build B(l), R(l). R returns to ordinary coordinate slope outside the core."""
    pB = even_profile(l, wB, 6)
    B = np.exp(np.log(B0) * pB)

    pR = even_profile(l, wR, 6)
    # g=1/aR in the core and tends to 1 outside. R=sqrt(1+(g l)^2).
    g = 1.0 - (1.0 - 1.0 / aR) * pR
    R = np.sqrt(1.0 + (g * l) ** 2)
    return B, R


def grad(A: np.ndarray, x: np.ndarray) -> np.ndarray:
    return np.gradient(A, x, edge_order=2)


def static_diagnostics(l: np.ndarray, B: np.ndarray, R: np.ndarray) -> dict[str, np.ndarray]:
    """Static N=1 specialization of the warped-product diagnostics."""
    Rl = grad(R, l)
    Rll_coord = grad(Rl, l)
    Bl = grad(B, l)

    # Covariant second derivative on 2D base diag(-1, B^2).
    # nab_ll R = R'' - Gamma^l_ll R' = R'' - (B'/B)R'
    nab_ll_R = Rll_coord - (Bl / B) * Rl
    gradR2 = (Rl / B) ** 2
    boxR = nab_ll_R / (B**2)

    Gtt = -2.0 * boxR + (1.0 - gradR2) / (R**2)
    Gll = -B**2 * (1.0 - gradR2) / (R**2)  # static cancellation of nab_ll terms

    rho = Gtt / (8.0 * math.pi)
    p_r = Gll / (8.0 * math.pi * B**2)
    nec = rho + p_r
    Gkk = 8.0 * math.pi * nec

    # Proper-coordinate shape diagnostics.
    dR_ds = Rl / B
    d2R_ds2 = nab_ll_R / (B**2)
    flare = d2R_ds2

    return {
        "rho": rho,
        "p_radial": p_r,
        "nec": nec,
        "Gkk": Gkk,
        "dR_ds": dR_ds,
        "d2R_ds2": d2R_ds2,
        "flare": flare,
        "B_grad_proper": Bl / (B**2),
        "R_grad_coord": Rl,
        "R_second_coord": Rll_coord,
    }


def qiscale_log(q: float, tau0: float = 1.0) -> float:
    if q >= 0.0:
        return float("inf")
    return math.log10(math.sqrt(C_QI / (abs(q) * tau0**4)))


def integrate_proper(l: np.ndarray, B: np.ndarray, y: np.ndarray, mask: np.ndarray | None = None) -> float:
    if mask is None:
        return float(np.trapezoid(y * B, l))
    return float(np.trapezoid((y * B)[mask], l[mask]))


def first_radius_crossing(l: np.ndarray, R: np.ndarray, target: float) -> float:
    pos = l >= 0
    lp = l[pos]
    Rp = R[pos]
    idx = np.where(Rp >= target)[0]
    if len(idx) == 0:
        return float("nan")
    return float(lp[idx[0]])


def proper_half_length_to_l(l: np.ndarray, B: np.ndarray, ltarget: float) -> float:
    if not np.isfinite(ltarget):
        return float("nan")
    posmask = (l >= 0) & (l <= ltarget)
    if np.sum(posmask) < 2:
        return 0.0
    return float(np.trapezoid(B[posmask], l[posmask]))


def classify(row: dict) -> str:
    rho_log = row["access_rho_log10_L0max"]
    nec_log = row["access_nec_log10_L0max"]
    transition = row["transition_max_abs_nec"]
    shoulder_rho = row["transition_max_abs_rho"]
    proper_to_R2 = row["proper_half_length_to_R2"]
    int_nec = row["integrated_neg_nec_total"]
    core_nec_min = row["access_nec_min"]

    if np.isfinite(rho_log) and rho_log < -0.1:
        return "rho-obstruction-persists"
    if core_nec_min < -0.01 and nec_log < 0.5:
        if proper_to_R2 > 6.0:
            return "rho-helped-nec-debt-stretched-long"
        return "rho-helped-nec-debt-remains"
    if transition > 2.0 or shoulder_rho > 1.0:
        return "transition-shoulder-burden"
    if int_nec > 1.0:
        return "integrated-nec-burden-large"
    if proper_to_R2 > 10.0:
        return "long-throat-engineering-burden"
    return "candidate-static-envelope"


def run(outdir: str = ".") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    l = np.linspace(-12.0, 12.0, 2401)

    B0s = [1.0, 1.2, math.sqrt(2), 1.6, 2.0, 3.0, 5.0, 8.0, 12.0]
    wBs = [0.45, 0.75, 1.1, 1.6, 2.4, 3.6, 5.0]
    aRs = [1.0, 1.4, 2.0, 3.0, 5.0, 8.0, 12.0]
    wRs = [0.45, 0.75, 1.1, 1.6, 2.4, 3.6, 5.0]

    rows = []
    digest_rows = []
    for B0 in B0s:
        for wB in wBs:
            for aR in aRs:
                for wR in wRs:
                    B, R = make_static_fields(l, B0, wB, aR, wR)
                    d = static_diagnostics(l, B, R)
                    rho = d["rho"]
                    nec = d["nec"]
                    Gkk = d["Gkk"]

                    access = np.abs(l) <= 0.25
                    support = np.abs(l) <= 0.75
                    transition = ((np.abs(l) >= 0.75) & (np.abs(l) <= 5.5))
                    allmask = np.ones_like(l, dtype=bool)

                    lR15 = first_radius_crossing(l, R, 1.5)
                    lR2 = first_radius_crossing(l, R, 2.0)
                    lR5 = first_radius_crossing(l, R, 5.0)
                    sR15 = proper_half_length_to_l(l, B, lR15)
                    sR2 = proper_half_length_to_l(l, B, lR2)
                    sR5 = proper_half_length_to_l(l, B, lR5)

                    row = {
                        "B0": B0,
                        "wB": wB,
                        "aR": aR,
                        "wR": wR,
                        "access_rho_min": float(np.min(rho[access])),
                        "access_rho_mean": float(np.mean(rho[access])),
                        "access_rho_max": float(np.max(rho[access])),
                        "access_nec_min": float(np.min(nec[access])),
                        "access_nec_mean": float(np.mean(nec[access])),
                        "access_Gkk_min": float(np.min(Gkk[access])),
                        "access_flare_mean": float(np.mean(d["flare"][access])),
                        "access_max_abs_B_grad_proper": float(np.max(np.abs(d["B_grad_proper"][access]))),
                        "transition_max_abs_rho": float(np.max(np.abs(rho[transition]))),
                        "transition_max_abs_nec": float(np.max(np.abs(nec[transition]))),
                        "transition_min_nec": float(np.min(nec[transition])),
                        "transition_max_abs_Gkk": float(np.max(np.abs(Gkk[transition]))),
                        "transition_max_abs_B_grad_proper": float(np.max(np.abs(d["B_grad_proper"][transition]))),
                        "integrated_neg_rho_access": integrate_proper(l, B, np.maximum(0.0, -rho), access),
                        "integrated_neg_nec_access": integrate_proper(l, B, np.maximum(0.0, -nec), access),
                        "integrated_neg_rho_support": integrate_proper(l, B, np.maximum(0.0, -rho), support),
                        "integrated_neg_nec_support": integrate_proper(l, B, np.maximum(0.0, -nec), support),
                        "integrated_neg_rho_total": integrate_proper(l, B, np.maximum(0.0, -rho), allmask),
                        "integrated_neg_nec_total": integrate_proper(l, B, np.maximum(0.0, -nec), allmask),
                        "proper_half_length_to_R1p5": sR15,
                        "proper_half_length_to_R2": sR2,
                        "proper_half_length_to_R5": sR5,
                        "coordinate_half_length_to_R2": lR2,
                        "max_B": float(np.max(B)),
                        "min_B": float(np.min(B)),
                        "max_R": float(np.max(R)),
                        "access_rho_log10_L0max": qiscale_log(float(np.min(rho[access]))),
                        "access_nec_log10_L0max": qiscale_log(float(np.min(nec[access]))),
                    }
                    row["failure_mode"] = classify(row)
                    rows.append(row)

                    # Digest only a few handpicked/interesting parameter surfaces.
                    if (B0 in [1.0, math.sqrt(2), 2.0, 5.0, 12.0]) and (wB in [0.75, 2.4, 5.0]) and (aR in [1.0, 3.0, 8.0]) and (wR in [0.75, 2.4, 5.0]):
                        for li in np.linspace(0, len(l)-1, 161).round().astype(int):
                            digest_rows.append({
                                "B0": B0, "wB": wB, "aR": aR, "wR": wR,
                                "l": float(l[li]), "B": float(B[li]), "R": float(R[li]),
                                "rho": float(rho[li]), "nec": float(nec[li]), "Gkk": float(Gkk[li]),
                                "flare": float(d["flare"][li]),
                            })

    df = pd.DataFrame(rows)
    df.to_csv(out / "proper_length_optimized_sweep.csv", index=False)
    pd.DataFrame(digest_rows).to_csv(out / "proper_length_profile_digest.csv", index=False)

    # Extracts: best candidates under several constraints.
    extracts = {}
    extracts["failure_mode_counts"] = df["failure_mode"].value_counts().to_dict()
    extracts["best_rho_scale"] = df.sort_values(["access_rho_log10_L0max", "transition_max_abs_nec"], ascending=[False, True]).head(20).to_dict(orient="records")
    extracts["best_nec_scale"] = df.sort_values(["access_nec_log10_L0max", "integrated_neg_nec_total"], ascending=[False, True]).head(20).to_dict(orient="records")
    cand = df[
        (df["access_rho_log10_L0max"] > 0.0)
        & (df["access_nec_log10_L0max"] > 0.0)
        & (df["transition_max_abs_nec"] < 1.0)
        & (df["proper_half_length_to_R2"] < 8.0)
        & (df["integrated_neg_nec_total"] < 1.0)
    ]
    extracts["candidate_static_envelopes_count"] = int(len(cand))
    extracts["candidate_static_envelopes"] = cand.sort_values(["integrated_neg_nec_total", "transition_max_abs_nec"]).head(30).to_dict(orient="records")
    extracts["best_balanced"] = df.assign(
        score=(
            df["integrated_neg_nec_total"]
            + 0.5 * df["integrated_neg_rho_total"]
            + 0.25 * df["transition_max_abs_nec"]
            + 0.05 * df["proper_half_length_to_R2"].fillna(50.0)
            - 0.5 * np.minimum(df["access_rho_log10_L0max"].replace(np.inf, 10.0), 10.0)
            - 0.25 * np.minimum(df["access_nec_log10_L0max"].replace(np.inf, 10.0), 10.0)
        )
    ).sort_values("score").head(30).to_dict(orient="records")

    (out / "proper_length_sweep_extracts.json").write_text(json.dumps(extracts, indent=2, allow_nan=True))

    summary = {
        "name": "proper-length optimized static throat sweep",
        "scope": "wormhole/QEE component only; static N=1 B(l),R(l) family",
        "metric": "ds^2=-dt^2+B(l)^2dl^2+R(l)^2dOmega^2",
        "grid_size": len(df),
        "parameters": {"B0": B0s, "wB": wBs, "aR": aRs, "wR": wRs},
        "high_level_result_placeholder": "See CSV/extracts; generated by script.",
    }
    (out / "proper_length_sweep_summary.json").write_text(json.dumps(summary, indent=2))

    files = [
        "run_proper_length_optimized_sweep.py",
        "proper_length_optimized_sweep.csv",
        "proper_length_profile_digest.csv",
        "proper_length_sweep_extracts.json",
        "proper_length_sweep_summary.json",
    ]
    checksums = {}
    for name in files:
        fp = out / name
        if fp.exists():
            checksums[name] = hashlib.sha256(fp.read_bytes()).hexdigest()
    (out / "proper_length_manifest.json").write_text(json.dumps({"files": files, "sha256": checksums}, indent=2))


if __name__ == "__main__":
    run(Path(__file__).resolve().parent)
