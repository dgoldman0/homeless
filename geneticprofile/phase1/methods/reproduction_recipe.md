# Reproduction Recipe

This is a high-level recipe for reproducing the public parts of the work. Exact private-target commands live outside this upload package.

## Inputs

- Public reference panels from their source repositories or archives.
- Public accession reads or genotype releases listed in `derived_tables/public_dataset_inventory.tsv`.
- A local private target genome supplied by the authorized analyst.
- hg19/GRCh37 coordinate convention for the canonical windows in this package.

## Workflow Outline

1. Download public references from source locations under their terms.
2. Harmonize variants to hg19/GRCh37 where needed.
3. Apply the canonical windows in `canonical_windows/phase1_canonical_windows.hg19.bed`.
4. Run whole-genome placement and Ashkenazi-control sensitivity checks.
5. Run local-window exact/IBD and phase-aware checks.
6. Run donor-painting or equivalent anchor-removal checks for chr3, chr9, and chr10.
7. Compare outputs to the public ledgers in `derived_tables/`.
8. Keep any private target calls outside a public repository.

## Expected Public-Level Outputs

- Local-object status ledger.
- Global sensitivity summary.
- Public dataset inventory.
- Figure source tables or regenerated figures.
- A claim index connecting statements to evidence classes.

