# simulation_3d_COLLAPSE.py - ВКЛЮЧАЕМ ГРАВИТАЦИЮ!
import numpy as np
from scipy.fft import fftn, ifftn
import matplotlib.pyplot as plt

# === УСИЛЕННЫЕ ПАРАМЕТРЫ ===
N = 32
L = 15.0  # Меньше область - сильнее гравитация
dx = L / N
x = np.linspace(-L/2, L/2, N, endpoint=False)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

k = 2*np.pi * np.fft.fftfreq(N, dx)
KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')

# === НАЧАЛЬНОЕ СОСТОЯНИЕ - БОЛЕЕ КОМПАКТНОЕ ===
sigma = 1.5  # Было 3.0 - делаем уже!
psi = np.exp(-(X**2 + Y**2 + Z**2)/(2*sigma**2))
psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx**3)

# === СИЛЬНАЯ ГРАВИТАЦИЯ ===
G_STRONG = 50.0  # БЫЛО 1.0 - УВЕЛИЧИВАЕМ В 50 РАЗ!

def potential(psi):
    rho = np.abs(psi)**2
    rho_k = fftn(rho)
    k2 = KX**2 + KY**2 + KZ**2 + 1e-12
    phi_k = -4 * np.pi * G_STRONG * rho_k / k2  # СИЛЬНАЯ ГРАВИТАЦИЯ!
    return np.real(ifftn(phi_k))

# === ЦИКЛ С КОЛЛАПСОМ ===
psi_history = []
density_peaks = []
print("Starting COLLAPSE simulation...")

for step in range(200):  # Больше шагов
    density = np.abs(psi)**2
    peak = np.max(density)
    
    if step % 20 == 0:
        print(f"Step {step}: max|ψ|² = {peak:.2e}")
        psi_history.append(psi.copy())
        density_peaks.append(peak)
    
    # Кинетика
    psi_k = fftn(psi)
    psi_k *= np.exp(-1j * 0.5 * (KX**2 + KY**2 + KZ**2) * 0.005)  # Меньше dt
    psi = ifftn(psi_k)
    
    # СИЛЬНАЯ гравитация
    Phi = potential(psi) 
    psi *= np.exp(-1j * Phi * 0.005)
    
    # Нормировка
    norm = np.sqrt(np.sum(np.abs(psi)**2) * dx**3)
    if norm > 0:
        psi /= norm

# === ВИЗУАЛИЗАЦИЯ КОЛЛАПСА ===
plt.figure(figsize=(15,5))

plt.subplot(131)
d0 = np.abs(psi_history[0])**2
plt.imshow(d0[:, :, N//2], cmap='hot', extent=[-L/2, L/2, -L/2, L/2])
plt.colorbar()
plt.title(f't=0: {np.max(d0):.2e}')

plt.subplot(132)  
d_mid = np.abs(psi_history[len(psi_history)//2])**2
plt.imshow(d_mid[:, :, N//2], cmap='hot', extent=[-L/2, L/2, -L/2, L/2])
plt.colorbar()
plt.title(f't=mid: {np.max(d_mid):.2e}')

plt.subplot(133)
d_end = np.abs(psi_history[-1])**2
plt.imshow(d_end[:, :, N//2], cmap='hot', extent=[-L/2, L/2, -L/2, L/2])
plt.colorbar() 
plt.title(f't=end: {np.max(d_end):.2e}')

plt.tight_layout()
plt.savefig('COLLAPSE_RESULT.png', dpi=120)
plt.show()

# График роста плотности
plt.figure(figsize=(10,4))
plt.subplot(121)
plt.plot(density_peaks, 'ro-')
plt.yscale('log')
plt.xlabel('Time steps')
plt.ylabel('Peak Density (log)')
plt.title('ГРАВИТАЦИОННЫЙ КОЛЛАПС!')
plt.grid(True)

plt.subplot(122)
plt.plot(density_peaks, 'bo-')
plt.xlabel('Time steps') 
plt.ylabel('Peak Density')
plt.title('Линейная шкала')
plt.grid(True)

plt.tight_layout()
plt.savefig('collapse_growth.png', dpi=120)
plt.show()

print(f"КОЛЛАПС: {density_peaks[0]:.2e} → {density_peaks[-1]:.2e}")
print(f"УВЕЛИЧЕНИЕ в {density_peaks[-1]/density_peaks[0]:.1f} раз!")
