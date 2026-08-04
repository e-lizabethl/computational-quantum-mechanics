import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from solvers import make_grids, gaussian_wavepacket, make_propagators, split_step_evolve

os.makedirs('../figures', exist_ok=True)

N = 2048
L = 300
x, dx, k = make_grids(N, L)

x0, sigma, k0 = -50, 5, 2.0
psi0 = gaussian_wavepacket(x, x0, sigma, k0)

def make_step_potential(x, x_step, V0):
    V = np.zeros_like(x)
    V[x >= x_step] = V0
    return V

x_step = 0        # step located at the origin
# V0 = 1.0   # first test clearly below E ≈ 2.0, should transmit mostly
V0 = 2.0           # step height, comparable to E ≈ k0²/2 = 2.0

V_step = make_step_potential(x, x_step, V0)

dt = 0.05
V_half_step, T_full_step = make_propagators(x, k, V_step, dt)

n_frames = 200
steps_per_frame = 4

psi = psi0.copy()
frames = [np.abs(psi)**2]

#plot in momentum space
psi0_k = np.fft.fft(psi0)
prob_k = np.abs(psi0_k)**2
prob_k = prob_k / (np.sum(prob_k) * (k[1]-k[0]))

k_sorted = np.fft.fftshift(k)
E_k_sorted = k_sorted**2 / 2
prob_k_sorted = np.fft.fftshift(prob_k)

above_mask = E_k_sorted >= V0
frac_above = np.sum(prob_k_sorted[above_mask]) * (k[1]-k[0])
print(f"Fraction of momentum distribution with E >= V0: {frac_above:.3f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(E_k_sorted, prob_k_sorted, color='darkgreen')
ax.axvline(V0, color='red', linestyle='--', label=f'$V_0$ = {V0}')
ax.set_xlim(0, 6)
ax.set_xlabel('Energy E = k²/2')
ax.set_ylabel('Probability density')
ax.set_title('Momentum-space energy distribution of initial wavepacket')
ax.legend()
plt.tight_layout()
plt.savefig('figures/momentum_distribution.png', dpi=120)

for _ in range(n_frames - 1):
    for _ in range(steps_per_frame):
        psi = split_step_evolve(psi, V_half_step, T_full_step)
    frames.append(np.abs(psi)**2)

# Continue evolving further, purely for the R/T measurement,
# beyond what's shown in the animation
extra_steps = 400
for _ in range(extra_steps):
    psi = split_step_evolve(psi, V_half_step, T_full_step)

# norm_check = np.sum(np.abs(psi)**2) * dx
# print("Final normalisation check:", norm_check)

fig, ax = plt.subplots(figsize=(8, 5))

line, = ax.plot(x, frames[0], color='steelblue', label='|ψ(x)|²')
title = ax.set_title('Wavepacket vs potential step, t = 0.00')

ax.set_xlim(x.min(), x.max())
ax.set_ylim(0, max(frames[0]) * 1.3)
ax.set_xlabel('x')
ax.set_ylabel('|ψ(x)|²')

ax2 = ax.twinx()
ax2.plot(x, V_step, color='gray', linestyle='--', alpha=0.6, label='V(x)')
ax2.set_ylabel('V(x)')
ax2.set_ylim(0, V0 * 3)

fig.legend(loc='upper right')

def update(frame_idx):
    line.set_ydata(frames[frame_idx])
    t = frame_idx * steps_per_frame * dt
    title.set_text(f'Wavepacket vs potential step, t = {t:.2f}')
    return line, title

ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=50, blit=False)
ani.save('figures/potential_step_evolution.gif', writer='pillow', fps=20)
print("saved gif")

from solvers import measure_reflection_transmission, theoretical_step_RT

R_numerical, T_numerical = measure_reflection_transmission(psi, x, x_step, dx)
E_mean = k0**2 / 2
R_theory, T_theory = theoretical_step_RT(E_mean, V0)

print(f"Numerical:   R = {R_numerical:.3f}, T = {T_numerical:.3f}")
print(f"Theoretical: R = {R_theory:.3f}, T = {T_theory:.3f}")
