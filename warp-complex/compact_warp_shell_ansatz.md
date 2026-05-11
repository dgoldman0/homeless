# Compact Warp Shells and Traversable Wormhole Throats

> Can a compact warp-drive spacetime, especially one with a small external cross-section and large internal volume, be consistently embedded in or propagated through a pre-existing traversable wormhole geometry without creating horizons, singularities, or uncontrollable stress-energy divergences?

## Abstract

This note formulates the question as a concrete family of Lorentzian metrics. The proposed starting point is a smooth Morris-Thorne wormhole in proper radial coordinates, combined with a generalized Bobrick-Martire warp shell carrying a Van den Broeck-style compact-exterior / large-interior capacity factor. The construction keeps the wormhole throat freedoms explicit, preserves the compact warp-side feature that motivates the question, and places the interaction in the tensor geometry rather than in analogy. Compatibility is encoded in the determinant, curvature invariants, Einstein tensor projections, ADM constraints, throat-area behavior, and null expansions during shell-throat overlap.

# Chosen Initial Pair

Consider first a smooth Morris-Thorne wormhole in proper radial coordinates, combined with a generalized Bobrick-Martire warp shell carrying a Van den Broeck-style compact-exterior / large-interior capacity factor. The pair was chosen because a general Morris-Thorne wormhole preserves the throat freedoms most likely to matter — radius, flare-out, redshift, tidal behavior, and exotic-matter distribution — while a generalized Bobrick-Martire warp shell with a Van den Broeck-style compact-exterior/large-interior factor preserves the exact warp-side feature the idea depends on: a small external geometric footprint enclosing a much larger interior volume. Together they avoid over-simplifying away the key interaction: whether the wormhole throat “sees” only the bubble’s compact exterior or whether the hidden interior volume reappears through curvature, stress-energy, horizons, or matching-condition failures.

## Wormhole background

The wormhole background is written in proper radial coordinates as

$$
ds^2_{\mathrm{WH}}
=
-e^{2\Phi(l)}dt^2+dl^2+r^2(l)d\Omega^2,
$$

with

$$
d\Omega^2=d\theta^2+\sin^2\theta\,d\phi^2.
$$

The coordinate $l$ is proper radial distance through the throat. The throat lies at $l=0$, where

$$
r(0)=r_0>0,\qquad r'(0)=0,\qquad r''(0)>0.
$$

The redshift function $\Phi(l)$ is smooth and finite. These conditions preserve the standard Morris-Thorne throat geometry: a minimum areal radius, finite redshift, and a controlled flare-out profile. The spatial metric on a constant-$t$ slice is

$$
q_{ij}dx^idx^j=dl^2+r^2(l)d\Omega^2.
$$

Its scalar curvature is

$$
{}^{(3)}R[q]
=
-\frac{4r''}{r}+\frac{2\left(1-(r')^2\right)}{r^2}.
$$

At the throat this becomes

$$
{}^{(3)}R[q]\big|_{l=0}
=
-\frac{4r''(0)}{r_0}+\frac{2}{r_0^2}.
$$

The flare-out curvature therefore enters the compatibility problem before the warp shell is introduced. The throat already contains the geometric feature that makes traversability possible, and the combined metric must preserve that feature while adding a compact moving shell.

## ADM representation of the warp side

The warp side is expressed in ADM form,

$$
ds^2=-\alpha^2dt^2+
\gamma_{ij}\left(dx^i+\beta^idt\right)
\left(dx^j+\beta^jdt\right),
$$

where $\alpha$ is the lapse, $\beta^i$ is the shift, and $\gamma_{ij}$ is the spatial metric. This form separates the time-rate function, the transport shift, and the spatial capacity carried by the shell.

The shell center follows a radial world-tube through the wormhole. Its center coordinate is denoted

$$
l=L(t),\qquad V(t)=\dot L(t).
$$

On each wormhole spatial slice, a tubular neighborhood is built around the radial trajectory. The coordinate $\rho$ denotes the background spatial distance from the shell center within that tube, measured using $q_{ij}$. In the local radial-axis approximation,

$$
\rho^2\simeq \left(l-L(t)\right)^2+r^2(L(t))\theta^2,
$$

with the angular coordinate chosen so that $\theta=0$ lies on the trajectory. The fully geometric version replaces this local expression with the normal distance in the tubular neighborhood of the trajectory. The shell support is kept inside that normal neighborhood, so the localization remains smooth throughout the crossing.

A smooth shell profile $S(\rho)$ localizes the warp structure:

$$
S(\rho)=1\quad (\rho\leq R_{\mathrm{in}}),
\qquad
S(\rho)=0\quad (\rho\geq R_{\mathrm{out}}),
$$

with $S\in C^\infty$ and wall thickness

$$
\Delta=R_{\mathrm{out}}-R_{\mathrm{in}}>0.
$$

The compact exterior is the finite support region $\rho<R_{\mathrm{out}}$. The large interior is encoded by a positive capacity factor inside that support.

## Capacity, lapse, and shift

The Van den Broeck-style capacity factor is represented by a positive interpolation

$$
A(\rho)=\exp\!\left[S(\rho)\ln C_0\right],
\qquad C_0>1.
$$

Thus

$$
A(\rho)=C_0\quad (\rho\leq R_{\mathrm{in}}),
\qquad
A(\rho)=1\quad (\rho\geq R_{\mathrm{out}}).
$$

The parameter $C_0$ measures the internal spatial capacity relative to the exterior wormhole slice. A scalar capacity factor gives the clean isotropic model. A refined anisotropic model replaces $A$ by separate radial and angular capacities, $A_\parallel(\rho)$ and $A_\perp(\rho)$, allowing throat-crossing length and angular area to scale differently. The scalar model is the closed first target because it makes the capacity deposit visible in one conformal factor.

A Bobrick-Martire-style time-rate factor is written in the same positive form,

$$
T(\rho)=\exp\!\left[S(\rho)\ln T_0\right],
\qquad T_0>0.
$$

The lapse combines the wormhole redshift with the shell time-rate:

$$
\alpha(t,x)=e^{\Phi(l)}T(\rho).
$$

The shift carries the shell motion along the radial tube. Let $n^i$ be the unit normal direction from the shell center in the wormhole spatial metric $q_{ij}$. Along the radial axis, $n^i\partial_i\simeq\partial_l$. The shift is

$$
\beta^i(t,x)=-V(t)S(\rho)n^i.
$$

The spatial metric carrying the capacity factor is

$$
\gamma_{ij}(t,x)=A^2(\rho)q_{ij}.
$$

The proposed combined metric is therefore

$$
\boxed{
ds^2=-e^{2\Phi(l)}T^2(\rho)dt^2
+A^2(\rho)q_{ij}
\left(dx^i-V(t)S(\rho)n^idt\right)
\left(dx^j-V(t)S(\rho)n^jdt\right)
}.
$$

In the radial-axis reduction this becomes

$$
ds^2=-e^{2\Phi(l)}T^2(\rho)dt^2
+A^2(\rho)\left(dl-V(t)S(\rho)dt\right)^2
+A^2(\rho)r^2(l)d\Omega^2.
$$

Outside the compact support, $S=0$, $A=1$, $T=1$, and $\beta^i=0$, so the metric returns exactly to the Morris-Thorne wormhole:

$$
ds^2\to -e^{2\Phi(l)}dt^2+dl^2+r^2(l)d\Omega^2.
$$

Inside the passenger region, $S=1$, and the local radial-axis form is

$$
ds^2\simeq -e^{2\Phi(l)}T_0^2dt^2
+C_0^2\left(dl-V(t)dt\right)^2
+C_0^2r^2(l)d\Omega^2.
$$

The exterior support remains set by $R_{\mathrm{out}}$, while the internal proper spatial scale is multiplied by $C_0$. This is the compact-exterior / large-interior mechanism expressed directly on a wormhole spatial background.

## Construction of the metric family

The metric family arises by retaining the wormhole as the exterior geometry and placing the warp shell in the wormhole’s ADM data. The Morris-Thorne metric supplies the proper radial coordinate $l$, the areal radius $r(l)$, the redshift $\Phi(l)$, and the throat flare-out. The ADM decomposition supplies lapse, shift, and spatial metric as independent carriers of time-rate, transport, and capacity. The shell profile $S(\rho)$ confines all warp-side deformation to a compact tube around the moving center $L(t)$. The exponential interpolations for $A$ and $T$ keep the capacity and lapse positive for all finite parameter values.

The background wormhole is recovered by the parameter choice

$$
C_0=1,\qquad T_0=1,\qquad V(t)=0.
$$

The generalized warp shell on a locally flat background is recovered by taking

$$
r(l)\to l,
\qquad
\Phi(l)\to0,
$$

inside a local patch away from the throat. The Van den Broeck-style capacity limit is represented by

$$
C_0\gg1,
\qquad
R_{\mathrm{out}}\ll C_0R_{\mathrm{in}}
$$

in the sense that the exterior support radius is held compact while the interior proper lengths and volumes grow with the capacity factor. The dynamic crossing regime is represented by a smooth trajectory $L(t)$ with finite $V(t)$ and finite $\dot V(t)$, for example a trajectory interpolating from one asymptotic side of the wormhole to the other.

This construction isolates the compositional question in one place: the shell-throat overlap, where $L(t)\approx0$ and $R_{\mathrm{in}}<\rho<R_{\mathrm{out}}$. There the wormhole flare-out, the capacity gradient, the lapse gradient, and the shift gradient occupy the same finite region of spacetime.

## Nondegeneracy and signature

For the ADM metric,

$$
\det g_{\mu\nu}=-\alpha^2\det\gamma_{ij}.
$$

Since

$$
\gamma_{ij}=A^2q_{ij},
$$

one has

$$
\det\gamma_{ij}=A^6r^4(l)\sin^2\theta.
$$

Thus

$$
\det g_{\mu\nu}
=-e^{2\Phi(l)}T^2(\rho)A^6(\rho)r^4(l)\sin^2\theta.
$$

Away from the ordinary polar coordinate degeneracy at $\sin\theta=0$, the metric remains nondegenerate wherever $r(l)>0$, $A(\rho)>0$, $T(\rho)>0$, and $\Phi(l)$ is finite. The proposed ansatz therefore carries regular Lorentzian signature at the level of the metric functions. The compatibility content lies in curvature, stress-energy, causal structure, and throat behavior.

## Curvature concentration from the capacity factor

The spatial scalar curvature of the capacity-scaled slice follows the three-dimensional conformal transformation law

$$
{}^{(3)}R[\gamma]
=A^{-2}\left(
{}^{(3)}R[q]
-4\Delta_q\ln A
-2\left|\nabla\ln A\right|_q^2
\right).
$$

For

$$
\ln A=S(\rho)\ln C_0,
$$

this becomes

$$
{}^{(3)}R[\gamma]
=A^{-2}\left[
{}^{(3)}R[q]
-4(\ln C_0)\Delta_qS
-2(\ln C_0)^2\left|\nabla S\right|_q^2
\right].
$$

Inside the passenger region and outside the shell, $\nabla S=0$ and $\Delta_qS=0$. The capacity contribution therefore lives in the wall. In a normal neighborhood where $|\nabla\rho|_q=1$,

$$
\left|\nabla S\right|_q^2=(S')^2,
$$

and

$$
\Delta_qS=S''+S'\Delta_q\rho.
$$

The wall contribution is consequently governed by

$$
(\ln C_0)S'',
\qquad
(\ln C_0)S'\Delta_q\rho,
\qquad
(\ln C_0)^2(S')^2.
$$

The compact-exterior / large-interior feature is visible here as a concentration law. Larger $C_0$ and smaller wall thickness $\Delta$ increase the curvature carried by the wall, while the background term ${}^{(3)}R[q]$ carries the wormhole flare-out. During shell-throat overlap, both contributions are present in the same geometric region.

## Extrinsic curvature and shell motion

The extrinsic curvature of the ADM slice is

$$
K_{ij}
=\frac{1}{2\alpha}
\left(D_i\beta_j+D_j\beta_i-\partial_t\gamma_{ij}\right),
$$

where $D_i$ is the covariant derivative compatible with $\gamma_{ij}$. With

$$
\beta^i=-V(t)S(\rho)n^i,
$$

and

$$
\gamma_{ij}=A^2(\rho)q_{ij},
$$

$K_{ij}$ receives contributions from the velocity $V(t)$, acceleration through $\dot V(t)$ in the time-dependence of the shell center, wall gradients $S'$ and $S''$, capacity gradients $A'$ and $A''$, and the wormhole connection built from $r(l)$ and $\Phi(l)$. The dynamic part of the compatibility question is encoded in the finite behavior of $K_{ij}$ and in its contractions.

The ADM Hamiltonian constraint gives the normal-observer energy density:

$$
16\pi\rho_n
=
{}^{(3)}R[\gamma]+K^2-K_{ij}K^{ij}.
$$

The momentum constraint gives the normal-observer momentum density:

$$
8\pi j_i
=
D_j\left(K^j{}_i-\delta^j{}_iK\right).
$$

These equations locate the stress-energy required by the combined geometry. The shell wall supplies the capacity-gradient terms, the throat supplies the flare-out curvature, and the motion supplies the extrinsic-curvature terms.

## Einstein tensor and energy-condition projections

The stress-energy tensor required by the ansatz is defined by

$$
T_{\mu\nu}=\frac{1}{8\pi}G_{\mu\nu}.
$$

The most relevant projections are the normal energy density,

$$
\rho_n=T_{\mu\nu}n^\mu n^\nu,
$$

and the null projections,

$$
T_{\mu\nu}k^\mu k^\nu
=\frac{1}{8\pi}G_{\mu\nu}k^\mu k^\nu.
$$

The null directions $k^\mu$ include radial outgoing and ingoing families, shell-normal families, and throat-crossing families. Their projections encode where the wormhole exotic matter and the warp-shell capacity matter combine, cancel, or concentrate. A finite, localized, parameter-controlled projection profile is the natural compatibility signature for the proposed family.

An integrated measure of null-energy demand over a spatial slice can be written schematically as

$$
\mathcal N[k]
=
\int_\Sigma
\max\left(0,-T_{\mu\nu}k^\mu k^\nu\right)
dV_\gamma,
$$

where

$$
dV_\gamma=A^3r^2(l)\sin\theta\,dl\,d\theta\,d\phi.
$$

The dependence of $\mathcal N[k]$ on $C_0$, $\Delta$, $r_0$, $r''(0)$, $V$, and $\Phi$ captures how the compact capacity redistributes the exotic support already associated with the two base geometries.

## Throat behavior under capacity scaling

In the spherically symmetric radial reduction, the effective areal radius of the capacity-scaled spatial metric is

$$
\mathcal R(l,t)=A(l,t)r(l).
$$

A throat is represented by a local minimum of $\mathcal R$, equivalently of $\mathcal R^2=A^2r^2$. The throat condition is

$$
\partial_l\left(A^2r^2\right)=0,
$$

with flare-out condition

$$
\partial_l^2\left(A^2r^2\right)>0.
$$

Expanding the first derivative gives

$$
\partial_l\left(A^2r^2\right)
=2AA_lr^2+2A^2rr'.
$$

At the original Morris-Thorne throat, $r'(0)=0$, so

$$
\partial_l\left(A^2r^2\right)\big|_{l=0}
=2A(0,t)A_l(0,t)r_0^2.
$$

The original throat location is preserved at $l=0$ when

$$
A_l(0,t)=0.
$$

When $A_l(0,t)$ is nonzero, the capacity field shifts the minimum-area surface. The shifted throat location satisfies

$$
\frac{A_l}{A}=-\frac{r'}{r}.
$$

This relation gives a precise geometric meaning to the question of what the wormhole throat “sees.” If the compact exterior is the only relevant object, the throat behavior follows the exterior support. If the large interior reappears through $A_l/A$ and higher derivatives, the throat responds to the capacity gradient rather than to the coordinate radius alone.

## Lapse-shift balance and causal surfaces

The ADM metric has

$$
g_{tt}=-\alpha^2+\gamma_{ij}\beta^i\beta^j.
$$

For the radial-axis reduction,

$$
g_{tt}=-e^{2\Phi}T^2+A^2V^2S^2.
$$

The balance surface is therefore

$$
e^{2\Phi(l)}T^2(\rho)=A^2(\rho)V^2(t)S^2(\rho).
$$

This surface records where the shell shift matches the local lapse-scaled spatial capacity. Its appearance, disappearance, and relation to the throat provide a compact causal diagnostic. In the spherically symmetric reduction, radial null expansions can be expressed using the effective areal radius

$$
\mathcal R=A r.
$$

With radial null directions

$$
k_\pm^\mu\partial_\mu
=
\frac{1}{\alpha}\left(\partial_t-\beta^l\partial_l\right)
\pm\frac{1}{A}\partial_l,
$$

the expansions are

$$
\theta_\pm
=\frac{2}{\mathcal R}
\left[
\frac{1}{\alpha}\left(\partial_t-\beta^l\partial_l\right)\mathcal R
\pm
\frac{1}{A}\partial_l\mathcal R
\right].
$$

The products and signs of $\theta_+$ and $\theta_-$ identify trapped, anti-trapped, and marginal regions in the reduced geometry. During shell-throat overlap, these expansions connect the warp shift, the capacity gradient, and the wormhole flare-out in a single geometric expression.

## Shell-throat overlap

The central interaction region is defined by

$$
L(t)\approx0,
\qquad
R_{\mathrm{in}}<\rho<R_{\mathrm{out}}.
$$

There the capacity wall intersects the throat neighborhood. The spatial curvature contains both

$$
{}^{(3)}R[q]
=-\frac{4r''}{r}+\frac{2\left(1-(r')^2\right)}{r^2}
$$

and

$$
-4\Delta_q\ln A-2|\nabla\ln A|^2_q.
$$

The extrinsic curvature contains both the shift gradient and the time-dependence of the moving capacity profile. The throat-area condition contains $A_l/A$ together with $r'/r$. The lapse-shift balance contains $A V S$ together with $e^\Phi T$. The Einstein tensor combines all of these quantities.

This region is the decisive support of the ansatz. Smoothness of the functions gives a smooth metric. Compatibility is represented by finite curvature invariants, controlled Einstein tensor projections, stable throat behavior, and null expansions that preserve traversability through the crossing.

## Compatibility diagnostics

The diagnostic quantities are geometric invariants and geometrically defined projections of the ansatz. The determinant is

$$
\det g=-e^{2\Phi}T^2A^6r^4\sin^2\theta.
$$

The curvature invariants are

$$
R,
\qquad
R_{\mu\nu}R^{\mu\nu},
\qquad
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}.
$$

The Einstein tensor projections are

$$
G_{\mu\nu}n^\mu n^\nu,
\qquad
G_{\mu\nu}k^\mu k^\nu,
\qquad
G_{\mu\nu}u^\mu u^\nu,
$$

where $n^\mu$ is the ADM normal, $k^\mu$ ranges over null directions relevant to the throat and shell wall, and $u^\mu$ ranges over timelike observer fields carried by the interior, wall, and exterior.

The ADM constraint quantities are

$$
{}^{(3)}R+K^2-K_{ij}K^{ij},
$$

and

$$
D_j\left(K^j{}_i-\delta^j{}_iK\right).
$$

The throat quantities are

$$
\partial_l(A^2r^2),
\qquad
\partial_l^2(A^2r^2),
$$

with the reduced null expansions

$$
\theta_\pm
=\frac{2}{Ar}
\left[
\frac{1}{\alpha}\left(\partial_t-\beta^l\partial_l\right)(Ar)
\pm
\frac{1}{A}\partial_l(Ar)
\right].
$$

The compatibility question becomes the behavior of these quantities as functions of

$$
C_0,
\qquad
\Delta,
\qquad
R_{\mathrm{out}},
\qquad
r_0,
\qquad
r''(0),
\qquad
\Phi(l),
\qquad
T_0,
\qquad
V(t).
$$

The mathematical content is especially concentrated in the scaling with $C_0$ and $\Delta$, since

$$
\nabla\ln A\sim\frac{\ln C_0}{\Delta},
\qquad
\Delta_q\ln A\sim\frac{\ln C_0}{\Delta^2}
$$

up to shape-function and wormhole-geometry factors. These scalings determine whether the compact exterior remains a genuinely compact gravitational footprint or whether the hidden interior volume returns as concentrated curvature and stress-energy.

## Deformation hierarchy

The ansatz contains a natural hierarchy of deformations. With $C_0=1$, $T_0=1$, and $V=0$, it is the Morris-Thorne wormhole. With $C_0=1$ and $V\neq0$, it is a moving generalized Bobrick-Martire shell on the wormhole background with unit capacity. With $V=0$ and $C_0>1$, it is a static compact-capacity region placed at or near the throat. With $V\neq0$ and $C_0>1$, it is the full compact-capacity shell crossing problem.

This hierarchy separates the sources of geometric cost. The moving-shell deformation isolates shift and extrinsic curvature. The static-capacity deformation isolates spatial curvature and throat-area response. The full crossing combines shift, capacity, redshift, flare-out, and null expansion behavior.

## Interpretation of outcomes

A compatible family would show that the throat responds primarily to the compact exterior support of the shell, with the large interior remaining geometrically contained by finite wall stresses and controlled causal behavior. In that regime, traversability would depend on the boundary data presented to the wormhole throat rather than on the passenger region’s proper volume alone.

A constrained family would identify where the compact-capacity mechanism deposits its cost. The wall may carry large curvature through $\nabla\ln A$ and $\Delta_q\ln A$. The throat may shift according to $A_l/A=-r'/r$. Null expansions may develop marginal surfaces when the lapse-shift balance aligns with the throat. Einstein tensor projections may concentrate where the capacity wall overlaps the flare-out region. Each outcome gives a precise geometric location for the interaction between the two base mechanisms.

The most informative result is a geometric classification by locus and scaling. The metric family can reveal whether the compact exterior is an invariant operational feature or a coordinate-efficient description whose physical cost reappears through curvature, stress-energy, and causal structure during throat crossing.

## Compact formulation

Let $(\Sigma,q)$ be the spatial slice of a smooth Morris-Thorne wormhole,

$$
q=dl^2+r^2(l)d\Omega^2,
$$

with throat data

$$
r(0)=r_0,
\qquad
r'(0)=0,
\qquad
r''(0)>0.
$$

Let $S(\rho)$ be a smooth compact shell profile in a tubular neighborhood of a radial trajectory $L(t)$, and let

$$
A(\rho)=e^{S(\rho)\ln C_0},
\qquad
T(\rho)=e^{S(\rho)\ln T_0},
\qquad
\beta^i=-\dot L(t)S(\rho)n^i.
$$

The combined metric family is

$$
g
=
-e^{2\Phi(l)}T^2dt^2
+A^2q_{ij}\left(dx^i+\beta^idt\right)\left(dx^j+\beta^jdt\right).
$$

The question becomes whether this family admits parameter regimes in which

$$
\det g\neq0,
$$

curvature invariants remain finite,

$$
G_{\mu\nu}n^\mu n^\nu,
\qquad
G_{\mu\nu}k^\mu k^\nu,
\qquad
G_{\mu\nu}u^\mu u^\nu
$$

remain finite and controlled, the effective throat condition

$$
\partial_l(A^2r^2)=0,
\qquad
\partial_l^2(A^2r^2)>0
$$

is preserved or smoothly displaced, and the radial null expansions

$$
\theta_\pm
=\frac{2}{Ar}
\left[
\frac{1}{\alpha}\left(\partial_t-\beta^l\partial_l\right)(Ar)
\pm
\frac{1}{A}\partial_l(Ar)
\right]
$$

preserve traversability while $L(t)$ carries the shell through $l=0$.

## Closing statement

The original question is represented by a concrete metric family: a Morris-Thorne throat carrying a compact Bobrick-Martire shell with a Van den Broeck-style capacity factor. The throat geometry supplies $r_0$, $r''(0)$, and $\Phi(l)$. The warp shell supplies $S(\rho)$, $V(t)$, and $T(\rho)$. The compact-large capacity mechanism supplies $A(\rho)$ and its wall gradients. Their interaction is concentrated where the shell wall overlaps the throat.

The decisive issue is whether the compact exterior remains the relevant geometric footprint during traversal, or whether the large interior volume returns through the invariant quantities of the combined spacetime. In this ansatz, that issue is carried by $G_{\mu\nu}$, the conformal curvature terms in $A$, the throat-area derivatives of $A^2r^2$, and the null expansions of the effective areal radius $Ar$.

## References

Morris and Thorne introduced the traversable wormhole framework used here in “Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity,” *American Journal of Physics* 56, 395 (1988), available at <https://www.pas.rochester.edu/~tim/introframe/AmJPhysBlackHoles.pdf>.

Bobrick and Martire formulated a general warp-drive framework in ADM language in “Introducing physical warp drives,” *Classical and Quantum Gravity* 38, 105009 (2021), available at <https://arxiv.org/abs/2102.06824>.

Van den Broeck introduced the compact-exterior / large-interior warp-drive modification in “A ‘warp drive’ with more reasonable total energy requirements,” *Classical and Quantum Gravity* 16, 3973 (1999), available at <https://arxiv.org/abs/gr-qc/9905084>.

Alcubierre’s original warp-drive metric appears in “The warp drive: hyper-fast travel within general relativity,” *Classical and Quantum Gravity* 11, L73 (1994), available at <https://arxiv.org/abs/gr-qc/0009013>.

Pfenning and Ford analyzed quantum-inequality constraints on Alcubierre-type warp geometries in *Classical and Quantum Gravity* 14, 1743 (1997), available at <https://arxiv.org/abs/gr-qc/9702026>.

Goldman, D. S. (2022). *An Inquiry on Warp Drives and Wormholes*. Center for Open Science. [https://doi.org/10.31219/osf.io/sre5z](https://doi.org/10.31219/osf.io/sre5z)
