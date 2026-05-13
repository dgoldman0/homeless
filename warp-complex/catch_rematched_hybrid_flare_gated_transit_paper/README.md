# Catch-Rematched Hybrid Flare-Gated Transit v1 Paper Bundle

This bundle contains a standalone LaTeX/PDF paper package for:

**Catch-Rematched Hybrid Flare-Gated Transit: A Packet-Centered Active-Rail Architecture for Source-Supplied Spacetime Engineering**

## Main files

- `latex/main.tex` - paper source.
- `latex/references.bib` - bibliography.
- `pdf/catch_rematched_hybrid_flare_gated_transit_v1.pdf` - compiled paper PDF.
- `data/` - compact CSV data tables used by the paper.
- `figures/` - figures included in the paper.
- `sources/literature_sources.md` - source notes and citation roles.
- `docs/reproducibility.md` - reproducibility notes.
- `MANIFEST.sha256` - checksums.

## Compilation

From `latex/`:

```bash
pdflatex main.tex
bibtex.original main
pdflatex main.tex
pdflatex main.tex
```

The PDF in `pdf/` was compiled from the included LaTeX source.
