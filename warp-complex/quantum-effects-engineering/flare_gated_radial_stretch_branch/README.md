# Flare-Gated Radial Stretch Branch Bundle

This bundle documents and reproduces the reduced branch test that moved the design from a B-only adiabatic radial-stretch protocol to a coupled B,R flare-gated radial-stretch protocol.

## Contents

- `MEMO_flare_gated_radial_stretch_branch.md` - main memo.
- `scripts/run_flare_gated_radial_stretch_branch.py` - reproducible reduced source-history screen.
- `data/branch_case_summary.csv` - full case table.
- `data/branch_phase_exposures.csv` - phase-by-phase exposure ledger.
- `data/comparison_table.csv` - compact comparison table used in the memo.
- `data/extracts.json` - machine-readable summary of core claims and selected cases.
- `figures/full_cycle_exposure_comparison.png` - B-only versus flare-gated exposure chart.
- `figures/phase_exposure_flare_gated_B8_TR10.png` - phase ledger chart for the representative branch.
- `docs/` - context notes, equations, and references to the prior framework and B-only evaluation.
- `manifest.json` - file list and checksums.

## Re-run

From this folder:

```bash
python scripts/run_flare_gated_radial_stretch_branch.py --outdir data
```

The script uses only NumPy and pandas. It is a prescribed-geometry screen, not a source construction.
