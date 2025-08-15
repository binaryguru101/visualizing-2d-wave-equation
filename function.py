import numpy as np

def validate_stability(length, time, nx, nt, alpha):
    """Validate the stability condition (r < 0.5) for the numerical solution.

    Raises a ValueError if the condition is not met, indicating an unstable
    configuration for the given parameters.
    """
    r = calculate_r(length, time, nx, nt, alpha)
    if r > 0.5:
        raise ValueError(f"Unstable configuration: r={r}. Ensure r < 0.5.")

def check_stability(length, time, alpha, nx_values, nt_values):
    """Finds stable (nx, nt) combinations for the heat equation simulation.

    Iterates through provided nx and nt values, returning a list of tuples
    for all combinations that satisfy the stability criterion (r < 0.5).
    Each tuple contains (length, time, nx, nt, r).
    """
    stable_combinations = []
    epsilon = 1e-10  # Small tolerance for floating-point comparison

    for nx in nx_values:
        dx = length / nx
        for nt in nt_values:
            dt = time / nt
            r = (alpha * dt) / (dx ** 2)

            # Include only stable combinations where r is strictly less than 0.5
            if r < 0.5 and r + epsilon < 0.5:
                stable_combinations.append((length, time, nx, nt, r))

    return stable_combinations

def function_temperature(x, length):
    """Defines the initial temperature distribution as a sine wave."""
    return np.sin(np.pi * x / length)

def calculate_r(length, time, nx, nt, alpha):
    """Calculates the stability factor r = alpha * dt / dx**2."""
    deltax = length / (nx - 1)
    deltat = time / (nt - 1)
    return alpha * deltat / deltax**2

def create_matrices(nx, r):
    """Creates the A and B matrices for the Crank-Nicolson scheme."""
    A = np.eye(nx) - r/2 * (np.eye(nx, k=1) + np.eye(nx, k=-1) - 2 * np.eye(nx))
    B = np.eye(nx) + r/2 * (np.eye(nx, k=1) + np.eye(nx, k=-1) - 2 * np.eye(nx))
    return A, B

def apply_boundary_conditions(matrix):
    """Applies Dirichlet boundary conditions (u=0 at ends) to a matrix."""
    matrix[0, :] = matrix[-1, :] = 0
    matrix[0, 0] = matrix[-1, -1] = 1
    return matrix

def heat_equation_CN(length, nx, time, nt, alpha, function_temperature):
    """Solves the 1D heat equation using the Crank-Nicolson method.

    Args:
        length (float): Length of the rod.
        nx (int): Number of spatial steps.
        time (float): Total simulation time.
        nt (int): Number of time steps.
        alpha (float): Thermal diffusivity.
        function_temperature (callable): Function defining the initial temperature
            profile, T(x, 0).

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing the spatial coordinates (x)
        and the temperature distribution (w) over time.
    """
    validate_stability(length, time, nx, nt, alpha)

    x = np.linspace(0, length, num=nx)
    w = np.zeros([nx, nt])

    for i in range(nx):
        w[i, 0] = function_temperature(x[i], length)

    w[0, :] = w[-1, :] = 0

    r = calculate_r(length, time, nx, nt, alpha)
    
    A, B = create_matrices(nx, r)
    
    A = apply_boundary_conditions(A)
    B = apply_boundary_conditions(B)

    for i in range(1, nt):
        d = B @ w[:, i-1]
        d[0] = d[-1] = 0
        w[:, i] = np.linalg.solve(A, d)

    return x, w

def heat_equation_analytical(length, nx, time, nt, alpha):
    """Calculates the analytical solution to the 1D heat equation.

    This solution is for a rod with an initial temperature of sin(pi*x/L)
    and zero-temperature boundary conditions.

    Args:
        length (float): Length of the rod.
        nx (int): Number of spatial steps.
        time (float): Total simulation time.
        nt (int): Number of time steps.
        alpha (float): Thermal diffusivity.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing the spatial coordinates (x)
        and the analytical temperature distribution (wa) over time.
    """
    validate_stability(length, time, nx, nt, alpha)

    wa = np.zeros([nx, nt])
    t = np.linspace(0, time, num=nt)
    x = np.linspace(0, length, num=nx)
    
    for i in range(nt):
        wa[:, i] = np.sin(np.pi * x / length) * np.exp(-alpha * (np.pi / length)**2 * t[i])
        wa[0, i] = wa[-1, i] = 0
        
    return x, wa