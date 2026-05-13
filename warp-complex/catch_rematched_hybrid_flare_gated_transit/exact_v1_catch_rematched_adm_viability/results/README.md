# Results layout

The GitHub bundle keeps compact atlas outputs:

- `atlas_compact.csv`: one row per evaluated slice/mode.
- `atlas_summary.json`: aggregate run summary and compact row list.
- `*.log`: console output from the run.

The full local runs also generate per-slice tensor archives, midplane CSV files, and slice summary JSON files. Those files are reproducible from `code/adm_3p1_viability_v3_baware.py` and are intentionally omitted from this GitHub bundle to keep the repository clean.
