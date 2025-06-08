import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

# Fungsi untuk membaca titik-titik data dari file
# Input: filename (string) - nama file data (default: "data.txt")
# Output: tuple (list_x, list_y) - dua list berisi nilai x dan y, atau (None, None) jika error
def read_data_points(filename="data.txt"):
    x_vals, y_vals = [], []
    # script_dir bersifat global, diasumsikan data.txt berada di direktori yang sama dengan skrip
    data_file_path = os.path.join(script_dir, filename)
    if not os.path.exists(data_file_path):
        print(f"Error: File data '{data_file_path}' tidak ditemukan.")
        return None, None
    try:
        with open(data_file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2: # Pastikan ada dua nilai per baris
                    x_vals.append(float(parts[0]))
                    y_vals.append(float(parts[1]))
    except Exception as e:
        print(f"Error saat membaca file data '{data_file_path}': {e}")
        return None, None
    return x_vals, y_vals

# Fungsi untuk membaca koefisien dari file
# Input: filepath (string) - path lengkap atau relatif ke file koefisien
# Output: numpy array berisi koefisien, atau None jika error
def read_coefficients(filepath): 
    coeffs = []
    if not os.path.exists(filepath):
        print(f"Error: File koefisien '{filepath}' tidak ditemukan di {os.getcwd()}. Path lengkap yang dicek: {os.path.abspath(filepath)}")
        return None
    try:
        with open(filepath, 'r') as f:
            for line in f:
                coeffs.append(float(line.strip()))
    except Exception as e:
        print(f"Error saat membaca file koefisien '{filepath}': {e}")
        return None
    return np.array(coeffs)

# Fungsi untuk mengevaluasi nilai polinomial pada titik x tertentu
# Input: x (float atau numpy array) - nilai x
#        coeffs (numpy array) - koefisien polinomial [a0, a1, a2, ...]
# Output: y (float atau numpy array) - nilai polinomial P(x)
def polynomial_function(x, coeffs):
    y = 0
    if coeffs is None: # Jika tidak ada koefisien, kembalikan nol
        return np.zeros_like(x) if isinstance(x, np.ndarray) else 0
    for i, c in enumerate(coeffs): # Hitung y = a0*x^0 + a1*x^1 + ...
        y += c * (x ** i)
    return y

# Fungsi untuk menghitung residual
# Residual = y_data - y_fit
# Input: y_data (list atau numpy array) - nilai y aktual
#        y_fit (list atau numpy array) - nilai y yang diprediksi oleh model
# Output: numpy array berisi residual
def calculate_residuals(y_data, y_fit):
    return np.array(y_data) - np.array(y_fit)

# Fungsi untuk menghitung R-squared (koefisien determinasi)
# R-squared = 1 - (SS_residual / SS_total)
# Input: y_data (list atau numpy array) - nilai y aktual
#        y_fit (list atau numpy array) - nilai y yang diprediksi oleh model
# Output: float - nilai R-squared
def calculate_r_squared(y_data, y_fit):
    y_data_np = np.array(y_data)
    y_fit_np = np.array(y_fit)
    y_mean = np.mean(y_data_np) # Rata-rata y_data
    ss_total = np.sum((y_data_np - y_mean)**2) # Sum of Squares Total
    ss_residual = np.sum((y_data_np - y_fit_np)**2) # Sum of Squares Residual
    if ss_total == 0: # Hindari pembagian dengan nol jika semua y_data sama
        return 1.0 if ss_residual == 0 else 0.0 # Jika residual juga nol, R2=1, jika tidak R2=0
    return 1 - (ss_residual / ss_total)

# Fungsi untuk membuat plot regresi polinomial untuk satu derajat tertentu
def plot_single_degree_fit(x_data, y_data, coefficients, degree, output_filename_base):
    if not x_data: # Jika tidak ada data x, buat rentang default
        x_plot_range = np.linspace(0, 1, 100)
    else: # Buat rentang x untuk plot dari min hingga max data x
        x_plot_range = np.linspace(min(x_data), max(x_data), 400)
    
    y_fit_curve = polynomial_function(x_plot_range, coefficients) # Hitung y untuk kurva regresi
    y_data_fit_points = polynomial_function(np.array(x_data), coefficients) # Hitung y_fit pada titik data x
    r_squared = calculate_r_squared(y_data, y_data_fit_points) # Hitung R-squared

    plt.figure(figsize=(10, 6)) # Buat figure baru
    plt.scatter(x_data, y_data, color='blue', label=f'Titik Data') # Plot titik data asli
    plt.plot(x_plot_range, y_fit_curve, color='red', label=f'Polinomial Hasil Fit (Derajat {degree})\nR² = {r_squared:.4f}') # Plot kurva regresi
    
    plt.title(f'Regresi Polinomial (Derajat {degree})')
    plt.xlabel('Nilai X')
    plt.ylabel('Nilai Y')
    plt.legend() # Tampilkan legenda
    plt.grid(True) # Tampilkan grid
    plt.axhline(0, color='black', linewidth=0.5) # Garis sumbu x
    plt.axvline(0, color='black', linewidth=0.5) # Garis sumbu y

    plot_filename = f"{output_filename_base}_deg{degree}.png" # Nama file output plot
    # Simpan plot di direktori Laporan, satu level di atas direktori skrip (Program/)
    laporan_dir = os.path.join(os.path.dirname(script_dir), "Laporan")
    os.makedirs(laporan_dir, exist_ok=True) # Buat direktori Laporan jika belum ada
    full_plot_path = os.path.join(laporan_dir, os.path.basename(plot_filename))

    try:
        plt.savefig(full_plot_path) # Simpan plot
        print(f"Plot disimpan ke {full_plot_path}")
    except Exception as e:
        print(f"Error saat menyimpan plot {full_plot_path}: {e}")
    plt.close() # Tutup figure untuk membebaskan memori

# Fungsi untuk membuat plot residual
def plot_residuals_chart(x_data, y_data, coefficients, degree, output_filename_base):
    if not x_data: # Jangan buat plot jika tidak ada data x
        return

    y_fit_points = polynomial_function(np.array(x_data), coefficients) # Hitung y_fit pada titik data x
    residuals = calculate_residuals(y_data, y_fit_points) # Hitung residual

    plt.figure(figsize=(10, 6)) # Buat figure baru
    plt.scatter(x_data, residuals, color='green') # Plot residual vs x_data
    plt.axhline(0, color='red', linestyle='--', linewidth=0.8) # Garis horizontal di y=0
    
    plt.title(f'Plot Residual untuk Regresi Polinomial (Derajat {degree})')
    plt.xlabel('Nilai X')
    plt.ylabel('Residual (y_data - y_fit)')
    plt.grid(True) # Tampilkan grid

    plot_filename = f"{output_filename_base}_residuals_deg{degree}.png" # Nama file output plot residual
    laporan_dir = os.path.join(os.path.dirname(script_dir), "Laporan")
    os.makedirs(laporan_dir, exist_ok=True)
    full_plot_path = os.path.join(laporan_dir, os.path.basename(plot_filename))
    
    try:
        plt.savefig(full_plot_path) # Simpan plot
        print(f"Plot disimpan ke {full_plot_path}")
    except Exception as e:
        print(f"Error saat menyimpan plot {full_plot_path}: {e}")
    plt.close() # Tutup figure

# Fungsi untuk membuat plot perbandingan beberapa derajat polinomial
def plot_comparative_fit(x_data, y_data, degrees_to_compare, output_filename_base):
    plt.figure(figsize=(12, 7)) # Buat figure baru
    plt.scatter(x_data, y_data, color='blue', label='Titik Data', s=30, alpha=0.6) # Plot titik data asli

    if not x_data: # Jika tidak ada data x, buat rentang default
        x_plot_range = np.linspace(0, 1, 100)
    else: # Buat rentang x untuk plot dari min hingga max data x
        x_plot_range = np.linspace(min(x_data), max(x_data), 400)

    colors = ['red', 'green', 'purple', 'orange', 'brown', 'pink'] # Daftar warna untuk kurva

    for i, degree in enumerate(degrees_to_compare): # Iterasi untuk setiap derajat yang akan dibandingkan
        coeff_filename_base = f"coefficients_deg{degree}.txt" # Nama file koefisien
        # Coba baca file koefisien dari direktori induk (root proyek), lalu dari direktori saat ini (Program/)
        path_in_parent = os.path.join(os.path.dirname(script_dir), coeff_filename_base)
        path_in_current = os.path.join(script_dir, coeff_filename_base)

        coeffs_to_try = path_in_parent
        if not os.path.exists(coeffs_to_try):
            print(f"File {path_in_parent} tidak ditemukan, mencoba {path_in_current}")
            coeffs_to_try = path_in_current
        
        print(f"Plot perbandingan: Membaca koefisien untuk derajat {degree} dari {coeffs_to_try}")
        coefficients = read_coefficients(coeffs_to_try) # Baca koefisien
        
        if coefficients is None: # Jika file koefisien tidak ditemukan, lewati derajat ini
            print(f"Melewati derajat {degree} dalam plot perbandingan (file koefisien tidak ditemukan di {path_in_parent} atau {path_in_current}).")
            continue
        
        y_fit_curve = polynomial_function(x_plot_range, coefficients) # Hitung y untuk kurva regresi
        y_data_fit_points = polynomial_function(np.array(x_data), coefficients) # Hitung y_fit pada titik data x
        r_squared = calculate_r_squared(y_data, y_data_fit_points) # Hitung R-squared
        plt.plot(x_plot_range, y_fit_curve, color=colors[i % len(colors)], label=f'Derajat {degree} (R²={r_squared:.3f})') # Plot kurva

    plt.title('Perbandingan Hasil Regresi Polinomial')
    plt.xlabel('Nilai X')
    plt.ylabel('Nilai Y')
    plt.legend(loc='best') # Tampilkan legenda di lokasi terbaik
    plt.grid(True) # Tampilkan grid
    plt.axhline(0, color='black', linewidth=0.5) # Garis sumbu x
    plt.axvline(0, color='black', linewidth=0.5) # Garis sumbu y
    
    degrees_str = '_'.join(map(str, degrees_to_compare)) # String untuk nama file dari daftar derajat
    plot_filename = f"{output_filename_base}_comparative_deg{degrees_str}.png" # Nama file output plot perbandingan
    laporan_dir = os.path.join(os.path.dirname(script_dir), "Laporan")
    os.makedirs(laporan_dir, exist_ok=True)
    full_plot_path = os.path.join(laporan_dir, os.path.basename(plot_filename))

    try:
        plt.savefig(full_plot_path) # Simpan plot
        print(f"Plot disimpan ke {full_plot_path}")
    except Exception as e:
        print(f"Error saat menyimpan plot {full_plot_path}: {e}")
    plt.close() # Tutup figure

# Direktori skrip global untuk resolusi path. Ini penting.
# __file__ adalah path ke skrip Python saat ini.
# os.path.abspath(__file__) memberikan path absolut ke skrip.
# os.path.dirname(...) mendapatkan direktori dari path tersebut.
script_dir = os.path.dirname(os.path.abspath(__file__))

def main():
    # Setup parser argumen command-line
    parser = argparse.ArgumentParser(description="Plot hasil regresi polinomial.")
    parser.add_argument("degree", type=int, nargs='?', default=2,
                        help="Derajat polinomial untuk plot hasil (default: 2).")
    parser.add_argument("--compare", nargs='+', type=int, default=[1, 2, 3, 4],
                        help="Daftar derajat untuk dibandingkan dalam satu plot. Pastikan program C++ telah dijalankan untuk derajat-derajat ini.")
    
    args = parser.parse_args() # Parse argumen
    target_degree = args.degree # Derajat target untuk plot individual dan residual
    degrees_to_compare = args.compare # Daftar derajat untuk plot perbandingan

    # Skrip Python ini berada di Program/, jadi script_dir adalah Program/
    # File data juga diharapkan berada di Program/
    data_file = "data.txt" 
    output_plot_base_name = "polynomial_regression" # Nama dasar untuk file plot output

    x_data, y_data = read_data_points(data_file) # Baca data (read_data_points menggunakan script_dir global)
    if x_data is None or y_data is None:
        print("Keluar karena error saat membaca titik data.")
        return

    # --- Plot untuk target_degree (plot individual dan residual) ---
    coeff_filename_target_base = f"coefficients_deg{target_degree}.txt" # Nama file koefisien target
    # Coba baca file koefisien dari direktori induk (root proyek), lalu dari direktori saat ini (Program/)
    path_in_parent_target = os.path.join(os.path.dirname(script_dir), coeff_filename_target_base)
    path_in_current_target = os.path.join(script_dir, coeff_filename_target_base)

    coeffs_to_try_target = path_in_parent_target
    if not os.path.exists(coeffs_to_try_target):
        print(f"File {path_in_parent_target} tidak ditemukan, mencoba {path_in_current_target}")
        coeffs_to_try_target = path_in_current_target
    
    print(f"Plot tunggal: Membaca koefisien untuk derajat {target_degree} dari {coeffs_to_try_target}")
    coefficients_target = read_coefficients(coeffs_to_try_target) # Baca koefisien target

    if coefficients_target is None:
        print(f"Koefisien untuk derajat {target_degree} tidak ditemukan. Tidak dapat menghasilkan plot individual untuk derajat ini.")
        print(f"Pastikan program C++ telah dijalankan dan file 'coefficients_deg{target_degree}.txt' ada di root proyek atau direktori Program/.")
    else:
        print(f"Titik data dibaca: {len(x_data)}")
        print(f"Koefisien untuk derajat {target_degree} dibaca: {coefficients_target}")
        # Buat plot regresi tunggal
        plot_single_degree_fit(x_data, y_data, coefficients_target, target_degree, output_plot_base_name)
        # Buat plot residual
        plot_residuals_chart(x_data, y_data, coefficients_target, target_degree, output_plot_base_name)

    # --- Plot perbandingan untuk degrees_to_compare ---
    print(f"\nMencoba menghasilkan plot perbandingan untuk derajat: {degrees_to_compare}")
    plot_comparative_fit(x_data, y_data, degrees_to_compare, output_plot_base_name)
    
    print("\nSkrip Python selesai.")

if __name__ == "__main__":
    # Tidak menggunakan os.chdir di sini, script_dir digunakan untuk semua konstruksi path relatif
    main()
