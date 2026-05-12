# Stage 1 QI-Management Poke: Static Wormhole Throat

## Purpose

This pass isolates the throat-support problem before adding transport, catch, or passenger coupling. The test uses the standard zero-redshift Morris--Thorne-style proper-radial throat

\[
ds^2=-dt^2+dl^2+r(l)^2d\Omega^2,\qquad r(l)=\sqrt{r_0^2+l^2}.
\]

This is the cleanest place to ask whether a QI-managed source carrier can be brought into the engineering envelope of the throat plant. The transport bubble is absent. The only burden being tested is the persistent flare-out support of the throat.

## Source required by the static throat

For this ultrastatic throat, the orthonormal energy density and pressures are

\[
\rho(l)=-{r_0^2\over 8\pi r(l)^4},
\]

\[
p_l(l)=-{r_0^2\over 8\pi r(l)^4},
\qquad
p_\perp(l)=+{r_0^2\over 8\pi r(l)^4}.
\]

At the throat,

\[
\rho_0=-{1\over 8\pi r_0^2},
\qquad
\rho_0+p_l=-{1\over 4\pi r_0^2}.
\]

The throat therefore asks for a stationary negative energy density and a radial NEC violation. This is the expected Morris--Thorne burden.

## QI proxy

The local Lorentzian-sampling quantum inequality used as a proxy is

\[
\int_{-\infty}^{\infty}\rho(\tau)\,
{\tau_0/\pi\over \tau^2+\tau_0^2}\,d\tau
\geq
-{3\over 32\pi^2\tau_0^4}.
\]

For the static throat, a static observer samples a constant negative density, so the average equals \(\rho_0\). Taking the largest local-flatness sampling time to be

\[
\tau_0=\eta r_0,
\]

the ratio of required negative density to allowed negative density at the throat is

\[
\mathcal R_{\rm QI}
=
{|\rho_0|\over 3/(32\pi^2\tau_0^4)}
=
{4\pi\over 3}\eta^4 r_0^2.
\]

The pass condition is \(\mathcal R_{\rm QI}\leq1\). This gives

\[
r_0\lesssim { \sqrt{3/(4\pi)}\over \eta^2}.
\]

Numerically:

| \(\eta\) | allowed \(r_0\) |
|---:|---:|
| 0.1 | \(4.89\times 10^1 L_P\) |
| 0.03 | \(5.43\times 10^2 L_P\) |
| 0.01 | \(4.89\times 10^3 L_P\) |
| 0.003 | \(5.43\times 10^4 L_P\) |
| 0.001 | \(4.89\times 10^5 L_P\) |

This reproduces the qualitative Ford--Roman result in the simplest possible diagnostic: a smooth static macroscopic throat with persistent negative energy is QI-hostile under this local proxy.

## Pulse-train result

A compensated pulse train was tested in which negative-energy pulses and positive repayment pulses repeat at a period much shorter than the throat curvature scale. This is the intended engineering regime if the classical geometry is supposed to see a smooth envelope.

The result is structural. If the cycle average remains negative enough to support the static throat, then any Lorentzian sampling window large compared with the pulse period recovers approximately that negative mean. If the pulse period is made long enough to avoid this averaged window, the geometry no longer sees a smooth static support and the throat becomes a breathing/dynamic problem.

So pulse management does not save the static throat by itself. It gives a control language for the source, while the averaged negative support remains the QI target.

## Thin-band estimate

The total line-integrated negative energy density for the smooth model is

\[
\int |\rho|\,dl = {1\over 16 r_0}.
\]

As a crude engineering estimate, compressing the same line integral into a band of thickness \(\delta\) gives

\[
|\rho|_{\rm band}\sim {1\over 16r_0\delta}.
\]

Applying the same QI proxy with \(\tau_0=\eta\delta\) gives

\[
\delta^3 \lesssim {16C_{\rm QI}r_0\over \eta^4},
\qquad
C_{\rm QI}={3\over32\pi^2}.
\]

This scaling permits larger absolute \(\delta\) for larger \(r_0\), but the fractional thickness falls as

\[
{\delta\over r_0}\sim r_0^{-2/3}.
\]

For a meter-scale throat, the estimate gives a support band far below ordinary microscopic engineering scales. This is the length-scale-discrepancy version of the Ford--Roman obstruction.

## Stage-1 conclusion

The static throat test says the quantum problem is already present before transport. A pulse carrier can be useful as an engineering representation of the source plant, but it does not change the central averaged-negative-energy constraint when the geometry requires a static mean support.

The useful direction is therefore not simply "pulse the static source and keep the same throat." The useful direction is a dynamic throat-support model with explicit breathing tolerance, repayment zones, and phase-managed access. That becomes Stage 2.

The transport/catch layer should stay out of this test. It can make a working throat usable by a passenger; it does not make the standard throat's static QI support easy.