## Troterrisation 
we want to implement e^-iHt, the time evolution operator, as an actual quantum circuit -> need to decompose it

our pipeline: simulate circuit, extract observable, compare to exact

- case 1: single Pauli term, no approximation needed (baseline case)
    - if H = 1/2 ω Z then e^-iHt is e^-1/2ωtZ is already a native gate R_z​(ωt)
    - useful for confirming stuff works correctly before introducing real approximation
- case 2: two non-commuting terms (where troterisation becomes necessary)
    - consider H = aX + bZ (field with components along two different axes), and since X and Z don't commute, e^-i(ax+bZ)t is not e^-aXte^-ibZt
    - first order Trotter approximation -> break total time t into n steps, delta_t = t/n and so e^-i(aX+bZ)t is approximately (e^-iaXdeltat_t e^-ibZdelta_t)^n
        - each factor individually a native gate (R_x, R_z)
        - this approximation gets better with more steps because the error shrinks linearly as you increase n (by the Baker-Campbell-Hausdorff formula)
    - second order Trotter -> symmetric splitting giving order delta_t^3 error per step

## Validation strategy
1. Ground truth: compute e−iHt∣ψ0​⟩ exactly, using matrix exponentiation
2. Trotterised circuit: build the gate sequence for given n, extract som observable
3. Compare: plot ⟨Z⟩ vs time for both methods
4. quantify convergence: plot error vs n to confirm it shrinks roughly linearly(first order) or cubically (if summetric splitting)

## Two-qubit interacting system
showing entanglement actually building up over tim eunder Hamiltonian evolution
- entanglement is the concept with no single-particle analogue
- showing entanglement emerges dynamically from physical interaction
    - why real quantum computers are needed for Hamiltonian simulation at scale, classical computers can't efficiently track entanglement
- Physical setup: two interacting spins
H = J Z_1 Z_2 + h(X_1 + X_2)
J Z_1 Z_2 is an interaction term that couples the two qubits, and h(X_1 + X_2) is a local field on each. Z_1 Z_2 doesn't commute X_1 or X_2
- Smart state: ∣00⟩, a completely unentangled product state
- What to track overtime: entanglement entrophy of one qubit (tracing out the other) 
    S = -Tr(rho1 log2 rho1)
    - rho1 is qubit 1's reduced density matrix (obtained by tracing out qubit2)

## Transmon
a transmon is the specific circuit design used by IBM, Google, and most superconducting qubit companies
- a nonlinear LC oscillator, where an inductor is replaced by a Josephson junction (a thin insulating barrier between two superconductors) to give V(phi) = -E_J cos(phi) instead of pure harmonic 1/2ω^2x^2
- near phi=0, cos(phi) approximation -> harmonic like at the bottom but phi^4 correction makes energy levels unevenly spaced (anharmonic), letting us address the 0 -> 1 transition with a specific drive frquency without also accidentally exciting 1 -> 2. 
