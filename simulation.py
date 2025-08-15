import configparser
import argparse
import numpy as np
from function import heat_equation_CN, heat_equation_analytical, function_temperature, check_stability
from plot import plot_solutions, plot_surface_solution

def process_configuration(config_file):
    """Reads a config file, runs simulations for stable parameters, and plots results.

    This function parses an INI-style configuration file to get simulation
    parameters. It then finds all stable combinations of spatial (nx) and
    temporal (nt) steps, runs both numerical and analytical solutions for each,
    saves the results, and generates plots.

    Args:
        config_file (str): Path to the INI configuration file.

    Raises:
        ValueError: If no stable combinations are found for the given parameters.
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    length = float(config.get('settings', 'length'))
    nx_values = list(map(int, config.get('settings', 'nx_values').split(',')))
    time = float(config.get('settings', 'time'))
    nt_values = list(map(int, config.get('settings', 'nt_values').split(',')))
    alpha = float(config.get('settings', 'alpha'))

    numerical_solution = config.get('paths', 'numerical_solution')
    analytical_solution = config.get('paths', 'analytical_solution')

    # Verify the presence of stable combinations, then solve and plot for those
    stable_combinations = check_stability(length, time, alpha, nx_values, nt_values)
    if not stable_combinations:
        raise ValueError(f"No stable combinations found for parameters in {config_file}.")

    for combination in stable_combinations:
        chosen_length, chosen_time, chosen_nx, chosen_nt, chosen_r = combination

        print(f"Running simulation with nx={chosen_nx}, nt={chosen_nt}, r={chosen_r:.4f}")

        x, w = heat_equation_CN(chosen_length, chosen_nx, chosen_time, chosen_nt, alpha, function_temperature)
        x, wa = heat_equation_analytical(chosen_length, chosen_nx, chosen_time, chosen_nt, alpha)

        np.save(numerical_solution, w)
        np.save(analytical_solution, wa)

        plot_solutions(x, w, wa, chosen_nt, chosen_time, chosen_length, chosen_nx, alpha)
        plot_surface_solution(x, w, chosen_nt, chosen_time, chosen_length, chosen_nx, alpha)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run heat equation simulation with a specific configuration file.")
    # Defines an optional positional argument for the config file path
    parser.add_argument("config_file", nargs="?", default="configurationA.txt")

    args = parser.parse_args()
    process_configuration(args.config_file)