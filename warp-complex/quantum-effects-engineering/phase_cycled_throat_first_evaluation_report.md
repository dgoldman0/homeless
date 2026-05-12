# Phase-Cycled Throat Support: First Evaluation of QI-Managed Wormhole Throat Operation

**Author:** Daniel S. Goldman  
**ORCID:** https://orcid.org/0000-0003-2835-3521  
**Date:** 2026-05-12

## Abstract

This report begins a new direction separate from the catch-rematched transport geometry: the quantum-effects engineering problem at the throat itself. The central idea, called **phase-cycled throat support**, is to replace the mental picture of a static exotic material band with an actively controlled throat plant whose negative-energy support appears in timed phases, is paired with positive-energy repayment structure, and is allowed to participate in a controlled geometric envelope. The goal is modest and operational. The evaluation asks whether quantum-inequality pressure can be brought into a classical engineering control envelope, not whether it can be bypassed.

Two reduced tests were performed. The first keeps a standard zero-redshift Morris--Thorne throat static and asks whether a smooth persistent source or a pulse train can satisfy a local Lorentzian quantum-inequality proxy. The second lets the throat radius breathe dynamically and asks whether source cycling creates a usable traversable phase while keeping curvature, null projections, and tidal proxies within a controlled range. The static model reproduces the expected Ford--Roman obstruction: a macroscopic smooth throat requires sampled negative energy far outside the proxy bound. The simple pulse-train attempt also returns the averaged negative support when sampled over many cycles. The dynamic breathing model creates positive-energy repayment phases and short negative-energy support phases, but the first reduced sweep places the apparent improvements in regimes with severe source pulses, expansion pulses, tidal spikes, and open windows far shorter than a throat crossing time.

The first evaluation therefore gives a clear boundary. A static smooth macroscopic throat lies outside the tested quantum-inequality envelope. A single-zone breathing throat creates the right source bookkeeping ingredients while pushing the geometry into violent operating phases. The next viable refinement, if this line is pursued, is a **spatially separated phase-cycled throat plant**: support bands, repayment bands, buffer regions, and protected access phases, rather than a globally breathing throat.

## 1. Motivation

The classical throat-loaded transit architecture moved the hard geometric burden into a prepared infrastructure region. That result is useful: the vehicle no longer carries the main warp-like support. The throat complex becomes the active system, while the passenger/coupling region becomes an operational interface. The quantum problem then becomes sharper. The throat support band carries the same kind of exotic burden that quantum inequalities target.

A static macroscopic traversable wormhole asks for negative energy that persists over macroscopic sampling times. Known quantum inequality results restrict this combination of magnitude and duration. The question in this report is therefore an engineering question rather than a loophole claim:

\[
\text{Can the throat plant operate as a controlled quantum-source system rather than a static exotic material?}
\]

Phase-cycled throat support treats the throat as a timed plant. Negative support phases are paired with positive repayment phases. The metric is allowed to respond within a controlled envelope. Passage, if it ever becomes possible, would occur during scheduled safe phases. This reframes the quantum issue as a control problem involving duty cycle, support amplitude, repayment delay, geometric ripple, and passenger access timing.

The first evaluation deliberately removes the transport/catch layer. The transport layer can help a vessel use a throat plant, but the plant itself must first show a plausible quantum-support operating envelope. This report studies the throat alone.

## 2. Background: sampled negative energy as the controlling constraint

Quantum field theory permits local negative energy densities in special states and boundary configurations, but sampled negative energy is constrained. A standard local Lorentzian sampling form in flat-space quantum inequality estimates is

\[
\int_{-\infty}^{\infty}\rho(\tau)
\frac{\tau_0/\pi}{\tau^2+\tau_0^2}\,d\tau
\geq
-\frac{3}{32\pi^2\tau_0^4}.
\]

The exact bound depends on field content, spacetime curvature, observer state, sampling assumptions, and domain of validity. The scaling captures the relevant engineering fact: allowed negative averaged energy becomes much smaller for long sampling times. A throat support band that remains negative over a macroscopic duration is therefore much harder to fit inside the quantum envelope than a short negative pulse.

Ford and Roman used this logic to constrain traversable wormhole geometries. Pfenning and Ford applied related quantum-inequality reasoning to Alcubierre-type warp geometries and found extremely thin wall requirements and overwhelming integrated negative energy. The phase-cycled idea accepts this pressure and asks whether the source can be operated as a high-frequency managed plant whose cycle remains compatible with a usable classical envelope.

## 3. The tested throat model

The starting geometry is the clean zero-redshift radial throat

\[
ds^2=-dt^2+dl^2+r(l)^2d\Omega^2,
\qquad
r(l)=\sqrt{r_0^2+l^2}.
\]

At the throat, the effective static source has

\[
\rho_0=-\frac{1}{8\pi r_0^2},
\qquad
\rho_0+p_l=-\frac{1}{4\pi r_0^2}.
\]

The first test applies the sampled-energy proxy directly to this static source. The second test promotes the throat radius to a time-dependent envelope,

\[
R(l,t)=\sqrt{a(t)^2+l^2},
\qquad
 ds^2=-dt^2+dl^2+R(l,t)^2d\Omega^2.
\]

The function \(a(t)\) is the throat-control degree of freedom. Smooth sinusoidal cycles and short open-gate pulses were tested. The effective source was read from

\[
T_{\mu\nu}^{\rm eff}=\frac{1}{8\pi}G_{\mu\nu},
\]

and the evaluation tracked sampled energy, radial null projections, angular tidal proxies, expansion-product proxies, and the fractional open/quasi-static part of the cycle.

This is a reduced diagnostic model. It identifies the direction of the constraints and the tradeoffs among source cycling, open time, and geometric violence. It is not a complete semiclassical solution.

## 4. Static throat result

Let the sampling time be a fixed fraction of the throat radius,

\[
\tau_0=\eta r_0.
\]

The ratio between the required static negative energy density and the Lorentzian QI allowance is

\[
\mathcal R_{\rm QI}
=\frac{|\rho_0|}{3/(32\pi^2\tau_0^4)}
=\frac{4\pi}{3}\eta^4 r_0^2.
\]

The condition \(\mathcal R_{\rm QI}\leq1\) gives a maximum radius in Planck units. The reduced sweep produced the following scale limits.

| Sampling fraction \(\eta\) | Maximum \(r_0/L_P\) | Maximum radius in meters |
|---:|---:|---:|
| 0.1 | \(4.89\times10^1\) | \(7.90\times10^{-34}\) |
| 0.03 | \(5.43\times10^2\) | \(8.77\times10^{-33}\) |
| 0.01 | \(4.89\times10^3\) | \(7.90\times10^{-32}\) |
| 0.003 | \(5.43\times10^4\) | \(8.77\times10^{-31}\) |
| 0.001 | \(4.89\times10^5\) | \(7.90\times10^{-30}\) |

For a meter-scale throat, \(r_0\approx6.19\times10^{34}L_P\). The corresponding static violation factor is enormous across the tested sampling fractions. This result places the static smooth throat far outside the known sampled-energy envelope.

The pulse-train test added compensated negative and positive source phases while keeping the same static support requirement. The result follows the scaling directly. When the pulse period is short enough for the throat to see an effectively steady support, Lorentzian windows spanning many cycles also recover the negative mean. When the period is stretched enough to reduce that averaged sampling burden, the geometry no longer receives continuous static support. The static-pulse version therefore compresses the problem into a timing contradiction: fast enough for the throat also means visible to the sampling bound; slow enough for the bound means discontinuous support.

## 5. Dynamic throat result

The dynamic test asks a different question. The throat is allowed to breathe, so the source does not have to mimic a static negative band at every moment. Negative support phases can coincide with throat opening, and positive repayment phases can coincide with compression or buffer states. This gives the phase-cycled idea its cleanest first trial.

The sweep tested sinusoidal breathing and open-pulse profiles. The core behavior is summarized by representative cases below. The quantities are dimensionless reduced proxies. Larger null projection, tidal, and expansion values indicate more severe source and geometry pulses.

| Case | Strict \(\log_{10}(L_{0,\max}/L_P)\) | Max radial null-projection proxy | Max angular tidal proxy | Max expansion-product proxy | Max \(|\dot a/a|\) | Quasi-static open fraction |
|---|---:|---:|---:|---:|---:|---:|
| static \(a=1\) | -0.31 | 2.0 | 0.0 | 0.0 | 0.0 | 1.000 |
| sinusoid \(\epsilon=0.1,\Omega=20\) | 3.84 | 91.36 | 44.44 | 16.16 | 2.01 | 0.017 |
| sinusoid \(\epsilon=0.6,\Omega=5\) | 2.48 | 87.50 | 37.50 | 56.25 | 3.75 | 0.017 |
| pulse \(a_c=0.5,w=0.02\) | 2.53 | \(1.43\times10^5\) | \(7.16\times10^4\) | \(1.11\times10^5\) | 154.04 | 0.0015 |
| pulse \(a_c=0.1,w=0.02\) | 1.12 | \(6.94\times10^5\) | \(3.47\times10^5\) | \(1.07\times10^6\) | 500.98 | 0.0005 |

The dynamic model produces the desired qualitative ingredients: the effective source contains both negative-support and positive-repayment phases, and some sampling windows become less hostile than the static case. The improvement appears together with strong dynamical cost. The cases that move the strict scale upward also introduce rapid breathing, null-projection pulses, angular tidal spikes, and a very small quasi-static open fraction.

The interpretation is direct. A single-zone throat can improve sampled-energy bookkeeping by becoming strongly time dependent, but the time dependence itself becomes a classical engineering burden. The throat behaves more like a violently driven resonator than a calm traversable gate.

## 6. Passage-window estimate

A useful macroscopic gate must remain open long enough for causal passage through the throat. The crude QI-compatible open-window estimate used in the evaluation gives, for a throat radius \(r_0\), an allowed open duration scaling like

\[
T_{\max}\sim (8\pi C_{\rm QI})^{1/4}\sqrt{r_0},
\qquad
C_{\rm QI}=\frac{3}{32\pi^2},
\]

in Planck units. The light-crossing time scales like \(r_0\). This difference is decisive for macroscopic radii: the open duration grows as \(\sqrt{r_0}\), while the traversal time grows as \(r_0\).

| Throat radius | Estimated QI open duration | Light-crossing time | Ratio |
|---:|---:|---:|---:|
| \(10^{-15}\,\mathrm m\) | \(2.96\times10^{-34}\,\mathrm s\) | \(3.34\times10^{-24}\,\mathrm s\) | \(8.89\times10^{-11}\) |
| \(10^{-9}\,\mathrm m\) | \(2.96\times10^{-31}\,\mathrm s\) | \(3.34\times10^{-18}\,\mathrm s\) | \(8.89\times10^{-14}\) |
| \(10^{-3}\,\mathrm m\) | \(2.96\times10^{-28}\,\mathrm s\) | \(3.34\times10^{-12}\,\mathrm s\) | \(8.89\times10^{-17}\) |
| \(1\,\mathrm m\) | \(9.37\times10^{-27}\,\mathrm s\) | \(3.34\times10^{-9}\,\mathrm s\) | \(2.81\times10^{-18}\) |
| \(10^3\,\mathrm m\) | \(2.96\times10^{-25}\,\mathrm s\) | \(3.34\times10^{-6}\,\mathrm s\) | \(8.89\times10^{-20}\) |

This estimate gives the first evaluation its strongest engineering conclusion. A simple open-close throat strategy produces windows far shorter than a causal crossing interval. Passage therefore requires something more structured than a globally open throat pulse.

## 7. Engineering interpretation

Phase-cycled throat support is still a useful concept because it names the correct engineering target. The throat plant would need control variables analogous to carrier frequency, duty cycle, repayment delay, positive-energy overshoot, buffer capacity, geometric ripple, and access phase. These are engineering handles. The first evaluation shows that the simplest single-zone versions put those handles in conflict.

The static source asks for a persistent negative average. The static pulse train returns that negative average under broad sampling. The global breathing throat creates repayment phases, yet it concentrates the burden into violent geometry pulses. The open-window estimate then shows that a gate which opens only during QI-friendly intervals gives unusably short macroscopic windows.

The next version must spatially organize the quantum bookkeeping. The natural refinement is a throat plant with separate regions:

\[
\text{support band}\quad + \quad\text{repayment/buffer band}\quad + \quad\text{protected passage island}.
\]

In that architecture, negative support phases would be localized where flare-out needs them, positive repayment would be routed into buffer regions, and the accessible path would be scheduled through a comparatively quiet phase. The success criterion would be a bounded ripple in the effective geometry, not a static throat held open by a steady exotic band.

The transport/catch system belongs after this step. It can protect passengers, time entry and exit, and decouple a vessel from throat-control phases. It does not carry the primary quantum support problem. The throat plant must first establish a workable phase-cycled envelope.

## 8. Boundary established by the first evaluation

This first evaluation establishes three boundaries.

First, the smooth static macroscopic throat remains outside the tested quantum-inequality envelope. The Planck-scale radius bounds recovered by the simple proxy agree with the established Ford--Roman message.

Second, pulse trains that merely approximate a static negative-energy source do not change the sampled-average problem. A fast carrier restores the required mean support to the sampling observer; a slow carrier removes the steady support needed by the static geometry.

Third, single-zone dynamic breathing creates positive repayment phases and shorter negative-energy episodes, while the associated geometric dynamics become severe. The improved sampled-energy cases come with strong null-projection pulses, tidal pulses, expansion pulses, and very short open fractions.

These results do not close the whole phase-cycled program. They identify the next necessary design feature: spatial separation between support, repayment, buffering, and passage. A future second evaluation should test a multi-zone throat model rather than a global breathing radius.

## 9. Next model to test

The next reduced model should introduce at least three coupled envelopes:

\[
a(l,t)=a_0(l)+a_{\rm support}(l,t)+a_{\rm repay}(l,t)+a_{\rm buffer}(l,t),
\]

with compactly separated profiles in \(l\). The diagnostics should track sampled energy along static throat observers, radial geodesic observers, and candidate protected passage paths. The geometric side should track null expansions, tidal histories, horizon indicators, and radiative source flux.

A meaningful success would look like a stable phase schedule: support phases maintain flare-out, repayment phases remain outside the protected passage island, and the metric ripple along the accessible path stays within a prescribed tidal and causal margin. The first evaluation shows that global breathing lacks this spatial structure. The next test should add it deliberately.

## References

M. S. Morris and K. S. Thorne, “Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity,” *American Journal of Physics* **56**, 395 (1988). This is the standard traversable-wormhole construction motivating the throat model and flare-out support requirement.

L. H. Ford and T. A. Roman, “Quantum field theory constrains traversable wormhole geometries,” *Physical Review D* **53**, 5496 (1996). This is the central quantum-inequality constraint source for macroscopic wormhole support.

M. J. Pfenning and L. H. Ford, “The unphysical nature of ‘warp drive’,” *Classical and Quantum Gravity* **14**, 1743 (1997). This applies quantum-inequality reasoning to warp-drive stress-energy and motivates the comparison between moving walls and fixed throat support.

L. H. Ford and T. A. Roman, “The quantum interest conjecture,” *Physical Review D* **60**, 104018 (1999). This motivates the repayment-phase language used in phase-cycled support.

C. J. Fewster and E. Teo, “Quantum inequalities and ‘quantum interest’ as eigenvalue problems,” *Physical Review D* **59**, 104016 (1999). This supports the interpretation of sampled-energy restrictions as constraints over sampling windows rather than instantaneous energy-density signs alone.

## Data products used

This report summarizes the outputs of the first two reduced evaluations:

`stage1_static_wormhole_qi_outputs.zip` contains the static throat QI ratio sweep, allowed-radius table, compressed-band estimate, pulse-train sampling demonstration, and summary metadata.

`stage2_dynamic_throat_qi_outputs.zip` contains the dynamic throat case summary, representative time series, Lorentzian sampling records, analytic open-window estimates, and model notes.
