# 3D Schrödinger-Newton Simulation
# Ready-to-run code for gravitational collapse in 3D

import numpy as np
from scipy.fft import fftn, ifftn
import matplotlib.pyplot as plt

class SchrodingerNewton3D:
    def __init__(self, N=64, L=10.0):
        self.N = N
        self.L = L
        self.dx = 2*L / N
        self.x = np.linspace(-L, L, N, endpoint=False)
        self.dk = 2*np.pi / (2*L)
        self.k = np.fft.fftfreq(N, d=self.dx) * 2*np.pi
        
        # 3D grids
        self.X, self.Y, self.Z = np.meshgrid(self.x, self.x, self.x, indexing='ij')
        self.KX, self.KY, self.KZ = np.meshgrid(self.k, self.k, self.k, indexing='ij')
        self.K2 = self.KX**2 + self.KY**2 + self.KZ**2
        
    def initial_condition(self):
        """Quantum superposition of two Gaussian wavepackets"""
        psi1 = np.exp(-(self.X-2)**2/4 - (self.Y)**2/4 - (self.Z)**2/4)
        psi2 = np.exp(-(self.X+2)**2/4 - (self.Y)**2/4 - (self.Z)**2/4)
        psi = (psi1 + psi2) / np.sqrt(2)
        return psi / np.sqrt(np.sum(np.abs(psi)**2) * self.dx**3)
    
    def gravitational_potential(self, density):
        """Solve Poisson equation for gravitational potential"""
        density_k = fftn(density)
        phi_k = -4*np.pi * density_k / (self.K2 + 1e-10)  # +1e-10 to avoid division by zero
        phi_k[self.K2 == 0] = 0  # set DC component to zero
        return np.real(ifftn(phi_k))
    
    def evolve(self, dt=0.01, steps=1000):
        """Split-step Fourier evolution"""
        psi = self.initial_condition()
        
        for step in range(steps):
            # Kinetic term (half step)
            psi_k = fftn(psi)
            psi_k *= np.exp(-0.5j * dt * self.K2)
            psi = ifftn(psi_k)
            
            # Potential term (full step)
            density = np.abs(psi)**2
            phi = self.gravitational_potential(density)
            psi *= np.exp(-1j * dt * phi)
            
            # Kinetic term (half step)
            psi_k = fftn(psi)
            psi_k *= np.exp(-0.5j * dt * self.K2)
            psi = ifftn(psi_k)
            
            if step % 100 == 0:
                self.plot_slice(psi, step, dt)
                
        return psi
    
    def plot_slice(self, psi, step, dt):
        """Plot 2D slice of the 3D density"""
        density = np.abs(psi)**2
        plt.figure(figsize=(8, 6))
        plt.imshow(density[:, :, self.N//2], extent=[-self.L, self.L, -self.L, self.L])
        plt.colorbar(label='|ψ|²')
        plt.title(f'3D Collapse - t = {step*dt:.2f}')
        plt.savefig(f'collapse_3d_step_{step:04d}.png')
        plt.close()

# Run the simulation
if __name__ == "__main__":
    sim = SchrodingerNewton3D(N=64, L=8.0)
    print("Starting 3D gravitational collapse simulation...")
    final_psi = sim.evolve(dt=0.05, steps=500)
    print("Simulation complete! Check generated PNG files.")
