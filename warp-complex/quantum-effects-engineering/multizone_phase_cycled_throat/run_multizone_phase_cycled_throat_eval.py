#!/usr/bin/env python3
"""
Multi-zone phase-cycled wormhole throat plant: reduced QEE evaluation.

This is a wormhole-component-only toy evaluation. It intentionally avoids the
transport/catch/passenger layers and asks whether spatially separated source
cycling gives more information than the earlier global breathing-throat model.

Metric proxy:
    ds^2 = -dt^2 + dl^2 + R(l,t)^2 dOmega^2

The script evaluates radial multi-zone actuation schedules for R(l,t), computes
exact warped-product Einstein-tensor proxies for this metric family, and tracks
local Lorentzian-sampled energy by observer zone.

It is not a full semiclassical calculation and not a numerical-relativity
evolution. It is a reproducible reduced failure-mode probe.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

LP_M = 1.616255e-35
C_LIGHT = 299_792_458.0
T_PLANCK_S = 5.391247e-44
C_QI = 3.0 / (32.0 * math.pi**2)


def zone_profiles(l: np.ndarray) -> dict[str, np.ndarray]:
    """Smooth even radial windows for access, support, repayment, and buffer zones."""
    x = np.abs(l)
    return {
        "core": np.exp(-(x / 0.35) ** 4),
        "access": np.exp(-(x / 0.22) ** 8),
        "support": np.exp(-((x - 0.45) / 0.18) ** 4),
        "repayment": np.exp(-((x - 0.90) / 0.25) ** 4),
        "buffer": np.exp(-((x - 1.55) / 0.35) ** 4),
        "outer": np.exp(-((x - 2.45) / 0.45) ** 4),
    }


def make_radius(case: str, t: np.ndarray, l: np.ndarray) -> np.ndarray:
    """Return R(l,t) for a named multi-zone schedule."""
    T, L = np.meshgrid(t, l, indexing="ij")
    Rbase = np.sqrt(1.0 + L**2)
    p = zone_profiles(l)
    Pc = p["core"][None, :]
    Pr = p["repayment"][None, :]
    Pb = p["buffer"][None, :]
    Po = p["outer"][None, :]

    if case == "static_reference":
        R = Rbase.copy()

    elif case == "sideband_repay_only":
        # Repayment/buffer cycling deliberately kept out of the protected access core.
        omega = 10.0
        R = Rbase + 0.10 * np.sin(omega * T) * Pr + 0.04 * np.sin(omega * T + math.pi / 2) * Pb

    elif case == "protected_core_sidecycle":
        # More aggressive side cycling, still with no intentional core actuation.
        omega = 22.0
        R = (
            Rbase
            + 0.14 * np.sin(omega * T) * Pr
            - 0.08 * np.sin(omega * T - 0.7) * Pb
            + 0.03 * np.sin(omega * T + 0.6) * Po
        )

    elif case == "mild_split_phase":
        # Small core actuation plus out-of-phase repayment and buffer bands.
        omega = 8.0
        R = (
            Rbase
            + 0.035 * np.sin(omega * T) * Pc
            + 0.075 * np.sin(omega * T + math.pi) * Pr
            + 0.030 * np.sin(omega * T + math.pi / 2) * Pb
        )

    elif case == "fast_split_phase":
        # Faster multi-zone actuation with a still-moderate core amplitude.
        omega = 28.0
        R = (
            Rbase
            + 0.060 * np.sin(omega * T) * Pc
            + 0.120 * np.sin(omega * T + math.pi) * Pr
            + 0.045 * np.sin(omega * T + math.pi / 2) * Pb
        )

    elif case == "ultrafast_tiny_core":
        # Tiny but very fast core motion: tests whether high-frequency bookkeeping helps.
        omega = 80.0
        R = (
            Rbase
            + 0.025 * np.sin(omega * T) * Pc
            + 0.080 * np.sin(omega * T + math.pi) * Pr
            + 0.030 * np.sin(omega * T + math.pi / 2) * Pb
        )

    elif case == "aggressive_core_phase":
        # Deliberately violent case: should improve QI bookkeeping if the trade is real.
        omega = 45.0
        R = (
            Rbase
            + 0.120 * np.sin(omega * T) * Pc
            + 0.180 * np.sin(omega * T + math.pi) * Pr
            + 0.060 * np.sin(omega * T + math.pi / 2) * Pb
        )

    elif case == "short_access_pulse_repay_shoulders":
        # Access core is mostly pinched, briefly opens, then shoulders repay.
        open_pulse = np.exp(-(T / 0.045) ** 4)
        repay = np.exp(-((T - 0.12) / 0.075) ** 4)
        buffer = np.exp(-((T - 0.22) / 0.11) ** 4)
        R = Rbase - 0.30 * Pc + 0.30 * open_pulse * Pc + 0.16 * repay * Pr - 0.07 * buffer * Pb

    elif case == "outward_repayment_wave":
        # Symmetric outward-moving source/ripple wave, representing routed repayment.
        open_pulse = np.exp(-(T / 0.06) ** 4)
        v = 4.0
        w = 0.18
        wave = (
            np.exp(-((np.abs(L) - (0.25 + v * np.maximum(T, 0.0))) / w) ** 4)
            * (T >= 0.0)
            * np.exp(-(T / 0.35) ** 2)
        )
        R = Rbase - 0.16 * Pc + 0.16 * open_pulse * Pc + 0.10 * wave + 0.04 * np.exp(-((T - 0.30) / 0.12) ** 4) * Pb

    elif case == "delayed_side_repay_with_static_core":
        # Explicit test of the tempting idea: keep core static, delay repayment outside.
        neg_side = -0.04 * np.exp(-((T + 0.10) / 0.09) ** 4) * Pr
        pos_side = 0.12 * np.exp(-((T - 0.18) / 0.10) ** 4) * Pr
        damp = -0.05 * np.exp(-((T - 0.30) / 0.16) ** 4) * Pb
        R = Rbase + neg_side + pos_side + damp

    else:
        raise ValueError(f"Unknown case: {case}")

    return np.maximum(R, 0.05)


def diagnostics(t: np.ndarray, l: np.ndarray, R: np.ndarray) -> dict[str, np.ndarray]:
    """
    Warped-product Einstein-tensor proxies for
        ds^2=-dt^2+dl^2+R(l,t)^2 dOmega^2.

    Static R=sqrt(1+l^2) gives rho=G_tt/(8pi)=-1/(8pi R^4),
    matching the static throat proxy at r0=1.
    """
    Rt = np.gradient(R, t, axis=0, edge_order=2)
    Rl = np.gradient(R, l, axis=1, edge_order=2)
    Rtt = np.gradient(Rt, t, axis=0, edge_order=2)
    Rll = np.gradient(Rl, l, axis=1, edge_order=2)
    Rtl = np.gradient(Rt, l, axis=1, edge_order=2)

    Gtt = -2.0 * Rll / R + (1.0 + Rt**2 - Rl**2) / R**2
    Gll = -2.0 * Rtt / R - (1.0 + Rt**2 - Rl**2) / R**2
    Gtl = -2.0 * Rtl / R

    rho = Gtt / (8.0 * math.pi)
    Gkp = Gtt + Gll + 2.0 * Gtl
    Gkm = Gtt + Gll - 2.0 * Gtl

    return {
        "R": R,
        "Rt": Rt,
        "Rl": Rl,
        "Rtt": Rtt,
        "Rll": Rll,
        "Rtl": Rtl,
        "Gtt": Gtt,
        "Gll": Gll,
        "Gtl": Gtl,
        "rho": rho,
        "Gkp": Gkp,
        "Gkm": Gkm,
        "tidal_ang": -Rtt / R,
        "theta_product": 4.0 * (Rt**2 - Rl**2) / R**2,
        "rate": Rt / R,
        "flux": Gtl / (8.0 * math.pi),
    }


def qi_zone_samples(t: np.ndarray, l: np.ndarray, rho: np.ndarray, zones: dict[str, tuple[float, float]]) -> list[dict[str, float | str]]:
    """Lorentzian-sampled energy at representative static observers in each radial zone."""
    tau0s = np.array([0.02, 0.05, 0.10, 0.20, 0.50, 1.00])
    centers = np.linspace(float(t[0] * 0.85), float(t[-1] * 0.85), 61)

    rows: list[dict[str, float | str]] = []
    for zone, (lo, hi) in zones.items():
        idxs = np.where((np.abs(l) >= lo) & (np.abs(l) <= hi))[0]
        # Downsample only within the selected zone.  Do not interpolate between
        # the first and last absolute-value match; symmetric bands would otherwise
        # accidentally include the throat core.
        if len(idxs) > 15:
            pick = np.unique(np.round(np.linspace(0, len(idxs) - 1, 15)).astype(int))
            idxs = idxs[pick]
        rho_sub = rho[:, idxs]

        strict_L = float("inf")
        strict_tau = float("nan")
        strict_t0 = float("nan")
        strict_l = float("nan")
        strict_avg = float("nan")
        min_sampled_avg = float("inf")
        max_sampled_avg = -float("inf")
        positive_fraction = 0.0
        count_total = 0
        count_positive = 0

        for tau0 in tau0s:
            W = (tau0 / math.pi) / ((t[None, :] - centers[:, None]) ** 2 + tau0**2)
            W = W / (np.trapezoid(W, t, axis=1)[:, None])
            avgs = np.trapezoid(W[:, :, None] * rho_sub[None, :, :], t, axis=1)

            min_sampled_avg = min(min_sampled_avg, float(np.min(avgs)))
            max_sampled_avg = max(max_sampled_avg, float(np.max(avgs)))
            count_total += avgs.size
            count_positive += int(np.sum(avgs > 0.0))

            neg = avgs < 0.0
            if np.any(neg):
                Lvals = np.full_like(avgs, float("inf"), dtype=float)
                Lvals[neg] = np.sqrt(C_QI / (np.abs(avgs[neg]) * tau0**4))
                flat = int(np.nanargmin(Lvals))
                if float(Lvals.flat[flat]) < strict_L:
                    ci, li = np.unravel_index(flat, Lvals.shape)
                    strict_L = float(Lvals[ci, li])
                    strict_tau = float(tau0)
                    strict_t0 = float(centers[ci])
                    strict_l = float(l[idxs[li]])
                    strict_avg = float(avgs[ci, li])

        positive_fraction = count_positive / count_total if count_total else 0.0
        rows.append({
            "zone": zone,
            "qi_min_sampled_avg": min_sampled_avg,
            "qi_max_sampled_avg": max_sampled_avg,
            "qi_positive_sample_fraction": positive_fraction,
            "qi_strict_L0max_planck_units": strict_L,
            "qi_strict_log10_L0max": math.log10(strict_L) if np.isfinite(strict_L) and strict_L > 0 else float("inf"),
            "qi_strict_tau0": strict_tau,
            "qi_strict_t0": strict_t0,
            "qi_strict_l": strict_l,
            "qi_strict_avg": strict_avg,
        })

    return rows


def summarize_case(case: str, t: np.ndarray, l: np.ndarray, d: dict[str, np.ndarray]) -> tuple[dict[str, float | str], list[dict[str, float | str]]]:
    zones = {
        "access_core": (0.00, 0.25),
        "support_inner": (0.00, 0.55),
        "repayment_band": (0.65, 1.15),
        "buffer_band": (1.25, 1.90),
        "outer_field": (2.10, 3.20),
    }

    R = d["R"]
    rho = d["rho"]
    Gkk = np.minimum(d["Gkp"], d["Gkm"])
    tidal = d["tidal_ang"]
    theta = d["theta_product"]
    rate = d["rate"]
    flux = d["flux"]

    row: dict[str, float | str] = {"case": case}
    for zone, (lo, hi) in zones.items():
        mask = (np.abs(l) >= lo) & (np.abs(l) <= hi)
        row[f"{zone}_min_rho"] = float(np.min(rho[:, mask]))
        row[f"{zone}_max_rho"] = float(np.max(rho[:, mask]))
        row[f"{zone}_mean_rho"] = float(np.mean(rho[:, mask]))
        row[f"{zone}_min_Gkk"] = float(np.min(Gkk[:, mask]))
        row[f"{zone}_max_abs_tidal"] = float(np.max(np.abs(tidal[:, mask])))
        row[f"{zone}_max_abs_theta_product"] = float(np.max(np.abs(theta[:, mask])))
        row[f"{zone}_max_abs_rate"] = float(np.max(np.abs(rate[:, mask])))
        row[f"{zone}_max_abs_flux"] = float(np.max(np.abs(flux[:, mask])))

    base = np.sqrt(1.0 + l**2)
    access_mask = np.abs(l) <= 0.25
    quiet = (
        (np.max(np.abs(rate[:, access_mask]), axis=1) < 0.10)
        & (np.max(np.abs(tidal[:, access_mask]), axis=1) < 1.00)
        & (np.max(np.abs(flux[:, access_mask]), axis=1) < 0.10)
    )
    open_mask = np.min(R[:, access_mask] / base[None, access_mask], axis=1) >= 0.90

    row["access_open_fraction"] = float(np.mean(open_mask))
    row["access_quiet_fraction"] = float(np.mean(quiet))
    row["access_quiet_open_fraction"] = float(np.mean(quiet & open_mask))
    row["access_min_R_over_base"] = float(np.min(R[:, access_mask] / base[None, access_mask]))
    row["access_max_R_over_base"] = float(np.max(R[:, access_mask] / base[None, access_mask]))

    qi_rows = qi_zone_samples(t, l, rho, zones)
    for q in qi_rows:
        zone = str(q["zone"])
        for k, v in q.items():
            if k != "zone":
                row[f"{zone}_{k}"] = v

    access_log = float(row["access_core_qi_strict_log10_L0max"])
    access_tidal = float(row["access_core_max_abs_tidal"])
    access_rate = float(row["access_core_max_abs_rate"])
    quiet_open = float(row["access_quiet_open_fraction"])

    if access_log < 0.0 and quiet_open > 0.90:
        failure_mode = "static-QI-obstruction-preserved"
    elif access_log > 0.5 and (access_tidal > 10.0 or access_rate > 1.0):
        failure_mode = "QI-improvement-bought-by-access-ripple"
    elif quiet_open < 0.05:
        failure_mode = "access-window-collapse"
    else:
        failure_mode = "mixed-no-clear-envelope"

    row["failure_mode"] = failure_mode
    return row, qi_rows


def main(outdir: str = ".") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    t = np.linspace(-1.20, 1.20, 801)
    l = np.linspace(-3.50, 3.50, 351)

    cases = [
        "static_reference",
        "sideband_repay_only",
        "protected_core_sidecycle",
        "delayed_side_repay_with_static_core",
        "mild_split_phase",
        "fast_split_phase",
        "ultrafast_tiny_core",
        "aggressive_core_phase",
        "short_access_pulse_repay_shoulders",
        "outward_repayment_wave",
    ]

    case_rows = []
    qi_rows_all = []
    digest_rows = []

    for case in cases:
        R = make_radius(case, t, l)
        d = diagnostics(t, l, R)
        row, qi_rows = summarize_case(case, t, l, d)
        case_rows.append(row)
        for q in qi_rows:
            qi_rows_all.append({"case": case, **q})

        idx0 = int(np.argmin(np.abs(l)))
        idx_repay = int(np.argmin(np.abs(np.abs(l) - 0.90)))
        idx_buffer = int(np.argmin(np.abs(np.abs(l) - 1.55)))
        for ti in np.linspace(0, len(t) - 1, 121).round().astype(int):
            digest_rows.append({
                "case": case,
                "t": float(t[ti]),
                "R_access_l0": float(d["R"][ti, idx0]),
                "rho_access_l0": float(d["rho"][ti, idx0]),
                "tidal_access_l0": float(d["tidal_ang"][ti, idx0]),
                "rate_access_l0": float(d["rate"][ti, idx0]),
                "rho_repay_rep_l": float(d["rho"][ti, idx_repay]),
                "rho_buffer_rep_l": float(d["rho"][ti, idx_buffer]),
            })

    pd.DataFrame(case_rows).to_csv(out / "multizone_case_summary.csv", index=False)
    pd.DataFrame(qi_rows_all).to_csv(out / "multizone_zone_qi_summary.csv", index=False)
    pd.DataFrame(digest_rows).to_csv(out / "multizone_time_digest.csv", index=False)

    summary = {
        "name": "multi-zone phase-cycled wormhole throat plant reduced evaluation",
        "scope": "wormhole component only; no transport/catch/passenger layer",
        "metric_proxy": "ds^2=-dt^2+dl^2+R(l,t)^2 dOmega^2",
        "zones": {
            "access_core": "|l| <= 0.25",
            "support_inner": "|l| <= 0.55",
            "repayment_band": "0.65 <= |l| <= 1.15",
            "buffer_band": "1.25 <= |l| <= 1.90",
            "outer_field": "2.10 <= |l| <= 3.20",
        },
        "high_level_result": (
            "Spatially separated side-band cycling can create positive repayment-like energy away from the core, "
            "but does not change the static QI obstruction seen by protected access observers. "
            "Core actuation can improve sampled-energy bookkeeping, but the improvement is purchased with access-core "
            "tidal/rate spikes or a collapsed quiet-open fraction."
        ),
        "interpretation": [
            "In this metric family, the flare-out/access core remains the bottleneck.",
            "Routing repayment away from the core is useful for reducing access exposure to repayment pulses, but it does not itself pay the local negative-energy support debt at the throat.",
            "The next model must either add more geometric freedom than one areal-radius field R(l,t), or treat this as evidence for a no-go within spherical areal-radius throat plants under the chosen proxy.",
        ],
        "constants": {
            "LP_M": LP_M,
            "C_LIGHT": C_LIGHT,
            "T_PLANCK_S": T_PLANCK_S,
            "C_QI": C_QI,
        },
    }
    (out / "multizone_model_summary.json").write_text(json.dumps(summary, indent=2))

    files = [
        "run_multizone_phase_cycled_throat_eval.py",
        "multizone_case_summary.csv",
        "multizone_zone_qi_summary.csv",
        "multizone_time_digest.csv",
        "multizone_model_summary.json",
    ]
    checksums = {}
    for name in files:
        fp = out / name
        if fp.exists():
            checksums[name] = hashlib.sha256(fp.read_bytes()).hexdigest()

    manifest = {
        "generated": "2026-05-12",
        "bundle": "multi-zone phase-cycled wormhole throat plant reduced evaluation",
        "scope": "wormhole/QEE component only",
        "files": files,
        "sha256": checksums,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
