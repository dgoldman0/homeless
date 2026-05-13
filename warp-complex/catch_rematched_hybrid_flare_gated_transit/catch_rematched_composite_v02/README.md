# Catch-Rematched Hybrid-Flare-Gated Composite v0.2

This bundle contains the v0.2 geometry-burden refinement for the exact-v1 / catch-rematched composite transit architecture.

## Main files

- `REPORT.md` — report and interpretation.
- `code/adm_3p1_viability_v3_baware.py` — ADM diagnostic engine.
- `code/run_v02_confirmation.py` — compact confirmation runner.
- `data/selected_confirmation_41x17.csv` — selected candidate confirmation summary.
- `data/selected_confirmation_41x17_per_slice.csv` — per-slice confirmation data.
- `data/selected_confirmation_summary.json` — ranked confirmation metadata.
- `derived/v02_tables.md` — generated tables used by the report.
- `sources/references.md` — literature references.
- `MANIFEST.sha256` — checksum manifest.

## Reproduce the confirmation table

From the bundle root:

```bash
python code/run_v02_confirmation.py --outdir data_recomputed
```

The default confirmation grid is `41 x 17 x 4` and evaluates the selected candidate set across:

```math
(V,\lambda)\in\{(5,5.75),(10,6),(10,11.5)\},
\qquad
X\in\{0.05,0.35,0.70,1.00,1.25\}.
```

The run writes:

- `data_recomputed/selected_confirmation_41x17.csv`
- `data_recomputed/selected_confirmation_41x17_per_slice.csv`
- `data_recomputed/selected_confirmation_summary.json`

