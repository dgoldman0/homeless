# v0.2 quantum-source admissibility proxy screen

This compact bundle records the pre-freeze ADM current-floor source screen for the catch-rematched composite v0.2 candidate.

The screen evaluates the conservative proxy

```math
Tkk_{\rm floor}=\rho_H-2|j_M|
```

from ADM source-demand fields over the packet, support edge, release edge, and service-union regions. Lorentzian sampling is applied along service position histories.

## Main files

- `MEMO.md` — findings, implications, freeze recommendation.
- `data/quantum_source_proxy_summary.csv` — compact scenario summary.
- `data/quantum_source_proxy_timeseries.csv` — service-position histories used for sampling.
- `data/quantum_source_proxy_summary.json` — machine-readable summary and screen note.
- `derived/screen_tables.md` — key tables from the run.
- `code/adm_3p1_viability_v3_baware.py` — ADM source-demand field generator used by this screen family.
- `code/summarize_quantum_source_proxy.py` — reproduces compact tables from the summary CSV.
- `sources/references.md` — literature context.
- `MANIFEST.sha256` — checksum manifest.

## Recompute compact tables

From the bundle root:

```bash
python code/summarize_quantum_source_proxy.py
```
