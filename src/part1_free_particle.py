import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from solvers import make_grids, gaussian_wavepacket, make_propagators, split_step_evolve

N = 1024
L = 200
x, dx, k = make_grids(N, L)

#sanitychecks
# print("dx * N =", dx * N, " (should equal L =", L, ")")
# print("k range:", k.min(), "to", k.max(), " (expect about +/-", np.pi / dx, ")")
# test = np.random.rand(N)
# print("FFT round trip OK:", np.allclose(test, np.fft.ifft(np.fft.fft(test))))

x0 = -50
sigma = 5
k0 = 2.0

psi0 = gaussian_wavepacket(x, x0, sigma, k0)

#check normalisation integral of |psi|^2 dx = 1
# prob_density = np.abs(psi0)**2
# norm_check = np.sum(prob_density) * dx
# print("Normalisation check:", norm_check, " (should be ~1.0)")

V_free = np.zeros_like(x)   # free particle: no potential anywhere

dt = 0.05
V_half_step, T_full_step = make_propagators(x, k, V_free, dt)

# psi = psi0.copy()
# n_steps = 400

# for _ in range(n_steps):
#     psi = split_step_evolve(psi, V_half_step, T_full_step)

# # checking normalisation still 1
# norm_check = np.sum(np.abs(psi)**2) * dx
# print("Normalisation after evolution:", norm_check)

# Precompute all frames first (cleaner than recomputing during animation)
n_frames = 150
steps_per_frame = 4   # skip some steps per frame so the animation isn't too slow to build

psi = psi0.copy()
frames = [np.abs(psi)**2]

for _ in range(n_frames - 1):
    for _ in range(steps_per_frame):
        psi = split_step_evolve(psi, V_half_step, T_full_step)
    frames.append(np.abs(psi)**2)

# Set up the animation
fig, ax = plt.subplots(figsize=(8, 5))
line, = ax.plot(x, frames[0], color='steelblue')
ax.set_xlim(x.min(), x.max())
ax.set_ylim(0, max(frames[0]) * 1.2)
ax.set_xlabel('x')
ax.set_ylabel('|ψ(x)|²')
title = ax.set_title('Free particle wavepacket evolution, t = 0.00')

def update(frame_idx):
    line.set_ydata(frames[frame_idx])
    t = frame_idx * steps_per_frame * dt
    title.set_text(f'Free particle wavepacket evolution, t = {t:.2f}')
    return line, title

ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=50, blit=False)

ani.save('figures/free_particle_evolution.gif', writer='pillow', fps=20)
print("saved gif")

