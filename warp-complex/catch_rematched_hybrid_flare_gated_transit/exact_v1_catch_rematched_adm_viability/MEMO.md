# Memo: Exact-v1 Catch-Rematched ADM Viability Implications

## Core result

The exact-v1 catch-rematched ADM diagnostic gives a clear engineering reading:

```math
\text{v1 throat infrastructure}
+
\text{catch-rematched packet service}
\longrightarrow
\text{packet-clear active-rail geometry with localized transition-source demand}.
```

The sampled packet worldtube remains timelike. The sampled support edge retains causal margin. The largest engineering burden appears in the catch/release transition structure through the Hamiltonian and momentum source-demand proxies.

The practical design statement is:

```math
\text{pair capacity with lapse, map packet velocity through }B_{\rm v1},
\text{ gate shift through the throat, and optimize transition currents}.
```

## Composite geometry evaluated

The slice diagnostic uses the v1 throat infrastructure metric family

```math
ds^2=-N_{\rm v1}(t,l)^2dt^2+B_{\rm v1}(t,l)^2dl^2+R_{\rm v1}(t,l)^2d\Omega^2,
```

and inserts the catch-rematched packet in ADM form:

```math
ds^2=-\alpha^2dt^2+
\gamma_{ll}(dl+\beta^l dt)^2+
\gamma_{\theta\theta}d\theta^2+
\gamma_{\phi\phi}d\phi^2.
```

The composite fields are

```math
\alpha=N_{\rm v1}(t,l)T_{\rm pkt}(l,X),
```

```math
\gamma_{ll}=B_{\rm v1}(t,l)^2A_{\parallel}(l,X)^2,
```

```math
\gamma_{\theta\theta}=R_{\rm v1}(t,l)^2A_{\perp}(l,X)^2,
\qquad
\gamma_{\phi\phi}=\gamma_{\theta\theta}\sin^2\theta,
```

```math
\beta^l=-U_{\rm coord}(X)E(X)W(l)^{p_\beta}S(l-X).
```

The ADM source-demand proxies are

```math
K_{ij}=\frac{D_i\beta_j+D_j\beta_i-\partial_t\gamma_{ij}}{2\alpha},
```

```math
\rho_H=\frac{{}^{(3)}R+K^2-K_{ij}K^{ij}}{16\pi},
```

```math
j_M^i=\frac{D_j(K^{ij}-\gamma^{ij}K)}{8\pi}.
```

The packet diagnostic is

```math
\mathcal N_{\rm pkt}=-\alpha^2+
\gamma_{ll}\left(U_{\rm coord}+\beta^l\right)^2.
```

The support-edge stationary monitor is

```math
g_{tt}=-\alpha^2+
\gamma_{ll}(\beta^l)^2.
```

## Implementation commitments that matter physically

### Capacity and lapse are one service field

The packet uses

```math
A_{\parallel}=\exp\left(qW^{p_A}\ln C_0\right),
```

```math
T_{\rm pkt}=\exp\left(qW^{p_A}\ln(\lambda C_0)\right),
```

which gives

```math
\frac{T_{\rm pkt}}{A_{\parallel}}=\lambda^{qW^{p_A}}.
```

This is an engineering rule. Spatial capacity and lapse support travel as a matched throat-service field. Capacity by itself creates a larger radial metric load; paired lapse support supplies the causal margin that makes the service packet coherent.

### v1 radial stretch defines the packet coordinate velocity

The v1 geometry stretches radial proper distance through

```math
\gamma_{ll}=B_{\rm v1}^2A_{\parallel}^2.
```

A packet service speed stated in proper-radial units maps to coordinate speed by

```math
U_{\rm coord}=\frac{U_{\rm proper}}{B_{\rm v1}(X)}.
```

This makes the catch-rematched choreography B-aware. The throat stretch helps the infrastructure by spreading proper distance, and the packet shift amplitude follows that stretched coordinate map.

### Transition source-current demand is the next design object

The packet and support-edge causal monitors clear the atlas. The source-demand proxies mark the active work zone. The highest p95 Hamiltonian and momentum source-demand values appear in the packet-adjacent and edge-adjacent transition bands:

```math
\rho_H \quad\text{tracks local Hamiltonian source demand},
```

```math
j_M \quad\text{tracks momentum/current demand from shift and geometry gradients}.
```

This identifies the next engineering target: smooth and minimize the catch/release source-current structure while preserving packet and edge clearance.

## Atlas results

Both atlases used

```math
N_l\times N_\theta\times N_\phi=81\times33\times8,
```

sampled ten packet-center locations,

```math
X\in[-0.35,1.45],
```

and compared three R treatments:

```math
R\in\{\text{v1 schedule},\text{always open},\text{delayed close}\}.
```

### Nominal service atlas

Command:

```bash
python code/adm_3p1_viability_v3_baware.py --atlas --outdir results/atlas_V5 --nl 81 --nth 33 --nph 8
```

Parameters:

```math
V=5,
\qquad
\lambda=5.75,
\qquad
p_\beta=1.
```

| quantity | value |
|---|---:|
| atlas slices | 30 |
| packet-clear slices | 30 |
| support-edge-clear slices | 30 |
| max packet norm | -0.6957815076 |
| max support-edge `g_tt` | -1.4109172423 |
| max packet `rho_H` p95 abs | 0.1910628892 |
| max support-edge `rho_H` p95 abs | 0.1319480799 |
| max packet `j_M` p95 abs | 0.0248643260 |
| max support-edge `j_M` p95 abs | 0.0654635953 |

Worst packet-norm slice:

| field | value |
|---|---:|
| X | 0.65 |
| R mode | v1 schedule |
| proper packet speed | 0.5522329240 |
| coordinate packet speed | 0.0690302010 |
| packet max norm | -0.6957815076 |
| packet max `g_tt` | -1.0008798001 |
| edge max `g_tt` | -17.7779166885 |

### High-stress edge-cleanup atlas

Command:

```bash
python code/adm_3p1_viability_v3_baware.py --atlas --outdir results/atlas_V10_lam6_p4 --V 10 --lambda-factor 6 --p-beta 4 --atlas-r-modes v1,always_open,delayed_close --nl 81 --nth 33 --nph 8
```

Parameters:

```math
V=10,
\qquad
\lambda=6,
\qquad
p_\beta=4.
```

| quantity | value |
|---|---:|
| atlas slices | 30 |
| packet-clear slices | 30 |
| support-edge-clear slices | 30 |
| max packet norm | -0.6282630564 |
| max support-edge `g_tt` | -1.4141740254 |
| max packet `rho_H` p95 abs | 0.1910630830 |
| max support-edge `rho_H` p95 abs | 0.1319480799 |
| max packet `j_M` p95 abs | 0.0244419195 |
| max support-edge `j_M` p95 abs | 0.0602274438 |

Worst packet-norm slice:

| field | value |
|---|---:|
| X | 0.65 |
| R mode | v1 schedule |
| proper packet speed | 0.6102695062 |
| coordinate packet speed | 0.0762848879 |
| packet max norm | -0.6282630564 |
| packet max `g_tt` | -1.0008856958 |
| edge max `g_tt` | -18.1741801870 |

## Engineering lessons

### 1. The combined design gives a packet-clear service geometry

The exact-v1 ADM atlas gives packet-clear and edge-clear slices across the nominal and high-stress samples. The result supports the active-rail interpretation:

```math
\text{the throat is the service apparatus},
\qquad
\text{the packet is the protected worldtube}.
```

This is the central engineering gain from combining v1 throat infrastructure with the catch-rematched transit packet.

### 2. B-aware choreography is part of the design

The v1 prestretch field changes the coordinate map of service motion. Packet speed, shift amplitude, catch timing, and release timing should be specified with both proper-radial and coordinate-radial readings.

A practical timing chart should carry both axes:

```math
X_{\rm coord},
\qquad
s_{\rm proper}=\int B_{\rm v1}(t,l)A_{\parallel}(l,X)\,dl.
```

### 3. Source-current demand is the active engineering burden

The ADM proxies place the main cost in the transition apparatus. The system asks for a source architecture that supplies localized Hamiltonian demand and momentum/current demand during catch and release.

The next optimization target is therefore

```math
\min_{E,q,C_{\rm catch},W,p_\beta}
\left[
\max |\rho_H|_{\rm transition}
+
\max |j_M|_{\rm transition}
+
\max |K|_{\rm transition}
\right]
```

subject to packet and support-edge clearance.

### 4. Edge shaping is a real actuator

The high-stress atlas uses

```math
\beta^l\propto W^{p_\beta},
\qquad
p_\beta=4,
```

and retains support-edge margin. This makes edge shaping an engineering knob. The next sweep should optimize p-beta against source-gradient demand, because stronger edge suppression changes the spatial derivatives that feed `rho_H`, `j_M`, and `K`.

### 5. R-open and delayed-close are service-support choices

The exact-v1 viability atlas supports the R-open and delayed-close service posture established in the reduced screens. In the combined design, R supplies flare reserve and angular geometry support during packet service. Reset happens after the packet-critical interval.

This shifts R from a passenger-safety switch into a throat-service shape actuator.

## Comparison to field expectations

### Morris-Thorne and Ford-Roman wormhole expectations

Morris-Thorne traversable wormholes establish the throat as the geometric object that requires exotic support. Ford-Roman quantum-inequality analysis makes the source-duration and source-thickness burden central for macroscopic traversable wormholes. The present work accepts that source burden as the supplied-resource assumption and evaluates the engineering geometry under that assumption.

Our contribution is the packet/infrastructure split:

```math
\text{wormhole throat support}
\longrightarrow
\text{active throat apparatus carrying packet service}.
```

This gives a more specific engineering target than a generally habitable throat.

### Alcubierre, Van den Broeck, and warp-shell expectations

Alcubierre-style superluminal warp metrics place the hard geometry in a moving warp bubble. Van den Broeck-style capacity factors reduce external footprint while increasing interior capacity complexity. The combined design uses the capacity idea while assigning the high-burden geometry to the throat infrastructure.

The ADM result supports the design rule:

```math
\text{capacity belongs with lapse and shift support inside the service apparatus}.
```

### Everett-Roman Krasnikov infrastructure expectation

Everett-Roman identify prepared spacetime infrastructure as the control resolution for bubble-wall causal separation. The combined design realizes that lesson in a throat-localized service channel:

```math
\text{prepared route infrastructure}
\longrightarrow
\text{prepared throat service apparatus}.
```

The catch-rematched packet gives the passenger-side operational layer that the infrastructure requires.

### Bobrick-Martire and modern warp-shell expectations

Bobrick-Martire frame warp geometries through ADM role separation: lapse, shift, spatial geometry, capacity, and shell motion. Fuchs et al. demonstrate the value of numerical ADM-style evaluation for a constant-velocity subluminal shell with a shift-vector distribution and a matter shell.

The present work extends that engineering style to a source-supplied superluminal/transit setting by combining:

```math
\text{ADM role separation}
+
\text{v1 throat controls}
+
\text{catch-rematched packet choreography}
+
\text{packet/edge/source-demand atlas}.
```

### Gao-Jafferis-Wall controlled traversability expectation

Gao-Jafferis-Wall show that timed negative averaged null energy can make an Einstein-Rosen bridge traversable in a controlled holographic setting. The shared lesson is source-history choreography. The combined design expresses that lesson in engineering variables: catch profile, shift release profile, throat relaxation profile, and source-current demand.

## What this work clarifies beyond the literature ingredients

The literature gives the components: throats, warp shells, capacity factors, prepared infrastructure, ADM role separation, and controlled traversability. The present work clarifies the engineering integration:

```math
\boxed{
\text{source-supplied FTL viability is governed by service-packet clearance and transition-current engineering.}
}
```

The field-relevant takeaways are:

1. **Passenger safety is a worldtube diagnostic.** The packet norm provides the service criterion for the moving passenger region.
2. **The throat apparatus carries the hard geometry.** v1 controls become infrastructure actuators: B for stretch and burden smoothing, R for flare reserve, N for matching and shoulder timing.
3. **Capacity, lapse, and shift form one managed service system.** The ADM atlas supports the paired capacity/lapse construction and throat-gated shift support.
4. **The support edge is an engineered component.** p-beta controls edge behavior and sets a source-gradient trade space.
5. **The transition layer is the next feasibility object.** `rho_H`, `j_M`, and `K` identify the catch/release source-current problem.

## Confidence update under source availability

The work raises conditional engineering confidence in the combined design.

The current atlas supports:

```math
\text{packet-clear transit slices},
```

```math
\text{support-edge causal margin},
```

```math
\text{B-aware catch/rematch choreography},
```

```math
\text{localized source-demand targets for the transition apparatus}.
```

The next reduced task is source-current optimization in the transition layer. The design target is explicit:

```math
\text{smooth }E(X),q(X),C_{\rm catch}(X),W(l),p_\beta
\text{ to reduce }\rho_H,j_M,K
\text{ while preserving packet and edge clearance.}
```

## Data and code included

Code:

- `code/adm_3p1_viability_v3_baware.py`

Nominal atlas:

- `results/atlas_V5/atlas_summary.json`
- `results/atlas_V5/atlas_compact.csv`
- per-slice `*_summary.json`, `*_midplane.csv`, and `*_tensors.npz`

High-stress atlas:

- `results/atlas_V10_lam6_p4/atlas_summary.json`
- `results/atlas_V10_lam6_p4/atlas_compact.csv`
- per-slice `*_summary.json`, `*_midplane.csv`, and `*_tensors.npz`

## References

- Morris, M. S. and Thorne, K. S. “Wormholes in spacetime and their use for interstellar travel.” *American Journal of Physics* 56, 395–412 (1988). DOI: `10.1119/1.15620`.
- Ford, L. H. and Roman, T. A. “Quantum field theory constrains traversable wormhole geometries.” *Physical Review D* 53, 5496–5507 (1996). DOI: `10.1103/PhysRevD.53.5496`. APS: <https://journals.aps.org/prd/abstract/10.1103/PhysRevD.53.5496>.
- Alcubierre, M. “The warp drive: hyper-fast travel within general relativity.” *Classical and Quantum Gravity* 11, L73–L77 (1994). DOI: `10.1088/0264-9381/11/5/001`.
- Van den Broeck, C. “A ‘warp drive’ with more reasonable total energy requirements.” *Classical and Quantum Gravity* 16, 3973–3979 (1999). DOI: `10.1088/0264-9381/16/12/314`.
- Everett, A. E. and Roman, T. A. “Superluminal subway: The Krasnikov tube.” *Physical Review D* 56, 2100–2108 (1997). DOI: `10.1103/PhysRevD.56.2100`. APS: <https://journals.aps.org/prd/abstract/10.1103/PhysRevD.56.2100>.
- Bobrick, A. and Martire, G. “Introducing physical warp drives.” *Classical and Quantum Gravity* 38, 105009 (2021). DOI: `10.1088/1361-6382/abdf6e`. Monash record: <https://research.monash.edu/en/publications/introducing-physical-warp-drives>.
- Gao, P., Jafferis, D. L. and Wall, A. C. “Traversable wormholes via a double trace deformation.” *Journal of High Energy Physics* 2017, 151 (2017). DOI: `10.1007/JHEP12(2017)151`. Springer: <https://link.springer.com/article/10.1007/JHEP12(2017)151>.
- Fuchs, J., Helmerich, C., Bobrick, A., Sellers, L., Melcher, B. and Martire, G. “Constant velocity physical warp drive solution.” *Classical and Quantum Gravity* 41, 095013 (2024). DOI: `10.1088/1361-6382/ad26aa`. Monash record: <https://research.monash.edu/en/publications/constant-velocity-physical-warp-drive-solution>.
- Helmerich, C., Fuchs, J., Bobrick, A., Sellers, L., Melcher, B. and Martire, G. “Analyzing warp drive spacetimes with Warp Factory.” *Classical and Quantum Gravity* 41, 095009 (2024). DOI: `10.1088/1361-6382/ad2e42`. Monash record: <https://research.monash.edu/en/publications/analyzing-warp-drive-spacetimes-with-warp-factory>.
