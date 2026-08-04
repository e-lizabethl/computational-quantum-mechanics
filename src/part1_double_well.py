import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
from solvers import make_grids, make_propagators, split_step_evolve

os.makedirs('figures', exist_ok=True)

N = 2048
L = 30
x, dx, k = make_grids(N, L)

V0, a = 1.0, 1.5
V_dw = V0 * (x**2/a**2 - 1)**2

# Find the two lowest eigenstates
diag = 1/dx**2 + V_dw
offdiag = -0.5/dx**2 * np.ones(N-1)
eigenvalues, eigenvectors = eigh_tridiagonal(diag, offdiag, select='i', select_range=(0, 1))

E_plus, E_minus = eigenvalues
delta_E = E_minus - E_plus
period_theory = 2 * np.pi / delta_E
print(f"E+ = {E_plus:.5f}, E- = {E_minus:.5f}, ΔE = {delta_E:.5f}")
print(f"Theoretical oscillation period: {period_theory:.3f}")

psi_plus = eigenvectors[:, 0]
psi_minus = eigenvectors[:, 1]
psi_plus /= np.sqrt(np.sum(np.abs(psi_plus)**2) * dx)
psi_minus /= np.sqrt(np.sum(np.abs(psi_minus)**2) * dx)

# Fix relative sign so psi_plus + psi_minus localizes on the LEFT well
psi_left_test = psi_plus + psi_minus
left_mass = np.sum(np.abs(psi_left_test[x < 0])**2) * dx
right_mass = np.sum(np.abs(psi_left_test[x > 0])**2) * dx
if right_mass > left_mass:
    psi_minus = -psi_minus

psi_left = (psi_plus + psi_minus) / np.sqrt(2)
print(f"Initial left-well probability: {np.sum(np.abs(psi_left[x<0])**2)*dx:.4f}")

# Evolve and track probability in the left well over time
dt = 0.02
V_half, T_full = make_propagators(x, k, V_dw, dt)

psi = psi_left.astype(complex).copy()
n_total_steps = int(1.2 * period_theory / dt)

times, left_probs = [], []
for step in range(n_total_steps):
    psi = split_step_evolve(psi, V_half, T_full)
    if step % 5 == 0:
        t = step * dt
        p_left = np.sum(np.abs(psi[x < 0])**2) * dx
        times.append(t)
        left_probs.append(p_left)

times, left_probs = np.array(times), np.array(left_probs)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(times, left_probs, label='Numerical: P(left well)')
ax.axvline(period_theory/2, color='red', linestyle='--', label=f'Theory: T/2 = {period_theory/2:.2f}')
ax.axvline(period_theory, color='gray', linestyle=':', label=f'Theory: T = {period_theory:.2f}')
ax.set_xlabel('t')
ax.set_ylabel('P(particle in left well)')
ax.set_title('Quantum tunnelling oscillation in a double well')
ax.legend()
plt.tight_layout()
plt.savefig('figures/double_well_oscillation.png', dpi=120)
print("saved")