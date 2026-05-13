#!/usr/bin/env python3
"""
Reduced radial ADM model for catch-rematched throat-supported shift-rail screens.

This is a lightweight causal/obstruction diagnostic. It is not a 3+1 constraint
solve, Einstein evolution, or semiclassical stress-tensor calculation.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Dict, Tuple
import math
import numpy as np

@dataclass(frozen=True)
class Params:
    V: float = 10.0
    v_exit: float = 0.5
    lam: float = 6.0
    C0: float = 20.0
    Cperp: float = 5.0
    B0: float = 6.0
    Rth: float = 1.25
    Rpass: float = 0.35
    w_th: float = 0.12
    w_pass: float = 0.08
    shoulder_center: float = 1.05
    shoulder_width: float = 0.35
    eta_N: float = 1.0
    x_catch: float = 0.05
    x_beta: float = 0.70
    x_q: float = 1.25
    w_catch: float = 0.25
    w_beta: float = 0.28
    w_q: float = 0.30
    p_beta: float = 4.0
    throat_gated: bool = True
    catch_enabled: bool = True
    late_catch: bool = False
    width_factor: float = 1.0

def _safe_tanh(x: float) -> float:
    if x > 40.0: return 1.0
    if x < -40.0: return -1.0
    return math.tanh(x)

def falloff(z: float, w: float) -> float:
    return 0.5 * (1.0 - _safe_tanh(z / max(w, 1e-12)))

def bump_sq(x2: float, R: float, w: float) -> float:
    z = (x2 - R * R) / max(2.0 * R * w, 1e-12)
    return 0.5 * (1.0 - _safe_tanh(z))

def effective_params(p: Params) -> Params:
    if p.late_catch:
        return replace(p, x_catch=p.x_beta)
    return p

def scalars(s: float, l: float, p: Params) -> Dict[str, float]:
    p = effective_params(p)
    wf = p.width_factor
    wc, wb, wq = p.w_catch * wf, p.w_beta * wf, p.w_q * wf
    wth, wpass = p.w_th * wf, p.w_pass * wf

    C = falloff(s - p.x_catch, wc) if p.catch_enabled else 1.0
    U = p.v_exit + (p.V - p.v_exit) * C
    E = falloff(s - p.x_beta, wb)
    q = falloff(s - p.x_q, wq)
    W = bump_sq(l * l, p.Rth, wth)
    S = bump_sq((l - s) * (l - s) + 1e-10, p.Rpass, wpass)
    A = math.exp(q * W * math.log(p.C0))
    T = math.exp(q * W * math.log(p.lam * p.C0))
    B = 1.0 + (p.B0 - 1.0) * W * q
    shoulder = math.exp(-((abs(l) - p.shoulder_center) / p.shoulder_width) ** 2)
    N = math.exp(p.eta_N * 0.18 * q * shoulder)
    Wfac = (W ** p.p_beta) if p.throat_gated else 1.0
    beta = -U * E * Wfac * S / B
    alpha = N * T
    sqrt_gll = B * A
    return {"C": C, "U": U, "E": E, "q": q, "W": W, "S": S, "A": A, "T": T, "B": B, "N": N, "beta": beta, "alpha": alpha, "sqrt_gll": sqrt_gll}

def metric_terms(s: float, l: float, p: Params) -> Tuple[float, float, float, float]:
    sc = scalars(s, l, p)
    alpha, sqrt_gll, beta = sc["alpha"], sc["sqrt_gll"], sc["beta"]
    gamma_ll = sqrt_gll * sqrt_gll
    gtt = -alpha * alpha + gamma_ll * beta * beta
    return alpha, sqrt_gll, beta, gtt

def null_speeds(s: float, l: float, p: Params) -> Tuple[float, float]:
    alpha, sqrt_gll, beta, _ = metric_terms(s, l, p)
    vp = -beta + alpha / sqrt_gll
    vm = -beta - alpha / sqrt_gll
    return vp, vm

def packet_norm(s: float, l: float, p: Params) -> float:
    sc = scalars(s, l, p)
    vcoord = sc["U"] / max(sc["B"], 1e-12)
    return -sc["alpha"] ** 2 + (sc["sqrt_gll"] * (vcoord + sc["beta"])) ** 2

def rk4_step(s: float, l: float, h: float, p: Params, family: str) -> float:
    idx = 0 if family == "outgoing" else 1
    def f(ss: float, ll: float) -> float:
        return null_speeds(ss, ll, p)[idx]
    k1 = f(s, l)
    k2 = f(s + 0.5*h, l + 0.5*h*k1)
    k3 = f(s + 0.5*h, l + 0.5*h*k2)
    k4 = f(s + h, l + h*k3)
    return l + h*(k1 + 2*k2 + 2*k3 + k4)/6.0

def integrate_ray(l0: float, p: Params, family: str, s0: float=-0.35, s1: float=3.0, ds: float=0.01):
    n = int(math.ceil((s1 - s0) / ds))
    s_vals = np.linspace(s0, s1, n+1)
    l_vals = np.empty(n+1)
    l = float(l0); l_vals[0]=l
    for i in range(n):
        h = float(s_vals[i+1] - s_vals[i])
        l = rk4_step(float(s_vals[i]), l, h, p, family)
        l_vals[i+1] = l
    return s_vals, l_vals

def summarize_bundle(p: Params, family: str, center_s: float, center_l: float, span: float=0.04, rays: int=7, s1: float=3.0, ds: float=0.01):
    l0s = np.linspace(center_l - span/2, center_l + span/2, rays)
    tracks = []
    s_vals = None
    for l0 in l0s:
        ss, ll = integrate_ray(float(l0), p, family, s0=center_s, s1=s1, ds=ds)
        s_vals = ss
        tracks.append(ll)
    L = np.vstack(tracks)
    span_t = L[-1,:] - L[0,:]
    inverted = bool(np.any(np.diff(L, axis=0) <= 0.0))
    min_abs_speed = float("inf")
    near_zero = 0
    total = 0
    for r in range(L.shape[0]):
        for ss, ll in zip(s_vals[::2], L[r,::2]):
            v = null_speeds(float(ss), float(ll), p)[0 if family=="outgoing" else 1]
            min_abs_speed = min(min_abs_speed, abs(float(v)))
            if abs(float(v)) < 1e-3:
                near_zero += 1
            total += 1
    return {
        "family": family,
        "center_s": float(center_s),
        "center_l": float(center_l),
        "start_span": float(span_t[0]),
        "min_span": float(np.min(span_t)),
        "final_span": float(span_t[-1]),
        "compression_ratio": float(np.min(span_t)/max(span_t[0],1e-12)),
        "inverted": inverted,
        "min_abs_null_speed": min_abs_speed,
        "near_zero_samples": near_zero,
        "sample_count": total,
        "near_zero_fraction": near_zero/max(total,1),
        "final_l_min": float(np.min(L[:,-1])),
        "final_l_max": float(np.max(L[:,-1])),
    }

def variant_params(name: str, width_factor: float=1.0) -> Params:
    if name == "active_rail":
        return Params(throat_gated=True, catch_enabled=True, late_catch=False, width_factor=width_factor)
    if name == "catch_independent_shift":
        return Params(throat_gated=False, catch_enabled=True, late_catch=False, width_factor=width_factor)
    if name == "naive_independent_no_catch":
        return Params(throat_gated=False, catch_enabled=False, late_catch=False, width_factor=width_factor)
    if name == "naive_throat_gated_no_catch":
        return Params(throat_gated=True, catch_enabled=False, late_catch=False, width_factor=width_factor)
    if name == "late_catch_throat_gated":
        return Params(throat_gated=True, catch_enabled=True, late_catch=True, width_factor=width_factor)
    raise ValueError(f"Unknown variant: {name}")

def dangerous_events(p: Params):
    p = effective_params(p)
    return {
        "leading_packet_edge_positive_support_edge": (p.Rth - p.Rpass, p.Rth),
        "trailing_packet_edge_positive_support_edge": (p.Rth + p.Rpass, p.Rth),
        "shift_fade_positive_support_edge": (p.x_beta, p.Rth),
        "throat_relax_positive_support_edge": (p.x_q, p.Rth),
        "packet_center_shift_fade": (p.x_beta, p.x_beta),
    }
