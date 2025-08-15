import matplotlib.pyplot as plt
from function import function_temperature, heat_equation_CN, heat_equation_analytical
import numpy as np

def plot_solutions(x, w, wa, nt, time, length, nx, alpha):
    """Compares the numerical and analytical heat equation solutions.

    Generates a 2D plot showing the temperature profile at four distinct
    time steps to visualize the evolution and accuracy.
    """
    plt.figure(figsize=(12, 6))
    # Select four representative time steps to plot
    timesteps = [0, int(nt/3), int(2*nt/3), nt-1]
    
    for i in timesteps:
        # Plot numerical solution (solid line) and analytical solution (dashed line)
        plt.plot(x, w[:, i], label=f'Numerical t={i*time/(nt-1):.2f}')
        plt.plot(x, wa[:, i], '--', label=f'Analytical t={i*time/(nt-1):.2f}')
    
    plt.xlabel('Position')
    plt.ylabel('Temperature')
    plt.legend()
    plt.title(f'Comparison of Numerical and Analytical Solutions of the Heat Equation\n'
              f'Length={length}, nx={nx}, Time={time}, nt={nt}, Alpha={alpha}')
    plt.show()

def plot_surface_solution(x, w, nt, time, length, nx, alpha):
    """Creates a 3D surface plot of the numerical temperature solution.

    Visualizes the temperature (z-axis) as a function of position (x-axis)
    and time (y-axis) to show the entire solution space.
    """
    # Create a meshgrid for the 3D plot
    X, T = np.meshgrid(x, np.linspace(0, time, nt))
    
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the temperature data as a surface
    ax.plot_surface(X, T, w.T, cmap='viridis') # Transpose w to match meshgrid dimensions
    
    ax.set_xlabel('Position')
    ax.set_ylabel('Time')
    ax.set_zlabel('Temperature')
    ax.set_title(f'3D Surface Plot of the Heat Equation Numerical Solution\n'
                  f'Length={length}, nx={nx}, Time={time}, nt={nt}, Alpha={alpha}')
    plt.show()