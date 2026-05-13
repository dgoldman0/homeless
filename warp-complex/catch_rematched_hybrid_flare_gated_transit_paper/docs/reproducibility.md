# Reproducibility notes

The paper uses compact summary outputs rather than full per-slice tensor archives.

## Figure generation

Run from the bundle root:

```bash
python scripts/build_paper_figures.py
```

This reads:

- `data/geometry_v02/selected_confirmation_41x17.csv`
- `data/quantum_screen/quantum_source_proxy_summary.csv`
- `data/robustness/grid_pressure_robustness_summary.csv`

and writes the four paper figures under `figures/`.

## Main computational scripts

- `scripts/adm_3p1_viability_v3_baware.py`: reduced ADM fields and source-demand diagnostics.
- `scripts/run_transition_refinement_fast.py`: transition-layer refinement using the B-aware ADM diagnostic.
- `scripts/run_v02_confirmation_narrow.py`: mixed-capacity geometry confirmation sweep.
- `scripts/run_v02_quantum_source_screen.py`: conservative current-floor source proxy.
- `scripts/run_candidate_robustness_checks.py`: pressure proxy, scoring, and grid robustness checks.

## Data conventions

The v01 geometry baseline is the prior composite geometry before mixed-capacity refinement. The v1 default is the balanced frozen candidate with `C0=20`, `C_perp=5`, `Rth=1.25`, `wth=0.12`, `B0=6`, and `wB=12`. The no-angular comparison sets `C_perp=1` while preserving the mixed-support geometry family.
