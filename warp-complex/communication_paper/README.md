# Catch-rematched throat-loaded transit ansatz paper bundle

This bundle contains a stand-alone LaTeX paper, BibTeX references, a compiled PDF, source snapshots, and the reduced-evaluation outputs used to support the paper.

## Main files

- `throat_loaded_catch_rematched_paper.pdf` - compiled paper.
- `latex/main.tex` - LaTeX source.
- `latex/references.bib` - BibTeX database.
- `sources/external_source_snapshots/` - saved verification snapshots for external papers used in the bibliography.
- `sources/repository_snapshots/` - saved notes for GitHub repository sources used in the paper.
- `evaluation_outputs/` - generated reduced-validation reports and data archives.

## Source packaging note

The container used to compile the paper could not directly download public internet PDFs. External papers were verified through the browsing tool using official arXiv/APS/DOI metadata pages and, when available, ar5iv-rendered full-text views. The bundle therefore includes source snapshots and relation notes rather than raw external PDF files. Repository-derived materials and generated evaluation outputs are included as local files.

## Compilation

From `latex/`, run:

```bash
pdflatex main.tex
bibtex.original main
pdflatex main.tex
pdflatex main.tex
```

The compiled PDF was visually rendered and spot-checked after compilation.
