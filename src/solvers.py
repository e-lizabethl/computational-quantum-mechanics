import numpy as np
from scipy.linalg import eigh_tridiagonal

def make_grids(N, L):
    dx = L / N #spacing between neighbouring points
    # N intervals not N-1: x excludes the right endpoint so the grid is periodic for FFT
    x = np.linspace(-L/2, L/2 - dx, N) #N evenly spaced points
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx) #2pi bc fft returns frequency but we want angular k
    return x, dx, k

def gaussian_wavepacket(x, x0, sigma, k0):
    """
    Initial Gaussian wavepacket.

    x0    : initial center position
    sigma : initial width (standard deviation)
    k0    : initial mean momentum (wavenumber)
    """
    norm = (2 * np.pi * sigma**2) ** (-0.25)
    envelope = np.exp(-(x - x0)**2 / (4 * sigma**2))
    phase = np.exp(1j * k0 * x)
    return norm * envelope * phase


def make_propagators(x, k, V, dt):
    """
    Precompute the two evolution factors used in split-step propagation.
    These don't change timestep to timestep (for a static potential),
    so we compute them once and reuse.
    """
    V_half_step = np.exp(-1j * V * dt / 2)      # position space, half step
    T_full_step = np.exp(-1j * k**2 * dt / 2)    # momentum space, full step
    return V_half_step, T_full_step


def split_step_evolve(psi, V_half_step, T_full_step):
    """
    Advance psi by one timestep dt using split-step Fourier method.
    """
    psi = psi * V_half_step          # half potential step (position space)
    psi_k = np.fft.fft(psi)          # move to momentum space
    psi_k = psi_k * T_full_step      # full kinetic step (momentum space)
    psi = np.fft.ifft(psi_k)         # back to position space
    psi = psi * V_half_step          # second half potential step
    return psi

def measure_reflection_transmission(psi, x, x_boundary, dx):
    """
    Measure reflected and transmitted probability by integrating
    |psi|^2 on either side of a boundary point.
    """
    prob_density = np.abs(psi)**2
    R = np.sum(prob_density[x < x_boundary]) * dx
    T = np.sum(prob_density[x >= x_boundary]) * dx
    return R, T

def theoretical_step_RT(E, V0):
    """
    Plane-wave reflection/transmission coefficients for a potential step.
    Assumes hbar = m = 1. Returns (R, T). If E < V0, returns (1.0, 0.0)
    since the classical wave is fully reflected (ignoring evanescent decay).
    """
    if E <= V0:
        return 1.0, 0.0
    k1 = np.sqrt(2 * E)
    k2 = np.sqrt(2 * (E - V0))
    R = ((k1 - k2) / (k1 + k2)) ** 2
    T = 4 * k1 * k2 / (k1 + k2) ** 2
    return R, T

def make_barrier_potential(x, x1, x2, V0):
    V = np.zeros_like(x)
    V[(x >= x1) & (x < x2)] = V0
    return V

def theoretical_barrier_T(E, V0, a):
    """
    Analytical transmission coefficient for a rectangular barrier.
    Handles both E < V0 (tunnelling) and E > V0 (over-barrier) cases.
    """
    if E < V0:
        kappa = np.sqrt(2 * (V0 - E))
        denom = 1 + (V0**2 * np.sinh(kappa * a)**2) / (4 * E * (V0 - E))
    else:
        k2 = np.sqrt(2 * (E - V0))
        denom = 1 + (V0**2 * np.sin(k2 * a)**2) / (4 * E * (E - V0)) if E != V0 else 1 + (V0*a)**2/4
    return 1 / denom

def make_double_well_potential(x, V0, a):
    return V0 * (x**2/a**2 - 1)**2

def transmon_energy_levels(E_C, E_J, N=2048, n_levels=4):
    """Diagonalize the transmon Hamiltonian, return lowest n_levels eigenvalues."""
    phi = np.linspace(-np.pi, np.pi, N)
    dphi = phi[1] - phi[0]
    V = -E_J * np.cos(phi)
    diag = 4*E_C * 2/dphi**2 + V
    offdiag = -4*E_C/dphi**2 * np.ones(N-1)
    eigenvalues, eigenvectors = eigh_tridiagonal(diag, offdiag, select='i', select_range=(0, n_levels-1))
    return eigenvalues, eigenvectors, phi, dphi