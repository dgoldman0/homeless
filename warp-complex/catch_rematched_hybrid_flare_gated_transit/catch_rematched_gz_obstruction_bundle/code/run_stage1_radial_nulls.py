#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
from radial_model import integrate_ray, null_speeds, variant_params

def run_stage1(out_dir: Path) -> dict:
    variants = ["active_rail","catch_independent_shift","naive_independent_no_catch","naive_throat_gated_no_catch","late_catch_throat_gated"]
    families = ["outgoing","ingoing"]
    width_factors = [1.0,0.5,0.25,0.125]
    summaries = []
    for variant in variants:
        for wf in width_factors:
            p = variant_params(variant, width_factor=wf)
            for family in families:
                l0s = np.linspace(-1.8, 1.8, 51)
                tracks = []
                min_abs_speed = float("inf"); near_zero = 0; total = 0
                for l0 in l0s:
                    ss, ll = integrate_ray(float(l0), p, family, s0=-0.35, s1=3.0, ds=0.012)
                    tracks.append(ll)
                    for s_i, l_i in zip(ss[::3], ll[::3]):
                        v = null_speeds(float(s_i), float(l_i), p)[0 if family=="outgoing" else 1]
                        min_abs_speed = min(min_abs_speed, abs(float(v)))
                        near_zero += int(abs(float(v)) < 1e-3)
                        total += 1
                L = np.vstack(tracks)
                summaries.append({
                    "variant": variant, "width_factor": wf, "family": family,
                    "final_min": float(np.min(L[:,-1])), "final_max": float(np.max(L[:,-1])),
                    "order_inverted": bool(np.any(np.diff(L, axis=0) <= 0.0)),
                    "min_abs_null_speed": min_abs_speed,
                    "near_zero_samples": near_zero, "sample_count": total,
                    "near_zero_fraction": near_zero/max(total,1)
                })
    out = {"stage":"stage1_radial_null_characteristics","summaries":summaries}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir/"stage1_summary.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../data")
    args = ap.parse_args()
    run_stage1(Path(args.out))
if __name__ == "__main__":
    main()
