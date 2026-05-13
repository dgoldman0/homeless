# From the Warp/Wormhole Interface to a Throat-Supported Shift Rail

This bundle contains a standalone paper package connecting:

1. Goldman’s 2022 exploratory question about warp drives and wormholes,
2. Garattini and Zatrimaylov’s wormhole--warp-drive correspondence,
3. the throat-supported shift-rail / catch-rematched active-rail architecture.

The paper frames the architectural pivot from bubble-through-throat imagery to throat-carried transport shift. Under source availability, the architecture organizes the burden into support-contained shift, packet catch/rematch, capacity shaping, support-edge containment, release timing, and reset.

## Layout

```text
paper/      LaTeX source, BibTeX source list, compiled PDF
code/       self-contained reduced diagnostic script
data/       generated JSON and compact markdown summary
figures/    generated figures used by the paper
sources/    literature source notes
README.md   this file
MANIFEST.sha256
```

## Reproduce the diagnostic data

From this directory:

```bash
python code/obstruction_screen.py
```

The script regenerates:

```text
data/obstruction_screen_results.json
data/obstruction_screen_summary.md
figures/packet_positive_points_width025.png
figures/packet_max_norm_width025.png
figures/min_null_speed_width025.png (supplemental diagnostic output)
figures/bundle_compression_width025.png (supplemental diagnostic output)
```

## Rebuild the PDF

From `paper/`:

```bash
pdflatex main.tex
pdflatex main.tex
```

`references.bib` is included as the bibliography source list for reuse. The current `main.tex` contains the rendered bibliography inline for simple compilation.

## Scope

The computation is a reduced radial ADM diagnostic. It tests packet norm, stationary infrastructure diagnostics, radial null speeds, and packet/support-edge bundle compression in stressed service branches. The paper foregrounds the packet-clearance figures; the null-speed and bundle-compression plots remain as supplemental diagnostic outputs. Constraint-quality initial data, off-axis global causal analysis, and semiclassical stress-tensor analysis are next technical gates.
