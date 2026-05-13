# Catch-Rematched / Garattini–Zatrimaylov Obstruction Screen Bundle

This bundle captures the research work from the session on comparing a catch-rematched throat-supported shift rail against the closest wormhole–warp-drive correspondence literature.

The bundle includes:

- `REPORT.md` — concise technical report with GitHub-rendered math blocks.
- `references/literature_sources.md` — literature notes and citation roles.
- `code/` — runnable Python scripts for reduced radial null-characteristic and packet/support-edge bundle screens.
- `data/` — generated JSON/CSV results from the included run.
- `MANIFEST.sha256` — SHA256 manifest for all files in the bundle.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python code/run_all.py
```

The run writes:

- `data/stage1_summary.json`
- `data/stage2_summary.json`
- `data/stage2_bundles.csv`

## Current included run

Stage 1 radial null-characteristic screen:

| Variant | Min absolute null speed | Max near-zero fraction | Order preserved | Final radial range |
|---|---:|---:|---:|---:|
| `active_rail` | 0.0014876 | 0.000e+00 | true | [-5.15014, 5.15014] |
| `catch_independent_shift` | 0.0014876 | 0.000e+00 | true | [-5.15014, 5.15014] |
| `naive_independent_no_catch` | 1.297e-04 | 4.172e-04 | true | [-5.15014, 5.15014] |
| `naive_throat_gated_no_catch` | 4.567e-04 | 4.172e-04 | true | [-5.15014, 5.15014] |
| `late_catch_throat_gated` | 3.945e-04 | 2.086e-04 | true | [-5.15014, 5.15014] |


Stage 2 packet/support-edge radial bundle screen:

| Variant | Min absolute null speed in event bundles | Worst compression ratio | Order preserved | Most constraining event |
|---|---:|---:|---:|---|
| `active_rail` | 0.680795 | 0.81055 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |
| `catch_independent_shift` | 0.680795 | 0.81055 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |
| `naive_independent_no_catch` | 0.19296 | 0.48761 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |
| `naive_throat_gated_no_catch` | 0.195152 | 0.705065 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |
| `late_catch_throat_gated` | 0.59346 | 0.798626 | true | `packet_center_shift_fade`, `ingoing`, width 1.0 |


## Interpretation

The active-rail variant preserves radial ray ordering and clears the packet/support-edge bundle screen in this reduced model. The naive baselines show stronger compression and lower null-speed margins. This supports the working distinction between a localized warp bubble traversing a wormhole and a throat-supported shift rail with catch/rematch choreography.

The next validation tier is a higher-fidelity obstruction paper: add curvature scaling at packet/support-edge intersections, global null maps, and constraint-quality initial-data tests.
