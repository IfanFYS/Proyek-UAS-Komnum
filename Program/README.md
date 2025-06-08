# Proyek UAS Komputasi Numerik: Regresi Polinomial

Proyek ini mengimplementasikan regresi polinomial menggunakan C++ untuk analisis data eksperimental dan Python untuk visualisasi.

## Struktur Direktori Proyek Utama

```
Tugas Proyek UAS/
├── Laporan/
│   ├── report.tex
│   ├── report.pdf (dihasilkan setelah kompilasi report.tex)
│   ├── polynomial_regression_deg2.png
│   ├── polynomial_regression_residuals_deg2.png
│   └── polynomial_regression_comparative_deg1_2_3_4.png
├── Program/
│   ├── polynomial_regression.cpp
│   ├── plot_regression.py
│   ├── data.txt
│   └── README.md (file ini)
├── coefficients_deg1.txt (dihasilkan oleh C++ executable)
├── coefficients_deg2.txt (dihasilkan oleh C++ executable)
├── coefficients_deg3.txt (dihasilkan oleh C++ executable)
├── coefficients_deg4.txt (dihasilkan oleh C++ executable)
└── polynomial_regression.exe (atau nama executable lain setelah kompilasi C++)
```

## Kompilasi Program C++

Program C++ (`polynomial_regression.cpp`) dapat dikompilasi menggunakan g++. Pastikan Anda berada di direktori `Program/` atau sesuaikan path.

```bash
g++ polynomial_regression.cpp -o ../polynomial_regression
```
Perintah di atas akan menghasilkan file executable bernama `polynomial_regression.exe` (atau `polynomial_regression` di Linux/macOS) di direktori root proyek (`Tugas Proyek UAS/`).

## Menjalankan Program

1.  **Jalankan Program C++:**
    Pastikan file `Program/data.txt` ada dan berisi data input. Dari direktori root proyek (`Tugas Proyek UAS/`), jalankan:
    ```bash
    ./polynomial_regression
    ```
    atau jika di Windows:
    ```bash
    .\polynomial_regression.exe
    ```
    Program akan membaca data dari `Program/data.txt` dan menghasilkan file koefisien (misalnya, `coefficients_deg2.txt`) di direktori root proyek. Program ini secara default akan menghitung untuk derajat 1, 2, 3, dan 4, dan menyimpan masing-masing ke `coefficients_deg1.txt`, `coefficients_deg2.txt`, dst.

2.  **Jalankan Skrip Python untuk Visualisasi:**
    Pastikan Anda memiliki Python dan pustaka `matplotlib` serta `scikit-learn` (untuk R-squared) terinstal.
    ```bash
    pip install matplotlib scikit-learn numpy
    ```
    Dari direktori `Program/`, jalankan skrip Python:
    ```bash
    python plot_regression.py
    ```
    Skrip ini akan:
    *   Membaca data dari `Program/data.txt`.
    *   Membaca koefisien dari file `coefficients_degN.txt` yang ada di direktori root proyek (satu tingkat di atas direktori `Program/`).
    *   Menghasilkan plot dan menyimpannya di direktori `Laporan/` (dua tingkat di atas direktori `Program/`, lalu masuk ke `Laporan/`).
        *   `Laporan/polynomial_regression_deg2.png`
        *   `Laporan/polynomial_regression_residuals_deg2.png`
        *   `Laporan/polynomial_regression_comparative_deg1_2_3_4.png`

    **Catatan Penting Path:**
    *   Program C++ (`polynomial_regression.exe` yang dijalankan dari root) mencari `Program/data.txt` dan menulis `coefficients_degN.txt` ke root.
    *   Skrip Python (`plot_regression.py` yang dijalankan dari `Program/`) mencari `data.txt` di direktori yang sama (`Program/`), mencari `../coefficients_degN.txt` (di root), dan menyimpan gambar ke `../Laporan/`.

## Data Input

File `Program/data.txt` harus berisi pasangan nilai x dan y, dipisahkan oleh spasi, satu pasangan per baris. Contoh:
```
0.0 1.1
0.5 1.8
1.0 2.7
...
```

## Repositori GitHub

Kode sumber dan detail proyek ini dapat ditemukan di repositori GitHub berikut:
[https://github.com/IfanFYS/Proyek-UAS-Komnum](https://github.com/IfanFYS/Proyek-UAS-Komnum)

## Laporan LaTeX

Laporan proyek (`Laporan/report.tex`) dapat dikompilasi menggunakan distribusi LaTeX (misalnya, MiKTeX, TeX Live, Overleaf). Pastikan untuk mengkompilasi beberapa kali agar semua referensi silang (gambar, persamaan, sitasi) teratasi dengan benar.
