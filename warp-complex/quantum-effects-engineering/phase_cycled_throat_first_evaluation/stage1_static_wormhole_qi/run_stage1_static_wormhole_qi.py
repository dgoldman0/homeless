#!/usr/bin/env python3
"""
Stage 1: static wormhole throat QI proxy evaluation.

This script reproduces the Stage 1 outputs for the phase-cycled throat-support
first evaluation. It uses a zero-redshift Morris--Thorne radial throat

    ds^2 = -dt^2 + dl^2 + r(l)^2 dOmega^2,
    r(l) = sqrt(r0^2 + l^2),

and the throat source proxy

    rho0 = -1/(8*pi*r0^2),
    rho0 + p_l = -1/(4*pi*r0^2),

in Planck units. It applies a Lorentzian-sampling quantum-inequality proxy

    int rho(t) (tau0/pi)/(t^2+tau0^2) dt >= -3/(32*pi^2*tau0^4).

The pulse-train section is a bookkeeping/demo proxy: it tests whether a
negative/positive pulse train can hide a sustained negative mean from
Lorentzian sampling windows. It is not a semiclassical proof.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

LP_M = 1.616255e-35
C_QI = 3.0 / (32.0 * math.pi**2)


def qi_bound(tau0: float) -> float:
    return -C_QI / tau0**4


def rho_throat(r0: float) -> float:
    return -1.0 / (8.0 * math.pi * r0**2)


def qi_ratio(r0: float, eta: float) -> float:
    tau0 = eta * r0
    return abs(rho_throat(r0)) / abs(qi_bound(tau0))


def lorentzian_avg(t: np.ndarray, rho: np.ndarray, t0: float, tau0: float) -> float:
    w = (tau0 / math.pi) / ((t - t0) ** 2 + tau0**2)
    # Normalize over finite numerical window so the CSV is stable across grid choices.
    return float(np.trapz(rho * w, t) / np.trapz(w, t))


def make_square_pulse_train(
    t: np.ndarray,
    period: float,
    rho_mean: float,
    negative_amp: float,
    positive_amp: float,
    neg_fraction: float = 0.10,
    pos_fraction: float = 0.16,
    pos_delay_fraction: float = 0.20,
) -> np.ndarray:
    """Simple compensated pulse train around a negative mean."""
    phase = np.mod(t, period) / period
    rho = np.full_like(t, rho_mean, dtype=float)
    rho[phase < neg_fraction] += negative_amp
    pos_start = pos_delay_fraction
    pos_end = min(1.0, pos_start + pos_fraction)
    rho[(phase >= pos_start) & (phase < pos_end)] += positive_amp
    return rho


def main(outdir: str = ".") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    etas = [0.1, 0.03, 0.01, 0.003, 0.001]
    r0s = np.array([1, 3, 10, 30, 100, 300, 1e3, 3e3, 1e4, 3e4, 1e5, 3e5, 1e6,
                    1e9, 1e12, 1e20, 6.18714249917247e34])

    rows = []
    for r0 in r0s:
        row = {"r0_Lp": float(r0), "rho_throat_planck": rho_throat(float(r0))}
        for eta in etas:
            ratio = qi_ratio(float(r0), eta)
            row[f"QI_ratio_eta_{eta:g}"] = ratio
            row[f"pass_eta_{eta:g}"] = bool(ratio <= 1.0)
        rows.append(row)
    pd.DataFrame(rows).to_csv(out / "static_wormhole_qi_ratio_sweep.csv", index=False)

    allowed = []
    for eta in etas:
        # |rho| <= C/tau0^4 with rho=1/(8pi r0^2), tau0=eta*r0.
        r0max = math.sqrt(8.0 * math.pi * C_QI) / (eta**2)
        allowed.append({"eta": eta, "r0_max_Lp": r0max, "r0_max_m": r0max * LP_M})
    pd.DataFrame(allowed).to_csv(out / "static_wormhole_qi_allowed_r0_by_sampling_fraction.csv", index=False)

    band_rows = []
    for r0 in [1e3, 1e6, 1e9, 1e12, 1e20, 6.18714249917247e34]:
        for eta in etas:
            # Crude compression estimate used in the report.
            delta = (16.0 * C_QI * r0 / eta**4) ** (1.0 / 3.0)
            band_rows.append({
                "r0_Lp": r0,
                "eta": eta,
                "delta_max_Lp": delta,
                "delta_max_m": delta * LP_M,
                "delta_over_r0": delta / r0,
            })
    pd.DataFrame(band_rows).to_csv(out / "compressed_exotic_band_crude_delta_estimate.csv", index=False)

    pulse_rows = []
    for r0 in [1e3, 1e6, 1e9, 1e12]:
        rho_mean = rho_throat(r0)
        for period in [1.0, 10.0, 100.0]:
            t = np.linspace(-20 * period, 20 * period, 20001)
            neg_amp = 80.0 * rho_mean  # more negative than mean
            pos_amp = -60.0 * rho_mean  # positive repayment
            rho = make_square_pulse_train(t, period, rho_mean, neg_amp, pos_amp)
            for tau0_over_period in [0.005, 0.02, 0.1, 0.5, 1.0, 5.0, 10.0]:
                tau0 = tau0_over_period * period
                centers = np.linspace(-period, period, 41)
                avgs = np.array([lorentzian_avg(t, rho, c, tau0) for c in centers])
                bound = qi_bound(tau0)
                pulse_rows.append({
                    "r0_Lp": r0,
                    "period_Lp": period,
                    "tau0_over_period": tau0_over_period,
                    "tau0_Lp": tau0,
                    "rho_req_mean": rho_mean,
                    "negative_amp": neg_amp,
                    "positive_amp": pos_amp,
                    "min_sampled_avg": float(np.min(avgs)),
                    "mean_sampled_avg": float(np.mean(avgs)),
                    "max_sampled_avg": float(np.max(avgs)),
                    "QI_bound": bound,
                    "violates_at_min": bool(np.min(avgs) < bound),
                    "geometry_window_ratio_at_tau0_0p1r0": qi_ratio(r0, 0.1),
                })
    pd.DataFrame(pulse_rows).to_csv(out / "pulse_train_lorentzian_sampling_demo.csv", index=False)

    summary = {
        "model": "zero-redshift static Morris-Thorne throat, r(l)=sqrt(r0^2+l^2)",
        "qi_proxy": "Lorentzian sampling bound, -3/(32*pi^2*tau0^4)",
        "conclusion": "static smooth macroscopic throat fails the local QI proxy; pulse train around a static mean does not hide the sustained negative average.",
        "constants": {"LP_M": LP_M, "C_QI": C_QI},
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
