import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

# Function to read data points from a file
def read_data_points(filename="data.txt"):
    x_vals, y_vals = [], []
    # script_dir is global, data.txt is expected to be in the same dir as the script
    data_file_path = os.path.join(script_dir, filename)
    if not os.path.exists(data_file_path):
        print(f"Error: Data file '{data_file_path}' not found.")
        return None, None
    try:
        with open(data_file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    x_vals.append(float(parts[0]))
                    y_vals.append(float(parts[1]))
    except Exception as e:
        print(f"Error reading data file '{data_file_path}': {e}")
        return None, None
    return x_vals, y_vals

# Function to read coefficients from a file
def read_coefficients(filepath): # Expects full or relative path to coeff file
    coeffs = []
    if not os.path.exists(filepath):
        print(f"Error: Coefficients file '{filepath}' not found in {os.getcwd()}. Full path checked: {os.path.abspath(filepath)}")
        return None
    try:
        with open(filepath, 'r') as f:
            for line in f:
                coeffs.append(float(line.strip()))
    except Exception as e:
        print(f"Error reading coefficients file '{filepath}': {e}")
        return None
    return np.array(coeffs)

# Function to evaluate the polynomial
def polynomial_function(x, coeffs):
    y = 0
    if coeffs is None:
        return np.zeros_like(x) if isinstance(x, np.ndarray) else 0
    for i, c in enumerate(coeffs):
        y += c * (x ** i)
    return y

# Function to calculate residuals
def calculate_residuals(y_data, y_fit):
    return np.array(y_data) - np.array(y_fit)

# Function to calculate R-squared
def calculate_r_squared(y_data, y_fit):
    y_data_np = np.array(y_data)
    y_fit_np = np.array(y_fit)
    y_mean = np.mean(y_data_np)
    ss_total = np.sum((y_data_np - y_mean)**2)
    ss_residual = np.sum((y_data_np - y_fit_np)**2)
    if ss_total == 0: 
        return 1.0 if ss_residual == 0 else 0.0
    return 1 - (ss_residual / ss_total)

def plot_single_degree_fit(x_data, y_data, coefficients, degree, output_filename_base):
    if not x_data: 
        x_plot_range = np.linspace(0, 1, 100)
    else:
        x_plot_range = np.linspace(min(x_data), max(x_data), 400)
    
    y_fit_curve = polynomial_function(x_plot_range, coefficients)
    y_data_fit_points = polynomial_function(np.array(x_data), coefficients)
    r_squared = calculate_r_squared(y_data, y_data_fit_points)

    plt.figure(figsize=(10, 6))
    plt.scatter(x_data, y_data, color='blue', label=f'Data Points')
    plt.plot(x_plot_range, y_fit_curve, color='red', label=f'Fitted Polynomial (Degree {degree})\nR² = {r_squared:.4f}')
    
    plt.title(f'Polynomial Regression Fit (Degree {degree})')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    plot_filename = f"{output_filename_base}_deg{degree}.png"
    laporan_dir = os.path.join(os.path.dirname(script_dir), "Laporan")
    os.makedirs(laporan_dir, exist_ok=True)
    full_plot_path = os.path.join(laporan_dir, os.path.basename(plot_filename))

    try:
        plt.savefig(full_plot_path)
        print(f"Plot saved to {full_plot_path}")
    except Exception as e:
        print(f"Error saving plot {full_plot_path}: {e}")
    plt.close()

def plot_residuals_chart(x_data, y_data, coefficients, degree, output_filename_base):
    if not x_data:
        return

    y_fit_points = polynomial_function(np.array(x_data), coefficients)
    residuals = calculate_residuals(y_data, y_fit_points)

    plt.figure(figsize=(10, 6))
    plt.scatter(x_data, residuals, color='green')
    plt.axhline(0, color='red', linestyle='--', linewidth=0.8)
    
    plt.title(f'Residual Plot for Polynomial Regression (Degree {degree})')
    plt.xlabel('X values')
    plt.ylabel('Residuals (y_data - y_fit)')
    plt.grid(True)

    plot_filename = f"{output_filename_base}_residuals_deg{degree}.png"
    laporan_dir = os.path.join(os.path.dirname(script_dir), "Laporan")
    os.makedirs(laporan_dir, exist_ok=True)
    full_plot_path = os.path.join(laporan_dir, os.path.basename(plot_filename))
    
    try:
        plt.savefig(full_plot_path)
        print(f"Plot saved to {full_plot_path}")
    except Exception as e:
        print(f"Error saving plot {full_plot_path}: {e}")
    plt.close()

def plot_comparative_fit(x_data, y_data, degrees_to_compare, output_filename_base):
    plt.figure(figsize=(12, 7))
    plt.scatter(x_data, y_data, color='blue', label='Data Points', s=30, alpha=0.6)

    if not x_data:
        x_plot_range = np.linspace(0, 1, 100)
    else:
        x_plot_range = np.linspace(min(x_data), max(x_data), 400)

    colors = ['red', 'green', 'purple', 'orange', 'brown', 'pink']

    for i, degree in enumerate(degrees_to_compare):
        # Try parent directory first, then current (script's) directory
        coeff_filename_base = f"coefficients_deg{degree}.txt"
        path_in_parent = os.path.join(os.path.dirname(script_dir), coeff_filename_base)
        path_in_current = os.path.join(script_dir, coeff_filename_base)

        coeffs_to_try = path_in_parent
        if not os.path.exists(coeffs_to_try):
            print(f"File {path_in_parent} not found, trying {path_in_current}")
            coeffs_to_try = path_in_current
        
        print(f"Comparative plot: Reading coefficients for degree {degree} from {coeffs_to_try}")
        coefficients = read_coefficients(coeffs_to_try)
        
        if coefficients is None:
            print(f"Skipping degree {degree} in comparative plot (coefficients file not found at {path_in_parent} or {path_in_current}).")
            continue
        
        y_fit_curve = polynomial_function(x_plot_range, coefficients)
        y_data_fit_points = polynomial_function(np.array(x_data), coefficients)
        r_squared = calculate_r_squared(y_data, y_data_fit_points)
        plt.plot(x_plot_range, y_fit_curve, color=colors[i % len(colors)], label=f'Degree {degree} (R²={r_squared:.3f})')

    plt.title('Comparative Polynomial Regression Fits')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.legend(loc='best')
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    
    degrees_str = '_'.join(map(str, degrees_to_compare))
    plot_filename = f"{output_filename_base}_comparative_deg{degrees_str}.png"
    laporan_dir = os.path.join(os.path.dirname(script_dir), "Laporan")
    os.makedirs(laporan_dir, exist_ok=True)
    full_plot_path = os.path.join(laporan_dir, os.path.basename(plot_filename))

    try:
        plt.savefig(full_plot_path)
        print(f"Plot saved to {full_plot_path}")
    except Exception as e:
        print(f"Error saving plot {full_plot_path}: {e}")
    plt.close()

# Global script_dir for path resolution. This is crucial.
script_dir = os.path.dirname(os.path.abspath(__file__))

def main():
    parser = argparse.ArgumentParser(description="Plot polynomial regression results.")
    parser.add_argument("degree", type=int, nargs='?', default=2,
                        help="Degree of the polynomial for which to plot results (default: 2).")
    parser.add_argument("--compare", nargs='+', type=int, default=[1, 2, 3, 4],
                        help="List of degrees to compare in a single plot. Ensures C++ program has run for these degrees.")
    
    args = parser.parse_args()
    target_degree = args.degree
    degrees_to_compare = args.compare

    # Python script itself is in Program/, so script_dir is Program/
    # Data file is also in Program/
    data_file = "data.txt" 
    output_plot_base_name = "polynomial_regression" 

    x_data, y_data = read_data_points(data_file) # read_data_points uses global script_dir
    if x_data is None or y_data is None:
        print("Exiting due to error reading data points.")
        return

    # --- Plot for the target_degree ---
    coeff_filename_target_base = f"coefficients_deg{target_degree}.txt"
    # Try parent dir first for target degree coeffs
    path_in_parent_target = os.path.join(os.path.dirname(script_dir), coeff_filename_target_base)
    path_in_current_target = os.path.join(script_dir, coeff_filename_target_base)

    coeffs_to_try_target = path_in_parent_target
    if not os.path.exists(coeffs_to_try_target):
        print(f"File {path_in_parent_target} not found, trying {path_in_current_target}")
        coeffs_to_try_target = path_in_current_target
    
    print(f"Single plot: Reading coefficients for degree {target_degree} from {coeffs_to_try_target}")
    coefficients_target = read_coefficients(coeffs_to_try_target)

    if coefficients_target is None:
        print(f"Coefficients for degree {target_degree} not found. Cannot generate individual plots for this degree.")
        print(f"Please ensure C++ program ran and 'coefficients_deg{target_degree}.txt' is in project root or Program/ directory.")
    else:
        print(f"Data points read: {len(x_data)}")
        print(f"Coefficients for degree {target_degree} read: {coefficients_target}")
        plot_single_degree_fit(x_data, y_data, coefficients_target, target_degree, output_plot_base_name)
        plot_residuals_chart(x_data, y_data, coefficients_target, target_degree, output_plot_base_name)

    print(f"\nAttempting to generate comparative plot for degrees: {degrees_to_compare}")
    plot_comparative_fit(x_data, y_data, degrees_to_compare, output_plot_base_name)
    
    print("\nPython script finished.")

if __name__ == "__main__":
    # No os.chdir here, script_dir is used for all relative path constructions
    main()
