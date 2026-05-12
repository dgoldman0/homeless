#!/usr/bin/env python3
"""
Stage 2: dynamic phase-cycled throat QI proxy evaluation.

This script reproduces the dynamic-throat first-poke outputs for the
phase-cycled throat-support idea. The model is the intentionally simple
zero-redshift breathing throat

    ds^2 = -dt^2 + dl^2 + R(l,t)^2 dOmega^2,
    R(l,t) = sqrt(a(t)^2 + l^2),

sampled at the throat l=0. The diagnostics are effective-source proxies
from the Einstein tensor in Planck units. They are used to evaluate whether
controlled throat breathing can turn a static QI obstruction into a bounded
engineering cycle.

This is not a full numerical-relativity evolution or a proof of semiclassical
admissibility. It is a cheap reduced diagnostic for source cycling, open-window
fractions, Lorentzian sampled energy, and breathing/tidal violence.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

LP_M = 1.616255e-35
C_LIGHT = 299_792_458.0
T_PLANCK_S = 5.391247e-44
C_QI = 3.0 / (32.0 * math.pi**2)


def qi_bound(tau0: float) -> float:
    return -C_QI / tau0**4


def l0_max_from_avg(avg_rho_dimless: float, tau0_dimless: float) -> float:
    """Largest L0/Lp allowed if rho_phys=avg/L0^2 and tau0_phys=tau0*L0."""
    if avg_rho_dimless >= 0:
        return float("inf")
    # |avg|/L0^2 <= C/(tau0^4 L0^4) => L0^2 <= C/(|avg| tau0^4)
    return math.sqrt(C_QI / (abs(avg_rho_dimless) * tau0_dimless**4))


def lorentzian_avg(t: np.ndarray, rho: np.ndarray, t0: float, tau0: float) -> float:
    w = (tau0 / math.pi) / ((t - t0) ** 2 + tau0**2)
    return float(np.trapz(rho * w, t) / np.trapz(w, t))


def case_a(case: str, t: np.ndarray, **kw) -> np.ndarray:
    if case == "static":
        return np.ones_like(t)
    if case == "sin":
        eps = float(kw.get("eps", 0.1))
        omega = float(kw.get("omega", 10.0))
        return 1.0 + eps * np.cos(omega * t)
    if case == "pulse":
        # Smooth open pulse: a_small + (1-a_small) exp(-(t/w)^4)
        a_closed = float(kw.get("a_closed", 0.5))
        width = float(kw.get("width", 0.02))
        return a_closed + (1.0 - a_closed) * np.exp(-(t / width) ** 4)
    raise ValueError(case)


def diagnostics(t: np.ndarray, a: np.ndarray) -> pd.DataFrame:
    dt = float(t[1] - t[0]) if len(t) > 1 else 1.0
    adot = np.gradient(a, dt)
    addot = np.gradient(adot, dt)
    # Throat l=0 effective proxies for R(l,t)=sqrt(a(t)^2+l^2).
    # Static terms reproduce rho=-1/(8*pi*a^2), Gkp=Gkm=-2/a^2 in the old report scale.
    rho = -1.0 / (8.0 * math.pi * a**2) + (adot**2) / (8.0 * math.pi * a**2)
    Gtt = 8.0 * math.pi * rho
    # Dynamic null-projection proxy: static -2/a^2 plus acceleration/speed terms.
    Gkp = -2.0 / a**2 + 2.0 * addot / np.maximum(a, 1e-12) + (adot / np.maximum(a, 1e-12)) ** 2
    Gkm = Gkp.copy()
    tidal_ang = -addot / np.maximum(a, 1e-12)
    theta_product = 4.0 * (adot / np.maximum(a, 1e-12)) ** 2
    adot_over_a = adot / np.maximum(a, 1e-12)
    return pd.DataFrame({
        "t": t,
        "a": a,
        "rho": rho,
        "Gtt": Gtt,
        "Gkp": Gkp,
        "Gkm": Gkm,
        "theta_product": theta_product,
        "tidal_ang": tidal_ang,
        "adot_over_a": adot_over_a,
    })


def qi_samples(df: pd.DataFrame, tau0s: list[float], centers: np.ndarray) -> pd.DataFrame:
    t = df["t"].to_numpy()
    rho = df["rho"].to_numpy()
    rows = []
    for tau0 in tau0s:
        for c in centers:
            avg = lorentzian_avg(t, rho, float(c), tau0)
            rows.append({
                "tau0": tau0,
                "t0": float(c),
                "lorentzian_avg_rho_dimless": avg,
                "L0max_planck_units": l0_max_from_avg(avg, tau0),
            })
    return pd.DataFrame(rows)


def summarize_case(name: str, df: pd.DataFrame, qidf: pd.DataFrame) -> dict:
    strict = qidf.loc[qidf["L0max_planck_units"].idxmin()]
    a = df["a"].to_numpy()
    max_a = float(np.max(a))
    open_mask = a > 0.9 * max_a
    quasistatic_mask = open_mask & (np.abs(df["adot_over_a"].to_numpy()) < 0.1)
    return {
        "case": name,
        "tmin": float(df["t"].min()),
        "tmax": float(df["t"].max()),
        "Nt": int(len(df)),
        "min_a": float(df["a"].min()),
        "max_a": float(df["a"].max()),
        "mean_a": float(df["a"].mean()),
        "min_rho": float(df["rho"].min()),
        "max_rho": float(df["rho"].max()),
        "mean_rho": float(df["rho"].mean()),
        "min_Gkp": float(df["Gkp"].min()),
        "min_Gkm": float(df["Gkm"].min()),
        "max_abs_tidal_angular": float(np.max(np.abs(df["tidal_ang"]))),
        "max_abs_theta_product": float(np.max(np.abs(df["theta_product"]))),
        "max_abs_adot_over_a": float(np.max(np.abs(df["adot_over_a"]))),
        "fraction_open_a_gt_0p9max": float(np.mean(open_mask)),
        "fraction_quasistatic_open": float(np.mean(quasistatic_mask)),
        "strict_tau0": float(strict["tau0"]),
        "strict_t0": float(strict["t0"]),
        "strict_avg_rho": float(strict["lorentzian_avg_rho_dimless"]),
        "strict_L0max_planck_units": float(strict["L0max_planck_units"]),
        "strict_log10_L0max": float(np.log10(strict["L0max_planck_units"])),
    }


def main(outdir: str = ".") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    cases = []
    definitions = [
        ("static_a1", "static", {}, np.linspace(-2.0, 2.0, 2001)),
        ("sin_eps0.05_om1", "sin", {"eps": 0.05, "omega": 1.0}, np.linspace(-6.0 * math.pi, 6.0 * math.pi, 2001)),
        ("sin_eps0.1_om20", "sin", {"eps": 0.1, "omega": 20.0}, np.linspace(-0.3 * math.pi, 0.3 * math.pi, 2001)),
        ("sin_eps0.6_om5", "sin", {"eps": 0.6, "omega": 5.0}, np.linspace(-1.2 * math.pi, 1.2 * math.pi, 2001)),
        ("pulse_ac0.5_w0.02", "pulse", {"a_closed": 0.5, "width": 0.02}, np.linspace(-1.0, 1.0, 2001)),
        ("pulse_ac0.1_w0.02", "pulse", {"a_closed": 0.1, "width": 0.02}, np.linspace(-1.0, 1.0, 2001)),
    ]
    tau0s = [0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]

    for name, kind, params, t in definitions:
        a = case_a(kind, t, **params)
        df = diagnostics(t, a)
        df.to_csv(out / f"timeseries_{name}.csv", index=False)
        centers = np.linspace(float(t[0]), float(t[-1]), 401)
        qidf = qi_samples(df, tau0s, centers)
        qidf.to_csv(out / f"qi_samples_{name}.csv", index=False)
        cases.append(summarize_case(name, df, qidf))

    pd.DataFrame(cases).to_csv(out / "dynamic_throat_case_summary.csv", index=False)

    open_rows = []
    # T_max ~ (8*pi*C_QI)^(1/4) sqrt(r0) in Planck units, then convert to seconds.
    pref = (8.0 * math.pi * C_QI) ** 0.25
    for radius_m in [1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1.0, 10.0]:
        r0_planck = radius_m / LP_M
        Tmax_planck = pref * math.sqrt(r0_planck)
        Tmax_s = Tmax_planck * T_PLANCK_S
        light_s = radius_m / C_LIGHT
        open_rows.append({
            "throat_radius_m": radius_m,
            "r0_planck": r0_planck,
            "QI_open_duration_est_s": Tmax_s,
            "light_crossing_time_s": light_s,
            "ratio_Tmax_to_light_crossing": Tmax_s / light_s,
        })
    pd.DataFrame(open_rows).to_csv(out / "analytic_open_window_estimates.csv", index=False)

    (out / "MODEL_NOTES.txt").write_text(
        "Dynamic phase-cycled throat support first-poke model.\n"
        "Metric proxy: ds^2=-dt^2+dl^2+(a(t)^2+l^2)dOmega^2.\n"
        "Diagnostics are effective Einstein-source proxies at l=0 plus Lorentzian QI sampling.\n"
        "This is a reduced exploratory model, not a full semiclassical calculation.\n"
    )


if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
