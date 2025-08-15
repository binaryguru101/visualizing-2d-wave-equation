import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(layout="wide", page_title="2D Wave Equation Simulator")

st.title("2D Wave Equation Simulator")
st.markdown("Visualize a vibrating membrane using a Fourier series solution. Adjust parameters in the sidebar and see the results.")

# Sidebar for user inputs
st.sidebar.header("Simulation Controls")
st.sidebar.markdown("### Grid & Wave Properties")
LX = st.sidebar.slider("Length of domain (X-axis)", 1.0, 5.0, 1.0)
LY = st.sidebar.slider("Length of domain (Y-axis)", 1.0, 5.0, 1.0)
C = st.sidebar.slider("Wave Speed (c)", 0.5, 5.0, 1.0)

st.sidebar.markdown("### Quality & Performance")
GRID_POINTS = st.sidebar.slider("Grid Resolution", 20, 100, 50, 10)
MODES = st.sidebar.slider("Number of Fourier Modes", 5, 50, 20, 5)

st.sidebar.markdown("### Initial Shape (Gaussian Pluck)")
x0 = st.sidebar.slider("Pluck Center (X-position)", 0.0, LX, LX * 0.6)
y0 = st.sidebar.slider("Pluck Center (Y-position)", 0.0, LY, LY * 0.4)
sigma = st.sidebar.slider("Pluck Width (sigma)", 0.05, 0.5, 0.1)


@st.cache_data
def calculate_fourier_coefficients(lx, ly, grid_pts, modes, pluck_x, pluck_y, pluck_sigma):
    """Calculates the Fourier coefficients based on the initial shape."""
    x = np.linspace(0, lx, grid_pts)
    y = np.linspace(0, ly, grid_pts)
    X, Y = np.meshgrid(x, y)
    dx = lx / (grid_pts - 1)
    dy = ly / (grid_pts - 1)

    # Initial Condition: A Gaussian "Pluck"
    u0 = np.exp(-((X - pluck_x)**2 + (Y - pluck_y)**2) / (2 * pluck_sigma**2))
    
    A_mn = np.zeros((modes, modes))
    for m in range(1, modes + 1):
        for n in range(1, modes + 1):
            sin_mx = np.sin(m * np.pi * X / lx)
            sin_ny = np.sin(n * np.pi * Y / ly)
            integrand = u0 * sin_mx * sin_ny
            A_mn[m-1, n-1] = (4 / (lx * ly)) * np.sum(integrand) * dx * dy
            
    return A_mn, u0

def solve_wave_at_time(t, A_mn, lx, ly, c, grid_pts, modes):
    """Calculates the displacement u(x, y, t) for a given time t."""
    x = np.linspace(0, lx, grid_pts)
    y = np.linspace(0, ly, grid_pts)
    X, Y = np.meshgrid(x, y)
    
    u = np.zeros_like(X)
    for m in range(1, modes + 1):
        for n in range(1, modes + 1):
            omega_mn = c * np.pi * np.sqrt((m / lx)**2 + (n / ly)**2)
            u += A_mn[m-1, n-1] * \
                 np.sin(m * np.pi * X / lx) * \
                 np.sin(n * np.pi * Y / ly) * \
                 np.cos(omega_mn * t)
    return X, Y, u


try:
    with st.spinner("Calculating Fourier coefficients..."):
        coeffs, initial_displacement = calculate_fourier_coefficients(LX, LY, GRID_POINTS, MODES, x0, y0, sigma)
    st.success("Coefficients calculated. Ready to visualize.")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Time Evolution")
    t = st.sidebar.slider("Time (t)", 0.0, 5.0, 0.0, 0.05)
    
    X, Y, U = solve_wave_at_time(t, coeffs, LX, LY, C, GRID_POINTS, MODES)

    st.header(f"Wave displacement at time t = {t:.2f} seconds")
    
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X, Y, U, cmap='viridis', rstride=1, cstride=1)
    
    ax.set_zlim(-1.1, 1.1)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Displacement")
    
    st.pyplot(fig)

except Exception as e:
    st.error(f"An error occurred during the simulation: {e}")