part2.md

## What is a qubit?
what you get when you take a real physical system of ladder of levels (engineered to be anharmonic in practice) and deliberately restrict attention to just E0 and E1, the two lowest levels. 
everything above is assume inaccessible (either you never drive the system hard enough to reach it, or anharmonicity makes those transiitions require different energy tha the one youre using)
-> a qubit is a truncation of the system

we can therefore write them as two component vectors (as column vectors)
∣0⟩ = (1 0) ground state
∣1⟩ = (0 1) first excited state

general superposition -> a general qubit state is ∣ψ⟩ = α∣0⟩ + β∣1⟩ = (α β) column vector

for a qubit, there are only two possible measurement outcomes, 0 or 1.
P(measure 0) = |alpha|^2 and P(measure 1) = |beta|^2
-> born rule

hadamard gate H takes ∣0⟩ to an equal superposition of alpha = beta = 1/sqrt(2) to give P(0) = P(1) = 0.5

## Entanglement

multi-particle/multi-qubit phenomenon
separable two-qubit state = can be factored into ∣ψ⟩=∣ϕA​⟩⊗∣ϕB​⟩, each qubit has its own independent state
if not = entangled