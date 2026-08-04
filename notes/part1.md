split step fourier method, standard efficient solver for the time-dependent schrodinger equation
- built spatial and momentum grids
- consructed initial gaussian wavepacket, parameterised by center position, width, and initial momentum
- built the time-evolution operator using the split-step fourier method, where at each timestep:
    1. you apply half a step of potential energy evolution in position space (multiple psi(x) with exp(-V(x)d_t/2hbar))
    2. fourier transform, apply a full step of kinetic energy evolution in momentum space (fft psi into momentum space and multiply by exp(-ihbark^2d_t/2m))
    3. inverse transform, apply the final half step of potential energy (inverse fft back to position space and multiply by exp(-iV(x)d_t/2hbar))
see doc for derivation of split-step method. momentum space bc differentiation becomes multiplication, which is needed for p hat (for kinetic energy term)

units conversion, set hbar =1 and m=1, standard for numerical qm simulations

## 1. free particle
- plot before and after to visually confirm the wavepacket both drifted from its inital momentum k0 and spreaded (quantum effect for free particles)
    - packet moved to the right, and widened, peak height dropped
    - since the gaussian is a superposition of many k-components, each moves at its own group velocity, and since they all travel at slightly different speeds they gradually separate and the packet spreads (smt that distinguishes quantum from classical motion)
    - animated, in figures

## 2. potential step
- since we are using a wavepacket (superposition of many momentums) an dnot a plane wave, we see:
    - part of packet reflects backwards
    - part transmits forward, if E > V0 then this is slower as KE reduced
    - E is not sharply defined (since its a spread of momenta)so should see partial reflection and transmission simultaneously, splitting into two visible packets
    - animated, in figures
    - observe interference of the incident, transmitted and reflected wave at the boundary, created a jagged rippled effect before the pieces fully separate and move apart
- numerically measure the reflection and transmission probabilities by intergrating psi squared over before and after the step to compare against theory
    - derivation in word doc
    - Numerical:   R = 0.690, T = 0.310
    - Theoretical: R = 1.000, T = 0.000
    - for V=2, theory says total reflection, but my simulation shows real transmission (31%) since the wavepacket is a spread of momentum centred on k0=2 so there are components on the distribution above E=2
    - Single-energy scattering theory predicts a sharp step behavior exactly at threshold (E = V0), but any real wavepacket has an energy spread, and that spread is precisely what smooths out the sharp theoretical prediction into partial transmission. The simulation captures physics the idealized plane-wave treatment cannot.
- built momentum-space plot to show visually that a real fraction of the distribution sits above the barrier threshold leading to transmission not being zero.
    - Fraction of momentum distribution with E >= V0: 0.499

## 3. tunnelling through a finite barrier
- classically forbidden, derivation standard result
- Numerical:   R = 0.9950, T = 0.0050
- can't tell on animation so zoomed in + log scale
- want to extract transmission coefficient as a function of energy and barrier width (T vs E curve)
    - at low energies well below V0, T is orders of magnitude larger than plane-wave theory predicts
        - tunnelling probability depends exponentially on energy (T ~ exp(-2sqrt(2(v0-E)a))) so even a small high=energy tail in the wavepacket momentum disribution contributes disproportionately to the average transmission
        - above the barrier, transmission varies only oscillatorily with energy, not exponentially so spread averages out much more normally
    - Tunnelling probability's exponential sensitivity to energy means realistic wavepackets, which always carry some energy spread, transmit substantially more than naive single-energy theory predicts. This effect is most dramatic deep in the classically forbidden region and vanishes above the barrier, where the energy-dependence becomes oscillatory rather than exponential.    

## Bound state 
which wavefunctions don't change shape over time at all, just accumulate an overall phase -> stationary states, solutions to the TISE
-> eigenvalue problem 
    - psi is a finite vector as our grid discretizes space into N points, so H hat acting on psi can be a N x N matrix
    - building potential V hat part -> is diagonal V(x_i) and zero everywhere else
    - building kinetic T hat part -> T hat is -1/2 d2/dx^2 (using hbar = m = 1)
        - use standard finite-difference approximation for second derivative (from taylor expansion) to gi ve 1/dx^2 for diagonal entries and -1/2dx^2 for off-diagonal entries (coupling to immediate neighbours only)
            - tridiagonal matrix -> zero everywhere except the main diagonal and two adjacent diagonals
            - is not exact, accurate to order dx^2. higher states oscillate more and approximations get worse
            - agreement is excellent for low-lying states and degrades predictably for higher states, consistent with the known order dx^2 truncation error of finite-difference discretization, which is more pronounced for rapidly-oscillating higher eigenstates
result: spectrum is evenly spaced by exactly 𝜔=1, between consecutive levels, the hallmark of the harmonic oscillator
- plotted eigenstates stacked on the potential, different E_n

## Double Well
V(x) = V0 (x^2/a^2 -1)^2 two symmetric minima at x= +/-a. 
two lowest eigenstates psi_+ (symmetric) and psi_- (antisymmetric) are nearly degenerate, split by a tiny energy gap delta_E  (tunnelling splitting)
the two psis have very slightly different energies, so this superpositions is not stationary, it evolves. the energies periodically swap into 1/sqrt(2) psi_+ +/- psi_- and back. oscillation period is T = 2pi/delta E
- plot showed clean agreement -> coherent quantum tunnelling
- the operating principle of superconducting flux qubits and charge qubits

## Link
- Bound states → qubits
Harmonic oscillator gives evenly-spaced levels (E_n = (n+0.5)ω). 
Real superconducting qubits use an *anharmonic* oscillator specifically 
so a single drive frequency only excites 0→1, not 1→2 as well. 
Same underlying math (discretized Hamiltonian, eigenvalue problem), 
different design choice (harmonic vs anharmonic) for a different purpose 
(natural physics vs. engineered two-level system).

- Split-step ↔ Trotterisation
Part 1's split-step Fourier method splits e^{-iHt} into alternating 
kinetic/potential pieces. This is structurally the same idea as 
Trotterisation on a quantum circuit: approximate a hard time-evolution 
operator by alternating simpler, individually-implementable pieces.

## Full Part 1 recap:
Free particle: spreading, drift
Potential step: reflection/transmission validated, threshold discrepancy explained via momentum-space spread
Finite barrier: real tunnelling measured, T vs E sweep showing exponential-sensitivity effects
Bound state: quantized energy levels validated to 4 decimal places, node structure visualized, directly bridging to qubit anharmonicity