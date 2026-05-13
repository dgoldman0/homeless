# Catch-Rematched Hybrid Flare-Gated Transit v1 Paper Bundle

This bundle contains a standalone LaTeX paper package for:

**Catch-Rematched Hybrid Flare-Gated Transit: A Packet-Centered Composite Wormhole-Warp Architecture**

## Main files

- `latex/main.tex` - standalone paper source.
- `latex/references.bib` - bibliography database.
- `pdf/catch_rematched_hybrid_flare_gated_transit_v1.pdf` - compiled paper PDF.
- `data/` - compact CSV/JSON outputs used by the paper.
- `scripts/` - scripts for reduced ADM diagnostics, transition refinement, geometry confirmation, source proxy screen, robustness checks, and figure generation.
- `figures/` - figures included in the paper.
- `sources/literature_sources.md` - source access notes and citation roles.
- `MANIFEST.sha256` - checksums for all files in the bundle.

## Scope

The paper freezes a reduced composite engineering reference model under the conditional assumption that the required source support can be supplied. It combines hybrid flare-gated wormhole infrastructure with catch-rematched throat-loaded packet transit, and reports transition, geometry, source-proxy, and robustness screens for the frozen v1 candidate.

## Compilation

From `latex/`, run:

```bash
pdflatex main.tex
bibtex.original main
pdflatex main.tex
pdflatex main.tex
```

Figures can be regenerated from the bundle root with:

```bash
python scripts/build_paper_figures.py
```
