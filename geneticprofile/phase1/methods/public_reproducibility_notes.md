# Public Reproducibility Notes

The package separates three reproducibility levels.

## Level 1: Fully Public Summary Audit

Anyone can inspect the included TSVs, figures, and summaries to evaluate whether the paper's claims match the stated evidence hierarchy.

Relevant files:

- `claims_index/phase1_claims_index.tsv`
- `canonical_windows/window_evidence_summary.tsv`
- `derived_tables/local_object_evidence_ledger.tsv`
- `derived_tables/anchor_validation_public_summary.tsv`
- `derived_tables/global_sensitivity_summary.tsv`

## Level 2: Public Reference Reruns

Readers can repeat public-data processing from original accessions where the source terms allow download. This package lists accessions and run provenance; raw or transformed third-party genotypes stay at source repositories.

Relevant files:

- `derived_tables/public_dataset_inventory.tsv`
- `manifests/source_report_manifest.tsv`
- `run_summaries/public_data_pilots_summary.md`

## Level 3: Private Target Reruns

Full reruns of the target-genome calls require private target data outside this package. That includes raw genotype/sequencing files, phased haplotypes, per-marker calls, family-side files, and match lists.

The public package can still support code review, claim review, window review, and comparator-priority review.
