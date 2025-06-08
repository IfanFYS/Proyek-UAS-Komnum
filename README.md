# Implementasi Regresi Polinomial

## Deskripsi Singkat
Proyek ini bertujuan untuk mengimplementasikan algoritma regresi polinomial menggunakan bahasa C++ untuk analisis data. Regresi polinomial adalah sebuah metode dalam statistika dan pembelajaran mesin yang digunakan untuk memodelkan hubungan antara variabel independen (x) dan variabel dependen (y) sebagai polinomial derajat ke-n. Program C++ akan membaca data dari file, menghitung koefisien polinomial menggunakan metode *normal equations* yang diselesaikan dengan eliminasi Gauss, dan menyimpan koefisien tersebut. Selanjutnya, sebuah skrip Python digunakan untuk memvisualisasikan data asli dan kurva polinomial yang dihasilkan, memberikan representasi grafis dari kecocokan model.

Proyek ini merupakan bagian dari Ujian Akhir Semester (UAS) mata kuliah Komputasi Numerik.

## Struktur Direktori
```
.
├── Laporan/
│   ├── report.tex             # File source LaTeX untuk laporan
│   ├── report.pdf             # File PDF laporan (dihasilkan dari kompilasi .tex)
│   ├── polynomial_regression_degN.png # Contoh plot hasil regresi
│   └── ...                    # Plot-plot lain yang dihasilkan
├── Program/
│   ├── polynomial_regression.cpp # Kode sumber C++ untuk regresi polinomial
│   ├── plot_regression.py     # Skrip Python untuk visualisasi
│   ├── data.txt               # Contoh file data input
│   └── polyreg.exe            # (Opsional) File executable C++ setelah kompilasi
├── coefficients_degN.txt      # File output koefisien dari C++ (disimpan di root)
└── README.md                  # File ini
```

## Cara Kompilasi dan Menjalankan Program C++

### Kompilasi
Program C++ (`polynomial_regression.cpp`) dapat dikompilasi menggunakan kompiler C++ seperti g++. Pastikan Anda berada di direktori `Program/` atau sesuaikan path.

Contoh perintah kompilasi (misalnya, menggunakan g++):
```bash
g++ polynomial_regression.cpp -o polyreg -std=c++11
```
Perintah di atas akan menghasilkan file executable bernama `polyreg` (atau `polyreg.exe` di Windows) di dalam direktori `Program/`.

### Menjalankan Program C++
Setelah kompilasi, program C++ dapat dijalankan dari terminal. Program ini membutuhkan dua argumen command-line:
1.  `<derajat_polinomial>`: Integer non-negatif yang menentukan derajat polinomial yang akan dicocokkan.
2.  `<path_lengkap_ke_file_data>`: String path absolut menuju file data (misalnya, `data.txt`).

Contoh perintah menjalankan program (dari direktori root proyek, jika executable ada di `Program/`):
```bash
# Untuk Linux/macOS
./Program/polyreg 2 "/path/absolut/ke/Proyek-UAS-Komnum/Program/data.txt"

# Untuk Windows (misalnya, jika Anda menggunakan Git Bash atau PowerShell)
./Program/polyreg.exe 2 "C:/path/absolut/ke/Proyek-UAS-Komnum/Program/data.txt"
```
Gantilah `"/path/absolut/ke/"` dengan path absolut yang sesuai di sistem Anda menuju direktori `Proyek-UAS-Komnum/Program/data.txt`.

Program akan mencetak matriks normal equations, vektor sisi kanan, dan koefisien yang dihitung ke konsol. Koefisien juga akan disimpan dalam file teks.

## Cara Menjalankan Skrip Python

### Dependensi
Skrip Python (`plot_regression.py`) memerlukan pustaka berikut:
*   `matplotlib`
*   `numpy`
*   `argparse` (biasanya sudah termasuk dalam instalasi Python standar)

Anda dapat menginstalnya menggunakan pip:
```bash
pip install matplotlib numpy
```

### Menjalankan Skrip Python
Skrip Python dijalankan dari terminal dan berada di direktori `Program/`. Skrip ini akan membaca file data (`Program/data.txt`) dan file koefisien yang dihasilkan oleh program C++ (misalnya, `coefficients_deg2.txt` yang diharapkan berada di direktori root proyek atau di direktori `Program/`).

Skrip menerima argumen opsional:
1.  `degree` (posisional, opsional): Derajat polinomial untuk plot tunggal dan plot residual. Defaultnya adalah `2`.
2.  `--compare` (opsional): Daftar satu atau lebih derajat polinomial yang akan dibandingkan dalam satu plot. Defaultnya adalah `1 2 3 4`.

Contoh perintah menjalankan skrip (dari direktori root proyek):
```bash
# Menjalankan dengan default (plot tunggal & residual untuk derajat 2, perbandingan untuk derajat 1,2,3,4)
python Program/plot_regression.py

# Menjalankan untuk plot tunggal & residual derajat 3, dan perbandingan default
python Program/plot_regression.py 3

# Menjalankan untuk plot tunggal & residual derajat 2, dan perbandingan untuk derajat 1,2,5
python Program/plot_regression.py --compare 1 2 5

# Menjalankan untuk plot tunggal & residual derajat 3, dan perbandingan untuk derajat 1,3,4
python Program/plot_regression.py 3 --compare 1 3 4
```
Pastikan file koefisien (`coefficients_degN.txt`) yang sesuai dengan derajat yang diminta sudah ada (dihasilkan oleh program C++). Plot akan disimpan di direktori `Laporan/`.

## Format File Data
File data (misalnya, `Program/data.txt`) harus berisi pasangan nilai x dan y per baris, dipisahkan oleh spasi.
Contoh:
```
0.0 1.1
0.5 1.8
1.0 2.7
...
```

## Output Program

### Program C++
*   **Konsol**: Mencetak matriks normal equations, vektor sisi kanan, dan koefisien yang dihitung.
*   **File Koefisien**: Membuat file teks bernama `coefficients_degN.txt` (misalnya, `coefficients_deg2.txt` untuk derajat 2) di direktori **root proyek** (jika direktori executable dapat ditentukan dan memiliki izin tulis) atau di **Current Working Directory (CWD)** sebagai fallback. File ini berisi koefisien polinomial $a_0, a_1, \dots, a_n$, masing-masing pada baris baru.

### Skrip Python
*   **Konsol**: Mencetak informasi tentang file yang dibaca dan plot yang disimpan.
*   **File Plot**: Menghasilkan file gambar `.png` di direktori `Laporan/`:
    *   `polynomial_regression_degN.png`: Plot data asli dan kurva regresi polinomial derajat N.
    *   `polynomial_regression_residuals_degN.png`: Plot residual untuk regresi derajat N.
    *   `polynomial_regression_comparative_degX_Y_Z.png`: Plot perbandingan beberapa kurva regresi (derajat X, Y, Z).

## Kontributor
*   **Nama**: Fathan Yazid Satriani
*   **NPM**: 2306250560

## Link Tambahan
*   **Repositori GitHub**: [https://github.com/IfanFYS/Proyek-UAS-Komnum](https://github.com/IfanFYS/Proyek-UAS-Komnum)
*   **Video Demonstrasi YouTube**: [PASTIKAN UNTUK MENGISI LINK YOUTUBE ANDA DI SINI]
