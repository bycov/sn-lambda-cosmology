# simulation.py — 1D Schrödinger–Newton collapse
import numpy as np
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt

# Параметры
N = 256
L = 40.0
dx = L / N
x = np.linspace(-L/2, L/2, N)
dt = 0.01
G = 1.0

# Начальное состояние: суперпозиция двух гауссиан
psi = np.exp(-(x+5)**2) + np.exp(-(x-5)**2)
psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx)

# Функция гравитационного потенциала
def potential(psi):
    rho = np.abs(psi)**2
    k = 2 * np.pi * np.fft.fftfreq(N, dx)
    phi_k = -4 * np.pi * G * fft(rho) / (k**2 + 1e-10)
    return np.real(ifft(phi_k))

# Эволюция
times = [0.0, 0.2, 0.4, 0.6, 1.0]
plt.figure(figsize=(10,6))
for t in times:
    for _ in range(int(t/dt)):
        # Кинетическая часть
        psi_k = fft(psi)
        psi_k *= np.exp(-1j * (np.pi * np.fft.fftfreq(N, dx))**2 * dt)
        psi = ifft(psi_k)
        # Потенциальная часть
        Phi = potential(psi)
        psi *= np.exp(-1j * Phi * dt)
    plt.plot(x, np.abs(psi)**2, label=f't={t}')
plt.legend()
plt.xlabel('x')
plt.ylabel('|ψ|²')
plt.title('Collapse')
plt.savefig('collapse_plot.png')
plt.show()
