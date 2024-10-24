# Korea Superconducting Tokamak Advanced Research (KSTAR)

## Adaptive ELM control

Ideally, tokamak fusion plasmas are operated at high pressure to benefit fusion performance. However, operating a plasma at high pressure typically results in the destabilization of so-called Edge Localized Modes (ELMs). These ELMs are associated with violent quasi-periodic expulsions of particles and heat. Reactor scale tokamaks are expected not to be able to tolerate ELMs, as the heat load will exceed material limits, thereby damaging the device and reducing availability. Resonant magnetic field perturbation (RMP) is a promising method to control ELMs. However, this often leads to considerable confinement degradation, limiting the fusion gain.

To address these critical issues, we are developing a Feedback ELM Controller aimed at achieving and sustaining full ELM suppression through the application of specific 3D Magnetic perturbations, while maximizing the plasma confinement. The Controller we developed so far has been deployed successfully on the KSTAR tokamak device during experiments, where Feedback achieved ELM suppression has been demonstrated repeatedly. Improvements and extensions of the controller are underway. See the Figure below for an example of ELM suppression by our ELM controller during the 2020 KSTAR campaign.

![Feedback controlled ELM suppression in KSTAR, 2020](../images/kstar_1.png)

In addition, the controller achieved the longest ELM-suppression discharge (world record). This was possible by strong confinement recovery by adaptive 3D control, which enhances non-inductive current fraction and extends the pulse.

![Long-pulse ELM suppression using adaptive 3D control, 2022](../images/kstar_2.png)

Recently, we are adopting the machine-learning algorithm to make a more advanced ELM controller. The major tasks for this control development are

- ELM precursor detection to avoid the loss of ELM suppression.
- Real-time optimization of the 3D spectrum.
- Radiation, density, beta, q95 control.

We are developing and testing these features in KSTAR recently, and expect that the success of control development will provide an ITER-relevant ELM control method.

## MHD modeling on the pedestal stability under RMPs

We are also developing the physics understanding of the role of RMPs on edge pedestal transport and stability. Nonlinear 3D MHD codes are utilized for numerical modeling, and such work will provide physics-based guidance for RMP control.

## 3D Spectroscopy

Coming soon.
