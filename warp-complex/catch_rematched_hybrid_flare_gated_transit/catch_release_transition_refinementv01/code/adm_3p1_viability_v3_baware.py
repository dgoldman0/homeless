#!/usr/bin/env python3
"""
ADM 3+1 viability diagnostics for the exact-v1 / catch-rematched throat-loaded composite design.

This script builds a single ADM slice or a small atlas of slices for the composite geometry

    ds^2 = -alpha^2 dt^2
           + gamma_ll (dl + beta^l dt)^2
           + gamma_thth dtheta^2
           + gamma_phph dphi^2

with

    alpha = N_v1(t,l) * T_pkt(l, X)
    gamma_ll = B_v1(t,l)^2 * A_parallel(l, X)^2
    gamma_thth = R_v1(t,l)^2 * A_perp(l, X)^2
    gamma_phph = gamma_thth * sin(theta)^2
    beta^l = -U(X) * E(X) * W(l)^p_beta * S(l-X)

It computes:
  - ADM fields: alpha, beta^i, gamma_ij
  - spatial Christoffels and 3-Ricci scalar
  - extrinsic curvature K_ij using K_ij = (D_i beta_j + D_j beta_i - d_t gamma_ij)/(2 alpha)
  - Hamiltonian source demand rho_H = (R3 + K^2 - K_ij K^ij)/(16 pi)
  - Momentum source demand j_M^i = D_j(K^ij - gamma^ij K)/(8 pi)
  - packet worldtube norm: -alpha^2 + gamma_ll (U + beta^l)^2
  - passive stationary-monitor g_tt = -alpha^2 + gamma_ll (beta^l)^2
  - support-edge diagnostics from the W transition band

The output is a JSON summary, an NPZ tensor archive, and a midplane CSV.

Recommended local command:

    python adm_3p1_viability.py --atlas --outdir adm_outputs --nl 81 --nth 33 --nph 8

A stronger single-slice run:

    python adm_3p1_viability.py --x0 0.25 --cycle-phase hold_mid --V 5 --lambda-factor 5.75 \
        --nl 121 --nth 49 --nph 12 --outdir adm_slice_V5

A high-stress single-slice run:

    python adm_3p1_viability.py --x0 0.25 --cycle-phase hold_mid --V 10 --lambda-factor 6 \
        --p-beta 4 --r-mode always_open --nl 121 --nth 49 --nph 12 --outdir adm_slice_V10_lam6
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np


# -----------------------------
# Smooth profiles and v1 geometry
# -----------------------------

def minjerk(x):
    x = np.clip(x, 0.0, 1.0)
    return 10.0*x**3 - 15.0*x**4 + 6.0*x**5


def pulse_smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return 16.0*x**2*(1.0-x)**2


def window_core(l, width, power=4):
    return np.exp(-(np.abs(l)/width)**power)


def window_shoulder(l, center=2.5, width=0.9, power=4):
    return np.exp(-((np.abs(l)-center)/width)**power)


def radius_access(l, a=1.0):
    return np.sqrt(a*a + l*l)


def falloff(z, w):
    return 0.5*(1.0 - np.tanh(z / max(w, 1e-12)))


@dataclass
class V1Params:
    B0: float = 8.0
    wB: float = 10.0
    T_B: float = 150.0
    T_R: float = 5.0
    T_H: float = 60.0
    T_C: float = 20.0
    T_Breset: float = 150.0
    Rc: float = 1.0
    wFlat: float = 1.6
    r_sh_amp: float = 0.0
    r_sh_center: float = 2.5
    r_sh_width: float = 1.2
    n_sh_amp: float = -0.18
    n_sh_center: float = 2.3
    n_sh_width: float = 1.0


@dataclass
class PacketParams:
    V: float = 5.0
    v_exit: float = 0.5
    lambda_factor: float = 5.75
    C0: float = 100.0
    C_perp: float = 1.0
    Rth: float = 0.75
    Rpass: float = 0.35
    wth: float = 0.05
    wpass: float = 0.05
    x_catch: float = 0.25
    x_beta: float = 0.70
    x_q: float = 1.25
    w_catch: float = 0.18
    w_beta: float = 0.20
    w_q: float = 0.20
    p_beta: float = 1.0
    p_capacity: float = 1.0
    packet_radius: float = 0.35


@dataclass
class GridParams:
    l_min: float = -2.4
    l_max: float = 2.4
    theta_min: float = 0.12
    theta_max: float = math.pi - 0.12
    phi_min: float = 0.0
    phi_max: float = 2.0*math.pi
    nl: int = 81
    nth: int = 33
    nph: int = 8


def v1_times(p: V1Params):
    t1 = p.T_B
    t2 = t1 + p.T_R
    t3 = t2 + p.T_H
    t4 = t3 + p.T_R
    t5 = t4 + p.T_C
    t6 = t5 + p.T_Breset
    return t1, t2, t3, t4, t5, t6


def cycle_time_from_phase(phase: str, p: V1Params) -> float:
    t1, t2, t3, t4, t5, t6 = v1_times(p)
    mapping = {
        "B_setup_mid": 0.5*t1,
        "pre_R_open": t1,
        "R_open_mid": 0.5*(t1+t2),
        "hold_start": t2,
        "hold_mid": 0.5*(t2+t3),
        "hold_end": t3,
        "R_close_mid": 0.5*(t3+t4),
        "comp_mid": 0.5*(t4+t5),
        "B_reset_mid": 0.5*(t5+t6),
    }
    if phase not in mapping:
        raise ValueError(f"unknown cycle phase {phase!r}; choose one of {sorted(mapping)}")
    return mapping[phase]


def A_sequence_scalar(t: float, p: V1Params):
    t1, t2, t3, t4, t5, t6 = v1_times(p)
    A_B = 0.0
    A_R = 0.0
    C = 0.0
    phase = "off"

    if 0.0 <= t < t1:
        A_B = float(minjerk(t/p.T_B))
        phase = "B_setup"
    elif t1 <= t < t5:
        A_B = 1.0
    elif t5 <= t <= t6:
        A_B = float(minjerk((t6-t)/p.T_Breset))
        phase = "B_reset"

    if t1 <= t < t2:
        A_R = float(minjerk((t-t1)/p.T_R))
        phase = "R_open"
    elif t2 <= t < t3:
        A_R = 1.0
        phase = "hold"
    elif t3 <= t < t4:
        A_R = float(minjerk((t4-t)/p.T_R))
        phase = "R_close"
    elif t4 <= t < t5:
        A_R = 0.0
        C = float(pulse_smooth((t-t4)/p.T_C))
        phase = "comp"

    return A_B, A_R, C, phase


def v1_controls(t: float, l: np.ndarray, p: V1Params, r_mode: str = "v1"):
    """
    Return N(l), B(l), R(l), and lifecycle scalars.
    r_mode modifies the R-flare actuator for testing:
      v1          : scheduled v1 R
      always_open : A_R = 1
      delayed_close : A_R = max(A_R, 1) during service-like slices; same as always_open for a single slice
      always_flat : A_R = 0
      half        : A_R = 0.5 * A_R
    """
    A_B, A_R, C, phase = A_sequence_scalar(t, p)

    if r_mode == "always_open":
        A_R_eff = 1.0
    elif r_mode == "delayed_close":
        A_R_eff = max(A_R, 1.0)
    elif r_mode == "always_flat":
        A_R_eff = 0.0
    elif r_mode == "half":
        A_R_eff = 0.5*A_R
    elif r_mode == "v1":
        A_R_eff = A_R
    else:
        raise ValueError("r_mode must be v1, always_open, delayed_close, always_flat, or half")

    F_B = window_core(l, p.wB)
    B = 1.0 + (p.B0 - 1.0)*A_B*F_B

    R_acc = radius_access(l)
    W_flat = window_core(l, p.wFlat)
    R_stand = R_acc + W_flat*(p.Rc - R_acc)
    H_R = window_shoulder(l, p.r_sh_center, p.r_sh_width)
    R = R_stand + A_R_eff*(R_acc - R_stand) + p.r_sh_amp*C*H_R

    H_N = window_shoulder(l, p.n_sh_center, p.n_sh_width)
    N = 1.0 + p.n_sh_amp*C*H_N

    return N, B, R, {"A_B": A_B, "A_R": A_R, "A_R_eff": A_R_eff, "C": C, "phase": phase}


# -----------------------------
# Packet profiles
# -----------------------------

def packet_state(X: float, pp: PacketParams):
    Ccatch = falloff(X - pp.x_catch, pp.w_catch)
    U = pp.v_exit + (pp.V - pp.v_exit)*Ccatch
    E = falloff(X - pp.x_beta, pp.w_beta)
    q = falloff(X - pp.x_q, pp.w_q)
    return float(U), float(E), float(q), float(Ccatch)


def bump_from_squared_radius(x2, R, w):
    z = (x2 - R*R)/(2.0*R*max(w, 1e-12))
    return 0.5*(1.0 - np.tanh(z))


def packet_profiles(l: np.ndarray, X: float, pp: PacketParams):
    U, E, q, Ccatch = packet_state(X, pp)
    W = bump_from_squared_radius(l*l, pp.Rth, pp.wth)
    S = bump_from_squared_radius((l-X)*(l-X), pp.Rpass, pp.wpass)

    A_par = np.exp(q*(W**pp.p_capacity)*np.log(pp.C0))
    A_perp = np.exp(q*(W**pp.p_capacity)*np.log(pp.C_perp))
    T_pkt = np.exp(q*(W**pp.p_capacity)*np.log(pp.lambda_factor * pp.C0))
    beta_l_up = -U*E*(W**pp.p_beta)*S

    return {
        "U": U,
        "E": E,
        "q": q,
        "Ccatch": Ccatch,
        "W": W,
        "S": S,
        "A_par": A_par,
        "A_perp": A_perp,
        "T_pkt": T_pkt,
        "beta_l_up": beta_l_up,
    }


# -----------------------------
# Grid and finite-difference helpers
# -----------------------------

def make_grid(gp: GridParams):
    l = np.linspace(gp.l_min, gp.l_max, gp.nl)
    th = np.linspace(gp.theta_min, gp.theta_max, gp.nth)
    # endpoint=False keeps periodic phi unique.
    ph = np.linspace(gp.phi_min, gp.phi_max, gp.nph, endpoint=False)
    return l, th, ph


def deriv_axis(arr: np.ndarray, coords: np.ndarray, axis: int, periodic: bool = False):
    """
    First derivative along a grid axis. Supports uniform grids.
    """
    if len(coords) < 3:
        return np.zeros_like(arr)

    h = float(coords[1] - coords[0])
    if periodic:
        return (np.roll(arr, -1, axis=axis) - np.roll(arr, 1, axis=axis)) / (2.0*h)

    return np.gradient(arr, h, axis=axis, edge_order=2)


def derivatives_scalar_or_tensor(arr: np.ndarray, coords: Tuple[np.ndarray, np.ndarray, np.ndarray]):
    l, th, ph = coords
    return np.stack([
        deriv_axis(arr, l, 0, periodic=False),
        deriv_axis(arr, th, 1, periodic=False),
        deriv_axis(arr, ph, 2, periodic=True),
    ], axis=0)


def safe_inv3(mat: np.ndarray):
    """
    Invert a field of 3x3 matrices with shape (...,3,3).
    """
    flat = mat.reshape((-1, 3, 3))
    inv = np.linalg.inv(flat)
    return inv.reshape(mat.shape)


# -----------------------------
# ADM fields
# -----------------------------

def build_fields(
    t_cycle: float,
    X: float,
    coords: Tuple[np.ndarray, np.ndarray, np.ndarray],
    v1p: V1Params,
    pp: PacketParams,
    r_mode: str = "v1",
):
    l, th, ph = coords
    L, TH, PH = np.meshgrid(l, th, ph, indexing="ij")
    sinth = np.sin(TH)

    N1, B1, R1, info = v1_controls(t_cycle, l, v1p, r_mode=r_mode)
    prof = packet_profiles(l, X, pp)

    alpha_l = N1 * prof["T_pkt"]
    gamma_ll_l = (B1*prof["A_par"])**2
    gamma_ang_l = (R1*prof["A_perp"])**2
    # Interpret packet U as proper-radial speed through the v1 B-stretched infrastructure.
    # Coordinate speed dX/dt is reduced by local B at the packet center.
    B_center = float(np.interp(X, l, B1))
    U_coord = prof["U"] / max(B_center, 1e-12)
    beta_l_up_l = -U_coord * prof["E"] * (prof["W"]**pp.p_beta) * prof["S"]

    shape = L.shape
    alpha = np.broadcast_to(alpha_l[:, None, None], shape).copy()
    beta_up = np.zeros(shape + (3,), dtype=float)
    beta_up[..., 0] = np.broadcast_to(beta_l_up_l[:, None, None], shape)

    gamma = np.zeros(shape + (3, 3), dtype=float)
    gamma[..., 0, 0] = np.broadcast_to(gamma_ll_l[:, None, None], shape)
    gamma[..., 1, 1] = np.broadcast_to(gamma_ang_l[:, None, None], shape)
    gamma[..., 2, 2] = np.broadcast_to((gamma_ang_l[:, None, None]) * sinth*sinth, shape)

    W = np.broadcast_to(prof["W"][:, None, None], shape).copy()
    S = np.broadcast_to(prof["S"][:, None, None], shape).copy()
    R_eff = np.broadcast_to((R1*prof["A_perp"])[:, None, None], shape).copy()

    return {
        "alpha": alpha,
        "beta_up": beta_up,
        "gamma": gamma,
        "W": W,
        "S": S,
        "R_eff": R_eff,
        "packet_U": U_coord,
        "packet_U_proper": prof["U"],
        "packet_E": prof["E"],
        "packet_q": prof["q"],
        "packet_Ccatch": prof["Ccatch"],
        "v1_info": info,
    }


def christoffel_3(gamma: np.ndarray, gamma_inv: np.ndarray, coords):
    """
    Spatial Christoffels Γ^i_{jk}; output shape grid+(3,3,3), indices [upper, lower, lower].
    """
    dg = derivatives_scalar_or_tensor(gamma, coords)  # [a, grid..., i, j]
    G = np.zeros(gamma.shape[:-2] + (3, 3, 3), dtype=float)

    for i in range(3):
        for j in range(3):
            for k in range(3):
                val = 0.0
                for m in range(3):
                    val = val + 0.5*gamma_inv[..., i, m]*(dg[j, ..., m, k] + dg[k, ..., m, j] - dg[m, ..., j, k])
                G[..., i, j, k] = val
    return G, dg


def spatial_ricci(gamma: np.ndarray, gamma_inv: np.ndarray, coords):
    Gamma, dg = christoffel_3(gamma, gamma_inv, coords)
    dGamma = derivatives_scalar_or_tensor(Gamma, coords)  # [a, grid..., upper, lower, lower]

    Ric = np.zeros(gamma.shape[:-2] + (3, 3), dtype=float)

    for i in range(3):
        for j in range(3):
            term1 = 0.0
            term2 = 0.0
            term3 = 0.0
            term4 = 0.0
            for k in range(3):
                term1 = term1 + dGamma[k, ..., k, i, j]
                term2 = term2 + dGamma[j, ..., k, i, k]
                for m in range(3):
                    term3 = term3 + Gamma[..., k, i, j]*Gamma[..., m, k, m]
                    term4 = term4 + Gamma[..., m, i, k]*Gamma[..., k, j, m]
            Ric[..., i, j] = term1 - term2 + term3 - term4

    R3 = np.einsum("...ij,...ij->...", gamma_inv, Ric)
    return Ric, R3, Gamma, dg


def extrinsic_curvature(
    gamma: np.ndarray,
    gamma_inv: np.ndarray,
    beta_up: np.ndarray,
    alpha: np.ndarray,
    Gamma: np.ndarray,
    dg: np.ndarray,
    gamma_t: np.ndarray,
    coords,
):
    beta_down = np.einsum("...ij,...j->...i", gamma, beta_up)
    dbeta_down = derivatives_scalar_or_tensor(beta_down, coords)  # [a, grid..., i]

    D_beta = np.zeros(gamma.shape[:-2] + (3, 3), dtype=float)
    for i in range(3):
        for j in range(3):
            val = dbeta_down[i, ..., j]
            for k in range(3):
                val = val - Gamma[..., k, i, j]*beta_down[..., k]
            D_beta[..., i, j] = val

    K = np.zeros_like(gamma)
    for i in range(3):
        for j in range(3):
            K[..., i, j] = (D_beta[..., i, j] + D_beta[..., j, i] - gamma_t[..., i, j])/(2.0*alpha)

    K_trace = np.einsum("...ij,...ij->...", gamma_inv, K)
    K_upup = np.einsum("...ia,...jb,...ab->...ij", gamma_inv, gamma_inv, K)
    KijKij = np.einsum("...ij,...ij->...", K, K_upup)
    return K, K_trace, K_upup, KijKij, beta_down


def time_derivative_gamma(
    t_cycle: float,
    X: float,
    dt: float,
    coords,
    v1p: V1Params,
    pp: PacketParams,
    r_mode: str,
):
    f0 = build_fields(t_cycle, X, coords, v1p, pp, r_mode)
    U0 = f0["packet_U"]
    f_plus = build_fields(t_cycle + dt, X + U0*dt, coords, v1p, pp, r_mode)
    f_minus = build_fields(t_cycle - dt, X - U0*dt, coords, v1p, pp, r_mode)
    return (f_plus["gamma"] - f_minus["gamma"])/(2.0*dt)


def momentum_source_demand(
    K_upup: np.ndarray,
    K_trace: np.ndarray,
    gamma_inv: np.ndarray,
    gamma: np.ndarray,
    Gamma: np.ndarray,
    coords,
):
    """
    j^i = D_j(K^ij - gamma^ij K)/(8 pi).
    D_j S^ij = ∂_j S^ij + Γ^i_jm S^mj + Γ^j_jm S^im
    """
    S_upup = K_upup - gamma_inv*K_trace[..., None, None]
    dS = derivatives_scalar_or_tensor(S_upup, coords)  # [a, grid..., i, j]

    div = np.zeros(gamma.shape[:-2] + (3,), dtype=float)
    for i in range(3):
        val = 0.0
        for j in range(3):
            val = val + dS[j, ..., i, j]
            for m in range(3):
                val = val + Gamma[..., i, j, m]*S_upup[..., m, j]
                val = val + Gamma[..., j, j, m]*S_upup[..., i, m]
        div[..., i] = val

    j_up = div/(8.0*math.pi)
    j_norm = np.sqrt(np.maximum(np.einsum("...ij,...i,...j->...", gamma, j_up, j_up), 0.0))
    return j_up, j_norm


# -----------------------------
# Diagnostics and output
# -----------------------------

def summarize_array(arr, mask=None):
    if mask is not None:
        vals = arr[mask]
    else:
        vals = arr.reshape(-1)
    vals = vals[np.isfinite(vals)]
    if vals.size == 0:
        return {"min": None, "max": None, "mean": None, "p95_abs": None, "max_abs": None}
    return {
        "min": float(np.min(vals)),
        "max": float(np.max(vals)),
        "mean": float(np.mean(vals)),
        "p95_abs": float(np.percentile(np.abs(vals), 95)),
        "max_abs": float(np.max(np.abs(vals))),
    }


def evaluate_slice(
    t_cycle: float,
    X: float,
    coords,
    v1p: V1Params,
    pp: PacketParams,
    r_mode: str,
    dt_time: float,
):
    fields = build_fields(t_cycle, X, coords, v1p, pp, r_mode)
    alpha = fields["alpha"]
    beta_up = fields["beta_up"]
    gamma = fields["gamma"]
    gamma_inv = safe_inv3(gamma)

    Ric3, R3, Gamma, dg = spatial_ricci(gamma, gamma_inv, coords)
    gamma_t = time_derivative_gamma(t_cycle, X, dt_time, coords, v1p, pp, r_mode)
    K, K_trace, K_upup, KijKij, beta_down = extrinsic_curvature(
        gamma, gamma_inv, beta_up, alpha, Gamma, dg, gamma_t, coords
    )

    rho_H = (R3 + K_trace*K_trace - KijKij)/(16.0*math.pi)
    j_up, j_norm = momentum_source_demand(K_upup, K_trace, gamma_inv, gamma, Gamma, coords)

    # Passenger and stationary monitors.
    U = fields["packet_U"]
    packet_norm = -alpha*alpha + gamma[..., 0, 0]*(U + beta_up[..., 0])**2
    gtt = -alpha*alpha + gamma[..., 0, 0]*(beta_up[..., 0])**2

    # Masks.
    l, th, ph = coords
    L, TH, PH = np.meshgrid(l, th, ph, indexing="ij")
    packet_mask = np.abs(L - X) <= pp.packet_radius
    edge_mask = (fields["W"] >= 0.05) & (fields["W"] <= 0.95)
    release_edge_mask = edge_mask & (fields["S"] >= 0.05)

    det_gamma = np.linalg.det(gamma.reshape((-1, 3, 3))).reshape(alpha.shape)
    eig_min = np.linalg.eigvalsh(gamma.reshape((-1, 3, 3))).reshape(alpha.shape + (3,))[..., 0]

    summary = {
        "t_cycle": float(t_cycle),
        "X": float(X),
        "r_mode": r_mode,
        "v1_info": fields["v1_info"],
        "packet": {
            "U": float(U),
            "E": float(fields["packet_E"]),
            "q": float(fields["packet_q"]),
            "Ccatch": float(fields["packet_Ccatch"]),
            "radius": float(pp.packet_radius),
        },
        "grid": {
            "nl": len(l),
            "nth": len(th),
            "nph": len(ph),
            "l_min": float(l[0]),
            "l_max": float(l[-1]),
            "theta_min": float(th[0]),
            "theta_max": float(th[-1]),
        },
        "global": {
            "alpha": summarize_array(alpha),
            "det_gamma": summarize_array(det_gamma),
            "min_eig_gamma": summarize_array(eig_min),
            "gtt": summarize_array(gtt),
            "packet_norm": summarize_array(packet_norm),
            "R3": summarize_array(R3),
            "K_trace": summarize_array(K_trace),
            "KijKij": summarize_array(KijKij),
            "rho_H": summarize_array(rho_H),
            "j_norm": summarize_array(j_norm),
        },
        "packet_region": {
            "point_count": int(np.sum(packet_mask)),
            "gtt": summarize_array(gtt, packet_mask),
            "packet_norm": summarize_array(packet_norm, packet_mask),
            "R3": summarize_array(R3, packet_mask),
            "K_trace": summarize_array(K_trace, packet_mask),
            "KijKij": summarize_array(KijKij, packet_mask),
            "rho_H": summarize_array(rho_H, packet_mask),
            "j_norm": summarize_array(j_norm, packet_mask),
            "fail_points_packet_norm_nonnegative": int(np.sum(packet_norm[packet_mask] >= 0.0)),
            "fail_points_gtt_nonnegative": int(np.sum(gtt[packet_mask] >= 0.0)),
        },
        "support_edge": {
            "point_count": int(np.sum(edge_mask)),
            "gtt": summarize_array(gtt, edge_mask),
            "R3": summarize_array(R3, edge_mask),
            "K_trace": summarize_array(K_trace, edge_mask),
            "KijKij": summarize_array(KijKij, edge_mask),
            "rho_H": summarize_array(rho_H, edge_mask),
            "j_norm": summarize_array(j_norm, edge_mask),
            "fail_points_gtt_nonnegative": int(np.sum(gtt[edge_mask] >= 0.0)),
        },
        "release_edge": {
            "point_count": int(np.sum(release_edge_mask)),
            "gtt": summarize_array(gtt, release_edge_mask),
            "packet_norm": summarize_array(packet_norm, release_edge_mask),
            "R3": summarize_array(R3, release_edge_mask),
            "rho_H": summarize_array(rho_H, release_edge_mask),
            "j_norm": summarize_array(j_norm, release_edge_mask),
            "fail_points_packet_norm_nonnegative": int(np.sum(packet_norm[release_edge_mask] >= 0.0)),
            "fail_points_gtt_nonnegative": int(np.sum(gtt[release_edge_mask] >= 0.0)),
        },
    }

    tensors = {
        "alpha": alpha,
        "beta_l": beta_up[..., 0],
        "gamma_ll": gamma[..., 0, 0],
        "gamma_thth": gamma[..., 1, 1],
        "gamma_phph": gamma[..., 2, 2],
        "gtt": gtt,
        "packet_norm": packet_norm,
        "R3": R3,
        "K_trace": K_trace,
        "KijKij": KijKij,
        "rho_H": rho_H,
        "j_norm": j_norm,
        "W": fields["W"],
        "S": fields["S"],
        "R_eff": fields["R_eff"],
        "det_gamma": det_gamma,
        "min_eig_gamma": eig_min,
    }

    return summary, tensors


def write_midplane_csv(path: Path, coords, tensors: Dict[str, np.ndarray]):
    l, th, ph = coords
    k_phi = 0
    rows = []
    for i, lv in enumerate(l):
        for j, tv in enumerate(th):
            row = {"l": float(lv), "theta": float(tv), "phi": float(ph[k_phi])}
            for name in [
                "alpha", "beta_l", "gamma_ll", "gamma_thth", "gamma_phph",
                "gtt", "packet_norm", "R3", "K_trace", "KijKij", "rho_H", "j_norm",
                "W", "S", "R_eff", "det_gamma", "min_eig_gamma",
            ]:
                row[name] = float(tensors[name][i, j, k_phi])
            rows.append(row)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def compact_status(summary: Dict):
    p = summary["packet_region"]
    e = summary["support_edge"]
    r = summary["release_edge"]
    return {
        "X": summary["X"],
        "r_mode": summary["r_mode"],
        "U": summary["packet"]["U"],
        "q": summary["packet"]["q"],
        "E": summary["packet"]["E"],
        "packet_max_norm": p["packet_norm"]["max"],
        "packet_fail_points": p["fail_points_packet_norm_nonnegative"],
        "packet_max_gtt": p["gtt"]["max"],
        "edge_max_gtt": e["gtt"]["max"],
        "edge_fail_points": e["fail_points_gtt_nonnegative"],
        "release_packet_max_norm": r["packet_norm"]["max"],
        "rho_H_packet_p95_abs": p["rho_H"]["p95_abs"],
        "j_packet_p95_abs": p["j_norm"]["p95_abs"],
        "rho_H_edge_p95_abs": e["rho_H"]["p95_abs"],
        "j_edge_p95_abs": e["j_norm"]["p95_abs"],
        "R3_packet_p95_abs": p["R3"]["p95_abs"],
        "K_packet_p95_abs": p["K_trace"]["p95_abs"],
    }


def run_single(args, outdir: Path, label: str):
    v1p = V1Params(
        B0=args.B0,
        wB=args.wB,
        T_B=args.T_B,
        T_R=args.T_R,
        T_H=args.T_H,
        T_C=args.T_C,
        T_Breset=args.T_Breset,
        n_sh_amp=args.n_sh_amp,
        n_sh_center=args.n_sh_center,
        n_sh_width=args.n_sh_width,
    )
    pp = PacketParams(
        V=args.V,
        v_exit=args.v_exit,
        lambda_factor=args.lambda_factor,
        C0=args.C0,
        C_perp=args.C_perp,
        Rth=args.Rth,
        Rpass=args.Rpass,
        wth=args.wth,
        wpass=args.wpass,
        x_catch=args.x_catch,
        x_beta=args.x_beta,
        x_q=args.x_q,
        w_catch=args.w_catch,
        w_beta=args.w_beta,
        w_q=args.w_q,
        p_beta=args.p_beta,
        p_capacity=args.p_capacity,
        packet_radius=args.packet_radius,
    )
    gp = GridParams(
        l_min=args.l_min,
        l_max=args.l_max,
        theta_min=args.theta_min,
        theta_max=args.theta_max,
        nl=args.nl,
        nth=args.nth,
        nph=args.nph,
    )
    coords = make_grid(gp)
    t_cycle = args.cycle_time if args.cycle_time is not None else cycle_time_from_phase(args.cycle_phase, v1p)

    summary, tensors = evaluate_slice(
        t_cycle=t_cycle,
        X=args.x0,
        coords=coords,
        v1p=v1p,
        pp=pp,
        r_mode=args.r_mode,
        dt_time=args.dt_time,
    )

    summary["parameters"] = {
        "v1": asdict(v1p),
        "packet": asdict(pp),
        "grid": asdict(gp),
        "dt_time": args.dt_time,
    }
    summary["compact_status"] = compact_status(summary)

    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / f"{label}_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    np.savez_compressed(
        outdir / f"{label}_tensors.npz",
        l=coords[0],
        theta=coords[1],
        phi=coords[2],
        **tensors,
    )
    write_midplane_csv(outdir / f"{label}_midplane.csv", coords, tensors)

    return summary


def run_atlas(args, outdir: Path):
    rows = []

    X_values = [float(x) for x in np.linspace(args.atlas_x_min, args.atlas_x_max, args.atlas_nx)]
    r_modes = args.atlas_r_modes.split(",")

    for r_mode in r_modes:
        r_mode = r_mode.strip()
        for X in X_values:
            local_args = argparse.Namespace(**vars(args))
            local_args.x0 = X
            local_args.r_mode = r_mode
            label = f"slice_X{X:+.3f}_{r_mode}".replace("+", "p").replace("-", "m").replace(".", "p")
            summary = run_single(local_args, outdir, label)
            row = compact_status(summary)
            row["label"] = label
            rows.append(row)
            print(json.dumps(row), flush=True)

    # Atlas CSV.
    fieldnames = list(rows[0].keys())
    with (outdir / "atlas_compact.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Atlas summary.
    atlas_summary = {
        "count": len(rows),
        "packet_fail_slices": int(sum(r["packet_fail_points"] > 0 for r in rows)),
        "edge_fail_slices": int(sum(r["edge_fail_points"] > 0 for r in rows)),
        "max_packet_norm": float(max(r["packet_max_norm"] for r in rows)),
        "max_edge_gtt": float(max(r["edge_max_gtt"] for r in rows)),
        "max_packet_rho_H_p95_abs": float(max(r["rho_H_packet_p95_abs"] for r in rows)),
        "max_edge_rho_H_p95_abs": float(max(r["rho_H_edge_p95_abs"] for r in rows)),
        "rows": rows,
    }
    with (outdir / "atlas_summary.json").open("w", encoding="utf-8") as f:
        json.dump(atlas_summary, f, indent=2)

    return atlas_summary


def parse_args():
    ap = argparse.ArgumentParser(description="ADM 3+1 viability diagnostics for exact-v1/catch-rematched composite geometry.")

    # Run mode.
    ap.add_argument("--outdir", default="adm_3p1_outputs")
    ap.add_argument("--atlas", action="store_true")
    ap.add_argument("--atlas-x-min", type=float, default=-0.35)
    ap.add_argument("--atlas-x-max", type=float, default=1.45)
    ap.add_argument("--atlas-nx", type=int, default=10)
    ap.add_argument("--atlas-r-modes", default="v1,always_open,delayed_close")

    # Slice selection.
    ap.add_argument("--x0", type=float, default=0.25)
    ap.add_argument("--cycle-phase", default="hold_mid")
    ap.add_argument("--cycle-time", type=float, default=None)
    ap.add_argument("--r-mode", default="v1", choices=["v1", "always_open", "delayed_close", "always_flat", "half"])
    ap.add_argument("--dt-time", type=float, default=1e-3)

    # Grid.
    ap.add_argument("--nl", type=int, default=81)
    ap.add_argument("--nth", type=int, default=33)
    ap.add_argument("--nph", type=int, default=8)
    ap.add_argument("--l-min", type=float, default=-2.4)
    ap.add_argument("--l-max", type=float, default=2.4)
    ap.add_argument("--theta-min", type=float, default=0.12)
    ap.add_argument("--theta-max", type=float, default=math.pi - 0.12)

    # v1 geometry.
    ap.add_argument("--B0", type=float, default=8.0)
    ap.add_argument("--wB", type=float, default=10.0)
    ap.add_argument("--T_B", type=float, default=150.0)
    ap.add_argument("--T_R", type=float, default=5.0)
    ap.add_argument("--T_H", type=float, default=60.0)
    ap.add_argument("--T_C", type=float, default=20.0)
    ap.add_argument("--T_Breset", type=float, default=150.0)
    ap.add_argument("--n-sh-amp", type=float, default=-0.18)
    ap.add_argument("--n-sh-center", type=float, default=2.3)
    ap.add_argument("--n-sh-width", type=float, default=1.0)

    # Packet.
    ap.add_argument("--V", type=float, default=5.0)
    ap.add_argument("--v-exit", type=float, default=0.5)
    ap.add_argument("--lambda-factor", type=float, default=5.75)
    ap.add_argument("--C0", type=float, default=100.0)
    ap.add_argument("--C-perp", type=float, default=1.0)
    ap.add_argument("--Rth", type=float, default=0.75)
    ap.add_argument("--Rpass", type=float, default=0.35)
    ap.add_argument("--wth", type=float, default=0.05)
    ap.add_argument("--wpass", type=float, default=0.05)
    ap.add_argument("--x-catch", type=float, default=0.25)
    ap.add_argument("--x-beta", type=float, default=0.70)
    ap.add_argument("--x-q", type=float, default=1.25)
    ap.add_argument("--w-catch", type=float, default=0.18)
    ap.add_argument("--w-beta", type=float, default=0.20)
    ap.add_argument("--w-q", type=float, default=0.20)
    ap.add_argument("--p-beta", type=float, default=1.0)
    ap.add_argument("--p-capacity", type=float, default=1.0)
    ap.add_argument("--packet-radius", type=float, default=0.35)

    return ap.parse_args()


def main():
    args = parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.atlas:
        summary = run_atlas(args, outdir)
        print("\nAtlas summary:")
        print(json.dumps(summary, indent=2))
    else:
        summary = run_single(args, outdir, "single")
        print(json.dumps(summary["compact_status"], indent=2))
        print(f"\nWrote outputs to: {outdir.resolve()}")


if __name__ == "__main__":
    main()
