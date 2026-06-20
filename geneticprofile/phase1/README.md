# Phase 1 Public Verification Package

This folder is a public-safe audit bundle for the phase 1 ancestry paper. It is designed for readers who want to understand the claims, inspect the evidence hierarchy, and double-check the work at the level of windows, aggregate scores, comparator classes, figures, and source provenance.

Raw genotype, phased haplotype, match-list, account-gated, and living-person material is excluded. The package uses a neutral label, `study_target`, for the analyzed genome.

Public destination:

`https://github.com/dgoldman0/homeless/tree/main/geneticprofile/phase1`

## What Is Included

- `paper/paper.pdf` and `paper/paper.tex`: rebuilt phase 1 paper with data availability.
- `claims_index/phase1_claims_index.tsv`: claim-to-evidence index for the major paper statements.
- `canonical_windows/`: hg19 window definitions and evidence status.
- `derived_tables/`: public-safe summaries of direct lineages, local objects, anchor validation, global sensitivity, Roma/Romani audit, and public dataset status.
- `paper/figures/`: final paper figures and the figure-generation script.
- `paper/bibliography.md`: bibliography/reference list without bundled third-party PDFs.
- `methods/`: guardrails and reproducibility notes.
- `manifests/`: source-report provenance, exclusion policy, and generated file manifest.
- `run_summaries/`: compact public narratives for the evidence layers.

## Package Boundary

This bundle supports review of the interpretation. Full target-genome reruns require private input files held outside this package. Public-reference pilots can be repeated from the listed accessions where the source terms allow download and local processing.

## Key Result Frame

The study target is Ashkenazi-centered at whole-genome scale. The strongest reusable findings are a direct maternal `H1aj1a` placement, a direct paternal `R-YP1366*(xR-Y50410)` placement, a chr10 Lithuanian-supported tract, a chr9 Jewish/Samaritan/Ashkenazi core, and a chr3 rare founder block with Mediterranean, eastern-Mediterranean, and West-Asian proxy structure.

## Suggested Reading Order

1. `paper/paper.pdf`
2. `PRIVACY_AND_SCOPE.md`
3. `claims_index/phase1_claims_index.tsv`
4. `canonical_windows/window_evidence_summary.tsv`
5. `derived_tables/local_object_evidence_ledger.tsv`
6. `run_summaries/evidence_synthesis.md`
7. `methods/public_reproducibility_notes.md`
