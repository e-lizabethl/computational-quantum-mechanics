## Part 3 notes

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


## transmon = "transmission-line shunted plasma oscillation qubit
a transmon is the specific circuit design used by IBM, Google, and most superconducting qubit companies
- a nonlinear LC oscillator, where an inductor is replaced by a Josephson junction (a thin insulating barrier between two superconductors) to give V(phi) = -E_J cos(phi) instead of pure harmonic 1/2ω^2x^2
- near phi=0, cos(phi) approximation -> harmonic like at the bottom but phi^4 correction makes energy levels unevenly spaced (anharmonic), letting us address the 0 -> 1 transition with a specific drive frquency without also accidentally exciting 1 -> 2. 

transmon hamiltonian: H = 3 E_C nhat^2 - E_J cos(phi hat)
where nhat = - i d/dphi, the charge number operator
E_C, the charging energy; E_J the josephson energy

Lowest 4 eigenvalues: [-40.25679248 -21.31492341  -3.52110135  12.98603842]
E1-E0 = 18.9419   (harmonic approx: sqrt(8*E_C*E_J) = 20.0000)
E2-E1 = 17.7938
Anharmonicity (E2-E1)-(E1-E0) = -1.1480   (analytic approx: -E_C = -1.0000)
saved

this matters because:
we started with a pure harmonic oscillator, showing perfectly even energy spacing, now we show that erplacing the harmonic potential with the actual physical potential used in real superconducting qubits introduces a small, specific, analytically-predictable anharmonicity, the design feature that makes transmons usable two-level systems
because the ladder is no longer even energy spacing betwen E1-E0 and E2-E1, driving at one frequency to control a qubit is off resonance for the other transitions, surpressing them and getting a clean two level system
but if E_J/E_C is too small, weak anharmonicity, transitions blur together and you get leakage, but if is too big, the system becomes highly sensitive to charge noise, random fluctuating electric fields shifting the qubit frequency unpredictably. EJ/EC ~50/100 is used in real transmons as a sweet spot

## rabi oscillations
H(t) = 1/2 ω0​ Z + Ωcos(ωt)X
ω0 qubit natural frequency (from transmon calculation E1-E0=18.94)
Ωcos(ωt)X is a microwave pulse, representing literal microwave radiation applied to the physical qubit chip, how IBM/Google apply single-qubit gates
when ω=ω0 on resonance, you get rabi oscillations, the qubit coherently swaps between ∣0⟩ and ∣1⟩. A pi-pulse, pulse lasting exactly half a rabi period, is how an X-gate is physically implement on real hardware

## T1/T2 theory
what happens on real hardware

- why unitary evolution isn't the whole story
    - so far every simulation has assumed the qubit/particle is perfectly isolated. in reality a physical qubit sits on a chip surrounded by other circuitry, held at a finite temperature, coupled to countless external degree of freedom (phonons, stray photons, nearby defects) -> not truly a closed system, constantly leaking tiny amounts of information into/receiving random kicks from its environment
    -> fundamental fact of any real physical system
- pure state becomes a density matrix (2 x 2 matrix encoding both populations (diagonal) and coherences (off diagonal))
    - rho = rho_00 rho_01
            rho_10 rho_11
    - rho_11 is the probability of measuring ∣1⟩ (same Born rule as before)
    - rho_01 and rho_10 is the coherence, captures the phase relationship between ∣0⟩ and ∣1⟩

- the Lindblad master equation for an open quantum system

T1: energy relaxation
    - T1 is the timescale of the decay of the qubit spontaneously going from 1 -> 0 and emiting energy. Lowering operator L1. 
T2: dephasing

"energy relaxation itself also destroys coherence"
    - if you don't know when the decay happened, you've lost phase information too
-> so T2 is bounded by T1

1/T2 = 1/2T1 + 1/T2*

T2* is the additional, pure dephasing contribution 

- current superconducting qubits (IBM, Google) report T1 and T2 typically in the tens to low hundreds of microseconds, while a single gate operation takes roughly tens of nanoseconds
- so you get roughly 1000-10000 gates before decoherence becomes a serious problem -> therefore quantum error correction exists

- i will take a single qubit but this tim elet it evolve under the lindblad equation instead of a plain unitary circuit. i will track how much is left in ∣1⟩ (population rho_11(t)) and how much quantumness/superposition character is left |rho(01(t))|
- to quantify how quickly 'quantumness' (coherence) disappears

once you have a real T1 and T2 you can directly compare it against your Rabi gate time and if T1,T2 >> 4.37, then your qubit survives comfortably many gate operations before decohering. if comparable, then youd be at the edge of usability

how many gates could I actually perform on this system before it stops being quantum?


