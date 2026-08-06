import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal

os.makedirs('figures', exist_ok=True)

# Transmon regime: E_J/E_C >> 1 suppresses charge noise while retaining anharmonicity
E_C = 1.0
E_J = 50.0

N = 2048
phi = np.linspace(-np.pi, np.pi, N)
dphi = phi[1] - phi[0]

V = -E_J * np.cos(phi)

# H = 4*E_C*n^2 - E_J*cos(phi), with n = -i d/dphi
# finite-difference kinetic term scaled by 4*E_C instead of 1/2
diag = 4*E_C * 2/dphi**2 + V
offdiag = -4*E_C/dphi**2 * np.ones(N-1)

eigenvalues, eigenvectors = eigh_tridiagonal(diag, offdiag, select='i', select_range=(0, 3))

E01 = eigenvalues[1] - eigenvalues[0]
E12 = eigenvalues[2] - eigenvalues[1]
anharmonicity = E12 - E01

print(f"Lowest 4 eigenvalues: {eigenvalues}")
print(f"E1-E0 = {E01:.4f}   (harmonic approx: sqrt(8*E_C*E_J) = {np.sqrt(8*E_C*E_J):.4f})")
print(f"E2-E1 = {E12:.4f}")
print(f"Anharmonicity (E2-E1)-(E1-E0) = {anharmonicity:.4f}   (analytic approx: -E_C = {-E_C:.4f})")

# Plot potential with the two lowest wavefunctions overlaid
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(phi, V, color='black', linewidth=1)

scale = 3
for n in range(2):
    psi_n = eigenvectors[:, n]
    psi_n /= np.sqrt(np.sum(np.abs(psi_n)**2) * dphi)
    ax.plot(phi, scale*psi_n + eigenvalues[n], label=f'n={n}')
    ax.axhline(eigenvalues[n], color='gray', linestyle=':', linewidth=0.5)

ax.set_xlabel('φ (superconducting phase)')
ax.set_ylabel('Energy / ψ(φ) (shifted)')
ax.set_title(f'Transmon potential (E_J/E_C = {E_J/E_C:.0f}): lowest 2 levels')
ax.legend()
plt.tight_layout()
plt.savefig('figures/transmon_levels.png', dpi=120)
print("saved")