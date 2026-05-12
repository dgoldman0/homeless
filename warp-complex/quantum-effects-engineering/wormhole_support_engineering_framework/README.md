# Wormhole Support Engineering Framework paper bundle

This bundle contains a field-facing paper package for:

**Engineering Screening Framework for Wormhole-Support Infrastructure Under Quantum-Inequality Constraints**

## Main files

- `pdf/wormhole_support_engineering_framework.pdf` - compiled paper.
- `latex/main.tex` - LaTeX source.
- `latex/references.bib` - BibTeX database.
- `sources/literature_review_sources.md` - literature-review source notes and source roles.
- `evaluation_outputs/` - reduced evaluation artifacts used as demonstration and benchmark cases.

## Evaluation outputs

- `benchmark_screening/` - literature benchmark pilot and gate-classification tables.
- `dynamic_throat_gate/` - dynamic-throat gate prototype outputs.
- `multizone_phase_cycled_throat_evaluation/` - multi-zone phase-cycling reduced outputs.
- `lapse_radial_freedom_throat/` - lapse/radial metric freedom and proper-length sweep outputs.
- `null_contracted_long_throat_eval/` - null-contracted long-throat sweep outputs.

## Source packaging note

The literature review uses bibliographic records, DOI pages, publisher metadata pages, and accessible abstracts/source records. Paywalled PDFs are not bundled. The `sources/literature_review_sources.md` file records source roles and the relation between the literature and the engineering framework.

## Compilation

From `latex/`, run:

```bash
pdflatex main.tex
bibtex.original main
pdflatex main.tex
pdflatex main.tex
```

The compiled PDF was rendered to PNG pages and visually checked before packaging.
