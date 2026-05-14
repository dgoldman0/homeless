#!/usr/bin/env python3
"""
Reduced source-freeze diagnostic for the source-shaped active rail.

This script is a compact reproducer for the summary tables in this bundle.
It is a prescribed-geometry Einstein-source ledger, not a matter model or constraint solve.

Run from this folder:

    python code/source_freeze_diagnostic.py

It writes data/global_case_metrics.csv.
"""
from __future__ import annotations

# NOTE:
# The full exploratory notebook used for this bundle evaluated the warped-product
# Einstein tensor for the reduced ADM rail. This lightweight script preserves the
# final reduced summary table as a deterministic regeneration utility. For a
# production repo version, promote the full tensor evaluator into a tested module.

from pathlib import Path
import pandas as pd

ROWS = [
    dict(case="static_sharp_q", min_rho_all=-0.102949, min_rho_pkt_packet_support=-0.165828,
         max_abs_j_l_edge=0.146736, max_abs_p_l_edge=0.079082, max_abs_pOmega_edge=1.286154,
         max_abs_pOmega_all=1.378406, min_Tkk_edge=-0.800502, min_Tkk_packet_support=-0.798959,
         packet_positive_points=0, edge_gtt_positive_points=0, max_packet_norm=-0.75, max_gtt_edge=-1.0),
    dict(case="soft_sharp_q", min_rho_all=-0.030124, min_rho_pkt_packet_support=-0.045259,
         max_abs_j_l_edge=0.073474, max_abs_p_l_edge=0.031430, max_abs_pOmega_edge=1.274933,
         max_abs_pOmega_all=1.366449, min_Tkk_edge=-0.323194, min_Tkk_packet_support=-0.319617,
         packet_positive_points=0, edge_gtt_positive_points=0, max_packet_norm=-0.75, max_gtt_edge=-1.0),
    dict(case="soft_wide_tanh_q_w08", min_rho_all=-0.035716, min_rho_pkt_packet_support=-0.038030,
         max_abs_j_l_edge=0.022965, max_abs_p_l_edge=0.043977, max_abs_pOmega_edge=1.145278,
         max_abs_pOmega_all=1.303571, min_Tkk_edge=-0.284631, min_Tkk_packet_support=-0.199881,
         packet_positive_points=0, edge_gtt_positive_points=0, max_packet_norm=-0.75, max_gtt_edge=-1.007185),
    dict(case="soft_minjerk_q_t0m04_Tr30", min_rho_all=-0.027982, min_rho_pkt_packet_support=-0.037729,
         max_abs_j_l_edge=0.037607, max_abs_p_l_edge=0.031430, max_abs_pOmega_edge=1.146401,
         max_abs_pOmega_all=1.308665, min_Tkk_edge=-0.290399, min_Tkk_packet_support=-0.201942,
         packet_positive_points=0, edge_gtt_positive_points=0, max_packet_norm=-0.75, max_gtt_edge=-1.0),
    dict(case="static_minjerk_q_t0m04_Tr30", min_rho_all=-0.102949, min_rho_pkt_packet_support=-0.137791,
         max_abs_j_l_edge=0.049505, max_abs_p_l_edge=0.079082, max_abs_pOmega_edge=1.158423,
         max_abs_pOmega_all=1.322054, min_Tkk_edge=-0.801479, min_Tkk_packet_support=-0.529381,
         packet_positive_points=0, edge_gtt_positive_points=0, max_packet_norm=-0.75, max_gtt_edge=-1.0),
]

def main():
    out = Path("data")
    out.mkdir(exist_ok=True)
    df = pd.DataFrame(ROWS)
    df.to_csv(out / "global_case_metrics.csv", index=False)
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
