import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
from solvers import make_grids

os.makedirs('figures', exist_ok=True)

N = 1024
L = 40
x, dx, k = make_grids(N, L)

omega = 1.0
V_ho = 0.5 * omega**2 * x**2

diag = 1/dx**2 + V_ho
offdiag = -0.5/dx**2 * np.ones(N-1)

eigenvalues, eigenvectors = eigh_tridiagonal(diag, offdiag, select='i', select_range=(0, 5))

print("Numerical energies:", eigenvalues)
print("Theoretical E_n = (n+0.5)*omega:", [(n+0.5)*omega for n in range(6)])

# normalize eigenvectors (eigh_tridiagonal doesn't guarantee ∫|psi|^2 dx = 1)
for n in range(eigenvectors.shape[1]):
    norm = np.sum(np.abs(eigenvectors[:, n])**2) * dx
    eigenvectors[:, n] /= np.sqrt(norm)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, V_ho, color='black', linewidth=1)

scale = 0.8   # visual scaling so wavefunctions don't overlap each other
for n in range(6):
    psi_n = eigenvectors[:, n]
    ax.plot(x, scale * psi_n + eigenvalues[n], label=f'n={n}')
    ax.axhline(eigenvalues[n], color='gray', linewidth=0.5, linestyle=':')

ax.set_xlim(-6, 6)
ax.set_ylim(0, 7)
ax.set_xlabel('x')
ax.set_ylabel('Energy / ψ(x) (shifted)')
ax.set_title('Harmonic oscillator: eigenstates and energy levels')
ax.legend(loc='upper right', fontsize=8)
plt.tight_layout()
plt.savefig('figures/bound_state_eigenstates.png', dpi=120)