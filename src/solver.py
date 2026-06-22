import numpy as np

def make_grids(N, L):
    dx = L / N #spacing between neighbouring points
    # N intervals not N-1: x excludes the right endpoint so the grid is periodic for FFT
    x = np.linspace(-L/2, L/2 - dx, N) #N evenly spaced points
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx) #2pi bc fft returns frequency but we want angular k
    return x, dx, k

N = 1024
L = 200
x, dx, k = make_grids(N, L)

print("dx * N =", dx * N, " (should equal L =", L, ")")
print("k range:", k.min(), "to", k.max(), " (expect about +/-", np.pi / dx, ")")

test = np.random.rand(N)
print("FFT round trip OK:", np.allclose(test, np.fft.ifft(np.fft.fft(test))))