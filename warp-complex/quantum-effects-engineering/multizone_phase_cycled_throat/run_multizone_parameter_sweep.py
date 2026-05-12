#!/usr/bin/env python3
"""Focused parameter sweep for the multi-zone throat QEE toy model."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from run_multizone_phase_cycled_throat_eval import diagnostics, qi_zone_samples, zone_profiles, C_QI


def radius_split(t: np.ndarray, l: np.ndarray, core_amp: float, repay_amp: float, buffer_amp: float, omega: float, phase: float) -> np.ndarray:
    T, L = np.meshgrid(t, l, indexing="ij")
    Rbase = np.sqrt(1.0 + L**2)
    p = zone_profiles(l)
    Pc = p["core"][None, :]
    Pr = p["repayment"][None, :]
    Pb = p["buffer"][None, :]
    R = (
        Rbase
        + core_amp * np.sin(omega * T) * Pc
        + repay_amp * np.sin(omega * T + phase) * Pr
        + buffer_amp * np.sin(omega * T + phase / 2.0) * Pb
    )
    return np.maximum(R, 0.05)


def summarize(t: np.ndarray, l: np.ndarray, R: np.ndarray) -> dict[str, float]:
    d = diagnostics(t, l, R)
    access_mask = np.abs(l) <= 0.25
    repay_mask = (np.abs(l) >= 0.65) & (np.abs(l) <= 1.15)
    base = np.sqrt(1.0 + l**2)
    rate = d["rate"]
    tidal = d["tidal_ang"]
    flux = d["flux"]
    rho = d["rho"]
    Gkk = np.minimum(d["Gkp"], d["Gkm"])

    quiet = (
        (np.max(np.abs(rate[:, access_mask]), axis=1) < 0.10)
        & (np.max(np.abs(tidal[:, access_mask]), axis=1) < 1.00)
        & (np.max(np.abs(flux[:, access_mask]), axis=1) < 0.10)
    )
    open_mask = np.min(R[:, access_mask] / base[None, access_mask], axis=1) >= 0.90

    zones = {"access_core": (0.00, 0.25), "repayment_band": (0.65, 1.15)}
    qi = qi_zone_samples(t, l, rho, zones)
    qdict = {q["zone"]: q for q in qi}

    return {
        "access_qi_log10_L0max": float(qdict["access_core"]["qi_strict_log10_L0max"]),
        "access_qi_min_sampled_avg": float(qdict["access_core"]["qi_min_sampled_avg"]),
        "access_positive_sample_fraction": float(qdict["access_core"]["qi_positive_sample_fraction"]),
        "repay_positive_sample_fraction": float(qdict["repayment_band"]["qi_positive_sample_fraction"]),
        "repay_qi_log10_L0max": float(qdict["repayment_band"]["qi_strict_log10_L0max"]),
        "access_max_abs_tidal": float(np.max(np.abs(tidal[:, access_mask]))),
        "access_max_abs_rate": float(np.max(np.abs(rate[:, access_mask]))),
        "access_max_abs_flux": float(np.max(np.abs(flux[:, access_mask]))),
        "access_min_rho": float(np.min(rho[:, access_mask])),
        "access_max_rho": float(np.max(rho[:, access_mask])),
        "access_min_Gkk": float(np.min(Gkk[:, access_mask])),
        "repay_min_Gkk": float(np.min(Gkk[:, repay_mask])),
        "access_quiet_open_fraction": float(np.mean(quiet & open_mask)),
        "access_open_fraction": float(np.mean(open_mask)),
    }


def classify(row: dict[str, float]) -> str:
    logL = row["access_qi_log10_L0max"]
    tidal = row["access_max_abs_tidal"]
    rate = row["access_max_abs_rate"]
    quiet = row["access_quiet_open_fraction"]
    if logL < 0.0 and quiet > 0.90:
        return "static-QI-preserved"
    if logL > 0.5 and (tidal > 10.0 or rate > 1.0):
        return "QI-improves-via-ripple"
    if quiet < 0.20:
        return "quiet-window-lost"
    return "transition/marginal"


def main(outdir: str = ".") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    t = np.linspace(-1.0, 1.0, 501)
    l = np.linspace(-3.0, 3.0, 251)

    rows = []
    for core_amp in [0.0, 0.005, 0.01, 0.02, 0.04, 0.08]:
        for repay_amp in [0.0, 0.06, 0.12, 0.20]:
            for omega in [4.0, 8.0, 16.0, 32.0, 64.0]:
                buffer_amp = 0.35 * repay_amp
                R = radius_split(t, l, core_amp, repay_amp, buffer_amp, omega, math.pi)
                row = {
                    "core_amp": core_amp,
                    "repay_amp": repay_amp,
                    "buffer_amp": buffer_amp,
                    "omega": omega,
                }
                row.update(summarize(t, l, R))
                row["failure_mode"] = classify(row)
                rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(out / "multizone_parameter_sweep.csv", index=False)

    # Pareto-ish extract: best access QI log among cases with quiet-open fractions above thresholds.
    extracts = {}
    for thr in [0.9, 0.5, 0.2, 0.05]:
        sub = df[df["access_quiet_open_fraction"] >= thr].copy()
        if len(sub):
            extracts[f"best_with_quiet_open_ge_{thr}"] = sub.sort_values("access_qi_log10_L0max", ascending=False).head(8).to_dict(orient="records")
        else:
            extracts[f"best_with_quiet_open_ge_{thr}"] = []

    # Best QI gains regardless of violence.
    extracts["best_access_qi_any"] = df.sort_values("access_qi_log10_L0max", ascending=False).head(12).to_dict(orient="records")
    extracts["failure_counts"] = df["failure_mode"].value_counts().to_dict()
    (out / "multizone_parameter_sweep_extracts.json").write_text(json.dumps(extracts, indent=2))


if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
