plan.md

classical split-step solver and quantum computer are running the same algorithm
- why? where does the analogy stop?

1. time evolution is applying e^-Ht to a state
    In your solver, the state is a wavefunction sampled on a grid and H is the kinetic-plus-potential operator. On a quantum computer, the state is a register of qubits and H is built from Pauli operators
2. trotterisation
    can't apply exp(-i(T+V)t) directly as T and V don't commute so you split it. a quantum algorithm uses this approximation
3. fourier
    FFT and QFT are same idea but one on amplitudes the other on qubit phases
4. where does this break?
    exponential compression (a grid of N points becomes log2(N) qubits)

Part 1 — Continuous QM simulation (the core, most time invested here): Numerical solution of the time-dependent Schrödinger equation. Four scenarios: free Gaussian wavepacket (spreading, phase evolution), potential step (reflection/transmission), finite barrier tunnelling (transmission coefficient vs energy and width), bound state potential (particle in a box or harmonic oscillator, showing quantisation). Physics is familiar from Year 2, the actual learning is numerical: discretisation, solver choice, boundary handling, extracting clean physical quantities from a wavefunction array.
Part 2 — Qiskit extension (deliberately kept light, now via QGSS rather than self-taught): basic qubit states, superposition, entanglement, measurement statistics. Small, contained, not a software engineering exercise. Certificate secured today, core concepts to be consolidated with me directly given the lab/badge situation.
Part 3 — Interpretation and comparison (the most original, most "you" section): relating the continuous wavefunction picture to the discrete circuit picture, what's physically the same, what's just representation.

Here's how it fits:

Part 1 solves the time-dependent Schrödinger equation directly, you're propagating ψ(x,t) using the split-step Fourier method, applying the time evolution operator numerically on a continuous spatial grid.
Part 2 builds quantum circuits, discrete qubits, gates, measurement.
Part 3 is where Trotterisation becomes the actual connective tissue between them. The core idea: on a quantum computer, you can't directly apply for an arbitrary Hamiltonian, gates only implement specific unitary operations. Trotterisation approximates  by breaking it into small time steps and decomposing the Hamiltonian into a sum of simpler terms, applying each piece's evolution separately in sequence

## what you've built already has a real, honest motivational thread to superconducting qubits (anharmonicity, tunnelling, two-level systems)
Superconducting qubits, the basis of current leading quantum hardware (e.g. IBM's Heron and Nighthawk processors, Google's Willow), rely on deliberately anharmonic potentials to isolate two-level dynamics from a naturally continuous spectrum. This project explores the underlying single-particle quantum mechanics, tunnelling, quantisation, coherent oscillation, that motivates this design choice, before extending into the discrete circuit formalism used to simulate and control such systems.
Google's Willow achieving 99.97% single-qubit gate fidelity is a nice concrete number to cite when discussing why anharmonicity/gate control matters practically

Quantum simulation is literally the founding motivation for quantum computers. Richard Feynman's original 1982 argument for why quantum computers should exist at all
Part 1 solver classically simulates a quantum system (the Schrödinger equation on a grid). Your Part 3 Trotterisation simulates a quantum system using a quantum circuit. You built both sides of Feynman's actual argument
- so i should link why classical simulation becomes intractable as qubit count grows
- How to use this in your writeup responsibly: a short paragraph in your introduction citing 1-2 concrete, real facts (like Google Willow's 99.97% single-qubit fidelity, or IBM's anharmonicity-based gate design), framed as motivation for studying this physics