# Exact-v1 Catch-Rematched ADM Viability Memo Bundle

This bundle contains a focused memo, the corrected ADM 3+1 diagnostic script, and generated results for two atlas runs.

## Contents

- `MEMO.md` — engineering memo and readout.
- `code/adm_3p1_viability_v3_baware.py` — corrected B-aware ADM diagnostic script.
- `results/atlas_V5/` — nominal atlas run for `V=5`, `lambda_factor=5.75`, `p_beta=1`.
- `results/atlas_V10_lam6_p4/` — high-stress atlas run for `V=10`, `lambda_factor=6`, `p_beta=4`.
- `results/*.log` — console logs from the two atlas runs.
- `MANIFEST.sha256` — SHA-256 hashes for every file in the bundle.

## Re-run commands

```bash
python code/adm_3p1_viability_v3_baware.py --atlas --outdir rerun_atlas_V5 --nl 81 --nth 33 --nph 8
```

```bash
python code/adm_3p1_viability_v3_baware.py --atlas --outdir rerun_atlas_V10_lam6_p4 --V 10 --lambda-factor 6 --p-beta 4 --atlas-r-modes v1,always_open,delayed_close --nl 81 --nth 33 --nph 8
```
