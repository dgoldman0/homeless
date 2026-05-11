# Shifting the Geometric Burden from the Moving Shell to the Wormhole Throat

## Purpose

This report develops the next architectural branch of the compact warp-shell / wormhole-throat ansatz. The tested branch placed the capacity factor, lapse support, and transport shift on a compact moving shell. The new branch keeps the same ADM structure and moves most of the capacity and lapse structure into the wormhole throat complex.

The design objective is direct:

> make the wormhole throat the active high-burden infrastructure, and make the moving warp-shell share lighter, softer, and easier to maintain.

This is a structural refinement of the base ansatz, whose diagnostic quantities already isolate the relevant carriers: spatial capacity `A`, lapse factor `T`, shift `beta`, effective throat radius `Ar`, Einstein-tensor projections, ADM constraints, and null expansions during shell-throat overlap.[^base]

The report uses fenced `math` blocks for GitHub rendering.

---

## Research context

Morris and Thorne’s traversable wormhole construction places the defining geometric work at the throat: finite redshift, flare-out, traversability, and exotic support all meet at the minimum-area surface.[^morris] That makes the throat a natural infrastructure site for any additional capacity or lapse structure.

Alcubierre’s warp geometry and later compact-exterior variants place the transport effect in a moving distortion region.[^alcubierre] Van den Broeck’s compact-exterior / large-interior construction is especially relevant because it separates the outside footprint from the interior volume, while still placing the geometry’s strong gradients near the bubble boundary.[^vdb] Pfenning and Ford’s quantum-inequality analysis highlights the importance of wall thickness and negative-energy localization for Alcubierre-type geometries.[^pfenningford]

Bobrick and Martire’s ADM formulation gives the most useful decomposition for this project: warp configurations can be discussed through lapse, shift, and spatial metric data, and space capacity and time-rate behavior can be treated as controlled ingredients.[^bobrick] This is exactly the separation used in the base ansatz.

Topological censorship and related energy-condition results provide the larger constraint background: traversable topology in classical GR requires energy-condition-violating support.[^topcens] Visser, Kar, and Dadhich show that the amount and distribution of energy-condition violation can be shaped by geometry, which fits the present goal of moving support into a planned throat layer.[^visserkar] Santiago, Schuster, and Visser sharpen the corresponding warp-drive side by showing that physically reasonable warp-drive geometries carry null-energy-condition violations in standard GR.[^santiago]

Israel junction theory and thin-shell methods frame the matching problem: when distinct geometric regions are joined or when strong support layers are localized, extrinsic-curvature jumps and surface stress-energy become part of the engineering content.[^israel]

The combined message is useful for this ansatz: the required exotic and high-gradient support can be treated as a locus-design problem. The throat is the strongest candidate locus because it already exists as the geometric support structure for traversability.

---

## Base branch already evaluated

The base ADM form is:

```math
g = -e^{2\Phi(l)}T^2dt^2
+ A^2q_{ij}\left(dx^i+\beta^idt\right)\left(dx^j+\beta^jdt\right).
```

The moving-shell branch used:

```math
A_{\rm shell}=\exp\left[S(\rho,t)\ln C_0\right]
```

and:

```math
\beta^i=-V(t)S(\rho,t)n^i.
```

The lapse tests produced three useful calibration points:

1. `T = 1` creates a severe high-capacity speed restriction through the causal-balance condition.
2. `T = A` produces a clean subluminal branch with transition at `V = 1`.
3. `T = lambda A`, implemented compactly as `T = A lambda^S`, moves the sampled causal-margin threshold to `lambda >= |V|`.

The third branch was the most informative current result. In the reduced scan:

```math
g_{tt}= -T^2 + A^2V^2S^2.
```

With:

```math
T=A\lambda^S,
```

inside the passenger region this becomes:

```math
g_{tt}\approx A^2(-\lambda^2+V^2).
```

The sampled causal-margin branch followed:

```math
\lambda \ge |V|.
```

For the tested grid, all sampled pairs with `lambda >= V` stayed on the causal-margin branch. The same scan also showed that the largest curvature and null-expansion values remain associated with high capacity, narrow walls, and high speed. That gives the next architectural target: keep the lapse-margin success, and move the high-gradient wall structure into the throat.

---

## Why the throat can carry the burden

The moving shell pays for compact capacity through wall gradients:

```math
\nabla\ln A,
\qquad
\Delta\ln A.
```

For a shell width `Delta`, the base scaling is:

```math
\nabla\ln A \sim \frac{\ln C_0}{\Delta},
\qquad
\Delta\ln A \sim \frac{\ln C_0}{\Delta^2}.
```

The throat already carries flare-out structure through `r(l)`. In the proper radial Morris-Thorne form, the spatial scalar curvature contribution contains:

```math
{}^{(3)}R[q]
=
-\frac{4r''}{r}
+
\frac{2\left(1-(r')^2\right)}{r^2}.
```

At the throat:

```math
r(0)=r_0,
\qquad
r'(0)=0,
\qquad
r''(0)>0.
```

The throat is therefore already the place where flare-out, redshift control, energy-condition violation, and traversability are organized. A throat-anchored capacity layer uses that existing support region as the geometric platform for `A` and `T`.

The architectural shift is:

```math
A(\rho,t) \longrightarrow A_{\rm throat}(l,t)\,A_{\rm passenger}(\rho,t),
```

with the high-amplitude part assigned to the throat factor.

---

## A controlled burden-sharing parameter

A clean way to define the shifted family is to introduce a burden-sharing parameter `eta`:

```math
\ln A
=
\ln C_0\left[(1-\eta)W(l;\Lambda(t)) + \eta S(\rho,t)\right],
\qquad
0\le\eta\le1.
```

Here:

- `W(l;Lambda(t))` is a throat-supported capacity profile.
- `S(rho,t)` is the passenger-shell profile.
- `eta = 1` recovers the moving-shell capacity branch.
- `eta = 0` places the capacity factor fully in the throat-supported branch during transit.

At throat overlap, choose the profiles so that `W approximately 1` and `S approximately 1` in the active transit region. Then:

```math
A\approx C_0
```

while the mobile shell carries the fraction `eta` of the logarithmic capacity gradient.

The mobile shell gradient scalings become:

```math
\nabla\ln A\big|_{\rm shell}
\sim
\eta\frac{\ln C_0}{\Delta_{\rm shell}},
```

```math
\left|\nabla\ln A\right|^2\big|_{\rm shell}
\sim
\eta^2\frac{(\ln C_0)^2}{\Delta_{\rm shell}^2},
```

```math
\Delta\ln A\big|_{\rm shell}
\sim
\eta\frac{\ln C_0}{\Delta_{\rm shell}^2}.
```

This gives a direct engineering interpretation. If `eta = 0.1`, the quadratic gradient contribution in the moving shell is reduced by about a factor of `100`, and the linear Laplacian contribution by about a factor of `10`, before profile-shape effects. If `eta = 0.01`, those factors become `10,000` and `100`.

The corresponding throat layer carries the complementary share:

```math
\nabla\ln A\big|_{\rm throat}
\sim
(1-\eta)\frac{\ln C_0}{L_{\rm throat}},
```

```math
\Delta\ln A\big|_{\rm throat}
\sim
(1-\eta)\frac{\ln C_0}{L_{\rm throat}^2}.
```

This is favorable when the throat support region can be thick:

```math
L_{\rm throat} \gtrsim \Delta_{\rm shell}.
```

A fixed megastructure can allocate a larger support length, use smoother profiles, and ramp fields on a planned timescale.

---

## Lapse support in the throat branch

The `T = lambda A` scan showed that lapse margin provides direct causal-margin control. The throat-shifted version keeps that result and relocates the high-gradient lapse structure.

Use:

```math
\ln T
=
\ln C_0\left[(1-\eta_T)W(l;\Lambda(t)) + \eta_T S(\rho,t)\right]
+
\ln\lambda\left[(1-\zeta)W(l;\Lambda(t)) + \zeta S(\rho,t)\right].
```

The strongest throat-loaded design uses:

```math
\eta_T\approx0,
\qquad
\zeta\approx0.
```

Then the throat complex supplies:

```math
T_{\rm throat}\approx \lambda A_{\rm throat},
```

and the mobile shell supplies a smaller local transition field.

In the active throat region, the causal-margin condition keeps the same leading form:

```math
T > A |V|S.
```

With throat-supported `T approximately lambda A`, this becomes:

```math
\lambda > |V|S.
```

The causal-margin result from the tested `T = lambda A` family therefore remains the design rule, while the compact lapse gradient moves into the fixed throat support.

---

## The mobile shell becomes a transit coupler

Once `A` and `T` are anchored to the throat, the moving shell mainly carries the shift and matching profile:

```math
\beta^i=-V(t)S_{\rm passenger}(\rho,t)n^i.
```

The shell still performs real geometric work. It controls transport, passenger localization, boundary matching, tidal smoothing, and the way the payload couples to the active throat layer. Its role becomes narrower and more maintainable.

The mobile component’s design goals become:

1. keep the passenger world-tube smooth;
2. control the shift profile through the throat;
3. keep null expansions in the transit region organized;
4. minimize jumps in the extrinsic curvature across the passenger boundary;
5. tune tidal components along representative timelike paths.

The high-amplitude capacity and lapse fields belong to the fixed throat complex.

---

## Engineering burden accounting

A useful regional burden measure is:

```math
B(\Omega)
=
\int_\Omega
\left(
w_R|R|
+
w_K\sqrt{|R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}|}
+
w_N\max(0,-G_{\mu\nu}k^\mu k^\nu)
+
w_\theta\max(0,\theta_+\theta_-)
\right)dV.
```

Use two regions:

```math
\Omega_{\rm throat}
=
\{ |l|\le L_{\rm throat} \},
```

```math
\Omega_{\rm shell}
=
\{ \rho\le R_{\rm out} \}\setminus\Omega_{\rm throat}.
```

Then define:

```math
f_{\rm throat}
=
\frac{B(\Omega_{\rm throat})}
{B(\Omega_{\rm throat})+B(\Omega_{\rm shell})}.
```

The throat-burden branch aims for:

```math
f_{\rm throat}\rightarrow 1.
```

This measure directly reports how much of the curvature, energy-condition, and null-expansion burden lives in the fixed complex.

For the capacity and lapse terms, the shift can be very large. For the transport shift and passenger matching terms, the shell retains a finite share. The engineering expectation is therefore:

| Quantity | Throat-shift potential | Reason |
|---|---:|---|
| Capacity gradients from `A` | high | assign logarithmic capacity to `W(l)` |
| Lapse-margin gradients from `T` | high | assign `lambda` support to `W(l)` |
| Exotic support for throat flare-out | high | throat already carries traversability support |
| Wall-localized curvature from compact capacity | high | replace moving compact wall with fixed support layer |
| Shift-driven extrinsic curvature | partial | `beta` remains tied to transit motion |
| Passenger tidal smoothing | partial | payload comfort remains a local matching task |
| Causal-margin rule | high continuity | `lambda > |V|S` remains the guiding condition |

---

## Formation picture for the throat complex

The shifted architecture suggests a staged formation path.

### 1. Establish the Morris-Thorne-class throat

The throat supplies the minimum-area surface, flare-out profile, finite redshift function, and the base exotic support layer.

```math
r(0)=r_0,
\qquad
r'(0)=0,
\qquad
r''(0)>0.
```

### 2. Broaden the active throat support

The throat layer should have enough proper thickness to carry capacity gradients smoothly:

```math
L_{\rm throat}\sim r_0
```

or larger, depending on the target `C0`.

This replaces a compact moving capacity wall of width `Delta_shell` with a planned support region of length `L_throat`.

### 3. Install the capacity profile

Define a throat capacity state:

```math
A_{\rm throat}(l,t)=
\exp\left[\Lambda(t)W(l)\ln C_0\right].
```

Here `Lambda(t)` ramps the throat from standby to active transit configuration.

### 4. Couple lapse support to capacity

Use:

```math
T_{\rm throat}(l,t)
=
A_{\rm throat}(l,t)\lambda^{\Lambda(t)W(l)}.
```

This preserves the lapse-margin relationship identified in the `T = lambda A` scan.

### 5. Use adiabatic throat pumping

Ramping the throat state over time gives:

```math
\partial_t\ln A_{\rm throat}
=
\dot\Lambda(t)W(l)\ln C_0.
```

A larger ramp time lowers the time-derivative contribution to extrinsic curvature. The fixed complex can use slow preparation and recovery cycles; the moving shell passes through the prepared state.

### 6. Move a lighter transit shell through the active throat

The passenger shell carries:

```math
S_{\rm passenger}(\rho,t),
\qquad
\beta^i=-V(t)S_{\rm passenger}n^i,
```

plus local comfort and matching fields.

---

## Consequences for the ease of the warp-bubble share

The mobile warp-bubble share becomes easier in specific geometric senses.

### Lower portable capacity gradient

With burden parameter `eta`, the moving shell carries `eta ln C0` of the capacity logarithm. The strongest wall terms respond directly to `eta` and `eta^2`.

### Softer passenger boundary

The passenger shell can use a larger wall thickness:

```math
\Delta_{\rm passenger} > \Delta_{\rm capacity,old}.
```

That reduces gradient-driven curvature in the mobile object and improves matching control.

### Reusable infrastructure

The throat complex carries the high-burden fields once, then repeats transit cycles. The moving shell becomes closer to a coupling capsule than a self-contained large-interior geometry generator.

### Cleaner separation of jobs

The throat complex supplies:

```math
A_{\rm throat},
\qquad
T_{\rm throat},
\qquad
r(l),
\qquad
\Phi(l).
```

The moving shell supplies:

```math
S_{\rm passenger},
\qquad
\beta^i,
\qquad
\text{tidal smoothing},
\qquad
\text{matching control}.
```

That division is the key engineering implication.

---

## Consequences for use cases

The throat-loaded branch changes the practical interpretation of the whole construction.

### Fixed-gate transit

The primary use case becomes a prepared wormhole gate. The mobile object passes through an active throat state. Most of the geometric apparatus remains fixed at the gate.

### Habitat or storage volume through a gate

A high-capacity throat layer can generate large effective internal capacity during transit or docking. The payload shell can remain comparatively light because the gate supplies the capacity state.

### Repeatable infrastructure

The fixed throat complex can be calibrated, shielded, monitored, and maintained as a persistent megastructure. The mobile shell needs compatibility with the gate field.

### Speed-family flexibility

The tested lapse relation:

```math
\lambda\ge |V|
```

continues to organize the active branch. With the lapse margin held by the throat, speed-family tuning becomes a property of the gate state.

---

## Diagnostics for the throat-loaded branch

The same diagnostics remain valid, with regional accounting added.

### Global regularity

```math
\det g=-e^{2\Phi}T^2A^6r^4\sin^2\theta.
```

### Curvature invariants

```math
R,
\qquad
R_{\mu\nu}R^{\mu\nu},
\qquad
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}.
```

### Energy projections

```math
G_{\mu\nu}n^\mu n^\nu,
\qquad
G_{\mu\nu}k^\mu k^\nu,
\qquad
G_{\mu\nu}u^\mu u^\nu.
```

### Throat behavior

```math
\mathcal R(l,t)=A(l,t)r(l).
```

```math
\partial_l\mathcal R=0,
\qquad
\partial_l^2\mathcal R>0.
```

### Null expansions

```math
\theta_\pm
=
\frac{2}{Ar}
\left[
\frac{1}{\alpha}\left(\partial_t-\beta^l\partial_l\right)(Ar)
\pm
\frac{1}{A}\partial_l(Ar)
\right].
```

### Regional burden share

```math
f_{\rm throat}
=
\frac{B(\Omega_{\rm throat})}
{B(\Omega_{\rm throat})+B(\Omega_{\rm shell})}.
```

The new branch succeeds as an architecture when `f_throat` rises while the passenger shell’s local tidal and null-expansion diagnostics remain controlled.

---

## Main implications

### 1. The throat becomes the capacity machine

The high-capacity part of the geometry is best treated as infrastructure. The throat already has the topology, flare-out, and exotic-support role. Adding `A_throat` and `T_throat` turns it into the capacity and lapse-support machine.

### 2. The mobile shell becomes a lower-burden transit object

The mobile shell can carry the shift, local passenger profile, and matching fields. Its capacity share can be dialed by `eta`. Small `eta` gives a large reduction in the portable gradient burden.

### 3. The `T = lambda A` result remains central

The tested branch established a simple design rule:

```math
\lambda\ge |V|.
```

The throat-loaded branch keeps that rule and assigns the lapse margin to fixed infrastructure.

### 4. Wider support layers are valuable

A throat support scale `L_throat` lets the gradients spread across a larger proper distance. This directly softens the curvature terms tied to `ln C0`.

### 5. Formation becomes an infrastructure problem

The formation sequence centers on constructing and stabilizing the wormhole complex, then activating a capacity/lapse state during transit. The mobile shell becomes a compatible payload system.

### 6. The next mathematical model is a burden-sharing family

The immediate model to evaluate is:

```math
\ln A
=
\ln C_0\left[(1-\eta)W(l;\Lambda(t)) + \eta S(\rho,t)\right],
```

```math
\ln T
=
\ln A+
\ln\lambda\left[(1-\zeta)W(l;\Lambda(t)) + \zeta S(\rho,t)\right],
```

```math
\beta^i=-V(t)S(\rho,t)n^i.
```

The parameters `eta` and `zeta` become explicit engineering knobs for moving burden between the fixed throat complex and the mobile transit shell.

---

## Report conclusion

The throat-burden architecture is a strong next branch of the ansatz.

The tested moving-shell families showed how lapse margin controls the causal-balance relation, and how compact capacity concentrates curvature and null-expansion structure in the shell wall. The throat-loaded branch keeps the useful lapse-margin rule and relocates the capacity/lapse gradients into a fixed wormhole support layer.

This changes the potential engineering picture. The high-burden component becomes the wormhole megastructure. The mobile warp-bubble component becomes a lighter transit shell that carries shift, passenger localization, and matching control. The expected outcome is a large reduction in the portable capacity burden, especially through the `eta` scaling of the moving-shell gradient terms.

The most important new diagnostic is the regional burden fraction:

```math
f_{\rm throat}
=
\frac{B(\Omega_{\rm throat})}
{B(\Omega_{\rm throat})+B(\Omega_{\rm shell})}.
```

That fraction turns the architectural goal into a measurable geometric result.

---

## Sources

[^base]: Base ansatz file in this project: `compact_warp_shell_wormhole_ansatz(1).md`.

[^morris]: Michael S. Morris and Kip S. Thorne, “Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity,” *American Journal of Physics* 56, 395 (1988). DOI: <https://doi.org/10.1119/1.15620>. ADS record: <https://ui.adsabs.harvard.edu/abs/1988AmJPh..56..395M>.

[^alcubierre]: Miguel Alcubierre, “The warp drive: hyper-fast travel within general relativity,” *Classical and Quantum Gravity* 11, L73-L77 (1994). arXiv version: <https://arxiv.org/abs/gr-qc/0009013>.

[^vdb]: Chris Van Den Broeck, “A ‘warp drive’ with more reasonable total energy requirements,” *Classical and Quantum Gravity* 16, 3973 (1999). arXiv: <https://arxiv.org/abs/gr-qc/9905084>.

[^pfenningford]: Michael J. Pfenning and L. H. Ford, “The unphysical nature of ‘Warp Drive’,” *Classical and Quantum Gravity* 14, 1743-1751 (1997). arXiv: <https://arxiv.org/abs/gr-qc/9702026>. DOI: <https://doi.org/10.1088/0264-9381/14/7/011>.

[^bobrick]: Alexey Bobrick and Gianni Martire, “Introducing Physical Warp Drives,” *Classical and Quantum Gravity* 38, 105009 (2021). arXiv: <https://arxiv.org/abs/2102.06824>. DOI: <https://doi.org/10.1088/1361-6382/abdf6e>.

[^topcens]: John L. Friedman, Kristin Schleich, and Donald M. Witt, “Topological Censorship,” *Physical Review Letters* 71, 1486 (1993). arXiv: <https://arxiv.org/abs/gr-qc/9305017>.

[^visserkar]: Matt Visser, Sayan Kar, and Naresh Dadhich, “Traversable wormholes with arbitrarily small energy condition violations,” *Physical Review Letters* 90, 201102 (2003). arXiv: <https://arxiv.org/abs/gr-qc/0301003>.

[^santiago]: Jessica Santiago, Sebastian Schuster, and Matt Visser, “Generic warp drives violate the null energy condition,” *Physical Review D* 105, 064038 (2022). arXiv: <https://arxiv.org/abs/2105.03079>. DOI: <https://doi.org/10.1103/PhysRevD.105.064038>.

[^israel]: Werner Israel, “Singular Hypersurfaces and Thin Shells in General Relativity,” *Nuovo Cimento B* 44, 1-14 (1966); correction 48, 463 (1967). DOI: <https://doi.org/10.1007/BF02712210>.

[^adm]: Éric Gourgoulhon, “3+1 formalism and bases of numerical relativity,” lecture notes (2007). PDF: <https://people-lux.obspm.fr/gourgoulhon/pdf/form3p1.pdf>. See also Abhay Ashtekar Corichi and collaborators’ ADM review: <https://arxiv.org/pdf/2210.10103>.
