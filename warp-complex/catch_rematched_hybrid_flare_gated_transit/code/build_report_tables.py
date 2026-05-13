#!/usr/bin/env python3
"""Build compact report tables from the generated composite-gate JSON outputs.

Run from the bundle root:
    python code/build_report_tables.py

The script reads data/*.json and writes derived/report_metrics.json and
-derived/report_tables.md. The main report copies values from these derived
outputs.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DERIVED = ROOT / "derived"
DERIVED.mkdir(exist_ok=True)


def load_json(name: str) -> Any:
    with (DATA / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def fmt(x: Any, sig: int = 3) -> str:
    if x is None:
        return "none"
    if isinstance(x, str):
        return x
    if isinstance(x, int):
        return str(x)
    try:
        val = float(x)
    except Exception:
        return str(x)
    if abs(val) >= 1e4 or (abs(val) < 1e-3 and val != 0):
        return f"{val:.{sig}g}"
    return f"{val:.{sig}g}"


def row_for_label(rows: list[dict[str, Any]], label: str, V: float, lam: float) -> dict[str, Any]:
    for r in rows:
        if r.get("label") == label and abs(float(r.get("V")) - V) < 1e-9 and abs(float(r.get("lam")) - lam) < 1e-9:
            return r
    raise KeyError((label, V, lam))


def main() -> None:
    detailed = load_json("composite_gate_detailed_diagnostics.json")
    rflare = load_json("composite_r_flare_gate_tests.json")
    extra = load_json("composite_extra_slim_and_edge_tests.json")

    metrics: dict[str, Any] = {}
    metrics["catch_threshold_summary"] = detailed["catch_threshold_summary"]

    # Gate classification source rows.
    metrics["selected_failure_states"] = [
        r for r in detailed["stress_cases_detailed"]
        if r["case"] in {"baseline", "no_hold", "edge_reinforced_p2", "late_catch_after_shift", "late_catch_after_relax"}
    ]
    metrics["ablation_results"] = detailed["ablation_results"]

    # R-flare highlights.
    r_highlights = []
    for V, lam in [(2.5, 2.875), (5, 3), (5, 5.75), (10, 6), (10, 11.5)]:
        for label in ["baseline_R_fades_with_q", "R_always_open", "R_always_flat", "R_sharp_release", "R_slow_release", "R_always_open_no_quiet_hold", "R_flat_no_quiet_hold"]:
            try:
                r = row_for_label(rflare, label, V, lam)
            except KeyError:
                continue
            r_highlights.append({
                "V": V,
                "lambda": lam,
                "label": label,
                "hard_packet_fail": r["hard_packet_fail"],
                "passive_gtt_fail": r["passive_gtt_fail"],
                "packet_max_norm": r["packet_max_norm"],
                "edge_max_gtt": r["edge_max_gtt"],
                "throat_min_d2_Reff2_min": r["throat_min_d2_Reff2_min"],
                "packet_boundary_angular_tidal_ratio": r["packet_boundary_maxabs_tidal_angular_ratio_to_base"],
                "support_edge_theta_ratio": r["support_edge_max_theta_prod_ratio_to_base"],
            })
    metrics["r_flare_highlights"] = r_highlights

    # Extra slim and p_beta highlights.
    extra_highlights = []
    for V, lam in [(5, 3), (5, 5.75), (10, 6), (10, 11.5)]:
        for label in ["slim_short_hold_Ropen_halfB_halfN", "very_slim_nohold_Ropen_noB_noN", "very_slim_plus_pbeta2", "baseline_plus_pbeta2", "latecatch_at_beta_pbeta_1", "latecatch_at_beta_pbeta_2", "latecatch_at_beta_pbeta_4"]:
            try:
                r = row_for_label(extra, label, V, lam)
            except KeyError:
                continue
            extra_highlights.append({
                "V": V,
                "lambda": lam,
                "label": label,
                "hard_packet_fail": r["hard_packet_fail"],
                "passive_gtt_fail": r["passive_gtt_fail"],
                "packet_max_norm": r["packet_max_norm"],
                "edge_max_gtt": r["edge_max_gtt"],
                "packet_boundary_angular_tidal_ratio": r["packet_boundary_maxabs_tidal_angular_ratio_to_base"],
                "support_edge_angular_tidal_ratio": r["support_edge_maxabs_tidal_angular_ratio_to_base"],
                "support_edge_theta_ratio": r["support_edge_max_theta_prod_ratio_to_base"],
            })
    metrics["extra_highlights"] = extra_highlights

    with (DERIVED / "report_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    lines: list[str] = []
    lines.append("# Derived report tables\n")
    lines.append("Generated from the JSON files in `data/` by `code/build_report_tables.py`.\n")

    lines.append("\n## Catch timing thresholds\n")
    lines.append("| V | lambda | first packet fail x_catch | delta vs beta | first packet gtt fail x_catch | first edge gtt fail x_catch |\n")
    lines.append("|---:|---:|---:|---:|---:|---:|\n")
    for r in metrics["catch_threshold_summary"]:
        lines.append(
            f"| {fmt(r['V'])} | {fmt(r['lam'])} | {fmt(r['first_packet_norm_fail_xcatch'])} | {fmt(r['first_packet_norm_fail_delta_beta'])} | {fmt(r['first_packet_gtt_fail_xcatch'])} | {fmt(r['first_edge_gtt_fail_xcatch'])} |\n"
        )

    lines.append("\n## R-flare highlights\n")
    lines.append("| V | lambda | variant | packet fail | passive gtt fail | packet max norm | min flare d2 | packet angular tidal x base | edge theta x base |\n")
    lines.append("|---:|---:|---|---:|---:|---:|---:|---:|---:|\n")
    for r in r_highlights:
        lines.append(
            f"| {fmt(r['V'])} | {fmt(r['lambda'])} | {r['label']} | {r['hard_packet_fail']} | {r['passive_gtt_fail']} | {fmt(r['packet_max_norm'])} | {fmt(r['throat_min_d2_Reff2_min'])} | {fmt(r['packet_boundary_angular_tidal_ratio'])} | {fmt(r['support_edge_theta_ratio'])} |\n"
        )

    lines.append("\n## Slim and edge-gating highlights\n")
    lines.append("| V | lambda | variant | packet fail | passive gtt fail | packet max norm | packet angular tidal x base | edge angular tidal x base | edge theta x base |\n")
    lines.append("|---:|---:|---|---:|---:|---:|---:|---:|---:|\n")
    for r in extra_highlights:
        lines.append(
            f"| {fmt(r['V'])} | {fmt(r['lambda'])} | {r['label']} | {r['hard_packet_fail']} | {r['passive_gtt_fail']} | {fmt(r['packet_max_norm'])} | {fmt(r['packet_boundary_angular_tidal_ratio'])} | {fmt(r['support_edge_angular_tidal_ratio'])} | {fmt(r['support_edge_theta_ratio'])} |\n"
        )

    (DERIVED / "report_tables.md").write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
