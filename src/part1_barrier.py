import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from solvers import (make_grids, gaussian_wavepacket, make_propagators,
                      split_step_evolve, make_barrier_potential,
                      measure_reflection_transmission, theoretical_barrier_T)

os.makedirs('figures', exist_ok=True)

N = 2048
L = 300
x, dx, k = make_grids(N, L)

x0, sigma, k0 = -50, 5, 2.0
psi0 = gaussian_wavepacket(x, x0, sigma, k0)

x1, x2 = 0, 5       # barrier from x=0 to x=5, width a=5
V0 = 3.0             # above mean energy (E=2.0), so this is genuinely classically forbidden

V_barrier = make_barrier_potential(x, x1, x2, V0)

dt = 0.05
V_half_step, T_full_step = make_propagators(x, k, V_barrier, dt)

#normalisation check
# prob_density = np.abs(psi0)**2
# norm_check = np.sum(prob_density) * dx
# print("Normalisation check:", norm_check, " (should be ~1.0)")

n_frames = 250
steps_per_frame = 4

psi = psi0.copy()
frames = [np.abs(psi)**2]

for _ in range(n_frames - 1):
    for _ in range(steps_per_frame):
        psi = split_step_evolve(psi, V_half_step, T_full_step)
    frames.append(np.abs(psi)**2)

extra_steps = 400
for _ in range(extra_steps):
    psi = split_step_evolve(psi, V_half_step, T_full_step)

# --- Animation 1: full view, linear scale (shows overall reflection/transmission) ---
fig1, ax1 = plt.subplots(figsize=(8, 5))
line1, = ax1.plot(x, frames[0], color='steelblue', label='|ψ(x)|²')
title1 = ax1.set_title('Wavepacket vs finite barrier (full view), t = 0.00')

ax1.set_xlim(x.min(), x.max())
ax1.set_ylim(0, max(frames[0]) * 1.3)
ax1.set_xlabel('x')
ax1.set_ylabel('|ψ(x)|²')

ax1b = ax1.twinx()
ax1b.plot(x, V_barrier, color='gray', linestyle='--', alpha=0.6, label='V(x)')
ax1b.set_ylabel('V(x)')
ax1b.set_ylim(0, V0 * 3)
fig1.legend(loc='upper right')

def update1(frame_idx):
    line1.set_ydata(frames[frame_idx])
    t = frame_idx * steps_per_frame * dt
    title1.set_text(f'Wavepacket vs finite barrier (full view), t = {t:.2f}')
    return line1, title1

ani1 = animation.FuncAnimation(fig1, update1, frames=n_frames, interval=50, blit=False)
ani1.save('figures/barrier_evolution_full.gif', writer='pillow', fps=20)
print("saved full view gif")


# --- Animation 2: zoomed, log-scale (shows tunnelling signal) ---
fig2, ax2 = plt.subplots(figsize=(8, 5))
line2, = ax2.plot(x, frames[0], color='steelblue', label='|ψ(x)|²')
title2 = ax2.set_title('Wavepacket vs finite barrier (zoomed, log scale), t = 0.00')

ax2.set_xlim(-30, 30)
ax2.set_yscale('log')
ax2.set_ylim(1e-6, max(frames[0]) * 2)
ax2.set_xlabel('x')
ax2.set_ylabel('|ψ(x)|² (log scale)')

ax2b = ax2.twinx()
ax2b.plot(x, V_barrier, color='gray', linestyle='--', alpha=0.6, label='V(x)')
ax2b.set_ylabel('V(x)')
ax2b.set_ylim(0, V0 * 3)
fig2.legend(loc='upper right')

def update2(frame_idx):
    line2.set_ydata(frames[frame_idx])
    t = frame_idx * steps_per_frame * dt
    title2.set_text(f'Wavepacket vs finite barrier (zoomed, log scale), t = {t:.2f}')
    return line2, title2

ani2 = animation.FuncAnimation(fig2, update2, frames=n_frames, interval=50, blit=False)
ani2.save('figures/barrier_evolution_zoomed.gif', writer='pillow', fps=20)
print("saved zoomed view gif")

R_numerical, T_numerical = measure_reflection_transmission(psi, x, x2, dx)
print(f"Numerical:   R = {R_numerical:.4f}, T = {T_numerical:.4f}")
print(f"(V0={V0} > mean energy E={k0**2/2}, so classically T should be exactly 0)")

k0_values = np.linspace(1.0, 3.0, 12)   # spans below, at, and above V0=3.0's corresponding energy
a = x2 - x1

T_numerical_list = []
E_list = []

for k0_test in k0_values:
    psi_test = gaussian_wavepacket(x, x0, sigma, k0_test)
    psi_evolved = psi_test.copy()

    n_steps_sweep = 1200   # enough for full separation across all tested energies
    for _ in range(n_steps_sweep):
        psi_evolved = split_step_evolve(psi_evolved, V_half_step, T_full_step)

    _, T_num = measure_reflection_transmission(psi_evolved, x, x2, dx)
    E_test = k0_test**2 / 2

    T_numerical_list.append(T_num)
    E_list.append(E_test)
    #print(f"k0={k0_test:.2f}, E={E_test:.3f}, T_numerical={T_num:.4f}")

E_theory = np.linspace(0.3, 6, 200)
T_theory = [theoretical_barrier_T(E, V0, a) for E in E_theory]

fig, ax = plt.subplots(figsize=(8,5))
ax.plot(E_theory, T_theory, color='gray', label='Theory (plane wave)')
ax.plot(E_list, T_numerical_list, 'o', color='crimson', label='Numerical (wavepacket)')
ax.axvline(V0, color='black', linestyle=':', alpha=0.5, label=f'$V_0$={V0}')
ax.set_xlabel('Energy E')
ax.set_ylabel('Transmission coefficient T')
ax.set_yscale('log')
ax.legend()
ax.set_title('Transmission vs Energy: barrier tunnelling')
plt.tight_layout()
plt.savefig('figures/T_vs_E.png', dpi=120)