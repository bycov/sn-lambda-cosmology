import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Gravitational collapse → mini-Big Bang (no singularity)
t = np.logspace(-30, 1, 1000)  # от Планковского времени
psi_sq = 1 / (1 + (t / 1e-32)**4)  # локализация без сингулярности
a_t = (t / 1e-32)**0.5 * psi_sq**0.25   # масштабный фактор ~ t^{1/2} → 1/t³ энергия

# Λ(t) ∝ 1/t³ — именно то, что нужно для halo freeze и low-l CMB
Lambda_t = 1 / t**3

plt.figure(figsize=(10,6))
plt.loglog(t, a_t, label='a(t) — расширение из коллапса', lw=3)
plt.loglog(t, Lambda_t / Lambda_t[-1], '--', label='Λ(t) ∝ 1/t³', lw=3)
plt.axvline(1e-32, color='red', ls=':', label='момент коллапса')
plt.xlabel('Время с момента коллапса (с)')
plt.title('Collapse-Generator 3D: рождение вселенной без сингулярности')
plt.legend()
plt.grid(alpha=0.3)
plt.show()
