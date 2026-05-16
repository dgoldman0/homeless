#!/usr/bin/env python3
"""
active_rail_lifecycle_quarantine.py

Purpose
-------
Build a lifecycle-resolved source ledger for the active-rail source analysis.

This script is designed for the repo state where:
1. the freeze report bundle exists,
2. the compact freeze diagnostic may only regenerate summary tables,
3. the full exploratory tensor evaluator may or may not be committed.

It does three things:

1. Looks for point-level source-ledger outputs.
2. If point-level outputs exist, computes lifecycle / packet-exposure ledgers.
3. If only summary CSVs exist, produces a transparent fallback report and names
   exactly what evaluator/output is missing.

This is NOT a matter model, not a constraint solve, and not an RSET calculation.
It is a postprocessor for prescribed-geometry demanded-source ledgers.

Run from repo root:

    python warp-complex/active_rail_source_analysis/active_rail_lifecycle_quarantine.py

Optional:

    python warp-complex/active_rail_source_analysis/active_rail_lifecycle_quarantine.py \
        --data-dir warp-complex/active_rail_source_analysis/active_rail_source_analysis_freeze_report/data \
        --out-dir warp-complex/active_rail_source_analysis/lifecycle_quarantine_report

Expected point-level columns
----------------------------
A usable point-level source ledger should contain at least:

    s, l
    rho_euler
    Tkk_plus or Tkk_minus or Tkk_min_radial
    p_l_unit
    p_omega_unit
    j_l_unit
    packet_norm

Helpful columns if present:

    volume_density
    region
    phase
    W, S, q, E, U

If the committed repo does not contain such a point-level CSV, this script will
still summarize the available freeze CSVs but will report that lifecycle
quarantine analysis cannot be completed without the missing evaluator/output.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

DEFAULT_DATA_DIR = Path(
    "warp-complex/active_rail_source_analysis/"
    "active_rail_source_analysis_freeze_report/data"
)

DEFAULT_OUT_DIR = Path(
    "warp-complex/active_rail_source_analysis/"
    "active_rail_lifecycle_quarantine_report"
)

POINT_FILE_CANDIDATES = [
    "source_quarantine_points.csv",
    "source_ledger_points.csv",
    "freeze_source_points.csv",
    "active_rail_source_points.csv",
    "source_ledger_active_rail_catch_throat_gated_w1_static_throat_points.csv",
    "source_ledger_active_rail_catch_throat_gated_w1_area_capacity_A2_points.csv",
    "source_ledger_active_rail_catch_throat_gated_w1_area_capacity_B2_points.csv",
]

SUMMARY_FILE_CANDIDATES = [
    "global_case_metrics.csv",
    "baseline_subtracted_active_excess_summary.csv",
    "source_quarantine_summary.csv",
    "source_quarantine_packet_peak_comparison.csv",
    "unfreeze_refined_sweep.csv",
    "unfreeze_refined_aggregate.csv",
]


@dataclass(frozen=True)
class LifecycleParams:
    """
    These should match the active-rail diagnostic unless overridden.

    x_catch, x_beta, x_q are service centers.
    w_catch, w_beta, w_q are transition widths.
    Rpass is the packet half-width/radius in the reduced radial screen.
    Rth is the nominal support throat radius.
    """

    Rpass: float = 0.35
    Rth: float = 1.25

    x_catch: float = 0.15
    x_beta: float = 0.70
    x_q: float = 1.25

    w_catch: float = 0.16
    w_beta: float = 0.18
    w_q: float = 0.18

    # Conservative live-packet cutoff:
    # passenger packet is counted as live through shift-fade safety margin,
    # but not through reset/decompression unless explicitly requested.
    live_packet_end_margin_widths: float = 2.0

    # If true, count the geometric packet mask through all phases.
    # If false, use the lifecycle live-packet mask.
    count_reset_as_packet_exposure: bool = False


CHANNELS = {
    "neg_rho": {
        "kind": "negative",
        "columns": ["rho_euler", "rho", "energy_density"],
        "description": "negative Eulerian energy density",
    },
    "neg_Tkk": {
        "kind": "negative_min",
        "columns": ["Tkk_min_radial", "Tkk_plus", "Tkk_minus"],
        "description": "negative radial null contraction",
    },
    "abs_p_l": {
        "kind": "absolute",
        "columns": ["p_l_unit", "p_l", "radial_pressure"],
        "description": "radial pressure magnitude",
    },
    "abs_pOmega": {
        "kind": "absolute",
        "columns": ["p_omega_unit", "pOmega", "p_omega", "angular_pressure"],
        "description": "angular pressure magnitude",
    },
    "abs_j_l": {
        "kind": "absolute",
        "columns": ["j_l_unit", "j_l", "radial_current"],
        "description": "radial current magnitude",
    },
}


# ---------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------

def read_csv_if_exists(path: Path) -> Optional[pd.DataFrame]:
    if path.exists():
        return pd.read_csv(path)
    return None


def find_first_existing(data_dir: Path, names: Iterable[str]) -> Optional[Path]:
    for name in names:
        p = data_dir / name
        if p.exists():
            return p
    return None


def find_point_file(data_dir: Path) -> Optional[Path]:
    direct = find_first_existing(data_dir, POINT_FILE_CANDIDATES)
    if direct:
        return direct

    # Fallback: search recursively for likely point-level CSV.
    candidates = []
    for p in data_dir.rglob("*.csv"):
        name = p.name.lower()
        if "point" in name and ("source" in name or "ledger" in name or "quarantine" in name):
            candidates.append(p)

    candidates.sort(key=lambda x: (len(str(x)), str(x)))
    return candidates[0] if candidates else None


def load_available_summaries(data_dir: Path) -> Dict[str, pd.DataFrame]:
    out: Dict[str, pd.DataFrame] = {}
    for name in SUMMARY_FILE_CANDIDATES:
        p = data_dir / name
        if p.exists():
            out[name] = pd.read_csv(p)

    # Also search subdirectories for known summary names.
    for p in data_dir.rglob("*.csv"):
        if p.name in out:
            continue
        lname = p.name.lower()
        if "summary" in lname or "metrics" in lname or "aggregate" in lname:
            try:
                out[str(p.relative_to(data_dir))] = pd.read_csv(p)
            except Exception:
                pass

    return out


# ---------------------------------------------------------------------
# Lifecycle masks
# ---------------------------------------------------------------------

def phase_name(s: float, p: LifecycleParams) -> str:
    if s < p.x_catch - 2.0 * p.w_catch:
        return "pre_catch_support"

    if abs(s - p.x_catch) <= 2.0 * p.w_catch:
        return "catch_rematch"

    if p.x_catch + 2.0 * p.w_catch < s < p.x_beta - 2.0 * p.w_beta:
        return "held_transport"

    if abs(s - p.x_beta) <= 2.0 * p.w_beta:
        return "shift_fade"

    if p.x_beta + 2.0 * p.w_beta < s < p.x_q - 2.0 * p.w_q:
        return "post_shift_pre_relax"

    if abs(s - p.x_q) <= 2.0 * p.w_q:
        return "decompression_reset"

    return "reset_tail"


def region_name(l: float, p: LifecycleParams) -> str:
    al = abs(l)
    if al <= 0.65 * p.Rth:
        return "core_throat"
    if al <= 1.20 * p.Rth:
        return "support_edge"
    if al <= 1.85 * p.Rth:
        return "outer_shoulder"
    return "exterior_tail"


def add_lifecycle_columns(df: pd.DataFrame, p: LifecycleParams) -> pd.DataFrame:
    df = df.copy()

    if "s" not in df.columns or "l" not in df.columns:
        raise ValueError("Point-level ledger must contain columns 's' and 'l'.")

    df["phase_lifecycle"] = df["s"].astype(float).map(lambda x: phase_name(x, p))
    df["region_lifecycle"] = df["l"].astype(float).map(lambda x: region_name(x, p))

    df["inside_packet_geom"] = (df["l"].astype(float) - df["s"].astype(float)).abs() <= p.Rpass

    live_end = p.x_beta + p.live_packet_end_margin_widths * p.w_beta
    df["inside_packet_live"] = df["inside_packet_geom"] & (df["s"].astype(float) <= live_end)

    if p.count_reset_as_packet_exposure:
        df["inside_packet_accounting"] = df["inside_packet_geom"]
    else:
        df["inside_packet_accounting"] = df["inside_packet_live"]

    if "volume_density" not in df.columns:
        df["volume_density"] = 1.0

    return df


# ---------------------------------------------------------------------
# Channel badness
# ---------------------------------------------------------------------

def resolve_channel_column(df: pd.DataFrame, channel: str) -> Tuple[str, np.ndarray]:
    spec = CHANNELS[channel]
    cols = [c for c in spec["columns"] if c in df.columns]

    if not cols:
        raise ValueError(
            f"Cannot resolve channel {channel!r}. "
            f"Expected one of columns {spec['columns']}; got {list(df.columns)}"
        )

    kind = spec["kind"]

    if kind == "negative_min":
        # For Tkk, if plus/minus are both present, use the more negative radial null channel.
        if "Tkk_min_radial" in df.columns:
            arr = df["Tkk_min_radial"].astype(float).to_numpy()
            return "Tkk_min_radial", arr

        arrays = [df[c].astype(float).to_numpy() for c in cols]
        arr = np.nanmin(np.vstack(arrays), axis=0)
        return "+".join(cols), arr

    col = cols[0]
    arr = df[col].astype(float).to_numpy()
    return col, arr


def badness_values(values: np.ndarray, channel: str) -> np.ndarray:
    kind = CHANNELS[channel]["kind"]

    if kind in ("negative", "negative_min"):
        return np.maximum(-values, 0.0)

    if kind == "absolute":
        return np.abs(values)

    raise ValueError(f"Unknown channel kind: {kind}")


def safe_fraction(numer: float, denom: float) -> float:
    if denom <= 0 or not math.isfinite(denom):
        return float("nan")
    return numer / denom


# ---------------------------------------------------------------------
# Ledger computation
# ---------------------------------------------------------------------

def summarize_by_group(df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
    rows = []

    for group_key, g in df.groupby(group_cols, dropna=False):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)

        row = {col: val for col, val in zip(group_cols, group_key)}
        row["points"] = len(g)

        volume = g["volume_density"].astype(float).to_numpy()

        for channel in CHANNELS:
            source_col, values = resolve_channel_column(g, channel)
            bad = badness_values(values, channel)
            burden = bad * volume

            packet_geom = g["inside_packet_geom"].to_numpy(dtype=bool)
            packet_live = g["inside_packet_live"].to_numpy(dtype=bool)
            packet_accounting = g["inside_packet_accounting"].to_numpy(dtype=bool)

            total = float(np.nansum(burden))
            geom = float(np.nansum(burden[packet_geom]))
            live = float(np.nansum(burden[packet_live]))
            acct = float(np.nansum(burden[packet_accounting]))

            row[f"{channel}_source_column"] = source_col
            row[f"{channel}_point_peak"] = float(np.nanmax(bad)) if bad.size else float("nan")
            row[f"{channel}_total_burden"] = total
            row[f"{channel}_packet_geom_burden"] = geom
            row[f"{channel}_packet_live_burden"] = live
            row[f"{channel}_packet_accounting_burden"] = acct
            row[f"{channel}_packet_geom_fraction"] = safe_fraction(geom, total)
            row[f"{channel}_packet_live_fraction"] = safe_fraction(live, total)
            row[f"{channel}_packet_accounting_fraction"] = safe_fraction(acct, total)

        if "packet_norm" in g.columns:
            row["packet_positive_live_points"] = int(
                ((g["packet_norm"].astype(float) > 0) & g["inside_packet_live"]).sum()
            )
            row["max_packet_norm_live"] = float(
                g.loc[g["inside_packet_live"], "packet_norm"].astype(float).max()
            ) if g["inside_packet_live"].any() else float("nan")

        rows.append(row)

    return pd.DataFrame(rows)


def top_bad_points(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    rows = []

    volume = df["volume_density"].astype(float).to_numpy()

    for channel in CHANNELS:
        source_col, values = resolve_channel_column(df, channel)
        bad = badness_values(values, channel)
        burden = bad * volume

        order = np.argsort(-burden)
        for rank, idx in enumerate(order[:top_n], start=1):
            rows.append({
                "channel": channel,
                "description": CHANNELS[channel]["description"],
                "source_column": source_col,
                "rank": rank,
                "s": float(df.iloc[idx]["s"]),
                "l": float(df.iloc[idx]["l"]),
                "phase": df.iloc[idx]["phase_lifecycle"],
                "region": df.iloc[idx]["region_lifecycle"],
                "inside_packet_geom": bool(df.iloc[idx]["inside_packet_geom"]),
                "inside_packet_live": bool(df.iloc[idx]["inside_packet_live"]),
                "badness_point_value": float(bad[idx]),
                "volume_density": float(volume[idx]),
                "volume_weighted_burden": float(burden[idx]),
            })

    return pd.DataFrame(rows)


def packet_peak_comparison(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    geom = df["inside_packet_geom"].to_numpy(dtype=bool)
    live = df["inside_packet_live"].to_numpy(dtype=bool)

    for channel in CHANNELS:
        source_col, values = resolve_channel_column(df, channel)
        bad = badness_values(values, channel)

        peak_total = float(np.nanmax(bad))
        peak_geom = float(np.nanmax(bad[geom])) if geom.any() else float("nan")
        peak_live = float(np.nanmax(bad[live])) if live.any() else float("nan")

        rows.append({
            "channel": channel,
            "description": CHANNELS[channel]["description"],
            "source_column": source_col,
            "peak_total": peak_total,
            "peak_inside_geometric_packet": peak_geom,
            "peak_inside_live_packet": peak_live,
            "live_over_total_peak": safe_fraction(peak_live, peak_total),
            "geometric_over_total_peak": safe_fraction(peak_geom, peak_total),
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------
# Fallback summary mode
# ---------------------------------------------------------------------

def write_fallback_report(
    data_dir: Path,
    out_dir: Path,
    summaries: Dict[str, pd.DataFrame],
    point_file: Optional[Path],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("# Active Rail Lifecycle Quarantine Fallback Report")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("No committed point-level source ledger was found.")
    lines.append("")
    lines.append("Lifecycle/quarantine analysis requires source values by `(s, l)` grid point.")
    lines.append("The committed compact freeze diagnostic appears to preserve or regenerate summary")
    lines.append("tables, but not the full tensor-evaluator point ledger.")
    lines.append("")
    lines.append("## Data directory checked")
    lines.append("")
    lines.append(f"`{data_dir}`")
    lines.append("")
    lines.append("## Point-level file search")
    lines.append("")
    lines.append(f"Point file found: `{point_file}`" if point_file else "Point file found: **none**")
    lines.append("")
    lines.append("## Available summary CSVs")
    lines.append("")

    if not summaries:
        lines.append("No summary CSVs were found either.")
    else:
        for name, df in summaries.items():
            lines.append(f"### `{name}`")
            lines.append("")
            lines.append(f"Shape: `{df.shape[0]} rows x {df.shape[1]} columns`")
            lines.append("")
            lines.append("Columns:")
            lines.append("")
            lines.append(", ".join(f"`{c}`" for c in df.columns))
            lines.append("")

    lines.append("## Missing evaluator/output")
    lines.append("")
    lines.append("To run the full lifecycle analysis, commit either:")
    lines.append("")
    lines.append("1. a point-level source CSV with columns:")
    lines.append("")
    lines.append("   `s, l, rho_euler, Tkk_plus/Tkk_minus or Tkk_min_radial, p_l_unit, p_omega_unit, j_l_unit, packet_norm`")
    lines.append("")
    lines.append("or")
    lines.append("")
    lines.append("2. a full tensor evaluator that can regenerate that CSV for the freeze candidate and unfreeze candidates.")
    lines.append("")
    lines.append("The lifecycle postprocessor can then compute:")
    lines.append("")
    lines.append("- packet overlap fractions by source channel,")
    lines.append("- live packet exposure only through catch/carry/fade,")
    lines.append("- top bad source points by phase and region,")
    lines.append("- packet peak fractions,")
    lines.append("- reset/decompression exposure separated from passenger exposure.")
    lines.append("")

    (out_dir / "FALLBACK_MISSING_POINT_LEDGER.md").write_text("\n".join(lines), encoding="utf-8")

    manifest = {
        "status": "fallback_missing_point_ledger",
        "data_dir": str(data_dir),
        "point_file": str(point_file) if point_file else None,
        "available_summaries": {
            name: {"rows": int(df.shape[0]), "columns": list(df.columns)}
            for name, df in summaries.items()
        },
    }

    (out_dir / "fallback_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------

def run_lifecycle_analysis(
    data_dir: Path,
    out_dir: Path,
    params: LifecycleParams,
    top_n: int,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    point_file = find_point_file(data_dir)
    summaries = load_available_summaries(data_dir)

    if point_file is None:
        write_fallback_report(data_dir, out_dir, summaries, point_file)
        print(f"[fallback] No point-level source ledger found. Wrote {out_dir}")
        return

    df = pd.read_csv(point_file)
    df = add_lifecycle_columns(df, params)

    # Write normalized point ledger with lifecycle columns.
    df.to_csv(out_dir / "lifecycle_points_with_masks.csv", index=False)

    global_summary = summarize_by_group(df, [])
    # summarize_by_group cannot group by [] in older pandas reliably, so handle directly.
    global_summary = summarize_global(df)
    global_summary.to_csv(out_dir / "lifecycle_global_summary.csv", index=False)

    phase_summary = summarize_by_group(df, ["phase_lifecycle"])
    phase_summary.to_csv(out_dir / "lifecycle_by_phase_summary.csv", index=False)

    region_summary = summarize_by_group(df, ["region_lifecycle"])
    region_summary.to_csv(out_dir / "lifecycle_by_region_summary.csv", index=False)

    phase_region_summary = summarize_by_group(df, ["phase_lifecycle", "region_lifecycle"])
    phase_region_summary.to_csv(out_dir / "lifecycle_by_phase_region_summary.csv", index=False)

    top_points = top_bad_points(df, top_n=top_n)
    top_points.to_csv(out_dir / "lifecycle_top_bad_points.csv", index=False)

    peaks = packet_peak_comparison(df)
    peaks.to_csv(out_dir / "lifecycle_packet_peak_comparison.csv", index=False)

    report = build_markdown_report(
        point_file=point_file,
        df=df,
        global_summary=global_summary,
        phase_summary=phase_summary,
        region_summary=region_summary,
        peaks=peaks,
        params=params,
    )
    (out_dir / "LIFECYCLE_QUARANTINE_REPORT.md").write_text(report, encoding="utf-8")

    manifest = {
        "status": "ok",
        "point_file": str(point_file),
        "params": asdict(params),
        "rows": int(df.shape[0]),
        "columns": list(df.columns),
        "outputs": sorted(p.name for p in out_dir.iterdir()),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"[ok] Wrote lifecycle quarantine report to {out_dir}")


def summarize_global(df: pd.DataFrame) -> pd.DataFrame:
    row = {"scope": "global", "points": len(df)}
    volume = df["volume_density"].astype(float).to_numpy()

    for channel in CHANNELS:
        source_col, values = resolve_channel_column(df, channel)
        bad = badness_values(values, channel)
        burden = bad * volume

        geom = df["inside_packet_geom"].to_numpy(dtype=bool)
        live = df["inside_packet_live"].to_numpy(dtype=bool)
        acct = df["inside_packet_accounting"].to_numpy(dtype=bool)

        total = float(np.nansum(burden))
        geom_b = float(np.nansum(burden[geom]))
        live_b = float(np.nansum(burden[live]))
        acct_b = float(np.nansum(burden[acct]))

        row[f"{channel}_source_column"] = source_col
        row[f"{channel}_point_peak"] = float(np.nanmax(bad)) if bad.size else float("nan")
        row[f"{channel}_total_burden"] = total
        row[f"{channel}_packet_geom_burden"] = geom_b
        row[f"{channel}_packet_live_burden"] = live_b
        row[f"{channel}_packet_accounting_burden"] = acct_b
        row[f"{channel}_packet_geom_fraction"] = safe_fraction(geom_b, total)
        row[f"{channel}_packet_live_fraction"] = safe_fraction(live_b, total)
        row[f"{channel}_packet_accounting_fraction"] = safe_fraction(acct_b, total)

    if "packet_norm" in df.columns:
        live = df["inside_packet_live"].to_numpy(dtype=bool)
        row["packet_positive_live_points"] = int(
            ((df["packet_norm"].astype(float).to_numpy() > 0) & live).sum()
        )
        row["max_packet_norm_live"] = float(
            df.loc[df["inside_packet_live"], "packet_norm"].astype(float).max()
        ) if df["inside_packet_live"].any() else float("nan")

    return pd.DataFrame([row])


def fmt_pct(x: float) -> str:
    if not math.isfinite(x):
        return "nan"
    return f"{100.0 * x:.1f}%"


def build_markdown_report(
    point_file: Path,
    df: pd.DataFrame,
    global_summary: pd.DataFrame,
    phase_summary: pd.DataFrame,
    region_summary: pd.DataFrame,
    peaks: pd.DataFrame,
    params: LifecycleParams,
) -> str:
    g = global_summary.iloc[0]

    rows = []
    for channel in CHANNELS:
        rows.append({
            "channel": channel,
            "description": CHANNELS[channel]["description"],
            "point_peak": g.get(f"{channel}_point_peak", float("nan")),
            "live_packet_fraction": fmt_pct(g.get(f"{channel}_packet_live_fraction", float("nan"))),
            "geometric_packet_fraction": fmt_pct(g.get(f"{channel}_packet_geom_fraction", float("nan"))),
        })

    compact = pd.DataFrame(rows)

    lines = []
    lines.append("# Lifecycle Quarantine Report")
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append(f"Point-level input: `{point_file}`")
    lines.append("")
    lines.append("## Lifecycle settings")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(asdict(params), indent=2))
    lines.append("```")
    lines.append("")
    lines.append("## Global packet-exposure summary")
    lines.append("")
    lines.append(compact.to_markdown(index=False))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("Use `live_packet_fraction` for passenger exposure. It counts the packet")
    lines.append("through active service and stops counting reset/decompression as passenger")
    lines.append("exposure unless `count_reset_as_packet_exposure` is enabled.")
    lines.append("")
    lines.append("Use `geometric_packet_fraction` as a conservative geometry overlap diagnostic.")
    lines.append("It counts points inside the packet-shaped mask even after the packet should")
    lines.append("have been released/rematched.")
    lines.append("")
    lines.append("## Files written")
    lines.append("")
    lines.append("- `lifecycle_points_with_masks.csv`")
    lines.append("- `lifecycle_global_summary.csv`")
    lines.append("- `lifecycle_by_phase_summary.csv`")
    lines.append("- `lifecycle_by_region_summary.csv`")
    lines.append("- `lifecycle_by_phase_region_summary.csv`")
    lines.append("- `lifecycle_top_bad_points.csv`")
    lines.append("- `lifecycle_packet_peak_comparison.csv`")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)

    ap.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)

    ap.add_argument("--Rpass", type=float, default=0.35)
    ap.add_argument("--Rth", type=float, default=1.25)

    ap.add_argument("--x-catch", type=float, default=0.15)
    ap.add_argument("--x-beta", type=float, default=0.70)
    ap.add_argument("--x-q", type=float, default=1.25)

    ap.add_argument("--w-catch", type=float, default=0.16)
    ap.add_argument("--w-beta", type=float, default=0.18)
    ap.add_argument("--w-q", type=float, default=0.18)

    ap.add_argument("--live-packet-end-margin-widths", type=float, default=2.0)

    ap.add_argument(
        "--count-reset-as-packet-exposure",
        action="store_true",
        help="Use geometric packet mask through reset/decompression. Conservative but may overcount passenger exposure.",
    )

    ap.add_argument("--top-n", type=int, default=30)

    return ap.parse_args()


def main() -> None:
    args = parse_args()

    params = LifecycleParams(
        Rpass=args.Rpass,
        Rth=args.Rth,
        x_catch=args.x_catch,
        x_beta=args.x_beta,
        x_q=args.x_q,
        w_catch=args.w_catch,
        w_beta=args.w_beta,
        w_q=args.w_q,
        live_packet_end_margin_widths=args.live_packet_end_margin_widths,
        count_reset_as_packet_exposure=args.count_reset_as_packet_exposure,
    )

    run_lifecycle_analysis(
        data_dir=args.data_dir,
        out_dir=args.out_dir,
        params=params,
        top_n=args.top_n,
    )


if __name__ == "__main__":
    main()
