
import numpy as np
from scipy.ndimage import convolve

class GrayScottSimulation:
    """
    Handles the Gray-Scott reaction-diffusion simulation.
    This version is designed to work with Manim's ValueTrackers
    to allow for real-time parameter changes.
    """
    def __init__(self, size=256, f_tracker=None, k_tracker=None):
        self.size = size
        
        # We now accept Manim ValueTrackers for f and k
        self.f = f_tracker
        self.k = k_tracker
        
        # Diffusion rates
        self.Du, self.Dv = 0.16, 0.08
        
        # Initialize grids
        self.U = np.ones((size, size))
        self.V = np.zeros((size, size))

        mid = size // 2
        r = size // 16
        self.U[mid - r : mid + r, mid - r : mid + r] = 0.50
        self.V[mid - r : mid + r, mid - r : mid + r] = 0.25
        self.U += np.random.rand(size, size) * 0.1
        self.V += np.random.rand(size, size) * 0.1

        # Laplacian kernel
        self.laplacian_kernel = np.array([[0.05, 0.2, 0.05],
                                          [0.2, -1, 0.2],
                                          [0.05, 0.2, 0.05]])

    def step(self, dt=1.0, steps=1):
        """Advance the simulation."""
        f_val = self.f.get_value()
        k_val = self.k.get_value()

        for _ in range(steps):
            Lu = convolve(self.U, self.laplacian_kernel, mode='reflect')
            Lv = convolve(self.V, self.laplacian_kernel, mode='reflect')

            uvv = self.U * self.V**2
            dudt = self.Du * Lu - uvv + f_val * (1 - self.U)
            dvdt = self.Dv * Lv + uvv - (f_val + k_val) * self.V

            self.U += dudt * dt
            self.V += dvdt * dt

    def get_v_channel_as_image(self):
        """Converts the V chemical concentration into a grayscale image array."""
        v_norm = np.clip(self.V, 0, 1)
        return (v_norm * 255).astype(np.uint8)