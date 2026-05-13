#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from radial_model import dangerous_events, summarize_bundle, variant_params

def run_stage2(out_dir: Path) -> dict:
    variants = ["active_rail","catch_independent_shift","naive_independent_no_catch","naive_throat_gated_no_catch","late_catch_throat_gated"]
    width_factors = [1.0,0.5,0.25,0.125]
    rows = []
    for variant in variants:
        for wf in width_factors:
            p = variant_params(variant, width_factor=wf)
            for event_name, (s0,l0) in dangerous_events(p).items():
                if not (-0.35 <= s0 <= 1.65):
                    continue
                for family in ["outgoing","ingoing"]:
                    rec = summarize_bundle(p, family, s0, l0, span=0.04, rays=7, s1=3.0, ds=0.01)
                    rec.update({"variant":variant, "width_factor":wf, "event":event_name})
                    rows.append(rec)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = {"stage":"stage2_packet_support_edge_radial_bundles", "rows":rows}
    (out_dir/"stage2_summary.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    with (out_dir/"stage2_bundles.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out", default="../data")
    args=ap.parse_args(); run_stage2(Path(args.out))
if __name__ == "__main__":
    main()
