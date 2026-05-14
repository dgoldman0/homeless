# Active-Rail Einstein Tensor Run Memo

## Purpose

This bundle records the forward Einstein-tensor calculation for the cleaned active-rail metric. The calculation takes the metric ansatz as input, computes the corresponding Einstein tensor, and supplies the tensor components needed for a demanded-source ledger.

The metric evaluated is:

$$
d\Sigma^2 =
-\alpha(\ell,\tau)^2 d\tau^2
+\gamma(\ell,\tau)\left(d\ell+\beta(\ell,\tau)d\tau\right)^2
+R_2(\ell,\tau)d\Omega^2 .
$$

Here $\tau$ is the rail service/evolution coordinate, $\ell$ is the radial rail/throat coordinate, $\alpha$ is the lapse, $\beta=\beta^\ell$ is the rail-direction shift, $\gamma=\gamma_{\ell\ell}$ is the radial spatial metric factor, and $R_2=\gamma_{\Omega\Omega}$ is the angular-sector closure.

## Run result

The symbolic run completed successfully. It generated the generic Einstein tensor for the metric above and wrote the independent components to `active_rail_G_components.txt`.

The demanded classical source is then obtained by:

$$
T_{\mu\nu}^{\rm demand}=\frac{1}{8\pi}G_{\mu\nu}.
$$

This confirms that the active-rail metric ansatz is source-ledger-ready once the profile functions are selected.

## Sanity check results

The resulting tensor has the symmetry structure expected from a spherically symmetric radial service metric.

The nonzero independent Einstein-tensor components are:

$$
G_{\tau\tau},\quad
G_{\tau\ell},\quad
G_{\ell\ell},\quad
G_{\theta\theta},\quad
G_{\phi\phi}.
$$

The angular relation is:

$$
G_{\phi\phi}=\sin^2\theta\,G_{\theta\theta}.
$$

The mixed angular flux components vanish:

$$
G_{\tau\theta}=G_{\tau\phi}=G_{\ell\theta}=G_{\ell\phi}=G_{\theta\phi}=0.
$$

This is the expected structure. The metric contains service-time dependence, radial dependence, radial shift, and spherical angular geometry. The demanded source therefore resolves into energy-density, radial-current, radial-pressure, and angular-pressure channels.

## Physical interpretation of the components

The component $G_{\tau\tau}$ is the coordinate energy-density channel. It carries the source burden associated with lapse shaping, radial capacity, angular closure, and shift structure.

The component $G_{\tau\ell}$ is the radial source-current channel. Its presence is appropriate for an active rail because the service geometry includes a time-dependent radial shift.

The component $G_{\ell\ell}$ is the radial pressure or radial tension channel. It captures the throat-direction support burden.

The angular components $G_{\theta\theta}$ and $G_{\phi\phi}$ are the angular pressure or angular tension channels. These are directly sensitive to the angular closure $R_2(\ell,\tau)$.

## Implications

The calculation establishes that the proposed reduced active-rail metric has a well-defined demanded-source tensor. This directly supports the source-ledger program: after choosing concrete profiles for $\alpha$, $\beta$, $\gamma$, and $R_2$, the tensor can be evaluated numerically and projected into observer/source channels.

The next quantitative evaluations are:

$$
\rho_{\rm Euler}=T_{\mu\nu}n^\mu n^\nu,
$$

$$
T_{\mu\nu}k^\mu k^\nu,
$$

$$
T_{\mu\nu}u^\mu_{\rm pkt}u^\nu_{\rm pkt},
$$

together with radial current, radial pressure/tension, and angular pressure/tension. These are the channels that determine how the active-rail geometry spends its source budget.

The angular closure $R_2=\gamma_{\Omega\Omega}$ is a decisive design choice. The Einstein tensor contains derivatives of $R_2$, including radial, service-time, and mixed derivatives. That means angular capacity, angular jacket behavior, and reset timing directly influence the demanded source.

The derivative structure also matches the paper’s engineering picture. Source demand concentrates where metric profiles change: support edges, catch/rematch layers, shift-fade layers, throat-relaxation layers, and reset shoulders.

## Bundle contents

- `active_rail_G_components.txt` — independent Einstein-tensor components written in SymPy text form.
- `active_rail_run_stdout.txt` — full console output from the successful run.
- `active_rail_run_stderr.txt` — captured runtime diagnostics from the execution environment.
- `active_rail_einstein_tensor.py` — symbolic Python script used to compute the tensor.
- `active_rail_einstein_tensor_memo.md` — this memo.
