# Source-Shaped Active Rail: Reduced-Design Freeze Report

**Status:** provisional reduced-design freeze  
**Design name:** source-shaped active rail v1  
**Date:** 2026-05-14  
**Scope:** diagnostic source-ledger and design-freeze report, not a peer-reviewed paper, not a constraint solve, and not a matter-model/RSET construction.

## Executive conclusion

The active-rail design can now be refrozen inside the reduced diagnostic family.

The refrozen candidate is:

```text
catch-rematched active rail
+ support-contained throat-gated shift
+ soft angular jacket
+ single long minimum-jerk support-decompression q(s)
+ baseline-subtracted source accounting
```

The important change is not a new transport rule. The original active-rail choreography remains intact: the packet is caught before shift release, and shift remains support-contained. The important change is that the generic frozen support relaxation has been replaced by an explicitly adiabatic support-decompression shoulder. This recovers an earlier design instinct from the adiabatic radial-process work in the repo and makes it explicit again in the active-rail geometry.

The strongest result is that the largest remaining angular-pressure ceiling is mostly a **standing plant-support ledger**, not an **active-service excess**. In the matched holding subtraction, the global angular-pressure ceiling is approximately:

```text
active total |pOmega|      1.286
matched holding |pOmega|   1.283
active excess             0.003
```

At the support edge:

```text
active total |pOmega|      1.194
matched holding |pOmega|   1.189
active excess             0.006
```

The active-service excess that remains during decompression is much smaller:

```text
core decompression active excess |pOmega|          ~0.213
support-edge decompression active excess |pOmega|  ~0.174
```

That changes the interpretation of the remaining pressure problem. It is no longer primarily a failure of the active service choreography. It is the baseline cost of the prepared support plant.

## Frozen reduced candidate

### Fixed architectural rules

```text
1. support-contained shift:
   supp(beta^l) subset supp(A,T)

2. packet ordering:
   catch/rematch before shift fade

3. shift release:
   shift fades while support is still present

4. support relaxation:
   q(s) is a long adiabatic decompression shoulder, not a sharp post-service falloff

5. angular support:
   soft angular jacket remains through fade/decompression and relaxes gently
```

### Working parameters

```text
Angular jacket:
  C_Omega = exp(a_Omega Q_Omega(s) W_Omega(l))
  a_Omega = 0.35
  R_Omega = R_th = 1.25
  w_Omega = 0.70
  x_Omega = 2.00
  w_tOmega = 0.60

Support decompression:
  q(s) = minimum-jerk down-ramp
  t0 = -0.4
  Tr = 3.0
```

The reduced ADM form remains:

```math
ds^2 =
-\alpha(l,s)^2 ds^2
+\gamma_{ll}(l,s)(dl+\beta^l(l,s)ds)^2
+\gamma_{\Omega\Omega}(l,s)d\Omega^2.
```

The refrozen angular closure is:

```math
\gamma_{\Omega\Omega} =
(l^2+R_{\rm th}^2) C_\Omega(s,l)^2.
```

The shift remains throat-gated and packet-localized. The active source demand is interpreted through:

```math
T_{\mu\nu}^{\rm demand} = \frac{1}{8\pi}G_{\mu\nu}[g].
```

The computation in this bundle is still an effective Einstein-source ledger for a prescribed geometry. It is not a proof of physical source availability.

---

# 1. Repo lineage and how the design evolved

This bundle sits downstream of several repo threads.

## 1.1 Adiabatic radial-process work

The earlier repo branch:

```text
warp-complex/quantum-effects-engineering/adiabatic_radial_process/
```

already studied an adiabatic setup/hold/reset protocol. Its memo framed the protocol as:

```text
setup ramp -> quasi-static access hold -> reset ramp
```

and found the key scaling:

```math
\max |\dot B/B| \sim T_r^{-1},
\qquad
\max |T_{\hat t\hat l}| \sim T_r^{-1},
\qquad
\max |\ddot B/B| \sim T_r^{-2}.
```

That earlier result was an engineering-control insight: dynamic support costs can be reduced by making support changes slow. The current work shows that this insight should have remained explicit in the active-rail \(q(s)\) design.

## 1.2 Hybrid flare-gated / catch-rematched work

The later catch-rematched hybrid flare-gated report introduced the active-rail packet-service framing:

```text
hybrid flare-gated throat infrastructure
+ catch-rematched throat-loaded service packet
-> active rail/catch transit geometry
```

It retained several crucial design rules:

```text
support-contained shift
catch before shift fade
shift fade before throat relaxation
quiet access hold as service separation
B/R/N as infrastructure actuators
```

It also distinguished passenger packet diagnostics from stationary infrastructure diagnostics.

The most important inheritance from that stage is the hard packet gate:

```math
x_{\rm catch} < x_\beta < x_q.
```

## 1.3 Active-rail paper package

The current active-rail paper package:

```text
warp-complex/active_rail_paper/
```

turned the service idea into a standalone paper bundle and obstruction screen. It fixed a stressed diagnostic branch at:

```text
V = 10
lambda = 6
```

and showed that caught branches preserve packet clearance while no-catch and late-catch branches fail.

The frozen active-rail screen was a useful packet-service scaffold, but its generic \(q(s)\) was too sharp for source-ledger accounting. In the active-rail diagnostic code, the support relaxation was represented by a compact tanh-like falloff with a relatively narrow width.

That was adequate for packet norm:

```text
active caught branch: packet-positive points = 0
no-catch / late-catch branches: packet-positive points > 0
```

but it was not adequate for the source ledger. Computing the demanded \(G_{\mu\nu}/8\pi\) exposed a dynamic angular-pressure spike during throat relaxation.

## 1.4 What was lost and refound

The adiabatic principle was not abandoned conceptually. It survived as:

```text
quiet hold
smooth release
setup/hold/reset language
service separation
```

But it was weakened in the frozen active-rail metric. The active-rail \(q(s)\) still encoded the right order, but not the right adiabatic shape.

The source-ledger work refound the earlier adiabatic idea in a more precise form:

```text
q(s) should be a long minimum-jerk decompression shoulder,
not a sharp post-service relaxation.
```

This is one of the central progress points of the present bundle.

---

# 2. Literature context and expectations

This work sits at the intersection of wormhole support, warp-drive ADM structure, prepared-route infrastructure, and dynamic-source accounting.

## 2.1 What the literature would lead us to expect

### Traversable wormholes

Morris--Thorne-style wormholes establish the throat-support problem: a traversable throat is not merely a passage but a supported geometric structure. Ford--Roman quantum-inequality work then makes the source burden severe by constraining the magnitude/duration/scale of negative energy. Hochberg--Visser dynamic wormhole work makes the local null-energy pressure unavoidable near dynamic throats.

Expectation from that literature:

```text
The throat/support region will carry a severe source ledger.
Dynamic throat changes will likely make NEC and null-channel behavior worse.
```

The current work agrees with that broad expectation: the burden is not eliminated. But it refines the geography: in the active-rail branch, the most important ledgers are support-edge, angular, and decompression channels, and after baseline subtraction much of the largest angular pressure belongs to the standing plant.

### Warp drives

Alcubierre-style warp drives foreground shift/wall burdens. Pfenning--Ford and later semiclassical work make the wall/source problem severe. Bobrick--Martire reframes warp drives in ADM terms, separating lapse, shift, spatial geometry, capacity, and source roles.

Expectation from that literature:

```text
The dangerous ledger might look like a moving bubble wall or shift shell.
```

The active-rail result is different. The caught active branch does not behave primarily like a passenger-carried bubble wall. The source burden is routed into infrastructure: support edge, angular jacket, and plant decompression.

### Wormhole--warp correspondence

Garattini and Zatrimaylov's wormhole--warp-drive correspondence argues that embedding warp-drive structure in a wormhole background forces one to confront intrinsic curvature and obstruction. It also clarifies why a localized Alcubierre-like bubble through a Morris--Thorne throat is a problematic branch.

Expectation from that literature:

```text
Do not expect a localized bubble crossing a throat to be the good branch.
A structured-background branch has to treat curvature and support as active participants.
```

The active rail follows that expectation. The packet is not the primary geometric engine. The throat plant carries the rail.

## 2.2 Where the literature is vague and this work becomes clearer

The literature usually tells us that the source problem is severe. It is often less explicit about the operational ledger:

```text
which region pays?
which phase pays?
which observer channel sees it?
which actuator matters most?
```

This work clarifies several of those points in the reduced model:

```text
1. Catch/rematch is packet-critical but not the main source-cost event.

2. Shift support containment routes the burden into the infrastructure.

3. The soft angular jacket is a source-routing actuator.
   It improves null and packet-support exposure.

4. The q(s) support relaxation schedule is a pressure actuator.
   Sharp q(s) produces a dynamic angular-pressure spike.

5. The standing plant still carries a large angular-pressure ledger.
   Baseline subtraction is necessary to avoid misreading this as active-service failure.

6. Velocity affects packet-timing failure strongly, but the caught-branch support-edge source burden is mostly geometry dominated over the checked range.
```

The surprising part is not that the source ledger is severe. The surprising part is which knobs mattered most.

---

# 3. What was tested

The work unfolded in layers.

## 3.1 Frozen active-rail source ledger

The first source-ledger question was:

```text
Given the frozen active-rail geometry, what source does it demand?
```

Using a provisional angular closure, the ledger showed:

```text
support-edge / angular / null channels dominate
catch is not the expensive source event
shift fade and throat relaxation are more expensive
packet timelikeness alone is insufficient as a source diagnostic
```

This forced unfreezing of the generic angular and support-relaxation sectors.

## 3.2 Angular closure sweep

The first controlled unfreeze varied only:

```math
\gamma_{\Omega\Omega}.
```

The useful pattern was a soft angular jacket:

```math
C_\Omega(s,l) =
\exp\left[a_\Omega Q_\Omega(s)W_\Omega(l)\right].
```

The jacket needed to be:

```text
mild, not large
broad, not sharp
co-located with the throat support, not a detached shell
persistent through fade/decompression
```

The soft jacket substantially reduced null-channel and packet-support exposure, while preserving packet clearance. It did not significantly reduce the standing angular-pressure ceiling. That was a key surprise.

## 3.3 Velocity check

The velocity check compared low and high transport demand. The main split was:

```text
packet-timing failure: velocity-sensitive
caught-branch source edge burden: mostly geometry/support dominated
```

At lower \(V\), no-catch and late-catch still fail, but not catastrophically. At high \(V=10\), the same failure mode becomes severe. The soft jacket remains useful at both low and high \(V\).

## 3.4 Holding-vs-active decomposition

The next check separated:

```text
standing plant support
active service
reset/decompression
```

This revealed that the remaining angular-pressure ceiling was not mainly catch or shift. It was mostly:

```text
standing angular/throat support
+ throat-relaxation path q(s)
```

That redirected the refinement away from more angular-jacket sweeping and toward \(q(s)\).

## 3.5 Adiabatic q(s)

Replacing the sharp \(q(s)\) falloff with a long minimum-jerk decompression shoulder gave the main closing result.

The best tested shape was:

```text
q(s): minimum-jerk decompression
t0 = -0.4
Tr = 3.0
```

Interpretation:

```text
support decompression begins slowly before the main service interval
support remains adequate through catch and shift fade
support relaxes adiabatically instead of sharply
```

This recovered the earlier adiabatic instinct from the repo.

## 3.6 Burden migration and baseline subtraction

The final checks asked whether the improvement was cheating by moving the burden into:

```text
outer shoulder
far exterior
late reset tail
packet boundary
```

The result was acceptable. The remaining large angular-pressure ceiling is mostly standing support.

---

# 4. Numerical summary

The following table is generated by the included diagnostic script. It compares representative candidates at \(V=10, \lambda=6\).

```text
| case                        |   min_rho_all |   min_rho_pkt_packet_support |   max_abs_j_l_edge |   max_abs_p_l_edge |   max_abs_pOmega_edge |   max_abs_pOmega_all |   min_Tkk_edge |   min_Tkk_packet_support |   packet_positive_points |   edge_gtt_positive_points |   max_packet_norm |   max_gtt_edge |
|:----------------------------|--------------:|-----------------------------:|-------------------:|-------------------:|----------------------:|---------------------:|---------------:|-------------------------:|-------------------------:|---------------------------:|------------------:|---------------:|
| static_sharp_q              |      -0.1029  |                     -0.1658  |            0.1467  |            0.07908 |                 1.286 |                1.378 |        -0.8005 |                  -0.799  |                        0 |                          0 |             -0.75 |         -1     |
| soft_sharp_q                |      -0.03012 |                     -0.04526 |            0.07347 |            0.03143 |                 1.275 |                1.366 |        -0.3232 |                  -0.3196 |                        0 |                          0 |             -0.75 |         -1     |
| soft_wide_tanh_q_w08        |      -0.03572 |                     -0.03803 |            0.02296 |            0.04398 |                 1.145 |                1.304 |        -0.2846 |                  -0.1999 |                        0 |                          0 |             -0.75 |         -1.007 |
| soft_minjerk_q_t0m04_Tr30   |      -0.02798 |                     -0.03773 |            0.03761 |            0.03143 |                 1.146 |                1.309 |        -0.2904 |                  -0.2019 |                        0 |                          0 |             -0.75 |         -1     |
| static_minjerk_q_t0m04_Tr30 |      -0.1029  |                     -0.1378  |            0.0495  |            0.07908 |                 1.158 |                1.322 |        -0.8015 |                  -0.5294 |                        0 |                          0 |             -0.75 |         -1     |
```

## Reading the table

### Static sharp q

This is the unrefined angular/source baseline. It has:

```text
support-edge null burden near -0.80
packet-support null burden near -0.80
support-edge |pOmega| near 1.29
packet clearance still clean
```

This shows why packet norm alone was not enough.

### Soft sharp q

Adding the soft angular jacket improves null and packet-support exposure, but the sharp \(q(s)\) remains a pressure problem.

### Soft wide tanh q

A wide tanh already shows the right direction: slow support relaxation helps. It is nearly competitive with the minimum-jerk version, but has less direct connection to the earlier adiabatic protocol and somewhat less clean reset interpretation.

### Soft minimum-jerk q

This is the freeze candidate. It preserves packet and stationary clearance, retains the jacket's null-channel benefit, and removes the major dynamic relaxation spike.

---

# 5. Baseline-subtracted active excess

The final freeze decision rests on baseline subtraction.

```text
| quantity                                          | region                          | phase                   |   active_total |   matched_holding |   active_excess | interpretation                                  |
|:--------------------------------------------------|:--------------------------------|:------------------------|---------------:|------------------:|----------------:|:------------------------------------------------|
| global |pOmega| ceiling                           | outer shoulder/support geometry | held/early service      |          1.286 |             1.283 |           0.003 | standing plant ledger dominates                 |
| support-edge |pOmega| ceiling                     | support edge                    | held/early service      |          1.194 |             1.189 |           0.006 | standing plant ledger dominates                 |
| core decompression |pOmega| active excess         | core throat                     | adiabatic decompression |          0.262 |             0.049 |           0.213 | remaining active excess, no longer dominant     |
| support-edge decompression |pOmega| active excess | support edge                    | adiabatic decompression |          0.927 |             0.753 |           0.174 | remaining active excess, below standing ceiling |
```

The interpretation is:

```text
The largest remaining |pOmega| is mostly a standing support-plant cost.
The active service excess is comparatively small after the minimum-jerk q(s) change.
```

---

# 6. What surprised us

## 6.1 Catch was not the source-cost bottleneck

Catch/rematch is essential for packet timelikeness. But it was not the dominant source-cost event. The large source events came from support edge, angular geometry, and support relaxation.

That separates two design roles:

```text
catch/rematch = packet choreography
soft jacket + adiabatic q = source routing
```

## 6.2 The angular jacket helped the wrong-looking thing first

The angular jacket barely changed the angular-pressure ceiling at first. That looked disappointing. But it strongly improved null-channel and packet-support exposure, which is exactly where the packet-centered rail needs protection.

So the angular jacket is not primarily a pressure reducer. It is a source-routing / compliance layer.

## 6.3 q(s) mattered more than expected

The sharp \(q(s)\) was acceptable for packet-norm screens, but bad for source-ledger screens. The old adiabatic work predicted this in spirit: dynamic support costs scale with transition rate and acceleration. The active-rail source ledger made that prediction concrete.

## 6.4 The pressure ceiling was mostly standing plant cost

Without subtraction, the remaining angular pressure looked like an active-rail failure. With subtraction, it became mostly a holding-plant ledger. That is a major interpretive correction.

---

# 7. Refrozen reduced design

## 7.1 The design

```text
source-shaped active rail v1
```

is:

```text
1. catch-rematched packet service
2. throat-gated support-contained shift
3. soft angular jacket
4. single long minimum-jerk q(s) decompression shoulder
5. baseline-subtracted source ledger accounting
```

## 7.2 Design rule

The active rail should now be described as:

```text
a packet service through an adiabatically decompressed, angular-jacketed throat rail.
```

More explicitly:

```text
The packet is protected by catch/rematch.
The shift is contained by throat support.
The support edge is protected by a soft angular jacket.
The throat support is not dropped; it is decompressed adiabatically.
```

## 7.3 Do not revert to the generic q(s)

The frozen active-rail paper's generic tanh \(q(s)\) served as a diagnostic scaffold. The refrozen design should not use it as the final source-shaped support schedule.

The support relaxation should be written as an adiabatic control protocol.

---

# 8. What remains outside the freeze

This is a reduced diagnostic freeze, not physical closure.

The following gates remain open:

```text
1. constraint-quality initial data
2. matter/source model
3. null-contracted quantum inequality sampling
4. off-axis null congruences and global causal structure
5. semiclassical RSET/backreaction
6. repeated-cycle accumulation and reset history
7. higher-order/adaptive derivative convergence
8. full angular-sector design beyond the soft jacket
```

The main remaining standing ledger is:

```text
outer/support angular-pressure plant cost
```

That should be assigned to plant support, not mistaken for active-service excess.

---

# 9. Recommended next paper/repo integration

## 9.1 Update active_rail_paper successor

The active-rail paper should not be overwritten casually. A new successor bundle should be created, e.g.:

```text
warp-complex/active_rail_source_analysis/source_shaped_freeze_v1/
```

## 9.2 Include as explicit sections

```text
1. Lineage from adiabatic radial-process protocol
2. Why frozen q(s) was adequate for packet norm but not source ledger
3. Observer-channel source ledger
4. Soft angular jacket sweep
5. Adiabatic q(s) recovery
6. Baseline-subtracted standing vs active ledger
7. Refrozen reduced design
8. Remaining gates
```

## 9.3 Avoid overclaiming

The correct claim is:

```text
In the reduced prescribed-geometry source ledger, the source-shaped active rail routes the active-service excess into controlled infrastructure channels. The main remaining angular-pressure ceiling is mostly a standing plant-support ledger rather than an active-service spike.
```

The incorrect claim would be:

```text
The source problem is solved.
```

It is not.

---

# 10. References and anchors

## Repo anchors

- `warp-complex/quantum-effects-engineering/adiabatic_radial_process/README.md`
- `warp-complex/quantum-effects-engineering/adiabatic_radial_process/adiabatic_radial_process_memo.md`
- `warp-complex/catch_rematched_hybrid_flare_gated_transit/REPORT.md`
- `warp-complex/active_rail_paper/README.md`
- `warp-complex/active_rail_paper/paper/main.tex`
- `warp-complex/active_rail_paper/code/obstruction_screen.py`
- `warp-complex/active_rail_paper/data/obstruction_screen_summary.md`

## Literature anchors

- Morris and Thorne, *Wormholes in spacetime and their use for interstellar travel*, American Journal of Physics, 1988.
- Morris, Thorne, and Yurtsever, *Wormholes, Time Machines, and the Weak Energy Condition*, Physical Review Letters, 1988.
- Alcubierre, *The warp drive: hyper-fast travel within general relativity*, Classical and Quantum Gravity, 1994.
- Ford and Roman, *Quantum field theory constrains traversable wormhole geometries*, Physical Review D, 1996.
- Pfenning and Ford, *The unphysical nature of warp drive*, Classical and Quantum Gravity, 1997.
- Everett and Roman, *Superluminal subway: The Krasnikov tube*, Physical Review D, 1997.
- Hochberg and Visser, *The Null Energy Condition in Dynamic Wormholes*, Physical Review Letters, 1998.
- Van den Broeck, *A warp drive with more reasonable total energy requirements*, Classical and Quantum Gravity, 1999.
- Bobrick and Martire, *Introducing physical warp drives*, Classical and Quantum Gravity, 2021.
- Finazzi, Liberati, and Barceló, *Semiclassical instability of dynamical warp drives*, Physical Review D, 2009.
- Garattini and Zatrimaylov, *On the wormhole--warp drive correspondence*, JCAP, 2024.

---

# 11. One-sentence freeze statement

The refrozen reduced design is a **catch-rematched, support-contained active rail with a soft angular jacket and a long minimum-jerk support-decompression shoulder**, where the remaining angular-pressure ceiling is interpreted as a standing support-plant ledger and the active-service excess has been reduced to a secondary decompression cost.
