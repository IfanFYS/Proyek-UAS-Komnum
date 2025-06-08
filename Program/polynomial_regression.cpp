#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <string> // Diperlukan untuk std::string, std::to_string

// Struktur untuk menyimpan titik data (x, y)
struct DataPoint {
    double x; // Nilai variabel independen
    double y; // Nilai variabel dependen
};

// Fungsi untuk mendapatkan direktori dari path file executable
// Berguna untuk menyimpan file output di lokasi yang sama dengan program
std::string getExecutableDir(const std::string& executable_path) {
    size_t last_slash_idx = executable_path.rfind('/'); // Cari slash terakhir (untuk path Linux/macOS)
    if (std::string::npos == last_slash_idx) {
        last_slash_idx = executable_path.rfind('\\'); // Jika tidak ada, cari backslash (untuk path Windows)
    }
    if (std::string::npos != last_slash_idx) {
        return executable_path.substr(0, last_slash_idx + 1); // Kembalikan path direktori termasuk slash/backslash terakhir
    }
    return ""; // Jika tidak ada pemisah path, kembalikan string kosong (mungkin CWD atau hanya nama exe)
}

// Fungsi untuk membaca data dari file dengan path lengkap yang diberikan
std::vector<DataPoint> readDataFromFullPath(const std::string& full_path_to_data) {
    std::vector<DataPoint> data; // Vektor untuk menyimpan titik-titik data
    std::cout << "Mencoba membaca data dari path lengkap: " << full_path_to_data << std::endl;
    std::ifstream file(full_path_to_data); // Buka file input
    if (!file.is_open()) { // Periksa apakah file berhasil dibuka
        std::cerr << "Error: Tidak dapat membuka file data " << full_path_to_data << std::endl;
        return data; // Kembalikan vektor kosong jika gagal
    }
    DataPoint p; // Variabel sementara untuk menyimpan satu titik data
    while (file >> p.x >> p.y) { // Baca nilai x dan y dari setiap baris
        data.push_back(p); // Tambahkan titik data ke vektor
    }
    file.close(); // Tutup file setelah selesai membaca
    if (!data.empty()) {
        std::cout << "Berhasil membaca data dari: " << full_path_to_data << std::endl;
    }
    return data; // Kembalikan vektor berisi data
}

// Fungsi untuk mencetak matriks (untuk keperluan debugging)
void printMatrix(const std::vector<std::vector<double>>& matrix) {
    for (const auto& row : matrix) { // Iterasi melalui setiap baris
        for (double val : row) { // Iterasi melalui setiap elemen dalam baris
            std::cout << std::setw(12) << std::fixed << std::setprecision(4) << val << " "; // Cetak elemen dengan format
        }
        std::cout << std::endl; // Pindah ke baris baru setelah satu baris selesai dicetak
    }
}

// Fungsi untuk mencetak vektor (untuk keperluan debugging)
void printVector(const std::vector<double>& vec) {
    for (double val : vec) { // Iterasi melalui setiap elemen dalam vektor
        std::cout << std::setw(12) << std::fixed << std::setprecision(4) << val << " "; // Cetak elemen dengan format
    }
    std::cout << std::endl; // Pindah ke baris baru setelah vektor selesai dicetak
}

// Fungsi untuk melakukan eliminasi Gauss untuk menyelesaikan sistem persamaan linear Ax = B
// Mengembalikan vektor solusi x
std::vector<double> gaussianElimination(std::vector<std::vector<double>> A, std::vector<double> B) {
    int n = B.size(); // Ukuran sistem (jumlah persamaan atau variabel)

    // Proses eliminasi maju (forward elimination)
    for (int i = 0; i < n; ++i) {
        // Pivoting parsial: cari baris dengan elemen pivot terbesar (nilai absolut)
        int maxRow = i;
        for (int k = i + 1; k < n; ++k) {
            if (std::abs(A[k][i]) > std::abs(A[maxRow][i])) {
                maxRow = k;
            }
        }
        // Tukar baris saat ini dengan baris yang memiliki pivot terbesar
        std::swap(A[i], A[maxRow]);
        std::swap(B[i], B[maxRow]);

        // Normalisasi baris pivot: bagi seluruh baris dengan elemen pivot
        double pivot_val = A[i][i];
        if (std::abs(pivot_val) < 1e-9) { // Periksa apakah pivot terlalu kecil (matriks singular)
             std::cerr << "Error: Matriks bersifat singular atau mendekati singular." << std::endl;
             return {}; // Kembalikan vektor kosong jika matriks singular
        }
        for (int j = i; j < n; ++j) {
            A[i][j] /= pivot_val;
        }
        B[i] /= pivot_val;

        // Eliminasi elemen di bawah pivot pada kolom saat ini
        for (int k = 0; k < n; ++k) {
            if (k != i) { // Untuk semua baris lain (kecuali baris pivot)
                double factor = A[k][i]; // Faktor pengali
                for (int j = i; j < n; ++j) { // Kurangkan (faktor * baris pivot) dari baris k
                    A[k][j] -= factor * A[i][j];
                }
                B[k] -= factor * B[i]; // Lakukan hal yang sama untuk vektor B
            }
        }
    }
    // Pada titik ini, matriks A seharusnya menjadi matriks identitas (atau mendekati)
    // dan vektor B berisi solusi
    return B; // Kembalikan vektor B yang kini berisi solusi x
}

// Fungsi untuk melakukan regresi polinomial
// Menerima vektor titik data dan derajat polinomial yang diinginkan
// Mengembalikan vektor koefisien polinomial (a0, a1, ..., an)
std::vector<double> polynomialRegression(const std::vector<DataPoint>& data, int degree) {
    int n_points = data.size();       // Jumlah titik data
    int m_coeffs = degree + 1;      // Jumlah koefisien (derajat + 1)

    // Pemeriksaan validitas input
    if (n_points == 0) { 
        std::cerr << "Error: Tidak ada titik data." << std::endl; 
        return {}; // Kembalikan vektor kosong jika tidak ada data
    }
    if (degree < 0) { 
        std::cerr << "Error: Derajat polinomial harus non-negatif." << std::endl; 
        return {}; // Kembalikan vektor kosong jika derajat negatif
    }
    if (n_points < m_coeffs) { 
        std::cerr << "Error: Jumlah titik data tidak cukup untuk derajat polinomial " << degree << std::endl; 
        return {}; // Kembalikan vektor kosong jika data tidak cukup
    }

    // Matriks SumX (X^T * X) berukuran (m_coeffs x m_coeffs)
    std::vector<std::vector<double>> SumX(m_coeffs, std::vector<double>(m_coeffs, 0.0));
    // Vektor SumXY (X^T * Y) berukuran (m_coeffs x 1)
    std::vector<double> SumXY(m_coeffs, 0.0);
    
    // Vektor untuk menyimpan jumlah dari x^k (sigma x_i^k)
    // Ukurannya 2*degree + 1 karena elemen terbesar di SumX adalah sigma x_i^(2*degree)
    std::vector<double> x_powers_sum(2 * degree + 1, 0.0);

    // Hitung sigma x_i^k untuk k dari 0 hingga 2*degree
    for (const auto& p : data) { // Iterasi melalui setiap titik data
        for (int j = 0; j <= 2 * degree; ++j) {
            x_powers_sum[j] += std::pow(p.x, j); // Akumulasi x^j
        }
    }

    // Bentuk matriks SumX (matriks normal equations)
    // SumX[i][j] = sigma x_k^(i+j)
    for (int i = 0; i < m_coeffs; ++i) {
        for (int j = 0; j < m_coeffs; ++j) {
            SumX[i][j] = x_powers_sum[i + j];
        }
    }

    // Bentuk vektor SumXY (vektor sisi kanan normal equations)
    // SumXY[i] = sigma (y_k * x_k^i)
    for (const auto& p : data) { // Iterasi melalui setiap titik data
        for (int i = 0; i < m_coeffs; ++i) {
            SumXY[i] += p.y * std::pow(p.x, i); // Akumulasi y * x^i
        }
    }

    // Cetak matriks dan vektor normal equations (untuk debugging)
    std::cout << "\nMatriks Normal Equations (SumX) untuk derajat " << degree << ":" << std::endl;
    printMatrix(SumX);
    std::cout << "Vektor Normal Equations (SumXY) untuk derajat " << degree << ":" << std::endl;
    printVector(SumXY);

    // Selesaikan sistem SumX * A = SumXY menggunakan eliminasi Gauss untuk mendapatkan koefisien A
    return gaussianElimination(SumX, SumXY);
}

// Fungsi utama program
int main(int argc, char* argv[]) {
    // Periksa apakah argumen command-line yang diperlukan diberikan
    if (argc < 3) {
        std::cerr << "Penggunaan: " << (argc > 0 ? argv[0] : "polynomial_regression") 
                  << " <derajat_polinomial> <path_lengkap_ke_file_data>" << std::endl;
        std::cerr << "Contoh: ./polyreg.exe 2 \"C:/path/ke/data.txt\"" << std::endl;
        return 1; // Keluar dengan kode error jika argumen tidak cukup
    }

    int polynomialDegree; // Variabel untuk menyimpan derajat polinomial
    std::string dataFileFullPath; // Variabel untuk menyimpan path lengkap file data
    std::string executableDir = ""; // Variabel untuk menyimpan direktori file executable

    // Dapatkan direktori tempat file executable dijalankan
    if (argc > 0 && argv[0] != nullptr) {
        executableDir = getExecutableDir(argv[0]);
    }
    std::cout << "Direktori executable ditentukan sebagai: " << executableDir << std::endl;

    // Parse argumen derajat polinomial dari command-line
    try {
        polynomialDegree = std::stoi(argv[1]); // Konversi argumen pertama ke integer
        if (polynomialDegree < 0) { // Periksa apakah derajat valid
            std::cerr << "Error: Derajat polinomial harus non-negatif. Diberikan: " << argv[1] << std::endl;
            return 1;
        }
    } catch (const std::invalid_argument& ia) { // Tangani jika argumen tidak valid
        std::cerr << "Argumen tidak valid untuk derajat polinomial: " << argv[1] << std::endl;
        return 1;
    } catch (const std::out_of_range& oor) { // Tangani jika argumen di luar jangkauan
        std::cerr << "Argumen untuk derajat polinomial di luar jangkauan: " << argv[1] << std::endl;
        return 1;
    }

    // Ambil path lengkap file data dari argumen command-line kedua
    dataFileFullPath = argv[2];
    std::cout << "Menggunakan Derajat Polinomial: " << polynomialDegree << std::endl;
    std::cout << "Path file data: " << dataFileFullPath << std::endl;

    // Baca data dari file
    std::vector<DataPoint> data = readDataFromFullPath(dataFileFullPath);

    // Periksa apakah data berhasil dibaca
    if (data.empty()) {
        std::cerr << "Keluar karena error saat memuat data." << std::endl;
        return 1; // Keluar jika tidak ada data yang dibaca
    }

    std::cout << "Jumlah titik data yang dibaca: " << data.size() << std::endl;

    // Lakukan regresi polinomial
    std::vector<double> coefficients = polynomialRegression(data, polynomialDegree);

    // Periksa apakah koefisien berhasil dihitung
    if (!coefficients.empty()) {
        std::cout << "\nKoefisien Polinomial yang Dihitung (a0, ..., an) untuk derajat " << polynomialDegree << ":" << std::endl;
        for (size_t i = 0; i < coefficients.size(); ++i) {
            std::cout << "a" << i << ": " << std::fixed << std::setprecision(6) << coefficients[i] << std::endl; // Cetak koefisien
        }

        // Tentukan nama file untuk menyimpan koefisien
        std::string coeffFilenameBase = "coefficients_deg" + std::to_string(polynomialDegree) + ".txt";
        // Simpan file koefisien di direktori yang sama dengan file executable
        std::string coeffFileFullPath = executableDir + coeffFilenameBase; 

        // Buka file untuk menulis koefisien
        std::ofstream coeffFile(coeffFileFullPath);
        if (coeffFile.is_open()) { // Periksa apakah file berhasil dibuka
            for (double coeff : coefficients) {
                coeffFile << std::fixed << std::setprecision(15) << coeff << std::endl; // Tulis setiap koefisien ke file
            }
            coeffFile.close(); // Tutup file
            std::cout << "\nKoefisien disimpan ke " << coeffFileFullPath << std::endl;
        } else {
            std::cerr << "Error: Tidak dapat membuka " << coeffFileFullPath << " untuk ditulis." << std::endl;
            // Jika gagal menyimpan di direktori executable (misalnya karena masalah izin),
            // coba simpan di Current Working Directory (CWD) sebagai fallback.
            std::cerr << "Mencoba menyimpan ke CWD: " << coeffFilenameBase << std::endl;
            std::ofstream coeffFileCWD(coeffFilenameBase); // Buka file di CWD
            if (coeffFileCWD.is_open()) {
                 for (double coeff : coefficients) {
                    coeffFileCWD << std::fixed << std::setprecision(15) << coeff << std::endl;
                }
                coeffFileCWD.close();
                std::cout << "\nKoefisien disimpan ke " << coeffFilenameBase << " (di CWD sebagai fallback)" << std::endl;
            } else {
                std::cerr << "Error: Tidak dapat membuka " << coeffFilenameBase << " untuk ditulis di CWD juga." << std::endl;
            }
        }
    } else {
        std::cerr << "Regresi polinomial gagal untuk derajat " << polynomialDegree << "." << std::endl;
        return 1; // Keluar jika regresi gagal
    }

    return 0; // Program selesai dengan sukses
}