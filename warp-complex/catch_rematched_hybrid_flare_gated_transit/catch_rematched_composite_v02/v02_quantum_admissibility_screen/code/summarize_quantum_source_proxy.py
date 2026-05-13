#!/usr/bin/env python3
"""Create compact tables for the v0.2 ADM current-floor source-admissibility screen."""
from pathlib import Path
import argparse
import json
import pandas as pd


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--summary-csv', default='data/quantum_source_proxy_summary.csv')
    ap.add_argument('--out', default='derived/recomputed_tables.md')
    args = ap.parse_args()

    df = pd.read_csv(args.summary_csv)
    stressed = df[df['scenario'] == 'V10_lam6'].copy()
    stressed_cols = [
        'label',
        'min_packet_tkk_floor_min',
        'max_packet_neg_volume_proxy',
        'max_packet_j_p95_abs',
        'max_packet_rho_p95_abs',
        'max_packet_R3_p95_abs',
        'max_packet_K_p95_abs',
        'packet_lor_min_tau0.2',
        'min_support_edge_tkk_floor_min',
        'max_support_edge_neg_volume_proxy',
        'support_edge_lor_min_tau0.2',
    ]

    agg = df.groupby('label').agg({
        'rel_max_packet_neg_volume_proxy': 'max',
        'rel_max_support_edge_neg_volume_proxy': 'max',
        'rel_max_service_union_neg_volume_proxy': 'max',
        'rel_max_packet_j_p95_abs': 'max',
        'rel_max_packet_rho_p95_abs': 'max',
        'rel_max_packet_R3_p95_abs': 'max',
        'rel_max_packet_K_p95_abs': 'max',
        'max_packet_packet_norm_max': 'max',
        'max_support_edge_gtt_max': 'max',
    }).reset_index()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as f:
        f.write('# Recomputed v0.2 quantum-source proxy tables\n\n')
        f.write('## Stressed scenario: V=10, lambda=6\n\n')
        f.write(stressed[stressed_cols].to_markdown(index=False))
        f.write('\n\n## Worst relative readout across all tested scenarios\n\n')
        f.write(agg.to_markdown(index=False))
        f.write('\n')

    compact = {
        'stressed_rows': stressed[stressed_cols].to_dict(orient='records'),
        'aggregate_rows': agg.to_dict(orient='records'),
    }
    (out.parent / 'recomputed_tables.json').write_text(json.dumps(compact, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
